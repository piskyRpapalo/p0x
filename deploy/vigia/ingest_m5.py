#!/usr/bin/env python3
"""P0X Fase 4 — ingesta telemetría M5 Atom (el-vigia) → Redis fragua.

Lee líneas JSON del M5 por serial (115200) y las publica en Redis:
  - hexelion:telemetry:m5:last  (SET, TTL 30s)  — última línea de telemetría
  - hexelion:telemetry:m5:scan  (SET, sin TTL)  — última línea i2c_scan verbatim
  - PUBLISH hexelion:telemetry:m5               — cada línea de telemetría

Read-only sobre el hardware: jamás escribe al serial.
La ausencia de dato es ausencia (TTL expira) — nunca se inventa un valor.
"""
import glob
import json
import sys
import time

import redis
import serial

SERIAL_GLOB = "/dev/serial/by-id/usb-Hades2001_M5stack_*-port0"
BAUD = 115200
REDIS_HOST = "100.82.94.83"
REDIS_PORT = 6379
KEY_LAST = "hexelion:telemetry:m5:last"
KEY_SCAN = "hexelion:telemetry:m5:scan"
CHANNEL = "hexelion:telemetry:m5"
TTL_LAST = 30  # s — si el M5 calla, la clave muere sola


def log(msg: str) -> None:
    print(f"[ingest_m5] {msg}", flush=True)


def find_port() -> str | None:
    hits = sorted(glob.glob(SERIAL_GLOB))
    return hits[0] if hits else None


def connect_redis() -> redis.Redis:
    return redis.Redis(host=REDIS_HOST, port=REDIS_PORT,
                       socket_timeout=5, socket_connect_timeout=5,
                       decode_responses=True)


def handle_line(r: redis.Redis, raw: str) -> None:
    raw = raw.strip()
    if not raw or not raw.startswith("{"):
        return
    try:
        obj = json.loads(raw)
    except json.JSONDecodeError:
        log(f"línea no-JSON descartada: {raw[:120]!r}")
        return
    now = time.time()
    if obj.get("event") == "i2c_scan":
        payload = json.dumps({"received_at": now, "raw": raw}, ensure_ascii=False)
        r.set(KEY_SCAN, payload)
        log(f"i2c_scan verbatim: {raw}")
        return
    obj["received_at"] = now
    obj["source"] = "el-vigia:m5atom"
    payload = json.dumps(obj, ensure_ascii=False)
    r.set(KEY_LAST, payload, ex=TTL_LAST)
    r.publish(CHANNEL, payload)


def main() -> None:
    r = None
    while True:
        try:
            if r is None:
                r = connect_redis()
                r.ping()
                log(f"Redis OK {REDIS_HOST}:{REDIS_PORT}")
            port = find_port()
            if port is None:
                log("M5 no presente; reintento en 10s")
                time.sleep(10)
                continue
            log(f"abriendo {port} @ {BAUD}")
            with serial.Serial(port, BAUD, timeout=10) as ser:
                # pulso RTS = reset del ESP32: el boot reemite i2c_scan,
                # así la clave :scan siempre refleja el bus real actual
                ser.dtr = False
                ser.rts = True
                time.sleep(0.1)
                ser.rts = False
                while True:
                    line = ser.readline()
                    if not line:
                        continue  # timeout de lectura; el TTL ya refleja el silencio
                    handle_line(r, line.decode("utf-8", errors="replace"))
        except redis.RedisError as e:
            log(f"Redis caído: {e}; reintento en 10s")
            r = None
            time.sleep(10)
        except (serial.SerialException, OSError) as e:
            log(f"serial caído: {e}; reintento en 10s")
            time.sleep(10)
        except KeyboardInterrupt:
            log("parada manual")
            return


if __name__ == "__main__":
    main()
