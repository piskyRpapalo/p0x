"""El almacen de mensajes de coordinacion. Solo se anade; nunca se reescribe.

EN PANTALLA SE LLAMA «EL ACTA»
------------------------------
El nombre de lore vive en la interfaz; aqui, en el codigo, todo es generico y
con gemelo ingles directo (`mensajes` -> messages), para que el dia de la
traduccion se traduzca el texto y no haya que renombrar un solo fichero.

Y «acta» no es decoracion: es la palabra del Escriba -- «Consta en acta,
Soberano», «un escriba que inventa un hash falsifica el acta». Este fichero
hace literalmente lo que esa voz describe.

POR QUE UNA CADENA DE HASH Y NO UNA CONVENCION
----------------------------------------------
El Enjambre Medallon define asi la capa firmada: *«cadena de solo anexion, cada
entrada referencia el hash de la anterior»*. No se inventa nada aqui: se aplica.

`loops.db` resuelve el mismo problema con cuatro disparadores de SQLite que
abortan cualquier UPDATE o DELETE, y su motivo esta escrito: no puede depender
de la disciplina de quien escriba el proximo bucle a las tres de la manana. Un
JSONL no tiene disparadores, asi que el equivalente es encadenar: cambiar una
linea pasada rompe el hash de todas las siguientes, y el gate lo ve.

No es criptografia contra un adversario -- cualquiera con el fichero puede
recalcular la cadena entera. Es contra el DESCUIDO, que es lo que de verdad
pasa: una edicion a mano para «arreglar» un mensaje viejo, un script que
reescribe en vez de anadir. Eso deja de pasar en silencio.

DOS CARAS, UNA PIEDRA
---------------------
Cada mensaje lleva `humano` (palabras para el Soberano) y `maquina` (datos con
fuente y acciones). Las dos tienen que contar lo mismo: el criterio B5 del
Medallon -- *«el resumen concuerda con el cuerpo»* -- nacio de un informe que
decia «sin hallazgos criticos» sobre un texto que describia un riesgo.
"""
from __future__ import annotations

import hashlib
import json
import os
import re
from datetime import datetime, timezone
from pathlib import Path

AQUI = Path(__file__).resolve().parent
ALMACEN = AQUI / "mensajes.jsonl"

# El hash cubre TODO menos el propio `hash`. Incluido `prev`: si no lo cubriera,
# se podrian reordenar dos mensajes sin romper nada.
CAMPO_HASH = "hash"
GENESIS = "0" * 64

TIPOS = ("digesto", "delta", "hallazgo", "aviso")
MIEMBROS = ("enlace", "cowork", "soberano", "guardian", "curador", "afinador")


class ActaRota(RuntimeError):
    """La cadena no cuadra. No se sigue escribiendo sobre algo que ya miente."""


def _canonico(m):
    """Los bytes que se hashean. Orden estable y separadores fijos.

    `sort_keys` no es cosmetica: sin el, el mismo mensaje escrito por dos
    versiones de Python podria dar dos hashes distintos y la cadena se rompería
    sola sin que nadie hubiera tocado nada.
    """
    sin = {k: v for k, v in m.items() if k != CAMPO_HASH}
    return json.dumps(sin, sort_keys=True, ensure_ascii=False,
                      separators=(",", ":")).encode("utf-8")


def hash_de(m):
    return hashlib.sha256(_canonico(m)).hexdigest()


def leer(ruta=None):
    """Todos los mensajes, en orden. Lineas vacias ignoradas; rotas, declaradas."""
    ruta = Path(ruta or ALMACEN)
    if not ruta.exists():
        return []
    fuera = []
    for n, linea in enumerate(ruta.read_text(encoding="utf-8").splitlines(), 1):
        linea = linea.strip()
        if not linea:
            continue
        try:
            fuera.append(json.loads(linea))
        except ValueError as e:
            raise ActaRota(f"linea {n} ilegible: {e}") from None
    return fuera


def verificar(ruta=None):
    """Recorre la cadena. Devuelve la lista de problemas, vacia si esta sana.

    Se devuelven TODOS y no solo el primero: si alguien reescribio tres lineas,
    saber solo de la primera obliga a repetir la comprobacion tres veces.
    """
    problemas = []
    try:
        ms = leer(ruta)
    except ActaRota as e:
        return [str(e)]

    anterior = GENESIS
    for i, m in enumerate(ms, 1):
        ident = m.get("id", f"#{i}")
        if m.get("prev") != anterior:
            problemas.append(
                f"{ident}: `prev` dice {str(m.get('prev'))[:12]}… y la linea "
                f"anterior hashea a {anterior[:12]}… — se insertó, se borró o "
                "se reordenó una línea")
        esperado = hash_de(m)
        if m.get(CAMPO_HASH) != esperado:
            problemas.append(
                f"{ident}: el contenido cambió después de escribirse "
                f"(hash {str(m.get(CAMPO_HASH))[:12]}… ≠ {esperado[:12]}…)")
        # Se encadena sobre el hash RECALCULADO, no sobre el guardado.
        #
        # Con el guardado, editar un mensaje solo rompia SU linea: la siguiente
        # seguia apuntando al hash viejo, que seguia escrito en el fichero, y
        # todo lo posterior pasaba en verde. Eso no es una cadena, es una suma
        # de comprobaciones sueltas. Encadenando sobre el contenido real, tocar
        # el mensaje 2 invalida el enlace del 3, del 4 y de todos: exactamente
        # lo que el Medallon pide cuando dice «cada entrada referencia el hash
        # de la anterior».
        #
        # Lo encontro el gate en su primera corrida.
        anterior = esperado
    return problemas


def _cifras(texto):
    """Los numeros que aparecen en un texto. Para el criterio B5.

    El separador solo cuenta si va SEGUIDO de digito. El patron ingenuo
    (`\d[\d.,]*`) se tragaba la coma que JSON pone tras cada valor, asi que
    «17» en la prosa y «17,» en el JSON eran dos numeros distintos y el acta
    rechazaba mensajes correctos. Una comprobacion que da falsos positivos se
    desactiva sola a la tercera vez.
    """
    return set(re.findall(r"\d+(?:[.,]\d+)*", texto or ""))


def incoherencias(m):
    """Las dos caras del mensaje, contrastadas. Criterio B5 del Medallon.

    No se intenta entender la prosa -- eso seria pedirle a un script que juzgue
    lenguaje, que es justo lo que el Medallon dice que no cuenta. Se comprueba
    lo comprobable: que toda cifra de la cara humana aparezca tambien en la de
    maquina. Un numero que solo existe en la prosa no lo midio nadie.
    """
    fallos = []
    humano = m.get("humano") or ""
    maquina = json.dumps(m.get("maquina") or {}, ensure_ascii=False)
    huerfanas = sorted(_cifras(humano) - _cifras(maquina))
    # Los anyos y las horas de la marca de tiempo no son medidas.
    huerfanas = [c for c in huerfanas if c not in _cifras(m.get("ts", ""))]
    if huerfanas:
        fallos.append(
            f"la cara humana cita cifras que la de máquina no respalda: "
            f"{', '.join(huerfanas)}")
    if not m.get("fuente"):
        fallos.append("sin `fuente[]`: una afirmación sin fuente es una opinión")
    return fallos


def escribir(de, para, tipo, humano, maquina, fuente,
             firma_requerida=False, ruta=None, ts=None):
    """Anade un mensaje al final. Verifica la cadena ANTES de escribir.

    Si el acta ya esta rota, no se escribe: anadir sobre una cadena que miente
    es firmar debajo de una falsificacion.
    """
    ruta = Path(ruta or ALMACEN)
    if de not in MIEMBROS:
        raise ValueError(f"'{de}' no es del acta. Miembros: {', '.join(MIEMBROS)}")
    if tipo not in TIPOS:
        raise ValueError(f"tipo '{tipo}' desconocido. Tipos: {', '.join(TIPOS)}")
    if not fuente:
        raise ValueError("sin fuente[] no se escribe: es la regla de la casa")

    rotos = verificar(ruta)
    if rotos:
        raise ActaRota("el acta ya está rota, no se escribe encima:\n  - " +
                       "\n  - ".join(rotos))

    ms = leer(ruta)
    anterior = ms[-1][CAMPO_HASH] if ms else GENESIS
    m = {
        "id": f"{len(ms) + 1:05d}",
        "de": de,
        "para": list(para),
        "tipo": tipo,
        "ts": ts or datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds"),
        "prev": anterior,
        "humano": humano,
        "maquina": maquina,
        "fuente": list(fuente),
        "firma_requerida": bool(firma_requerida),
    }
    malas = incoherencias(m)
    if malas:
        raise ValueError("las dos caras no cuadran:\n  - " + "\n  - ".join(malas))

    m[CAMPO_HASH] = hash_de(m)
    ruta.parent.mkdir(parents=True, exist_ok=True)
    # Append en modo texto con una sola escritura: una linea entera o ninguna.
    with open(ruta, "a", encoding="utf-8") as fh:
        fh.write(json.dumps(m, ensure_ascii=False) + "\n")
        fh.flush()
        os.fsync(fh.fileno())
    return m
