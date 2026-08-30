#!/usr/bin/env python3
"""Deuda firmada: el empaquetado y las guias dejan de decir «aurelius».

POR QUE ANTES DE PUBLICAR NADA DE INSTALACION
---------------------------------------------
`install.sh` e `install.ps1` van a clonar el repositorio y arrancar el binario.
Si se publican con el nombre viejo dentro, cada persona que instale se lleva a
casa una copia de la deuda -- y a partir de ahi ya no se renombra, se migra.

`bin/` ya estaba hecho (los `aurelius-*` son symlinks a los `preceptoros-*`).
Lo que queda: los dos iconos, el guion de construccion, el modulo que carga el
lanzador, y las cuatro guias.

QUE NO SE TOCA
--------------
`~/.aurelius` como RUTA DE DATOS no se reescribe a ciegas: hoy es un symlink de
compatibilidad a `~/.preceptoros`, y `casa.py` resuelve la casa por su cuenta.
Las guias si pasan a nombrar la casa nueva, que es la que el producto usa desde
la mudanza; pero el symlink se queda, porque quien instalo antes lo tiene.

Dry-run por defecto; `--si` aplica.
"""
from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path

RAIZ = Path.home() / "p0x" / "preceptor"

# Renombrados de fichero. `git mv` para que la historia siga al fichero.
MUEVE = [("empaquetado/aurelius.ico", "empaquetado/preceptoros.ico"),
         ("empaquetado/aurelius.png", "empaquetado/preceptoros.png")]

# Sustituciones de texto, en orden. Las mas especificas PRIMERO: si
# `aurelius` -> `preceptoros` corriera antes, se llevaria por delante
# `~/.aurelius` y `aurelius.ico` y el resto no encontraria nada que arreglar.
# Lo que NO se toca: los nombres de variable de entorno `AURELIUS_*`. Son
# fallbacks deliberados -- `${PRECEPTOROS_REPO:-${AURELIUS_REPO:-...}}` -- y
# existen para que a quien los tenga exportados de antes no se le rompa nada.
# Renombrarlos no seria saldar una deuda: seria romper la compatibilidad que
# alguien escribio a proposito. Se protegen antes de sustituir y se restauran
# despues.
PROTEGIDO = "\x00AURELIUSVAR\x00"

CAMBIOS = [
    # la casa de datos: a la nueva, que es la que el producto usa ya
    (r"~/\.aurelius\b", "~/.preceptoros"),
    (r"\$HOME/\.aurelius\b", "$HOME/.preceptoros"),
    # el arbol clonado
    (r"~/aurelius\b", "~/preceptoros"),
    # binarios y artefactos
    (r"\bbin/aurelius-", "bin/preceptoros-"),
    (r"\bdist/aurelius\b", "dist/preceptoros"),
    (r"\baurelius-pwa\b", "preceptoros-pwa"),
    (r"\baurelius-build\b", "preceptoros-build"),
    (r"\baurelius_pwa\b", "preceptoros_pwa"),
    (r"empaquetado/aurelius\.(ico|png)", r"empaquetado/preceptoros.\1"),
    (r"--name aurelius\b", "--name preceptoros"),
    # lo que quede suelto, ya sin riesgo de pisar los casos de arriba
    (r"\baurelius\b", "preceptoros"),
    (r"\bAurelius\b", "PreceptorOS"),
]

FICHEROS = ["empaquetado/construir_pc.sh", "empaquetado/lanzador.py",
            "INSTALACION_ANDROID.md", "INSTALL_ANDROID.md",
            "INSTALACION_PC.md", "INSTALL_PC.md",
            "test_pwa.py", "test_compass.py",
            "bin/instalar-pc", "bin/instalar-android",
            "bin/crear-acceso-directo-android", "bin/detectar-termux-boot",
            "bin/preceptoros-servicio", "bin/preceptoros-servicio-pc",
            "bin/preceptoros-puente", "bin/preceptoros-pwa", "bin/eco-remoto"]


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--si", action="store_true")
    a = ap.parse_args(argv)
    total = 0

    for viejo, nuevo in MUEVE:
        vp, np_ = RAIZ / viejo, RAIZ / nuevo
        if np_.exists():
            continue
        if not vp.exists():
            print(f"  ⬜ {viejo} no existe"); continue
        print(f"  {'✓' if a.si else '·'} mv {viejo} → {nuevo}")
        total += 1
        if a.si:
            subprocess.run(["git", "-C", str(RAIZ), "mv", viejo, nuevo], check=True)

    for rel in FICHEROS:
        p = RAIZ / rel
        if not p.exists():
            print(f"  ⬜ {rel} no existe"); continue
        t = original = p.read_text(encoding="utf-8")
        t = re.sub(r"AURELIUS_([A-Z_]+)", lambda m: PROTEGIDO + m.group(1), t)
        for patron, sust in CAMBIOS:
            t = re.sub(patron, sust, t)
        t = t.replace(PROTEGIDO, "AURELIUS_")
        if t == original:
            continue
        n = sum(1 for _ in re.finditer(r"(?i)aurelius", original))
        print(f"  {'✓' if a.si else '·'} {rel} · {n} ocurrencia(s)")
        total += 1
        if a.si:
            p.write_text(t, encoding="utf-8")

    quedan = subprocess.run(
        ["bash", "-lc", f"grep -ril aurelius {' '.join(FICHEROS)} "
                        "empaquetado/ 2>/dev/null | sort -u"],
        cwd=str(RAIZ), capture_output=True, text=True).stdout.strip()
    if a.si and quedan:
        print("\n  ⚠️  todavía nombran aurelius:", file=sys.stderr)
        for l in quedan.splitlines():
            print(f"     {l}", file=sys.stderr)
    print(f"\n{total} cambio(s) {'aplicados' if a.si else 'a aplicar'}"
          + ("" if a.si else " · --si para hacerlo"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
