#!/usr/bin/env python3
"""reflejo_m5_watch.py — P0X Pista A · Reflejos #2 y #3 (hermanos del M5).

Un solo runner, DOS arcos independientes sobre la misma telemetría del M5
(Redis hexelion:telemetry:m5:last, TTL 30s, publicada por el-vigia):

  · reflejo-termico-m5  — BME680 temp_c ≥ 40.0°C → aviso REFLEX.
      Rearme: ≤ 38.0°C sostenido (3 lecturas). Umbral por DATO (2026-07-11):
      baseline medida 30.29 ±0.01°C (18 muestras) → +10°C = anomalía real.
  · reflejo-vibracion   — ADXL345 Δ|g| ≥ 0.25 g → "movimiento detectado".
      Rearme: 3 lecturas seguidas con Δ|g| < 0.10. Umbral por DATO: placa
      quieta Δ|g| máx 0.0615 / media 0.0235 → 0.25 ≈ 4× el máximo en reposo.

SOLO aviso/protección, jamás valor (IronClaw); SIN LLM en el lazo. El sensor
ausente (clave Redis expirada = M5 callado) NO dispara nada: ausencia ≠ dato.
Ambos son @sun_synchronous-neutros (no dependen de la Era energética).

Test vivo (acciones reales a consola/jsonl):
  --test-temp 30,41,42,39,37,37,37   --test-mag 2.31,2.90,2.32,2.31,2.31
Doctrina: mente/reflejos/reflejo-termico-m5.md · reflejo-vibracion.md
Unit PROPUESTA: deploy/fragua/reflejo-m5.service (no habilitada).
"""
import argparse
import json
import time
from datetime import datetime, timezone
from pathlib import Path

REDIS_HOST, REDIS_PORT = "127.0.0.1", 6379
KEY_M5 = "hexelion:telemetry:m5:last"
BITACORA_KEY = "hexelion:bitacora:live"
BITACORA_MAX = 200
TELEMETRIA = Path("/mnt/nvme/p0x/mente/telemetria/reflejos.jsonl")
POLL_S = 5  # cadencia real del M5

TEMP_DISPARO_C = 40.0
TEMP_REARME_C = 38.0
TEMP_REARME_N = 3
MAG_DISPARO_G = 0.25
MAG_QUIETO_G = 0.10
MAG_REARME_N = 3


def _now_iso():
    return datetime.now(timezone.utc).isoformat()


def emit_console(line: str, r) -> None:
    if r is None:
        return
    try:
        entry = json.dumps({"ts": datetime.now().strftime("%H:%M:%S"),
                            "type": "reflex", "line": line}, ensure_ascii=False)
        r.lpush(BITACORA_KEY, entry)
        r.ltrim(BITACORA_KEY, 0, BITACORA_MAX - 1)
    except Exception:
        pass


def log_reflejo(reflejo: str, disparo: str, valor: dict, accion: str, ms: int) -> None:
    rec = {"ts": _now_iso(), "reflejo": reflejo, "disparo": disparo,
           "valor": valor, "accion": accion, "ms": ms}
    TELEMETRIA.parent.mkdir(parents=True, exist_ok=True)
    with TELEMETRIA.open("a", encoding="utf-8") as f:
        f.write(json.dumps(rec, ensure_ascii=False) + "\n")


class ReflejoTermico:
    """ARMADO ↔ DISPARADO por temp_c con histéresis 40/38 y rearme sostenido."""

    def __init__(self, r):
        self.estado, self.frias, self.r = "ARMADO", 0, r

    def step(self, temp_c, t0):
        if temp_c is None:
            return None  # sensor ausente: ausencia ≠ dato
        if self.estado == "ARMADO":
            self.frias = 0
            if temp_c >= TEMP_DISPARO_C:
                ms = round((time.monotonic() - t0) * 1000)
                line = (f"REFLEX · reflejo-termico-m5: temperatura ambiente alta "
                        f"({temp_c:.1f}°C ≥ {TEMP_DISPARO_C:.0f}) → aviso al Soberano")
                emit_console(line, self.r)
                log_reflejo("reflejo-termico-m5", "TEMP_ALTA",
                            {"temp_c": temp_c}, "aviso REFLEX", ms)
                self.estado = "DISPARADO"
                return "DISPARO"
        else:
            if temp_c <= TEMP_REARME_C:
                self.frias += 1
                if self.frias >= TEMP_REARME_N:
                    ms = round((time.monotonic() - t0) * 1000)
                    line = (f"REFLEX · reflejo-termico-m5: temperatura normalizada "
                            f"({temp_c:.1f}°C ≤ {TEMP_REARME_C:.0f} sostenido) → rearmado")
                    emit_console(line, self.r)
                    log_reflejo("reflejo-termico-m5", "TEMP-rearme",
                                {"temp_c": temp_c}, "rearme", ms)
                    self.estado, self.frias = "ARMADO", 0
                    return "REARME"
            else:
                self.frias = 0
        return None


class ReflejoVibracion:
    """Sismógrafo casero: Δ|g| entre lecturas consecutivas."""

    def __init__(self, r):
        self.estado, self.quietas, self.prev_mag, self.r = "ARMADO", 0, None, r

    def step(self, mag, t0):
        if mag is None:
            self.prev_mag = None  # tras silencio, re-siembra el baseline
            return None
        if self.prev_mag is None:
            self.prev_mag = mag
            return None
        delta = abs(mag - self.prev_mag)
        self.prev_mag = mag
        if self.estado == "ARMADO":
            self.quietas = 0
            if delta >= MAG_DISPARO_G:
                ms = round((time.monotonic() - t0) * 1000)
                line = (f"REFLEX · reflejo-vibracion: movimiento detectado "
                        f"(Δ|g|={delta:.3f} ≥ {MAG_DISPARO_G})")
                emit_console(line, self.r)
                log_reflejo("reflejo-vibracion", "MOVIMIENTO",
                            {"delta_g": round(delta, 4), "mag_g": round(mag, 4)},
                            "aviso REFLEX", ms)
                self.estado = "DISPARADO"
                return "DISPARO"
        else:
            if delta < MAG_QUIETO_G:
                self.quietas += 1
                if self.quietas >= MAG_REARME_N:
                    ms = round((time.monotonic() - t0) * 1000)
                    line = ("REFLEX · reflejo-vibracion: quietud sostenida → rearmado")
                    emit_console(line, self.r)
                    log_reflejo("reflejo-vibracion", "QUIETUD-rearme",
                                {"delta_g": round(delta, 4)}, "rearme", ms)
                    self.estado, self.quietas = "ARMADO", 0
                    return "REARME"
            else:
                self.quietas = 0
        return None


def leer_m5(r):
    """(temp_c, |g|) desde Redis; (None, None) si el M5 calla (TTL vencido)."""
    try:
        raw = r.get(KEY_M5)
        if not raw:
            return None, None
        t = json.loads(raw)
        a = t.get("accel_g") or {}
        mag = None
        if all(a.get(k) is not None for k in ("x", "y", "z")):
            mag = (a["x"] ** 2 + a["y"] ** 2 + a["z"] ** 2) ** 0.5
        return t.get("temp_c"), mag
    except Exception:
        return None, None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--test-temp", help="secuencia temp_c por comas (acciones reales)")
    ap.add_argument("--test-mag", help="secuencia |g| por comas (acciones reales)")
    ap.add_argument("--once", action="store_true")
    args = ap.parse_args()

    try:
        import redis
        r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT,
                        decode_responses=True, socket_timeout=3)
    except Exception:
        r = None
        print("[reflejo-m5] WARN: sin redis — sin consola")

    termico, vib = ReflejoTermico(r), ReflejoVibracion(r)

    if args.test_temp or args.test_mag:
        temps = [float(x) for x in (args.test_temp or "").split(",") if x]
        mags = [float(x) for x in (args.test_mag or "").split(",") if x]
        for i in range(max(len(temps), len(mags))):
            t0 = time.monotonic()
            ev_t = termico.step(temps[i] if i < len(temps) else None, t0)
            ev_v = vib.step(mags[i] if i < len(mags) else None, t0)
            print(f"[reflejo-m5] paso {i}: temp={temps[i] if i < len(temps) else '—'} "
                  f"({termico.estado}{'·' + ev_t if ev_t else ''}) · "
                  f"mag={mags[i] if i < len(mags) else '—'} "
                  f"({vib.estado}{'·' + ev_v if ev_v else ''})")
        return

    print(f"[reflejo-m5] watch vivo · temp {TEMP_DISPARO_C}/{TEMP_REARME_C}°C · "
          f"Δ|g| {MAG_DISPARO_G}/{MAG_QUIETO_G} · poll {POLL_S}s")
    while True:
        t0 = time.monotonic()
        temp, mag = leer_m5(r)
        termico.step(temp, t0)
        vib.step(mag, t0)
        if args.once:
            print(f"[reflejo-m5] temp={temp} mag={None if mag is None else round(mag,4)} · "
                  f"termico={termico.estado} vib={vib.estado}")
            break
        time.sleep(POLL_S)


if __name__ == "__main__":
    main()
