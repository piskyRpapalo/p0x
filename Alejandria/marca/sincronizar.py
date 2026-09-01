"""Lleva los masters de `marca/` a los dos destinos que los pintan.

POR QUE EXISTE: los 512x512 con alfa son MASTERS -- 300 KB cada uno. Servir eso
en una PWA es tirar 5 MB por una cara de 128 px. Este script deriva la copia que
cada destino necesita, y deja escrito de donde salio: sin el, la unica respuesta
a "de donde viene este webp" es la memoria de quien lo hizo.

LOS NOMBRES NO SON LIBRES. En la web, `test_web.py::test_cada_simbolo_del_hub_
existe` exige `assets/agente-<symbol>.webp` por cada `agentes[].symbol` de
hub.json. En la app no hay contrato de prefijo, asi que se usa el nombre pelado
del simbolo. Cambiar cualquiera de los dos rompe una imagen en silencio: un
<img> a un fichero ausente no falla, simplemente no pinta.

POR DEFECTO NO PISA NADA. Los ocho `agente-ojo-*.webp` de la web ya estaban y ya
pasan el gate; reescribirlos con otro encoder cambiaria 8 ficheros sin cambiar
un pixel visible. Con --forzar se rehacen todos.
"""
import argparse
import os
import sys

from PIL import Image

AQUI = os.path.dirname(os.path.abspath(__file__))
WEB = os.path.expanduser("~/preceptoros-web/public/assets")
APP = os.path.expanduser("~/p0x/preceptor/assets")

BUSTOS = ("corazon", "despierto", "dormido", "grieta",
          "halo", "ojo", "oscuro", "rompe")
OJOS = ("ambar", "azul", "birrete", "bombilla",
        "cerebro", "libro", "rojo", "verde")

# (master, destino, nombre_web, nombre_app, lado)
# El busto es AVATAR: se ve grande en el perfil, por eso 256. El ojo es
# cabezal de chat, nunca pasa de 128 en pantalla.
PLAN = ([("busto-%s.png" % n, "busto-%s.webp" % n, "busto-%s.webp" % n, 256)
         for n in BUSTOS]
        + [("ojo-%s.png" % n, "agente-ojo-%s.webp" % n, "ojo-%s.webp" % n, 128)
           for n in OJOS])

CALIDAD = 85
METODO = 6


def deriva(master, destino, lado):
    im = Image.open(master).convert("RGBA")
    if im.size != (lado, lado):
        im = im.resize((lado, lado), Image.LANCZOS)
    im.save(destino, "WEBP", quality=CALIDAD, method=METODO)
    return os.path.getsize(destino)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--forzar", action="store_true",
                    help="rehace tambien los que ya existen")
    args = ap.parse_args(argv)

    faltan = [d for d in (WEB, APP) if not os.path.isdir(d)]
    if faltan:
        print("NO_DATA: no existe el destino: " + ", ".join(faltan),
              file=sys.stderr)
        print("  remedio: comprueba que los dos repos estan clonados aqui",
              file=sys.stderr)
        return 2

    escritos = saltados = 0
    for nombre, en_web, en_app, lado in PLAN:
        master = os.path.join(AQUI, nombre)
        if not os.path.isfile(master):
            print("NO_DATA: falta el master %s" % nombre, file=sys.stderr)
            return 2
        for destino in (os.path.join(WEB, en_web), os.path.join(APP, en_app)):
            if os.path.exists(destino) and not args.forzar:
                print("  = %-34s (ya estaba)" % os.path.relpath(destino,
                                                               os.path.expanduser("~")))
                saltados += 1
                continue
            bytes_ = deriva(master, destino, lado)
            print("  + %-34s %6d B  %dx%d" % (
                os.path.relpath(destino, os.path.expanduser("~")),
                bytes_, lado, lado))
            escritos += 1
    print("escritos %d · ya estaban %d · masters %d"
          % (escritos, saltados, len(PLAN)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
