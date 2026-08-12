#!/usr/bin/env python3
"""Auditor chat->disco: compara los D-ids ESPERADOS con los que hay en disco.

Los otros auditores verifican que lo escrito sea correcto. Ninguno puede
verificar que este TODO: una decision que se tomo en conversacion y nunca se
escribio no deja rastro en el disco, luego mirando solo el disco es invisible.

Por eso este auditor lee la lista de esperados de un fichero FUERA de git
(el archivo de razonamiento, D41) y la compara con el estado firmado. La lista
es la memoria; el estado firmado es la prueba; la distancia es el hallazgo.

Salida: una linea por hallazgo. Codigo 1 si hay ausencias reales, 0 si no.
Un HUECO declarado (D24) es NO_DATA, no una ausencia: se informa y no bloquea.

    python3 audit_dids.py [--razonamiento RUTA] [--firmado RUTA]
"""

from __future__ import annotations

import argparse
import os
import re
import sys

RAZONAMIENTO = os.path.expanduser(
    "~/.local/share/p0x/razonamiento/ARCHIVO_RAZONAMIENTO.md"
)

# La raiz se deriva de la posicion de ESTE fichero, no de un literal ni del
# directorio de trabajo: `run_audit.sh` invoca a los auditores sin hacer `cd`,
# asi que una ruta relativa se rompe segun desde donde se llame. `P0X_ROOT`
# manda si esta puesto, para poder auditar un clon.
#
# Deliberadamente NO se copia el patron de audit_lib.py, que cae a un literal
# absoluto: ese literal apunta hoy a un directorio inexistente en este nodo.
_RAIZ = os.environ.get("P0X_ROOT") or os.path.abspath(
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..")
)
FIRMADO = os.path.join(_RAIZ, "Cuarentena", "03_ESTADO_FIRMADO.md")

INICIO = "<!-- D_IDS_ESPERADOS:INICIO -->"
FIN = "<!-- D_IDS_ESPERADOS:FIN -->"

# Las dos formas legitimas en que un D-id vive en el estado firmado.
# D1-D7 son filas de tabla; D8 en adelante son cabeceras. Un auditor que solo
# busque cabeceras declara siete ausencias falsas.
FORMA_CABECERA = "cabecera"
FORMA_TABLA = "tabla"
FORMA_HUECO = "HUECO"


def leer_esperados(ruta: str) -> list[tuple[str, str]]:
    """[(d_id, forma)] leidos de la region delimitada por marcadores.

    La region va entre marcadores a proposito: anadir prosa al archivo de
    razonamiento no debe cambiar lo que el auditor cree que espera.
    """
    try:
        with open(ruta, encoding="utf-8") as fh:
            texto = fh.read()
    except OSError as e:
        print(f"BLOQUEADO · no puedo leer el archivo de razonamiento: {e}")
        print("  El auditor NO asume una lista vacia: sin lista no hay "
              "auditoria, y una auditoria vacia diria 'todo bien'.")
        sys.exit(2)

    if INICIO not in texto or FIN not in texto:
        print(f"BLOQUEADO · faltan los marcadores en {ruta}")
        sys.exit(2)

    bloque = texto.split(INICIO, 1)[1].split(FIN, 1)[0]
    esperados = []
    for linea in bloque.splitlines():
        linea = linea.strip()
        if not linea:
            continue
        partes = linea.split()
        if len(partes) < 2:
            print(f"BLOQUEADO · linea sin forma declarada: {linea!r}")
            sys.exit(2)
        esperados.append((partes[0], partes[1]))
    return esperados


def leer_en_disco(ruta: str) -> tuple[set[str], set[str]]:
    """(ids como cabecera, ids como fila de tabla) presentes en el firmado."""
    try:
        with open(ruta, encoding="utf-8") as fh:
            texto = fh.read()
    except OSError as e:
        print(f"BLOQUEADO · no puedo leer el estado firmado: {e}")
        sys.exit(2)
    cabeceras = set(re.findall(r"^## (D[0-9]+) · ", texto, re.MULTILINE))
    tablas = set(re.findall(r"^\| \*\*(D[0-9]+)\*\* \|", texto, re.MULTILINE))
    return cabeceras, tablas


def main() -> int:
    ap = argparse.ArgumentParser(description="Auditor chat->disco de D-ids")
    ap.add_argument("--razonamiento", default=RAZONAMIENTO)
    ap.add_argument("--firmado", default=FIRMADO)
    args = ap.parse_args()

    esperados = leer_esperados(args.razonamiento)
    cabeceras, tablas = leer_en_disco(args.firmado)
    en_disco = cabeceras | tablas

    ausentes: list[str] = []
    forma_mal: list[str] = []
    huecos: list[str] = []

    for d_id, forma in esperados:
        if forma == FORMA_HUECO:
            if d_id in en_disco:
                forma_mal.append(
                    f"{d_id} · declarado HUECO en el archivo de razonamiento "
                    f"pero PRESENTE en disco — actualiza el archivo"
                )
            else:
                huecos.append(d_id)
            continue
        if d_id not in en_disco:
            ausentes.append(d_id)
            continue
        real = FORMA_CABECERA if d_id in cabeceras else FORMA_TABLA
        if real != forma:
            forma_mal.append(f"{d_id} · esperado como {forma}, en disco {real}")

    esperados_ids = {d for d, _ in esperados}
    huerfanos = sorted(
        en_disco - esperados_ids,
        key=lambda x: int(x[1:]),
    )

    print("── AUDITOR chat→disco · D-ids " + "─" * 35)
    print(f"esperados : {len(esperados)}  (de {args.razonamiento})")
    print(f"en disco  : {len(en_disco)}  (de {args.firmado})")
    print(f"  cabecera: {len(cabeceras)}   tabla: {len(tablas)}")
    print()

    for d in ausentes:
        print(f"  AUSENTE   · {d} esperado y NO esta en disco")
    for m in forma_mal:
        print(f"  FORMA     · {m}")
    for d in huerfanos:
        print(f"  HUERFANO  · {d} en disco y NO esta en la lista de esperados")
    for d in huecos:
        print(f"  NO_DATA   · {d} hueco declarado — no se rellena, no bloquea")

    fallos = len(ausentes) + len(forma_mal) + len(huerfanos)
    print()
    print(f"RESULTADO: {fallos} hallazgo(s) que bloquean, "
          f"{len(huecos)} NO_DATA declarado(s)")
    return 1 if fallos else 0


if __name__ == "__main__":
    sys.exit(main())
