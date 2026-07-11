#!/usr/bin/env python3
"""reflejo_bateria_watch.py — P0X Pista A · Reflejo determinista #1.

Arco espinal: sensor (NUT upsc) -> umbral (OB/LB) -> acción protectora
(tsp -S 0, frena la cola batch) -> evento a consola (Bitácora Live, REFLEX) ->
registro (mente/telemetria/reflejos.jsonl). Con histéresis (rearme tras N
lecturas OL consecutivas) y un solo disparo por episodio.

SIN LLM en el lazo. Proceso AUTÓNOMO: ni el gateway ni Ollama participan. El
Monje NARRA este reflejo post-hoc si se le pregunta; jamás lo ejecuta.

Doctrina: mente/reflejos/reflejo-bateria.md.
Servicio propose-only: deploy/fragua/reflejo-bateria.service (no habilitada).

Uso:
  python3 reflejo_bateria_watch.py                 # watch vivo (sensor real)
  python3 reflejo_bateria_watch.py --once          # una lectura real y sale
  python3 reflejo_bateria_watch.py --test-seq OB,OB,OL,OL,OL   # test vivo
El --test-seq inyecta la secuencia de ups.status en la MISMA máquina de estados;
las acciones REALES sí se ejecutan (tsp/redis/jsonl) — es un test honesto de la
lógica que además dispara los efectos reales.
"""
import argparse
import json
import shutil
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

# Era energética (patrón @sleeping rescatado, arqueología #43): este reflejo es
# @sun_synchronous de facto — protege la UPS porque HOY no hay batería solar.
# Cuando P0X_BATTERY_PRESENT=true, sus umbrales se revisan (ver patrón MD).
sys.path.insert(0, str(Path(__file__).resolve().parent))
from energia_era import ENERGY_ERA  # noqa: E402

# ── Config (honest-sensors: la UPS real del rack) ───────────────────────────
UPS_NAME = "greencell"
POLL_S = 15                       # alineado con NUT pollinterval
REARME_OL_CONSECUTIVAS = 3        # ~45s de OL estable antes de rearmar (anti-parpadeo)
REDIS_HOST, REDIS_PORT = "127.0.0.1", 6379
BITACORA_KEY = "hexelion:bitacora:live"
BITACORA_MAX = 200
REFLEJO = "reflejo-bateria"
TELEMETRIA = Path("/mnt/nvme/p0x/mente/telemetria/reflejos.jsonl")
# Pausa de la cola: `tsp -S 0` NO sirve (task-spooler impone mínimo 1 slot). Se
# usa el patrón idiomático: una COMPUERTA que ocupa el único slot (FIFO) hasta
# que se retira el hold. El job en curso se respeta; lo encolado detrás espera.
HOLD_FILE = "/tmp/reflejo-bateria.hold"
GATE_LABEL = "reflejo-hold"

# Binarios: shutil.which + fallback absoluto (lección PATH-systemd de OPERACIONES:
# los servicios systemd no traen ~/.local/bin ni el PATH interactivo).
UPSC_BIN = shutil.which("upsc") or "/usr/bin/upsc"
TSP_BIN = shutil.which("tsp") or shutil.which("ts") or "/usr/bin/tsp"


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _now_hm() -> str:
    return datetime.now().strftime("%H:%M:%S")


def read_ups(status_override: str | None = None) -> dict:
    """Lee `upsc <ups>` (una llamada trae todas las variables). En modo test,
    status_override reemplaza SOLO ups.status; battery/voltage siguen siendo
    los reales si la UPS responde (contexto honesto para el registro)."""
    data = {"status": None, "battery_charge": None, "input_voltage": None}
    try:
        out = subprocess.run([UPSC_BIN, UPS_NAME], capture_output=True,
                             text=True, timeout=10).stdout
        vals = {}
        for line in out.splitlines():
            if ":" in line:
                k, v = line.split(":", 1)
                vals[k.strip()] = v.strip()
        data["status"] = vals.get("ups.status")
        data["battery_charge"] = vals.get("battery.charge")
        data["input_voltage"] = vals.get("input.voltage")
    except Exception as e:  # sensor caído: honest-sensors, se registra el error
        data["error"] = str(e)
    if status_override is not None:
        data["status"] = status_override
    return data


def is_disparo(status: str | None) -> bool:
    if not status:
        return False
    toks = status.split()
    return "OB" in toks or "LB" in toks


def is_ol(status: str | None) -> bool:
    return bool(status) and "OL" in status.split()


def _gate_viva() -> bool:
    """¿Hay una compuerta reflejo-hold viva (running/queued) en la cola?"""
    try:
        out = subprocess.run([TSP_BIN, "-l"], capture_output=True,
                             text=True, timeout=10).stdout
        return any(GATE_LABEL in ln and ("running" in ln or "queued" in ln)
                   for ln in out.splitlines())
    except Exception:
        return False


def pausar_cola() -> str:
    """Acción protectora: pausa la cola batch. Crea el hold y encola una
    compuerta que ocupa el único slot hasta que el hold desaparezca. Idempotente
    (si el watcher reinició y ya hay compuerta viva, no encola otra)."""
    try:
        Path(HOLD_FILE).touch()
        if not _gate_viva():
            loop = f"while [ -f {HOLD_FILE} ]; do sleep 3; done"
            subprocess.run([TSP_BIN, "-L", GATE_LABEL, "sh", "-c", loop],
                           capture_output=True, timeout=10, check=False)
        return "pausa (compuerta tsp + hold)"
    except Exception as e:
        return f"pausa-fallida:{e}"


def reanudar_cola() -> str:
    """Rearme: retira el hold. La compuerta sale de su bucle (~3s) y libera el
    slot; la cola vuelve a arrancar trabajo."""
    try:
        Path(HOLD_FILE).unlink(missing_ok=True)
        return "reanudada (hold liberado)"
    except Exception as e:
        return f"reanudar-fallida:{e}"


def emit_console(line: str, redis_mod) -> None:
    """Evento a la Bitácora Live (mismo bus/patrón que hexelion_gateway.py:1662).
    El watcher empuja directo a Redis: arco desacoplado del gateway."""
    if redis_mod is None:
        return
    try:
        r = redis_mod.Redis(host=REDIS_HOST, port=REDIS_PORT,
                            decode_responses=True, socket_timeout=3)
        entry = json.dumps({"ts": _now_hm(), "type": "reflex", "line": line},
                           ensure_ascii=False)
        r.lpush(BITACORA_KEY, entry)
        r.ltrim(BITACORA_KEY, 0, BITACORA_MAX - 1)
        r.close()
    except Exception:
        pass


def log_reflejo(disparo: str, valor: dict, accion: str, ms: int) -> dict:
    rec = {"ts": _now_iso(), "reflejo": REFLEJO, "disparo": disparo,
           "valor": valor, "accion": accion, "ms": ms}
    TELEMETRIA.parent.mkdir(parents=True, exist_ok=True)
    with TELEMETRIA.open("a", encoding="utf-8") as f:
        f.write(json.dumps(rec, ensure_ascii=False) + "\n")
    return rec


class Reflejo:
    """Máquina de estados con histéresis. ARMADO (OL) <-> DISPARADO (OB/LB).
    Un solo disparo por episodio; rearme solo tras N lecturas OL consecutivas."""

    def __init__(self, redis_mod):
        self.estado = "ARMADO"
        self.ol_seguidas = 0
        self.redis_mod = redis_mod

    def step(self, reading: dict, t0: float) -> list:
        status = reading.get("status")
        valor = {"status": status,
                 "battery_charge": reading.get("battery_charge"),
                 "input_voltage": reading.get("input_voltage")}
        events = []

        if self.estado == "ARMADO":
            self.ol_seguidas = 0
            if is_disparo(status):
                accion = pausar_cola()
                ms = round((time.monotonic() - t0) * 1000)
                disparo = "LB" if (status and "LB" in status.split()) else "OB"
                line = (f"REFLEX · reflejo-bateria: UPS en batería ({disparo}) "
                        f"→ cola batch en pausa (compuerta tsp)")
                emit_console(line, self.redis_mod)
                rec = log_reflejo(disparo, valor, accion, ms)
                self.estado = "DISPARADO"
                events.append(("DISPARO", line, rec))

        elif self.estado == "DISPARADO":
            if is_ol(status):
                self.ol_seguidas += 1
                if self.ol_seguidas >= REARME_OL_CONSECUTIVAS:
                    accion = reanudar_cola()
                    ms = round((time.monotonic() - t0) * 1000)
                    line = ("REFLEX · reflejo-bateria: red restablecida (OL estable) "
                            "→ cola batch reanudada (hold liberado)")
                    emit_console(line, self.redis_mod)
                    rec = log_reflejo("OL-rearme", valor, accion, ms)
                    self.estado = "ARMADO"
                    self.ol_seguidas = 0
                    events.append(("REARME", line, rec))
            else:
                # sigue OB/LB (o lectura incierta): resetea el contador de OL.
                self.ol_seguidas = 0

        return events


def main() -> None:
    ap = argparse.ArgumentParser(description="Reflejo determinista #1: UPS OB/LB pausa la cola batch.")
    ap.add_argument("--test-seq", help="secuencia de ups.status por comas (p.ej. OB,OB,OL,OL,OL); acciones reales")
    ap.add_argument("--poll", type=float, default=POLL_S, help="segundos entre lecturas (watch vivo)")
    ap.add_argument("--once", action="store_true", help="una lectura real y sale")
    args = ap.parse_args()

    try:
        import redis as redis_mod
    except Exception:
        redis_mod = None
        print("[reflejo-bateria] WARN: módulo redis no disponible — sin evento a consola")

    reflejo = Reflejo(redis_mod)

    if args.test_seq:
        seq = [s.strip() for s in args.test_seq.split(",") if s.strip()]
        print(f"[reflejo-bateria] TEST-SEQ {seq} — acciones REALES (tsp/redis/jsonl)")
        for st in seq:
            t0 = time.monotonic()
            reading = read_ups(status_override=st)
            evs = reflejo.step(reading, t0)
            tag = evs[0][0] if evs else "—"
            print(f"[reflejo-bateria] status={st:<6} estado={reflejo.estado:<10} "
                  f"ol={reflejo.ol_seguidas} evento={tag}")
        return

    print(f"[reflejo-bateria] watch vivo · era={ENERGY_ERA} · upsc {UPS_NAME} · poll {args.poll}s · "
          f"rearme {REARME_OL_CONSECUTIVAS} OL consecutivas · upsc={UPSC_BIN} tsp={TSP_BIN}")
    while True:
        t0 = time.monotonic()
        reading = read_ups()
        reflejo.step(reading, t0)
        if args.once:
            print(f"[reflejo-bateria] lectura: {reading} · estado={reflejo.estado}")
            break
        time.sleep(args.poll)


if __name__ == "__main__":
    main()
