#!/usr/bin/env python3
"""Pruebas del Nexo. Lo que tiene que ser verdad de un panel que solo mira.

Ninguna toca el arbol de PreceptorOS ni escribe fuera de su temporal. El
servidor se levanta en un puerto efimero de verdad -- no se simula-- porque lo
que se quiere comprobar es el comportamiento por HTTP, y un doble de la clase
no responde 501 a un POST por su cuenta.
"""

import json
import os
import re
import tempfile
import threading
import time
import unittest
from unittest import mock
import urllib.error
import urllib.request
from pathlib import Path

import sensores
import servidor as SV
from sensores import registro

AQUI = Path(__file__).resolve().parent


class ServidorEnPie:
    """Levanta el Nexo en un puerto que elige el sistema y lo apaga al salir."""

    def __enter__(self):
        self.srv = SV.construir(puerto=0)
        self.puerto = self.srv.server_address[1]
        self.hilo = threading.Thread(target=self.srv.serve_forever, daemon=True)
        self.hilo.start()
        return self

    def __exit__(self, *_):
        self.srv.shutdown()
        self.srv.server_close()

    def url(self, ruta):
        return f"http://127.0.0.1:{self.puerto}{ruta}"

    def get(self, ruta):
        with urllib.request.urlopen(self.url(ruta), timeout=5) as r:
            return r.status, r.read().decode("utf-8"), dict(r.headers)

    def flujo(self, ruta, segundos=4):
        """Lee un trozo del flujo y corta. Sin esto habria que esperar a que
        el servidor cerrara, y un flujo bien hecho no cierra nunca."""
        trozo = []
        r = urllib.request.urlopen(self.url(ruta), timeout=segundos)
        try:
            fin = time.monotonic() + segundos
            while time.monotonic() < fin:
                try:
                    linea = r.readline()
                except (TimeoutError, OSError):
                    # Se acabo lo que habia que leer. No es un fallo: entre
                    # tanda y tanda el flujo calla, y callar es lo correcto --
                    # el latido llega cuando toca, no cuando la prueba mira.
                    break
                if not linea:
                    break
                trozo.append(linea.decode("utf-8", "replace"))
                if len(trozo) > 400:
                    break
        finally:
            r.close()
        return "".join(trozo)

    def pide(self, ruta, metodo="GET", datos=None):
        req = urllib.request.Request(self.url(ruta), method=metodo, data=datos)
        try:
            with urllib.request.urlopen(req, timeout=5) as r:
                return r.status, r.read().decode("utf-8")
        except urllib.error.HTTPError as e:
            return e.code, e.read().decode("utf-8", "replace")


class ElContratoDelSensor(unittest.TestCase):
    """Un sensor devuelve dato o hueco declarado. Nunca None, nunca una excepcion."""

    def test_1_un_hueco_lleva_causa_y_hora(self):
        h = sensores.hueco("porque si")
        self.assertEqual(h["estado"], sensores.NO_DATA)
        self.assertEqual(h["causa"], "porque si")
        self.assertIn("medido", h)

    def test_2_un_dato_lleva_hora_aunque_no_se_pida(self):
        d = sensores.dato(cifra=7)
        self.assertEqual(d["estado"], "ok")
        self.assertEqual(d["cifra"], 7)
        self.assertTrue(d["medido"])

    def test_3_un_sensor_que_revienta_sale_como_hueco(self):
        @sensores.a_prueba_de_balas
        def roto():
            raise RuntimeError("el disco se fue")
        self.assertEqual(roto()["estado"], sensores.NO_DATA)
        # La causa es para una persona; el nombre de la excepcion, para quien
        # depura. Separados a proposito: mezclarlos convierte la causa en jerga,
        # y ademas hace que toda causa acabe pareciendose a un fallo generico.
        self.assertIn("no pudo completar su lectura", roto()["causa"])
        self.assertEqual(roto()["detalle"], "RuntimeError")
        self.assertNotIn("Error", roto()["causa"])

    def test_4_un_sensor_que_devuelve_basura_sale_como_hueco(self):
        for basura in (None, 42, "texto", [], {"sin": "estado"}):
            with self.subTest(basura=basura):
                @sensores.a_prueba_de_balas
                def malo(_b=basura):
                    return _b
                self.assertEqual(malo()["estado"], sensores.NO_DATA)

    def test_5_un_sensor_que_no_existe_no_es_un_error(self):
        self.assertEqual(registro.uno("no_existe")["estado"], sensores.NO_DATA)

    def test_6_un_sensor_caido_no_tumba_a_los_demas(self):
        antes = dict(registro.SENSORES)
        try:
            registro.registrar("_bueno", lambda: sensores.dato(v=1))
            registro.registrar("_malo", lambda: 1 / 0)
            todo = registro.todo()["lecturas"]
            self.assertEqual(todo["_bueno"]["estado"], "ok")
            self.assertEqual(todo["_malo"]["estado"], sensores.NO_DATA)
        finally:
            registro.SENSORES.clear()
            registro.SENSORES.update(antes)


class LaPuertaHTTP(unittest.TestCase):
    def test_7_salud_responde_json_con_su_hora(self):
        with ServidorEnPie() as s:
            codigo, cuerpo, cab = s.get("/api/salud")
            self.assertEqual(codigo, 200)
            datos = json.loads(cuerpo)
            self.assertEqual(datos["estado"], "ok")
            self.assertTrue(datos["medido"])
            self.assertIn("application/json", cab["Content-Type"])
            self.assertEqual(cab["Cache-Control"], "no-store")

    def test_8_estado_devuelve_todas_las_lecturas(self):
        with ServidorEnPie() as s:
            datos = json.loads(s.get("/api/estado")[1])
            self.assertIn("lecturas", datos)
            for nombre, lectura in datos["lecturas"].items():
                with self.subTest(sensor=nombre):
                    self.assertIn(lectura["estado"], ("ok", sensores.NO_DATA))

    def test_9_una_ruta_inventada_da_404_con_causa_no_una_pagina_de_error(self):
        with ServidorEnPie() as s:
            codigo, cuerpo = s.pide("/api/lo_que_sea")
            self.assertEqual(codigo, 404)
            self.assertEqual(json.loads(cuerpo)["estado"], sensores.NO_DATA)

    def test_10_no_hay_un_solo_verbo_que_escriba(self):
        with ServidorEnPie() as s:
            for metodo in ("POST", "PUT", "DELETE", "PATCH"):
                with self.subTest(metodo=metodo):
                    codigo, _ = s.pide("/api/estado", metodo, b"{}")
                    self.assertIn(codigo, (405, 501),
                                  "el panel mira; no manda")

    def test_11_no_se_puede_salir_del_directorio_estatico(self):
        with ServidorEnPie() as s:
            for intento in ("/../servidor.py", "/../../.ssh/id_ed25519",
                            "/..%2fservidor.py"):
                with self.subTest(intento=intento):
                    codigo, cuerpo = s.pide(intento)
                    self.assertIn(codigo, (403, 404))
                    self.assertNotIn("import", cuerpo)

    def test_12_ata_a_localhost_y_no_a_todas_las_interfaces(self):
        """Salir al tailnet se firma aparte. No puede pasar por descuido."""
        self.assertEqual(SV.ANFITRION, "127.0.0.1")
        fuente = (AQUI / "servidor.py").read_text(encoding="utf-8")
        self.assertNotIn('"0.0.0.0"', fuente)

    def test_13_el_servidor_no_depende_de_nada_de_fuera(self):
        fuente = (AQUI / "servidor.py").read_text(encoding="utf-8")
        for prohibido in ("requests", "flask", "fastapi", "aiohttp", "jinja"):
            self.assertNotIn(prohibido, fuente.lower())


class SensoresDeSistema(unittest.TestCase):
    """El nivel y los bucles. Lo que se mide de la maquina, no de los proyectos."""

    def test_14_la_soberania_se_pregunta_al_nucleo_no_se_recalcula(self):
        fuente = (AQUI / "sensores" / "soberania.py").read_text(encoding="utf-8")
        self.assertIn("import soberania", fuente)
        for copiado in ("NIVEL_MAXIMO = 3", "CAPACIDADES = {"):
            self.assertNotIn(copiado, fuente,
                             "la tabla del nucleo no se copia: se pregunta")

    def test_15_el_sensor_de_soberania_no_escribe_en_el_nucleo(self):
        fuente = (AQUI / "sensores" / "soberania.py").read_text(encoding="utf-8")
        for escritura in ("write_text", "fijar_nivel", "modo_santuario",
                          "open(", "unlink"):
            self.assertNotIn(escritura, fuente, "el nivel 3 se engancha, no reforma")

    def test_16_el_nivel_es_un_entero_en_rango_o_un_hueco(self):
        lectura = registro.uno("soberania")
        if lectura["estado"] == "ok":
            self.assertIsInstance(lectura["nivel"], int)
            self.assertGreaterEqual(lectura["nivel"], 0)
            self.assertLessEqual(lectura["nivel"], lectura["maximo"])
        else:
            self.assertTrue(lectura["causa"])

    def test_17_los_timers_se_leen_con_show_y_no_parseando_la_tabla(self):
        fuente = (AQUI / "sensores" / "timers.py").read_text(encoding="utf-8")
        self.assertIn('"show"', fuente)
        # La cadena entrecomillada, no la palabra: el docstring del modulo
        # explica precisamente por que NO se usa, y nombrarla ahi es correcto.
        self.assertNotIn('"list-timers"', fuente,
                         "esa tabla alinea fechas con espacios dentro: se adivina")

    def test_18_un_timer_sin_estrenar_no_declara_resultado(self):
        """systemd dice `Result=success` de un servicio que jamas arranco."""
        lectura = registro.uno("timers")
        if lectura["estado"] != "ok":
            self.skipTest(f"sin systemd de usuario: {lectura['causa']}")
        for fila in lectura["propios"] + lectura["ajenos"]:
            with self.subTest(unidad=fila["unidad"]):
                if fila["ultima"] == sensores.NO_DATA:
                    self.assertEqual(fila["resultado"], sensores.NO_DATA)
                    self.assertTrue(fila["causa"])

    def test_19_los_timers_del_sistema_no_se_cuentan_como_bucles_propios(self):
        lectura = registro.uno("timers")
        if lectura["estado"] != "ok":
            self.skipTest("sin systemd de usuario")
        for fila in lectura["propios"]:
            self.assertFalse(fila["unidad"].startswith(("ubuntu-", "launchpadlib")))

    def test_20_el_sensor_de_timers_no_arranca_ni_para_nada(self):
        fuente = (AQUI / "sensores" / "timers.py").read_text(encoding="utf-8")
        for verbo in ('"start"', '"stop"', '"restart"', '"enable"', '"disable"',
                      '"daemon-reload"'):
            self.assertNotIn(verbo, fuente, "ventana de lectura: no ejecuta")

    def test_21_cada_ruta_nueva_responde_una_lectura_valida(self):
        with ServidorEnPie() as s:
            for ruta in ("/api/soberania", "/api/timers"):
                with self.subTest(ruta=ruta):
                    codigo, cuerpo, _ = s.get(ruta)
                    self.assertEqual(codigo, 200)
                    self.assertIn(json.loads(cuerpo)["estado"],
                                  ("ok", sensores.NO_DATA))


class SensoresDeProyecto(unittest.TestCase):
    """Los cuatro proyectos. Cada uno mide lo suyo o declara por que no puede."""

    def test_22_todos_los_sensores_estan_registrados(self):
        esperados = {"soberania", "timers", "preceptor", "lora", "cinek", "jardin"}
        self.assertTrue(esperados.issubset(set(registro.SENSORES)),
                        f"faltan: {esperados - set(registro.SENSORES)}")

    def test_23_ningun_sensor_de_proyecto_escribe_desde_la_lectura(self):
        """`medir()` escribe, y por eso se llama a mano. `leer()` jamas."""
        for nombre in ("lora", "cinek", "jardin", "soberania", "timers"):
            fuente = (AQUI / "sensores" / f"{nombre}.py").read_text(encoding="utf-8")
            with self.subTest(sensor=nombre):
                for escritura in ("write_text", "write_bytes", "mkdir", "unlink"):
                    self.assertNotIn(escritura, fuente)

    def test_24_la_tanda_del_nucleo_siempre_viene_con_su_hora(self):
        lectura = registro.uno("preceptor")
        if lectura["estado"] != "ok":
            self.skipTest(lectura["causa"])
        tanda = lectura["tanda"]
        if tanda["estado"] == "ok":
            self.assertTrue(tanda["medido"], "una cifra sin hora es un rumor")
            self.assertIn("rancia", tanda)
        else:
            self.assertIn("--medir", tanda["causa"], "y se dice como medirla")

    def test_25_una_tanda_rancia_se_declara_rancia(self):
        import sensores.preceptor as P
        viejo = P.CACHE
        with tempfile.TemporaryDirectory() as d:
            falsa = Path(d) / "tanda.json"
            falsa.write_text(json.dumps({
                "medido": "2020-01-01T00:00:00+00:00", "pruebas": 1,
                "suites": 1, "verde": True}), encoding="utf-8")
            P.CACHE = falsa
            try:
                tanda = P.tanda()
            finally:
                P.CACHE = viejo
        self.assertTrue(tanda["rancia"])
        self.assertIn("24 h", tanda["causa"])

    def test_26_una_tanda_ilegible_no_se_pinta_como_buena(self):
        import sensores.preceptor as P
        viejo = P.CACHE
        with tempfile.TemporaryDirectory() as d:
            rota = Path(d) / "tanda.json"
            rota.write_text("{roto", encoding="utf-8")
            P.CACHE = rota
            try:
                tanda = P.tanda()
            finally:
                P.CACHE = viejo
        self.assertEqual(tanda["estado"], sensores.NO_DATA)

    def test_27_una_carpeta_sin_pesos_no_cuenta_como_adapter(self):
        lectura = registro.uno("lora")
        if lectura["estado"] != "ok":
            self.skipTest(lectura["causa"])
        for a in lectura["adapters"]:
            with self.subTest(adapter=a["nombre"]):
                if a["estado"] == "ok":
                    self.assertGreater(a["bytes"], 0)
                else:
                    self.assertTrue(a["causa"])
        self.assertEqual(lectura["entrenados"],
                         sum(1 for a in lectura["adapters"] if a["estado"] == "ok"))

    def test_28_el_pipeline_no_se_lee_entero_solo_se_lista(self):
        fuente = (AQUI / "sensores" / "cinek.py").read_text(encoding="utf-8")
        for lectura in ("read_text", "readlines", "read_bytes"):
            self.assertNotIn(lectura, fuente,
                             "un registro de MiB en una respuesta de 30 s tira el panel")

    def test_29_el_jardin_mira_el_disco_cada_vez_y_no_una_sola(self):
        """Un marcador que dice «en espera» sin mirar lo diria tambien despues."""
        import sensores.jardin as J
        lectura = J.leer()
        self.assertEqual(lectura["estado"], sensores.NO_DATA)
        self.assertIn("sin carpeta en disco", lectura["causa"])
        viejo = J.RAIZ
        with tempfile.TemporaryDirectory() as d:
            (Path(d) / "jardin").mkdir()
            J.RAIZ = Path(d)
            try:
                self.assertEqual(J.leer()["estado"], "ok",
                                 "si la carpeta aparece, el sensor tiene que verla")
            finally:
                J.RAIZ = viejo

    def test_30_cada_ruta_de_proyecto_responde(self):
        with ServidorEnPie() as s:
            for ruta in ("/api/preceptor", "/api/lora", "/api/cinek", "/api/jardin"):
                with self.subTest(ruta=ruta):
                    codigo, cuerpo, _ = s.get(ruta)
                    self.assertEqual(codigo, 200)
                    self.assertIn(json.loads(cuerpo)["estado"],
                                  ("ok", sensores.NO_DATA))


class LaCara(unittest.TestCase):
    """Lo que tiene que ser verdad de una pagina que no puede salir a la red."""

    FICHEROS = ("index.html", "static/hexelion.css", "static/nexo.js")

    def cara(self, nombre):
        return (AQUI / "estatico" / nombre).read_text(encoding="utf-8")

    def test_31_la_cara_no_carga_nada_de_fuera(self):
        """Zero-CDN, y comprobado: ni htmx, ni alpine, ni una fuente remota."""
        for nombre in self.FICHEROS:
            texto = self.cara(nombre)
            with self.subTest(fichero=nombre):
                for fuera in ("http://", "https://", "//unpkg", "//cdn",
                              "jsdelivr", "cloudflare", "fonts.googleapis",
                              "@import url("):
                    self.assertNotIn(fuera, texto)

    def test_32_no_hay_ni_un_framework(self):
        """React, Vue, Angular, htmx, Alpine: ninguno, ni local ni remoto.

        La reactividad la da `EventSource`, que es del navegador: cero bytes
        descargados y cero dependencias que auditar.
        """
        for nombre in self.FICHEROS:
            bajo = self.cara(nombre).lower()
            with self.subTest(fichero=nombre):
                for marco in ("react", "vue", "angular", "htmx", "alpine",
                              "jquery", "svelte"):
                    self.assertNotIn(marco, bajo)
        self.assertIn("new EventSource(", self.cara("static/nexo.js"))

    def test_33_el_cliente_no_compone_html_solo_lo_coloca(self):
        """Ni plantillas ni concatenacion en el navegador: el HTML llega hecho."""
        js = self.cara("static/nexo.js")
        self.assertIn("innerHTML = ev.data", js)
        self.assertNotIn("<div", js)
        self.assertNotIn("<span", js)

    def test_34_el_escapado_ocurre_en_un_solo_sitio(self):
        """En Python, sobre el dato crudo. No repartido por siete pintores."""
        fuente = (AQUI / "fragmentos.py").read_text(encoding="utf-8")
        self.assertIn("from html import escape", fuente)
        js = self.cara("static/nexo.js")
        self.assertNotIn("replace(/[&<>", js, "el escapado ya no vive aqui")

    def test_35_cada_seccion_de_la_pagina_tiene_su_fragmento_y_al_reves(self):
        """Una seccion sin fragmento se queda vacia para siempre; un fragmento
        sin seccion es un dato que nadie ve. Las dos averias son invisibles."""
        import fragmentos as FR
        en_html = set(re.findall(r'<section class="mod[^"]*" id="m-([a-z]+)"',
                                 self.cara("index.html")))
        self.assertEqual(en_html, set(FR.FRAGMENTOS))
        self.assertEqual(en_html, set(FR.TARJETAS))
        # Ya no es una igualdad con los sensores: dos tarjetas pueden comer del
        # mismo --el rack y la malla lo hacen--. Lo que si tiene que cumplirse
        # es que toda tarjeta coma de algo que existe, y que ningun sensor se
        # quede sin quien lo ensene.
        fuentes = {FR.sensor_de(n) for n in FR.TARJETAS}
        self.assertTrue(fuentes <= set(registro.SENSORES),
                        f"tarjetas sin sensor: {fuentes - set(registro.SENSORES)}")
        self.assertEqual(set(registro.SENSORES) - fuentes, set(),
                         "hay un sensor que no se ensena en ninguna tarjeta")

    def test_36_todo_sensor_tiene_quien_lo_ensene(self):
        import fragmentos as FR
        self.assertEqual({FR.sensor_de(n) for n in FR.TARJETAS},
                         set(registro.SENSORES))

    def test_37_la_pagina_se_sirve_entera_desde_el_nexo(self):
        with ServidorEnPie() as s:
            for ruta in ("/", "/static/hexelion.css", "/static/nexo.js"):
                with self.subTest(ruta=ruta):
                    codigo, cuerpo, cab = s.get(ruta)
                    self.assertEqual(codigo, 200)
                    self.assertTrue(cuerpo.strip())
                    self.assertEqual(cab["X-Frame-Options"], "DENY")

    def test_38_no_data_no_se_pinta_como_un_valor(self):
        import fragmentos as FR
        self.assertIn('class="nodata"', FR.hueco())
        self.assertIn(".nodata{", self.cara("static/hexelion.css"))
        self.assertIn('class="nodata"', FR.fila("k", None))


class ElBrutalismo(unittest.TestCase):
    """Estructura rigida, alto contraste, y el halo solo donde hay vida."""

    def css(self):
        return (AQUI / "estatico" / "static" / "hexelion.css").read_text(encoding="utf-8")

    def test_39_el_fondo_es_oscuro_profundo_y_no_negro_plano(self):
        self.assertIn("--fondo:#060B09", self.css().replace(" ", ""))

    def test_40_radio_de_borde_cero_en_todas_partes(self):
        css = self.css()
        self.assertIn("border-radius:0", css.replace(" ", ""))
        for valor in re.findall(r"border-radius:\s*([^;}]+)", css):
            with self.subTest(valor=valor):
                self.assertEqual(valor.strip(), "0")

    def test_41_ni_un_gradiente_ni_una_sombra_difusa(self):
        css = self.css()
        for prohibido in ("linear-gradient", "radial-gradient", "conic-gradient",
                          "box-shadow", "backdrop-filter"):
            self.assertNotIn(prohibido, css)

    def test_42_ninguna_animacion_de_entrada(self):
        css = self.css()
        for prohibido in ("@keyframes", "animation:", "transition:"):
            self.assertNotIn(prohibido, css)

    def test_43_el_halo_vive_solo_en_las_cifras_vivas(self):
        for regla in self.css().split("}"):
            if "text-shadow" not in regla or "{" not in regla:
                continue
            selector = regla.rsplit("{", 1)[0].strip().splitlines()[-1]
            self.assertIn("viva", selector, f"halo fuera de una cifra viva: {selector}")

    def test_44_una_sola_familia_y_es_monoespaciada(self):
        css = self.css()
        self.assertIn("monospace", css)
        for prohibida in ("serif;", "Georgia", "Cinzel", "sans-serif"):
            self.assertNotIn(prohibida, css)


class ElFlujo(unittest.TestCase):
    """SSE: el servidor empuja HTML, un solo lector, y saber envejecer."""

    def js(self):
        return (AQUI / "estatico" / "static" / "nexo.js").read_text(encoding="utf-8")

    def test_45_el_flujo_manda_html_terminado_y_no_json(self):
        with ServidorEnPie() as s:
            trozo = s.flujo("/api/flujo", segundos=4)
        self.assertIn("event: m-", trozo)
        self.assertIn("data: <div class=", trozo)
        self.assertNotIn('data: {"', trozo, "por el flujo no viaja json")

    def test_46_el_flujo_manda_un_latido_aunque_nada_cambie(self):
        """Una conexion viva que no habla es indistinguible de una muerta."""
        with ServidorEnPie() as s:
            self.assertIn("event: latido", s.flujo("/api/flujo", segundos=4))

    def test_47_un_solo_lector_para_todas_las_pestanas(self):
        """Abrir una pestaña mas cuesta un socket, no una ronda de sondas."""
        fuente = (AQUI / "vigia.py").read_text(encoding="utf-8")
        self.assertIn("threading.Condition", fuente)
        servidor = (AQUI / "servidor.py").read_text(encoding="utf-8")
        flujo = servidor.split("def _flujo(")[1].split("def _evento(")[0]
        self.assertNotIn("registro.uno", flujo,
                         "el flujo no lee sensores: espera al vigia")

    def test_48_solo_se_manda_lo_que_ha_cambiado(self):
        import vigia as V
        v = V.Vigia(cada=999)
        try:
            self.assertTrue(v.refrescar(), "la primera ronda compone las siete")
            self.assertEqual([n for n in v.refrescar() if n not in ("nodos",)], [],
                             "una segunda ronda seguida no puede cambiarlo todo")
        finally:
            v.parar()

    def test_49_el_formato_sse_parte_bien_lo_que_lleve_saltos(self):
        servidor = (AQUI / "servidor.py").read_text(encoding="utf-8")
        self.assertIn('for linea in str(dato).split("\\n")', servidor)
        import fragmentos as FR
        for nombre in FR.FRAGMENTOS:
            with self.subTest(sensor=nombre):
                self.assertNotIn("\n", FR.html_de(nombre, registro.uno(nombre)))

    def test_50_si_el_latido_para_la_pagina_deja_de_fingirse_viva(self):
        js = self.js()
        self.assertIn("classList.add('rancio')", js)
        self.assertIn("flujo.onerror", js)
        self.assertIn("setInterval", js, "un socket abierto y mudo tambien envejece")
        self.assertNotIn("innerHTML = ''", js, "lo medido no se borra: se marca")

    def test_51_la_reconexion_no_se_escribe_a_mano(self):
        """EventSource reconecta solo. Escribirlo seria reimplementar el navegador."""
        js = self.js()
        self.assertNotIn("setTimeout(conectar", js)
        self.assertNotIn("reconnect", js.lower())

    def test_52_abrir_y_cerrar_no_cuesta_ni_un_byte_de_estado(self):
        """`<details>` en vez de un toggle con estado: el navegador ya sabe, y
        ademas lo hace con teclado y con lector de pantalla."""
        fuente = (AQUI / "fragmentos.py").read_text(encoding="utf-8")
        self.assertIn("<details", fuente)
        self.assertNotIn("x-data", fuente)
        self.assertNotIn("addEventListener('click'", self.js())


class ElDiagramaDeCapas(unittest.TestCase):
    """Layer stack segun la gramatica de diagram-design, compuesto en Python."""

    def svg(self, nivel=0):
        import fragmentos as FR
        return FR.capas(nivel, "pie de prueba")

    def test_53_cuatro_bandas_y_ni_una_mas(self):
        niveles = re.findall(r'data-nivel="(\d)"', self.svg())
        self.assertEqual(sorted(niveles), ["0", "1", "2", "3"])

    def test_54_toda_coordenada_es_divisible_por_cuatro(self):
        svg = self.svg()
        for attr in ("x", "y", "width", "height"):
            for valor in re.findall(rf'\b{attr}="(\d+)"', svg):
                with self.subTest(attr=attr, valor=valor):
                    self.assertEqual(int(valor) % 4, 0)

    def test_55_una_banda_focal_y_solo_una(self):
        for nivel in (0, 1, 2, 3):
            with self.subTest(nivel=nivel):
                svg = self.svg(nivel)
                self.assertEqual(svg.count("banda focal"), 1)
                self.assertEqual(svg.count(f'data-nivel="{nivel}"'), 1)
                self.assertIn(f'class="banda focal" data-nivel="{nivel}"', svg)

    def test_56_lo_que_esta_por_encima_del_nivel_sale_dormido(self):
        svg = self.svg(1)
        self.assertEqual(svg.count("banda dormida"), 2)   # el 2 y el 3

    def test_57_sin_lectura_no_hay_banda_focal(self):
        """No saber en que nivel corre no puede parecerse a estar en el 0."""
        import fragmentos as FR
        frag = FR.de("soberania", {"estado": "NO_DATA", "causa": "sin guardian"})
        self.assertIsNone(frag["nivel"])
        self.assertNotIn("banda focal", FR.capas(frag["nivel"], frag["pie"]))

    def test_58_la_banda_focal_la_decide_el_servidor(self):
        js = (AQUI / "estatico" / "static" / "nexo.js").read_text(encoding="utf-8")
        self.assertNotIn("focal", js)
        self.assertNotIn("banda", js)


class ElRack(unittest.TestCase):
    """El unico sensor que sale de la maquina, y el unico con interruptor."""

    def fuente(self):
        return (AQUI / "sensores" / "nodos.py").read_text(encoding="utf-8")

    def test_51_el_panel_no_abre_sesiones_ssh(self):
        """Una ventana que entra por SSH en cuatro maquinas cada 30 s es un
        agente con llaves, no una ventana."""
        f = self.fuente()
        for prohibido in ('"ssh"', "'ssh'", "paramiko", "ssh -", "scp "):
            self.assertNotIn(prohibido, f)

    def test_52_los_nodos_se_indexan_por_su_nombre_del_tailnet(self):
        """Medido: La Fragua se llama `ubuntu` en su propio sistema. Indexar por
        HostName la dejaba fuera del mapa como si estuviera caida."""
        f = self.fuente()
        self.assertIn("DNSName", f)
        self.assertIn("def _nombre(", f)

    def test_53_con_la_red_cortada_no_se_pregunta_y_se_dice(self):
        import sensores.nodos as N
        antes = N.sin_red()
        try:
            N.sin_red(True)
            lectura = N.leer()
            self.assertEqual(lectura["estado"], sensores.NO_DATA)
            self.assertIn("red cortada", lectura["causa"])
        finally:
            N.sin_red(antes)

    def test_54_el_interruptor_llega_desde_la_linea_de_ordenes(self):
        fuente = (AQUI / "servidor.py").read_text(encoding="utf-8")
        self.assertIn("--sin-red", fuente)
        self.assertIn("nodos.sin_red(args.sin_red)", fuente)

    def test_55_toda_correccion_al_gateway_se_declara(self):
        """El registro remoto da este nodo por caido. Corregirlo esta bien;
        corregirlo en silencio no."""
        f = self.fuente()
        self.assertIn("correcciones.append", f)
        self.assertIn("avisos", f)
        lectura = registro.uno("nodos")
        if lectura["estado"] == "ok":
            self.assertIsInstance(lectura["avisos"], list)
            for fila in lectura["nodos"]:
                self.assertIn(fila["estado"],
                              ("ONLINE", "OFFLINE", "CRITICO", "EN ESPERA",
                               sensores.NO_DATA))

    def test_56_un_estado_critico_nunca_viene_sin_su_alerta(self):
        lectura = registro.uno("nodos")
        if lectura["estado"] != "ok":
            self.skipTest(lectura["causa"])
        for fila in lectura["nodos"]:
            with self.subTest(nodo=fila["nodo"]):
                if fila["estado"] == "CRITICO":
                    self.assertTrue(fila["alerta"],
                                    "un rojo sin causa no se puede reparar")

    def test_56b_la_direccion_del_gateway_no_vive_en_el_codigo(self):
        """Infraestructura en la maquina, no en la historia del repo."""
        f = self.fuente()
        self.assertNotIn("http://la-", f)
        self.assertIn("os.environ.get(VARIABLE)", f)

    def test_56c_sin_gateway_declarado_el_panel_no_adivina_uno(self):
        import sensores.nodos as N
        antes_conf, antes_env = N.CONF, os.environ.get(N.VARIABLE)
        antes_rack = N.RACK_CONF
        with tempfile.TemporaryDirectory() as d:
            N.CONF = Path(d) / "no_existe.conf"
            # Un rack propio: sin gateway NO es lo mismo que sin rack, y sin
            # este fichero la prueba comprobaria lo segundo creyendo medir lo
            # primero. En una maquina sin rack.conf --toda menos la nuestra--
            # pasaba por el motivo equivocado.
            rack = Path(d) / "rack.conf"
            rack.write_text("nodo-x | metal | papel | nodo-x\n", encoding="utf-8")
            N.RACK_CONF = rack
            os.environ.pop(N.VARIABLE, None)
            try:
                self.assertEqual(N.gateway(), "")
                lectura = N.leer()
                self.assertEqual(lectura["estado"], "ok",
                                 "sin gateway el tailnet sigue contestando")
                self.assertFalse(lectura["gateway_declarado"])
                self.assertIn("sin gateway declarado", lectura["causa"])
            finally:
                N.CONF, N.RACK_CONF = antes_conf, antes_rack
                if antes_env is not None:
                    os.environ[N.VARIABLE] = antes_env

    def test_56e_sin_rack_declarado_no_se_inventan_nodos(self):
        """Un panel relleno de ejemplos es peor que uno vacio: el vacio se ve."""
        import sensores.nodos as N
        antes = N.RACK_CONF
        with tempfile.TemporaryDirectory() as d:
            N.RACK_CONF = Path(d) / "no_existe.conf"
            try:
                lectura = N.leer()
                self.assertEqual(lectura["estado"], sensores.NO_DATA)
                self.assertIn("sin rack declarado", lectura["causa"])
            finally:
                N.RACK_CONF = antes

    def test_56d_una_sonda_que_falta_no_es_un_nodo_dormido(self):
        """La cicatriz. Que el gateway calle no dice que un nodo duerma: dice
        que no lo sabemos, y eso tiene nombre propio."""
        # Sin comentarios: la cicatriz que explica por que NO se hace cita la
        # linea vieja, y citarla ahi es correcto. Lo que no puede es ejecutarse.
        codigo = "\n".join(l for l in self.fuente().splitlines()
                           if not l.lstrip().startswith("#"))
        self.assertNotIn('estado = "EN ESPERA"', codigo,
                         "una ausencia de dato no puede afirmar un estado")
        self.assertIn("sin_sonda.append", codigo)
        lectura = registro.uno("nodos")
        if lectura["estado"] != "ok":
            self.skipTest(lectura["causa"])
        for fila in lectura["nodos"]:
            with self.subTest(nodo=fila["nodo"]):
                self.assertNotEqual(
                    fila["estado"], "EN ESPERA",
                    f"{fila['nodo']} declarado dormido sin haberlo medido")

    def test_56f_una_sonda_que_mira_a_otro_nodo_se_declara(self):
        """CICATRIZ. La alerta decia «ais-catcher caido» a secas y atribuia la
        averia al nodo de la tarjeta. La sonda del gateway apunta a un host
        propio, que puede no ser ese -- y medido, no lo era. Una alerta que
        senala la maquina equivocada manda a arreglar lo que no esta roto.
        """
        import sensores.nodos as N
        rack = [("nodo-a", "metal", "adquisicion RF · ADS-B y AIS", "a")]
        antena = {"ais": {"live": False, "origin": "http://otro-nodo:10110/x"},
                  "adsb": {"live": True, "aircraft": 3}}

        def remoto(_b, ruta):
            return antena if "antenna" in ruta else {"nodes": []}

        with mock.patch.object(N, "rack", return_value=rack), \
             mock.patch.object(N, "propio", return_value=""), \
             mock.patch.object(N, "gateway", return_value="http://x"), \
             mock.patch.object(N, "_tailscale", return_value={"nodo-a": True}), \
             mock.patch.object(N, "_json_remoto", side_effect=remoto):
            lectura = N.leer()
        fila = lectura["nodos"][0]
        self.assertEqual(fila["estado"], "CRITICO")
        self.assertIn("otro-nodo", fila["alerta"], "la alerta dice a donde mira")
        self.assertIn("NO es nodo-a", fila["alerta"])
        self.assertTrue(any("desfasado" in a for a in lectura["avisos"]))

    def test_56g_el_host_de_una_sonda_se_recorta_al_nombre(self):
        """Ni dominio ni puerto: lo que hace falta enseñar es a que MAQUINA."""
        import sensores.nodos as N
        self.assertEqual(N._host("http://un-nodo.una-red.example:10110/s.json"),
                         "un-nodo")
        self.assertEqual(N._host(""), "")
        self.assertEqual(N._host("file:/run/algo/x.json"), "")

    def test_57_el_rack_es_una_tira_no_una_rejilla_fija(self):
        """Un quinto nodo tiene que alargar la fila, no re-maquetarla."""
        css = (AQUI / "estatico" / "static" / "hexelion.css").read_text(encoding="utf-8")
        tira = css.split(".tira{")[1].split("}")[0]
        self.assertIn("overflow-x:auto", tira)
        self.assertNotIn("grid-template-columns", tira)

    def test_58_el_rojo_solo_aparece_cuando_hay_algo_roto(self):
        css = (AQUI / "estatico" / "static" / "hexelion.css").read_text(encoding="utf-8")
        # Por REGLA y no por linea: una regla puede ocupar tres renglones, y el
        # selector solo esta en el primero. Partir por lineas suspendia reglas
        # correctas por el sitio donde cabia el texto.
        for regla in css.split("}"):
            if "var(--red)" not in regla or "{" not in regla:
                continue
            selector = regla.rsplit("{", 1)[0].strip().splitlines()[-1]
            # `roto` es como la malla llama a un nodo en fallo. Entra en la
            # lista por lo que significa, no por parecerse a las otras.
            self.assertTrue(
                any(p in selector for p in ("critico", "alerta", "c-crit", "roto")),
                f"rojo fuera de un fallo real: {selector}")


class LaMalla(unittest.TestCase):
    """La topologia, dibujada sin una sola libreria de mapas."""

    def malla(self, estados):
        import fragmentos as FR
        return FR.mapa({"nodos": [{"nodo": n, "estado": s} for n, s in estados],
                        "criticos": sum(1 for _, s in estados if s == "CRITICO")})

    def test_59_no_hay_ninguna_libreria_de_mapas(self):
        """Un mapa geografico aqui seria una mentira util: de esta topologia
        importa quien ve a quien, y eso no tiene coordenadas."""
        fuente = (AQUI / "fragmentos.py").read_text(encoding="utf-8")
        for pesado in ("leaflet", "mapbox", "openlayers", "googleapis", "tile"):
            self.assertNotIn(pesado, fuente.lower())

    def test_60_un_cuadrado_por_nodo_y_una_arista_por_pareja(self):
        html = self.malla([("a", "ONLINE"), ("b", "ONLINE"),
                           ("c", "CRITICO"), ("d", "OFFLINE")])["html"]
        self.assertEqual(html.count('class="nodo-mapa'), 4)
        self.assertEqual(html.count("<line"), 6, "cuatro nodos son seis parejas")

    def test_61_el_estado_del_nodo_llega_al_dibujo(self):
        html = self.malla([("a", "ONLINE"), ("b", "CRITICO"),
                           ("c", "OFFLINE"), ("d", sensores.NO_DATA)])["html"]
        for clase in ("vivo", "roto", "ido", "mudo"):
            self.assertIn(f'nodo-mapa {clase}', html)

    def test_62_la_malla_tambien_cae_en_la_rejilla_de_cuatro(self):
        html = self.malla([("a", "ONLINE"), ("b", "ONLINE"), ("c", "ONLINE")])["html"]
        for attr in ("x1", "y1", "x2", "y2", "x", "y", "width", "height"):
            for valor in re.findall(rf'\b{attr}="(-?\d+)"', html):
                with self.subTest(attr=attr, valor=valor):
                    self.assertEqual(int(valor) % 4, 0)

    def test_63_sin_nodos_no_se_dibuja_una_malla_vacia(self):
        frag = self.malla([])
        self.assertEqual(frag["chip"], sensores.NO_DATA)
        self.assertIn("nodata", frag["html"])

    def test_64_la_malla_y_el_rack_comen_del_mismo_sensor(self):
        """Dos lecturas del mismo hecho serian dos verdades sobre el mismo hecho."""
        import fragmentos as FR
        self.assertEqual(FR.sensor_de("mapa"), FR.sensor_de("nodos"))


class ElSegundoCerebro(unittest.TestCase):
    """La forma de una memoria. Jamas su contenido."""

    def test_65_no_se_lee_una_sola_palabra_de_la_memoria(self):
        """Es la memoria de una persona y el panel puede acabar en una pantalla
        que mira alguien mas. Se cuenta; no se selecciona texto."""
        fuente = (AQUI / "sensores" / "cerebro.py").read_text(encoding="utf-8")
        for columna in ("select what", "select why", "select *", "select text",
                        "fetchall"):
            self.assertNotIn(columna, fuente.lower())
        self.assertIn("count(*)", fuente)

    def test_66_la_base_se_abre_en_solo_lectura(self):
        fuente = (AQUI / "sensores" / "cerebro.py").read_text(encoding="utf-8")
        self.assertIn("mode=ro", fuente)
        for escritura in ("insert", "update ", "delete", "drop", "commit()"):
            self.assertNotIn(escritura, fuente.lower())

    def test_67_sin_memoria_en_el_disco_se_declara_el_hueco(self):
        import sensores.cerebro as C
        with mock.patch.object(C, "ruta", return_value=None):
            lectura = C.leer()
        self.assertEqual(lectura["estado"], sensores.NO_DATA)
        self.assertIn("no hay ninguna memoria", lectura["causa"])

    def test_68_un_jardin_vacio_tiene_forma(self):
        """Cinco huecos y no una fila en blanco: es la diferencia entre «no hay
        nada» y «no se ha mirado»."""
        import sensores.cerebro as C
        self.assertEqual(C.silueta(0, 10), "○" * C.PUNTOS)
        self.assertEqual(len(C.silueta(0, 10)), C.PUNTOS)

    def test_69_lo_que_existe_nunca_sale_como_vacio(self):
        """Uno entre mil redondea a cero puntos. Un recuerdo que existe no puede
        dibujarse igual que ninguno."""
        import sensores.cerebro as C
        for cuantos, techo in ((1, 1000), (1, 100), (3, 500)):
            with self.subTest(cuantos=cuantos, techo=techo):
                self.assertIn("●", C.silueta(cuantos, techo))

    def test_70_la_silueta_siempre_mide_lo_mismo(self):
        import sensores.cerebro as C
        for cuantos in (0, 1, 5, 50, 5000):
            self.assertEqual(len(C.silueta(cuantos, 50)), C.PUNTOS)

    def test_71_una_base_de_otra_version_no_es_una_averia(self):
        import sensores.cerebro as C
        import sqlite3
        with tempfile.TemporaryDirectory() as d:
            db = Path(d) / "memory.db"
            con = sqlite3.connect(db)
            con.execute("create table engrams (id integer primary key)")
            con.commit()
            con.close()
            with mock.patch.object(C, "ruta", return_value=db):
                lectura = C.leer()
        self.assertEqual(lectura["estado"], "ok")
        self.assertIn("enlaces", lectura["faltan"], "lo que falta se declara")

    def test_72_un_fichero_que_no_es_una_memoria_sale_como_hueco(self):
        import sensores.cerebro as C
        with tempfile.TemporaryDirectory() as d:
            db = Path(d) / "memory.db"
            db.write_bytes(b"esto no es sqlite")
            with mock.patch.object(C, "ruta", return_value=db):
                lectura = C.leer()
        self.assertEqual(lectura["estado"], sensores.NO_DATA)
        self.assertTrue(lectura["causa"])


class LaCamara(unittest.TestCase):
    """Una etiqueta y cero JavaScript. Y ninguna etiqueta si no hay camara."""

    def test_73_sin_camara_declarada_no_se_apunta_a_ninguna_red(self):
        """El panel por defecto no carga un solo recurso de fuera."""
        import sensores.observe as O
        import fragmentos as FR
        with mock.patch.object(O, "direccion", return_value=""):
            lectura = O.leer()
        self.assertEqual(lectura["estado"], sensores.NO_DATA)
        html = FR.html_de("observe", lectura)
        self.assertNotIn("<img", html)
        self.assertNotIn("http", html)

    def test_74_una_camara_que_no_contesta_no_se_pinta_rota(self):
        """Un <img> roto ensena el icono de imagen partida: parece un fallo del
        panel y es de la camara, y no dice cual de los dos."""
        import sensores.observe as O
        import fragmentos as FR
        with mock.patch.object(O, "direccion", return_value="http://inventada/x"), \
             mock.patch.object(O, "_responde", side_effect=TimeoutError("nada")):
            lectura = O.leer()
        self.assertEqual(lectura["estado"], sensores.NO_DATA)
        self.assertIn("sin senal", lectura["causa"])
        self.assertNotIn("<img", FR.html_de("observe", lectura))

    def test_75_una_camara_viva_se_pinta_con_una_etiqueta_y_nada_mas(self):
        import sensores.observe as O
        import fragmentos as FR
        with mock.patch.object(O, "direccion", return_value="http://camara/s"), \
             mock.patch.object(O, "_responde",
                               return_value="multipart/x-mixed-replace"):
            lectura = O.leer()
        self.assertTrue(lectura["mjpeg"])
        html = FR.html_de("observe", lectura)
        self.assertIn('<img class="camara"', html)
        self.assertNotIn("<script", html)
        self.assertNotIn("onload", html)

    def test_76_la_direccion_de_la_camara_no_vive_en_el_codigo(self):
        fuente = (AQUI / "sensores" / "observe.py").read_text(encoding="utf-8")
        self.assertNotIn("http://", fuente)
        self.assertIn("os.environ.get(VARIABLE)", fuente)

    def test_77_el_cliente_sigue_sin_saber_de_nada_de_esto(self):
        """La restriccion que sostiene todo: el JS solo coloca lo que llega."""
        js = (AQUI / "estatico" / "static" / "nexo.js").read_text(encoding="utf-8")
        for palabra in ("camara", "mjpeg", "malla", "cerebro", "silueta",
                        "engrama", "observe"):
            self.assertNotIn(palabra, js.lower())


class ElCielo(unittest.TestCase):
    """Aeronaves situadas, sin una sola libreria de mapas."""

    def avion(self, lat, lon, pies=5000, hexid="abc123"):
        import sensores.adsb as A
        return {"hex": hexid, "vuelo": "TEST1", "lat": lat, "lon": lon,
                "pies": pies, "nudos": 400, "escalon": A.escalon(pies)}

    def lectura(self, aviones, oidas=None):
        import sensores.adsb as A
        v = A.ventana(aviones)
        return {"estado": "ok", "aviones": aviones, "situadas": len(aviones),
                "oidas": oidas if oidas is not None else len(aviones),
                "mudas": max((oidas or len(aviones)) - len(aviones), 0),
                "ventana": {"sur": v[0], "norte": v[1], "oeste": v[2],
                            "este": v[3], "origen": v[4]}}

    def test_77b_sin_gateway_el_cielo_no_dice_que_la_antena_calla(self):
        """No tener a quien preguntar y preguntar sin respuesta son dos cosas."""
        import sensores.adsb as A
        with mock.patch.object(A.nodos, "gateway", return_value=""):
            lectura = A.leer()
        self.assertEqual(lectura["estado"], sensores.NO_DATA)
        self.assertIn("sin gateway", lectura["causa"])
        self.assertNotIn("no contesta", lectura["causa"])

    def test_78_no_hay_ninguna_libreria_de_mapas(self):
        for fichero in ("sensores/adsb.py", "fragmentos.py",
                        "estatico/static/nexo.js"):
            bajo = (AQUI / fichero).read_text(encoding="utf-8").lower()
            with self.subTest(fichero=fichero):
                for pesado in ("leaflet", "openlayers", "mapbox", "googleapis",
                               "tile.openstreetmap", "d3."):
                    self.assertNotIn(pesado, bajo)

    def test_79_un_solo_avion_no_divide_entre_cero(self):
        """La formula obvia --normalizar entre minimo y maximo-- revienta aqui."""
        import fragmentos as FR
        html = FR.adsb(self.lectura([self.avion(38.7, -9.1)]))["html"]
        self.assertEqual(html.count("<circle"), 1)

    def test_80_dos_aviones_cerca_no_se_pintan_en_esquinas_opuestas(self):
        """El fallo del encuadre automatico: dos aviones a pocos kilometros
        acabarian en extremos del dibujo, y el mapa mentiria sobre la distancia."""
        import fragmentos as FR
        import re as _re
        cerca = [self.avion(38.70, -9.10), self.avion(38.72, -9.12)]
        html = FR.adsb(self.lectura(cerca))["html"]
        xs = [float(x) for x in _re.findall(r'cx="([\d.]+)"', html)]
        ys = [float(y) for y in _re.findall(r'cy="([\d.]+)"', html)]
        self.assertLess(max(xs) - min(xs), FR.ADSB_ANCHO * 0.5,
                        "dos aviones cercanos no pueden ocupar medio mapa")
        self.assertLess(max(ys) - min(ys), FR.ADSB_ALTO * 0.5)

    def test_81_la_escala_no_cambia_cuando_entra_otro_avion_cerca(self):
        """Con encuadre automatico, un avion quieto parece moverse porque entro
        otro por el otro lado. Con suelo, se queda quieto."""
        import fragmentos as FR
        import re as _re
        def x_del_primero(aviones):
            html = FR.adsb(self.lectura(aviones))["html"]
            return float(_re.findall(r'cx="([\d.]+)"', html)[0])
        uno = [self.avion(38.70, -9.10)]
        dos = uno + [self.avion(38.71, -9.11)]
        self.assertAlmostEqual(x_del_primero(uno), x_del_primero(dos), delta=40)

    def test_82_el_norte_queda_arriba(self):
        import fragmentos as FR
        import re as _re
        html = FR.adsb(self.lectura([self.avion(39.5, -9.0),
                                     self.avion(38.5, -9.0)]))["html"]
        ys = [float(y) for y in _re.findall(r'cy="([\d.]+)"', html)]
        self.assertLess(ys[0], ys[1], "el de mas latitud va mas arriba")

    def test_83_los_tres_escalones_de_altura(self):
        import sensores.adsb as A
        self.assertEqual(A.escalon(500), "baja")
        self.assertEqual(A.escalon(18000), "media")
        self.assertEqual(A.escalon(36000), "alta")
        self.assertEqual(A.escalon(None), sensores.NO_DATA)

    def test_84_la_altura_no_usa_el_rojo(self):
        """El rojo de este panel significa «hay algo roto». Un avion alto no
        esta averiado: esta lejos. Dos significados para un color deja el
        codigo sin significado."""
        css = (AQUI / "estatico" / "static" / "hexelion.css").read_text(encoding="utf-8")
        cielo = css.split(".cielo .avion")[1].split("/* ── la camara")[0]
        self.assertNotIn("var(--red)", cielo)

    def test_85_la_altura_tambien_se_lee_sin_color(self):
        """El relleno se vacia segun sube. Quien no distinga verde de ambar
        sigue viendo tres cosas distintas."""
        css = (AQUI / "estatico" / "static" / "hexelion.css").read_text(encoding="utf-8")
        self.assertIn(".cielo .alta{fill:none", css)

    def test_86_cada_avion_lleva_su_rotulo_sin_una_linea_de_javascript(self):
        import fragmentos as FR
        html = FR.adsb(self.lectura([self.avion(38.7, -9.1)]))["html"]
        self.assertIn("<title>", html)
        self.assertNotIn("onmouseover", html)
        self.assertNotIn("<script", html)

    def test_87_las_que_no_dicen_donde_estan_se_cuentan_igual(self):
        """Ensenar «2 aviones» oyendo a ocho es mentir por omision: el numero
        es cierto y la frase es falsa."""
        import fragmentos as FR
        frag = FR.adsb(self.lectura([self.avion(38.7, -9.1)], oidas=8))
        self.assertIn("1 de 8", frag["chip"])
        self.assertIn("7 emiten sin decir donde estan", frag["html"])

    def test_88_sin_ninguna_situada_no_se_dibuja_un_cielo_vacio(self):
        import sensores.adsb as A
        import fragmentos as FR
        # Se declara el gateway: sin el, el sensor corta ANTES de llegar a la
        # red y este caso comprobaria «no hay gateway» creyendo medir «el
        # gateway no contesta». Dos huecos distintos con la misma forma.
        with mock.patch.object(A, "_url", return_value="http://inventado/x"), \
             mock.patch.object(A.urllib.request, "urlopen",
                               side_effect=TimeoutError("nada")):
            lectura = A.leer()
        self.assertEqual(lectura["estado"], sensores.NO_DATA)
        self.assertIn("no contesta", lectura["causa"])
        html = FR.html_de("adsb", lectura)
        self.assertNotIn("<svg", html)
        self.assertIn("nodata", html)

    def test_89_una_ventana_ilegible_se_ignora_y_no_revienta(self):
        import sensores.adsb as A
        antes = os.environ.get(A.VARIABLE)
        try:
            for basura in ("", "1,2", "norte,sur", "9,9,9,9", "a,b,c,d"):
                os.environ[A.VARIABLE] = basura
                with self.subTest(ventana=basura):
                    v = A.ventana([{"lat": 38.7, "lon": -9.1}])
                    self.assertEqual(v[4], "deducida")
        finally:
            os.environ.pop(A.VARIABLE, None)
            if antes is not None:
                os.environ[A.VARIABLE] = antes

    def test_90_una_ventana_declarada_manda_y_se_dice(self):
        import sensores.adsb as A
        antes = os.environ.get(A.VARIABLE)
        os.environ[A.VARIABLE] = "38.0,40.0,-10.0,-8.0"
        try:
            v = A.ventana([{"lat": 38.7, "lon": -9.1}])
            self.assertEqual((v[0], v[1], v[2], v[3]), (38.0, 40.0, -10.0, -8.0))
            self.assertEqual(v[4], "declarada")
        finally:
            os.environ.pop(A.VARIABLE, None)
            if antes is not None:
                os.environ[A.VARIABLE] = antes

    def test_91_un_avion_fuera_de_la_ventana_se_pega_al_borde(self):
        """Con ventana declarada puede haber trafico fuera. Un circulo pintado
        a x=-40 no se ve pero SI cuenta arriba, y esa resta no cuadraria."""
        import fragmentos as FR
        import re as _re
        lectura = self.lectura([self.avion(38.7, -9.1)])
        lectura["ventana"] = {"sur": 45.0, "norte": 46.0, "oeste": 0.0,
                              "este": 1.0, "origen": "declarada"}
        html = FR.adsb(lectura)["html"]
        x = float(_re.findall(r'cx="([\d.]+)"', html)[0])
        y = float(_re.findall(r'cy="([\d.]+)"', html)[0])
        self.assertTrue(0 <= x <= FR.ADSB_ANCHO)
        self.assertTrue(0 <= y <= FR.ADSB_ALTO)


if __name__ == "__main__":
    unittest.main(verbosity=2)
