#!/usr/bin/env python3
"""El Auditor, en su forma mas barata: determinista y sin modelo.

POR QUE EXISTE, Y SE MIDIO HOY
------------------------------
El 2026-08-31, `qwen2.5:1.5b` leyo un JSON que decia con todas sus letras que
el gemelo NO es concluyente, y escribio en la ficha «Gemelo declarado:
F1s202-EU, Chip BK7231N» como si lo fuera. En la misma ficha propuso
«flashear la nueva version del software» -- que es literalmente la prohibicion
numero dos del JSON que acababa de leer.

Eso no es un modelo malo: es el modo de fallo normal de un modelo pequeno al
que se le pide fidelidad a un documento largo. Lo que estaba mal era el
proceso: no habia nada entre el modelo y la firma.

DUAL_MODEL_AUDITOR.md dice que el que propone nunca es el que aprueba. Este es
el escalon mas barato de esa doctrina: no hace falta un segundo modelo para
cazar una contradiccion literal contra el JSON de entrada. Un `in` basta, y un
`in` no alucina.

Salida: 0 si la ficha se puede firmar, 1 si no. El JSON del veredicto va a
stdout para que quede en el registro tambien cuando bloquea -- un bloqueo sin
causa legible es un fallo mudo, y la metrica de exito de esa doctrina lo
prohibe expresamente.
"""
from __future__ import annotations
import json, pathlib, re, sys

AQUI = pathlib.Path(__file__).resolve().parent


def audita(ficha: str, d: dict):
    fallos, texto = [], ficha.lower()

    # 1 · las prohibiciones del propio JSON, buscadas en la ficha.
    #
    # CICATRIZ DEL PROPIO AUDITOR (2026-08-31): la primera version decia
    # «si aparece "flashear" Y NO aparece "no flashear"». Dio VERDE sobre una
    # ficha que proponia flashear -- porque esa misma ficha copiaba la lista de
    # prohibiciones, y ese "no flashear" desactivaba la regla. Un filtro que se
    # apaga solo cuando el texto cita la prohibicion es exactamente el fallo
    # silencioso que S0 existe para sospechar.
    #
    # La cura: se BORRAN las menciones prohibitivas y se busca en lo que queda.
    # Lo que sobrevive a ese borrado es una propuesta de flasheo, no una cita.
    sin_citas = re.sub(r"no\s+(se\s+)?(debe\s+|hay\s+que\s+)?flashea\w*", "", texto)
    sin_citas = re.sub(r"flasheo\s+prohibido", "", sin_citas)
    if re.search(r"\bflashea\w*\b", sin_citas):
        fallos.append({
            "regla": "prohibicion_flashear",
            "detalle": "la ficha propone flashear fuera de toda cita a la "
                       "prohibicion, y el JSON lo prohibe en "
                       "prohibiciones_vigentes"})

    # 2 · el gemelo: si el JSON dice que NO es concluyente, la ficha no puede
    #     presentarlo como prueba del chip.
    g = d.get("gemelo", {})
    if not g.get("concluyente", True):
        dice_aviso = any(p in texto for p in
                         ("no es concluyente", "no concluyente", "no prueba",
                          "dos chips", "2 chips", "no es prueba"))
        if not dice_aviso:
            fallos.append({
                "regla": "gemelo_no_concluyente",
                "detalle": "el JSON declara gemelo.concluyente=false y la ficha "
                           "no lo advierte: la presenta como confirmacion del chip"})

    # 3 · nada de afirmar una liberacion que no ocurrio
    if re.search(r"(ha sido|fue|quedo)\s+liberad", texto):
        fallos.append({
            "regla": "liberacion_inventada",
            "detalle": "la ficha afirma que el aparato fue liberado; el JSON "
                       "dice compatibilidad_cloudcutter=false"})

    # 4 · la barrera dominante es administrativa y tiene que aparecer
    if "administrativ" not in texto:
        fallos.append({
            "regla": "barrera_omitida",
            "detalle": "la ficha no menciona la barrera administrativa, que es "
                       "la causa dominante segun el JSON"})
    return fallos


def main():
    d = json.loads((AQUI / "m10-inventario.json").read_text(encoding="utf-8"))
    fp = AQUI / "ficha-autopsia.md"
    ficha = fp.read_text(encoding="utf-8") if fp.exists() else ""
    if not ficha.strip():
        fallos = [{"regla": "ficha_vacia", "detalle": "no hay ficha que auditar"}]
    else:
        fallos = audita(ficha, d)
    v = {"auditor": "determinista", "version": 1,
         "ficha_bytes": len(ficha.encode()),
         "aprobada": not fallos, "fallos": fallos,
         "mensaje": ("la ficha puede firmarse" if not fallos else
                     "BLOQUEADA: " + "; ".join(f["regla"] for f in fallos))}
    (AQUI / "veredicto.json").write_text(
        json.dumps(v, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(json.dumps(v, ensure_ascii=False, indent=1))
    return 0 if not fallos else 1


if __name__ == "__main__":
    raise SystemExit(main())
