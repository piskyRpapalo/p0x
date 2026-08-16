#!/usr/bin/env python3
"""Auditor chat->disco: compara los D-ids ESPERADOS con los que hay en disco.

Los otros auditores verifican que lo escrito sea correcto. Ninguno puede
verificar que este TODO: una decision que se tomo en conversacion y nunca se
escribio no deja rastro en el disco, luego mirando solo el disco es invisible.

Por eso este auditor lee la lista de esperados de un fichero FUERA de git
(el archivo de razonamiento, D41) y la compara con el estado firmado. La lista
es la memoria; el estado firmado es la prueba; la distancia es el hallazgo.

Salida: una linea por hallazgo. Codigo 1 si hay ausencias reales, 0 si no.

Un HUECO no es una ausencia, pero no todos los huecos valen lo mismo, y el
auditor que los trataba igual no servia para lo unico que importa: notar que
una edicion acaba de abrir uno. Se declara la ANTIGUEDAD del hueco:

  HUECO_PREEXISTENTE  el salto es anterior a la serie que audita. Nadie vivo
                      sabe que fue (D24). NO_DATA puro: se informa, no bloquea.
  HUECO_NUEVO         el salto lo abrio una edicion de esta serie (D42). Es
                      hallazgo BLOQUEANTE mientras su motivo no conste en el
                      ESTADO FIRMADO. No basta con explicarlo en el archivo de
                      razonamiento: ese fichero es memoria, no prueba, y lo
                      edita el mismo proceso al que se le esta auditando. Un
                      hueco que se justifica a si mismo en su propio cuaderno
                      es un hueco sin justificar.

El HUECO a secas ya no se acepta: obligaba a decidir de memoria si un salto
era viejo o recien hecho, que es exactamente la clase de juicio atencional que
D28 prohibe. Declarar la antiguedad cuesta una palabra y la vuelve mecanica.

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

# Antiguedad del hueco. Ver el docstring: la distincion es el objeto de este
# auditor, no un detalle de formato.
FORMA_HUECO_PRE = "HUECO_PREEXISTENTE"
FORMA_HUECO_NUEVO = "HUECO_NUEVO"
HUECOS = (FORMA_HUECO_PRE, FORMA_HUECO_NUEVO)

# Forma retirada. Se rechaza en vez de mapearse a una de las dos por defecto:
# cualquier default aqui adivina la antiguedad de un hueco, que es el dato.
FORMA_HUECO_OBSOLETA = "HUECO"


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
        d_id, forma = partes[0], partes[1]
        if forma == FORMA_HUECO_OBSOLETA:
            print(f"BLOQUEADO · {d_id} declarado como {FORMA_HUECO_OBSOLETA} "
                  f"a secas, forma retirada.")
            print(f"  Declara {FORMA_HUECO_PRE} (salto anterior a esta serie) "
                  f"o {FORMA_HUECO_NUEVO} (salto abierto por una edicion de "
                  f"esta serie).")
            sys.exit(2)
        if forma not in (FORMA_CABECERA, FORMA_TABLA, *HUECOS):
            print(f"BLOQUEADO · {d_id} declarado con forma desconocida: "
                  f"{forma!r}")
            sys.exit(2)
        esperados.append((d_id, forma))
    return esperados


def justificado_en_firmado(d_id: str, texto: str) -> bool:
    """¿El estado firmado cita este D-id en el cuerpo de alguna decision?

    Se busca en el firmado y NO en el archivo de razonamiento a proposito: un
    hueco nuevo se cierra firmando su motivo donde vive la prueba. El limite
    de palabra evita que D4 se de por justificado al aparecer D42.
    """
    return re.search(rf"\b{re.escape(d_id)}\b", texto) is not None


def leer_en_disco(ruta: str) -> tuple[set[str], set[str], str]:
    """(ids como cabecera, ids como fila de tabla, texto) del firmado."""
    try:
        with open(ruta, encoding="utf-8") as fh:
            texto = fh.read()
    except OSError as e:
        print(f"BLOQUEADO · no puedo leer el estado firmado: {e}")
        sys.exit(2)
    cabeceras = set(re.findall(r"^## (D[0-9]+) · ", texto, re.MULTILINE))
    tablas = set(re.findall(r"^\| \*\*(D[0-9]+)\*\* \|", texto, re.MULTILINE))
    return cabeceras, tablas, texto


def main() -> int:
    ap = argparse.ArgumentParser(description="Auditor chat->disco de D-ids")
    ap.add_argument("--razonamiento", default=RAZONAMIENTO)
    ap.add_argument("--firmado", default=FIRMADO)
    args = ap.parse_args()

    esperados = leer_esperados(args.razonamiento)
    cabeceras, tablas, texto_firmado = leer_en_disco(args.firmado)
    en_disco = cabeceras | tablas

    ausentes: list[str] = []
    forma_mal: list[str] = []
    huecos: list[str] = []
    huecos_sin_firmar: list[str] = []

    for d_id, forma in esperados:
        if forma in HUECOS:
            if d_id in en_disco:
                forma_mal.append(
                    f"{d_id} · declarado {forma} en el archivo de "
                    f"razonamiento pero PRESENTE en disco — actualiza el "
                    f"archivo"
                )
            elif forma == FORMA_HUECO_NUEVO and not justificado_en_firmado(
                d_id, texto_firmado
            ):
                huecos_sin_firmar.append(d_id)
            else:
                huecos.append(f"{d_id} ({forma})")
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
    for d in huecos_sin_firmar:
        print(f"  HUECO_NUEVO · {d} lo abrio una edicion de esta serie y su "
              f"motivo NO consta en el estado firmado")
        print(f"                explicarlo en el archivo de razonamiento no "
              f"basta: ese fichero es memoria, no prueba")
    for d in huecos:
        print(f"  NO_DATA   · {d} hueco declarado — no se rellena, no bloquea")

    fallos = len(ausentes) + len(forma_mal) + len(huerfanos) + len(
        huecos_sin_firmar
    )
    print()
    print(f"RESULTADO: {fallos} hallazgo(s) que bloquean, "
          f"{len(huecos)} NO_DATA declarado(s)")
    return 1 if fallos else 0


if __name__ == "__main__":
    sys.exit(main())
