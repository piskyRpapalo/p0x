#!/usr/bin/env python3
"""set_rtc_m5.py — P0X #30: fija el DS3231 del M5 a hora de PORTUGAL.

One-shot. Envía "T<epoch>" por serial (handler rtc_set del firmware 2026-07-11).
El DS3231 guarda hora de PARED: se manda el reloj de Lisboa "como si fuera UTC".
Requiere el puerto libre (parar p0x-m5-ingest antes). Uso:
  sudo systemctl stop p0x-m5-ingest
  ~/p0x-telemetry/venv/bin/python set_rtc_m5.py
  sudo systemctl start p0x-m5-ingest
"""
import glob
import sys
import time
from datetime import datetime, timezone
from zoneinfo import ZoneInfo

import serial

PORT = sorted(glob.glob("/dev/serial/by-id/usb-Hades2001_M5stack_*-port0"))[0]

lisboa = datetime.now(ZoneInfo("Europe/Lisbon"))
epoch_pared = int(lisboa.replace(tzinfo=timezone.utc).timestamp())
print(f"hora Lisboa: {lisboa:%Y-%m-%d %H:%M:%S} -> T{epoch_pared}")

with serial.Serial(PORT, 115200, timeout=12) as ser:
    time.sleep(0.5)
    ser.reset_input_buffer()
    ser.write(f"T{epoch_pared}\n".encode())
    deadline = time.time() + 15
    while time.time() < deadline:
        line = ser.readline().decode(errors="replace").strip()
        if '"rtc_set"' in line:
            print("RESPUESTA:", line)
            sys.exit(0 if '"ok":true' in line else 1)
        elif line:
            print("(telemetria)", line[:80])
print("SIN respuesta rtc_set", file=sys.stderr)
sys.exit(2)
