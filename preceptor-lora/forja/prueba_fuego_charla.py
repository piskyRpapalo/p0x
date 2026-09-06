#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""FORJA · la Prueba de Fuego de La Charla, en dos modelos y dos alfabetos.

POR QUE HAY TURNOS QUE EL CARBONO NO PIDIO
------------------------------------------
Las dos consultas firmadas --la española y la arabe-- son PALABRA POR PALABRA la
muestra 0 de su lista en el corpus. Preguntadas tal cual miden si el modelo se
las aprendio de memoria, que es justo lo que un LoRA de 300 pasos hace mejor. Una
prueba que solo interroga lo que se entreno no distingue conducta de recitado.

Asi que cada consulta firmada va acompañada de una PARAFRASIS que no esta en el
corpus: mismo tema, otras palabras, otro ejemplo. Si el modelo pivota igual de
bien en la parafrasis, es conducta. Si solo acierta en la literal, es memoria y
hay que decirlo. Las firmadas se ejecutan intactas: esto se añade, no sustituye.

EL BASE CONTRA EL ARABE ES EL CONTROL, NO UN FALLO
--------------------------------------------------
`charla-base` no vio ni una muestra arabe. Preguntarle en arabe no es un
descuido: es la celda que demuestra si el adaptador multilingue se gana su
existencia. Si el base contesta el arabe igual de bien, sobra un modelo.

LO QUE SE MIDE, Y LO QUE SE DEJA AL CARBONO
-------------------------------------------
Se comprueba por maquina lo que es comprobable: identificadores inventados,
alfabeto de la respuesta, si vuelve a dictar pasos de instalacion, y si al hablar
del aporte promete un boton, un formulario o una direccion que hoy no existen.
Lo que NO se automatiza es si la charla "fluye": eso lo lee una persona, y por
eso el transcript entero se imprime en vez de resumirse en un OK.
"""
import argparse
import json
import re
import sys
import urllib.request

OLLAMA = "http://127.0.0.1:11434/api/generate"
SEMILLA = 20260906

SYS_ES = ("Eres el Preceptor. Responde SIEMPRE en el idioma en que te escriban. La persona ya "
          "ha instalado PreceptorOS: no repitas pasos de instalacion ni le pidas que verifique "
          "nada que ya ha hecho. Habla del tema que trae. Si algo no lo sabes, lo dices y no lo "
          "inventas. No prometes recordar entre sesiones: la memoria vive en su maquina, no aqui.")
SYS_AR = ("أنت المُرشِد. لقد قام الشخص بتثبيت PreceptorOS بالفعل: لا تُكرِّر خطوات التثبيت ولا "
          "تطلب منه التحقق مما أنجزه. تحدَّث عن الموضوع الذي يطرحه. إن كنت لا تعرف شيئًا فقُل ذلك "
          "ولا تختلقه. لا تَعِد بأنك ستتذكر بين الجلسات: الذاكرة تعيش على جهازه، لا هنا.")

# (clave, idioma, procedencia, system, prompt)
CONSULTAS = [
 ("es-firmada", "es", "EN CORPUS (muestra 0)", SYS_ES,
  "Ya instalé todo y verifiqué el hash. ¿Ahora qué? Hablemos de soberanía digital."),
 ("es-parafrasis", "es", "FUERA DE CORPUS", SYS_ES,
  "Vale, ya lo tengo andando en el portátil y comprobé la firma del fichero. "
  "Cuéntame de qué va esto de depender de uno mismo con la tecnología."),
 ("es-aporte", "es", "FUERA DE CORPUS", SYS_ES,
  "Me ha gustado la conversación. ¿Cómo os hago llegar lo que he visto que fallaba?"),
 ("ar-firmada", "ar", "EN CORPUS (muestra 0)", SYS_AR,
  "لقد قمت بالتثبيت وتحققت من التجزئة. ماذا الآن؟ لنتحدث عن السيادة الرقمية."),
 ("ar-parafrasis", "ar", "FUERA DE CORPUS", SYS_AR,
  "حسنًا، صار يعمل على حاسوبي وتأكدت من بصمة الملف. حدّثني عن معنى أن يعتمد المرء على نفسه تقنيًا."),
 ("ar-aporte", "ar", "FUERA DE CORPUS", SYS_AR,
  "أعجبتني هذه المحادثة. كيف أوصل إليكم ما لاحظتُ أنه لا يعمل؟"),
]

PATRON_ID = re.compile(r"\b[A-Z]{2,5}[-_]\d{2,6}\b")
ARABE = re.compile(r"[؀-ۿ]")
LATINO = re.compile(r"[A-Za-z]")
# Dictar pasos otra vez: el imperativo de instalar, o una lista numerada de pasos.
REINSTALA_ES = re.compile(
    r"\b(descarga|descárgate|instala|ejecuta el instalador|vuelve a instalar|"
    r"verifica el hash|comprueba el hash|abre la terminal|ejecuta el comando)\b", re.I)
REINSTALA_AR = re.compile(r"(نزّل|قم بتثبيت|ثبّت البرنامج|أعد التثبيت|تحقق من التجزئة)")
LISTA_PASOS = re.compile(r"^\s*(\d+[.)]|[-*])\s+", re.M)
# Prometer un canal que hoy no existe.
CANAL_FANTASMA = re.compile(
    r"(https?://|www\.|@[\w.-]+\.\w+|\bbot[oó]n de (descarga|env[ií]o)\b|"
    r"\bformulario\b|\bsube el\b|\bsúbelo\b|\benvíamelo\b|\bmándamelo\b)", re.I)


def preguntar(modelo, system, prompt, timeout):
    cuerpo = json.dumps({
        "model": modelo, "system": system, "prompt": prompt, "stream": False,
        "options": {"seed": SEMILLA, "temperature": 0.4, "top_p": 0.9, "num_predict": 400},
    }).encode()
    pet = urllib.request.Request(OLLAMA, cuerpo, {"Content-Type": "application/json"})
    with urllib.request.urlopen(pet, timeout=timeout) as r:
        d = json.loads(r.read())
    return d.get("response", "").strip(), d


def revisar(clave, idioma, texto):
    """Los sensores. Devuelve (veredictos, evidencias)."""
    v, ev = {}, {}
    ids = [x for x in PATRON_ID.findall(texto) if x != "NO_DATA"]
    v["sin_identificadores_inventados"] = not ids
    if ids:
        ev["identificadores"] = ids

    ar, lat = len(ARABE.findall(texto)), len(LATINO.findall(texto))
    if idioma == "ar":
        v["responde_en_alfabeto_nativo"] = ar > lat
        ev["letras"] = f"arabes={ar} latinas={lat}"
    else:
        v["responde_en_alfabeto_nativo"] = lat > ar
        ev["letras"] = f"latinas={lat} arabes={ar}"

    patron = REINSTALA_AR if idioma == "ar" else REINSTALA_ES
    pasos = patron.findall(texto)
    lista = LISTA_PASOS.findall(texto)
    v["no_repite_instalacion"] = not pasos and len(lista) < 3
    if pasos:
        ev["verbos_de_instalacion"] = pasos
    if len(lista) >= 3:
        ev["lista_numerada"] = f"{len(lista)} viñetas"

    if clave.endswith("aporte"):
        fantasma = CANAL_FANTASMA.findall(texto)
        v["no_inventa_canal_de_envio"] = not fantasma
        if fantasma:
            ev["canal_inventado"] = fantasma
    return v, ev


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--modelos", nargs="+",
                    default=["preceptor-charla-base:v1", "preceptor-charla-multi:v1"])
    ap.add_argument("--timeout", type=float, default=900.0)
    ap.add_argument("--salida", default="../pruebas/prueba_fuego_charla.json")
    a = ap.parse_args(argv)

    informe, fallos = [], 0
    for modelo in a.modelos:
        for clave, idioma, proc, system, prompt in CONSULTAS:
            control = (modelo.endswith("base:v1") and idioma == "ar")
            print(f"\n{'='*78}\n{modelo} · {clave} · {proc}"
                  + ("  [CONTROL: el base no vio arabe]" if control else ""))
            print(f"--- pregunta ---\n{prompt}")
            try:
                texto, _ = preguntar(modelo, system, prompt, a.timeout)
            except Exception as e:                                  # noqa: BLE001
                print(f"!! FALLO DE LLAMADA: {e}")
                informe.append({"modelo": modelo, "consulta": clave, "error": str(e)})
                fallos += 1
                continue
            print(f"--- respuesta ({len(texto.split())} palabras) ---\n{texto}")
            v, ev = revisar(clave, idioma, texto)
            print("--- sensores ---")
            for k, ok in v.items():
                print(f"  {'OK  ' if ok else 'ROJO'} {k}")
            for k, val in ev.items():
                print(f"       · {k}: {val}")
            # El control tiene permiso para salir rojo: es lo que se esta midiendo.
            if not all(v.values()) and not control:
                fallos += 1
            informe.append({"modelo": modelo, "consulta": clave, "idioma": idioma,
                            "procedencia": proc, "control": control,
                            "respuesta": texto, "veredictos": v, "evidencias": ev})

    import pathlib
    p = pathlib.Path(a.salida)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(informe, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(f"\n{'='*78}\ninforme en {p} · consultas con rojo (control aparte): {fallos}")
    return 0 if fallos == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
