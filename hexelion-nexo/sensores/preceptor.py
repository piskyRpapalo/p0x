"""El nucleo publico: su version, y la ultima tanda de pruebas con su edad.

La version se lee EN VIVO del propio arbol, que es la unica forma de que no
mienta. La tanda no: correr 526 pruebas tarda minutos y una peticion HTTP no
puede esperar eso, asi que se mide aparte --`python3 -m sensores.preceptor
--medir`-- y aqui se lee lo medido **con su hora al lado**.

Esa hora es la mitad del dato. Un «526/526» sin fecha no distingue una tanda de
hace un minuto de una de hace tres semanas, y la segunda no dice nada sobre el
arbol de hoy. Pasadas 24 h la lectura se marca rancia; sin ninguna tanda
registrada, NO_DATA.
"""

import json
import re
import subprocess
import sys
from datetime import datetime, timedelta
from pathlib import Path

import sensores
from sensores import registro

NUCLEO = Path(__file__).resolve().parents[2] / "aurelius"
CACHE = Path(__file__).resolve().parents[1] / "estado" / "tanda.json"
RANCIA = timedelta(hours=24)


def _version():
    if str(NUCLEO) not in sys.path:
        sys.path.insert(0, str(NUCLEO))
    import version as _v
    return _v.corta(), _v.version()


def medir():
    """Corre la tanda y guarda el resultado. Se llama a mano, nunca desde HTTP.

    Escritura atomica: se escribe al lado y se renombra. Un panel que lee a
    mitad de escritura veria un json roto, y el json roto de una tanda buena es
    indistinguible del de una tanda que se corto.
    """
    proc = subprocess.run(["bash", "bin/pruebas", "--rapido"], cwd=NUCLEO,
                          capture_output=True, text=True, timeout=1800)
    texto = proc.stdout + proc.stderr
    m = re.search(r"(\d+) pruebas · (\d+) suites", texto)
    verde = re.search(r"VERDE · (\d+)/(\d+)", texto)
    resultado = {
        "medido": sensores.ahora(),
        "pruebas": int(m.group(1)) if m else None,
        "suites": int(m.group(2)) if m else None,
        "verde": bool(verde) and proc.returncode == 0,
        "codigo": proc.returncode,
    }
    CACHE.parent.mkdir(parents=True, exist_ok=True)
    parcial = CACHE.with_suffix(".json.partial")
    parcial.write_text(json.dumps(resultado, ensure_ascii=False, indent=1) + "\n",
                       encoding="utf-8")
    parcial.replace(CACHE)
    return resultado


def _edad(iso):
    try:
        return datetime.now().astimezone() - datetime.fromisoformat(iso)
    except Exception:                                            # noqa: BLE001
        return None


def tanda():
    """La ultima tanda registrada, con su edad. Sin nucleo al lado tambien.

    Vive aparte de `leer()` a proposito: leer la cache no necesita que el arbol
    del nucleo este ahi, y mezclarlas hacia que una prueba de la cache fallara
    en cualquier maquina donde el nucleo no fuera vecino -- que es toda menos la
    nuestra. Una prueba que depende del vecindario no prueba el codigo.
    """
    salida = {"estado": sensores.NO_DATA,
              "causa": "no hay ninguna tanda registrada · corre: "
                       "python3 -m sensores.preceptor --medir"}
    if CACHE.is_file():
        try:
            crudo = json.loads(CACHE.read_text(encoding="utf-8"))
        except ValueError:
            crudo = None
        if isinstance(crudo, dict) and crudo.get("pruebas"):
            edad = _edad(crudo.get("medido", ""))
            rancia = edad is None or edad > RANCIA
            salida = {
                "estado": "ok",
                "pruebas": crudo["pruebas"], "suites": crudo["suites"],
                "verde": bool(crudo.get("verde")),
                "medido": crudo.get("medido"),
                "rancia": rancia,
                "causa": "medida hace mas de 24 h · no dice nada del arbol de hoy"
                          if rancia else "",
            }
    return salida


def leer():
    try:
        corta, larga = _version()
    except Exception as e:                                       # noqa: BLE001
        return sensores.hueco(
            "el nucleo publico no esta junto a este panel · su version se lee "
            "de su arbol, y sin arbol no hay version", type(e).__name__)
    return sensores.dato(version=corta, huella=larga, tanda=tanda(),
                         ruta="preceptor-os-core/")


registro.registrar("preceptor", leer)


if __name__ == "__main__":
    if "--medir" in sys.argv:
        print(json.dumps(medir(), ensure_ascii=False, indent=1))
    else:
        print(json.dumps(leer(), ensure_ascii=False, indent=1))
