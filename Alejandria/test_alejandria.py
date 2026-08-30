#!/usr/bin/env python3
"""El gate de la capa Alejandria. No existia ninguno.

POR QUE HACE FALTA UN GATE PROPIO
---------------------------------
Los dos gates del proyecto no miran aqui, y no por descuido: el del MVP tiene su
raiz en `preceptor/` y `Alejandria/` es su hermano, no su hijo; el de la web
solo escanea `public/` de otro repositorio.

Asi que hasta hoy esta capa -- la que MIDE el rack y la que el Soberano lee para
decidir -- no tenia quien la midiera a ella. El instrumento sin instrumento.

    python3 ~/p0x/Alejandria/test_alejandria.py
"""
from __future__ import annotations

import json
import os
import sys
import tempfile
import unittest
from pathlib import Path

RAIZ = Path(__file__).resolve().parent
sys.path.insert(0, str(RAIZ / "mensajes"))
import mensajes as M  # noqa: E402

# D1-bis, firmada el 2026-08-30: el mismo tope que el Agora para la consola.
# El alcance es HTML/JS/CSS, como D1; el Python queda fuera.
#
# El motivo no es el peso de descarga -- el Ojo se sirve en loopback y no paga
# latencia de red, igual que la interfaz de la app, que por eso quedo exenta de
# D1. El motivo es que se lea: `ojo.js` llego al 94,5 % del cupo y la respuesta
# correcta fue partir en modulos, no engordar. Cuatro ficheros pequenos se leen;
# uno de 25 KB no, y `dashboard.js` es la prueba de a donde lleva no tener tope.
TOPE = 10 * 1024
CONSOLA = RAIZ / "ojo"


class PesoDeLaConsola(unittest.TestCase):

    def test_cada_fichero_de_la_consola_bajo_10_kb(self):
        for p in sorted(CONSOLA.rglob("*")):
            if p.is_file() and p.suffix in (".html", ".css", ".js"):
                with self.subTest(fichero=p.name):
                    self.assertLess(
                        p.stat().st_size, TOPE,
                        f"{p.name} pesa {p.stat().st_size} B · D1-bis son "
                        f"{TOPE}. Partelo en modulos, no lo recortes: los "
                        "comentarios de esta capa son su razonamiento.")

    def test_la_consola_solo_escucha_en_loopback(self):
        """Que nadie la ate a 0.0.0.0 «temporalmente».

        La auditoria del 2026-08-30 encontro un `http.server` en 0.0.0.0:8080
        sin auth ni logs, seis horas expuesto. El Ojo ensena el rack ENTERO: si
        se ata a todas las interfaces, lo reparte.
        """
        codigo = (CONSOLA / "ojo.py").read_text(encoding="utf-8")
        self.assertIn('("127.0.0.1", a.puerto)', codigo,
                      "el Ojo ya no fija 127.0.0.1 al abrir el socket")
        self.assertNotIn('"0.0.0.0"', codigo, "el Ojo escucha fuera de loopback")


class ElActa(unittest.TestCase):
    """Los tres candados del acta. Cada uno se prueba ensuciandola de verdad."""

    def setUp(self):
        self.dir = tempfile.mkdtemp()
        self.ruta = Path(self.dir) / "mensajes.jsonl"

    def _uno(self, humano="Dos hallazgos y 3 commits.", maquina=None, fuente=None):
        return M.escribir(
            de="enlace", para=["soberano"], tipo="digesto",
            humano=humano,
            maquina=maquina if maquina is not None else
            {"hechos": ["2 hallazgos", "3 commits"], "acciones": []},
            fuente=fuente if fuente is not None else ["loops.db:latidos"],
            ruta=self.ruta)

    def test_la_cadena_sana_se_verifica(self):
        for _ in range(3):
            self._uno()
        self.assertEqual(M.verificar(self.ruta), [])

    def test_un_mensaje_sin_fuente_no_se_escribe(self):
        with self.assertRaises(ValueError) as e:
            self._uno(fuente=[])
        self.assertIn("fuente", str(e.exception))

    def test_una_linea_modificada_rompe_la_cadena(self):
        self._uno(); self._uno(); self._uno()
        lineas = self.ruta.read_text(encoding="utf-8").splitlines()
        m = json.loads(lineas[1])
        m["humano"] = "esto lo cambio alguien despues"      # sin recalcular hash
        lineas[1] = json.dumps(m, ensure_ascii=False)
        self.ruta.write_text("\n".join(lineas) + "\n", encoding="utf-8")

        rotos = M.verificar(self.ruta)
        self.assertTrue(rotos, "el acta se dejo modificar sin protestar")
        self.assertTrue(any("cambió después de escribirse" in r for r in rotos),
                        f"no senala la edicion: {rotos}")
        # Y la siguiente tambien cae: la cadena propaga.
        self.assertTrue(any("se insertó, se borró o se reordenó" in r for r in rotos),
                        f"la cadena no propago el fallo: {rotos}")

    def test_una_linea_borrada_rompe_la_cadena(self):
        self._uno(); self._uno(); self._uno()
        lineas = self.ruta.read_text(encoding="utf-8").splitlines()
        del lineas[1]
        self.ruta.write_text("\n".join(lineas) + "\n", encoding="utf-8")
        self.assertTrue(M.verificar(self.ruta),
                        "borrar una linea del medio no rompio nada")

    def test_no_se_escribe_encima_de_un_acta_rota(self):
        self._uno(); self._uno()
        lineas = self.ruta.read_text(encoding="utf-8").splitlines()
        m = json.loads(lineas[0]); m["humano"] = "manipulado"
        lineas[0] = json.dumps(m, ensure_ascii=False)
        self.ruta.write_text("\n".join(lineas) + "\n", encoding="utf-8")
        with self.assertRaises(M.ActaRota):
            self._uno()

    def test_las_dos_caras_tienen_que_contar_lo_mismo(self):
        """Criterio B5 del Medallon, aplicado a lo comprobable.

        No se juzga la prosa -- eso es justo lo que el Medallon dice que no
        cuenta. Se comprueba que toda cifra de la cara humana este respaldada
        por la de maquina: un numero que solo existe en el texto no lo midio
        nadie.
        """
        with self.assertRaises(ValueError) as e:
            self._uno(humano="Se cerraron 47 hallazgos.",
                      maquina={"hechos": ["2 hallazgos"], "acciones": []})
        self.assertIn("47", str(e.exception))

    def test_el_acta_viva_del_nodo_esta_sana(self):
        """La de verdad, no una de mentira."""
        viva = RAIZ / "mensajes" / "mensajes.jsonl"
        if not viva.exists():
            self.skipTest("todavia no hay acta en este nodo")
        self.assertEqual(M.verificar(viva), [])


class ElGlosario(unittest.TestCase):

    def test_cada_entrada_declara_su_fuente(self):
        ruta = CONSOLA / "glosario.json"
        if not ruta.exists():
            self.skipTest("todavia no hay glosario")
        datos = json.loads(ruta.read_text(encoding="utf-8"))
        for e in datos["entradas"]:
            with self.subTest(termino=e.get("termino")):
                for campo in ("termino", "que_hace", "donde_verlo", "fuente"):
                    self.assertTrue(e.get(campo),
                                    f"falta `{campo}`: sin fuente es prosa inventada")

    def test_lo_que_no_existe_se_declara_no_data(self):
        """El glosario incluye conceptos NO construidos a proposito.

        `dead_path`, el director cronificado y S0 estan especificados y no
        existen. Un glosario que solo cuenta lo que hay deja creer que lo demas
        funciona -- y son justo las piezas que vigilan a las otras.
        """
        ruta = CONSOLA / "glosario.json"
        if not ruta.exists():
            self.skipTest("todavia no hay glosario")
        datos = json.loads(ruta.read_text(encoding="utf-8"))
        sin_dato = [e for e in datos["entradas"] if e.get("estado") == "NO_DATA"]
        self.assertTrue(sin_dato,
                        "ninguna entrada declara NO_DATA: sospechoso, porque "
                        "hay piezas medidas como no construidas")


if __name__ == "__main__":
    unittest.main(verbosity=1)
