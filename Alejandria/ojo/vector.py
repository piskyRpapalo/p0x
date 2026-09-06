#!/usr/bin/env python3
"""El Vector de Estado Soberano: el rack, tipado, en el momento de preguntar.

QUE ES
------
Lo que el Ojo entrega hoy es prosa para una IA que lee. Esto es lo otro: un
objeto validado contra `esquema_vector.json` que se inyecta como
`[SYSTEM CONTEXT]` delante del prompt, para que el modelo local hable del rack
que hay y no del rack que se imagina.

LO QUE ESTE MODULO NO HACE, Y ES LO MAS IMPORTANTE DE EL
-------------------------------------------------------
No mide casi nada por su cuenta. En este repo ya habia TRES implementaciones de
«una lectura con su procedencia», y escribir una cuarta habria sido crear una
cuarta verdad sobre los mismos hechos:

  * `hexelion-nexo/sensores/`   -> los diez sensores del Nexo (ok / NO_DATA).
  * `preceptor/metricas.py`     -> el metal local (MEDIDO / NORMA / NO_DATA).
  * `Alejandria/ojo/ojo.py`     -> lo que el panel ya sirve.

Este fichero es el SOBRE que las adapta, y los adaptadores viven aqui juntos y
en un solo sitio (`de_metricas`, `de_nexo`) para que la equivalencia no se
bifurque. Cuando una fuente cambie de forma, se arregla una funcion, no doce.

LOS CUATRO ESTADOS, Y POR QUE NO SON DOS
----------------------------------------
`MEDIDO` sale de un aparato o del kernel. `NORMA` lo declara alguien y nadie lo
ha medido -- el canon del nodo lleva meses pagando esa confusion, con el techo
de VRAM del Jetson como cicatriz. `NO_DATA` es el hueco con su causa. `STALE`
es un dato que fue bueno y ya no puede leerse como «lo que hay».

El esquema hace cumplir la invariante que lo sostiene todo: **valor nulo si y
solo si NO_DATA**. Un cero decorativo no es un dato bajo, es una magnitud que
no existe, y aqui no cabe escribirlo aunque se quiera.

PRESUPUESTO DE SONDEO
---------------------
`ojo.py` prohibe sondar el rack al pintar. Este modulo hereda la regla y ademas
la hace visible: cada salida de la maquina se anota por su nombre en
`presupuesto.sondas`, y `--sin-red` las deja todas en NO_DATA declarado. Si
algun dia se cuela una sonda nueva, se ve en la salida en vez de descubrirse
por una espera de treinta segundos.
"""

import json
import os
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime
from pathlib import Path

AQUI = Path(__file__).resolve().parent
ESQUEMA = AQUI / "esquema_vector.json"
RAIZ = AQUI.parents[1]
# El modulo de metricas del producto se carga POR RUTA, nunca por sys.path: meter
# `preceptor/` entero en el path importaria de paso decenas de modulos que esta
# consola no usa, y varios se llaman igual que los de aqui (`estado`, `mensajes`).
# Es la misma decision, y por el mismo motivo, que ya tomo `ojo.py`.
METRICAS_PY = RAIZ / "preceptor" / "metricas.py"
# El Nexo SI necesita el path: sus sensores hacen `import sensores` entre ellos.
NEXO = RAIZ / "hexelion-nexo"
CACHE_REPOS = AQUI / "cache_repos.json"
CACHE_GATES = AQUI / "cache_gates.json"
# Ollama por loopback: escucha en `*:11434`, asi que 127.0.0.1 llega sin salir
# de la maquina. Preguntarle por la malla seria una sonda de red de verdad.
OLLAMA = "http://127.0.0.1:11434"
ESPERA_OLLAMA = 1.5
# Por encima de esto una cache deja de poder leerse como «lo que hay»: pasa a STALE.
RANCIO_S = 24 * 3600

VERSION_ALFABETO = "alfabeto-p0x@1.0.0"


# ---------------------------------------------------------------- la lectura

def ahora():
    return datetime.now().astimezone().isoformat(timespec="seconds")


def lectura(clave, valor, unidad, fuente, estado="MEDIDO", **extra):
    """Un dato con su procedencia y su hora. Sin las dos cosas es un rumor."""
    d = {"clave": clave, "estado": estado, "valor": valor, "unidad": unidad,
         "medido": ahora(), "fuente": fuente}
    d.update({k: v for k, v in extra.items() if v})
    return d


def hueco(clave, unidad, causa, fuente, detalle="", remedio="", nota=""):
    """La unica forma legitima de no tener dato: declararlo, con su motivo.

    `causa` es la frase que lee una persona. `detalle` es para quien depura. Van
    separados porque mezclarlos convierte la causa en jerga -- y una causa que
    acaba en «Error» no se distingue de una causa que nadie escribio.
    """
    return {"clave": clave, "estado": "NO_DATA", "valor": None, "unidad": unidad,
            "medido": ahora(), "fuente": fuente, "causa": causa,
            **({"detalle": detalle} if detalle else {}),
            **({"remedio": remedio} if remedio else {}),
            **({"nota": nota} if nota else {})}


# ------------------------------------------------------------ adaptadores

def de_metricas(d, clave=None, fuente="preceptor/metricas.py"):
    """Traduce una metrica del producto. Conserva MEDIDO frente a NORMA."""
    clave = clave or d.get("clave", "?")
    if d.get("estado") == "NO_DATA":
        return hueco(clave, d.get("unidad", ""), d.get("causa", "sin causa declarada"),
                     fuente, d.get("detalle", ""))
    return lectura(clave, d.get("valor"), d.get("unidad", ""),
                   d.get("como") or fuente,
                   estado="NORMA" if d.get("estado") == "NORMA" else "MEDIDO")


def de_nexo(clave, d, unidad="", campos=None, fuente="hexelion-nexo/sensores"):
    """Traduce una lectura del Nexo, que solo conoce `ok` y `NO_DATA`.

    `campos` recorta lo que viaja: el vector se inyecta en cada consulta, y un
    sensor entero -con su lista de aviones o su tabla de nodos- se come el
    presupuesto de tokens sin que nadie lo note hasta que el turno tarda.
    """
    if not isinstance(d, dict) or d.get("estado") != "ok":
        causa = (d or {}).get("causa") or "el sensor no devolvio una lectura"
        return hueco(clave, unidad, causa, fuente, (d or {}).get("detalle", ""))
    valor = {k: d[k] for k in (campos or []) if k in d} if campos else \
            {k: v for k, v in d.items() if k not in ("estado", "causa", "detalle", "medido")}
    return lectura(clave, valor, unidad, fuente)


# ------------------------------------------------------- fuentes de verdad

_metricas_cache = []


def _metricas():
    """El modulo de metricas, cargado por ruta y solo una vez por proceso."""
    if _metricas_cache:
        return _metricas_cache[0]
    if not METRICAS_PY.exists():
        return None
    import importlib.util
    spec = importlib.util.spec_from_file_location("p0x_metricas_vector", METRICAS_PY)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    _metricas_cache.append(mod)
    return mod


def _nexo(nombre):
    """Una lectura del registro del Nexo, o el hueco de por que no la hay."""
    try:
        if str(NEXO) not in sys.path:
            sys.path.insert(0, str(NEXO))
        from sensores import registro                      # noqa: PLC0415
        import sensores.adsb, sensores.jardin, sensores.nodos   # noqa: F401,PLC0415
        return registro.uno(nombre)
    except Exception as e:                                 # noqa: BLE001
        return {"estado": "NO_DATA",
                "causa": "el Nexo no se pudo cargar desde el Ojo",
                "detalle": type(e).__name__}


def _hwmon(nombre, etiqueta=None):
    """La temperatura de un chip por el NOMBRE de su hwmon, no por su numero.

    Los numeros de `/sys/class/hwmon/hwmonN` los reparte el kernel en el orden
    en que aparecen los drivers: fijar `hwmon3` funciona hasta el primer
    arranque en que no.
    """
    base = Path("/sys/class/hwmon")
    if not base.is_dir():
        return None
    for d in sorted(base.glob("hwmon*")):
        try:
            if (d / "name").read_text().strip() != nombre:
                continue
            for entrada in sorted(d.glob("temp*_input")):
                if etiqueta:
                    lbl = entrada.with_name(entrada.name.replace("_input", "_label"))
                    if not lbl.exists() or lbl.read_text().strip() != etiqueta:
                        continue
                return int(entrada.read_text().strip()) / 1000.0
        except (OSError, ValueError):
            continue
    return None


def _primero(patron):
    """El primer fichero que casa, leido entero. Para los contadores de la GPU."""
    for p in sorted(Path("/sys/class/drm").glob(patron)):
        try:
            return p.read_text().strip()
        except OSError:
            continue
    return None


def _cache(ruta, clave, unidad, remedio):
    """Una cache con su fecha. Rancia se declara STALE; no se calla ni se refresca sola."""
    if not ruta.exists():
        return hueco(clave, unidad, f"no hay cache en {ruta.name}", "cache local",
                     remedio=remedio)
    try:
        d = json.loads(ruta.read_text(encoding="utf-8"))
    except (OSError, ValueError) as e:
        return hueco(clave, unidad, f"{ruta.name} ilegible", "cache local",
                     f"{type(e).__name__}: {e}", remedio="revisar el JSON a mano")
    edad = time.time() - ruta.stat().st_mtime
    d2 = lectura(clave, d.get("valor", d), unidad, d.get("fuente", f"cache · {ruta.name}"))
    if edad > RANCIO_S:
        d2["estado"] = "STALE"
        d2["causa"] = f"la cache tiene {int(edad // 3600)} h · ya no es «lo que hay»"
        d2["remedio"] = remedio
    d2["medido"] = d.get("medido", d2["medido"])
    return d2


# -------------------------------------------------------------- secciones

def _salud_hardware(sondas, sin_red):
    m = _metricas()
    if m is not None:
        cpu = de_metricas(m._temperatura(), "cpu_temp_c")
        mem = {x["clave"]: x for x in m.memoria_del_sistema()}
    else:
        cpu = hueco("cpu_temp_c", "C", "no existe preceptor/metricas.py",
                    "preceptor/metricas.py",
                    remedio="el modulo de metricas vive en el repo del producto")
        mem = {}

    gpu_t = _hwmon("amdgpu", "edge")
    ocup = _primero("card*/device/gpu_busy_percent")
    vram_u = _primero("card*/device/mem_info_vram_used")
    vram_t = _primero("card*/device/mem_info_vram_total")

    nota_vram = ("carve-out de la misma DDR5 que usa la CPU, asi que estos bytes "
                 "YA estan contados en la RAM del sistema: no se suman")

    def _mem(clave, campo, unidad="MiB"):
        d = mem.get(campo)
        if d is None:
            return hueco(clave, unidad, "metricas.py no declara este campo",
                         "preceptor/metricas.py")
        return de_metricas(d, clave)

    soberano = {
        "cpu_temp_c": cpu,
        "gpu_temp_c": (lectura("gpu_temp_c", gpu_t, "C", "/sys hwmon amdgpu · edge")
                       if gpu_t is not None else
                       hueco("gpu_temp_c", "C", "no hay hwmon llamado amdgpu",
                             "/sys/class/hwmon")),
        "gpu_ocupacion_pct": (lectura("gpu_ocupacion_pct", int(ocup), "%",
                                      "/sys drm · gpu_busy_percent")
                              if ocup is not None else
                              hueco("gpu_ocupacion_pct", "%",
                                    "el driver no expone gpu_busy_percent", "/sys/class/drm")),
        "vram_usada_b": (lectura("vram_usada_b", int(vram_u), "B",
                                 "/sys drm · mem_info_vram_used", nota=nota_vram)
                         if vram_u is not None else
                         hueco("vram_usada_b", "B", "el driver no expone mem_info_vram_used",
                               "/sys/class/drm")),
        "vram_total_b": (lectura("vram_total_b", int(vram_t), "B",
                                 "/sys drm · mem_info_vram_total", nota=nota_vram)
                         if vram_t is not None else
                         hueco("vram_total_b", "B", "el driver no expone mem_info_vram_total",
                               "/sys/class/drm")),
        # `memoria_libre_mb` de metricas.py es MemAvailable, no MemFree: lo que de
        # verdad se puede pedir. Se renombra aqui y se conserva su `como`.
        "ram_disponible_mb": _mem("ram_disponible_mb", "memoria_libre_mb"),
        "ram_total_mb": _mem("ram_total_mb", "memoria_total_mb"),
        "carga_1m": lectura("carga_1m", round(os.getloadavg()[0], 2), "carga",
                            "/proc/loadavg"),
    }

    if sin_red:
        nodos = hueco("nodos", "nodos",
                      "el vector se pidio con la red cortada · los nodos remotos "
                      "no se preguntan, y no preguntarlos es la respuesta correcta",
                      "hexelion-nexo/sensores/nodos")
    else:
        sondas.append("nexo:nodos (tailscale local + gateway de la forja)")
        nodos = de_nexo("nodos", _nexo("nodos"), "nodos",
                        campos=("en_pie", "criticos", "fuente", "avisos"))
    return {"soberano": soberano, "nodos": nodos}


def _ambiental(sondas, sin_red):
    if sin_red:
        consumo = hueco("consumo_w", "W",
                        "el vector se pidio con la red cortada · el vatimetro "
                        "esta en la LAN", "Nous A1T")
    else:
        m = _metricas()
        if m is None:
            consumo = hueco("consumo_w", "W", "no existe preceptor/metricas.py",
                            "preceptor/metricas.py")
        else:
            sondas.append("enchufe:vatimetro (LAN)")
            consumo = de_metricas(m._consumo_w(), "consumo_w")

    jardin = _nexo("jardin") if not sin_red else None
    causa_jardin = ((jardin or {}).get("causa")
                    or "sin lector de sensores del jardin en este nodo")

    adsb = _nexo("adsb") if not sin_red else {"estado": "NO_DATA",
                                              "causa": "el vector se pidio con la red cortada"}
    if not sin_red:
        sondas.append("nexo:adsb (gateway de la forja)")

    def _adsb(clave, campo):
        if not isinstance(adsb, dict) or adsb.get("estado") != "ok":
            return hueco(clave, "aeronaves",
                         (adsb or {}).get("causa", "sin lectura de la antena"),
                         "hexelion-nexo/sensores/adsb", (adsb or {}).get("detalle", ""))
        return lectura(clave, adsb.get(campo), "aeronaves",
                       "hexelion-nexo/sensores/adsb")

    return {
        "consumo_w": consumo,
        # Este hueco no es una averia: es la frontera de lo que este rack sabe.
        "generacion_solar_w": hueco(
            "generacion_solar_w", "W",
            "nadie mide la generacion en este rack · el vatimetro mide lo que se "
            "GASTA, no de donde viene",
            "canon del nodo",
            remedio="un medidor del lado del panel, o un inversor que publique",
            nota="mientras esto sea NO_DATA, la regla «si solar > consumo, lanza "
                 "tarea pesada» NO es evaluable, y quien la aplique estara "
                 "estimando, no midiendo"),
        "co2_ppm": hueco("co2_ppm", "ppm", causa_jardin,
                         "hexelion-nexo/sensores/jardin"),
        "humedad_suelo_pct": hueco("humedad_suelo_pct", "%", causa_jardin,
                                   "hexelion-nexo/sensores/jardin"),
        "adsb_total": _adsb("adsb_total", "oidas"),
        "adsb_visibles": _adsb("adsb_visibles", "situadas"),
        "rs485": hueco("rs485", "lecturas",
                       "no hay ningun lector de RS485 en el repo · el bus solo "
                       "aparece nombrado en documentacion",
                       "barrido del repo",
                       remedio="si se cablea, el colector sale como propuesta en "
                               "p0x/propuestas/ -- no se aplica por SSH desde aqui"),
        # Ausencia DECLARADA, que no es lo mismo que un sensor que falla: se sabe
        # donde esta y por que no habla.
        "esp32": hueco("esp32", "lecturas",
                       "retirado de los dispositivos · pendiente de reconexion",
                       "declarado por el Soberano el 2026-09-06",
                       remedio="al reconectarlo, actualizar recursos.json del Ojo"),
        "camara": hueco("camara", "fotogramas",
                        "retirada de los dispositivos · pendiente de reconexion",
                        "declarado por el Soberano el 2026-09-06",
                        remedio="al reconectarla, actualizar recursos.json del Ojo"),
    }


def _ecosistema(sondas, sin_red):
    if sin_red:
        inst = hueco("modelos_instalados", "modelos",
                     "el vector se pidio con la red cortada · ni el loopback",
                     "ollama")
        carg = hueco("modelos_cargados", "modelos",
                     "el vector se pidio con la red cortada · ni el loopback", "ollama")
        pelados = hueco("tags_pelados", "tags",
                        "sin lista de modelos no hay tags que contar", "ollama")
        backend = hueco("backend", "backend",
                        "sin lista de modelos cargados no se puede demostrar el backend",
                        "ollama")
    else:
        sondas.append("ollama:/api/tags (loopback)")
        try:
            with urllib.request.urlopen(f"{OLLAMA}/api/tags",
                                        timeout=ESPERA_OLLAMA) as r:
                nombres = sorted(m["name"] for m in
                                 json.loads(r.read().decode("utf-8"))["models"])
            inst = lectura("modelos_instalados", nombres, "modelos",
                           "ollama /api/tags")
            sueltos = [n for n in nombres if n.endswith(":latest")]
            pelados = lectura("tags_pelados", sueltos, "tags", "ollama /api/tags",
                              nota="apuntan a variantes Thinking con razonamiento "
                                   "no desactivable")
        except Exception as e:                             # noqa: BLE001
            inst = hueco("modelos_instalados", "modelos", "Ollama no contesta por loopback",
                         "ollama /api/tags", type(e).__name__)
            pelados = hueco("tags_pelados", "tags", "sin lista de modelos no hay "
                            "tags que contar", "ollama /api/tags")

        sondas.append("ollama:/api/ps (loopback)")
        try:
            with urllib.request.urlopen(f"{OLLAMA}/api/ps",
                                        timeout=ESPERA_OLLAMA) as r:
                vivos = json.loads(r.read().decode("utf-8")).get("models", [])
            carg = lectura("modelos_cargados",
                           [{"nombre": v.get("name"),
                             "hasta": v.get("expires_at", "")[:19]} for v in vivos],
                           "modelos", "ollama /api/ps")
            if vivos:
                backend = lectura("backend",
                                  vivos[0].get("details", {}).get("family", "") or "cargado",
                                  "backend", "ollama /api/ps")
            else:
                # No se hereda de la sesion anterior: Vulkan puede caerse entre
                # arranques segun el drop-in, y suponerlo es como no medirlo.
                backend = hueco("backend", "backend",
                                "ningun modelo cargado · sin uno cargado no hay "
                                "backend que demostrar",
                                "ollama /api/ps",
                                remedio="cargar un modelo y volver a preguntar")
        except Exception as e:                             # noqa: BLE001
            carg = hueco("modelos_cargados", "modelos", "Ollama no contesta por loopback",
                         "ollama /api/ps", type(e).__name__)
            backend = hueco("backend", "backend", "sin lista de cargados no se puede "
                            "demostrar el backend", "ollama /api/ps")

    return {
        "modelos_instalados": inst,
        "modelos_cargados": carg,
        "tags_pelados": pelados,
        "backend": backend,
        # GitHub NO se llama al construir el vector: seria una sonda a la nube en
        # el arranque de cada consulta, en un sistema que existe para no depender
        # de la nube.
        "repos": _cache(CACHE_REPOS, "repos", "repos",
                        "python3 ojo/vector.py --refrescar-repos"),
        "gates": _cache(CACHE_GATES, "gates", "gates",
                        "correr los gates y escribir cache_gates.json"),
    }


def _usuario():
    """Solo de artefactos declarados. Lo que no este, hueco -- no se deduce.

    La ubicacion es dato personal: grano de ciudad como mucho, y no sale de esta
    maquina. Por eso tampoco se adivina de una IP ni de un perfil publico.
    """
    return {
        "idioma": lectura("idioma", "es", "idioma", "canon del nodo · CLAUDE.md",
                          estado="NORMA",
                          nota="doctrina, reportes y commits en español; la UI de "
                               "herramientas que lo pidan, en ingles"),
        "modo_respuesta": lectura("modo_respuesta", "parar-y-reportar", "modo",
                                  "canon del nodo · CLAUDE.md", estado="NORMA"),
        "ubicacion_aprox": hueco("ubicacion_aprox", "ciudad",
                                 "ningun artefacto local la declara",
                                 "Alejandria/identidad_publica.json",
                                 remedio="añadir `ciudad` a identidad_publica.json "
                                         "si se quiere que el vector la lleve"),
    }


# ------------------------------------------------------------------ armado

def construir(sin_red=False):
    t0 = time.monotonic()
    sondas = []
    v = {
        "esquema": 1,
        "generado": ahora(),
        "presupuesto": {"sin_red": bool(sin_red), "sondas": sondas, "ms": 0},
        "salud_hardware": _salud_hardware(sondas, sin_red),
        "instantanea_ambiental": _ambiental(sondas, sin_red),
        "estado_ecosistema": _ecosistema(sondas, sin_red),
        "contexto_usuario": _usuario(),
    }
    v["presupuesto"]["ms"] = round((time.monotonic() - t0) * 1000, 1)
    return v


# El unico sitio donde las dos lenguas se tocan. Si esta tabla se bifurca,
# el rack acaba con dos palabras para el mismo hueco y ninguna manda.
A_ALFABETO = {"MEDIDO": "ok", "NORMA": "ok", "NO_DATA": "sin_dato", "STALE": "stale"}


def _resumen_repos(valor):
    """Nueve repos con nombre, visibilidad y archivado cuestan 175 tokens MEDIDOS.

    Alfabeto §4: lo que ya existe se referencia, no se retransmite -- el receptor
    lo trae por lectura local si lo necesita. Para decidir quien contesta una
    consulta importa el recuento, no la lista; la lista sigue entera en el vector
    de esta maquina, que es donde se puede leer sin pagar cable.
    """
    if not isinstance(valor, list):
        return valor
    return {"n": len(valor),
            "pub": sum(1 for r in valor if r.get("vis") == "PUBLIC"),
            "priv": sum(1 for r in valor if r.get("vis") == "PRIVATE"),
            "arch": sum(1 for r in valor if r.get("arch"))}


# Lo que viaja resumido, con su motivo medido en el docstring de cada uno. Es una
# lista corta y explicita a proposito: un resumen automatico por tamaño acabaria
# recortando el dia que importe, y sin avisar.
RESUMEN_EN_EL_CABLE = {"repos": _resumen_repos}


def a_alfabeto(v):
    """El vector en el sobre del Alfabeto P0X §3, para hablar con otro silicio.

    `NORMA` no tiene palabra en el lexico §2 -- hay `ok`, `sin_dato`, `stale`,
    `degradado` y `caido`, y ninguna significa «declarado pero no medido». Se
    traduce a `ok` conservando `norma: true`, para no perder la distincion, y la
    falta queda propuesta como enmienda: un ID nuevo entra por la ZONA EVOLUTIVA
    y lo firma el carbono, no este fichero.
    """
    def trad(d):
        if isinstance(d, dict) and "estado" in d and "clave" in d:
            fuera = {"e": A_ALFABETO.get(d["estado"], "sin_dato")}
            if d["estado"] == "NORMA":
                fuera["norma"] = True
            if d["valor"] is not None:
                resumir = RESUMEN_EN_EL_CABLE.get(d["clave"])
                fuera["v"] = resumir(d["valor"]) if resumir else d["valor"]
            if d.get("causa"):
                fuera["c"] = d["causa"]
            return fuera
        if isinstance(d, dict):
            return {k: trad(x) for k, x in d.items()}
        return d

    return {
        "v": VERSION_ALFABETO,
        "md": "vector-soberano@1",
        "dom": "telemetria",
        "op": "telemetria",
        "in": {k: trad(v[k]) for k in ("salud_hardware", "instantanea_ambiental",
                                       "estado_ecosistema", "contexto_usuario")},
        "out": "ack",
    }


def validar(v):
    """Contra el esquema. Devuelve [] si valida, o la lista de fallos."""
    try:
        import jsonschema                                  # noqa: PLC0415
    except ImportError:
        return ["jsonschema no esta instalado · sin el no hay validacion, y sin "
                "validacion esto no es un vector, es un diccionario"]
    esquema = json.loads(ESQUEMA.read_text(encoding="utf-8"))
    val = jsonschema.Draft202012Validator(esquema)
    return [f"{'/'.join(str(p) for p in e.path)}: {e.message}"
            for e in val.iter_errors(v)]


def resumen(v):
    """Las cifras que un humano quiere de un vistazo, y cuantos huecos hay."""
    huecos, total = [], 0
    def anda(d, ruta=""):
        nonlocal total
        if isinstance(d, dict) and "estado" in d and "clave" in d:
            total += 1
            if d["estado"] == "NO_DATA":
                huecos.append(ruta)
            return
        if isinstance(d, dict):
            for k, x in d.items():
                anda(x, f"{ruta}.{k}" if ruta else k)
    for k in ("salud_hardware", "instantanea_ambiental", "estado_ecosistema",
              "contexto_usuario"):
        anda(v[k], k)
    return {"lecturas": total, "huecos": len(huecos), "cuales": huecos}


def refrescar_repos():
    """La UNICA puerta por la que este modulo habla con GitHub, y es a mano.

    Vive fuera de `construir()` a proposito: llamar a la nube en el arranque de
    cada consulta seria pagar latencia -y dependencia- en un sistema que existe
    justamente para no tenerla. Aqui se pide, se escribe con su fecha, y el
    vector lo lee de disco sabiendo cuando se midio.
    """
    import subprocess                                      # noqa: PLC0415
    try:
        salida = subprocess.run(
            ["gh", "repo", "list", "--limit", "50", "--json",
             "name,visibility,isArchived"],
            capture_output=True, text=True, timeout=30, check=True).stdout
        repos = [{"n": r["name"], "vis": r["visibility"],
                  "arch": r["isArchived"]} for r in json.loads(salida)]
    except FileNotFoundError:
        return "no hay `gh` en el PATH"
    except subprocess.CalledProcessError as e:
        return f"gh fallo: {(e.stderr or '').strip()[:120]}"
    except Exception as e:                                 # noqa: BLE001
        return f"{type(e).__name__} pidiendo la lista a GitHub"
    CACHE_REPOS.write_text(json.dumps(
        {"valor": repos, "medido": ahora(), "fuente": "gh repo list"},
        ensure_ascii=False, indent=1), encoding="utf-8")
    return ""


def main(argv=None):
    argv = list(sys.argv[1:] if argv is None else argv)

    if "--refrescar-repos" in argv:
        fallo = refrescar_repos()
        if fallo:
            print("no se refresco:", fallo, file=sys.stderr)
            return 1
        print(f"cache de repos escrita en {CACHE_REPOS.name}")
        return 0

    sin_red = "--sin-red" in argv
    v = construir(sin_red=sin_red)

    if "--alfabeto" in argv:
        print(json.dumps(a_alfabeto(v), ensure_ascii=False, indent=1))
        return 0
    if "--resumen" in argv:
        r = resumen(v)
        print(f"{r['lecturas']} lecturas · {r['huecos']} huecos · "
              f"{v['presupuesto']['ms']} ms · {len(v['presupuesto']['sondas'])} sondas")
        for c in r["cuales"]:
            print("  hueco:", c)
        return 0

    fallos = validar(v) if "--validar" in argv else []
    print(json.dumps(v, ensure_ascii=False, indent=1))
    if fallos:
        print("\nNO VALIDA:", file=sys.stderr)
        for f in fallos:
            print("  ·", f, file=sys.stderr)
        return 1
    if "--validar" in argv:
        print("\nvalida contra esquema_vector.json", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
