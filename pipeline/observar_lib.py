"""observar_lib.py — P0X misión OBSERVAR (Bloque B).

Capa de estado en disco para los jobs de destilación YouTube → delta.
Todo el estado vive en pipeline/observar/<job_id>/ — resiliente a reinicios
del gateway y de la cola. Escritura atómica (tmp + os.replace) bajo flock.

Estados: queued → transcribing → delta → pending_review → accepted|discarded
         (+ requeued_thermal, error)
"""
import fcntl
import json
import os
import re
import subprocess
import time
from datetime import datetime, timezone
from pathlib import Path

P0X = Path(os.environ.get("P0X_ROOT", "/mnt/nvme/p0x"))
PIPE = P0X / "pipeline"
OBSERVAR_DIR = PIPE / "observar"
MENTE = P0X / "mente"
NECROPOLIS = MENTE / "necropolis"  # fuera de SCOPE_DIRS de ingest_mente: jamás se indexa
THERMAL = Path("/sys/class/thermal/thermal_zone0/temp")

ESTADOS = {"queued", "transcribing", "delta", "pending_review",
           "accepted", "discarded", "requeued_thermal", "error"}

_YT_RE = re.compile(
    r"(?:youtube\.com/(?:watch\?(?:.*&)?v=|shorts/|live/|embed/)|youtu\.be/)"
    r"([A-Za-z0-9_-]{11})")


def utcnow() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def leer_temp_c() -> float | None:
    try:
        return int(THERMAL.read_text().strip()) / 1000.0
    except (OSError, ValueError):
        return None  # sin sensor no hay guard, pero jamás se inventa un valor


def resolve_video_id(url: str) -> str | None:
    m = _YT_RE.search(url)
    if m:
        return m.group(1)
    try:
        r = subprocess.run(
            ["yt-dlp", "--no-playlist", "--skip-download", "--print", "id", url],
            capture_output=True, text=True, timeout=60, check=True)
        vid = (r.stdout.strip().splitlines() or [""])[0]
        return vid or None
    except (subprocess.SubprocessError, OSError):
        return None


def transcript_path(video_id: str) -> Path | None:
    """Transcript ya existente (cache): corpus/ primero, luego pipeline/out/."""
    for base in (P0X / "corpus" / video_id, PIPE / "out" / video_id):
        for name in ("transcript.txt", "transcript.json"):
            p = base / name
            if p.exists():
                return p
    return None


def job_dir(job_id: str) -> Path:
    if not re.fullmatch(r"[A-Za-z0-9_-]{1,80}", job_id):
        raise ValueError(f"job_id inválido: {job_id!r}")
    return OBSERVAR_DIR / job_id


def _atomic_write(path: Path, data: str) -> None:
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(data, encoding="utf-8")
    os.replace(tmp, path)


def _with_lock(d: Path):
    lock = d / ".lock"
    fh = open(lock, "w", encoding="utf-8")
    fcntl.flock(fh, fcntl.LOCK_EX)
    return fh


def crear_job(url: str, comentario: str, video_id: str,
              transcript_cached: bool) -> dict:
    ts = datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S")
    job_id = f"{video_id}-{ts}"
    d = job_dir(job_id)
    d.mkdir(parents=True, exist_ok=False)
    state = {
        "job_id": job_id, "url": url, "video_id": video_id,
        "comentario": comentario, "state": "queued",
        "transcript_cached": transcript_cached,
        "requeues_thermal": 0,
        "created_at": utcnow(), "updated_at": utcnow(),
        "history": [{"ts": utcnow(), "state": "queued",
                     "temp_c": leer_temp_c()}],
    }
    _atomic_write(d / "state.json", json.dumps(state, ensure_ascii=False, indent=2))
    return state


def leer_state(job_id: str) -> dict | None:
    p = job_dir(job_id) / "state.json"
    if not p.exists():
        return None
    return json.loads(p.read_text(encoding="utf-8"))


def transicion(job_id: str, nuevo: str, **extra) -> dict:
    if nuevo not in ESTADOS:
        raise ValueError(f"estado desconocido: {nuevo}")
    d = job_dir(job_id)
    fh = _with_lock(d)
    try:
        state = json.loads((d / "state.json").read_text(encoding="utf-8"))
        state["state"] = nuevo
        state["updated_at"] = utcnow()
        state.update(extra)
        state["history"].append(
            {"ts": utcnow(), "state": nuevo, "temp_c": leer_temp_c(),
             **({k: v for k, v in extra.items() if k in
                 ("motivo", "error", "fase")})})
        _atomic_write(d / "state.json",
                      json.dumps(state, ensure_ascii=False, indent=2))
        return state
    finally:
        fcntl.flock(fh, fcntl.LOCK_UN)
        fh.close()


def listar_jobs(estado: str | None = None) -> list[dict]:
    out = []
    if not OBSERVAR_DIR.exists():
        return out
    for d in sorted(OBSERVAR_DIR.iterdir()):
        p = d / "state.json"
        if not p.is_file():
            continue
        try:
            s = json.loads(p.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            continue
        if estado and s.get("state") != estado:
            continue
        # stale: >2h sin transición en un estado no terminal
        try:
            upd = datetime.fromisoformat(s["updated_at"])
            edad = (datetime.now(timezone.utc) - upd).total_seconds()
        except (KeyError, ValueError):
            edad = None
        s["stale"] = bool(
            edad is not None and edad > 7200 and
            s.get("state") in ("queued", "transcribing", "delta"))
        out.append(s)
    return out


def log_runner(job_id: str, msg: str) -> None:
    with open(job_dir(job_id) / "runner.log", "a", encoding="utf-8") as f:
        f.write(f"{utcnow()} {msg}\n")


def sobre_alfabeto(job_id: str, op: str, dom: str, entrada: dict,
                   out_shape: str, md: str = "pipeline-ingesta@1.0.0") -> None:
    """Sobre del ALFABETO_P0X §3 — una línea JSON por operación del job."""
    sobre = {"v": "alfabeto-p0x@1.0.0", "md": md, "dom": dom, "op": op,
             "in": entrada, "out": out_shape}
    with open(job_dir(job_id) / "alfabeto.jsonl", "a", encoding="utf-8") as f:
        f.write(json.dumps(sobre, ensure_ascii=False) + "\n")


def telemetria_lengua(dom: str, op: str, tok_in: int, tok_out: int,
                      valida: bool, ms: int) -> None:
    """Registro económico obligatorio (ALFABETO_P0X §6) en lengua.jsonl."""
    dest = MENTE / "telemetria"
    dest.mkdir(parents=True, exist_ok=True)
    linea = {"ts": time.time(), "dom": dom, "op": op, "tok_in": tok_in,
             "tok_out": tok_out, "valida": valida, "ms": ms, "alfabeto": True}
    with open(dest / "lengua.jsonl", "a", encoding="utf-8") as f:
        f.write(json.dumps(linea, ensure_ascii=False) + "\n")
