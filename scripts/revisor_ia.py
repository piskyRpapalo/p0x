#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""La AI revisora · lee conversaciones de la web y saca patrones, en local.

QUE HACE Y QUE NO SALE DE AQUI
------------------------------
Lee conversaciones de un SQLite propio, se las pasa a un modelo pequeño de la
Ollama DE ESTA MAQUINA, y escribe lo que encuentre en `mente/
revision_conversaciones.md`. No hay una sola llamada a nada que no sea
`127.0.0.1`. El silicio es la frontera y aqui se nota en el codigo, no en una
promesa: si alguien mete un `requests.post` a un dominio de fuera, se ve en el
diff.

POR QUE UN 3B Y NO EL MEJOR QUE HAYA
------------------------------------
Resumir patrones no necesita el modelo mas listo: necesita el que no ocupe la
RAM que hace falta para servir la web. `llama3.2:3b` son 2 GB. Y NO se usa
`preceptor-v7`, que pesa lo mismo: esta entrenado para responder `NO_DATA`, que
es exactamente la conducta que arruina un trabajo de analisis.

PROPOSE-ONLY POR DEFECTO
------------------------
Sin `--ejecutar` no escribe ni marca nada: enseña cuantas conversaciones hay sin
revisar y para. Es la misma guarda que llevan los trainers de la forja, y existe
porque un cron que empieza a escribir en el Segundo Cerebro sin que nadie lo
haya visto funcionar una vez es como se llena un repositorio de ruido.

APPEND-ONLY, COMO `dead_path.jsonl`
-----------------------------------
El informe se AÑADE al final del fichero con su fecha. Nunca se reescribe una
entrada anterior: una revision que corrige a la de ayer se lee entera al lado de
la de ayer, y asi se ve que cambio de opinion el sistema y cuando.
"""
from __future__ import annotations

import argparse
import json
import sqlite3
import sys
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
BASE = Path.home() / ".preceptoros" / "conversaciones.db"
INFORME = RAIZ / "mente" / "revision_conversaciones.md"
OLLAMA = "http://127.0.0.1:11434/api/generate"
MODELO = "llama3.2:3b"
LOTE = 50

# La tabla y su indice de texto completo. `revisada` NO se borra ni se
# actualiza a mano: la escribe este guion y es lo unico que impide releer mil
# veces lo mismo. `user_hash` puede faltar --quien no se hizo firma-- y eso es
# un hecho, no un hueco que rellenar.
ESQUEMA = """
CREATE TABLE IF NOT EXISTS conversaciones (
  id             INTEGER PRIMARY KEY AUTOINCREMENT,
  timestamp      TEXT NOT NULL,
  model_used     TEXT NOT NULL,
  user_prompt    TEXT NOT NULL,
  model_response TEXT NOT NULL,
  user_hash      TEXT,
  session_id     TEXT NOT NULL,
  revisada       INTEGER NOT NULL DEFAULT 0
);
CREATE VIRTUAL TABLE IF NOT EXISTS conversaciones_fts
  USING fts5(user_prompt, model_response, content='conversaciones', content_rowid='id');
CREATE TRIGGER IF NOT EXISTS conversaciones_ai AFTER INSERT ON conversaciones BEGIN
  INSERT INTO conversaciones_fts(rowid, user_prompt, model_response)
  VALUES (new.id, new.user_prompt, new.model_response);
END;
"""

PETICION = """Analiza estas conversaciones entre personas y un asistente.

Responde SOLO con un objeto JSON, sin texto antes ni despues, con exactamente estas tres claves:
{"patrones": [...], "no_data": [...], "sugerencias": [...]}

- "patrones": confusiones o preguntas que se repiten.
- "no_data": casos en que el asistente dijo que no sabia, y que pregunto la persona despues.
- "sugerencias": cambios concretos para las instrucciones del asistente.

Cada lista contiene frases cortas. Si una lista no tiene nada, dejala vacia: no inventes.

CONVERSACIONES:
"""


def abrir(ruta: Path) -> sqlite3.Connection:
    ruta.parent.mkdir(parents=True, exist_ok=True)
    con = sqlite3.connect(ruta)
    con.executescript(ESQUEMA)
    con.commit()
    return con


def sin_revisar(con, limite):
    cur = con.execute(
        "SELECT id, timestamp, model_used, user_prompt, model_response "
        "FROM conversaciones WHERE revisada = 0 ORDER BY id LIMIT ?", (limite,))
    return cur.fetchall()


def preguntar(modelo, texto, timeout):
    """Un turno contra la Ollama local. Si no responde, se dice y se para --
    un informe a medias con forma de informe entero es peor que ninguno."""
    cuerpo = json.dumps({"model": modelo, "prompt": texto, "stream": False,
                         "format": "json",
                         "options": {"temperature": 0.2, "num_predict": 700}}).encode()
    pet = urllib.request.Request(OLLAMA, cuerpo, {"Content-Type": "application/json"})
    with urllib.request.urlopen(pet, timeout=timeout) as r:
        return json.loads(r.read()).get("response", "")


def escribir(informe: Path, datos, n, modelo):
    informe.parent.mkdir(parents=True, exist_ok=True)
    ahora = datetime.now(timezone.utc).isoformat(timespec="seconds")
    lineas = [f"\n## {ahora} · {n} conversaciones · {modelo}\n"]
    for clave, titulo in (("patrones", "Patrones"),
                          ("no_data", "Donde dijo que no sabia"),
                          ("sugerencias", "Sugerencias para el prompt")):
        v = datos.get(clave) or []
        lineas.append(f"\n**{titulo}**\n")
        if not v:
            lineas.append("\n- NO_DATA — el revisor no encontro nada en este lote.\n")
        else:
            for x in v:
                lineas.append(f"\n- {str(x).strip()}\n")
    if not informe.exists():
        informe.write_text(
            "# Revision de conversaciones\n\n"
            "Lo escribe `scripts/revisor_ia.py` con un modelo local, y se AÑADE: "
            "ninguna entrada se reescribe. Una revision que corrige a la de ayer se "
            "lee al lado de la de ayer.\n", encoding="utf-8")
    with informe.open("a", encoding="utf-8") as f:
        f.write("".join(lineas))


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--ejecutar", action="store_true",
                    help="sin esto no escribe ni marca nada: cuenta y para")
    ap.add_argument("--base", type=Path, default=BASE)
    ap.add_argument("--modelo", default=MODELO)
    ap.add_argument("--lote", type=int, default=LOTE)
    ap.add_argument("--timeout", type=float, default=600.0)
    # LA BUSQUEDA VIVE AQUI Y NO EN UNA PAGINA `/admin`, y el motivo es de
    # presupuesto, no de gusto: la web esta en 9 de 9 paginas y una decima pide
    # amnistia firmada. Ademas una consola local no necesita autenticacion
    # porque no esta expuesta: la frontera la pone el silicio, no un login.
    ap.add_argument("--buscar", metavar="TEXTO",
                    help="busca en las conversaciones con el indice FTS5 y para")
    a = ap.parse_args(argv)

    con = abrir(a.base)
    if a.buscar:
        cur = con.execute(
            "SELECT c.id, c.timestamp, c.model_used, c.user_prompt, c.model_response "
            "FROM conversaciones_fts f JOIN conversaciones c ON c.id = f.rowid "
            "WHERE conversaciones_fts MATCH ? ORDER BY c.id DESC LIMIT 25", (a.buscar,))
        filas_b = cur.fetchall()
        print(f"{len(filas_b)} coincidencias de {a.buscar!r}")
        for f in filas_b:
            print(f"\n[{f[0]}] {f[1]} · {f[2]}\n  PERSONA:   {f[3][:160]}"
                  f"\n  ASISTENTE: {f[4][:160]}")
        return 0
    filas = sin_revisar(con, a.lote)
    total = con.execute("SELECT COUNT(*) FROM conversaciones").fetchone()[0]
    print(json.dumps({"base": str(a.base), "conversaciones": total,
                      "sin_revisar": len(filas), "modelo": a.modelo},
                     ensure_ascii=False))

    if not filas:
        print("Nada que revisar. No se escribe informe: un informe sin datos "
              "es una entrada de diario que dice que no hubo diario.")
        return 0
    if not a.ejecutar:
        print("\nPLAN, no ejecucion. Anade --ejecutar cuando el carbono firme.")
        return 0

    bloque = "\n\n".join(
        f"[{i}] modelo={f[2]}\nPERSONA: {f[3]}\nASISTENTE: {f[4]}"
        for i, f in enumerate(filas, 1))
    try:
        crudo = preguntar(a.modelo, PETICION + bloque, a.timeout)
    except (urllib.error.URLError, TimeoutError, OSError) as e:
        print(f"NO_DATA · la Ollama local no respondio: {e}", file=sys.stderr)
        return 1
    try:
        datos = json.loads(crudo)
    except json.JSONDecodeError:
        print("NO_DATA · el revisor no devolvio JSON. No se marca nada como "
              "revisado: se vuelve a intentar en la pasada siguiente.",
              file=sys.stderr)
        return 1

    escribir(INFORME, datos, len(filas), a.modelo)
    con.executemany("UPDATE conversaciones SET revisada = 1 WHERE id = ?",
                    [(f[0],) for f in filas])
    con.commit()
    print(f"Escrito en {INFORME} · {len(filas)} marcadas como revisadas")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
