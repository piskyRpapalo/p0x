#!/usr/bin/env python3
"""El Nexo · micro-servidor de solo lectura para el panel del orquestador.

Biblioteca estandar y nada mas. Ata a `127.0.0.1` a proposito: exponerlo al
tailnet es una decision aparte, se firma aparte, y no se hereda de haber
arrancado esto una vez.

**Solo lee.** No hay un solo verbo que escriba: ni POST, ni PUT, ni DELETE. Un
panel que puede apagar cosas es una superficie de mando, y una superficie de
mando pide una conversacion sobre quien la alcanza que aqui no se ha tenido.
Lo que este panel hace es mirar.
"""

import argparse
import json
import sys
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI))

import sensores                                                  # noqa: E402
from sensores import registro                                    # noqa: E402

# Importar un sensor es registrarlo. La lista es esta y no un barrido del
# directorio, por el motivo escrito en `sensores/registro.py`.
from sensores import (cinek, jardin, lora, nodos, preceptor,      # noqa: E402,F401
                      soberania, timers)

PUERTO = 8765
ANFITRION = "127.0.0.1"
ESTATICO = AQUI / "estatico"

# Lo que se puede pedir por HTTP, y nada mas. Una lista blanca y no un
# `getattr` sobre el nombre de la ruta: con `getattr` cualquier atributo del
# modulo se vuelve alcanzable desde fuera, y eso no es una API, es una puerta.
RUTAS = {
    "/api/salud": lambda: {"estado": "ok", "version": VERSION,
                           "sensores": sorted(registro.SENSORES),
                           "medido": sensores.ahora()},
    "/api/estado": lambda: registro.todo(),
    "/api/soberania": lambda: registro.uno("soberania"),
    "/api/timers": lambda: registro.uno("timers"),
    "/api/preceptor": lambda: registro.uno("preceptor"),
    "/api/lora": lambda: registro.uno("lora"),
    "/api/cinek": lambda: registro.uno("cinek"),
    "/api/jardin": lambda: registro.uno("jardin"),
    "/api/nodos": lambda: registro.uno("nodos"),
}

VERSION = "0.1.0"

TIPOS = {".html": "text/html; charset=utf-8", ".css": "text/css; charset=utf-8",
         ".js": "text/javascript; charset=utf-8", ".svg": "image/svg+xml",
         ".png": "image/png", ".ico": "image/x-icon"}


class Nexo(BaseHTTPRequestHandler):
    server_version = "Nexo/" + VERSION
    protocol_version = "HTTP/1.1"

    def log_message(self, formato, *args):
        """Silencio por defecto. Un panel que se refresca cada 30 s llena un
        journal de ruido y entierra la linea que importaba."""
        if self.server.ruidoso:
            super().log_message(formato, *args)

    def _responder(self, codigo, cuerpo, tipo):
        self.send_response(codigo)
        self.send_header("Content-Type", tipo)
        self.send_header("Content-Length", str(len(cuerpo)))
        # Cero cache: el panel pregunta porque quiere el dato de ahora.
        self.send_header("Cache-Control", "no-store")
        # Nada de fuera entra en esta pagina, ni siquiera si alguien la enmarca.
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("X-Frame-Options", "DENY")
        self.end_headers()
        if self.command != "HEAD":
            self.wfile.write(cuerpo)

    def _json(self, datos, codigo=200):
        cuerpo = (json.dumps(datos, ensure_ascii=False, indent=1) + "\n").encode("utf-8")
        self._responder(codigo, cuerpo, "application/json; charset=utf-8")

    def do_GET(self):
        ruta = self.path.split("?", 1)[0].rstrip("/") or "/"
        if ruta.startswith("/api"):
            fabrica = RUTAS.get(ruta)
            if fabrica is None:
                return self._json({"estado": sensores.NO_DATA,
                                   "causa": f"no hay ninguna ruta «{ruta}»"}, 404)
            try:
                return self._json(fabrica())
            except Exception as e:                               # noqa: BLE001
                # Ni con el sensor entero roto se devuelve un 500 mudo: el panel
                # tiene que poder pintar el hueco y decir por que.
                return self._json({"estado": sensores.NO_DATA,
                                   "causa": f"la lectura fallo · {type(e).__name__}"}, 200)
        return self._estatico(ruta)

    do_HEAD = do_GET

    def _estatico(self, ruta):
        nombre = "index.html" if ruta == "/" else ruta.lstrip("/")
        destino = (ESTATICO / nombre).resolve()
        # La comprobacion que impide servir medio disco por una ruta con `..`.
        if not str(destino).startswith(str(ESTATICO.resolve()) + "/") \
                and destino != ESTATICO.resolve():
            return self._responder(403, b"fuera de sitio\n", "text/plain; charset=utf-8")
        if not destino.is_file():
            return self._responder(404, b"no esta\n", "text/plain; charset=utf-8")
        tipo = TIPOS.get(destino.suffix, "application/octet-stream")
        self._responder(200, destino.read_bytes(), tipo)


def construir(puerto=PUERTO, anfitrion=ANFITRION, ruidoso=False):
    servidor = ThreadingHTTPServer((anfitrion, puerto), Nexo)
    servidor.ruidoso = ruidoso
    servidor.daemon_threads = True
    return servidor


def main(argv=None):
    p = argparse.ArgumentParser(description="El Nexo · panel de solo lectura")
    p.add_argument("--puerto", type=int, default=PUERTO)
    p.add_argument("--anfitrion", default=ANFITRION,
                   help="por defecto 127.0.0.1 · salir de ahi se firma aparte")
    p.add_argument("--ruidoso", action="store_true", help="una linea por peticion")
    # El unico sensor que sale de la maquina es el de nodos, y por eso es el
    # unico con interruptor. Con esto puesto el panel entero se queda dentro.
    p.add_argument("--sin-red", action="store_true",
                   help="no preguntar al tailnet · los nodos remotos salen NO_DATA")
    args = p.parse_args(argv)
    nodos.sin_red(args.sin_red)
    servidor = construir(args.puerto, args.anfitrion, args.ruidoso)
    if args.sin_red:
        print("red cortada · los nodos remotos no se preguntan")
    print(f"Nexo · http://{args.anfitrion}:{args.puerto}  ·  ctrl-c para parar")
    try:
        servidor.serve_forever()
    except KeyboardInterrupt:
        print("\nparado.")
    finally:
        servidor.server_close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
