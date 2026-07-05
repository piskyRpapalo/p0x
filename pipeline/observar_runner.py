#!/usr/bin/env python3
"""observar_runner.py — P0X misión OBSERVAR (Bloque B).

Lo que corre tsp: p0x-enqueue python3 observar_runner.py <job_id>

Cadena: (ingest_youtube si falta transcript) → delta_engine → pending_review.
Guard térmico: al inicio, entre fases y cada 10 llamadas LLM (callback);
>80°C → re-encolar (máx 3), estado requeued_thermal. Temps en history.
"""
import subprocess
import sys
from pathlib import Path

PIPE = Path(__file__).resolve().parent
sys.path.insert(0, str(PIPE))

import delta_engine  # noqa: E402
import observar_lib as ol  # noqa: E402

TMAX = 80.0
MAX_REQUEUES = 3
ENQUEUE = PIPE.parent / "bin" / "p0x-enqueue"


class Recalentado(Exception):
    pass


def guard_termico(job_id: str, fase: str) -> None:
    t = ol.leer_temp_c()
    ol.log_runner(job_id, f"guard térmico [{fase}]: zone0={t}°C")
    if t is not None and t > TMAX:
        raise Recalentado(f"{t}°C > {TMAX} en {fase}")


def reencolar(job_id: str, motivo: str) -> int:
    state = ol.leer_state(job_id)
    n = state.get("requeues_thermal", 0) + 1
    if n > MAX_REQUEUES:
        ol.transicion(job_id, "error",
                      error=f"térmico: {MAX_REQUEUES} re-encolados agotados ({motivo})")
        return 1
    ol.transicion(job_id, "requeued_thermal", requeues_thermal=n, motivo=motivo)
    subprocess.run([str(ENQUEUE), "python3", str(PIPE / "observar_runner.py"),
                    job_id], check=False)
    ol.log_runner(job_id, f"re-encolado #{n} por térmica: {motivo}")
    return 0


def asegurar_transcript(job_id: str, state: dict) -> None:
    if ol.transcript_path(state["video_id"]) is not None:
        ol.log_runner(job_id, "transcript en cache — skip ingest_youtube")
        return
    ol.transicion(job_id, "transcribing")
    r = subprocess.run(
        [sys.executable, str(PIPE / "ingest_youtube.py"), state["url"]],
        cwd=str(PIPE), capture_output=True, text=True)
    tail = (r.stdout + r.stderr)[-2000:]
    ol.log_runner(job_id, f"ingest_youtube rc={r.returncode}\n{tail}")
    if r.returncode != 0 or ol.transcript_path(state["video_id"]) is None:
        raise RuntimeError(f"ingest_youtube falló (rc={r.returncode})")


def main() -> int:
    if len(sys.argv) != 2:
        print("uso: observar_runner.py <job_id>")
        return 2
    job_id = sys.argv[1]
    state = ol.leer_state(job_id)
    if state is None:
        print(f"job {job_id} inexistente")
        return 2
    if state["state"] in ("accepted", "discarded"):
        ol.log_runner(job_id, f"estado terminal {state['state']} — nada que hacer")
        return 0
    try:
        guard_termico(job_id, "inicio")
        asegurar_transcript(job_id, state)
        guard_termico(job_id, "post-transcript")
        ol.transicion(job_id, "delta")
        delta_engine.set_thermal_callback(
            lambda: guard_termico(job_id, "cada-10-llamadas"))
        delta_engine.generar_delta(job_id)
        ol.transicion(job_id, "pending_review")
        ol.log_runner(job_id, "listo: pending_review")
        return 0
    except Recalentado as e:
        return reencolar(job_id, str(e))
    except Exception as e:  # noqa: BLE001 — el estado en disco es el contrato
        ol.transicion(job_id, "error", error=str(e)[:500])
        ol.log_runner(job_id, f"ERROR: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
