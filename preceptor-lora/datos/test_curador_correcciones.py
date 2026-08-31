#!/usr/bin/env python3
"""El eslabon [4]: Bronze -> Silver. Solo stdlib.

Lo que se comprueba aqui, sobre todo, es que el curador sepa DECIR QUE NO HAY.
Un dataset vacio y un dataset limpio se parecen mucho en un fichero de salida
y no significan lo mismo en absoluto. Es la misma trampa que S0 vigila en los
bucles: el filtro que da verde porque no miro.
"""
from __future__ import annotations

import os
import sqlite3
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import curador_correcciones as CC  # noqa: E402


def _memoria(filas):
    """Una memoria de mentira con el esquema REAL de preceptor/captura.py."""
    d = tempfile.mkdtemp()
    ruta = os.path.join(d, "memory.db")
    c = sqlite3.connect(ruta)
    c.executescript("""
    create table turnos (
        id integer primary key autoincrement,
        cuando text not null default (datetime('now')),
        prompt text not null, respuesta text not null,
        modelo text not null default 'NO_DATA',
        idioma text not null default 'NO_DATA',
        consent integer not null default 0,
        correccion text, corregido text,
        motivo text not null default 'NO_DATA');""")
    c.executemany(
        "insert into turnos (prompt,respuesta,modelo,idioma,consent,correccion,motivo)"
        " values (?,?,?,?,?,?,?)", filas)
    c.commit(); c.close()
    return ruta


class TestVacio(unittest.TestCase):

    def test_cero_correcciones_no_es_un_dataset_limpio(self):
        """La distincion que da sentido al modulo entero."""
        r = CC.curar(_memoria([]))
        self.assertEqual("NO_DATA", r["estado"])
        self.assertIn("ninguna", r["causa"].lower() + r["causa"])
        self.assertEqual([], r["pares"])

    def test_turnos_sin_consentimiento_no_entran(self):
        """`consent` nace en 0 y solo el carbono lo sube.

        Un par capturado no es material de entrenamiento: es un recuerdo de la
        persona. Colarlo en el dataset seria entrenar con algo que nadie
        autorizo, y es el fallo mas caro posible porque no se puede deshacer
        una vez esta en los pesos.
        """
        r = CC.curar(_memoria([
            ("p", "mala", "m", "es", 0, "buena", "porque si"),
        ]))
        self.assertEqual("NO_DATA", r["estado"])
        self.assertEqual([], r["pares"])
        self.assertEqual(1, r["descartados"]["sin_consentimiento"])

    def test_consentido_pero_sin_correccion_tampoco_es_un_par(self):
        """Media pieza no es un par: hace falta el rechazado Y el elegido."""
        r = CC.curar(_memoria([("p", "r", "m", "es", 1, None, "x")]))
        self.assertEqual([], r["pares"])
        self.assertEqual(1, r["descartados"]["sin_correccion"])


class TestAgrupacion(unittest.TestCase):

    def test_agrupa_por_modelo_base_y_skill(self):
        """Mezclar bases distintas en un dataset es entrenar sobre dos cosas."""
        r = CC.curar(_memoria([
            ("p1", "mala1", "preceptor-v7", "es", 1, "buena1", "tono"),
            ("p2", "mala2", "preceptor-v7", "es", 1, "buena2", "tono"),
            ("p3", "mala3", "otro-modelo", "es", 1, "buena3", "tono"),
        ]))
        self.assertEqual("MEDIDO", r["estado"])
        self.assertEqual(3, len(r["pares"]))
        self.assertEqual({"preceptor-v7", "otro-modelo"}, set(r["grupos"]))
        self.assertEqual(2, r["grupos"]["preceptor-v7"])

    def test_el_par_lleva_rechazado_y_elegido_con_esos_nombres(self):
        """El formato de preferencia que la Forja ya espera."""
        r = CC.curar(_memoria([("p", "mala", "m", "es", 1, "buena", "tono")]))
        par = r["pares"][0]
        self.assertEqual("mala", par["rechazado"])
        self.assertEqual("buena", par["elegido"])
        self.assertEqual("p", par["prompt"])
        self.assertEqual("m", par["modelo_base"])


class TestHonestidad(unittest.TestCase):

    def test_siempre_declara_cuantos_miro_y_cuantos_descarto(self):
        """Un filtro que no dice lo que descarta no se puede auditar."""
        r = CC.curar(_memoria([
            ("p", "r", "m", "es", 0, "c", "x"),
            ("p", "r", "m", "es", 1, None, "x"),
            ("p", "r", "m", "es", 1, "c", "x"),
        ]))
        self.assertEqual(3, r["mirados"])
        self.assertEqual(1, len(r["pares"]))
        self.assertEqual(2, sum(r["descartados"].values()))

    def test_sin_memoria_es_no_data_no_cero(self):
        r = CC.curar("/no/existe/memory.db")
        self.assertEqual("NO_DATA", r["estado"])
        self.assertTrue(r["causa"])


if __name__ == "__main__":
    unittest.main()
