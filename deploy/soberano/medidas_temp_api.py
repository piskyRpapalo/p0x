#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""El buzon temporal de medidas, en el Soberano. Append-only y sin dependencias.

POR QUE NO ES FastAPI, Y SE DECLARA
-----------------------------------
El encargo decia «el gateway FastAPI del Soberano». Ese gateway NO EXISTE: aqui
escuchan nginx, la app del MVP y open-webui, y FastAPI no esta instalado en
ningun vento de esta maquina --ni hay sudo para ponerlo--. Se hace con
`http.server` de la biblioteca estandar: mismo contrato, misma tabla, cero
instalacion. Es ademas la regla que el MVP ya se aplica.

LO QUE ESTE BUZON NO PUEDE HACER HOY, Y CONVIENE SABERLO ANTES DE APUNTARLE
--------------------------------------------------------------------------
`api.preceptoros.org` resuelve a Cloudflare y sale por el tunel de la-fragua;
este proceso vive en el Beelink. Y `downloads.preceptoros.org` SI apunta a la IP
publica de este nodo --95.92.164.201-- pero no responde: el puerto no esta
abierto desde fuera. O sea que un navegador ajeno NO llega aqui todavia. Si
llegan: el navegador del propio Soberano y cualquier cosa de la tailnet.

Se escribe igual porque el trabajo que falta es de red, no de codigo, y porque
el guion de sincronizacion ya puede vaciarlo hacia la-fragua cuando su endpoint
exista.

APPEND-ONLY, COMO `dead_path.jsonl`
-----------------------------------
Solo INSERT. `processed` la mueve el sincronizador y nadie mas. No hay DELETE ni
UPDATE de contenido: un registro que se puede editar no es un registro.

SE ATA A 127.0.0.1 POR DEFECTO. Abrirlo a la tailnet es `--host`, a mano y
sabiendo lo que se hace. Un buzon que acepta escrituras y nace escuchando en
todas las interfaces es la clase de servicio que este canon prohibe crear sin
firma.
"""
from __future__ import annotations

import argparse
import json
import sqlite3
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

BASE = Path.home() / ".preceptoros" / "medidas_temp.db"
RUTA = "/api/v1/medidas-temp"
TOPE = 256 * 1024          # un cuerpo mayor que esto no es una medida

ESQUEMA = """
CREATE TABLE IF NOT EXISTS medidas (
  id           INTEGER PRIMARY KEY AUTOINCREMENT,
  timestamp    TEXT NOT NULL,
  user_hash    TEXT,
  payload_json TEXT NOT NULL,
  processed    INTEGER NOT NULL DEFAULT 0
);
"""


def abrir(ruta: Path) -> sqlite3.Connection:
    ruta.parent.mkdir(parents=True, exist_ok=True)
    con = sqlite3.connect(ruta, check_same_thread=False)
    con.executescript(ESQUEMA)
    con.commit()
    return con


class Buzon(BaseHTTPRequestHandler):
    con: sqlite3.Connection = None       # lo pone `main`
    server_version = "buzon-medidas"     # sin version de Python en la cabecera

    def _responder(self, codigo, cuerpo):
        crudo = json.dumps(cuerpo, ensure_ascii=False).encode()
        self.send_response(codigo)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(crudo)))
        # Solo el sitio publico. Un buzon de escritura con `*` acepta lo que le
        # mande cualquier pagina que el visitante tenga abierta.
        self.send_header("Access-Control-Allow-Origin", "https://preceptoros.org")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()
        self.wfile.write(crudo)

    def do_OPTIONS(self):                                    # noqa: N802
        self._responder(204, {})

    def do_GET(self):                                        # noqa: N802
        if self.path != "/salud":
            self._responder(404, {"error": "no existe"}); return
        n = self.con.execute("SELECT COUNT(*) FROM medidas").fetchone()[0]
        sin = self.con.execute(
            "SELECT COUNT(*) FROM medidas WHERE processed = 0").fetchone()[0]
        self._responder(200, {"vivo": True, "medidas": n, "sin_sincronizar": sin})

    def do_POST(self):                                       # noqa: N802
        if self.path != RUTA:
            self._responder(404, {"error": "no existe"}); return
        try:
            largo = int(self.headers.get("Content-Length") or 0)
        except ValueError:
            self._responder(400, {"error": "Content-Length ilegible"}); return
        if largo <= 0 or largo > TOPE:
            self._responder(413, {"error": f"cuerpo fuera de rango (tope {TOPE} B)"}); return
        try:
            datos = json.loads(self.rfile.read(largo))
        except (json.JSONDecodeError, UnicodeDecodeError):
            self._responder(400, {"error": "el cuerpo no es JSON"}); return
        if not isinstance(datos, dict):
            self._responder(400, {"error": "se esperaba un objeto"}); return
        # `user_hash` puede faltar --quien no se hizo firma-- y eso es un hecho,
        # no un hueco que rellenar con un anonimo inventado.
        huella = datos.get("user_hash")
        if huella is not None and not isinstance(huella, str):
            self._responder(400, {"error": "user_hash debe ser texto o faltar"}); return
        cur = self.con.execute(
            "INSERT INTO medidas (timestamp, user_hash, payload_json) VALUES (?,?,?)",
            (datetime.now(timezone.utc).isoformat(timespec="seconds"), huella,
             json.dumps(datos, ensure_ascii=False)))
        self.con.commit()
        self._responder(201, {"guardado": True, "id": cur.lastrowid})

    def log_message(self, formato, *args):
        # El registro por defecto escupe la IP de quien escribe en stderr. Aqui
        # no se guarda quien, solo que. Se calla a proposito.
        return


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--host", default="127.0.0.1",
                    help="127.0.0.1 por defecto. La tailnet se pide a mano")
    ap.add_argument("--puerto", type=int, default=8791)
    ap.add_argument("--base", type=Path, default=BASE)
    a = ap.parse_args(argv)

    Buzon.con = abrir(a.base)
    srv = ThreadingHTTPServer((a.host, a.puerto), Buzon)
    print(json.dumps({"escuchando": f"http://{a.host}:{a.puerto}", "ruta": RUTA,
                      "base": str(a.base)}, ensure_ascii=False), flush=True)
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        print("\nparado a mano")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
