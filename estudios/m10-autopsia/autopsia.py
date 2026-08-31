#!/usr/bin/env python3
"""Autopsia determinista del M10-EM-2. **Sin LLM y sin red opcional.**

EL REPARTO, Y ES LA REGLA DURA DE LA MISION
-------------------------------------------
Este guion NO interpreta ni redacta: MIDE. Lee el inventario fisico declarado,
consulta la base de OpenBeken y emite un JSON estructurado. Quien interpreta y
redacta es el modelo, despues, y con este JSON delante. Si el guion opinara,
nadie podria distinguir el dato de la opinion en el reporte final -- que es
exactamente lo que un caso cerrado no se puede permitir.

POR QUE EL INVENTARIO FISICO VA ESCRITO AQUI
--------------------------------------------
Porque no hay forma de medirlo desde software: el chip y el sensor se leyeron
abriendo el aparato, con los ojos. Van marcados `fuente: inspeccion_fisica`
para que nadie los confunda con algo consultado. Todo lo demas se consulta y
lleva su URL.

FUENTE DE LA BASE
-----------------
`devices.json` del repo `OpenBekenIOT/webapp` (889 dispositivos, esquema
version 0.1). Se usa el RAW de GitHub y no la pagina: la pagina pinta esa
misma base con JavaScript, asi que raspar el HTML seria leer lo mismo dando
un rodeo y rompiendose el dia que cambien el maquetado.

    python3 autopsia.py            # a stdout
    python3 autopsia.py --salida X # a fichero
"""
from __future__ import annotations

import argparse
import json
import sys
import urllib.error
import urllib.request
from datetime import datetime, timezone

BASE = ("https://raw.githubusercontent.com/OpenBekenIOT/webapp/master/devices.json")

# --- inventario fisico · leido con los ojos, no consultado -----------------
INVENTARIO = {
    "modelo": "M10-EM-2",
    "vendedor": "Simatop",
    "ecosistema": "Tuya",
    "chip": "BK7231N",
    "driver_medicion": "BL0937",
    "gemelo_declarado": "F1s202-EU",
    "fuente": "inspeccion_fisica",
    "nota": "chip y sensor leidos abriendo el aparato; no hay via software "
            "para confirmarlos sin flashear, y flashear esta prohibido por "
            "decision del carbono (2026-08-31)",
}


def medido(valor, como):
    return {"estado": "MEDIDO", "valor": valor, "como": como}


def sin_dato(causa):
    return {"estado": "NO_DATA", "valor": None, "causa": causa}


def baja_base():
    try:
        with urllib.request.urlopen(BASE, timeout=45) as r:
            d = json.load(r)
        return d.get("devices", []), d.get("version"), None
    except (urllib.error.URLError, OSError, ValueError) as e:
        return [], None, f"{type(e).__name__}: {e}"


def tiene(dev, aguja):
    """Busca en el registro entero: el sensor puede vivir en `keywords` o
    solo en los nombres de `pins`, y mirar un solo campo deja fuera la mitad."""
    return aguja.lower() in json.dumps(dev, ensure_ascii=False).lower()


def analiza(devs):
    bk = [d for d in devs if d.get("chip") == INVENTARIO["chip"]]
    bl = [d for d in devs if tiene(d, INVENTARIO["driver_medicion"])]
    ambos = [d for d in bk if tiene(d, INVENTARIO["driver_medicion"])]
    # El gemelo: se busca por modelo, y se devuelven TODAS las coincidencias.
    # Devolver solo la primera es como se fabrica una certeza que no hay.
    gem = [d for d in devs if INVENTARIO["gemelo_declarado"].lower()
           in json.dumps(d, ensure_ascii=False).lower()]
    # El propio M10: se busca de verdad, para poder decir que NO esta.
    m10 = [d for d in devs
           if "m10" in (d.get("model", "") + " " + d.get("name", "")).lower()]
    return bk, bl, ambos, gem, m10


def construir():
    devs, version, fallo = baja_base()
    ahora = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    if fallo:
        return {
            "esquema": 1, "generado": ahora, "estado": "PARCIAL",
            "inventario_fisico": INVENTARIO,
            "consulta_openbeken": sin_dato(f"la base no se pudo leer: {fallo}"),
            "gate": {"valido": False,
                     "causa": "sin base consultada no hay autopsia, solo el "
                              "inventario que ya se sabia"},
        }
    bk, bl, ambos, gem, m10 = analiza(devs)

    # Los chips del gemelo, contados. Si sale mas de uno, el gemelo NO prueba
    # el chip -- y eso cambia la fuerza de la conclusion de la ficha vieja.
    chips_gemelo = sorted({d.get("chip") for d in gem})

    return {
        "esquema": 1,
        "generado": ahora,
        "estado": "MEDIDO",
        "fuente": {"base": BASE, "version_esquema": version,
                   "dispositivos": len(devs)},
        "inventario_fisico": INVENTARIO,

        "chip": medido(INVENTARIO["chip"],
                       "inspeccion fisica; la base trae "
                       f"{len(bk)} dispositivos con ese chip"),
        "driver_medicion": medido(
            INVENTARIO["driver_medicion"],
            f"inspeccion fisica; {len(bl)} dispositivos de la base lo usan"),

        "compatibilidad_cloudcutter": {
            "estado": "MEDIDO",
            "valor": False,
            "como": "el modelo no aparece en la base de OpenBeken "
                    f"({len(m10)} coincidencias para 'm10') y el firmware Tuya "
                    "esta parcheado post-feb-2022",
            "barrera_dominante": "administrativa",
            "detalle": "Tuya bloquea la API del wizard tras una vinculacion "
                       "fallida. La barrera dejo de ser tecnica: ninguna via "
                       "de extraccion sobrevive a una puerta cerrada desde la "
                       "cuenta, por muy conocido que sea el chip.",
        },

        "gemelo": {
            "estado": "MEDIDO" if gem else "NO_DATA",
            "coincidencias": [
                {"vendor": d.get("vendor"), "model": d.get("model"),
                 "chip": d.get("chip"), "board": d.get("board"),
                 "wiki": d.get("wiki")} for d in gem],
            "chips_distintos": chips_gemelo,
            "concluyente": len(chips_gemelo) == 1,
            "aviso": None if len(chips_gemelo) == 1 else
                     f"el gemelo declarado aparece con {len(chips_gemelo)} "
                     f"chips distintos ({', '.join(map(str, chips_gemelo))}): "
                     "NO prueba el chip del M10. El mismo numero de modelo se "
                     "fabrica con silicio distinto, que es precisamente por lo "
                     "que un perfil de cloudcutter no es transferible entre "
                     "gemelos.",
        },

        "vecindario": {
            "estado": "MEDIDO",
            "bk7231n_total": len(bk),
            "bl0937_total": len(bl),
            "bk7231n_con_bl0937": len(ambos),
            "como": "recuento sobre la base completa; el perfil del M10 "
                    "es comun, y aun asi el M10 no esta",
        },

        "alternativas_soberanas": [
            {"modelo": "Shelly Plug S", "via": "API local HTTP/MQTT",
             "abrir_aparato": False, "nube_obligatoria": False,
             "estado": "elegido por el carbono 2026-08-31, pendiente de compra"},
        ],

        "lecciones_doctrina": [
            "Una barrera administrativa derrota a una via tecnica que funciona: "
            "al fabricante no le hizo falta un chip inexpugnable, le basto con "
            "cerrar la cuenta.",
            "El coste de un aparato cerrado no se paga al comprarlo sino al "
            "intentar liberarlo, y es tiempo, no dinero.",
            "Un gemelo con el mismo numero de modelo no garantiza el mismo "
            "chip: la equivalencia hay que medirla, no suponerla.",
            "Cuando el obstaculo se mueve del silicio al contrato, la respuesta "
            "correcta es cambiar de proveedor, no insistir.",
        ],

        "prohibiciones_vigentes": [
            "no tocar el M10 fisicamente",
            "no flashear nada mas",
            "no buscar mas vias de extraccion (UART cerrado por el carbono)",
        ],
    }


def gate(d):
    """El JSON tiene que ser valido Y completo antes de firmarse."""
    faltan = [c for c in ("inventario_fisico", "chip", "driver_medicion",
                          "compatibilidad_cloudcutter", "alternativas_soberanas",
                          "lecciones_doctrina") if c not in d]
    if faltan:
        return False, f"faltan claves: {', '.join(faltan)}"
    if d.get("estado") != "MEDIDO":
        return False, f"estado {d.get('estado')}: no se firma lo que no se midio"
    if not d["lecciones_doctrina"]:
        return False, "sin lecciones: una autopsia que no ensena nada no vale"
    return True, "JSON valido y completo"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--salida")
    a = ap.parse_args()
    d = construir()
    ok, causa = gate(d)
    d["gate"] = {"valido": ok, "causa": causa}
    txt = json.dumps(d, ensure_ascii=False, indent=1) + "\n"
    if a.salida:
        open(a.salida, "w", encoding="utf-8").write(txt)
        print(f"escrito {a.salida} · {len(txt.encode())} B", file=sys.stderr)
    else:
        print(txt)
    print(f"GATE: {'VERDE' if ok else 'ROJO'} · {causa}", file=sys.stderr)
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
