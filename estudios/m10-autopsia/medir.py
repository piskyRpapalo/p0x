#!/usr/bin/env python3
"""Corre el modelo sobre el JSON medido y CRONOMETRA el nodo mientras lo hace.

Por que un guion y no una tuberia de shell: los tokens/W solo salen si el
consumo se muestrea DURANTE la inferencia, no antes y despues. Un `cat` del
riel al terminar mide el reposo, no el trabajo -- y publicar eso como consumo
del estudio seria la clase de cifra que este rack lleva cuatro puertas cazando.

El riel se busca por NOMBRE (VDD_IN), jamas por indice: el numero de hwmon
cambia entre arranques y leer el indice de al lado da el consumo de otra cosa.
"""
from __future__ import annotations
import json, pathlib, re, subprocess, sys, threading, time

AQUI = pathlib.Path(__file__).resolve().parent
MODELO = sys.argv[1] if len(sys.argv) > 1 else "qwen3:8b"
INA = pathlib.Path("/sys/bus/i2c/drivers/ina3221/1-0040/hwmon/hwmon1")


def riel_vdd_in():
    for f in sorted(INA.glob("in*_label")):
        if f.read_text().strip() == "VDD_IN":
            n = re.sub(r"\D", "", f.name)
            return INA / f"curr{n}_input", INA / f"in{n}_input"
    return None, None


class Vatimetro(threading.Thread):
    """Muestrea VDD_IN cada 200 ms mientras dura la inferencia."""
    def __init__(self):
        super().__init__(daemon=True)
        self.c, self.v = riel_vdd_in()
        self.muestras, self.corriendo = [], True

    def run(self):
        while self.corriendo and self.c:
            try:
                mA = int(self.c.read_text()); mV = int(self.v.read_text())
                self.muestras.append(mA * mV / 1e6)      # vatios
            except OSError:
                pass
            time.sleep(0.2)

    def resumen(self):
        if not self.muestras:
            return {"estado": "NO_DATA",
                    "causa": "no se encontro el riel VDD_IN del INA3221"}
        m = self.muestras
        return {"estado": "MEDIDO", "unidad": "W", "muestras": len(m),
                "media": round(sum(m) / len(m), 2),
                "pico": round(max(m), 2), "minimo": round(min(m), 2),
                "como": "INA3221 riel VDD_IN, muestreado a 5 Hz durante la inferencia"}


def pedir(cuerpo):
    """Una peticion a /api/generate. Devuelve el JSON o {'_error': causa}."""
    import urllib.request, urllib.error
    req = urllib.request.Request(
        "http://127.0.0.1:11434/api/generate",
        data=json.dumps(cuerpo).encode(),
        headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=1800) as h:
            return json.load(h)
    except urllib.error.HTTPError as e:
        return {"_error": f"HTTP {e.code}: {e.read().decode()[:200]}"}
    except (urllib.error.URLError, OSError, ValueError) as e:
        return {"_error": f"{type(e).__name__}: {e}"}


PROMPT = """Eres el analista de una autopsia de hardware. Te doy un JSON MEDIDO por un
guion determinista. NO inventes ni un dato que no este en el JSON; si algo falta,
escribe NO_DATA con su causa. Responde en espanol, en Markdown, con estas tres partes:

## 1. Ficha tecnica de autopsia
## 2. Prompt reutilizable para futuros intentos de liberacion OTA
## 3. Entrada para LA_NECROPOLIS.md (causa, intento, reemplazo)

Presta atencion especial a `gemelo.aviso`: si el gemelo NO es concluyente, dilo en
la ficha, porque la ficha anterior lo daba por prueba del chip.

JSON:
"""


def main():
    datos = (AQUI / "m10-inventario.json").read_text(encoding="utf-8")
    d = json.loads(datos)
    if not d.get("gate", {}).get("valido"):
        print("PARA: el JSON de entrada no pasa su gate", file=sys.stderr)
        return 2

    # SE USA LA API HTTP, NO EL CLI. Medido hoy: `ollama run` con este prompt
    # largo y `--think false` se QUEDA COLGADO --proceso vivo, ningun modelo
    # cargado, 5 W de consumo-- en vez de devolver el 400 que devuelve con un
    # prompt corto. Y aunque no colgara, el CLI escupe las cifras entre
    # secuencias de escape de su spinner y habria que rascarlas con regex.
    # La API devuelve eval_count y eval_duration como numeros, que es lo que
    # una medicion necesita.
    #
    # `think` solo se manda si el modelo lo soporta: contra qwen3:4b-instruct
    # ollama responde 400 «does not support thinking». No es el no-op
    # silencioso del `-ngl 999`: aqui el flag no se ignora, revienta.
    cuerpo = {"model": MODELO, "prompt": PROMPT + datos, "stream": False}
    w = Vatimetro(); w.start()
    t0 = time.monotonic()
    r = pedir(cuerpo)
    pensamiento = "no se pidio pensamiento (la API no lo activa por defecto)"
    if r.get("_error") and "does not support thinking" in str(r.get("_error")):
        cuerpo.pop("think", None)
        r = pedir(cuerpo)
        pensamiento = "el modelo no piensa: no hay nada que apagar"
    dur = time.monotonic() - t0
    w.corriendo = False; w.join(timeout=2)

    if r.get("_error"):
        print("PARA: la API de ollama fallo: " + str(r["_error"]), file=sys.stderr)
        return 2
    est = {k: r.get(k) for k in
           ("eval_count", "eval_duration", "prompt_eval_count",
            "prompt_eval_duration", "total_duration", "load_duration")}

    pot = w.resumen()
    salida = (r.get("response") or "").strip()
    (AQUI / "ficha-autopsia.md").write_text(salida, encoding="utf-8")

    tok = int(est.get("eval_count") or 0)
    med = pot.get("media")
    informe = {
        "modelo": MODELO,
        "duracion_s": round(dur, 1),
        "tokens_generados": tok if tok else None,
        "tokens_por_segundo": (round(tok / (est["eval_duration"] / 1e9), 2)
                               if tok and est.get("eval_duration") else None),
        "potencia_W": pot,
        "tokens_por_vatio": (round(tok / dur / med, 2)
                             if tok and med else None),
        "energia_Wh": round(med * dur / 3600, 4) if med else None,
        "bytes_ficha": len(salida.encode()),
        "pensamiento": pensamiento,
        "crudo_ollama": est,
    }
    (AQUI / "medicion.json").write_text(
        json.dumps(informe, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(json.dumps(informe, ensure_ascii=False, indent=1))
    return 0 if salida else 1


if __name__ == "__main__":
    raise SystemExit(main())
