#!/usr/bin/env python3
"""Pruebas del Nexo. Lo que tiene que ser verdad de un panel que solo mira.

Ninguna toca el arbol de PreceptorOS ni escribe fuera de su temporal. El
servidor se levanta en un puerto efimero de verdad -- no se simula-- porque lo
que se quiere comprobar es el comportamiento por HTTP, y un doble de la clase
no responde 501 a un POST por su cuenta.
"""

import json
import re
import tempfile
import threading
import unittest
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
        self.assertIn("RuntimeError", roto()["causa"])

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
                tanda = P.leer()["tanda"]
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
                tanda = P.leer()["tanda"]
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

    def cara(self, nombre):
        return (AQUI / "estatico" / nombre).read_text(encoding="utf-8")

    def test_31_la_cara_no_carga_nada_de_fuera(self):
        """v9 traia Google Fonts y Leaflet por CDN. Aqui eso no entra."""
        for nombre in ("index.html", "hexelion.css", "nexo.js"):
            texto = self.cara(nombre)
            with self.subTest(fichero=nombre):
                for fuera in ("http://", "https://", "//unpkg", "//cdn",
                              "fonts.googleapis", "@import url("):
                    self.assertNotIn(fuera, texto,
                                     "un panel que necesita internet para "
                                     "dibujarse es una contradiccion")

    def test_32_la_cara_no_abre_ningun_socket_que_no_sea_su_propia_api(self):
        js = self.cara("nexo.js")
        for prohibido in ("WebSocket", "EventSource", "sendBeacon",
                          "XMLHttpRequest", "import("):
            self.assertNotIn(prohibido, js)
        for llamada in re.findall(r"fetch\(\s*'([^']*)'", js):
            self.assertTrue(llamada.startswith("/api/"),
                            f"la cara pide fuera de su api: {llamada}")

    def test_33_todo_lo_que_se_pinta_pasa_por_el_escapador(self):
        js = self.cara("nexo.js")
        self.assertIn("const esc =", js)
        # `innerHTML` solo se escribe desde `pinta`, que recibe html ya escapado.
        self.assertEqual(js.count(".innerHTML"), 1,
                         "un segundo innerHTML es un segundo sitio donde revisar")

    def test_34_no_data_no_se_pinta_como_un_valor(self):
        js = self.cara("nexo.js")
        self.assertIn('class="nodata"', js)
        css = self.cara("hexelion.css")
        self.assertIn(".nodata{", css.replace(" ", ""))

    def test_35_cada_modulo_del_html_tiene_su_pintor_y_al_reves(self):
        html = self.cara("index.html")
        js = self.cara("nexo.js")
        en_html = set(re.findall(r'id="m-([a-z]+)"', html))
        pintores = set(re.findall(r"^  ([a-z]+)\(d\) \{", js, re.M))
        self.assertEqual(en_html, pintores,
                         "una tarjeta sin pintor se queda en «Cargando…» "
                         "para siempre y nadie se entera")

    def test_36_los_sensores_y_las_tarjetas_son_los_mismos(self):
        html = self.cara("index.html")
        en_html = set(re.findall(r'id="m-([a-z]+)"', html))
        self.assertEqual(en_html, set(registro.SENSORES),
                         "un sensor sin tarjeta es un dato que nadie ve")

    def test_37_la_pagina_se_sirve_entera_desde_el_nexo(self):
        with ServidorEnPie() as s:
            for ruta in ("/", "/hexelion.css", "/nexo.js"):
                with self.subTest(ruta=ruta):
                    codigo, cuerpo, cab = s.get(ruta)
                    self.assertEqual(codigo, 200)
                    self.assertTrue(cuerpo.strip())
                    self.assertEqual(cab["X-Frame-Options"], "DENY")


if __name__ == "__main__":
    unittest.main(verbosity=2)
