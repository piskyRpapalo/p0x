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
import sqlite3
import sys
import time
import urllib.error
import urllib.request
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

AQUI = Path(__file__).resolve().parent
ESTADO = AQUI.parent / "estado.json"
# El libro de latidos de los bucles. Vive fuera del repo, en el mismo sitio al
# que se mudo la memoria del producto.
LOOPS = Path.home() / ".preceptoros" / "loops.db"
# Ollama por LOOPBACK a proposito: escucha en `*:11434`, asi que 127.0.0.1
# llega sin salir de la maquina. Preguntarle por la tailnet seria una sonda de
# red, y esta consola no hace sondas de red.
OLLAMA = "http://127.0.0.1:11434"
# Por encima de esto, un snapshot deja de poder leerse como «lo que hay».
RANCIO_S = 3600

# El modulo de metricas del producto, cargado POR RUTA y no por sys.path. Meter
# `~/p0x/preceptor` entero en el path importaria de paso sesenta modulos que
# esta consola no usa, y algunos se llaman como los de aqui (`estado`,
# `mensajes`): la primera colision seria un import silencioso del fichero
# equivocado. Solo stdlib al otro lado, asi que cargarlo es barato.
METRICAS_PY = Path.home() / "p0x" / "preceptor" / "metricas.py"

ESTATICOS = {
    "/": ("ojo.html", "text/html; charset=utf-8"),
    # El Ojo-Vivo convive con la consola de texto en vez de sustituirla: la
    # de texto se lee por SSH y en una terminal, el refugio no.
    "/vivo": ("vivo.html", "text/html; charset=utf-8"),
    "/vivo.html": ("vivo.html", "text/html; charset=utf-8"),
    "/vivo.css": ("vivo.css", "text/css; charset=utf-8"),
    "/vivo.js": ("vivo.js", "application/javascript; charset=utf-8"),
    "/ojo.html": ("ojo.html", "text/html; charset=utf-8"),
    "/ojo.css": ("ojo.css", "text/css; charset=utf-8"),
    "/ojo.js": ("ojo.js", "application/javascript; charset=utf-8"),
    "/glosario.js": ("glosario.js", "application/javascript; charset=utf-8"),
    "/grafo.js": ("grafo.js", "application/javascript; charset=utf-8"),
    "/arranque.js": ("arranque.js", "application/javascript; charset=utf-8"),
    "/acta.js": ("acta.js", "application/javascript; charset=utf-8"),
    "/digesto.js": ("digesto.js", "application/javascript; charset=utf-8"),
}

CAPA = AQUI.parent
GLOSARIO = AQUI / "glosario.json"
RECURSOS = AQUI / "recursos.json"
ARRANQUE = AQUI / "arranque.json"
GRAFO = AQUI / "grafo.json"
FASES = CAPA / "fases.json"
IDENTIDAD = CAPA / "identidad_publica.json"
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

    def _fichero_json(self, ruta, nombre, causa, remedio=None):
        """Sirve un JSON de disco tal cual, o declara por que no puede."""
        if not ruta.exists():
            return self._json(200, {"estado": "NO_DATA", "causa": causa,
                                    "remedio": remedio or f"crear {nombre}"})
        try:
            return self._responder(200, ruta.read_bytes(),
                                   "application/json; charset=utf-8")
        except OSError as e:
            return self._json(200, {"estado": "NO_DATA",
                                    "causa": f"{type(e).__name__}"})

    @staticmethod
    def _modelos_vivos():
        """Que modelos hay AHORA, no cuando alguien midio por ultima vez.

        EL FALLO QUE LO ORIGINA (2026-09-01). `estado.json` declaraba ocho
        modelos; `ollama list` daba dos. La lectura tenia 37 horas y se leia
        como si fuera de ahora: la web publica llego a declarar servido un
        adaptador que ya no existia, y esta consola lo respaldaba. Un dato
        viejo presentado como actual es peor que un hueco declarado.

        No rompe la regla «no mide, pinta», que prohibe SONDAR EL RACK al
        pintar --red, ssh, esperas--. Esto es loopback contra un servicio de
        esta misma maquina, con `timeout` de segundo y medio y NO_DATA con su
        causa si no contesta. Nunca deja la consola colgada, que es lo que la
        regla protege.
        """
        url = f"{OLLAMA}/api/tags"
        try:
            with urllib.request.urlopen(url, timeout=1.5) as r:
                datos = json.loads(r.read().decode("utf-8"))
        except (urllib.error.URLError, OSError, ValueError) as e:
            return {"estado": "NO_DATA", "causa": f"{type(e).__name__} contra {url}",
                    "remedio": "comprobar que Ollama escucha en 11434"}
        nombres = sorted(m.get("name", "?") for m in datos.get("models", []))
        pelados = [n for n in nombres if n.endswith(":latest")]
        return {"estado": "OK", "medido_en": "ahora", "modelos": len(nombres),
                "nombres": nombres,
                # El canon del nodo prohibe los tags pelados. Se cuentan aqui
                # para que se vean, no para juzgarlos: quien decide es el
                # Soberano, y esta consola solo se lo pone delante.
                "tags_pelados": pelados}

    @staticmethod
    def _trabajando():
        """Que bucles estan DENTRO de una pasada ahora mismo.

        POR QUE ESTO NO ROMPE LA REGLA «NO MIDE, PINTA»
        -----------------------------------------------
        Esa regla existe para que la consola no se cuelgue justo cuando el rack
        cae: prohibe SONDAR el rack --red, ssh, subprocesos-- al pintar. Leer un
        fichero SQLite local es de la misma familia que leer `estado.json` o
        calcular la frescura al vuelo: no sale de esta maquina y no espera a
        nadie. Se abre en `mode=ro` y con `timeout=0`: si otro proceso tiene el
        libro tomado, esto devuelve NO_DATA en vez de quedarse esperando.

        Y tiene que ser al vuelo, no del recolector: «esta corriendo AHORA» con
        media hora de retraso no es el mismo hecho. Un bucle `oneshot` dura
        segundos; si se sirviera desde `estado.json` la respuesta seria siempre
        «ninguno», que es una respuesta falsa disfrazada de dato.

        Ocupado = su ultimo latido es `entra`. Cuando sale, escribe `sale`.
        """
        if not LOOPS.exists():
            return {"estado": "NO_DATA", "causa": f"no existe {LOOPS.name}",
                    "remedio": "los bucles todavia no han latido en este nodo"}
        try:
            cx = sqlite3.connect(f"file:{LOOPS}?mode=ro", uri=True, timeout=0)
            try:
                filas = cx.execute("""
                    SELECT l.bucle, l.evento, l.momento FROM latidos l
                    JOIN (SELECT bucle, MAX(momento) m FROM latidos GROUP BY bucle) u
                      ON u.bucle = l.bucle AND u.m = l.momento
                """).fetchall()
            finally:
                cx.close()
        except sqlite3.Error as e:
            # La causa entera, no «error de base de datos»: `no such column`
            # y `database is locked` son dos averias distintas y se arreglan
            # de forma distinta.
            return {"estado": "NO_DATA", "causa": f"{type(e).__name__}: {e}",
                    "remedio": f"comprobar el esquema de {LOOPS.name}"}
        ahora = time.time()
        ocupados = [{"bucle": b, "desde_hace_s": int(ahora - m)}
                    for b, ev, m in filas if ev == "entra"]
        return {"estado": "OK", "ocupados": ocupados,
                "vistos": len(filas),
                "nota": "ocupado = su ultimo latido es `entra` y aun no hay `sale`"}

    @staticmethod
    def _consumo():
        """Los vatios del rack, del enchufe, ahora.

        DECLARADO: esto SI es una sonda de red, y la regla 2 de la cabecera
        dice «no mide, pinta». La excepcion se abre a proposito y se acota
        igual que `_modelos_vivos`: `timeout=2` dentro del propio modulo,
        NO_DATA con causa si no contesta, y jamas una espera larga. El motivo
        es que el consumo no lo escribe nadie en `estado.json`: o se pide aqui
        o no existe. Si algun dia el recolector lo escribe, esta funcion sobra
        y se retira -- ese es el sitio correcto y este es el atajo honesto.

        Se importa por ruta y en el momento de servir, no al arrancar: que
        falte el modulo del producto no puede tumbar la consola del rack.
        """
        if not METRICAS_PY.exists():
            return {"clave": "consumo_w", "estado": "NO_DATA", "valor": None,
                    "unidad": "W",
                    "causa": f"no existe {METRICAS_PY}",
                    "remedio": "el modulo de metricas vive en el repo del producto"}
        try:
            import importlib.util
            spec = importlib.util.spec_from_file_location("p0x_metricas", METRICAS_PY)
            mod = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(mod)
            return mod._consumo_w()
        except Exception as e:                     # noqa: BLE001
            return {"clave": "consumo_w", "estado": "NO_DATA", "valor": None,
                    "unidad": "W",
                    "causa": f"metricas.py no se pudo cargar: {type(e).__name__}: {e}"}

    @staticmethod
    def _arranque():
        """LA PUERTA DE ENTRADA. Una sola peticion y una sesion fria sabe donde
        esta, que reglas la atan, que tiene a mano y como esta el rack AHORA.

        POR QUE ES UNA SOLA RUTA Y NO CUATRO
        ------------------------------------
        Porque una sesion que tiene que acordarse de pedir cuatro cosas pedira
        tres. La orientacion que hay que juntar a mano no se junta: se supone.
        Aqui se compone lo que ya existe --`arranque.json` las reglas,
        `recursos.json` lo que hay a mano-- y se le añade el pulso del rack en
        el mismo objeto, para que nadie razone con un dato de anteayer creyendo
        que es de ahora.

        Cada trozo que falte se declara en su sitio y no tumba el resto: una
        puerta que no abre porque le falta una hoja es peor que media puerta.
        """
        import os

        def leer(ruta, nombre):
            try:
                return json.loads(ruta.read_text(encoding="utf-8"))
            except (OSError, ValueError) as e:
                return {"estado": "NO_DATA", "causa": f"{nombre}: {type(e).__name__}"}

        d = {"esquema": 1,
             "lee_esto_primero": leer(ARRANQUE, "arranque.json"),
             "lo_que_tienes_a_mano": leer(RECURSOS, "recursos.json")}

        # LAS FRONTERAS, DERIVADAS DEL MAPA Y NO COPIADAS A MANO. Son las
        # aristas `no_es` de grafo.json: si manana se anade una, aparece aqui
        # sola. Copiarlas seria crear una segunda verdad sobre el mismo hecho,
        # que es lo que este rack lleva un mes pagando.
        #
        # Van en el arranque y no en una ruta aparte porque confundir dos
        # productos no es un error que se cometa por falta de detalle: se
        # comete por no haber mirado. Si hay que pedirlas, no se piden.
        g = leer(GRAFO, "grafo.json")
        nombres = {n["id"]: n["nombre"] for n in g.get("nodos", [])}
        d["fronteras_que_no_se_cruzan"] = [
            {"esto": nombres.get(e["de"], e["de"]),
             "no_es": nombres.get(e["a"], e["a"]),
             "por_que": e.get("nota", "")}
            for e in g.get("aristas", []) if e.get("tipo") == "no_es"
        ] or {"estado": "NO_DATA", "causa": "grafo.json no declara fronteras"}
        # El reparto de cerebros NO se lee de la memoria de nadie: vive en el
        # entorno, y una sesion nunca debe poder confundirse de cerebro.
        d["cerebro"] = {"P0X_BRAIN": os.environ.get("P0X_BRAIN"),
                        "eres": "local · NO tocas canon ni doctrina"
                        if os.environ.get("P0X_BRAIN") == "local"
                        else "frontera · antes de un refactor mecanico, propon cc-local"}
        return d

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
            # AL VUELO y no del recolector: ver `_trabajando`. Es el unico
            # campo de esta respuesta que describe el instante en que se pide.
            d["trabajando"] = self._trabajando()
            # Y los modelos, EN VIVO. El resto de esta respuesta es un snapshot;
            # esta clave no lo es, y por eso va aparte en vez de pisar
            # `componentes.ollama.nombres`: dos hechos distintos, dos sitios.
            d["ollama_vivo"] = self._modelos_vivos()
            # El vatiaje, tambien EN VIVO y por el mismo motivo que los modelos:
            # el snapshot no lo trae. Va en su propia clave, con la forma de
            # metrica del producto (estado/valor/unidad/como o causa), para que
            # el panel no tenga que aprender un segundo formato.
            d["consumo_w"] = self._consumo()
            # Un snapshot rancio deja de poder leerse como «lo que hay». Se
            # dice con una palabra, al lado de los segundos, porque nadie mira
            # un entero de seis cifras y calcula horas de cabeza. Me paso a mi.
            d["frescura"] = ("RANCIO" if d["frescura_segundos"] > RANCIO_S
                             else "FRESCO")
            return self._json(200, d)

        if ruta == "/api/glosario":
            return self._fichero_json(GLOSARIO, "glosario.json",
                                      "no hay glosario en esta consola")

        if ruta == "/api/arranque":
            d = self._arranque()
            # El pulso va DENTRO del mismo objeto a proposito: si hubiera que
            # pedirlo aparte, media sesion arrancaria sin el.
            d["rack_ahora"] = {"consumo_w": self._consumo(),
                               "ollama_vivo": self._modelos_vivos(),
                               "trabajando": self._trabajando()}
            return self._json(200, d)

        if ruta == "/api/grafo":
            # El mapa de productos. Es DATO, no dibujo: el dibujo lo hace
            # grafo.js y podria ser otro manana sin tocar esta topologia.
            return self._fichero_json(GRAFO, "grafo.json",
                                      "no hay mapa de productos en esta consola")

        if ruta == "/api/recursos":
            # QUE TIENE A MANO una sesion en este nodo. Vive aqui y no en la
            # memoria de nadie porque cada sesion empieza en frio: sin esta
            # lista, un Claude nuevo no sabe que puede abrir la web en un
            # telefono real ni que hay un enchufe que mide vatios, y termina
            # suponiendo lo que podria haber medido.
            return self._fichero_json(RECURSOS, "recursos.json",
                                      "no hay inventario de recursos en esta consola")

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

        if ruta == "/api/fases":
            return self._fichero_json(
                FASES, "fases.json",
                "no existe fases.json; es SALIDA de continuidad.db, no un "
                "fichero escrito a mano",
                remedio="python3 ~/p0x/Alejandria/fases.py")

        if ruta == "/api/identidad":
            # Lo unico de esta consola pensado para ser publico. Va envuelto
            # en {"identidad": ...} y no crudo: asi el fichero puede crecer
            # con claves nuevas sin que el render tenga que adivinar si lo
            # que le llega es el dato o el parte de que no lo hay.
            if not IDENTIDAD.exists():
                return self._json(200, {
                    "estado": "NO_DATA",
                    "causa": "no existe identidad_publica.json",
                    "remedio": "crear ~/p0x/Alejandria/identidad_publica.json"})
            try:
                datos = json.loads(IDENTIDAD.read_text(encoding="utf-8"))
            except (OSError, ValueError) as e:
                return self._json(200, {
                    "estado": "NO_DATA",
                    "causa": f"identidad_publica.json ilegible: {e}",
                    "remedio": "revisar el JSON a mano"})
            return self._json(200, {"estado": "OK", "identidad": datos,
                                    "fuente": "identidad_publica.json"})

        if ruta == "/api/companero":
            # El compañero ACTIVO no tiene fuente todavia. Devolver aqui un
            # "Instalador" a secas seria fabricar el dato: el panel diria que
            # el Soberano eligio compañero cuando nadie ha elegido nada.
            # Lo que si es contrato --el compañero POR DEFECTO-- se sirve, y
            # lo elegido se declara NO_DATA con su causa.
            return self._json(200, {
                "estado": "OK",
                "por_defecto": "el Instalador",
                "elegido": None,
                "causa": "ninguna fuente registra el compañero elegido",
                "nota": "El Centro esta dibujado; hablar con el companero es "
                        "V4 («centro vivo») del contrato visual. Hasta "
                        "entonces esto declara el hueco en vez de rellenarlo."})

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


def comprobar():
    """Dice si el Ojo puede servir, SIN abrir un puerto. Devuelve 0 o 1.

    Responde UNA pregunta --¿esta entero lo que hay que servir?-- y deja la
    otra --¿arranca el servidor?-- para quien lo arranque. Mezclarlas es lo que
    hacia que un fallo no dijese cual de las dos habia fallado.

    Un fichero que falta NO se convierte en un cero ni en un aviso suave: sale
    NO_DATA con su causa, y el codigo de salida lo repite para que un gate
    pueda leerlo sin parsear texto.
    """
    filas = []
    # Las tres piezas de la topologia V1 del contrato visual. Se nombran una a
    # una a proposito: si manana desaparece `vivo.css`, el Ojo seguiria
    # devolviendo 200 en todas las rutas y sirviendo un esqueleto sin estilo.
    for nombre, _ in sorted({v for v in ESTATICOS.values()}):
        ruta = AQUI / nombre
        filas.append((nombre, ruta.is_file(), ruta.stat().st_size if ruta.is_file() else 0,
                      "fichero estatico"))
    # Las fuentes de datos. Que falten NO impide servir: el Ojo pinta NO_DATA.
    # Por eso se declaran aparte y no cuentan para el codigo de salida.
    fuentes = [("estado.json", ESTADO), ("fases.json", FASES),
               ("glosario.json", GLOSARIO), ("identidad_publica.json", IDENTIDAD),
               ("mensajes.jsonl", ACTA),
               # Los dos del arranque. Que falte uno no impide servir, pero
               # deja a la proxima sesion sin puerta: se dice aqui.
               ("arranque.json", ARRANQUE), ("recursos.json", RECURSOS),
               ("grafo.json", GRAFO)]

    ancho = max(len(n) for n, *_ in filas)
    print("== lo que el Ojo tiene que servir ==")
    faltan = 0
    for nombre, hay, tam, _ in filas:
        if hay:
            print(f"  MEDIDO   {nombre:<{ancho}}  {tam} B")
        else:
            faltan += 1
            print(f"  NO_DATA  {nombre:<{ancho}}  no existe en {AQUI}")

    print("== las fuentes que lee (su ausencia se pinta, no rompe) ==")
    for nombre, ruta in fuentes:
        existe = Path(str(ruta)).is_file()
        print(f"  {'MEDIDO ' if existe else 'NO_DATA'}  {nombre}"
              + ("" if existe else "  · el Ojo lo declarara en pantalla"))

    if faltan:
        print(f"NO SIRVE · faltan {faltan} pieza(s) de la topologia V1")
        return 1
    print(f"SIRVE · {len(filas)} piezas presentes")
    return 0


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--check", action="store_true",
                    help="dice si el Ojo puede servir y sale; no abre puerto")
    ap.add_argument("--arranque", action="store_true",
                    help="orientacion de arranque en JSON y sale; no abre puerto")
    ap.add_argument("--puerto", type=int, default=8790)
    a = ap.parse_args(argv)

    # `--check` responde y sale: no abre puerto, asi que puede vivir en un
    # gate sin ocupar un puerto ni dejar un proceso suelto.
    if a.check:
        return comprobar()
    # `--arranque` escupe la misma orientacion SIN abrir puerto. Una IA local
    # con solo una terminal no deberia tener que levantar un servidor para
    # saber donde esta.
    if a.arranque:
        d = Ojo._arranque()
        d["rack_ahora"] = {"consumo_w": Ojo._consumo(),
                           "ollama_vivo": Ojo._modelos_vivos()}
        print(json.dumps(d, ensure_ascii=False, indent=1))
        return 0
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
