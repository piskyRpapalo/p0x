#!/usr/bin/env python3
"""El Ojo del Soberano · consola de operaciones del rack. Solo loopback.

POR QUE VIVE AQUI Y NO EN EL PRODUCTO
--------------------------------------
El encargo original pedia meter esto en `preceptor/interface/dashboard.html`.
No cabe ahi, por dos razones que no son de estilo:

  * ese dashboard es LA CARA DEL USUARIO -- memoria, frontera, camino, perfil.
    Se sirve a quien instale PreceptorOS. Meterle `OLLAMA :: ONLINE`, el estado
    del Doogee y las latencias de la-fragua es enviar el rack del Soberano a la
    app de cada persona, con IPs de tailnet dentro de un producto cuya promesa
    entera es que el contexto no se escapa.
  * `estado.py` del producto guarda las banderas de INSTALACION, y su propio
    docstring prohibe crear dos verdades sobre el mismo hecho. `/api/estado` ya
    existe sirviendolas.

Asi que el Ojo es suyo: su directorio, su servidor, su puerto. Gana tres cosas
-- cero riesgo para el gate del producto, cero fuga de rack, y puede enseñar
justo lo que el producto nunca debe.

DOS REGLAS DE ESTE SERVIDOR
---------------------------
1. **Solo 127.0.0.1.** No es un detalle de configuracion: la auditoria de hoy
   encontro un `python3 -m http.server` en 0.0.0.0:8080, sin auth y sin logs,
   expuesto a la LAN y a la tailnet entera durante seis horas porque nadie
   miraba la interfaz, solo el numero. Esta consola enseña el rack: si se ata a
   0.0.0.0, lo reparte.
2. **No mide. Pinta.** Sirve lo que `recolector.py` dejo escrito y calcula la
   frescura al vuelo. Un panel que mide al pintar se cuelga justo cuando el
   rack cae -- que es exactamente el momento en que hace falta.
"""
from __future__ import annotations

import argparse
import json
import sys
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

AQUI = Path(__file__).resolve().parent
ESTADO = AQUI.parent / "estado.json"

ESTATICOS = {
    "/": ("ojo.html", "text/html; charset=utf-8"),
    "/ojo.html": ("ojo.html", "text/html; charset=utf-8"),
    "/ojo.css": ("ojo.css", "text/css; charset=utf-8"),
    "/ojo.js": ("ojo.js", "application/javascript; charset=utf-8"),
    "/glosario.js": ("glosario.js", "application/javascript; charset=utf-8"),
    "/acta.js": ("acta.js", "application/javascript; charset=utf-8"),
    "/digesto.js": ("digesto.js", "application/javascript; charset=utf-8"),
}

CAPA = AQUI.parent
GLOSARIO = AQUI / "glosario.json"
ACTA = CAPA / "mensajes" / "mensajes.jsonl"
DIGESTOS = CAPA / "digesto"


class Ojo(BaseHTTPRequestHandler):
    server_version = "Ojo/1.0"

    def log_message(self, fmt, *args):
        pass  # sin ruido en la terminal del Soberano

    def _responder(self, codigo, cuerpo, tipo):
        if isinstance(cuerpo, str):
            cuerpo = cuerpo.encode("utf-8")
        self.send_response(codigo)
        self.send_header("Content-Type", tipo)
        self.send_header("Content-Length", str(len(cuerpo)))
        # Nada de cache: un panel de estado cacheado es un panel que miente.
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(cuerpo)

    def _fichero_json(self, ruta, nombre, causa):
        """Sirve un JSON de disco tal cual, o declara por que no puede."""
        if not ruta.exists():
            return self._json(200, {"estado": "NO_DATA", "causa": causa,
                                    "remedio": f"crear {nombre}"})
        try:
            return self._responder(200, ruta.read_bytes(),
                                   "application/json; charset=utf-8")
        except OSError as e:
            return self._json(200, {"estado": "NO_DATA",
                                    "causa": f"{type(e).__name__}"})

    def _json(self, codigo, datos):
        self._responder(codigo, json.dumps(datos, ensure_ascii=False),
                        "application/json; charset=utf-8")

    def do_GET(self):
        ruta = self.path.split("?")[0]

        if ruta == "/api/rack":
            if not ESTADO.exists():
                return self._json(200, {
                    "estado": "NO_DATA",
                    "causa": f"no existe {ESTADO.name}",
                    "remedio": "~/p0x/Alejandria/verificar_sesion.sh",
                    "frescura_segundos": None})
            try:
                d = json.loads(ESTADO.read_text(encoding="utf-8"))
            except ValueError as e:
                return self._json(200, {
                    "estado": "NO_DATA",
                    "causa": f"estado.json ilegible: {e}",
                    "remedio": "~/p0x/Alejandria/verificar_sesion.sh",
                    "frescura_segundos": None})
            # La frescura es un CAMPO, no un adorno de la pantalla: asi el
            # script y el panel no pueden discrepar sobre si el dato esta viejo.
            d["frescura_segundos"] = int(time.time() - d.get("epoch", 0))
            return self._json(200, d)

        if ruta == "/api/glosario":
            return self._fichero_json(GLOSARIO, "glosario.json",
                                      "no hay glosario en esta consola")

        if ruta == "/api/acta":
            # La cadena se verifica AL SERVIR, no al escribir solamente. Un
            # acta se rompe editando el fichero por fuera, y eso no pasa por
            # ninguna funcion de escritura: si no se comprueba aqui, no se
            # comprueba nunca en la pantalla de quien la lee.
            sys.path.insert(0, str(CAPA / "mensajes"))
            try:
                import mensajes as M
                problemas = M.verificar(ACTA)
                return self._json(200, {"estado": "OK",
                                        "mensajes": M.leer(ACTA),
                                        "cadena_sana": not problemas,
                                        "problemas": problemas})
            except Exception as e:                 # noqa: BLE001
                return self._json(200, {
                    "estado": "NO_DATA", "causa": f"{type(e).__name__}: {e}",
                    "remedio": "python3 ~/p0x/Alejandria/test_alejandria.py"})

        if ruta == "/api/digesto":
            ds = sorted(DIGESTOS.glob("digesto-*.md")) if DIGESTOS.exists() else []
            if not ds:
                return self._json(200, {
                    "estado": "NO_DATA", "causa": "todavia no hay ningun digesto",
                    "remedio": "~/p0x/Alejandria/verificar_sesion.sh"})
            ult = ds[-1]
            texto = ult.read_text(encoding="utf-8")
            cuerpo = texto.split("## Los hechos", 1)[0]
            return self._json(200, {
                "estado": "OK", "fichero": ult.name,
                "frescura_segundos": int(time.time() - ult.stat().st_mtime),
                "bronze": "BRONZE · en cuarentena" in texto,
                "cuerpo": cuerpo.split("\n", 4)[-1].strip()})

        pieza = ESTATICOS.get(ruta)
        if not pieza:
            return self._json(404, {"estado": "NO_DATA", "causa": "aqui no vive eso"})
        try:
            crudo = (AQUI / pieza[0]).read_bytes()
        except OSError as e:
            return self._json(500, {"estado": "NO_DATA",
                                    "causa": f"{type(e).__name__}"})
        return self._responder(200, crudo, pieza[1])


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--puerto", type=int, default=8790)
    a = ap.parse_args(argv)
    # 127.0.0.1 clavado y sin bandera para cambiarlo. Una consola que enseña el
    # rack no debe poder atarse a 0.0.0.0 "sin querer".
    srv = ThreadingHTTPServer(("127.0.0.1", a.puerto), Ojo)
    print(f"👁  El Ojo del Soberano · http://127.0.0.1:{a.puerto}/  (Ctrl-C para cerrar)")
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        print("\ncerrado")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
