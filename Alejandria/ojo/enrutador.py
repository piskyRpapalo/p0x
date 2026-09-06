#!/usr/bin/env python3
"""El enrutador del Ojo: quien contesta, con que contrato y con que datos delante.

DETERMINISTA A PROPOSITO
------------------------
No hay red neuronal decidiendo quien decide. Un clasificador que elige experto
es una caja que no se puede auditar cuando se equivoca, y aqui la eleccion tiene
que poder explicarse con una frase: «fue al fisico porque la consulta dijo
`entrenar` y el vector dice que quedan 32 GB». Reglas + estado, y el motivo
viaja siempre en la respuesta.

LOS EXPERTOS NO SE INVENTAN AQUI
--------------------------------
Ya existen como artefactos firmados y versionados en `mente/`. La Orquesta §2.2
es explicita: la IA interna consume MDs RENDERIZADOS (`md_id@version`), jamas
prompts sueltos, y si la version no cuadra se aborta. Asi que este fichero no
lleva ni un prompt de personalidad dentro: lee el contrato del disco, comprueba
su ancla de version y lo renderiza. Si alguien edita `monje.md`, cambia el
comportamiento del experto y NO hay que tocar codigo.

EL CONTRATO DE DATOS DEL TURNO, Y POR QUE HACE FALTA
----------------------------------------------------
Las voces del Sinodo traen su propia lista blanca -- claves de Redis y
colecciones de Qdrant que sirve La Torre--. Este nodo no sirve ninguna de esas
claves: lo que tiene delante es el Vector de Estado Soberano. Renderizar la voz
tal cual y alimentarla con otra cosa seria pedirle que cite lo que no le hemos
dado, que es la forma mas rapida de fabricar una invencion.

Por eso el turno añade su propio contrato, marcado y aparte: **para este turno,
la lista blanca es el vector**. La voz se renderiza intacta -- no se reescribe
un artefacto firmado desde el codigo-- y la diferencia queda declarada.

EL GROUNDING SE COMPRUEBA, NO SE PIDE POR FAVOR
-----------------------------------------------
La salida viene acotada por esquema (`format` de Ollama) y trae `apoyado_en`:
las claves del vector en las que se apoya. Despues se comprueba que esas claves
EXISTAN de verdad. Un modelo que cita `instantanea_ambiental.generacion_solar_w`
como si tuviera valor queda cazado por la maquina, no por quien lea.
"""

import json
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path

AQUI = Path(__file__).resolve().parent
if str(AQUI) not in sys.path:
    sys.path.insert(0, str(AQUI))

import vector as V                                          # noqa: E402

MENTE = V.RAIZ / "mente"
OLLAMA = V.OLLAMA
ESPERA = 600          # el 30B en este metal genera despacio; el techo es generoso a proposito

# Cada experto es (contrato en disco, ancla de version, modelo, señales). El
# ancla se comprueba contra el front-matter: si el artefacto cambia de version
# sin que nadie mire, esto aborta en vez de servir un contrato que ya no es.
EXPERTOS = {
    "edge-ai": {
        "titulo": "Edge-AI · el metal y lo que corre en el",
        "contrato": MENTE / "esferas" / "edge-ai.md",
        "ancla": ("firmado", "2026-07-12"),
        "modelo": "qwen3-coder:30b",
        "por_defecto": True,
        "señales": ("codigo", "script", "python", "systemd", "servicio", "puerto",
                    "instalar", "compilar", "bench", "ollama", "modelo", "contexto",
                    "num_ctx", "vulkan", "cuantiza", "refactor", "test", "gate"),
    },
    "codice": {
        "titulo": "El Escriba · doctrina, memoria y lo que esta firmado",
        "contrato": MENTE / "voces" / "escriba.md",
        "ancla": ("version", "1.2.0"),
        "modelo": "preceptor-cazanido-v3:llama3.2",
        "por_defecto": False,
        "señales": ("doctrina", "canon", "ironclaw", "regla", "norma", "firma",
                    "propose-only", "glosario", "alfabeto", "memoria", "esfera",
                    "voz", "artefacto", "quien decide", "permitido", "prohibido"),
    },
    "fisico": {
        "titulo": "El Monje · termodinamica, energia y sensores",
        "contrato": MENTE / "voces" / "monje.md",
        "ancla": ("version", "1.3.0"),
        # MEDIDO el 2026-09-06 sobre el mismo turno compuesto: `llama3.2:3b`
        # devuelve `apoyado_en` VACIO y se agarra al unico hueco; `qwen3:4b` con
        # el razonamiento apagado cita las cinco claves del dictamen. Cuesta
        # 15,4 s frente a 3,7 s, y ese es el precio de que la respuesta este
        # agarrada a algo. Tag explicito: nunca `:latest`.
        "modelo": "qwen3:4b",
        "por_defecto": False,
        "señales": ("consumo", "vatio", "watt", "temperatura", "termica", "calor",
                    "solar", "energia", "bateria", "ups", "entrenar", "lora",
                    "afinar", "gpu", "ram", "memoria libre", "ventilador", "co2",
                    "humedad", "sensor", "adsb", "aviones", "carga", "pesada"),
    },
}

# Lo que el modelo puede devolver, y nada mas. Va tal cual al `format` de Ollama.
ESQUEMA_SALIDA = {
    "type": "object",
    "additionalProperties": False,
    "required": ["respuesta", "apoyado_en", "sin_dato"],
    "properties": {
        "respuesta": {"type": "string"},
        "apoyado_en": {"type": "array", "items": {"type": "string"},
                       "description": "claves del vector en las que se apoya"},
        "sin_dato": {"type": "array", "items": {"type": "string"},
                     "description": "lo que haria falta y no esta"},
        "confianza": {"enum": ["alta", "media", "baja"]},
    },
}


# ------------------------------------------------------- dictamen previo

# Umbral DECLARADO, no medido: por debajo de esto no cabe holgadamente ni la
# forja por CPU ni un modelo mediano al lado. Sale de que el 30B instalado ocupa
# 18,6 GB; nadie ha medido el pico real de una forja, y hasta que se mida esto es
# una norma con procedencia, no una medida.
RAM_HOLGADA_MIB = 16384


def dictamen_fisico(v):
    """El veredicto que NO necesita modelo: aritmetica sobre lo medido.

    Regla de oro §3 -- si es determinista, se ejecuta directo. Preguntar a un
    LLM si 32.747 MiB son mas que 16.384 es pagar tokens por una comparacion, y
    ademas abre una superficie de invencion donde no hacia falta ninguna.

    El modelo, si se le llama, REDACTA este dictamen. No lo calcula.
    """
    r = _rutas(v)
    apoyos, contras, faltan = [], [], []

    def dato(ruta):
        d = r.get(ruta)
        if not d or d["estado"] == "NO_DATA":
            faltan.append(ruta)
            return None
        apoyos.append(ruta)
        return d["valor"]

    ram = dato("salud_hardware.soberano.ram_disponible_mb")
    carga = dato("salud_hardware.soberano.carga_1m")
    temp = dato("salud_hardware.soberano.cpu_temp_c")
    vatios = dato("instantanea_ambiental.consumo_w")
    cargados = dato("estado_ecosistema.modelos_cargados")
    # Se cita a proposito aunque sea un hueco: es la frontera de la respuesta.
    solar = r.get("instantanea_ambiental.generacion_solar_w")
    if solar and solar["estado"] == "NO_DATA":
        faltan.append("instantanea_ambiental.generacion_solar_w")

    if ram is None:
        return {"veredicto": "no se puede saber", "apoyado_en": apoyos,
                "sin_dato": faltan,
                "motivos": ["sin la RAM disponible no hay respuesta: es la cifra "
                            "que decide"]}

    if ram < RAM_HOLGADA_MIB:
        contras.append(f"quedan {ram} MiB libres, por debajo de los "
                       f"{RAM_HOLGADA_MIB} que esta consola declara holgados")
    if carga is not None and carga > 4:
        contras.append(f"la carga de 1 min es {carga}: el metal ya esta ocupado")
    if temp is not None and temp > 80:
        contras.append(f"la CPU esta a {temp} C antes de empezar")
    if cargados:
        contras.append("hay modelo(s) cargado(s) en Ollama disputando la misma "
                       "DDR5: " + ", ".join(m.get("nombre", "?") for m in cargados))

    motivos = [f"RAM disponible {ram} MiB"]
    if temp is not None:
        motivos.append(f"CPU a {temp} C")
    if carga is not None:
        motivos.append(f"carga 1 min {carga}")
    if vatios is not None:
        motivos.append(f"el rack esta consumiendo {vatios} W")
    motivos.append("la regla «si solar > consumo, lanza tarea pesada» NO es "
                   "evaluable: nadie mide la generacion en este rack")

    return {"veredicto": "no" if ram < RAM_HOLGADA_MIB else
                         ("si, con reservas" if contras else "si"),
            "apoyado_en": apoyos, "sin_dato": faltan,
            "motivos": motivos + [f"reserva: {c}" for c in contras]}


DICTAMENES = {"fisico": dictamen_fisico}


# ------------------------------------------------------------- contratos

def _frontmatter(texto):
    if not texto.startswith("---"):
        return {}, texto
    partes = texto.split("---", 2)
    if len(partes) < 3:
        return {}, texto
    fm = {}
    for linea in partes[1].splitlines():
        m = re.match(r"^([a-z_]+):\s*(.+?)\s*$", linea)
        if m:
            fm[m.group(1)] = m.group(2).strip().strip('"')
    return fm, partes[2]


def contrato(experto_id):
    """El contrato renderizado, o el motivo exacto por el que no se puede servir.

    Protocolo §4.5: version que no cuadra, aborta. No se sirve «lo que haya»:
    un experto con un contrato distinto del que dice tener es un experto que
    nadie ha revisado.
    """
    e = EXPERTOS[experto_id]
    if not e["contrato"].exists():
        return None, f"no existe {e['contrato'].name} · sin contrato no hay experto"
    texto = e["contrato"].read_text(encoding="utf-8")
    fm, cuerpo = _frontmatter(texto)
    campo, esperado = e["ancla"]
    visto = fm.get(campo)
    if visto != esperado:
        return None, (f"{e['contrato'].name} declara {campo} {visto!r} y el enrutador "
                      f"ancla en {esperado!r} · se aborta en vez de servir un contrato "
                      "que ya no es el revisado")
    return cuerpo.strip(), ""


def _sustituye_contrato_de_datos(cuerpo, turno):
    """Cambia la lista blanca de la voz por la de este turno, y lo DECLARA.

    MEDIDO, no supuesto. La primera version renderizaba la voz entera y añadia
    el contrato del turno debajo. El Monje contesto citando
    `/api/health/nodes` y `/api/telemetry/m5` -- claves de SU lista blanca, que
    las sirve La Torre y que este nodo no tiene-- y el gate de grounding lo
    caza. Un modelo de 3B obedece la lista que ve primero, y la de la voz venia
    antes y mas detallada.

    Sustituir no es reescribir el artefacto: en disco `monje.md` sigue intacto y
    firmado. Lo que cambia es el RENDER de este turno, y el plan lo dice en
    `sustituciones` para que nadie crea que el experto lleva su contrato entero.
    """
    lineas, fuera, dentro, hecho, ejemplos = cuerpo.splitlines(), [], False, False, 0
    for ln in lineas:
        if ln.startswith("## "):
            dentro = ln.upper().startswith("## CONTRATO DE DATOS")
            if dentro:
                fuera.append(turno.strip())
                hecho = True
                continue
        if dentro:
            continue
        # Los few-shot de la ZONA EVOLUTIVA citan las claves de La Torre («R:
        # Soberano, `hexelion:telemetry:m5:last` esta viva pero...»), y un
        # ejemplo pesa mas que una regla: era de ahi de donde el modelo sacaba
        # las rutas de API que se inventaba. Se retira el ejemplo, no la voz --
        # el arquetipo, el mantra y el tono siguen.
        if ln.lstrip().startswith(("P:", "R:")):
            ejemplos += 1
            continue
        fuera.append(ln)
    return "\n".join(fuera).strip(), (hecho, ejemplos)


# -------------------------------------------------------------- eleccion

def _normaliza(texto):
    tabla = str.maketrans("áéíóúüñ", "aeiouun")
    return texto.lower().translate(tabla)


def elegir(consulta, v):
    """El experto, y el motivo con nombre y apellidos.

    La esfera `edge-ai` es la titular por decision del Soberano: cuando nada
    tira mas fuerte hacia otro lado, contesta el metal.
    """
    texto = _normaliza(consulta)
    marcador = {}
    for eid, e in EXPERTOS.items():
        vistas = [s for s in e["señales"] if _normaliza(s) in texto]
        if vistas:
            marcador[eid] = vistas

    if not marcador:
        eid = next(k for k, e in EXPERTOS.items() if e["por_defecto"])
        return eid, ["ninguna señal reconocida · contesta el titular (edge-ai)"], marcador
    eid = max(marcador, key=lambda k: (len(marcador[k]),
                                       EXPERTOS[k]["por_defecto"]))
    motivo = [f"señales de «{eid}»: " + ", ".join(marcador[eid])]
    otros = {k: vs for k, vs in marcador.items() if k != eid}
    if otros:
        motivo.append("tambien sonaron: " + " · ".join(
            f"{k} ({len(vs)})" for k, vs in otros.items()))
    return eid, motivo, marcador


def veto_del_estado(eid, v):
    """Lo que el estado del rack tiene que decir ANTES de elegir modelo.

    No bloquea: avisa con dato. Un enrutador que manda una consulta a un 30B que
    no esta cargado sin decir lo que cuesta hace esperar diez minutos a alguien
    que habria preferido otra cosa.
    """
    avisos = []
    modelo = EXPERTOS[eid]["modelo"]
    inst = v["estado_ecosistema"]["modelos_instalados"]
    carg = v["estado_ecosistema"]["modelos_cargados"]

    if inst["estado"] == "NO_DATA":
        avisos.append("no se pudo listar Ollama · no se sabe si el modelo esta instalado")
    elif modelo not in (inst["valor"] or []):
        avisos.append(f"{modelo} NO esta instalado en este nodo")

    cargados = [m.get("nombre") for m in (carg["valor"] or [])] \
        if carg["estado"] != "NO_DATA" else []
    if cargados and modelo not in cargados:
        ram = v["salud_hardware"]["soberano"]["ram_disponible_mb"]
        libre = f"{ram['valor']} MiB libres" if ram["estado"] != "NO_DATA" else "RAM sin medir"
        avisos.append(f"{modelo} no esta cargado · cargarlo cuesta tiempo de pared ({libre})")
    return avisos


# --------------------------------------------------------------- armado

CONTRATO_DEL_TURNO = """
## CONTRATO DE DATOS DE ESTE TURNO (manda sobre la lista blanca de arriba)
Este turno NO corre en La Torre y no tiene delante ni Redis ni Qdrant. La unica
fuente permitida es el VECTOR DE ESTADO SOBERANO que viene abajo.

1. Cita solo claves que esten en el vector, con su ruta completa.
2. Una clave con `estado: NO_DATA` NO tiene valor. Decir su numero es inventarlo.
3. `NORMA` es declarado por alguien, no medido: no lo presentes como medida.
4. Si falta lo que haria falta para contestar, dilo en `sin_dato` y responde con
   lo que si hay. «No se puede saber con esto» es una respuesta correcta.
5. En `apoyado_en` van las rutas exactas que has usado. Se comprueban.

## LAS UNICAS RUTAS QUE EXISTEN
Cualquier otra cosa que escribas en `apoyado_en` sera rechazada por la maquina.
{rutas}
"""


def componer(consulta, v, eid=None):
    """La peticion entera, SIN llamar a nadie. Asi se puede probar sin red."""
    if eid is None:
        eid, motivo, marcador = elegir(consulta, v)
    else:
        motivo, marcador = [f"experto forzado a mano: {eid}"], {}
    cuerpo, fallo = contrato(eid)
    e = EXPERTOS[eid]
    # No se puede pedir que cite de una lista que nunca se le enseño. La primera
    # version pedia «rutas exactas» y solo mandaba el JSON anidado con claves
    # cortas: el modelo se invento `/api/health/models` imitando el ESTILO del
    # contrato de la voz. Las rutas van explicitas, con su estado al lado para
    # que un hueco se vea antes de citarlo.
    catalogo = "\n".join(
        f"- {r} [{d['estado']}]" for r, d in sorted(_rutas(v).items()))
    turno = CONTRATO_DEL_TURNO.replace("{rutas}", catalogo)

    sustituciones = []
    if cuerpo:
        cuerpo, (cambiado, ejemplos) = _sustituye_contrato_de_datos(cuerpo, turno)
        sustituciones.append(
            "CONTRATO DE DATOS de la voz -> contrato de este turno (el vector)"
            if cambiado else
            "el contrato no declara lista blanca propia · se añade la del turno")
        if ejemplos:
            sustituciones.append(
                f"retirados {ejemplos} ejemplos P:/R: que citaban claves de otro nodo")
        sistema = cuerpo if cambiado else cuerpo + "\n" + turno
    else:
        sistema = ""
    sobre = V.a_alfabeto(v)
    previo = DICTAMENES[eid](v) if eid in DICTAMENES else None
    prompt = ("[SYSTEM CONTEXT · vector de estado soberano]\n"
              + json.dumps(sobre["in"], ensure_ascii=False, separators=(",", ":"))
              + (("\n\n[DICTAMEN YA CALCULADO · no lo recalcules, REDACTALO]\n"
                  + json.dumps(previo, ensure_ascii=False)) if previo else "")
              + "\n\n[CONSULTA]\n" + consulta)
    return {
        "experto": eid,
        "titulo": e["titulo"],
        "contrato": f"{e['contrato'].name}@{e['ancla'][1]}",
        "contrato_ok": not fallo,
        "sustituciones": sustituciones,
        "fallo_contrato": fallo,
        "modelo": e["modelo"],
        "motivo": motivo,
        "señales": marcador,
        "avisos_del_estado": veto_del_estado(eid, v),
        "dictamen": previo,
        "peticion": {"model": e["modelo"], "system": sistema, "prompt": prompt,
                     "stream": False, "format": ESQUEMA_SALIDA,
                     "options": {"temperature": 0},
                     # El razonamiento va ENCENDIDO por defecto en la familia
                     # qwen3, y en un bucle eso es tiempo de pared invisible.
                     **({"think": False} if e["modelo"].startswith("qwen3") else {})},
    }


# ------------------------------------------------------------- ejecucion

def _rutas(v):
    """Todas las rutas de lectura del vector, para comprobar los apoyos."""
    fuera = {}
    def anda(d, p=""):
        if isinstance(d, dict) and "clave" in d and "estado" in d:
            fuera[p] = d
        elif isinstance(d, dict):
            for k, x in d.items():
                anda(x, f"{p}.{k}" if p else k)
    for k in ("salud_hardware", "instantanea_ambiental", "estado_ecosistema",
              "contexto_usuario"):
        anda(v[k], k)
    return fuera


def comprobar_apoyos(salida, v):
    """Que lo citado exista, y que no se cite un hueco como si tuviera valor.

    Es el gate de grounding, y es mecanico: no depende de que alguien lea la
    respuesta con atencion.
    """
    rutas = _rutas(v)
    fallos = []
    for ruta in salida.get("apoyado_en", []):
        limpia = ruta.strip().lstrip("`").rstrip("`")
        coincide = [r for r in rutas if r == limpia or r.endswith("." + limpia)]
        if not coincide:
            fallos.append(f"cita «{ruta}», que no es una clave del vector")
            continue
        d = rutas[coincide[0]]
        if d["estado"] == "NO_DATA":
            fallos.append(f"se apoya en «{ruta}», que es un hueco declarado")
    return fallos


def preguntar(peticion):
    """Una llamada, sin reintento silencioso. Un fallo se cuenta (Alfabeto §3)."""
    cuerpo = json.dumps(peticion).encode("utf-8")
    req = urllib.request.Request(f"{OLLAMA}/api/generate", cuerpo,
                                 {"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=ESPERA) as r:
        d = json.loads(r.read().decode("utf-8"))
    return d


def responder(consulta, v=None, ejecutar=False):
    v = v if v is not None else V.construir()
    plan = componer(consulta, v)
    if not ejecutar:
        return plan, None
    if not plan["contrato_ok"]:
        return plan, {"error": plan["fallo_contrato"]}
    try:
        bruto = preguntar(plan["peticion"])
    except Exception as e:                                  # noqa: BLE001
        return plan, {"error": f"el motor local no contesto: {type(e).__name__}"}
    try:
        salida = json.loads(bruto.get("response", ""))
    except ValueError:
        return plan, {"error": "la salida no es JSON pese al esquema · fallo contado, "
                               "no se reintenta en silencio",
                      "bruto": bruto.get("response", "")[:400]}
    salida["_grounding"] = comprobar_apoyos(salida, v)
    # MEDIDO tres veces con llama3.2:3b sobre «¿puedo entrenar un LoRA ahora?»:
    # el dictamen determinista cita cuatro claves medidas y el modelo devuelve
    # `apoyado_en` vacio y se agarra al unico hueco. Servir eso como respuesta
    # seria cambiar un veredicto auditable por uno peor, asi que se dice.
    d = plan.get("dictamen")
    if d and len(salida.get("apoyado_en", [])) < len(d["apoyado_en"]):
        salida["_aporta"] = (
            f"el modelo se apoya en {len(salida.get('apoyado_en', []))} claves y el "
            f"dictamen determinista en {len(d['apoyado_en'])}: manda el dictamen")
    salida["_tokens"] = {"prompt": bruto.get("prompt_eval_count"),
                         "salida": bruto.get("eval_count"),
                         "ms": round(bruto.get("total_duration", 0) / 1e6)}
    return plan, salida


def main(argv=None):
    argv = list(sys.argv[1:] if argv is None else argv)
    ejecutar = "--ejecutar" in argv
    consulta = " ".join(a for a in argv if not a.startswith("--")) \
        or "¿Puedo entrenar un LoRA ahora?"

    v = V.construir()
    plan, salida = responder(consulta, v, ejecutar=ejecutar)

    print(f"CONSULTA   {consulta}")
    print(f"EXPERTO    {plan['experto']} · {plan['titulo']}")
    print(f"CONTRATO   {plan['contrato']}  {'ok' if plan['contrato_ok'] else plan['fallo_contrato']}")
    print(f"MODELO     {plan['modelo']}")
    for m in plan["motivo"]:
        print(f"MOTIVO     {m}")
    for x in plan["sustituciones"]:
        print(f"RENDER     {x}")
    for a in plan["avisos_del_estado"]:
        print(f"AVISO      {a}")
    if plan.get("dictamen"):
        d = plan["dictamen"]
        print(f"\nDICTAMEN   {d['veredicto']}   (determinista, sin modelo)")
        for m in d["motivos"]:
            print(f"  · {m}")
        for f in d["sin_dato"]:
            print(f"  hueco: {f}")
    peticion = plan["peticion"]
    print(f"PROMPT     {len(peticion['system'])} B de contrato + "
          f"{len(peticion['prompt'])} B de vector y consulta")

    if salida is None:
        print("\n(sin --ejecutar no se llama al modelo: esto es el plan del turno)")
        return 0
    if "error" in salida:
        print("\nFALLO:", salida["error"])
        return 1
    if plan.get("dictamen"):
        print("\n(el veredicto es el DICTAMEN de arriba · lo de abajo es como lo "
              "redacta el modelo, y no manda)")
    print("\nRESPUESTA  " + salida.get("respuesta", ""))
    print("APOYADO EN " + ", ".join(salida.get("apoyado_en", [])))
    print("SIN DATO   " + ", ".join(salida.get("sin_dato", [])))
    if salida["_grounding"]:
        print("\nGROUNDING ROTO:")
        for f in salida["_grounding"]:
            print("  ·", f)
        return 1
    print("GROUNDING  ok · todo lo citado existe y ninguno es un hueco")
    if salida.get("_aporta"):
        print("APORTE     " + salida["_aporta"])
    print(f"COSTE      {salida['_tokens']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
