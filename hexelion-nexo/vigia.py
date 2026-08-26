"""Un solo lector, muchos mirones.

El problema que resuelve: con N pestañas abiertas y un sensor por peticion, N
navegadores hacen que se hable con systemd, con el disco y con el tailnet N
veces cada treinta segundos. La cuenta crece con la audiencia, y la audiencia
no deberia costar nada.

Aqui hay **un** hilo que refresca la instantanea y la deja compuesta en HTML.
Los flujos abiertos no leen sensores: esperan a que suba el numero de version y
mandan lo que haya cambiado. Abrir una pestaña mas cuesta un socket, no una
ronda de sondas.

Y por eso el flujo nunca se bloquea leyendo: cuando el sensor de nodos tarda
cuatro segundos contra el tailnet, quien espera es el refrescador, no los que
miran.
"""

import threading

import fragmentos
from sensores import registro

CADA = 30.0


class Vigia:
    def __init__(self, cada=CADA):
        self.cada = cada
        self._cond = threading.Condition()
        self._tarjetas = {}      # nombre -> html de la seccion
        self._version = 0
        self._medido = ""
        self._parar = threading.Event()
        self._hilo = None

    # ── lectura ──────────────────────────────────────────────────────────
    def instantanea(self):
        with self._cond:
            return dict(self._tarjetas), self._version, self._medido

    def espera(self, desde, tiempo=25.0):
        """Bloquea hasta que haya version nueva. Devuelve lo que cambio.

        El tiempo maximo existe para que un flujo que lleva rato quieto pueda
        mandar un latido: sin el, un proxy silencioso por el medio cierra la
        conexion creyendola muerta, y el navegador no distingue eso de un fallo.
        """
        with self._cond:
            if self._version <= desde:
                self._cond.wait(tiempo)
            return dict(self._tarjetas), self._version, self._medido

    # ── el hilo ──────────────────────────────────────────────────────────
    def refrescar(self):
        """Una ronda. Devuelve los nombres cuya tarjeta cambio."""
        # Se recorren las TARJETAS y no los sensores: dos tarjetas pueden comer
        # del mismo sensor --el rack y la malla lo hacen-- y en ese caso la
        # lectura se hace UNA vez y se compone dos.
        lecturas, nuevas = {}, {}
        for nombre in fragmentos.TARJETAS:
            fuente = fragmentos.sensor_de(nombre)
            if fuente not in lecturas:
                # `registro.uno` ya es a prueba de balas: un sensor que revienta
                # devuelve hueco, no excepcion. Aqui no hay nada que capturar.
                lecturas[fuente] = registro.uno(fuente)
            nuevas[nombre] = fragmentos.html_de(nombre, lecturas[fuente])
        with self._cond:
            cambiadas = [n for n, h in nuevas.items() if self._tarjetas.get(n) != h]
            if cambiadas:
                self._tarjetas.update(nuevas)
                self._version += 1
                self._medido = fragmentos.NO_DATA
            self._medido = _ahora()
            self._cond.notify_all()
        return cambiadas

    def _bucle(self):
        while not self._parar.is_set():
            self.refrescar()
            self._parar.wait(self.cada)

    def arrancar(self):
        self.refrescar()                      # la primera, antes de servir nada
        self._hilo = threading.Thread(target=self._bucle, daemon=True,
                                      name="vigia")
        self._hilo.start()
        return self

    def parar(self):
        self._parar.set()
        with self._cond:
            self._cond.notify_all()
        if self._hilo is not None:
            self._hilo.join(timeout=2)


def _ahora():
    import sensores
    return sensores.ahora()
