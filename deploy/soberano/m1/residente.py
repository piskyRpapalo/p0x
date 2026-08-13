#!/usr/bin/env python3
"""M1 · el hijo residente · las dos capas vivas entre mensajes.

Residente NO es servicio. No hay puerto, no hay socket, no hay nada escuchando:
son dos procesos hijos con sus tuberias abiertas, que siguen vivos porque nadie
los ha cerrado todavia. Si este programa muere, mueren con el. Eso es
exactamente lo que un servicio NO hace, y por eso esto cumple D75.

Lo que ahorra: el modelo tarda ~2,3 s en cargarse desde disco. Pagarlo una vez
por conversacion en vez de una vez por frase es la diferencia entre hablar y
esperar.

Uso:  python3 residente.py            (interactivo, escribe y responde)
      python3 residente.py --medir    (mide y sale: es el numero del reporte)
"""
from __future__ import annotations

import argparse
import os
import subprocess
import sys
import time

CASA = os.path.expanduser("~/aurelius-m1")
LLAMA = os.path.expanduser(
    "~/soberano-bench/bin/llama-b10068-bin-ubuntu-vulkan-x64/llama-b10068")
MODELO = os.path.expanduser(
    "~/soberano-bench/models/Qwen3-4B-Instruct-2507-Q4_K_M.gguf")
VOZ = os.path.join(CASA, "voces", "es_ES-sharvard-medium.onnx")
PIPER = os.path.join(CASA, "venv", "bin", "piper")
ARQUETIPO = os.path.expanduser("~/aurelius-mvp/ARQUETIPO.md")
CONTEXTO = 4096
FIN = "\x04"


def caracter(idioma="es"):
    seccion = ("## §3 · El texto · Español" if idioma == "es"
               else "## §2 · El texto · English")
    doc = open(ARQUETIPO, encoding="utf-8").read()
    return doc.split(seccion)[1].split("```")[1].strip()


class Cerebro:
    """llama-cli vivo, hablando por sus tuberias. Un hijo, no un servidor."""

    def __init__(self, idioma="es"):
        entorno = dict(os.environ, LD_LIBRARY_PATH=LLAMA)
        self.proc = subprocess.Popen(
            [os.path.join(LLAMA, "llama-cli"),
             "-m", MODELO, "-c", str(CONTEXTO), "-ngl", "99",
             # Sin -st: eso es "un solo turno" y mataba al residente tras la
             # primera frase. Un hijo que muere en cada mensaje no es residente,
             # es el modo de siempre con otro nombre.
             "--no-warmup", "-sys", caracter(idioma)],
            stdin=subprocess.PIPE, stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL, env=entorno, text=True, bufsize=1)
        self._hasta_prompt()

    def _hasta_prompt(self):
        """Lee hasta que el hijo pide turno.

        El turno es "> " AL PRINCIPIO DE LINEA. Buscarlo en cualquier posicion
        no vale: el banner de ayuda del propio programa lleva "/read <file>",
        y ese "> " interno cortaba la lectura antes de tiempo. Se descubrio
        midiendo — los dos primeros turnos devolvian trozos del banner en 0,00 s,
        que es la clase de cifra que uno querria creerse.
        """
        buf = ""
        while True:
            ch = self.proc.stdout.read(1)
            if not ch:
                return buf
            buf += ch
            if buf.endswith("\n> "):
                return buf

    def pregunta(self, texto):
        self.proc.stdin.write(texto + "\n")
        self.proc.stdin.flush()
        crudo = self._hasta_prompt()
        # La respuesta es lo que hay entre el eco de la pregunta y el turno
        # siguiente. Se limpian los adornos de la interfaz, no el contenido.
        lineas = [l for l in crudo.splitlines()
                  if l.strip() and not l.startswith("[ Prompt:")
                  and l.strip() != texto.strip() and l.strip() != ">"]
        return "\n".join(lineas).strip().rstrip(">").strip()

    def cierra(self):
        try:
            self.proc.stdin.close()
        except OSError:
            pass
        self.proc.terminate()


class Voz:
    """piper vivo, una invocacion por frase pero sin recargar el modelo.

    piper termina cuando su entrada se cierra, asi que lo residente aqui es el
    modelo de voz en cache de pagina, no el proceso. Se declara: el ahorro es
    real pero menor que el del cerebro, y decir lo contrario seria inventar.
    """

    def __init__(self, hablante="0"):
        self.hablante = hablante
        self.hay = os.path.exists(PIPER) and os.path.exists(VOZ)

    def di(self, texto):
        if not self.hay:
            return None
        t0 = time.perf_counter()
        crudo = subprocess.run(
            [PIPER, "-m", VOZ, "-s", self.hablante, "--output-raw"],
            input=texto.encode("utf-8"), capture_output=True).stdout
        return time.perf_counter() - t0, len(crudo) / 2 / 22050


def medir():
    print("── hijo residente · medida en este metal " + "─" * 26)
    t0 = time.perf_counter()
    cerebro = Cerebro()
    arranque = time.perf_counter() - t0
    print(f"  arranque del hijo (una vez por conversacion): {arranque:.2f} s")

    preguntas = ["He perdido una tarde de trabajo. ¿Qué hago?",
                 "¿Y si no guardé nada?",
                 "Gracias."]
    tiempos = []
    for p in preguntas:
        t0 = time.perf_counter()
        r = cerebro.pregunta(p)
        dt = time.perf_counter() - t0
        tiempos.append(dt)
        print(f"  turno {len(tiempos)}: {dt:.2f} s · {r[:64]!r}")
    cerebro.cierra()

    voz = Voz()
    if voz.hay:
        dt, dur = voz.di("No veo discos. Dime qué pasa.")
        print(f"  voz: {dt:.2f} s para {dur:.1f} s de audio")

    print(f"\n  RESIDENTE · turno medio {sum(tiempos)/len(tiempos):.2f} s "
          f"(sin volver a cargar el modelo)")
    print(f"  el arranque de {arranque:.2f} s se paga UNA vez, no en cada frase")
    return 0


def main():
    ap = argparse.ArgumentParser(description="Aurelius M1 · hijo residente")
    ap.add_argument("--medir", action="store_true")
    a = ap.parse_args()
    if a.medir:
        return medir()
    cerebro = Cerebro()
    voz = Voz()
    print("Aurelius vivo. Ctrl+D para cerrar.\n")
    try:
        while True:
            try:
                linea = input("> ").strip()
            except EOFError:
                break
            if not linea:
                continue
            print(cerebro.pregunta(linea))
    finally:
        cerebro.cierra()
    return 0


if __name__ == "__main__":
    sys.exit(main())
