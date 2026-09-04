"""Deriva la cara de la marca a los siete sitios que la ensenan.

LA CARA OFICIAL es `cara-oficial.jpg`: copia BYTE A BYTE del render original
(`Images-preceptorOS-head/Gemini_Generated_Image_4pm0mw...`), elegida por el
Soberano el 2026-09-02. Vive aqui versionada, y no en la carpeta de originales,
porque esa esta fuera de git: sin este fichero la cadena no se puede rehacer
sin ir al almacenamiento frio.

POR QUE ESTA Y NO UN MASTER DE `marca/`. Los `busto-*.png` salieron de recortar
los JPEG y recuperarles el alfa a mano (`marca.py`, la funcion `congelar`,
porque los originales traian el damero de transparencia DIBUJADO en pixeles).
Ese trabajo es bueno para un avatar sobre cualquier fondo, pero para el icono
cuesta lo que se vio el 2026-09-02: al recomponerlos sobre un fondo y volver a
cuantizarlos salian con el pelo cortado y cascotes sueltos que se leen como
picos blancos. Esta cara YA TRAE su fondo oscuro y su halo violeta horneados:
aqui solo se reescala. Copiar y pegar, que era lo pedido.

DOS TAMANOS Y UNA REGLA:
  ICONO `any`      · el cuadrado entero. La cabeza ya ocupa el 90 % del alto.
  ICONO `maskable` · la cabeza encogida al 72 %, con relleno del mismo oscuro.
    El sistema le recorta un circulo por encima; lo que toque el borde
    desaparece, y eso solo se ve ya instalado en el lanzador de otro.

Y LA TARJETA SOCIAL, que es la puerta: la misma cara a la izquierda sobre el
mismo oscuro liso --por eso no hay costura-- y el texto a la derecha.

    python3 iconos.py --comprobar   # falla si algun producto ensena otra cara
    python3 iconos.py --si          # los rehace
"""
import argparse
import hashlib
import io
import os
import sys

from PIL import Image, ImageDraw, ImageFont

AQUI = os.path.dirname(os.path.abspath(__file__))
WEB = os.path.expanduser("~/preceptoros-web/public/assets")
APP = os.path.expanduser("~/p0x/preceptor/assets")
CARA = os.path.join(AQUI, "cara-oficial.jpg")

# Medidos del propio master, no elegidos: el fondo es su esquina, y la cabeza
# es lo claro dentro del lienzo. Si el master cambia, estos cambian con el.
TINTA = (30, 24, 34)
CABEZA = (126, 49, 900, 967)          # x0, y0, x1, y1 sobre 1024x1024
LIENZO = 1024

CLARO = (228, 232, 236)
BRONCE = (147, 112, 92)

TITULO = ("Preceptor", "OS")
LEMA = "Tu IA, tu memoria, tu soberanía."
# La metafora de aduana se retiro el 2026-09-02 por decision del Soberano:
# describia el producto como un puesto de control, y es lo contrario -- una
# GUIA que se instala y acompana. El tono que manda es familiar y plug&play.
PIE = ["Una guía que se instala y ya te acompaña.",
       "Sin cuentas · sin telemetría · sin nube obligatoria"]

FUENTES = ("/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf",
           "/usr/share/fonts/truetype/noto/NotoSans-Regular.ttf")


def fuente(ruta, tam):
    if not os.path.isfile(ruta):
        raise SystemExit("NO_DATA: falta la fuente %s\n"
                         "  remedio: instala fonts-noto-core, o cambia FUENTES"
                         % ruta)
    return ImageFont.truetype(ruta, tam)


def cara():
    return Image.open(CARA).convert("RGB")


def icono(lado, alto_cabeza, apaga_halo=None):
    """Cuadrado de `lado` px con la cabeza a `alto_cabeza` de fraccion del alto.

    Se escala el LIENZO ENTERO y se centra por la CABEZA, no por el lienzo: el
    master tiene 49 px de aire arriba y 57 abajo, asi que centrar el cuadrado
    deja la cabeza cuatro pixeles alta. A 192 px eso se ve.

    `apaga_halo` es la fraccion del lado donde el halo tiene que haber muerto
    del todo. Solo la usa el MASKABLE, y no es cosmetica: el halo violeta llega
    hasta el canto del master, asi que para cualquier medidor honesto --el gate
    incluido-- eso ES dibujo, y ningun tamano de cabeza haria que el icono
    cupiera en su circulo. Se apaga con un desvanecido radial al MISMO oscuro
    del fondo: sin costura, porque es exactamente el color que ya hay debajo.
    """
    c = cara()
    alto_actual = (CABEZA[3] - CABEZA[1]) / LIENZO
    escala = (alto_cabeza / alto_actual) * lado / LIENZO
    c = c.resize((max(1, round(LIENZO * escala)),) * 2, Image.LANCZOS)

    fondo = Image.new("RGB", (lado, lado), TINTA)
    # centro de la cabeza en el master, llevado a la escala nueva
    cx = (CABEZA[0] + CABEZA[2]) / 2 * escala
    cy = (CABEZA[1] + CABEZA[3]) / 2 * escala
    fondo.paste(c, (round(lado / 2 - cx), round(lado / 2 - cy)))

    if apaga_halo is None:
        return fondo
    r1 = apaga_halo * lado
    r0 = r1 * 0.86                       # hasta aqui, intacto; de aqui a r1, se va
    mascara = Image.new("L", (lado, lado), 0)
    d = ImageDraw.Draw(mascara)
    pasos = 48
    for i in range(pasos, -1, -1):
        r = r0 + (r1 - r0) * i / pasos
        v = round(255 * (1 - i / pasos))
        d.ellipse([lado / 2 - r, lado / 2 - r, lado / 2 + r, lado / 2 + r], fill=v)
    d.ellipse([lado / 2 - r0, lado / 2 - r0, lado / 2 + r0, lado / 2 + r0], fill=255)
    return Image.composite(fondo, Image.new("RGB", (lado, lado), TINTA), mascara)


def tarjeta(ancho=1200, alto=630):
    """La cara a la izquierda y el texto a la derecha, sobre el MISMO oscuro.

    Fondo liso y no degradado: el master trae su halo sobre este color exacto,
    asi que pegarlo encima no deja costura. Un degradado obligaria a recortar
    el halo, que es justo lo que hace aparecer un borde.
    """
    fondo = Image.new("RGB", (ancho, alto), TINTA)

    # La cabeza mide 500 px de alto: la de la tarjeta anterior median 488, y se
    # queda con aire arriba y abajo en vez de tocar el canto.
    alto_cabeza = 500
    escala = alto_cabeza / (CABEZA[3] - CABEZA[1])
    c = cara().resize((round(LIENZO * escala),) * 2, Image.LANCZOS)
    izq = round(45 - CABEZA[0] * escala)            # 45 px de margen a la cara
    arr = round((alto - alto_cabeza) / 2 - CABEZA[1] * escala)
    fondo.paste(c, (izq, arr))

    d = ImageDraw.Draw(fondo)
    x = round(ancho * 0.42)
    f_tit, f_lema, f_pie = (fuente(FUENTES[0], 86), fuente(FUENTES[1], 40),
                            fuente(FUENTES[1], 30))
    y = 195
    d.text((x, y), TITULO[0], font=f_tit, fill=CLARO)
    d.text((x + d.textlength(TITULO[0], font=f_tit), y), TITULO[1],
           font=f_tit, fill=BRONCE)
    y += 125
    d.text((x, y), LEMA, font=f_lema, fill=CLARO)
    y += 78
    d.line([(x, y), (ancho - 60, y)], fill=BRONCE, width=2)
    y += 30
    for linea in PIE:
        d.text((x, y), linea, font=f_pie, fill=BRONCE)
        y += 44
    return fondo


def puerta(lado, alto_cabeza, apaga_halo=None, radio=0.455):
    """El icono de la PUERTA: la misma cara, con un anillo de bronce.

    POR QUE EXISTE, medido el 2026-09-04. La web y la app son dos productos
    instalables, y hasta hoy compartian icono BYTE A BYTE --mismo sha256-- y
    ademas el mismo `short_name`. O sea: quien seguia el camino entero acababa
    con dos iconos identicos y la misma etiqueta debajo, uno al lado del otro
    en su pantalla de inicio, y ninguna forma de saber cual era cual. Justo en
    el momento en que ya habia hecho el trabajo de instalar las dos cosas.

    POR QUE UN ANILLO Y NO OTRA CARA. Los otros masters de esta carpeta
    --green, blue, Orange, marble, los wake-- son placas de croma: su esquina
    mide (7,247,0). Componerlos sobre un fondo es exactamente el trabajo que la
    cabecera de este fichero documenta como fallido: pelo cortado y cascotes
    que se leen como picos blancos. El unico master compuesto es
    `cara-oficial.jpg`, asi que la puerta se separa por marca, no por retrato:
    misma familia, distinta insignia. A tamano de icono un anillo se distingue
    antes que un cambio de tono de fondo.

    EL RADIO NO ES EL MISMO EN LAS DOS VARIANTES, y esa es la trampa. Android
    recorta los maskable a un circulo del 80 % del lado, y este fichero ya
    apaga el halo a 0.395 para que quepa. Un anillo pintado a 0.455 caeria
    fuera del recorte Y dentro de la zona que el desvanecido borra: no se
    veria, o se veria a medias segun el telefono. En el maskable va a 0.32, que
    esta dentro de la parte que el desvanecido deja intacta (0.395 x 0.86).
    """
    base = icono(lado, alto_cabeza, apaga_halo)
    d = ImageDraw.Draw(base)
    r = radio * lado
    grosor = max(2, round(lado / 34))
    d.ellipse([lado / 2 - r, lado / 2 - r, lado / 2 + r, lado / 2 + r],
              outline=BRONCE, width=grosor)
    return base


# La puerta (web) estrena insignia; el taller (app) NO se toca, y el orden de
# esa decision importa: su icono ya esta instalado en aparatos, y cambiarlo
# moveria el dibujo bajo el dedo de quien ya lo tiene. Estrena el que todavia
# no ha llegado a ninguna pantalla de inicio.
PLAN = [
    (os.path.join(WEB, "preceptor-og.png"), tarjeta),
    (os.path.join(WEB, "icon-192.png"), lambda: puerta(192, 0.90)),
    (os.path.join(WEB, "icon-512.png"), lambda: puerta(512, 0.90)),
    (os.path.join(WEB, "icon-512-maskable.png"),
     lambda: puerta(512, 0.55, apaga_halo=0.395, radio=0.32)),
    (os.path.join(APP, "icono-192.png"), lambda: icono(192, 0.90)),
    (os.path.join(APP, "icono-512.png"), lambda: icono(512, 0.90)),
    (os.path.join(APP, "icono-512-maskable.png"), lambda: icono(512, 0.55, apaga_halo=0.395)),
]


def _codifica(im, destino=None):
    """Un solo sitio donde se decide COMO se guarda.

    FASTOCTREE, 256 COLORES, SIN DIFUMINADO. El gate declara un techo de 256 KB
    para los tres iconos del manifiesto juntos, y la primera version no cabia.
    Bajar la paleta era el reflejo, y era el movimiento equivocado: a 128
    colores MEDIANCUT dejaba el bronce de la maquina ROSA -- se ve a simple
    vista-- porque reparte la paleta por volumen y el marmol gris y el halo
    violeta se la comen entera.

    Medido el 2026-09-02 sobre el icono de 512, error medio por canal contra el
    original sin cuantizar (global · zona del bronce):

        MEDIANCUT   128   135 KB   2,83 · 9,27      <- el rosa
        MEDIANCUT   192   154 KB   2,34 · 7,37
        FASTOCTREE  256   100 KB   2,62 · 5,28      <- este
        MAXCOVERAGE 256    77 KB   5,13 · 5,56      banda el halo

    FASTOCTREE gana en las dos cosas a la vez: menos error en el bronce que
    ninguna mediana, y la mitad de bytes. Los tres iconos suman 168 KB y sobran
    93 del techo. El difuminado se queda fuera aparte: es ruido, y el ruido no
    comprime.

    Estaba escrito dos veces --al generar y al comprobar-- y esa es la forma
    exacta de que la comprobacion empiece a fallar sin que nada este mal.
    """
    q = im.convert("RGB").quantize(colors=256, method=Image.FASTOCTREE,
                                   dither=Image.NONE)
    if destino is None:
        buf = io.BytesIO()
        q.save(buf, "PNG", optimize=True)
        return buf.getvalue()
    q.save(destino, "PNG", optimize=True)
    return None


def comprobar():
    """Los siete ficheros, contra lo que este guion generaria HOY.

    Un icono desincronizado no da ningun error: la web ensena una cara, la app
    instalada ensena otra, y eso solo lo ve quien tenga las dos delante -- que
    no es nadie. Compara BYTES, no fechas: un fichero puede ser mas nuevo y
    traer la cara vieja si alguien lo copio de otro sitio.
    """
    mal = []
    for destino, hacer in PLAN:
        nombre = os.path.relpath(destino, os.path.expanduser("~"))
        if not os.path.exists(destino):
            mal.append("%s · NO EXISTE" % nombre)
            continue
        esperado = hashlib.sha256(_codifica(hacer())).hexdigest()
        with open(destino, "rb") as f:
            actual = hashlib.sha256(f.read()).hexdigest()
        if esperado != actual:
            mal.append("%s · cara distinta de la que manda el master" % nombre)
        else:
            print("  ok  %s" % nombre)
    if mal:
        print("\nDESCUADRE en %d de %d:" % (len(mal), len(PLAN)), file=sys.stderr)
        for m in mal:
            print("  FALLA  " + m, file=sys.stderr)
        print("  remedio: python3 iconos.py --si", file=sys.stderr)
        return 1
    print("\nlos %d cuadran" % len(PLAN))
    return 0


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--si", action="store_true", help="escribe de verdad")
    ap.add_argument("--comprobar", action="store_true",
                    help="falla si algun producto ensena una cara distinta")
    args = ap.parse_args(argv)

    if not os.path.isfile(CARA):
        print("NO_DATA: falta el master %s" % CARA, file=sys.stderr)
        print("  remedio: copialo de Alejandria/Images-preceptorOS-head/",
              file=sys.stderr)
        return 2
    if args.comprobar:
        return comprobar()

    for destino, hacer in PLAN:
        antes = os.path.getsize(destino) if os.path.exists(destino) else None
        if not args.si:
            print("  ~ %-52s %s" % (os.path.relpath(destino, os.path.expanduser("~")),
                                    "existe" if antes else "NUEVO"))
            continue
        _codifica(hacer(), destino)
        print("  + %-52s %7d B%s" % (
            os.path.relpath(destino, os.path.expanduser("~")),
            os.path.getsize(destino),
            "" if antes is None else "  (antes %d)" % antes))
    if not args.si:
        print("\nnada escrito. Repite con --si.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
