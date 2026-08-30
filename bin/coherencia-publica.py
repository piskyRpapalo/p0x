#!/usr/bin/env python3
"""Comprueba que lo que la web PRESUME es lo que los gates MIDEN.

EL HALLAZGO QUE LO ORIGINA
--------------------------
El 2026-08-30, `public/{es,en,fr}/index.html` anunciaban «526 pruebas en verde
en la app». El gate del MVP producia 429 passed + 2 skipped + 167 subtests.
**Ningun comando daba 526.** Estaba en produccion, en tres idiomas, y llevaba
ahi el tiempo que llevara.

No es una errata: es una reclamacion publica no reproducible, que es justo lo
que la doctrina de honest sensors existe para impedir. Y no se arregla
escribiendo el numero bueno a mano, porque a mano vuelve a derivar en cuanto
alguien añada un test. Se arregla convirtiendo la cifra en una MEDICION.

COMO
----
Este guion corre los dos gates, escribe lo medido en `counters.json` -- con el
mismo esquema y la misma disciplina que `contadores.py` -- y actualiza la linea
de credenciales de las tres portadas. Despues, `test_web.py` comprueba que el
HTML y `counters.json` coinciden: rapido, sin red y sin depender del otro repo.

Reparto deliberado: la MEDICION cruza repos y vive aqui; la COMPROBACION es
local al Agora y vive en su gate. Un gate que necesitase el MVP para pasar
dejaria de poder correrse solo.

    python3 ~/p0x/bin/coherencia-publica.py         # comprueba (dry-run)
    python3 ~/p0x/bin/coherencia-publica.py --si    # mide y actualiza
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

CASA = Path.home()
MVP = CASA / "p0x" / "preceptor"
WEB = CASA / "preceptoros-web"
PUBLICO = WEB / "public"
CONTADORES = PUBLICO / "counters.json"

# La linea de credenciales. Los dos primeros <b>N</b> son las dos cifras de
# pruebas; el tercero y el cuarto son «cero» y «10 KB», que no son numeros y
# por eso el patron exige digitos.
PROOF = re.compile(r'(<p class="proof">.*?</p>)', re.S)
CIFRA = re.compile(r"<b>(\d[\d.  ]*)</b>")


def _gate(cwd, cmd, patron, nombre):
    try:
        p = subprocess.run(cmd, cwd=str(cwd), capture_output=True, text=True,
                           timeout=600)
    except (OSError, subprocess.TimeoutExpired) as e:
        return None, f"{nombre}: {type(e).__name__}"
    salida = (p.stdout or "") + (p.stderr or "")
    m = re.search(patron, salida)
    if not m:
        return None, f"{nombre}: no se pudo leer el resumen del gate"
    if p.returncode != 0:
        return None, f"{nombre}: el gate termino en ROJO, no se publica su cifra"
    return int(m.group(1)), None


def medir():
    """Los dos gates. Un gate en rojo NO publica cifra: sale NO_DATA.

    Publicar «429 en verde» cuando el gate esta en rojo seria exactamente el
    tipo de cifra que este guion existe para erradicar.
    """
    app, e1 = _gate(MVP, ["python3", "-m", "pytest", "--tb=no", "-q"],
                    r"(\d+) passed", "gate del MVP")
    web, e2 = _gate(WEB, ["python3", "test_web.py"], r"Ran (\d+) tests?",
                    "gate de la web")
    return {"app": (app, e1), "web": (web, e2)}


def _metrica(clave, valor, causa, como):
    if valor is None:
        return {"clave": clave, "estado": "NO_DATA", "valor": None,
                "unidad": "pruebas", "causa": causa}
    return {"clave": clave, "estado": "MEDIDO", "valor": valor,
            "unidad": "pruebas", "como": como}


def escribir_contadores(medidas):
    d = json.loads(CONTADORES.read_text(encoding="utf-8"))
    nuevas = [
        _metrica("pruebas_app", medidas["app"][0], medidas["app"][1],
                 "python3 -m pytest -q en el repo del MVP, cifra 'N passed'"),
        _metrica("pruebas_web", medidas["web"][0], medidas["web"][1],
                 "python3 test_web.py en este repo, cifra 'Ran N tests'"),
    ]
    por_clave = {m["clave"]: m for m in d["metricas"]}
    for m in nuevas:
        por_clave[m["clave"]] = m
    d["metricas"] = list(por_clave.values())
    d["ultima_lectura"] = datetime.now(timezone.utc).isoformat(timespec="seconds")
    CONTADORES.write_text(json.dumps(d, indent=2, ensure_ascii=False) + "\n",
                          encoding="utf-8")


def portadas():
    """Las portadas de idioma. La raiz queda fuera: es un selector de idioma,
    ruteo sin contenido, y no lleva linea de credenciales. Mismo criterio que
    ya usan test_web.py y contadores.py."""
    return sorted(p for p in PUBLICO.rglob("index.html") if p.parent != PUBLICO)


def revisar(app, web, aplicar):
    """Compara y, si se pide, corrige. Devuelve la lista de divergencias.

    La sustitucion es POSICIONAL y no por valor: se reemplaza la primera cifra
    y la segunda de la linea de credenciales, sean las que sean. Buscar «526»
    y cambiarlo por «429» funcionaria hoy y fallaria en silencio el dia que la
    cifra publicada sea otra -- que es justo el dia que importa.
    """
    divergencias = []
    for p in portadas():
        t = p.read_text(encoding="utf-8")
        m = PROOF.search(t)
        if not m:
            divergencias.append((p, "sin línea de credenciales"))
            continue
        bloque = m.group(1)
        pos = [(mm.start(), mm.end(), int(re.sub(r"\D", "", mm.group(1))))
               for mm in CIFRA.finditer(bloque)]
        if len(pos) < 2:
            divergencias.append((p, "la línea de credenciales no tiene dos cifras"))
            continue

        quiero = [app, web]
        etiqueta = ["app", "web"]
        nuevo_bloque, cursor, trozos = None, 0, []
        cambiado = False
        for i, (ini, fin, actual) in enumerate(pos[:2]):
            deseado = quiero[i]
            trozos.append(bloque[cursor:ini])
            if deseado is None or deseado == actual:
                trozos.append(bloque[ini:fin])
            else:
                divergencias.append(
                    (p, f"{etiqueta[i]}: publica {actual}, el gate mide {deseado}"))
                trozos.append(f"<b>{deseado}</b>")
                cambiado = True
            cursor = fin
        trozos.append(bloque[cursor:])
        nuevo_bloque = "".join(trozos)

        if aplicar and cambiado:
            p.write_text(t.replace(bloque, nuevo_bloque), encoding="utf-8")
    return divergencias


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--si", action="store_true",
                    help="mide y actualiza (por defecto: solo comprueba)")
    a = ap.parse_args(argv)

    medidas = medir()
    app, e_app = medidas["app"]
    web, e_web = medidas["web"]
    print(f"  gate MVP  → {app if app is not None else '⬜ NO_DATA: ' + str(e_app)}")
    print(f"  gate web  → {web if web is not None else '⬜ NO_DATA: ' + str(e_web)}")

    div = revisar(app, web, a.si)
    if not div:
        print("  ✅ la web publica exactamente lo que los gates miden")
        if a.si:
            escribir_contadores(medidas)
            print(f"  counters.json actualizado")
        return 0

    for p, motivo in div:
        print(f"  {'✓ corregido' if a.si else '🔴'} {p.relative_to(PUBLICO)} — {motivo}")
    if a.si:
        escribir_contadores(medidas)
        print("  counters.json actualizado")
        return 0
    print("\n  (comprobación · vuelve a llamarlo con --si para corregir)",
          file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
