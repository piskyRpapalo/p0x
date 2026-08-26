"""La forja: en que fase esta, que datasets hay y que adapters se llegaron a producir.

Nada se ejecuta ni se entrena desde aqui: se cuentan ficheros. La fase sale del
README del propio proyecto --su primera linea de estado-- y no de una constante
escrita aqui, que se quedaria vieja el dia que la fase cambie sin que nadie
tocara este fichero.
"""

import re
from pathlib import Path

import sensores
from sensores import registro

FORJA = Path(__file__).resolve().parents[2] / "aurelius-lora"
# Lo que convierte una carpeta en un adapter de verdad. Una carpeta vacia con
# nombre prometedor no es un adapter, y contarla inflaria la cifra.
PESO = "adapter_model.safetensors"


def _fase():
    readme = FORJA / "README.md"
    if not readme.is_file():
        return sensores.NO_DATA
    for linea in readme.read_text(encoding="utf-8", errors="replace").splitlines()[:20]:
        m = re.search(r"Estado:\s*\*{0,2}([^*\n.]+)", linea)
        if m:
            return m.group(1).strip().rstrip(".·").strip()
    return sensores.NO_DATA


def _lineas(fichero):
    try:
        with open(fichero, "rb") as f:
            return sum(1 for linea in f if linea.strip())
    except OSError:
        return None


def leer():
    if not FORJA.is_dir():
        return sensores.hueco("la forja no existe en disco")

    datasets = []
    for f in sorted((FORJA / "data").glob("*.jsonl")) if (FORJA / "data").is_dir() else []:
        n = _lineas(f)
        datasets.append({"nombre": f.name,
                         "ejemplos": n if n is not None else sensores.NO_DATA,
                         "bytes": f.stat().st_size})

    adapters = []
    salida = FORJA / "salida"
    if salida.is_dir():
        for d in sorted(p for p in salida.iterdir() if p.is_dir()):
            peso = d / PESO
            if peso.is_file():
                adapters.append({"nombre": d.name, "bytes": peso.stat().st_size,
                                 "estado": "ok"})
            else:
                adapters.append({"nombre": d.name, "bytes": 0,
                                 "estado": sensores.NO_DATA,
                                 "causa": "carpeta sin fichero de pesos"})

    total = sum(d["ejemplos"] for d in datasets if isinstance(d["ejemplos"], int))
    return sensores.dato(
        fase=_fase(),
        datasets=datasets,
        adapters=adapters,
        ejemplos_totales=total if datasets else sensores.NO_DATA,
        entrenados=sum(1 for a in adapters if a["estado"] == "ok"),
    )


registro.registrar("lora", leer)
