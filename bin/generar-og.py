#!/usr/bin/env python3
"""Genera la tarjeta Open Graph de preceptoros.org. Procedural, reproducible.

El canon dice «procedural, nunca assets pesados». Una imagen social no puede ser
SVG -- la mayoria de los raspadores (Slack, LinkedIn, X) no lo renderizan -- asi
que hay que producir un PNG. Lo que si se puede es que ese PNG no sea un binario
caido del cielo: este guion lo REGENERA, y por eso el asset es auditable.

Herramienta de CONSTRUCCION, no del producto. Usa Pillow del python del sistema.
Eso no roza la promesa de «MVP stdlib only»: el MVP no lo importa ni lo necesita,
y lo que se despliega es el PNG, no este fichero.

    python3 ~/p0x/bin/generar-og.py
"""
from __future__ import annotations

import sys
from pathlib import Path

DESTINO = Path.home() / "preceptoros-web" / "public" / "assets" / "preceptor-og.png"
FUENTE_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
FUENTE_R = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

# Los mismos tokens que base.css. Si divergen, la tarjeta deja de ser la marca.
TINTA = (30, 24, 38)
VIOLETA = (109, 90, 224)
BRONCE = (120, 98, 76)
BRONCE_CLARO = (147, 112, 92)
MARMOL = (228, 232, 236)

W, H = 1200, 630


def main():
    try:
        from PIL import Image, ImageDraw, ImageFont
    except ImportError:
        print("NO_DATA: falta Pillow en este interprete.\n"
              "Remedio: correr con /usr/bin/python3, que lo trae.", file=sys.stderr)
        return 1

    img = Image.new("RGB", (W, H), TINTA)
    d = ImageDraw.Draw(img)

    # Degradado vertical sutil hacia el violeta. Barato en bytes: el PNG
    # comprime bandas horizontales casi a nada.
    for y in range(H):
        t = (y / H) ** 1.6
        d.line([(0, y), (W, y)],
               fill=tuple(int(TINTA[i] + (VIOLETA[i] - TINTA[i]) * t * 0.30)
                          for i in range(3)))

    # El ojo, la marca. Se dibuja en ALMENDRA y no en elipse, igual que el
    # favicon: la elipse daba un ojo de buho y la marca del busto es un parpado.
    # Se compone de dos arcos de circunferencia que se cortan -- la forma de
    # lente clasica -- calculados y no aproximados a ojo.
    cx, cy, mitad, alto = 250, 300, 225, 118
    def parpado(signo):
        # Circunferencia que pasa por (cx±mitad, cy) y por (cx, cy+signo*alto).
        radio = (mitad ** 2 + alto ** 2) / (2 * alto)
        centro = cy + signo * (radio - alto)
        pasos, pts = 80, []
        for i in range(pasos + 1):
            x = cx - mitad + (2 * mitad) * i / pasos
            dy = max(radio ** 2 - (x - cx) ** 2, 0) ** .5
            pts.append((x, centro - signo * dy))
        return pts

    contorno = parpado(1) + list(reversed(parpado(-1)))
    d.line(contorno + [contorno[0]], fill=BRONCE, width=7, joint="curve")

    ri = 78
    d.ellipse([cx - ri, cy - ri, cx + ri, cy + ri], fill=VIOLETA)
    d.ellipse([cx - ri * .44, cy - ri * .44, cx + ri * .44, cy + ri * .44], fill=TINTA)
    # El brillo, DENTRO del iris: fuera se leia como una mancha.
    bx, by, br = cx - ri * .42, cy - ri * .42, ri * .17
    d.ellipse([bx - br, by - br, bx + br, by + br], fill=MARMOL)

    titulo = ImageFont.truetype(FUENTE_B, 84)
    lema = ImageFont.truetype(FUENTE_R, 38)
    pie = ImageFont.truetype(FUENTE_R, 27)

    x = 500
    d.text((x, 208), "Preceptor", font=titulo, fill=MARMOL)
    ancho = d.textlength("Preceptor", font=titulo)
    d.text((x + ancho, 208), "OS", font=titulo, fill=BRONCE_CLARO)

    d.text((x, 322), "Tu IA, tu memoria, tu soberanía.", font=lema, fill=MARMOL)
    d.line([(x, 392), (W - 90, 392)], fill=BRONCE, width=3)
    d.text((x, 414), "La aduana entre tú y la nube.", font=pie, fill=BRONCE_CLARO)
    d.text((x, 452), "Sin cuentas · sin telemetría · sin nube obligatoria",
           font=pie, fill=BRONCE_CLARO)

    DESTINO.parent.mkdir(parents=True, exist_ok=True)
    img.save(DESTINO, "PNG", optimize=True)
    print(f"{DESTINO} · {DESTINO.stat().st_size} B · {W}x{H}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
