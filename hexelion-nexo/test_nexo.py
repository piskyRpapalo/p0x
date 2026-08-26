#!/usr/bin/env python3
"""Pruebas del Nexo. Lo que tiene que ser verdad de un panel que solo mira.

Ninguna toca el arbol de PreceptorOS ni escribe fuera de su temporal. El
servidor se levanta en un puerto efimero de verdad -- no se simula-- porque lo
que se quiere comprobar es el comportamiento por HTTP, y un doble de la clase
no responde 501 a un POST por su cuenta.
"""

import json
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


if __name__ == "__main__":
    unittest.main(verbosity=2)
