#!/usr/bin/env python3
"""El Enlace: traduce el estado del rack a palabras. En pantalla, «El Enlace dice».

LA VOZ
------
Sale de `mente/voces/enlace.md`: Jano, dios de los umbrales. *«Ninguna puerta se
abre sin la palabra del Soberano.»* Sintetiza, no enumera. Se dirige al humano
como Soberano. **Jamas ejecuta.** Y su grounding es literal: si una fuente no
reporto dato, se dice -- «ausencia no es cero», y *«no lo se con los datos que
tengo» es correcto y deseable*.

No se inventa una voz nueva: el Enlace traduce y el Escriba registra. Lo que
esto escribe en el acta lo firma el formato, no la prosa.

DOS PASOS, DOS ESTANTES DEL MEDALLON
------------------------------------
**Paso 1, determinista -- SILVER.** Se leen fuentes y se extraen hechos, cada
uno con su procedencia. Lo hace codigo, no un modelo. Es lo unico que cuenta
como medido.

**Paso 2, parafrasis -- BRONZE, en cuarentena.** Un modelo local convierte esos
hechos en prosa. El Medallon es tajante: *«un modelo puede escribir que una
funcion existe; el script comprueba si el fichero esta. Solo lo segundo
cuenta.»* Asi que la prosa nace en cuarentena y va marcada como tal. Si el
modelo no responde, el digesto sale igual con los hechos, y la prosa se declara
NO_DATA: un digesto sin adornos es util; uno con adornos inventados, no.

EL GATE B1-B5
-------------
Los cinco criterios de `ENJAMBRE_MEDALLON.txt:134-148`, «nacidos de fallos
reales de este sistema, uno por uno». Se comprueban sobre el digesto ya escrito,
y si alguno cae, el digesto no se publica en el acta.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sqlite3
import subprocess
import sys
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

AQUI = Path(__file__).resolve().parent
CAPA = AQUI.parent
ESTADO = CAPA / "estado.json"
CONT = Path.home() / "p0x" / "preceptor-internal" / "continuidad"
BANDEJA = Path.home() / "p0x" / "preceptor-internal" / "docs" / "bandeja_firmas.md"
DEAD_PATH = Path.home() / "p0x" / "preceptor-internal" / "agentes" / "bucles" / "dead_path.jsonl"

sys.path.insert(0, str(CAPA / "mensajes"))
import mensajes as ACTA  # noqa: E402

REPOS = {"p0x": Path.home() / "p0x",
         "preceptor": Path.home() / "p0x" / "preceptor",
         "preceptoros-web": Path.home() / "preceptoros-web",
         "preceptor-internal": Path.home() / "p0x" / "preceptor-internal"}

MODELO = os.environ.get("ENLACE_MODELO", "preceptor-v7:latest")

# La voz, en el sistema del modelo. Corta a proposito: un prompt largo se
# reprocesa entero en cada llamada y este bucle corre en cada cierre de sesion.
PAPEL = (
    "Eres el Enlace: el puente entre el rack y el Soberano. Sintetizas, no "
    "enumeras. Te diriges a el como «Soberano». JAMAS ejecutas ni propones "
    "ejecutar: describes y senalas. Escribes en espanol, sobrio y breve.\n"
    "REGLA DURA: solo puedes afirmar lo que este en los HECHOS que te doy, y "
    "cada parrafo cita entre corchetes la fuente del hecho que usa. Si algo no "
    "esta en los hechos, no lo digas. «No lo se con los datos que tengo» es "
    "una respuesta correcta. Ausencia no es cero."
)


def _corre(cmd, timeout=20, cwd=None):
    try:
        p = subprocess.run(cmd, capture_output=True, text=True,
                           timeout=timeout, cwd=cwd)
        return p.returncode == 0, (p.stdout or "") + (p.stderr or "")
    except Exception as e:                          # noqa: BLE001
        return False, f"{type(e).__name__}: {e}"


def _hecho(clave, valor, fuente):
    return {"clave": clave, "valor": valor, "fuente": fuente}


# --------------------------------------------------------------------------
# PASO 1 · los hechos. Deterministas, con fuente. SILVER.
# --------------------------------------------------------------------------

def hechos(desde=None):
    fuera, huecos = [], []

    # --- commits desde el ultimo digesto ---
    for nombre, ruta in REPOS.items():
        if not (ruta / ".git").exists():
            continue
        cmd = ["git", "-C", str(ruta), "log", "--oneline", "--no-decorate"]
        cmd += [f"--since={desde}"] if desde else ["-8"]
        ok, salida = _corre(cmd)
        lineas = [l for l in salida.strip().splitlines() if l.strip()] if ok else []
        if lineas:
            fuera.append(_hecho(f"commits en {nombre}", f"{len(lineas)}: " +
                                "; ".join(l.split(" ", 1)[-1][:70] for l in lineas[:4]),
                                f"git log {nombre}"))
        ok2, n = _corre(["git", "-C", str(ruta), "rev-list", "--count",
                         "@{upstream}..HEAD"])
        if ok2 and n.strip().isdigit() and int(n.strip()):
            fuera.append(_hecho(f"sin empujar en {nombre}", n.strip(),
                                f"git rev-list {nombre}"))

    # --- el estado del rack ---
    if ESTADO.exists():
        try:
            d = json.loads(ESTADO.read_text(encoding="utf-8"))
            c = d.get("componentes", {})
            rojos = [k for k, v in c.items()
                     if isinstance(v, dict) and v.get("estado") == "RED"]
            fuera.append(_hecho("componentes en rojo",
                                ", ".join(f"{k} ({c[k].get('causa','?')[:60]})"
                                          for k in rojos) or "ninguno",
                                "estado.json"))
            for k in ("mvp_gate", "web_gate"):
                b = c.get(k, {})
                if b.get("estado") == "OK":
                    fuera.append(_hecho(k, f"{b.get('pasa')} pruebas en verde",
                                        f"estado.json:{k}"))
        except ValueError as e:
            huecos.append(("estado.json", f"ilegible: {e}",
                           "python3 ~/p0x/Alejandria/recolector.py --completo"))
    else:
        huecos.append(("estado.json", "no existe",
                       "python3 ~/p0x/Alejandria/recolector.py --completo"))

    # --- que dijo cada bucle, de su propio latido ---
    fuera += hechos_del_enjambre(huecos)

    # --- la bandeja de firmas ---
    if BANDEJA.exists():
        filas = [l for l in BANDEJA.read_text(encoding="utf-8").splitlines()
                 if l.startswith("|") and "PENDIENTE" in l]
        # El CONTENIDO de lo pendiente, no solo cuantas hay. Con el numero solo,
        # el modelo se inventaba la pregunta de firma -- y una pregunta
        # inventada en el bloque «que necesita tu firma» es lo peor que puede
        # producir esto: pide atencion humana para algo que nadie midio.
        for l in filas[:4]:
            campos = [c.strip() for c in l.strip("|").split("|")]
            if len(campos) >= 3:
                fuera.append(_hecho(f"pendiente de firma ({campos[1]})", campos[2],
                                    "docs/bandeja_firmas.md"))
        fuera.append(_hecho("bandeja de firmas",
                            f"{len(filas)} propuesta(s) pendientes" if filas
                            else "sin propuestas pendientes",
                            "docs/bandeja_firmas.md"))
    else:
        huecos.append(("bandeja_firmas.md", "no existe", "revisar director.py"))

    # --- dead_path: declarado, no rellenado ---
    if not DEAD_PATH.exists():
        huecos.append((
            "dead_path.jsonl",
            "no existe; especificado en MISION_TENEDOR.md, fase F1 pendiente. "
            "Ningun bucle lo escribe todavia",
            "construir F1, o retirarlo de la lista de fuentes"))

    return fuera, huecos


def hechos_del_enjambre(huecos):
    """El ultimo latido de cada bucle. Lo que HIZO, no su codigo de salida."""
    base = None
    try:
        sys.path.insert(0, str(Path.home() / "p0x" / "preceptor"))
        import casa as _casa
        base = _casa.raiz() / "loops.db"
    except Exception:                               # noqa: BLE001
        pass
    if not base or not base.exists():
        huecos.append(("loops.db", "no se pudo localizar la base de latidos",
                       "python3 ~/p0x/preceptor/preceptoros.py --view"))
        return []
    fuera = []
    try:
        con = sqlite3.connect(f"file:{base}?mode=ro", uri=True, timeout=5)
        # La columna de `bucles` es `nombre`, no `bucle`. Con el nombre
        # equivocado la consulta reventaba y el digesto salia SIN el bloque
        # «que piensa cada agente» -- el central -- declarado como un hueco de
        # permisos. Un error de esquema disfrazado de problema de acceso.
        for (nombre,) in con.execute("select nombre from bucles order by nombre"):
            fila = con.execute(
                "select resultado, nota, datetime(momento,'unixepoch','localtime') "
                "from latidos where bucle=? and evento='sale' "
                "order by momento desc limit 1", (nombre,)).fetchone()
            if fila:
                fuera.append(_hecho(f"bucle {nombre}",
                                    f"{fila[0]} · {fila[1] or 'sin nota'} · {fila[2]}",
                                    f"loops.db:latidos/{nombre}"))
            else:
                fuera.append(_hecho(f"bucle {nombre}",
                                    "registrado pero sin ninguna corrida",
                                    "loops.db:bucles"))
        con.close()
    except sqlite3.Error as e:
        huecos.append(("loops.db", f"{type(e).__name__}: {e}", "revisar permisos"))
    return fuera


# --------------------------------------------------------------------------
# PASO 2 · la parafrasis. BRONZE, en cuarentena.
# --------------------------------------------------------------------------

def _host_ollama():
    v = os.environ.get("OLLAMA_HOST", "").strip()
    if v:
        return v.rstrip("/")
    try:
        for l in (Path.home() / ".config" / "environment.d" / "50-p0x.conf"
                  ).read_text(encoding="utf-8").splitlines():
            if l.strip().startswith("OLLAMA_HOST="):
                return l.partition("=")[2].strip().strip("\"'").rstrip("/")
    except OSError:
        pass
    return ""


def _pedir(host, prompt, tokens=260):
    """Una llamada al modelo local. Devuelve (texto, tokens, segundos) o None."""
    cuerpo = json.dumps({
        "model": MODELO, "prompt": prompt, "stream": False,
        # Razonamiento APAGADO: canon del nodo en todo bucle. Los tokens que
        # cuesta pensar en voz baja se pagan en tiempo de pared.
        "think": False,
        "options": {"temperature": 0.2, "num_predict": tokens, "num_ctx": 8192},
    }).encode("utf-8")
    try:
        req = urllib.request.Request(f"{host}/api/generate", data=cuerpo,
                                     headers={"Content-Type": "application/json"})
        with urllib.request.urlopen(req, timeout=120) as r:
            d = json.loads(r.read().decode("utf-8"))
    except (urllib.error.URLError, OSError, ValueError):
        return None
    return ((d.get("response") or "").strip(),
            d.get("eval_count", 0), (d.get("eval_duration", 0) or 0) / 1e9)


def _corto(h, tope=140):
    """Un hecho, recortado para el modelo. El fichero guarda el entero."""
    return f"- {h['clave']} = {str(h['valor'])[:tope]}  [{h['fuente']}]"


def parafrasear(lista, huecos):
    """Devuelve (prosa, nota). Prosa None si no se pudo: se declara, no se finge.

    BLOQUE A BLOQUE, y no de una vez. Medido: pidiendole los cuatro bloques en
    una sola llamada, `preceptor-v7` devolvia uno o dos y se dejaba el resto --
    y cuantos mas hechos, peor. Un modelo de 2,3 GB sigue UNA instruccion bien
    y cuatro mal; no es un fallo suyo, es pedirle lo que no da.

    Cuatro llamadas cortas cuestan lo mismo en tiempo de pared que una larga y
    aciertan. Y cada bloque recibe SOLO los hechos que le tocan, que es otra
    forma de lo mismo: menos contexto irrelevante, menos deriva.
    """
    host = _host_ollama()
    if not host:
        return None, "OLLAMA_HOST no esta en el entorno ni en environment.d"

    del_enjambre = [h for h in lista if h["clave"].startswith("bucle ")]
    pendientes = [h for h in lista if h["clave"].startswith("pendiente de firma")]
    rojos = [h for h in lista if h["clave"] == "componentes en rojo"
             and "ninguno" not in str(h["valor"])]
    resto = [h for h in lista if h not in del_enjambre and h not in pendientes]

    piezas = []
    marca = {"tokens": 0, "seg": 0.0, "recortado": 0}

    def pedir(titulo, instruccion, material, tope=260):
        if not material:
            return
        cuerpo = "\n".join(_corto(h) for h in material)
        r = _pedir(host, f"{PAPEL}\n\nHECHOS MEDIDOS (cada uno acaba con su "
                         f"fuente entre corchetes):\n{cuerpo}\n\n{instruccion}\n"
                         "Cita [fuente] en cada linea. No escribas titulos.", tope)
        if not r or not r[0]:
            return
        marca["tokens"] += r[1]
        marca["seg"] += r[2]
        piezas.append(f"## {titulo}\n{r[0].strip()}")

    pedir("Qué pasó",
          "Resume en 3 o 4 vinetas lo que ha pasado. Sintetiza, no enumeres.", resto)
    pedir("Qué piensa cada agente",
          "Una linea por bucle: que hizo y cuando. Nada mas.", del_enjambre)

    if pendientes or rojos:
        # UNO solo, elegido aqui. B4 dice «priorizar es trabajo de quien
        # reporta», y quien reporta es este guion, no el modelo: darle dos
        # asuntos y pedirle una pregunta es delegarle la prioridad y ademas
        # invitarle a escribir dos. Manda lo que ya esta en la bandeja sobre lo
        # que solo esta en rojo: la bandeja ya paso por un bucle que decidio
        # que merecia tu atencion.
        antes = len(piezas)
        pedir("Qué necesita tu firma",
              "Escribe UNA SOLA pregunta al Soberano sobre esto. Solo la "
              "pregunta, sin numerar y sin nada mas.",
              (pendientes or rojos)[:1], tope=120)
        if len(piezas) > antes:
            # El modelo devuelve dos preguntas por mucho que se le pida una: es
            # un 2,3 GB. Se recorta AQUI y se declara, porque B4 dice que
            # priorizar es trabajo de quien reporta -- y quien reporta es este
            # guion. Recortar en silencio seria lo unico inaceptable: la
            # marca lo dice en el encabezado del digesto.
            bloque = piezas[-1]
            partes = re.split(r"(?<=\?)\s+", bloque.split("\n", 1)[-1].strip())
            if len(partes) > 1:
                primera = re.sub(r"^\s*\d+[.)]\s*", "", partes[0]).strip()
                piezas[-1] = "## Qué necesita tu firma\n" + primera
                marca["recortado"] = len(partes)
    else:
        piezas.append("## Qué necesita tu firma\nNada pendiente de tu firma.")

    # El bloque de huecos NO lo escribe el modelo: se compone del dato. Es el
    # que menos puede permitirse una invencion -- si algo no se pudo medir,
    # decirlo mal es peor que no decirlo.
    piezas.append("## NO_DATA\n" + ("\n".join(
        f"- {c} [{q}]" for q, c, _ in huecos) if huecos
        else "- Ninguno: todas las fuentes respondieron."))

    if len(piezas) < 3:
        return None, "el modelo local no completó los bloques"
    recorte = (f" · se recortaron {marca['recortado'] - 1} pregunta(s) de más "
               "en «Qué necesita tu firma» (B4: priorizar es trabajo de quien "
               "reporta)") if marca["recortado"] else ""
    return "\n\n".join(piezas), (
        f"{MODELO} · {marca['tokens']} tokens en {marca['seg']:.1f} s · "
        f"{len(piezas)} bloques · BRONZE (en cuarentena: lo escribio un "
        f"modelo){recorte}")


# EL GATE · B1-B5 del Medallon
# --------------------------------------------------------------------------

BLOQUES = ("## Qué pasó", "## Qué piensa cada agente",
           "## Qué necesita tu firma", "## NO_DATA")


def gate(prosa, lista, huecos):
    """Los cinco criterios. Devuelve la lista de fallos, vacia si pasa."""
    fallos = []
    if prosa is None:
        return []                    # sin prosa no hay nada que juzgar: ya es NO_DATA

    # B3 se mide contra TODO el material entregado, no solo contra las claves
    # de fuente. En la primera corrida el gate tumbo una parafrasis correcta
    # porque el modelo cito `MISION_TENEDOR.md`, un nombre que estaba DENTRO
    # del texto de un hueco que yo mismo le habia dado. Citar algo que se leyo
    # en el material es exactamente lo que B3 pide -- «las conclusiones se
    # escriben DESPUES de mirar» --, no lo que prohibe. El gate era el
    # equivocado, no la prosa.
    corpus = " ".join([f"{h['clave']} {h['valor']} {h['fuente']}" for h in lista] +
                      [f"{q} {c} {r}" for q, c, r in huecos])
    fuentes = {h["fuente"] for h in lista} | {q for q, _, _ in huecos}
    # Un corchete puede citar VARIAS fuentes -- «[git log p0x, git log
    # preceptor]» es una cita legitima cuando una vinieta resume cuatro
    # hechos. El gate leia la cadena entera como una sola fuente y tumbaba
    # parafrasis correctas. Se separan por coma.
    # Una cita NO cruza el salto de linea. Sin esa restriccion, un corchete
    # que el modelo deja sin cerrar hace que el patron se trague texto hasta
    # el siguiente `]` de otro parrafo, y B3 denuncia como «fuente inventada»
    # un trozo de prosa. Medido: «37 suites confirmadas, docs/bandeja_firmas».
    #
    # Con `[^\]\n]`, un corchete sin cerrar sencillamente no es una cita --
    # que es lo correcto: no se puede exigir la fuente de algo que el modelo
    # no llego a declarar como cita.
    citadas = {t.strip() for grupo in re.findall(r"\[([^\]\n]+)\]", prosa)
               for t in grupo.split(",") if t.strip()}

    # B1 · toda cifra con el comando que la produjo.
    cifras_prosa = set(re.findall(r"\b\d[\d.,]*\b", prosa))
    cifras_hechos = set()
    for h in lista:
        cifras_hechos |= set(re.findall(r"\b\d[\d.,]*\b", f"{h['valor']} {h['clave']}"))
    huerfanas = sorted(cifras_prosa - cifras_hechos)
    if huerfanas:
        fallos.append(f"B1 · cifras que no salen de ningun hecho: {', '.join(huerfanas)}")

    # B2 · lo indeterminado, declarado.
    if huecos and "NO_DATA" not in prosa:
        fallos.append(f"B2 · hay {len(huecos)} hueco(s) y la prosa no los declara")

    # B3 · conclusiones despues de mirar: no se cita lo que no se leyo.
    inventadas = sorted(c for c in citadas
                        if c not in fuentes and not any(c in f for f in fuentes)
                        and c not in corpus)
    if inventadas:
        fallos.append(f"B3 · cita fuentes que el paso 1 no leyo: {', '.join(inventadas)}")

    # B4 · UNA sola pregunta abierta.
    m = re.search(r"## Qué necesita tu firma(.*?)(?=\n## |\Z)", prosa, re.S)
    if m:
        n = m.group(1).count("?")
        if n > 1:
            fallos.append(f"B4 · {n} preguntas abiertas; priorizar es trabajo "
                          "de quien reporta")

    # B5 · el resumen concuerda con el cuerpo.
    faltan = [b for b in BLOQUES if b not in prosa]
    if faltan:
        fallos.append(f"B5 · faltan bloques: {', '.join(faltan)}")
    return fallos


# --------------------------------------------------------------------------

def render(lista, huecos, prosa, nota, sello):
    L = [f"# El Enlace dice · {sello}", ""]
    if prosa:
        L += ["> **BRONZE · en cuarentena.** Lo de abajo lo redactó un modelo "
              "local a partir de los hechos medidos. Los hechos son Silver; "
              "la prosa, no.", f"> `{nota}`", "", prosa, ""]
    else:
        L += [f"> ⬜ **Sin paráfrasis.** {nota}", "",
              "> El digesto sale igual con los hechos: uno sin adornos es útil; "
              "uno con adornos inventados, no.", ""]
    L += ["---", "", "## Los hechos (Silver · medidos)", "",
          "| Qué | Valor | Fuente |", "|---|---|---|"]
    L += [f"| {h['clave']} | {h['valor']} | `{h['fuente']}` |" for h in lista]
    L += ["", "## Huecos declarados", ""]
    L += ([f"- **{q}** — {c} · *remedio:* {r}" for q, c, r in huecos]
          or ["*Ninguno: todas las fuentes respondieron.*"])
    L += ["", "---", "",
          "*El Enlace traduce y señala. No actúa: ninguna puerta se abre sin tu palabra.*"]
    return "\n".join(L) + "\n"


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--sesion", default=datetime.now().strftime("%Y-%m-%d"))
    ap.add_argument("--desde", help="fecha para git log (por defecto, ultimos 8)")
    ap.add_argument("--sin-modelo", action="store_true",
                    help="salta el paso 2; util para probar el paso determinista")
    a = ap.parse_args(argv)

    lista, huecos = hechos(a.desde)
    if not lista:
        print("⬜ NO_DATA · ninguna fuente respondio: no hay digesto que escribir",
              file=sys.stderr)
        return 1

    prosa, nota = (None, "salteado con --sin-modelo") if a.sin_modelo \
        else parafrasear(lista, huecos)

    fallos = gate(prosa, lista, huecos)
    if fallos:
        # La prosa cae; los hechos NO. Se publica el digesto sin ella y se dice
        # por que: perder la medida por culpa del adorno seria el peor cambio.
        nota = "la parafrasis no pasó el gate B1-B5: " + " · ".join(fallos)
        prosa = None

    sello = datetime.now().strftime("%Y%m%d-%H%M%S")
    AQUI.mkdir(parents=True, exist_ok=True)
    destino = AQUI / f"digesto-{sello}.md"
    destino.write_text(render(lista, huecos, prosa, nota, sello), encoding="utf-8")

    resumen = (prosa.split("\n## ")[0].replace("## Qué pasó", "").strip()[:600]
               if prosa else
               f"{len(lista)} hechos medidos y {len(huecos)} hueco(s) declarados. "
               f"Sin paráfrasis: {nota}")
    m = ACTA.escribir(
        de="enlace", para=["soberano"], tipo="digesto",
        humano=resumen,
        # Los recuentos van en la cara de maquina como DATO, no solo como
        # lista. Si la cara humana dice «16 hechos», ese 16 tiene que estar
        # respaldado por el otro lado -- es literalmente el criterio B5, y el
        # acta lo rechazo la primera vez que no lo estuvo. Tenia razon.
        maquina={"n_hechos": len(lista), "n_huecos": len(huecos),
                 "hechos": lista,
                 "huecos": [{"fuente": q, "causa": c, "remedio": r}
                            for q, c, r in huecos],
                 "acciones": [], "parafrasis": nota,
                 "estante": "BRONZE" if prosa else "—"},
        fuente=sorted({h["fuente"] for h in lista}),
        firma_requerida=False)

    con = sqlite3.connect(str(CONT / "continuidad.db"), timeout=10)
    con.execute("""CREATE TABLE IF NOT EXISTS digestos (
        id INTEGER PRIMARY KEY AUTOINCREMENT, sesion TEXT, sello TEXT,
        fichero TEXT, mensaje TEXT, hechos INTEGER, huecos INTEGER,
        estante TEXT, gate TEXT)""")
    con.execute("INSERT INTO digestos (sesion, sello, fichero, mensaje, hechos, "
                "huecos, estante, gate) VALUES (?,?,?,?,?,?,?,?)",
                (a.sesion, sello, destino.name, m["id"], len(lista), len(huecos),
                 "BRONZE" if prosa else "—",
                 "verde" if not fallos else " · ".join(fallos)))
    con.commit(); con.close()

    print(f"  digesto → {destino.name} · {len(lista)} hechos · "
          f"{len(huecos)} hueco(s) · acta {m['id']}")
    if fallos:
        print("  🔴 la paráfrasis no pasó el gate: " + " · ".join(fallos))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
