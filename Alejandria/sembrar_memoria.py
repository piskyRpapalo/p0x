#!/usr/bin/env python3
"""Siembra la memoria del nodo con engramas DERIVADOS de la medicion.

POR QUE NO SE ESCRIBEN A MANO
------------------------------
Un engrama escrito a mano es una frase que envejece: dice «Ollama escucha en tal
sitio» y el dia que cambie seguira diciendolo, con toda la autoridad de estar en
la memoria. Es la misma enfermedad que hizo que la Orden Maestra diera por
pendientes seis tareas ya hechas.

Asi que estos tres salen de `Alejandria/estado.json`, es decir, de lo que el
recolector MIDIO. Si el fichero no existe o esta rancio, no se inventa nada: se
declara NO_DATA y se para. Un engrama falso en la memoria es peor que un hueco,
porque el hueco se ve.

POR QUE VIVE EN Alejandria/ Y NO EN preceptor/
-----------------------------------------------
DESVIACION MINIMA ADITIVA DECLARADA. La orden lo situaba en el repo del
producto. Pero esto no es codigo de producto: es una herramienta de rack que
siembra ESTA maquina con datos de ESTE rack. Metida en `preceptor/` viajaria en
el paquete de cualquiera que instale PreceptorOS. Usa la API del producto
(`memory.escribir_engrama`), que es lo que importa, y vive donde vive el resto
del utillaje del nodo.

Dry-run por defecto; `--si` escribe. IronClaw en la linea de comandos.
"""
from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

RAIZ = Path(__file__).resolve().parent
ESTADO = RAIZ / "estado.json"
PRODUCTO = Path.home() / "p0x" / "preceptor"
RANCIO_S = 6 * 3600

sys.path.insert(0, str(PRODUCTO))
import casa as _casa      # noqa: E402
import memory as M        # noqa: E402


def _medida():
    if not ESTADO.exists():
        return None, (f"no existe {ESTADO}",
                      "python3 ~/p0x/Alejandria/recolector.py --completo")
    try:
        d = json.loads(ESTADO.read_text(encoding="utf-8"))
    except ValueError as e:
        return None, (f"estado.json ilegible: {e}",
                      "python3 ~/p0x/Alejandria/recolector.py --completo")
    edad = time.time() - d.get("epoch", 0)
    if edad > RANCIO_S:
        return None, (f"la medida tiene {int(edad // 3600)} h y sembraria datos viejos",
                      "~/p0x/Alejandria/verificar_sesion.sh")
    return d, None


def engramas_de(d):
    """Los tres del encargo, cada uno derivado de un componente medido.

    Si un componente no se pudo medir, ESE engrama no se siembra. Sembrar
    parcialmente es honesto; rellenar el hueco con una suposicion, no.
    """
    c = d["componentes"]
    fuera, huecos = [], []

    o = c.get("ollama", {})
    if o.get("estado") == "OK":
        fuera.append(dict(
            what=f"Ollama de este nodo escucha en {o['host']}, no en localhost",
            why="Trampa de configuracion: un `ollama list` pelado falla con "
                "«could not connect» y parece que el servicio esta caido. Esta vivo.",
            where_ref="soberano",
            learned=f"OLLAMA_HOST vive en ~/.config/environment.d/50-p0x.conf, "
                    f"no en .bashrc (que las shells no interactivas no leen). "
                    f"Medido: {o['modelos']} modelos, {o['latencia_ms']} ms, "
                    f"backend {o['backend']}."))
    else:
        huecos.append(f"ollama: {o.get('causa', 'sin medir')}")

    t = c.get("tailscale", {})
    if t.get("estado") == "OK":
        fuera.append(dict(
            what=f"La red superpuesta une el rack: {t['online']} de {t['total']} "
                 f"nodos en linea",
            why="Cero puertos crudos expuestos a internet. Es lo que permite que "
                "los nodos se hablen sin abrir nada al exterior.",
            where_ref="rack",
            learned="En linea: " + (", ".join(t.get("nodos_online") or []) or "ninguno") +
                    ". Fuera de linea: " + (", ".join(t.get("nodos_offline") or []) or "ninguno") +
                    ". Solo la-fragua tiene tunel hacia fuera."))
    else:
        huecos.append(f"tailscale: {t.get('causa', 'sin medir')}")

    l = c.get("lora_v7", {})
    if l.get("estado") == "OK":
        fuera.append(dict(
            what="LoRA v7 servido en Ollama: " + ", ".join(l["adaptadores"]),
            why="Son las dos lineas (A y B) entrenadas sobre sft_cot_v7.jsonl, "
                "109 lineas, en CPU.",
            where_ref="soberano",
            learned="La forja vive en ~/.venvs/aurelius-forja y su torch es +cpu: "
                    "no hay ruta GPU en este nodo. Entrenar v8 exige decidir si va "
                    "aqui en CPU o en la-torre, que tiene CUDA pero no peft ni trl."))
    else:
        huecos.append(f"lora_v7: {l.get('causa', 'sin medir')}")

    return fuera, huecos


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--si", action="store_true", help="escribe (por defecto: dry-run)")
    ap.add_argument("--db", help="ruta de la memoria (por defecto, la del producto)")
    a = ap.parse_args(argv)

    d, fallo = _medida()
    if d is None:
        print(f"⬜ NO_DATA · {fallo[0]}\n   Remedio: {fallo[1]}", file=sys.stderr)
        return 1

    nuevos, huecos = engramas_de(d)
    for h in huecos:
        print(f"  ⬜ no se siembra · {h}")
    if not nuevos:
        print("  🔴 ningún componente medido: no hay nada que sembrar", file=sys.stderr)
        return 1

    ruta = Path(a.db) if a.db else (_casa.raiz() / "memory.db")
    print(f"  memoria: {ruta}")
    if not ruta.exists():
        print(f"  🔴 no existe {ruta}", file=sys.stderr)
        return 1

    with M.abrir(str(ruta)) as c:
        # La migracion aditiva primero: una memoria nacida antes de D11 no
        # admite un recuerdo nuevo hasta que pasa por aqui.
        M.asegurar_tablas(c)
        ya = {f[0] for f in c.execute("select what from engrams")}
        pendientes = [e for e in nuevos if e["what"] not in ya]
        for e in nuevos:
            marca = "·" if e["what"] in ya else ("✓" if a.si else "+")
            estado = " (ya está)" if e["what"] in ya else ""
            print(f"  {marca} {e['what'][:76]}{estado}")
        if a.si:
            for e in pendientes:
                M.escribir_engrama(c, origen_dispositivo="soberano", **e)
            M.asegurar_busqueda(c)
        total = c.execute("select count(*) from engrams where status!='archivado'"
                          ).fetchone()[0]

    print(f"\n  {len(pendientes)} engrama(s) {'sembrados' if a.si else 'a sembrar'} "
          f"· {total} vivos en la memoria")
    if not a.si and pendientes:
        print("  (dry-run · vuelve a llamarlo con --si para escribir)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
