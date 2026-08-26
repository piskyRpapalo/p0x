#!/usr/bin/env python3
"""Caos. Se rompe cada cosa a proposito y se exige que el panel diga la verdad.

La pregunta que contesta esta suite no es «¿aguanta?» sino **«¿que enseña
mientras no aguanta?»**. Un panel que sobrevive a la caida de un nodo pintando
el ultimo valor conocido ha aguantado y ha mentido, y mentir es la unica averia
de la que este arbol no se recupera: si el panel puede inventar una vez, deja de
poder creerse nunca.

Nada de esto necesita red. Se le miente a los sensores con `unittest.mock` --que
es como se simula un fallo sin provocarlo-- y se comprueba lo que sale.

Tres cosas que NO se comprueban aqui, y merecen decirse:

- **No se exige que un nodo caido se note en menos de dos segundos.** El panel
  refresca cada 30 s a proposito. Lo que si se mide es la latencia del
  MECANISMO: cuanto tarda un cambio en llegar desde que el refrescador lo ve.
  Confundir la cadencia con la latencia haria pasar una prueba que no prueba
  nada.
- **No se exige la etiqueta «RTL-SDR ausente».** Es un diagnostico, no una
  medida, y en este rack seria falso: la misma radio esta recibiendo ADS-B. Lo
  que se exige es que haya CAUSA MEDIDA, y hay un caso que prohibe expresamente
  afirmar ausencia de hardware.
- **No se exige un texto concreto en la cara.** Se exige que el hueco viaje con
  su motivo; como se redacte es otra cosa.
"""

import time
import unittest
from pathlib import Path
from unittest import mock

import fragmentos
import sensores
import vigia as V
from sensores import cinek, jardin, lora, nodos, preceptor  # noqa: F401
from sensores import registro, soberania, timers            # noqa: F401

NO_DATA = sensores.NO_DATA
CARA = Path(__file__).resolve().parent / "estatico"

# Un tailnet de mentira: cuatro nodos, uno de ellos caido.
RACK = [("nodo-uno", "metal", "nucleo publico · inferencia local", "uno"),
        ("nodo-dos", "metal", "gateway · voz", "dos"),
        ("nodo-tres", "metal", "adquisicion RF · ADS-B y AIS", "tres"),
        ("nodo-cuatro", "metal", "inferencia acelerada", "cuatro")]

SALUD = {"nodes": [{"node_id": "cuatro", "health": "online",
                    "probes": {"ollama_11434": True}}]}
ANTENA_SANA = {"ais": {"live": True, "vessels": 12},
               "adsb": {"live": True, "aircraft": 9}}
ANTENA_ROTA = {"ais": {"live": False, "vessels": 0},
               "adsb": {"live": True, "aircraft": 9}}


def _rack(vivos, salud=SALUD, antena=ANTENA_SANA, revienta_gateway=False):
    """Lee el sensor de nodos contra un mundo inventado."""
    def remoto(_base, ruta):
        if revienta_gateway:
            raise TimeoutError("el gateway no contesta")
        return antena if "antenna" in ruta else salud
    with mock.patch.object(nodos, "rack", return_value=RACK), \
         mock.patch.object(nodos, "propio", return_value="nodo-uno"), \
         mock.patch.object(nodos, "gateway", return_value="http://inventado"), \
         mock.patch.object(nodos, "_tailscale", return_value=vivos), \
         mock.patch.object(nodos, "_json_remoto", side_effect=remoto):
        return nodos.leer()


def _fila(lectura, nombre):
    return next(f for f in lectura["nodos"] if f["nodo"] == nombre)


class CaeUnNodo(unittest.TestCase):
    """El tailnet deja de verlo. No se hereda el ultimo valor conocido."""

    TODOS = {"nodo-uno": True, "nodo-dos": True,
             "nodo-tres": True, "nodo-cuatro": True}

    def test_1_un_nodo_vivo_sale_en_pie(self):
        """El control negativo. Sin el, un sensor que dijera OFFLINE siempre
        pasaria toda esta suite."""
        self.assertEqual(_fila(_rack(self.TODOS), "nodo-dos")["estado"], "ONLINE")

    def test_2_un_nodo_que_cae_sale_offline_y_no_con_su_ultimo_valor(self):
        caido = dict(self.TODOS, **{"nodo-dos": False})
        fila = _fila(_rack(caido), "nodo-dos")
        self.assertEqual(fila["estado"], "OFFLINE")
        self.assertEqual(fila["nota"], "no responde en el tailnet")

    def test_3_un_nodo_que_el_tailnet_no_nombra_es_hueco_no_es_caido(self):
        """No saber de un nodo y saber que esta caido son cosas distintas.

        Pintar la primera como la segunda es inventar: OFFLINE es una
        afirmacion sobre el mundo, y aqui no hay con que sostenerla.
        """
        fila = _fila(_rack({"nodo-uno": True}), "nodo-tres")
        self.assertEqual(fila["estado"], NO_DATA)
        self.assertNotEqual(fila["estado"], "OFFLINE")

    def test_4_la_tarjeta_del_nodo_caido_no_lleva_ni_un_cero_decorativo(self):
        caido = dict(self.TODOS, **{"nodo-dos": False})
        html = fragmentos.html_de("nodos", _rack(caido))
        self.assertIn("OFFLINE", html)
        self.assertNotIn(">0<", html, "un cero es indistinguible de una medida")

    def test_5_ni_un_indicador_de_espera_en_toda_la_cara(self):
        """El sitio donde vive la mentira comoda: girar para siempre en vez de
        decir que no hay dato."""
        for fichero in ("index.html", "static/nexo.js", "static/hexelion.css"):
            bajo = (CARA / fichero).read_text(encoding="utf-8").lower()
            with self.subTest(fichero=fichero):
                for girando in ("spinner", "@keyframes", "animation:",
                                "cargando…", "loading"):
                    self.assertNotIn(girando, bajo)


class CaeElGateway(unittest.TestCase):
    """Sin sondas profundas el panel sigue, y dice de que se ha quedado ciego."""

    TODOS = {"nodo-uno": True, "nodo-dos": True,
             "nodo-tres": True, "nodo-cuatro": True}

    def test_6_el_panel_no_se_cae_con_el_gateway(self):
        lectura = _rack(self.TODOS, revienta_gateway=True)
        self.assertEqual(lectura["estado"], "ok")
        self.assertEqual(len(lectura["nodos"]), 4)

    def test_7_lo_que_dependia_del_gateway_queda_declarado(self):
        lectura = _rack(self.TODOS, revienta_gateway=True)
        self.assertTrue(lectura["avisos"])
        self.assertIn("gateway", " ".join(lectura["avisos"]).lower())
        self.assertNotIn("gateway de la forja", lectura["fuente"],
                         "la fuente no puede seguir citando lo que ya no habla")

    def test_8_sin_gateway_no_se_afirma_nada_sobre_los_servicios(self):
        """Lo que se sabe --responde en el tailnet-- se dice. Lo demas, no."""
        fila = _fila(_rack(self.TODOS, revienta_gateway=True), "nodo-cuatro")
        self.assertEqual(fila["estado"], "ONLINE")
        self.assertIn(NO_DATA, fila["nota"])
        self.assertNotEqual(fila["estado"], "EN ESPERA")

    def test_9_la_cara_sabe_decir_cuanto_lleva_sin_flujo(self):
        js = (CARA / "static" / "nexo.js").read_text(encoding="utf-8")
        self.assertIn("sin latido desde hace", js)
        self.assertIn("ultimoLatido", js)
        self.assertIn("classList.add('rancio')", js)


class FaltaUnSentido(unittest.TestCase):
    """Una cadena de radio caida. Con su causa medida, no con un diagnostico."""

    TODOS = {"nodo-uno": True, "nodo-dos": True,
             "nodo-tres": True, "nodo-cuatro": True}

    def test_10_la_cadena_sana_no_dispara_nada(self):
        self.assertEqual(_fila(_rack(self.TODOS), "nodo-tres")["estado"], "ONLINE")

    def test_11_la_cadena_caida_sale_critica_con_alerta(self):
        fila = _fila(_rack(self.TODOS, antena=ANTENA_ROTA), "nodo-tres")
        self.assertEqual(fila["estado"], "CRITICO")
        self.assertTrue(fila["alerta"], "un rojo sin causa no se puede reparar")

    def test_12_no_se_afirma_que_falte_hardware(self):
        """El diagnostico comodo seria «la radio no esta». Seria falso: la otra
        cadena esta recibiendo por esa misma radio. Se nombra el servicio."""
        fila = _fila(_rack(self.TODOS, antena=ANTENA_ROTA), "nodo-tres")
        texto = (fila["alerta"] + " " + fila["nota"]).lower()
        for afirmacion in ("desconectado", "ausente", "no conectado",
                           "sin hardware", "dongle"):
            self.assertNotIn(afirmacion, texto,
                             "eso es un diagnostico, no una medida")
        self.assertIn("ais", texto)

    def test_13_lo_que_si_recibe_se_sigue_diciendo(self):
        """Media radio caida no apaga la otra media."""
        fila = _fila(_rack(self.TODOS, antena=ANTENA_ROTA), "nodo-tres")
        self.assertIn("9", fila["nota"])


class LaLatenciaDelMecanismo(unittest.TestCase):
    """Cuanto tarda un cambio en salir. No es lo mismo que cada cuanto se mira."""

    def test_14_un_cambio_se_publica_en_cuanto_el_refrescador_lo_ve(self):
        v = V.Vigia(cada=999)
        try:
            v.refrescar()
            _, version, _ = v.instantanea()
            with mock.patch.object(registro, "uno",
                                   return_value=sensores.hueco("caos")):
                t0 = time.monotonic()
                v.refrescar()
                tarjetas, nueva, _ = v.instantanea()
                tardado = time.monotonic() - t0
            self.assertGreater(nueva, version, "el cambio tiene que publicarse")
            self.assertLess(tardado, 2.0, f"tardo {tardado:.2f} s")
            self.assertIn(NO_DATA, tarjetas["nodos"])
        finally:
            v.parar()

    def test_15_quien_espera_se_entera_sin_preguntar(self):
        """El flujo no sondea: duerme sobre la Condition hasta que hay novedad."""
        import threading
        v = V.Vigia(cada=999)
        recibido = []
        try:
            v.refrescar()
            _, version, _ = v.instantanea()

            def mirar():
                recibido.append(v.espera(version, 3.0)[1])

            hilo = threading.Thread(target=mirar)
            hilo.start()
            time.sleep(0.1)
            with mock.patch.object(registro, "uno",
                                   return_value=sensores.hueco("caos")):
                v.refrescar()
            hilo.join(timeout=3)
            self.assertTrue(recibido, "el que esperaba no desperto")
            self.assertGreater(recibido[0], version)
        finally:
            v.parar()


class MetricaDeHonestidad(unittest.TestCase):
    """El barrido: ningun hueco puede viajar mudo, en ningun sensor."""

    def test_16_todo_hueco_lleva_causa_en_todos_los_sensores(self):
        mudos = []
        for nombre in sorted(registro.SENSORES):
            lectura = registro.uno(nombre)
            if lectura["estado"] != "ok" and not lectura.get("causa"):
                mudos.append(nombre)
        self.assertEqual(mudos, [], f"huecos sin causa: {mudos}")

    def test_17_todo_hueco_lleva_causa_tambien_con_el_sensor_reventado(self):
        for nombre in sorted(registro.SENSORES):
            with self.subTest(sensor=nombre):
                with mock.patch.dict(registro.SENSORES,
                                     {nombre: lambda: 1 / 0}):
                    lectura = registro.uno(nombre)
                self.assertEqual(lectura["estado"], NO_DATA)
                self.assertTrue(lectura["causa"])

    def test_18_ninguna_causa_dice_desconocido(self):
        """«unknown» es un hueco que no explica nada: tiene la forma de una
        causa y no lo es."""
        for nombre in sorted(registro.SENSORES):
            causa = (registro.uno(nombre).get("causa") or "").lower()
            with self.subTest(sensor=nombre):
                for vacia in ("unknown", "desconocido", "n/a", "error",
                              "algo fallo", "???"):
                    self.assertNotIn(vacia, causa)

    def test_19_ningun_estado_de_nodo_viaja_sin_explicarse(self):
        vivos = {"nodo-uno": True, "nodo-dos": False, "nodo-cuatro": True}
        for antena in (ANTENA_SANA, ANTENA_ROTA):
            for fila in _rack(vivos, antena=antena)["nodos"]:
                with self.subTest(nodo=fila["nodo"], ais=antena["ais"]["live"]):
                    self.assertTrue(fila["nota"], "un estado sin nota es mudo")
                    if fila["estado"] == "CRITICO":
                        self.assertTrue(fila["alerta"])

    def test_20_el_hueco_llega_hasta_el_html_y_se_ve(self):
        """Que el dato sea honesto no basta: tiene que llegar honesto a la cara."""
        for nombre in sorted(registro.SENSORES):
            html = fragmentos.html_de(nombre, sensores.hueco("el caos"))
            with self.subTest(sensor=nombre):
                self.assertIn("nodata", html)
                self.assertIn("el caos", html, "la causa tiene que verse")


if __name__ == "__main__":
    unittest.main(verbosity=2)
