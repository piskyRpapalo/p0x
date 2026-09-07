#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Vacia el buzon temporal del Soberano hacia la-fragua, cuando exista alli.

QUE ES ESTO Y POR QUE HACE FALTA
--------------------------------
Las medidas de los testers se estan guardando en el Beelink porque
`/api/v1/medidas` de la-fragua devuelve 404: no hay tabla, no es que este
vacia. Este guion es el puente para el dia que la haya. Mientras tanto NO
pierde nada -- el buzon es append-only y `processed` solo avanza cuando la otra
punta confirma.

LO QUE NUNCA HACE, Y ES LA MITAD DEL DISEÑO
-------------------------------------------
No marca como enviada una medida que no se confirmo. Si la-fragua responde
cualquier cosa que no sea 200 o 201, esa fila se queda en 0 y se reintenta.
Marcar por optimismo es como se pierden los datos que mas cuestan: los que solo
existian una vez.

Y NO BORRA. Sincronizada no es lo mismo que desechable: la copia del Soberano se
queda, porque la otra punta tambien se puede caer.

PROPOSE-ONLY POR DEFECTO. Sin `--ejecutar` cuenta lo que hay y para.
"""
from __future__ import annotations

import argparse
import json
import sqlite3
import urllib.error
import urllib.request
from pathlib import Path

BASE = Path.home() / ".preceptoros" / "medidas_temp.db"
DESTINO = "https://api.preceptoros.org/api/v1/medidas"


def pendientes(con, limite):
    return con.execute(
        "SELECT id, timestamp, user_hash, payload_json FROM medidas "
        "WHERE processed = 0 ORDER BY id LIMIT ?", (limite,)).fetchall()


def enviar(destino, fila, timeout):
    _id, ts, huella, payload = fila
    cuerpo = json.dumps({"timestamp": ts, "user_hash": huella,
                         "medida": json.loads(payload)}, ensure_ascii=False).encode()
    pet = urllib.request.Request(destino, cuerpo, {"Content-Type": "application/json"})
    with urllib.request.urlopen(pet, timeout=timeout) as r:
        return r.status


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--ejecutar", action="store_true",
                    help="sin esto cuenta y para, sin enviar nada")
    ap.add_argument("--base", type=Path, default=BASE)
    ap.add_argument("--destino", default=DESTINO)
    ap.add_argument("--lote", type=int, default=100)
    ap.add_argument("--timeout", type=float, default=30.0)
    a = ap.parse_args(argv)

    if not a.base.exists():
        print(json.dumps({"base": str(a.base), "existe": False,
                          "nota": "no hay buzon todavia: nadie ha enviado una medida"}))
        return 0
    con = sqlite3.connect(a.base)
    filas = pendientes(con, a.lote)
    total = con.execute("SELECT COUNT(*) FROM medidas").fetchone()[0]
    print(json.dumps({"base": str(a.base), "medidas": total,
                      "sin_sincronizar": len(filas), "destino": a.destino},
                     ensure_ascii=False))
    if not filas:
        return 0
    if not a.ejecutar:
        print("\nPLAN, no ejecucion. Anade --ejecutar cuando el carbono firme.")
        return 0

    enviadas, fallos = 0, []
    for f in filas:
        try:
            codigo = enviar(a.destino, f, a.timeout)
        except urllib.error.HTTPError as e:
            fallos.append((f[0], f"HTTP {e.code}")); continue
        except (urllib.error.URLError, TimeoutError, OSError) as e:
            fallos.append((f[0], str(e)[:60])); continue
        if codigo in (200, 201):
            con.execute("UPDATE medidas SET processed = 1 WHERE id = ?", (f[0],))
            enviadas += 1
        else:
            fallos.append((f[0], f"codigo {codigo}"))
    con.commit()
    print(f"enviadas {enviadas} · sin confirmar {len(fallos)}")
    for i, causa in fallos[:5]:
        print(f"  · id {i}: {causa}")
    if fallos:
        print("Las que no confirmaron SIGUEN en 0 y se reintentan. Marcar por "
              "optimismo es como se pierden los datos que solo existian una vez.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
