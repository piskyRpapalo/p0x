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

# El tope de la capa Alejandria: 32 KB por fichero.
#
# CORRIGE a la D1-bis de 10 KB que se firmo antes: `plan_v5.md` -- el contrato
# visual y de prioridades vigente -- abre con «Capa Alejandria: tope 32 KB/
# fichero», y ese contrato manda sobre una regla mia anterior.
#
# El motivo del cambio es el Ojo-Vivo: la topologia, los estados y el
# mobiliario que vienen en V1-V4 no caben en 10 KB por fichero sin trocear la
# consola en una docena de modulos, y una docena de ficheros de 800 bytes no se
# lee mejor que cuatro de 8 KB -- se lee peor.
#
# Lo que NO cambia es por que hay tope: el Ojo se sirve en loopback y no paga
# latencia de red, asi que esto no protege una descarga; protege que el fichero
# se pueda leer entero. `dashboard.js` con 25 KB es la prueba de a donde lleva
# no tener ninguno.
TOPE = 32 * 1024
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


class GateDelEnlace(unittest.TestCase):
    """B1-B5 del Medallon, comprobados sin llamar al modelo.

    Se le pasa prosa sintetica a `gate()` y se mira que veredicto da. No hace
    falta Ollama: el gate es codigo determinista, y una prueba que necesitara
    el modelo para comprobar el gate del modelo seria su propia contradiccion.
    """

    def setUp(self):
        sys.path.insert(0, str(RAIZ / "digesto"))
        import digesto
        self.D = digesto
        self.lista = [
            {"clave": "bucle guardian", "valor": "ok · 77 ficheros mirados",
             "fuente": "loops.db:latidos/guardian"},
            {"clave": "mvp_gate", "valor": "436 pruebas en verde",
             "fuente": "estado.json:mvp_gate"},
        ]
        self.huecos = [("dead_path.jsonl", "no existe; fase F1 pendiente",
                        "construir F1")]

    def _prosa(self, firma="¿Firmas la F1?", extra=""):
        return ("## Qué pasó\n- El guardián miró 77 ficheros. "
                "[loops.db:latidos/guardian]\n" + extra +
                "\n## Qué piensa cada agente\n- guardian: 77 ficheros. "
                "[loops.db:latidos/guardian]\n"
                "\n## Qué necesita tu firma\n" + firma +
                "\n\n## NO_DATA\n- no existe [dead_path.jsonl]\n")

    def test_una_parafrasis_limpia_pasa(self):
        self.assertEqual(self.D.gate(self._prosa(), self.lista, self.huecos), [])

    def test_B3_muerde_con_una_fuente_inventada(self):
        mala = self._prosa(extra="- Segun el informe. [informe_secreto.md]\n")
        fallos = self.D.gate(mala, self.lista, self.huecos)
        self.assertTrue(any(f.startswith("B3") for f in fallos), fallos)
        self.assertIn("informe_secreto.md", " ".join(fallos))

    def test_B3_admite_varias_fuentes_en_un_corchete(self):
        """Una viñeta que resume dos hechos cita los dos. Es legitimo.

        El gate leia el corchete entero como UNA fuente y tumbaba parafrasis
        correctas. Este caso existe para que no vuelva a pasar.
        """
        buena = self._prosa(extra="- Todo verde. "
                            "[loops.db:latidos/guardian, estado.json:mvp_gate]\n")
        self.assertEqual([f for f in self.D.gate(buena, self.lista, self.huecos)
                          if f.startswith("B3")], [])

    def test_B3_admite_citar_algo_que_venia_DENTRO_de_un_hecho(self):
        """El material entregado incluye el TEXTO de los huecos, no solo su clave.

        La primera corrida real tumbo una parafrasis correcta porque el modelo
        cito `F1`, que estaba dentro de la causa de un hueco que se le habia
        dado. Citar lo que se leyo es lo que B3 pide, no lo que prohibe.
        """
        buena = self._prosa(extra="- Falta la fase. [construir F1]\n")
        self.assertEqual([f for f in self.D.gate(buena, self.lista, self.huecos)
                          if f.startswith("B3")], [])

    def test_un_corchete_sin_cerrar_no_inventa_una_cita(self):
        """Medido en una corrida real del cierre.

        El modelo dejo `[loops.db:latidos/afinador` sin cerrar, y el patron se
        trago texto hasta el `]` de otro parrafo: B3 denuncio como fuente
        inventada un trozo de prosa («37 suites confirmadas,
        docs/bandeja_firmas»). No se puede exigir la fuente de algo que el
        modelo no llego a declarar como cita.
        """
        rota = ("## Qué pasó\n- El afinador certificó. [loops.db:latidos/afinador\n"
                "- 37 suites confirmadas. [estado.json:mvp_gate]\n"
                "\n## Qué piensa cada agente\n- guardian: 77. "
                "[loops.db:latidos/guardian]\n"
                "\n## Qué necesita tu firma\n¿Firmas?\n"
                "\n## NO_DATA\n- no existe [dead_path.jsonl]\n")
        self.assertEqual([f for f in self.D.gate(rota, self.lista, self.huecos)
                          if f.startswith("B3")], [])

    def test_B2_muerde_si_hay_huecos_y_no_se_declaran(self):
        sin = self._prosa().replace("## NO_DATA\n- no existe [dead_path.jsonl]\n", "")
        self.assertTrue(any(f.startswith("B2")
                            for f in self.D.gate(sin, self.lista, self.huecos)))

    def test_B4_muerde_con_dos_preguntas(self):
        dos = self._prosa(firma="¿Firmas la F1? ¿Y el puerto?")
        self.assertTrue(any(f.startswith("B4")
                            for f in self.D.gate(dos, self.lista, self.huecos)))

    def test_sin_prosa_no_hay_nada_que_juzgar(self):
        """Si el modelo no respondio, el digesto sale con los hechos y ya.
        Juzgar la ausencia como fallo perderia la medida por culpa del adorno."""
        self.assertEqual(self.D.gate(None, self.lista, self.huecos), [])


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
