#!/usr/bin/env python3
"""Deriva `preceptoros-web/public/modelos.json` del catalogo REAL de Ollama.

POR QUE ESTE FICHERO NO SE ESCRIBE A MANO
-----------------------------------------
La regla de la casa es que una cifra publicada es una MEDICION. Un catalogo de
modelos escrito a mano envejece igual que envejecio la linea de credenciales
que decia «526 pruebas» cuando el gate medía otra cosa: nadie lo nota hasta
que ya lleva meses mintiendo. Aqui el nombre, el tamano, la familia, la
cuantizacion y la ventana de contexto salen del disco y del demonio, o no
salen.

QUE SE PUBLICA, Y POR QUE NO ES TODO
------------------------------------
El nodo tiene NUEVE modelos en Ollama. Publicarlos todos seria publicar el
inventario de una maquina personal --con sus experimentos y sus nombres
internos-- y eso es telemetria del rack, que por doctrina vive en el Ojo y no
en la web.

La regla de publicacion es DERIVADA, no una lista a mano: se publica lo que la
Forja DECLARA, es decir lo que tiene un `.Modelfile` en
`preceptor-lora/modelfiles/`, mas la base que ese Modelfile necesita. Un
adaptador sin su base no se puede usar, asi que la base es producto tambien.

Todo lo demas se queda en casa. Y el catalogo dice cuantos se quedaron fuera y
por que: un filtro que no declara lo que descarta es un filtro que no se puede
auditar.

    python3 ~/p0x/bin/modelos-servidos.py         # ensena lo que escribiria
    python3 ~/p0x/bin/modelos-servidos.py --si    # lo escribe
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

CASA = Path.home()
LORA = CASA / "p0x" / "preceptor-lora"
MODELFILES = LORA / "modelfiles"
SALIDA = CASA / "preceptoros-web" / "public" / "modelos.json"

# El demonio puede estar en la tailnet y no en loopback: en este nodo
# OLLAMA_HOST apunta a la direccion de tailnet, no a 127.0.0.1. Se lee del
# entorno, que es de donde lo lee el propio `ollama`, en vez de fijar una
# direccion -- incrustarla la deja congelada en el repo el dia que cambie, y
# ademas es justo lo que la guardia de higiene de este repo prohibe.
ANFITRION = os.environ.get("OLLAMA_HOST", "http://127.0.0.1:11434").rstrip("/")
if not ANFITRION.startswith("http"):
    ANFITRION = "http://" + ANFITRION


def catalogo_vivo():
    """Lo que Ollama dice tener AHORA. Si no contesta, no se inventa nada."""
    try:
        with urllib.request.urlopen(ANFITRION + "/api/tags", timeout=10) as r:
            return {m["name"]: m for m in json.load(r).get("models", [])}, None
    except (urllib.error.URLError, OSError, ValueError, KeyError) as e:
        return {}, f"{type(e).__name__}: {e}"


def declarados():
    """Lo que la Forja declara: un registro por Modelfile.

    Se saca `FROM` (la base), `ADAPTER` (que lo convierte en adaptador y no en
    modelo suelto) y `PARAMETER num_ctx` (la ventana, que METRICAS_NORMA fija
    como norma). Nada de esto se teclea aqui: se lee del fichero que ya usa
    `ollama create`, asi que no puede separarse de la realidad sin que la
    creacion del modelo tambien falle.
    """
    if not MODELFILES.is_dir():
        # Un generador NO puede informar de un fallo con `return valor`: eso
        # se convierte en el valor de StopIteration y quien itera ve una lista
        # vacia, indistinguible de «la Forja no declara nada todavia». Se
        # levanta, que es la unica forma de que se note.
        raise FileNotFoundError(f"no existe {MODELFILES}")
    for mf in sorted(MODELFILES.glob("*.Modelfile")):
        t = mf.read_text(encoding="utf-8")
        # Los comentarios fuera antes de buscar directivas: este Modelfile
        # EXPLICA su base en prosa ademas de declararla, y un `FROM` citado en
        # un comentario no es un `FROM`.
        vivo = "\n".join(l for l in t.splitlines() if not l.lstrip().startswith("#"))
        base = re.search(r"^\s*FROM\s+(\S+)", vivo, re.M)
        adaptador = re.search(r"^\s*ADAPTER\s+(\S+)", vivo, re.M)
        ctx = re.search(r"^\s*PARAMETER\s+num_ctx\s+(\d+)", vivo, re.M)
        if not base:
            # Se salta, pero NO en silencio: un Modelfile sin FROM es un
            # defecto de la Forja y tiene que doler en el sitio donde se mira.
            print(f"AVISO · {mf.name} no declara FROM: fuera del catalogo",
                  file=sys.stderr)
            continue
        yield {
            "nombre": mf.stem,
            "modelo_base": base.group(1),
            "es_adaptador": bool(adaptador),
            "ventana_contexto": int(ctx.group(1)) if ctx else None,
            "declarado_en": f"preceptor-lora/modelfiles/{mf.name}",
        }


def medido(clave, valor, unidad, como):
    return {"clave": clave, "estado": "MEDIDO", "valor": valor,
            "unidad": unidad, "como": como}


def sin_dato(clave, causa, unidad):
    return {"clave": clave, "estado": "NO_DATA", "valor": None,
            "unidad": unidad, "causa": causa}


def ficha(reg, vivos):
    """Un registro publicable. Lo que Ollama no confirme sale NO_DATA."""
    m = vivos.get(reg["nombre"]) or vivos.get(reg["nombre"] + ":latest")
    f = {
        "id": reg["nombre"],
        "modelo_base": reg["modelo_base"],
        "tipo": "adaptador" if reg["es_adaptador"] else "modelo",
        "declarado_en": reg["declarado_en"],
        # Servir es otra puerta. Hoy no hay endpoint publico de chat y D3
        # --la cola maxima del Jetson-- sigue sin firmar, asi que decir
        # «servido» aqui seria prometer algo que no existe.
        "servido_publicamente": False,
        "causa_no_servido": "sin endpoint publico de chat; D3 sin firmar",
    }
    if m is None:
        f["metricas"] = [sin_dato("modelo_tamano_bytes",
                                  "declarado por la Forja pero no presente en el "
                                  "catalogo de Ollama de este nodo", "bytes")]
        return f
    det = m.get("details") or {}
    f["metricas"] = [
        medido("modelo_tamano_bytes", m["size"], "bytes", "Ollama /api/tags"),
        medido("parametros", det.get("parameter_size"), "parametros",
               "Ollama /api/tags · details.parameter_size"),
        medido("cuantizacion", det.get("quantization_level"), "nivel",
               "Ollama /api/tags · details.quantization_level"),
        medido("familia", det.get("family"), "familia",
               "Ollama /api/tags · details.family"),
    ]
    f["metricas"].append(
        medido("ventana_contexto", reg["ventana_contexto"], "tokens",
               "PARAMETER num_ctx del Modelfile")
        if reg["ventana_contexto"] else
        sin_dato("ventana_contexto", "el Modelfile no fija num_ctx", "tokens"))
    return f


def construir():
    vivos, fallo = catalogo_vivo()
    regs = list(declarados())
    fichas = []
    for r in regs:
        fichas.append(ficha(r, vivos))
        # La base de un adaptador es producto: sin ella no se puede usar.
        if r["es_adaptador"] and r["modelo_base"] not in [f["id"] for f in fichas]:
            b = vivos.get(r["modelo_base"])
            fichas.append({
                "id": r["modelo_base"],
                "modelo_base": r["modelo_base"],
                "tipo": "base",
                "declarado_en": r["declarado_en"] + " (FROM)",
                "servido_publicamente": False,
                "causa_no_servido": "sin endpoint publico de chat; D3 sin firmar",
                "metricas": [
                    medido("modelo_tamano_bytes", b["size"], "bytes", "Ollama /api/tags"),
                    medido("parametros", (b.get("details") or {}).get("parameter_size"),
                           "parametros", "Ollama /api/tags"),
                    medido("cuantizacion", (b.get("details") or {}).get("quantization_level"),
                           "nivel", "Ollama /api/tags"),
                    medido("familia", (b.get("details") or {}).get("family"),
                           "familia", "Ollama /api/tags"),
                ] if b else [sin_dato("modelo_tamano_bytes",
                                      "la base declarada no esta en Ollama", "bytes")],
            })
    ahora = datetime.now(timezone.utc).replace(microsecond=0)
    return {
        "esquema": 1,
        "estado": "MEDIDO" if not fallo else "PARCIAL",
        "ultima_lectura": ahora.isoformat(),
        "nota": "Catalogo DERIVADO: los nombres y las bases salen de los "
                "Modelfile de la Forja; los tamanos, de Ollama. Nada esta "
                "escrito a mano. Se publica lo que la Forja declara mas la "
                "base que necesita: el resto del catalogo del nodo es privado.",
        "fuente": "preceptor-lora/modelfiles/*.Modelfile + Ollama /api/tags",
        "modelos": fichas,
        "no_publicados": (
            medido("no_publicados", max(0, len(vivos) - len(fichas)), "modelos",
                   "modelos presentes en Ollama sin Modelfile que los declare")
            if not fallo else
            sin_dato("no_publicados", f"Ollama no contesto: {fallo}", "modelos")),
        "lectura_ollama": (sin_dato("catalogo_ollama", fallo, "modelos")
                           if fallo else
                           medido("catalogo_ollama", len(vivos), "modelos",
                                  "Ollama /api/tags")),
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--si", action="store_true", help="escribe el fichero")
    a = ap.parse_args()
    d = construir()
    txt = json.dumps(d, ensure_ascii=False, indent=1) + "\n"
    if not a.si:
        print(txt)
        print(f"[dry-run] {len(txt.encode())} B · usa --si para escribir",
              file=sys.stderr)
        return 0
    SALIDA.write_text(txt, encoding="utf-8")
    n = sum(1 for m in d["modelos"] if m["tipo"] != "base")
    print(f"escrito {SALIDA} · {len(txt.encode())} B · {len(d['modelos'])} fichas "
          f"({n} de la Forja + bases)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
