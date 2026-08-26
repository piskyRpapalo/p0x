"""El HTML lo escribe el servidor. El navegador solo lo coloca.

Antes esto vivia en `nexo.js`: llegaba JSON y siete pintores lo convertian en
HTML en el cliente. Ahora la lectura se convierte en fragmento AQUI y por el
flujo viaja HTML terminado. Tres cosas cambian y las tres importan:

- El navegador no parsea ni decide nada. Coloca una cadena y se acaba.
- El escapado ocurre en un solo sitio, en Python, sobre el dato crudo -- y no
  en cada pintor, que es donde se olvida uno.
- La regla de «sin dato, NO_DATA con causa» deja de estar repetida en dos
  lenguajes. Un solo `sin_dato()` la aplica a todo lo que sale.

Biblioteca estandar: `html.escape` y nada mas.
"""

from html import escape

NO_DATA = "NO_DATA"


def _vacio(v):
    return v is None or v == NO_DATA or v == ""


def e(v):
    return escape(str(v), quote=True)


def hueco(texto=NO_DATA):
    return f'<span class="nodata">{e(texto)}</span>'


def fila(k, v, clase="", sangrada=False):
    cuerpo = hueco() if _vacio(v) else f'<span class="{e(clase)}">{e(v)}</span>'
    extra = " fila--sangrada" if sangrada else ""
    return (f'<div class="fila{extra}"><span class="k">{e(k)}</span>'
            f'<span class="v">{cuerpo}</span></div>')


def causa(texto):
    return f'<p class="causa">{e(texto)}</p>' if texto else ""


def cifra(valor, pie, viva=False):
    clase = "cifra viva" if viva else "cifra"
    dentro = hueco() if _vacio(valor) else e(valor)
    return f'<div class="{clase}">{dentro}<small>{e(pie)}</small></div>'


def sin_dato(lectura):
    motivo = (lectura or {}).get("causa") or "el sensor no devolvio nada"
    detalle = (lectura or {}).get("detalle") or ""
    return {"chip": NO_DATA, "clase": "c-warn",
            "html": f'<div class="cifra">{hueco()}</div>' + causa(motivo)
                    + (f'<p class="detalle">{e(detalle)}</p>' if detalle else "")}


# ── un fragmento por sensor ─────────────────────────────────────────────────

def soberania(d):
    caps = "".join(
        fila(c["nombre"], "concedida" if c["concedida"] else "no concedida",
             "c-ok" if c["concedida"] else "c-mut")
        for c in d.get("capacidades", []))
    pie = ("corte activo · el centinela manda sobre lo declarado"
           if d.get("cortado")
           else f'nivel {d.get("nivel")} en vigor · nada por encima esta concedido')
    return {
        "chip": "santuario · corte" if d.get("cortado") else f'nivel {d.get("nivel")}',
        "clase": "c-warn" if d.get("cortado") else ("c-ok" if d.get("nivel") == 0 else "c-gold"),
        "html": caps + causa("el nivel 0 no aparece en la tabla: lo que el suelo "
                             "ya hace no pide permiso"),
        "nivel": d.get("nivel"),
        "pie": pie,
    }


CLASE_NODO = {"ONLINE": "c-ok", "CRITICO": "c-crit", "OFFLINE": "c-mut",
              "EN ESPERA": "c-warn", NO_DATA: "c-warn"}


def nodos(d):
    tarjetas = []
    for n in d.get("nodos", []):
        critico = " nodo--critico" if n["estado"] == "CRITICO" else ""
        alerta = (f'<p class="nodo__alerta">{e(n["alerta"])}</p>'
                  if n.get("alerta") else "")
        sondas = ", ".join(n.get("sondas") or [])
        # <details> y no un toggle con estado en JS: el navegador ya sabe abrir
        # y cerrar, lo hace con teclado y con lector de pantalla, y no cuesta
        # un solo byte de descarga ni de memoria.
        detalle = (f'<details class="nodo__mas"><summary>sondas</summary>'
                   f'<p>{e(sondas)}</p></details>') if sondas else ""
        tarjetas.append(
            f'<article class="nodo{critico}"><header><b>{e(n["nodo"])}</b>'
            f'<span class="chip {CLASE_NODO.get(n["estado"], "c-mut")}">'
            f'{e(n["estado"])}</span></header>'
            f'<p class="nodo__metal">{e(n["metal"])}</p>'
            f'<p class="nodo__nota">{hueco() if _vacio(n["nota"]) else e(n["nota"])}</p>'
            f'{alerta}{detalle}</article>')
    avisos = d.get("avisos") or []
    return {
        "chip": f'{d.get("en_pie")} en pie' + (f' · {d["criticos"]} critico'
                                               if d.get("criticos") else ""),
        "clase": "c-crit" if d.get("criticos") else "c-ok",
        "html": f'<div class="tira">{"".join(tarjetas)}</div>'
                + causa("fuente: " + str(d.get("fuente", NO_DATA))
                        + (" · " + " · ".join(avisos) if avisos else "")),
    }


def preceptor(d):
    t = d.get("tanda") or {}
    ok = t.get("estado") == "ok"
    verde = ok and t.get("verde")
    rancia = ok and t.get("rancia")
    medido = (t.get("medido") or "").replace("T", " ")[:16]
    return {
        "chip": ("verde · rancia" if rancia else "verde") if verde else NO_DATA,
        "clase": ("c-warn" if rancia else "c-ok") if verde else "c-warn",
        "html": cifra(f'{t["pruebas"]} / {t["pruebas"]}' if ok else None,
                      f'{t["suites"]} SUITES' if ok else "SIN TANDA REGISTRADA",
                      viva=bool(verde and not rancia))
                + fila("version", d.get("version"))
                + fila("ficheros de la cara", (d.get("huella") or {}).get("ficheros"))
                + fila("medida", medido or None)
                + fila("ruta", d.get("ruta"), "c-mut")
                + causa(t.get("causa", "")),
    }


def timers(d):
    filas = []
    sin_estrenar = 0
    for f in d.get("propios", []):
        filas.append(fila(f["unidad"].replace(".timer", ""), f["proxima"],
                          "c-ok" if f["activo"] else "c-crit"))
        if _vacio(f["ultima"]):
            sin_estrenar += 1
        etiqueta = "sin estrenar" if _vacio(f["resultado"]) else f["resultado"]
        filas.append(fila(f"ultima · {etiqueta}", f["ultima"],
                          "c-mut" if f["resultado"] == "success" else "c-warn", True))
    nota = f'{sin_estrenar} armado(s) y sin dispararse nunca · ' if sin_estrenar else ""
    return {"chip": f'{d.get("cuantos")} bucles',
            "clase": "c-warn" if sin_estrenar else "c-ok",
            "html": "".join(filas) + causa(
                nota + f'{d.get("cuantos_ajenos")} timers del sistema, aparte')}


def lora(d):
    ads = "".join(
        fila(a["nombre"],
             f'{a["bytes"] / 1048576:.1f} MiB' if a["estado"] == "ok" else None,
             "c-ok" if a["estado"] == "ok" else "", True)
        for a in d.get("adapters", []))
    return {"chip": f'{d.get("entrenados")} adapters',
            "clase": "c-gold" if d.get("entrenados") else "c-warn",
            "html": cifra(d.get("ejemplos_totales"),
                          f'EJEMPLOS · {len(d.get("datasets", []))} DATASETS')
                    + fila("fase", d.get("fase"), "c-warn")
                    + fila("con pesos",
                           f'{d.get("entrenados")} de {len(d.get("adapters", []))}')
                    + ads
                    + causa("una carpeta sin fichero de pesos no cuenta como adapter")}


def cinek(d):
    filas = "".join(
        fila(r["nombre"], f'{r["bytes"] / 1024:.0f} KiB · {r["dias"]} d')
        for r in d.get("registros", [])[:4])
    quietud = d.get("quietud_dias")
    return {"chip": f'{quietud} d sin tocar',
            "clase": "c-warn" if isinstance(quietud, int) and quietud > 7 else "c-ok",
            "html": cifra(quietud, "DIAS DE QUIETUD") + filas
                    + causa(f'{d.get("nota", "")} · los registros se listan, no se leen')}


def jardin(d):
    return {"chip": "en espera", "clase": "c-mut",
            "html": fila("rutas en disco", " · ".join(d.get("rutas") or []) or None)
                    + fila("sensores", d.get("sensores_declarados"))
                    + fila("ultima lectura", d.get("ultima_lectura"))
                    + causa(d.get("causa", ""))}


# ── el layer stack, compuesto aqui ──────────────────────────────────────────
# La banda focal la decide Python y llega marcada. Antes la ponia el navegador
# con classList.toggle: funcionaba, y era logica de decision viviendo en el
# cliente por costumbre y no por motivo. Aqui hay un sitio menos donde mirar.

CAPAS = ((3, 24, "ECOSISTEMA", "hardware · complementos · fuera del build"),
         (2, 88, "EXPANSION", "todo lo que cruza el borde · consentido uno a uno"),
         (1, 152, "ARNES", "un modelo en este disco · no sale de la maquina"),
         (0, 216, "SANTUARIO", "el suelo · no pide permiso a nadie"))


def capas(nivel, pie):
    bandas = []
    for n, y, nombre, nota in CAPAS:
        clase = "banda"
        if n == nivel:
            clase += " focal"
        elif n > (nivel if isinstance(nivel, int) else -1):
            clase += " dormida"
        bandas.append(
            f'<g class="{clase}" data-nivel="{n}">'
            f'<rect x="96" y="{y}" width="800" height="64"/>'
            f'<text class="eyebrow" x="112" y="{y + 36}">L{n}</text>'
            f'<text class="nombre" x="192" y="{y + 36}">{e(nombre)}</text>'
            f'<text class="nota" x="880" y="{y + 36}" text-anchor="end">{e(nota)}</text>'
            f'</g>')
    return ('<svg class="capas" viewBox="0 0 1000 344" role="img" '
            'aria-label="Las cuatro capas de soberania, con la capa en vigor destacada">'
            '<g class="brujula"><text class="eyebrow" x="40" y="52">alcance</text>'
            '<path d="M 56 200 L 56 76 M 48 92 L 56 76 L 64 92"/>'
            '<text class="eyebrow" x="40" y="272">suelo</text></g>'
            + "".join(bandas)
            + '<rect class="silueta" x="96" y="24" width="800" height="256"/>'
            + f'<text class="pie" x="96" y="308">{e(pie)}</text></svg>')


# ── la seccion entera, cabecera incluida ────────────────────────────────────
# El titulo vive AQUI y no en el HTML: la seccion se reemplaza entera por el
# flujo, asi que si el titulo viviera en la pagina se perderia en el primer
# refresco. Un solo sitio, y lo que llega es la tarjeta terminada.

# Cada tarjeta declara DE QUE SENSOR come. Casi siempre del que se llama igual,
# pero el mapa y el rack comparten lectura: son dos formas de mirar el mismo
# dato, y un segundo sensor para lo mismo serian dos verdades sobre un hecho.
TARJETAS = {
    "soberania": ("Capas de soberania", True, "soberania"),
    "nodos": ("El rack", True, "nodos"),
    "mapa": ("La malla", False, "nodos"),
    "observe": ("Observe · camara", False, "observe"),
    "adsb": ("El cielo · ADS-B", False, "adsb"),
    "cerebro": ("Segundo cerebro", False, "cerebro"),
    "preceptor": ("Nucleo publico", False, "preceptor"),
    "timers": ("Bucles de agentes", False, "timers"),
    "lora": ("La forja · adapters", False, "lora"),
    "cinek": ("Pipeline de video", False, "cinek"),
    "jardin": ("Jardin · permacultura", False, "jardin"),
}


def sensor_de(nombre):
    return TARJETAS.get(nombre, (None, None, nombre))[2]


def seccion(nombre, frag):
    titulo = TARJETAS.get(nombre, (nombre, False, nombre))[0]
    figura = ""
    if nombre == "soberania" and "nivel" in frag:
        figura = f'<div class="mod__body mod__body--figura">{capas(frag["nivel"], frag.get("pie", ""))}</div>'
    return (f'<div class="mod__head"><span class="mod__title">'
            f'<span class="pico">&#9656;</span> {e(titulo)}</span>'
            f'<span class="mod__spacer"></span>'
            f'<span class="chip {e(frag["clase"])}">{e(frag["chip"])}</span></div>'
            f'{figura}'
            f'<div class="mod__body">{frag["html"]}</div>')


# ── el mapa · la malla, dibujada ────────────────────────────────────────────
# Sin libreria de mapas, y no por ahorro: un mapa geografico aqui seria una
# mentira util -- lo que importa de esta topologia no es donde estan las
# maquinas sino QUIEN VE A QUIEN, y eso no tiene coordenadas. Se dibuja la
# malla: todos con todos, que es lo que hace una red de este tipo.
#
# Come del mismo sensor que la tarjeta del rack. Un segundo sensor para el
# mismo dato serian dos verdades sobre el mismo hecho.

MAPA_ANCHO, MAPA_ALTO, MAPA_R = 400, 224, 88
COLOR_ESTADO = {"ONLINE": "vivo", "CRITICO": "roto",
                "OFFLINE": "ido", NO_DATA: "mudo"}


def _en_rejilla(v):
    """A multiplo de 4. La misma regla que el layer stack, por el mismo motivo."""
    return int(round(v / 4.0)) * 4


def _sitios(cuantos):
    """Reparte los nodos en un circulo. Dos se ponen enfrentados, no encima."""
    import math
    cx, cy = MAPA_ANCHO // 2, MAPA_ALTO // 2
    if cuantos == 1:
        return [(cx, cy)]
    return [(_en_rejilla(cx + MAPA_R * math.cos(-math.pi / 2 + 2 * math.pi * i / cuantos)),
             _en_rejilla(cy + MAPA_R * 0.62 * math.sin(-math.pi / 2 + 2 * math.pi * i / cuantos)))
            for i in range(cuantos)]


def mapa(d):
    nodos_ = d.get("nodos", [])
    if not nodos_:
        return sin_dato({"causa": "sin nodos que dibujar"})
    sitios = _sitios(len(nodos_))

    # Las aristas primero, para que los nodos queden encima de las lineas.
    aristas = []
    for i in range(len(sitios)):
        for j in range(i + 1, len(sitios)):
            (x1, y1), (x2, y2) = sitios[i], sitios[j]
            aristas.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}"/>')

    marcas = []
    for (x, y), n in zip(sitios, nodos_):
        clase = COLOR_ESTADO.get(n["estado"], "mudo")
        marcas.append(
            f'<g class="nodo-mapa {clase}">'
            f'<rect x="{x - 8}" y="{y - 8}" width="16" height="16"/>'
            f'<text x="{x}" y="{y + 28}" text-anchor="middle">{e(n["nodo"])}</text>'
            f'<text class="est" x="{x}" y="{y + 40}" text-anchor="middle">'
            f'{e(n["estado"])}</text></g>')

    return {
        "chip": f'{len(nodos_)} nodos',
        "clase": "c-crit" if d.get("criticos") else "c-ok",
        "html": (f'<svg class="malla" viewBox="0 0 {MAPA_ANCHO} {MAPA_ALTO}" '
                 f'role="img" aria-label="La malla: {len(nodos_)} nodos, todos '
                 f'conectados con todos">'
                 f'<g class="aristas">{"".join(aristas)}</g>'
                 f'{"".join(marcas)}</svg>'
                 + causa("cada linea es un enlace cifrado punto a punto · no hay "
                         "centro, y por eso no hay nodo cuya caida apague el resto")),
    }


# ── el cielo · aeronaves situadas ───────────────────────────────────────────

ADSB_ANCHO, ADSB_ALTO = 400, 300
# Escala de altura, no semaforo. Ver el comentario del CSS: el rojo de este
# panel ya significa «roto», y un avion alto no esta roto, esta lejos.
COLOR_ALTURA = {"baja": "baja", "media": "media", "alta": "alta"}


def _situar(a, v):
    """Grados a pixeles. La `y` va invertida: el norte esta arriba."""
    x = (a["lon"] - v["oeste"]) / (v["este"] - v["oeste"]) * ADSB_ANCHO
    y = (v["norte"] - a["lat"]) / (v["norte"] - v["sur"]) * ADSB_ALTO
    # Se recorta al marco en vez de dejar que un avion salga del dibujo: con
    # ventana declarada puede haber trafico fuera de ella, y un circulo pintado
    # a x=-40 no se ve pero SI cuenta en la cifra de arriba. Pegado al borde,
    # al menos, dice «esta por ahi».
    return max(6, min(ADSB_ANCHO - 6, x)), max(6, min(ADSB_ALTO - 6, y))


def adsb(d):
    v = d["ventana"]
    marcas = []
    for a in d.get("aviones", []):
        x, y = _situar(a, v)
        clase = COLOR_ALTURA.get(a["escalon"], "muda")
        pies = a["pies"]
        # `<title>` dentro del circulo: el navegador ensena el rotulo al pasar
        # por encima, sin una linea de JavaScript ni un solo byte de libreria.
        rotulo = (f'{a["vuelo"]} · {a["hex"]} · '
                  f'{pies if pies != NO_DATA else NO_DATA} ft · '
                  f'{a["nudos"] if a["nudos"] != NO_DATA else NO_DATA} kt')
        marcas.append(f'<circle class="avion {clase}" cx="{x:.1f}" cy="{y:.1f}" '
                      f'r="4"><title>{e(rotulo)}</title></circle>')

    # El marco y la cruz si caen en la rejilla de 4: son estructura, no dato.
    guia = (f'<rect class="marco" x="0" y="0" width="{ADSB_ANCHO}" height="{ADSB_ALTO}"/>'
            f'<line class="cruz" x1="{ADSB_ANCHO // 2}" y1="0" '
            f'x2="{ADSB_ANCHO // 2}" y2="{ADSB_ALTO}"/>'
            f'<line class="cruz" x1="0" y1="{ADSB_ALTO // 2}" '
            f'x2="{ADSB_ANCHO}" y2="{ADSB_ALTO // 2}"/>')

    mudas = d.get("mudas", 0)
    nota = (f'{d.get("situadas")} situadas de {d.get("oidas")} oidas · '
            f'{mudas} emiten sin decir donde estan · escala {v["origen"]}')
    return {
        "chip": f'{d.get("situadas")} de {d.get("oidas")}',
        "clase": "c-warn" if mudas else "c-ok",
        "html": (f'<svg class="cielo" viewBox="0 0 {ADSB_ANCHO} {ADSB_ALTO}" '
                 f'role="img" aria-label="{e(nota)}">{guia}{"".join(marcas)}</svg>'
                 + causa(nota)),
    }


# ── el segundo cerebro · la forma, nunca el contenido ───────────────────────

def cerebro(d):
    filas = "".join(
        f'<div class="fila"><span class="k">{e(f["que"])}</span>'
        f'<span class="v"><span class="puntos">{e(f["silueta"])}</span> '
        f'{e(f["cuantos"])}</span></div>'
        for f in d.get("filas", []))
    vacio = d.get("vacio")
    falta = d.get("faltan") or []
    return {
        "chip": ("vacio" if vacio else f'{d.get("engramas")} engramas'),
        "clase": "c-warn" if vacio else "c-gold",
        "html": (cifra(d.get("densidad"), "ENLACES POR ENGRAMA",
                       viva=bool(d.get("enlaces")))
                 + filas
                 + causa((d.get("causa") or "")
                         + (" · sin tabla de " + ", ".join(falta) if falta else "")
                         + " · se cuenta la forma; no se lee una sola palabra")),
    }


# ── la camara · una etiqueta, cero JavaScript ───────────────────────────────

def observe(d):
    # `<img>` y ya esta: el navegador lleva decadas leyendo MJPEG. Y solo se
    # emite cuando la camara YA contesto, porque un `<img>` roto ensena el icono
    # de imagen partida -- que parece un fallo del panel y es de la camara, y no
    # dice cual de los dos.
    return {"chip": "en vivo" if d.get("mjpeg") else "responde",
            "clase": "c-ok",
            "html": f'<img class="camara" src="{e(d["url"])}" alt="camara en vivo">'
                    + causa(f'{d.get("tipo")} · sin una linea de JavaScript')}


FRAGMENTOS = {"soberania": soberania, "nodos": nodos, "mapa": mapa,
              "adsb": adsb,
              "preceptor": preceptor, "timers": timers, "lora": lora,
              "cinek": cinek, "jardin": jardin, "cerebro": cerebro,
              "observe": observe}


def de(nombre, lectura):
    """Lectura -> fragmento. Un sensor sin dato, o que revienta, sale como hueco."""
    pintor = FRAGMENTOS.get(nombre)
    if pintor is None or not lectura or lectura.get("estado") != "ok":
        frag = sin_dato(lectura)
        if nombre == "soberania":
            # Sin lectura no hay banda focal. El diagrama sale entero y apagado,
            # que dice la verdad: no se sabe en que nivel corre.
            frag["nivel"], frag["pie"] = None, "sin lectura del guardian"
        return frag
    try:
        return pintor(lectura)
    except Exception:                                            # noqa: BLE001
        return sin_dato({"causa": "la tarjeta no se pudo componer con esta lectura"})


def html_de(nombre, lectura):
    """Lo que viaja por el flujo: una seccion terminada, en una sola linea.

    Una sola linea porque en SSE cada salto obliga a un `data:` nuevo, y un
    fragmento partido a mano es un fragmento que un dia se parte mal.
    """
    return seccion(nombre, de(nombre, lectura)).replace("\n", " ")
