#!/usr/bin/env python3
"""Convierte `estado.json` en el Markdown que lee una sesion nueva.

No mide nada. Esa es toda la gracia: antes habia DOS codigos midiendo lo mismo
-- el shell de volcado y quien mirase el rack a mano -- y ya divergian sin que
nadie lo notara (el mismo snapshot llegó a decir 8 modelos en una seccion y 7
doce lineas mas abajo, porque una parte filtraba por nombre y la otra no).

Una medicion, dos formatos. Si el Markdown y el JSON discrepan, es un bug de
este fichero y de nadie mas.
"""
from __future__ import annotations

import json
import sys
import time
from pathlib import Path

RAIZ = Path(__file__).resolve().parent
ENTRADA = RAIZ / "estado.json"
SALIDA = RAIZ / "ALEJANDRIA_ESTADO_ACTUAL.md"

MARCA = {"OK": "✅", "RED": "🔴", "NO_DATA": "⬜"}


def edad(segundos):
    if segundos is None:
        return "NO_DATA"
    s = int(segundos)
    if s < 90:
        return f"{s} s"
    if s < 5400:
        return f"{s // 60} min"
    if s < 172800:
        return f"{s // 3600} h"
    return f"{s // 86400} d"


def linea(clave, bloque):
    est = bloque.get("estado", "?")
    return f"| {MARCA.get(est, '❔')} `{est}` | **{clave}** |"


def render(d):
    c = d["componentes"]
    frescura = time.time() - d.get("epoch", 0)
    out = []
    a = out.append

    a("# 🏛️ ESTADO DEL SISTEMA · PROYECTO ALEJANDRÍA")
    a("")
    a(f"**Generado:** {d['generado']} · **modo:** `{d['modo']}` · "
      f"**antigüedad al leer esto:** {edad(frescura)}")
    a("")
    if frescura > 86400:
        a("> 🔴 **STALE · contexto perdido.** Este fichero tiene más de 24 h. "
          "No lo uses como verdad: ejecuta `~/p0x/Alejandria/verificar_sesion.sh` primero.")
        a("")
    elif frescura > 3600:
        a("> 🟠 **STALE.** Más de una hora. Ejecuta "
          "`~/p0x/Alejandria/verificar_sesion.sh` antes de decidir nada.")
        a("")

    rojos = [k for k, v in c.items() if isinstance(v, dict) and v.get("estado") == "RED"]
    huecos = [k for k, v in c.items() if isinstance(v, dict) and v.get("estado") == "NO_DATA"]
    a(f"**Resumen:** {len(rojos)} en rojo · {len(huecos)} NO_DATA · "
      f"el resto en verde.")
    if rojos:
        a("")
        for k in rojos:
            a(f"- 🔴 **{k}** — {c[k].get('causa', 'sin causa declarada')}")
    if huecos:
        a("")
        for k in huecos:
            a(f"- ⬜ **{k}** — {c[k].get('causa', '?')} · *remedio:* "
              f"{c[k].get('remedio', '?')}")
    a("")
    a("---")
    a("")

    # --- servicios ---
    a("## 1 · Servicios")
    a("")
    o = c.get("ollama", {})
    a(f"- {MARCA.get(o.get('estado'), '❔')} **Ollama** — "
      + (f"{o.get('modelos')} modelos · {o.get('latencia_ms')} ms · "
         f"backend {o.get('backend')} · residentes: "
         f"{', '.join(o.get('residentes') or []) or 'ninguno'}"
         if o.get("estado") == "OK" else o.get("causa", "?")))
    if o.get("estado") == "OK":
        for n in o.get("nombres", []):
            a(f"  - `{n}`")
    g = c.get("api_guia", {})
    a(f"- {MARCA.get(g.get('estado'), '❔')} **API Guía** — "
      + (f"`:9001` vivo · unidad de **{g.get('gestor')}** ({g.get('unidad')}) · "
         f"alcanzada por {g.get('alcanzado_en')}"
         if g.get("estado") == "OK" else g.get("causa", "?")))
    a("  - *Nota: es unidad de SISTEMA. Preguntarle a `systemctl --user` "
      "devuelve «no existe», que es cierto y no significa nada.*")
    l = c.get("lora_v7", {})
    a(f"- {MARCA.get(l.get('estado'), '❔')} **LoRA v7** — "
      + (", ".join(f"`{x}`" for x in l.get("adaptadores", []))
         if l.get("estado") == "OK" else l.get("causa", "?")))
    a("")

    # --- enjambre ---
    a("## 2 · Enjambre")
    a("")
    a("*Son unidades `Type=oneshot`: **«inactive» entre disparos es el estado "
      "sano**. Lo que informa es `Result` y la próxima cita, no `is-active`.*")
    a("")
    a("| | Agente | Cadencia | Última | Próxima |")
    a("|---|---|---|---|---|")
    for n, b in (c.get("enjambre") or {}).items():
        a(f"| {MARCA.get(b.get('estado'), '❔')} | **{n}** | {b.get('cadencia', '?')} "
          f"| {b.get('ultima', '?')} | {b.get('proxima', '?')} |")
    a("")

    # --- puertos ---
    p = c.get("puertos", {})
    a("## 3 · Puertos")
    a("")
    if p.get("estado") == "OK":
        a(f"{p.get('total')} a la escucha · **{p.get('expuestos')} fuera de loopback**.")
        a("")
        a("| Dirección | Alcance | Proceso |")
        a("|---|---|---|")
        for f in p.get("lista", []):
            alcance = "🌐 **expuesto**" if f["expuesto"] else "🔒 loopback"
            a(f"| `{f['addr']}` | {alcance} | {f['proceso']} |")
    else:
        a(p.get("causa", "?"))
    a("")

    # --- memoria ---
    m = c.get("memoria", {})
    a("## 4 · Memoria")
    a("")
    if m.get("estado") == "OK":
        a(f"- `{m.get('ruta')}` · {m.get('tamano_b')} B · "
          f"índice FTS: {'sí' if m.get('fts') else 'NO'}")
        for t, n in m.get("tablas", []):
            a(f"  - `{t}`: **{n}**")
        eng = m.get("engramas", 0)
        turnos = dict(m.get("tablas", [])).get("turnos", 0)
        if eng <= 1 < turnos:
            a("")
            a(f"  > ⚠️ **{eng} engrama frente a {turnos} turnos.** La memoria no "
              "está vacía: está **sin destilar**. El uso existe y la memoria no "
              "lo captura. Causa sin investigar.")
    else:
        a(f"- {m.get('causa', '?')}")
    a("")

    # --- gates ---
    a("## 5 · Gates")
    a("")
    for clave, nombre in (("mvp_gate", "MVP (`preceptor`)"), ("web_gate", "Web (`preceptoros-web`)")):
        b = c.get(clave, {})
        est = b.get("estado", "?")
        detalle = ", ".join(f"{k}={v}" for k, v in b.items()
                            if k in ("pasa", "salta", "subtests"))
        sello = ""
        if b.get("arrastrado"):
            sello = f" · ⏳ *arrastrado de una corrida de hace {edad(b.get('edad_s'))}*"
        a(f"- {MARCA.get(est, '❔')} **{nombre}** — {detalle or b.get('causa', '?')}{sello}")
    a("")

    # --- resto ---
    a("## 6 · Rack y recursos")
    a("")
    t = c.get("tailscale", {})
    if t.get("estado") == "OK":
        a(f"- **Tailscale** — {t.get('online')}/{t.get('total')} en línea")
        a(f"  - online: {', '.join(t.get('nodos_online') or []) or '—'}")
        a(f"  - offline: {', '.join(t.get('nodos_offline') or []) or '—'}")
    dg = c.get("doogee", {})
    a(f"- {MARCA.get(dg.get('estado'), '❔')} **Doogee** — "
      + (f"`{dg.get('serial')}` ({dg.get('conexion')})"
         if dg.get("estado") == "OK" else dg.get("causa", "?")))
    ds = c.get("disco", {})
    a(f"- {MARCA.get(ds.get('estado'), '❔')} **Disco** — "
      f"{ds.get('libre_gb')} GB libres de {ds.get('total_gb')} GB")
    a("")
    a("---")
    a("")
    a("*Generado por `informe.py` desde `estado.json`. No mide nada: si esto y "
      "el JSON discrepan, el bug está aquí.*")
    a("*Para refrescar: `~/p0x/Alejandria/verificar_sesion.sh`*")
    return "\n".join(out) + "\n"


def main(argv=None):
    entrada = Path(argv[0]) if argv else ENTRADA
    if not entrada.exists():
        sys.stderr.write(f"NO_DATA: no existe {entrada}. "
                         "Remedio: python3 recolector.py --completo\n")
        return 1
    d = json.loads(entrada.read_text(encoding="utf-8"))
    SALIDA.write_text(render(d), encoding="utf-8")
    print(f"informe escrito en {SALIDA}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
