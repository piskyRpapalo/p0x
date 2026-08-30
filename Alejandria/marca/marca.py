"""Recorta el busto de PreceptorOS de los JPEG de Gemini. Marca principal.

EL PROBLEMA: los JPEG traen la transparencia DIBUJADA -- un damero de dos
grises (~26x21 px) horneado en pixeles. No hay alfa que rescatar.

LO QUE NO FUNCIONA: filtrar por color. El marmol del busto tambien es casi
blanco, asi que una tolerancia generosa se come la cara y una apretada deja
media pared de damero. Medido: con tolerancia 26 el fondo se lleva trozos de
frente y mejilla; con 4 no quita casi nada.

LO QUE SI: usar la ESTRUCTURA. Un pixel de damero tiene, a un periodo exacto
de distancia, el tono CONTRARIO. El marmol no alterna con esa cadencia. La
comprobacion es local, asi que el periodo no entero (25,7 x 21,3) no acumula
deriva: el vecino a 26 px cae dentro del cuadro de al lado igualmente.

Y DESPUES: quedan motas sueltas donde el JPEG emborrono los bordes del damero.
Se limpian por componentes conexas -- se conserva la cabeza y los cascotes con
cuerpo, se tira lo que mide menos que un cascote.
"""
import numpy as np
from collections import deque
from PIL import Image, ImageFilter

CLARO = np.array([254, 255, 250])
OSCURO = np.array([215, 215, 210])
PX, PY = 26, 21                      # periodo del damero, medido


def _desplaza(m, dy, dx):
    r = np.zeros_like(m)
    ys = slice(max(0, dy), m.shape[0] + min(0, dy))
    xs = slice(max(0, dx), m.shape[1] + min(0, dx))
    yd = slice(max(0, -dy), m.shape[0] + min(0, -dy))
    xd = slice(max(0, -dx), m.shape[1] + min(0, -dx))
    r[yd, xd] = m[ys, xs]
    return r


def _dilata(m, r=3):
    out = m.copy()
    for dy in range(-r, r + 1):
        for dx in range(-r, r + 1):
            out |= _desplaza(m, dy, dx)
    return out


def _inundar(cand):
    h, w = cand.shape
    f = np.zeros((h, w), bool)
    cola = deque()
    for y, x in ([(y, x) for x in range(w) for y in (0, h - 1)] +
                 [(y, x) for y in range(h) for x in (0, w - 1)]):
        if cand[y, x] and not f[y, x]:
            f[y, x] = True; cola.append((y, x))
    while cola:
        y, x = cola.popleft()
        for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            ny, nx = y + dy, x + dx
            if 0 <= ny < h and 0 <= nx < w and cand[ny, nx] and not f[ny, nx]:
                f[ny, nx] = True; cola.append((ny, nx))
    return f


def _componentes(m, minimo, lum=None):
    """Conserva las islas con cuerpo y descarta los restos de damero.

    Dos criterios, y el segundo importa mas de lo que parece: hay cuadros de
    damero enteros que el inundado no alcanza --su prueba de alternancia
    fallo-- y que son demasiado grandes para caer por tamano. Se reconocen
    porque son PLANOS: un cuadro de damero tiene desviacion casi cero y un
    tono exacto. Un cascote de marmol, por pequeno que sea, tiene sombra,
    borde y relieve. La planitud los separa sin discutir.
    """
    h, w = m.shape
    visto = np.zeros((h, w), bool)
    salida = np.zeros((h, w), bool)
    for y0 in range(h):
        for x0 in range(w):
            if not m[y0, x0] or visto[y0, x0]:
                continue
            cola = deque([(y0, x0)]); visto[y0, x0] = True; isla = [(y0, x0)]
            while cola:
                y, x = cola.popleft()
                for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    ny, nx = y + dy, x + dx
                    if 0 <= ny < h and 0 <= nx < w and m[ny, nx] and not visto[ny, nx]:
                        visto[ny, nx] = True; cola.append((ny, nx)); isla.append((ny, nx))
            if len(isla) < minimo:
                continue
            if lum is not None:
                v = np.array([lum[y, x] for y, x in isla], float)
                plano = v.std() < 6.0 and (abs(v.mean() - 254) < 8 or
                                           abs(v.mean() - 215) < 8)
                if plano:
                    continue          # cuadro de damero, no cascote
            for y, x in isla:
                salida[y, x] = True
    return salida


def _erosiona(m, r=2):
    out = m.copy()
    for dy in range(-r, r + 1):
        for dx in range(-r, r + 1):
            out &= _desplaza(m, dy, dx)
    return out


def solo_mayor(m, erosion=0):
    """Con `erosion`, encoge antes de contar islas y luego devuelve los
       pixeles originales que caen dentro. Un puente de uno o dos pixeles
       --que el desenfoque del alfa crea solo-- no sobrevive al encogido, y
       asi el trozo de la cabeza vecina deja de contar como parte de esta."""
    if erosion:
        nucleo = _mayor(_erosiona(m, erosion))
        return m & _dilata(nucleo, erosion + 2)
    return _mayor(m)


def _mayor(m):
    """La isla mas grande y nada mas: la cabeza.

    Para la marca es lo correcto y no una simplificacion. Los restos de damero
    que sobreviven a todo lo anterior son islas propias, y aqui desaparecen
    todas de una vez sin mas heuristica. Los cascotes que vuelan en la
    secuencia de despertar tambien caen -- por eso esa secuencia se recorta
    con `solo_mayor=False`, que es donde los cascotes cuentan.
    """
    h, w = m.shape
    visto = np.zeros((h, w), bool)
    mejor = []
    for y0 in range(h):
        for x0 in range(w):
            if not m[y0, x0] or visto[y0, x0]:
                continue
            cola = deque([(y0, x0)]); visto[y0, x0] = True; isla = [(y0, x0)]
            while cola:
                y, x = cola.popleft()
                for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    ny, nx = y + dy, x + dx
                    if 0 <= ny < h and 0 <= nx < w and m[ny, nx] and not visto[ny, nx]:
                        visto[ny, nx] = True; cola.append((ny, nx)); isla.append((ny, nx))
            if len(isla) > len(mejor):
                mejor = isla
    out = np.zeros((h, w), bool)
    for y, x in mejor:
        out[y, x] = True
    return out


def recortar(ruta, tol=20, minimo=400, mayor=True):
    """JPEG con damero -> RGBA con alfa de verdad. No recorta el lienzo:
       el encuadre se decide fuera, en comun para toda una secuencia."""
    im = Image.open(ruta).convert("RGB")
    a = np.asarray(im).astype(np.int16)
    sat = a.max(2) - a.min(2)
    claro = (sat < 18) & (np.abs(a - CLARO).max(2) < tol)
    oscuro = (sat < 18) & (np.abs(a - OSCURO).max(2) < tol)
    # La alternancia se exige en LOS DOS EJES. Con uno solo bastaba, y los
    # rizos del pelo caian: entre bucle y bucle hay damero, y el borde
    # rizo/hueco alterna en horizontal por casualidad. Un damero de verdad
    # alterna tambien en vertical; un rizo, no.
    def _alt(dy, dx):
        return (claro & _desplaza(oscuro, dy, dx)) | (oscuro & _desplaza(claro, dy, dx))
    en_x = _alt(0, PX) | _alt(0, -PX)
    en_y = _alt(PY, 0) | _alt(-PY, 0)
    cand = (claro | oscuro) & _dilata(en_x & en_y, 3)
    bruto = ~_inundar(cand)
    sujeto = solo_mayor(bruto) if mayor else _componentes(bruto, minimo, lum=a.mean(2))
    alfa = Image.fromarray(np.where(sujeto, 255, 0).astype(np.uint8), "L")
    im.putalpha(alfa.filter(ImageFilter.GaussianBlur(0.7)))
    return im


def recortar_oscuro(ruta, umbral=190, minimo=400):
    """Para los que ya vienen sobre fondo oscuro liso."""
    im = Image.open(ruta).convert("RGB")
    a = np.asarray(im).astype(np.int16)
    sujeto = _componentes(~_inundar(a.sum(2) < umbral), minimo)
    alfa = Image.fromarray(np.where(sujeto, 255, 0).astype(np.uint8), "L")
    im.putalpha(alfa.filter(ImageFilter.GaussianBlur(0.7)))
    return im


def mascara(im, umbral=24):
    return np.asarray(im.split()[3]) > umbral


def desfase(a, b, radio=14):
    """Cuanto hay que mover `b` para que encaje con `a`. Fuerza bruta sobre
       la mascara: exacto, y a este tamano cuesta menos que discutirlo."""
    ma, mb = mascara(a), mascara(b)
    mejor, dxy = -1, (0, 0)
    for dy in range(-radio, radio + 1):
        for dx in range(-radio, radio + 1):
            s = (ma & _desplaza(mb, dy, dx)).sum()
            if s > mejor:
                mejor, dxy = s, (dy, dx)
    union = (ma | _desplaza(mb, *dxy)).sum()
    return dxy, mejor / union if union else 0.0


def _masc_n(im, n):
    return np.asarray(im.split()[3].resize((n, n), Image.LANCZOS)) > 24


def registrar(ref, im, grueso=10, fino=6):
    """Desplazamiento que hace encajar `im` sobre `ref`. Dos pasadas.

    HACE FALTA, y esto se midio antes de escribirlo: los paquetes de cuatro no
    vienen alineados. En los tres packs, la fila de abajo esta 28-40 px mas
    arriba que la de encima. Componerlos tal cual daria una animacion en la
    que la cabeza da un salto vertical a mitad de ciclo -- y como entre
    variantes SOLO cambia el ojo, ese salto seria lo unico que se veria.

    Primero a 256 px --barato, encuentra el desplazamiento grande-- y despues
    a resolucion completa en una ventana pequena alrededor.
    """
    n = 256; k = im.width // n
    ma, mb = _masc_n(ref, n), _masc_n(im, n)
    mejor, base = -1, (0, 0)
    for dy in range(-grueso, grueso + 1):
        for dx in range(-grueso, grueso + 1):
            s = (ma & _desplaza(mb, dy, dx)).sum()
            if s > mejor:
                mejor, base = s, (dy, dx)
    by, bx = base[0] * k, base[1] * k
    MA, MB = mascara(ref), mascara(im)
    mejor, fin = -1, (by, bx)
    for dy in range(by - fino, by + fino + 1):
        for dx in range(bx - fino, bx + fino + 1):
            s = (MA & _desplaza(MB, dy, dx)).sum()
            if s > mejor:
                mejor, fin = s, (dy, dx)
    union = (MA | _desplaza(MB, *fin)).sum()
    return fin, (mejor / union if union else 0.0)


def mover(im, dy, dx):
    lienzo = Image.new("RGBA", im.size, (0, 0, 0, 0))
    lienzo.paste(im, (dx, dy))
    return lienzo


def congelar(ims, ref=0):
    """Congela la POSICION, no el contorno. Y la diferencia costo una prueba.

    La idea de partida era imponer a todos la silueta del fotograma de
    referencia: entre variantes solo cambia el ojo, luego el contorno deberia
    ser uno solo. Se hizo, se miro, y estaba mal: el solape real entre
    fotogramas es del 90-100%, no del 100%, porque cada cuadro es un render
    aparte y la cabeza cambia un poco de forma. Al imponer una silueta ajena,
    los que menos encajaban --ojo-cerebro, ojo-azul, habla-3-- salian con
    mordiscos negros en el pelo.

    Lo que SI es comun y por tanto lo que se congela es donde esta la cabeza.
    Cada fotograma conserva su propio alfa, que para el es exacto, y se
    desplaza hasta caer en el mismo sitio que los demas. Alineados y sin
    mordiscos: la animacion no salta y ningun cuadro lleva un contorno que no
    es el suyo.
    """
    base = ims[ref]
    salida, informe = [], []
    for i, im in enumerate(ims):
        if i == ref:
            salida.append(im.copy()); informe.append(((0, 0), 1.0)); continue
        (dy, dx), iou = registrar(base, im)
        salida.append(mover(im, dy, dx))
        informe.append(((dy, dx), iou))
    return salida, informe


def islas(m, minimo=20000):
    """Todas las islas con cuerpo, de mayor a menor, con su caja."""
    h, w = m.shape
    visto = np.zeros((h, w), bool)
    out = []
    for y0 in range(h):
        for x0 in range(w):
            if not m[y0, x0] or visto[y0, x0]:
                continue
            cola = deque([(y0, x0)]); visto[y0, x0] = True
            ys = [y0]; xs = [x0]
            while cola:
                y, x = cola.popleft()
                for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    ny, nx = y + dy, x + dx
                    if 0 <= ny < h and 0 <= nx < w and m[ny, nx] and not visto[ny, nx]:
                        visto[ny, nx] = True; cola.append((ny, nx))
                        ys.append(ny); xs.append(nx)
            if len(ys) >= minimo:
                out.append((len(ys), (min(xs), min(ys), max(xs) + 1, max(ys) + 1)))
    out.sort(reverse=True)
    return out


def partir_pack(ruta, cuantos=4, margen=12):
    """Separa un paquete de N cabezas SIN suponer una rejilla.

    Cortar por la mitad parecia obvio y estaba mal: medido, las cabezas de la
    fila de abajo salian con 512 px de alto exactos, que es el alto del
    cuadrante -- estaban CORTADAS por el corte. De ahi venia el falso desfase
    de 28-40 px, que no era desfase sino amputacion.

    Aqui se recorta el pack entero una vez, se buscan las N islas mayores y
    cada una se lleva su caja real. Sin rejilla que adivinar.
    """
    entero = recortar(ruta, mayor=False, minimo=20000)
    m = mascara(entero)
    cajas = [c for _, c in islas(m)[:cuantos]]
    # Dos cabezas que se tocan salen como UNA isla. Se detecta por altura --el
    # doble de lo normal-- y se parte por la fila de menos contacto: el cuello
    # de botella entre las dos, que en una cabeza sola no existe.
    while len(cajas) < cuantos:
        cajas.sort(key=lambda c: c[3] - c[1], reverse=True)
        x0, y0, x1, y1 = cajas[0]
        banda = m[y0:y1, x0:x1].sum(1)
        a, b = int(len(banda) * 0.35), int(len(banda) * 0.65)
        corte = y0 + a + int(np.argmin(banda[a:b]))
        cajas = cajas[1:] + [(x0, y0, x1, corte), (x0, corte, x1, y1)]
    cajas.sort(key=lambda c: (round(c[1] / 100), c[0]))
    # orden de lectura: por filas y luego por columnas
    cajas.sort(key=lambda c: (round(c[1] / 100), c[0]))
    W, H = entero.size
    fuera = []
    for x0, y0, x1, y1 in cajas:
        rec = entero.crop((max(0, x0 - margen), max(0, y0 - margen),
                           min(W, x1 + margen), min(H, y1 + margen)))
        # Al partir dos cabezas que se tocan, a cada mitad le queda un trozo
        # de la vecina pegado al corte. Se ve como un saliente blanco en el
        # borde. Quedarse con la isla mayor DENTRO del recorte lo quita sin
        # tener que adivinar donde estaba exactamente la costura.
        a = np.asarray(rec.split()[3])
        rec.putalpha(Image.fromarray(
            # Umbral alto a proposito: el desenfoque del alfa puede tender un
            # puente de un pixel entre el trozo vecino y la cabeza, y entonces
            # "la isla mayor" se los lleva a los dos.
            np.where(solo_mayor(a > 128, erosion=2), a, 0).astype(np.uint8), "L"))
        fuera.append(rec)
    return fuera


LIENZO = 640


def centrar(im, lado=LIENZO):
    """Cada cabeza en un lienzo comun, centrada por su caja. Sin esto no se
       pueden ni comparar: vienen recortadas a medidas distintas."""
    c = im.split()[3].point(lambda v: 255 if v > 24 else 0).getbbox()
    rec = im.crop(c)
    k = min(lado * 0.94 / rec.width, lado * 0.94 / rec.height)
    nw, nh = round(rec.width * k), round(rec.height * k)
    out = Image.new("RGBA", (lado, lado), (0, 0, 0, 0))
    out.paste(rec.resize((nw, nh), Image.LANCZOS), ((lado - nw) // 2, (lado - nh) // 2))
    return out
