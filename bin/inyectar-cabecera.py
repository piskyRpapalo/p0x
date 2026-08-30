#!/usr/bin/env python3
"""Pone favicon y Open Graph en todas las páginas del Ágora. Idempotente.

Hacerlo a mano en diecisiete ficheros y tres idiomas es exactamente la tarea
que se hace mal la segunda vez: se olvida una página, o se pega una `og:url`
copiada de otra. Este guion lo deriva de la ruta y se puede correr cien veces.

Por defecto NO escribe: enseña qué tocaría. `--si` aplica. Es IronClaw en la
línea de comandos -- el silicio propone, el carbono firma.

    python3 ~/p0x/bin/inyectar-cabecera.py          # dry-run
    python3 ~/p0x/bin/inyectar-cabecera.py --si     # aplica
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

RAIZ = Path.home() / "preceptoros-web" / "public"
ORIGEN = "https://preceptoros.org"

FAVICON = '<link rel="icon" type="image/svg+xml" href="/assets/favicon.svg">'

# Solo las páginas que alguien comparte llevan tarjeta social. Ponerla en las
# diecisiete engordaría ficheros que ya rozan los 10 KB sin que nadie llegue a
# verla: nadie pega en un chat el enlace de una guía de instalación.
CON_TARJETA = {"index.html", "playground.html"}

LEMAS = {
    "es": ("PreceptorOS · Tu IA, tu memoria, tu soberanía",
           "La aduana entre tú y la nube. Memoria persistente en tu máquina, "
           "contexto saneado antes de salir. Sin cuentas, sin telemetría, sin nube obligatoria."),
    "en": ("PreceptorOS · Your AI, your memory, your sovereignty",
           "The customs house between you and the cloud. Persistent memory on your "
           "machine, context sanitised before it leaves. No accounts, no telemetry, no cloud."),
    "fr": ("PreceptorOS · Ton IA, ta mémoire, ta souveraineté",
           "La douane entre toi et le nuage. Mémoire persistante sur ta machine, "
           "contexte assaini avant de sortir. Sans comptes, sans télémétrie, sans nuage."),
}
LEMAS_PLAYGROUND = {
    "es": ("Probador de privacidad · PreceptorOS",
           "Pega tu contexto y mira qué sale antes de dárselo a una IA de la nube. "
           "En tu navegador, sin instalar nada, con los huecos declarados."),
    "en": ("Privacy Playground · PreceptorOS",
           "Paste your context and see what comes out before you hand it to a cloud AI. "
           "In your browser, nothing to install, with the gaps declared."),
    "fr": ("Testeur de confidentialité · PreceptorOS",
           "Colle ton contexte et vois ce qui sort avant de le donner à une IA du nuage. "
           "Dans ton navigateur, rien à installer, avec les trous déclarés."),
}


def idioma_de(p: Path) -> str:
    return p.parent.name if p.parent.name in LEMAS else "es"


def tarjeta(p: Path) -> str:
    idi = idioma_de(p)
    fuente = LEMAS_PLAYGROUND if p.name == "playground.html" else LEMAS
    titulo, desc = fuente.get(idi, fuente["es"])
    rel = p.relative_to(RAIZ).as_posix()
    # La canonica de un indice es su DIRECTORIO, no el fichero: /es/ y no
    # /es/index.html. Publicar las dos formas parte las señales de compartido
    # entre dos URLs que son la misma pagina.
    if rel.endswith("index.html"):
        rel = rel[:-len("index.html")]
    url = f"{ORIGEN}/{rel}"
    return "\n".join([
        f'<meta property="og:title" content="{titulo}">',
        f'<meta property="og:description" content="{desc}">',
        f'<meta property="og:image" content="{ORIGEN}/assets/preceptor-og.png">',
        f'<meta property="og:url" content="{url}">',
        '<meta property="og:type" content="website">',
        '<meta name="twitter:card" content="summary_large_image">',
    ])


def procesar(p: Path, aplicar: bool):
    t = p.read_text(encoding="utf-8")
    original = t
    hechos = []

    if 'rel="icon"' not in t:
        # Va justo tras el <title>: es donde lo busca cualquiera que abra el
        # fichero, y donde no estorba a las metas que ya existen.
        m = re.search(r"</title>\n?", t)
        if m:
            t = t[:m.end()] + FAVICON + "\n" + t[m.end():]
            hechos.append("favicon")

    if p.name in CON_TARJETA and "og:title" in t:
        arreglado = re.sub(r'(og:url" content="[^"]*?)index\.html(")', r"\1\2", t)
        if arreglado != t:
            t = arreglado
            hechos.append("og:url canónica")

    if p.name in CON_TARJETA and "og:title" not in t:
        ancla = re.search(r'<link rel="icon"[^>]*>\n', t) or re.search(r"</title>\n?", t)
        if ancla:
            t = t[:ancla.end()] + tarjeta(p) + "\n" + t[ancla.end():]
            hechos.append("open graph")

    if t == original:
        return None
    if aplicar:
        p.write_text(t, encoding="utf-8")
    return hechos, len(original), len(t)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--si", action="store_true", help="aplica (por defecto: dry-run)")
    a = ap.parse_args(argv)

    TOPE = 10 * 1024
    tocados, avisos = 0, []
    for p in sorted(RAIZ.rglob("*.html")):
        r = procesar(p, a.si)
        if not r:
            continue
        hechos, antes, despues = r
        tocados += 1
        marca = " ⚠️ PASA DE 10 KB" if despues >= TOPE else ""
        if despues >= TOPE:
            avisos.append(p)
        print(f"  {'✓' if a.si else '·'} {p.relative_to(RAIZ)} "
              f"[{', '.join(hechos)}] {antes} → {despues} B{marca}")

    print(f"\n{tocados} fichero(s) {'modificados' if a.si else 'a modificar'}"
          f"{' · sin cambios pendientes' if not tocados else ''}")
    if avisos:
        # El tope no se rompe en silencio. Si algo se pasa, se dice aquí y no
        # se descubre en el gate tres commits después.
        print("🔴 rompen el tope de 10 KB del Ágora:", file=sys.stderr)
        for p in avisos:
            print(f"   {p.relative_to(RAIZ)}", file=sys.stderr)
        return 1
    if not a.si and tocados:
        print("(dry-run · vuelve a llamarlo con --si para aplicar)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
