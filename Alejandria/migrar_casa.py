#!/usr/bin/env python3
"""Muda ~/.aurelius a ~/.preceptoros y deja un symlink de compatibilidad.

QUE HACE FALTA SABER ANTES DE CORRERLO
---------------------------------------
`~/.aurelius` NO esta en reposo. `aurelius.service` la tiene abierta en modo
WAL **y ademas es quien sirve el :8740** -- lo que un informe llamo «el MVP
local» es en realidad esa unidad. Mudarla en caliente arriesga el diario de
escritura, asi que este guion PARA el servicio, muda, y lo vuelve a arrancar.
Si no puede pararlo, no muda: para y lo dice.

`casa.py` ya tiene el renombrado resuelto (`NOMBRE = ".preceptoros"`,
`NOMBRES_ANTERIORES = (".aurelius",)`), asi que NO hace falta tocar codigo del
producto. Hoy `raiz()` devuelve la casa vieja porque la nueva no existe --
adopta lo que hay en su sitio en vez de mover gigas sin permiso, que es
justamente la decision correcta. En cuanto exista `~/.preceptoros`, `heredada()`
devuelve None y `raiz()` apunta sola a la casa nueva.

POR QUE `mv` Y NO COPIAR
------------------------
Las dos rutas cuelgan del mismo sistema de ficheros, asi que `mv` es un
renombrado: instantaneo y atomico, pese los megas que pese. Copiar y borrar
despues abriria una ventana en la que existen dos casas con datos distintos --
y aqui son 2,5 GiB, medidos: una auditoria anterior dijo «76 MB» porque conto
solo el primer nivel y se dejo `modelos/` entera. Otro numero que parecia
medido y era una mirada a medias.

Lo que viaja entero, incluidos dos polizones que se declaran y no se tocan:
`cache_prompt.bin` (77 MB, regenerable) y `memory.db.antes-de-p0` (un respaldo
manual del 12 de agosto). Decidir si se quedan es del Soberano, no de este
guion: borrar algo de la casa de alguien durante una mudanza es la peor
ocasion posible para equivocarse.

Dry-run por defecto. `--si` muda.
"""
from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
import time
from pathlib import Path

CASA = Path.home()
VIEJA = CASA / ".aurelius"
NUEVA = CASA / ".preceptoros"
UNIDAD = "aurelius.service"


def _sc(*args, timeout=30):
    p = subprocess.run(["systemctl", "--user", *args], capture_output=True,
                       text=True, timeout=timeout)
    return p.returncode == 0, (p.stdout + p.stderr).strip()


def diagnostico():
    lineas = []
    if NUEVA.is_symlink():
        lineas.append(f"🔴 {NUEVA} ya es un symlink → {os.readlink(NUEVA)}")
    elif NUEVA.exists():
        lineas.append(f"· {NUEVA} YA existe (la mudanza ya se hizo)")
    if VIEJA.is_symlink():
        lineas.append(f"· {VIEJA} ya es symlink → {os.readlink(VIEJA)}")
    elif VIEJA.is_dir():
        n = sum(1 for _ in VIEJA.rglob("*"))
        peso = sum(p.stat().st_size for p in VIEJA.rglob("*") if p.is_file())
        lineas.append(f"· {VIEJA} es directorio real · {n} entradas · "
                      f"{peso / 2**20:.1f} MiB")
    ok, activo = _sc("is-active", UNIDAD)
    lineas.append(f"· {UNIDAD}: {activo}")
    # Mismo sistema de ficheros: si no lo fuera, `mv` seria copia y borrado.
    try:
        mismo = os.stat(CASA).st_dev == os.stat(VIEJA).st_dev
        lineas.append(f"· mismo sistema de ficheros: {'sí' if mismo else 'NO'}")
    except OSError:
        pass
    return lineas


def migrar(aplicar):
    for l in diagnostico():
        print("  " + l)
    print()

    if NUEVA.exists() and not NUEVA.is_symlink():
        print("  ✅ nada que hacer: la casa nueva ya existe")
        return 0
    if not VIEJA.exists():
        print(f"  ⬜ NO_DATA · no existe {VIEJA} ni {NUEVA}: no hay casa que mudar",
              file=sys.stderr)
        return 1
    if VIEJA.is_symlink():
        print(f"  🔴 {VIEJA} ya es symlink pero la casa nueva no existe: "
              "estado inconsistente, no toco nada", file=sys.stderr)
        return 1

    if not aplicar:
        print(f"  + parar {UNIDAD}")
        print(f"  + mv {VIEJA} → {NUEVA}")
        print(f"  + ln -s {NUEVA} {VIEJA}   (compatibilidad)")
        print(f"  + arrancar {UNIDAD}")
        print("\n  (dry-run · vuelve a llamarlo con --si para mudar)")
        return 0

    ok, salida = _sc("is-active", UNIDAD)
    estaba_viva = salida.strip() == "active"
    if estaba_viva:
        print(f"  · parando {UNIDAD} (tiene el WAL abierto y sirve el :8740)")
        ok, salida = _sc("stop", UNIDAD)
        if not ok:
            print(f"  🔴 no se pudo parar: {salida}\n     NO se muda nada.",
                  file=sys.stderr)
            return 1
        # Se espera a que suelte de verdad, no se supone.
        for _ in range(40):
            if _sc("is-active", UNIDAD)[1].strip() != "active":
                break
            time.sleep(0.25)
        print("    parada confirmada")

    try:
        VIEJA.rename(NUEVA)
        print(f"  ✓ mudado: {VIEJA} → {NUEVA}")
        VIEJA.symlink_to(NUEVA, target_is_directory=True)
        print(f"  ✓ symlink de compatibilidad: {VIEJA} → {NUEVA}")
    except OSError as e:
        print(f"  🔴 {type(e).__name__}: {e}", file=sys.stderr)
        return 1
    finally:
        if estaba_viva:
            ok, salida = _sc("start", UNIDAD)
            print(f"  {'✓' if ok else '🔴'} {UNIDAD} arrancada de nuevo"
                  + ("" if ok else f": {salida}"))
    return 0


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--si", action="store_true", help="muda (por defecto: dry-run)")
    return migrar(ap.parse_args(argv).si)


if __name__ == "__main__":
    raise SystemExit(main())
