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


PRODUCTO = os.path.expanduser("~/aurelius-mvp")


def _wav(crudo):
    import io
    import wave
    buf = io.BytesIO()
    with wave.open(buf, "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(22050)
        w.writeframes(crudo)
    return buf.getvalue()


class Cara:
    """El puente residente -> cara. Sin socket, y conviene decir por que.

    Una pagina abierta con doble clic desde el disco no puede recibir nada de
    un proceso local: para eso haria falta un puerto, y un puerto es justo lo
    que D75 cierra. Asi que el puente va en la direccion que SI existe — el
    residente produce el turno de verdad, sintetiza su voz, y REESCRIBE la
    cara con las dos cosas dentro. El boton reproduce una respuesta real,
    no una linea grabada de antemano.

    Lo que este puente NO hace, dicho aqui para que nadie lo descubra por
    sorpresa: la pregunta se escribe en el terminal, no en la pagina. Que la
    pagina pregunte exige socket (prohibido) o que la persona elija un fichero
    en cada turno. Esa decision es del Soberano, no mia.
    """

    def __init__(self, ruta_db, salida):
        self.ruta_db, self.salida = ruta_db, salida
        self.turnos = []

    def anota(self, pregunta, respuesta, crudo, lore=None):
        import base64
        turno = {"tu": pregunta, "el": respuesta}
        if crudo:
            turno["audio"] = ("data:audio/wav;base64,"
                              + base64.b64encode(_wav(crudo)).decode())
        if lore:
            turno["lore"] = lore
        self.turnos.append(turno)

    def refresca(self):
        import json
        import tempfile
        with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False,
                                         encoding="utf-8") as fh:
            json.dump(self.turnos, fh, ensure_ascii=False)
            ruta = fh.name
        r = subprocess.run(
            [sys.executable, os.path.join(PRODUCTO, "cara.py"),
             "--db", self.ruta_db, "--out", self.salida,
             "--turnos", ruta, "--sin-voz"],
            cwd=PRODUCTO, capture_output=True, text=True)
        os.unlink(ruta)
        return r.returncode == 0


def con_cara(ruta_db, salida, preguntas=None):
    """Una conversacion de verdad, con la cara al dia despues de cada turno."""
    sys.path.insert(0, PRODUCTO)
    try:
        import lore as L
        import cara as C
    except ImportError:
        L = C = None

    print("── residente enganchado a la cara " + "─" * 33)
    t0 = time.perf_counter()
    cerebro, voz = Cerebro(), Voz()
    cara = Cara(ruta_db, salida)
    arranque = time.perf_counter() - t0
    print(f"  arranque (una vez): {arranque:.2f} s")

    guion = preguntas or []
    turnos, usadas, callado = [], set(), 0
    for pregunta in guion:
        t0 = time.perf_counter()
        respuesta = cerebro.pregunta(pregunta)
        t_modelo = time.perf_counter() - t0

        t1 = time.perf_counter()
        crudo = None
        if voz.hay:
            # Lo que se OYE se limpia; lo que se MUESTRA no se toca. Las dos
            # espacios de fin de linea del modelo son un salto de pagina, y
            # dichos en voz alta se convierten en un silencio a mitad de idea.
            dicho = C.para_voz(respuesta) if C else respuesta
            crudo = subprocess.run(
                [PIPER, "-m", VOZ, "-s", voz.hablante, "--output-raw"],
                input=dicho.encode("utf-8"), capture_output=True).stdout
        t_voz = time.perf_counter() - t1

        elegida = L.elegir(pregunta + " " + respuesta, "es",
                           usadas=usadas) if L else None
        pieza = None
        if elegida:
            usadas.add(elegida[0])       # no se repite pieza en la misma charla
            pieza = elegida[1]
        else:
            # El lector callado se CUENTA. Quedarse en silencio es la conducta
            # correcta cuando no hay pieza que encaje, pero un silencio que
            # nadie cuenta no se distingue de una cobertura que no existe.
            callado += 1
        cara.anota(pregunta, respuesta, crudo, pieza)

        t2 = time.perf_counter()
        cara.refresca()
        t_cara = time.perf_counter() - t2

        total = t_modelo + t_voz + t_cara
        turnos.append((t_modelo, t_voz, t_cara, total))
        print(f"  · {pregunta[:38]!r}")
        print(f"    modelo {t_modelo:.2f}s · voz {t_voz:.2f}s · "
              f"cara {t_cara:.2f}s · TOTAL {total:.2f}s"
              + ("  (+lore)" if pieza else ""))
    cerebro.cierra()
    if turnos:
        med = [sum(x[i] for x in turnos) / len(turnos) for i in range(4)]
        print(f"\n  MEDIA · modelo {med[0]:.2f}s · voz {med[1]:.2f}s · "
              f"cara {med[2]:.2f}s · TURNO COMPLETO {med[3]:.2f}s")
    if guion:
        print(f"  lector callado: {callado} de {len(guion)} turnos "
              f"(sin pieza que encajara, que es lo correcto cuando no la hay)")
        _anota_lector(len(guion), callado)
    print(f"  cara al dia en: {salida}")
    return 0


def _anota_lector(turnos, callado):
    """Una linea por conversacion en la telemetria. Sin esto, decidir si LORE
    cubre poco o mucho se haria de memoria, que es como no decidirlo."""
    import json
    ruta = os.path.expanduser("~/p0x/mente/telemetria/lector.jsonl")
    if not os.path.isdir(os.path.dirname(ruta)):
        return
    try:
        with open(ruta, "a", encoding="utf-8") as fh:
            fh.write(json.dumps({"turnos": turnos, "callado": callado,
                                 "con_pieza": turnos - callado},
                                ensure_ascii=False) + "\n")
    except OSError:
        pass


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
    ap.add_argument("--cara", metavar="HTML",
                    help="keep a face up to date after every real turn")
    ap.add_argument("--db", default=os.path.expanduser("~/.aurelius/memory.db"))
    ap.add_argument("--guion", nargs="*", metavar="PREGUNTA",
                    help="questions to run without a keyboard (for measuring)")
    a = ap.parse_args()
    if a.medir:
        return medir()
    if a.cara:
        return con_cara(a.db, a.cara, a.guion)
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
