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
import os
import sys
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI))


def _cargar_env(ruta=None):
    """Lee `.env` si existe. Lo que ya venga en el entorno MANDA.

    Ese orden importa: un fichero no puede pisar lo que alguien puso a mano al
    arrancar, porque entonces `NEXO_GATEWAY=... python3 servidor.py` mentiria
    sobre lo que hace. Ausente no es un fallo -- todo esto es opcional.
    """
    ruta = ruta or (AQUI / ".env")
    try:
        crudo = ruta.read_text(encoding="utf-8")
    except OSError:
        return {}
    puestas = {}
    for linea in crudo.splitlines():
        linea = linea.strip()
        if not linea or linea.startswith("#") or "=" not in linea:
            continue
        clave, _, valor = linea.partition("=")
        clave, valor = clave.strip(), valor.strip().strip('"').strip("'")
        if clave and clave not in os.environ:
            os.environ[clave] = valor
            puestas[clave] = valor
    return puestas


_cargar_env()

import fragmentos                                               # noqa: E402
import sensores                                                  # noqa: E402
import vigia as _vigia                                           # noqa: E402
from sensores import registro                                    # noqa: E402

# Importar un sensor es registrarlo. La lista es esta y no un barrido del
# directorio, por el motivo escrito en `sensores/registro.py`.
from sensores import (adsb, cerebro, cinek, jardin, lora, nodos,  # noqa: E402,F401
                      observe, preceptor, soberania, timers)

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
    "/api/cerebro": lambda: registro.uno("cerebro"),
    "/api/observe": lambda: registro.uno("observe"),
    "/api/adsb": lambda: registro.uno("adsb"),
    "/api/nodos": lambda: registro.uno("nodos"),
}

# Cuanto espera un flujo quieto antes de mandar un latido. Un proxy silencioso
# por el medio cierra lo que lleva rato callado, y el navegador no distingue esa
# muerte de un fallo -- asi que se habla aunque no haya novedad.
LATIDO = 25.0

VERSION = "0.2.0"

# El vigia: un hilo que refresca y muchos flujos que solo miran. Se arranca en
# `construir()` y no al importar, para que las pruebas puedan levantar el
# servidor sin dejar un hilo suelto por cada caso.
VIGIA = _vigia.Vigia()

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
        if ruta == "/api/flujo":
            return self._flujo()
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

    def _flujo(self):
        """Server-Sent Events. Lo que viaja es HTML terminado, no JSON.

        El navegador no parsea nada ni decide nada: coge la cadena y la coloca.
        Y se manda **solo lo que ha cambiado**, no las siete tarjetas cada vez
        -- con seis quietas y una viva, eso son 386 bytes en vez de 8 KB.
        """
        if self.command == "HEAD":
            return self._responder(200, b"", "text/event-stream; charset=utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "text/event-stream; charset=utf-8")
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Accel-Buffering", "no")
        self.end_headers()
        self.close_connection = True

        visto = -1
        try:
            while True:
                tarjetas, version, medido = (
                    VIGIA.instantanea() if visto < 0 else VIGIA.espera(visto, LATIDO))
                if version != visto:
                    for nombre, html in tarjetas.items():
                        self._evento("m-" + nombre, html)
                    visto = version
                # El latido va siempre: es lo que le dice a la cara que sigue
                # habiendo alguien al otro lado aunque nada haya cambiado.
                self._evento("latido", medido)
        except (BrokenPipeError, ConnectionResetError):
            pass                      # la pestaña se cerro. No es un fallo.
        except OSError:
            pass

    def _evento(self, nombre, dato):
        # Un `data:` por linea, que es lo que exige el formato. Los fragmentos
        # ya vienen en una sola, pero un dato de fuera podria no venirlo.
        cuerpo = f"event: {nombre}\n"
        for linea in str(dato).split("\n"):
            cuerpo += f"data: {linea}\n"
        self.wfile.write((cuerpo + "\n").encode("utf-8"))
        self.wfile.flush()

    def _estatico(self, ruta):
        # `/static/...` y `/` cuelgan del mismo arbol: el directorio `static`
        # vive dentro de `estatico/`, asi que la ruta ya cuadra sin traduccion.
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


def construir(puerto=PUERTO, anfitrion=ANFITRION, ruidoso=False, vigilar=True):
    if vigilar and VIGIA._hilo is None:
        VIGIA.arrancar()
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
