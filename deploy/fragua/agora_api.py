#!/usr/bin/env python3
"""El Agora · /api/v1. Perfiles, companeros y seleccion. Corre en la-fragua.

ALCANCE, Y ES ESTRECHO A PROPOSITO
-----------------------------------
Tres endpoints y nada mas. El canon del nodo soberano dice «propose-only hacia
otros nodos»; la mision para desplegar aqui esta firmada y esta ACOTADA a esto.
Cualquier cosa que no sean estos tres caminos necesita palabra nueva.

COMO SE PRUEBA QUIEN ERES
--------------------------
Con un reto de un solo uso. `GET /reto` devuelve un nonce; quien quiera crear
un perfil o elegir companero firma `pseudonimo|clave_publica|reto` con su
clave privada Ed25519 y manda la firma. El servidor la verifica con la clave
publica que le dan: eso demuestra POSESION de la privada, que es lo unico que
hace falta aqui.

Hasta ayer esto no existia y la API lo declaraba en cada respuesta --
«cualquiera puede crear un perfil con la clave publica de otro». Ya no: sin la
privada no se pasa de la puerta.

El nonce es de UN SOLO USO y caduca. Sin las dos cosas, una firma capturada
una vez vale para siempre, y entonces el reto no es un reto: es una
contrasena larga viajando en claro.

`pynacl` es la unica dependencia de este servicio y es deliberada: la promesa
de «stdlib only» rige la Boveda -- el producto que se instala la gente -- no
el Agora, que corre en el rack del Soberano. Meter criptografia a mano seria
mucho peor que declarar la dependencia.

Escucha en LOOPBACK. Al exterior solo sale por el tunel, que se crea aparte y
con firma.
"""
from __future__ import annotations

import json
import os
import re
import sqlite3
import time
from pathlib import Path

from fastapi import FastAPI, HTTPException, Response
from pydantic import BaseModel, Field

from nacl.exceptions import BadSignatureError
from nacl.signing import VerifyKey

# guardia:permitir es la ruta de datos del nodo de destino, no de este
# La monta el Soberano en la-fragua y es parte del contrato de este artefacto:
# un deploy/<nodo>/ que no dice donde escribe obliga a leerse el codigo para
# saberlo. Se deja como DEFECTO y no como constante: `AGORA_DATOS` la cambia.
DATOS = Path(os.environ.get("AGORA_DATOS", "/mnt/nvme/agora_db"))  # guardia:permitir ruta del nodo de destino, no de este
DB = DATOS / "agora.db"
CATALOGO = Path(__file__).resolve().parent / "agentes.json"
VERSION = "v1"
RETO_VIVE_S = 300      # cinco minutos: lo que tarda una persona, no una cola

app = FastAPI(title="PreceptorOS · El Agora", version="1.0.0",
              docs_url=f"/api/{VERSION}/docs", openapi_url=f"/api/{VERSION}/openapi.json")

HEX64 = re.compile(r"^[0-9a-fA-F]{64}$")


def abrir():
    """WAL, y un solo escritor. La base vive en el NVMe, no en la microSD."""
    DATOS.mkdir(parents=True, exist_ok=True)
    c = sqlite3.connect(DB, timeout=10)
    c.row_factory = sqlite3.Row
    c.execute("PRAGMA journal_mode=WAL")
    c.execute("PRAGMA foreign_keys=ON")
    return c


def init():
    with abrir() as c:
        c.executescript("""
        CREATE TABLE IF NOT EXISTS perfiles (
          pseudonimo TEXT PRIMARY KEY,
          clave_publica TEXT NOT NULL UNIQUE,
          creado_en REAL NOT NULL,
          -- Se declara en la propia fila que esto NO esta verificado. Una
          -- columna que lo dice es mas dificil de olvidar que un comentario.
          firma_verificada INTEGER NOT NULL DEFAULT 0);
        -- El tablon. Vacio a proposito: no se siembran hilos de ejemplo en la
        -- base. La web YA lleva `threads.json` con hilos declarados EJEMPLO
        -- para cuando el Agora no contesta; sembrarlos aqui los convertiria en
        -- reales sin que nadie los haya escrito, que es justo lo que
        -- `community.html` dice no hacer.
        CREATE TABLE IF NOT EXISTS hilos (
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          tipo TEXT NOT NULL, titulo TEXT NOT NULL,
          autor TEXT NOT NULL, cuando REAL NOT NULL,
          respuestas INTEGER NOT NULL DEFAULT 0);
        CREATE INDEX IF NOT EXISTS idx_hilos ON hilos(cuando DESC);
        CREATE TABLE IF NOT EXISTS selecciones (
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          pseudonimo TEXT NOT NULL,
          agente TEXT NOT NULL,
          cuando REAL NOT NULL,
          FOREIGN KEY (pseudonimo) REFERENCES perfiles(pseudonimo));
        -- Solo se anade: la eleccion anterior no se pisa. Saber que alguien
        -- cambio de companero, y cuando, es informacion; sobrescribir la
        -- borra.
        CREATE INDEX IF NOT EXISTS idx_sel ON selecciones(pseudonimo, cuando);
        -- La ficha publica. `bio` y `avatar` se anaden a una tabla que ya
        -- tiene filas en produccion, asi que van por ALTER y no en el CREATE:
        -- un CREATE TABLE IF NOT EXISTS con columnas nuevas no las anade a la
        -- tabla que ya existe -- no falla, simplemente no hace nada, y el
        -- endpoint saldria con «no such column» en el primer SELECT.
        -- Los retos: uno por peticion, y se queman al usarse. Guardarlos en la
        -- base y no en memoria es lo que hace que un reinicio no invalide los
        -- que hay en vuelo -- y que dos procesos no se contradigan.
        CREATE TABLE IF NOT EXISTS retos (
          reto TEXT PRIMARY KEY, creado REAL NOT NULL,
          usado INTEGER NOT NULL DEFAULT 0);
        """)
        # ALTER idempotente: SQLite no tiene `ADD COLUMN IF NOT EXISTS`, asi
        # que se pregunta a la propia tabla que columnas tiene. Repetir el
        # ALTER seria un error, no un no-op.
        tiene = {f["name"] for f in c.execute("PRAGMA table_info(perfiles)")}
        for col, tipo in (("bio", "TEXT"), ("avatar", "TEXT")):
            if col not in tiene:
                c.execute(f"ALTER TABLE perfiles ADD COLUMN {col} {tipo}")
        c.commit()


def catalogo():
    try:
        return json.loads(CATALOGO.read_text(encoding="utf-8"))
    except (OSError, ValueError) as e:
        raise HTTPException(503, {"estado": "NO_DATA",
                                  "causa": f"catalogo ilegible: {type(e).__name__}",
                                  "remedio": "revisar deploy/fragua/agentes.json"})


class NuevoPerfil(BaseModel):
    pseudonimo: str = Field(min_length=3, max_length=64)
    clave_publica: str = Field(min_length=64, max_length=64)
    reto: str
    firma: str
    # La ficha es OPCIONAL, y por eso son `None` y no cadena vacia: hay que
    # poder distinguir «no toco la bio» de «borra la bio». Con "" las dos
    # peticiones serian la misma y crear una identidad borraria la ficha.
    bio: str | None = Field(default=None, max_length=2000)
    avatar: str | None = Field(default=None, max_length=32)


class Seleccion(BaseModel):
    pseudonimo: str
    agente: str
    reto: str
    firma: str


def quemar_reto(c, reto):
    """Un reto vale UNA vez y dura poco. Devuelve el motivo del rechazo o None.

    Se marca usado en la MISMA transaccion que lo comprueba: si se hiciera
    despues de verificar la firma, dos peticiones simultaneas con el mismo
    reto pasarian las dos.
    """
    fila = c.execute("select creado, usado from retos where reto=?", (reto,)).fetchone()
    if not fila:
        return "ese reto no existe: pide uno en GET /api/v1/reto"
    if fila["usado"]:
        return "ese reto ya se uso: los retos valen una sola vez"
    if time.time() - fila["creado"] > RETO_VIVE_S:
        return f"ese reto caduco (vive {RETO_VIVE_S} s)"
    c.execute("update retos set usado=1 where reto=?", (reto,))
    return None


def verificar(pseudonimo, clave_publica, reto, firma, ficha=None):
    """Ed25519 sobre `pseudonimo|clave_publica|reto`. Falla CERRADO.

    Los tres campos van en el mensaje a proposito: firmar solo el reto dejaria
    reusar esa firma para otro pseudonimo, y firmar solo el pseudonimo la
    dejaria valer para siempre.

    CUANDO VIENE FICHA, LA FICHA SE FIRMA. El mensaje pasa a ser
    `pseudonimo|clave_publica|reto|avatar|bio`. Sin esto la firma probaria
    quien eres y no QUE ESCRIBES: cualquiera que interceptase una peticion
    valida podria cambiarle la biografia por el camino y la firma seguiria
    cuadrando. Una firma que no cubre el contenido no lo protege.

    El formato es condicional a proposito, y no abre un hueco: una firma de
    tres campos NO vale para una peticion con ficha --el servidor verifica el
    mensaje de cinco y no cuadra-- y una de cinco tampoco vale si se le quita
    la ficha por el camino. No hay degradacion posible en ninguna direccion.
    Y el cliente que ya esta desplegado (`auth.js`, que firma tres campos para
    crear identidad) sigue funcionando sin tocarlo.
    """
    base = f"{pseudonimo}|{clave_publica.lower()}|{reto}"
    if ficha is not None:
        avatar, bio = ficha
        base = f"{base}|{avatar}|{bio}"
    mensaje = base.encode("utf-8")
    try:
        VerifyKey(bytes.fromhex(clave_publica)).verify(mensaje, bytes.fromhex(firma))
        return True
    except (BadSignatureError, ValueError, TypeError):
        return False


@app.get(f"/api/{VERSION}/salud")
def salud():
    with abrir() as c:
        n = c.execute("select count(*) from perfiles").fetchone()[0]
    return {"estado": "OK", "version": VERSION, "perfiles": n,
            "firmas_verificadas": True, "reto_vive_s": RETO_VIVE_S,
            "aviso": "las escrituras exigen firma Ed25519 sobre un reto de un solo uso"}


@app.get(f"/api/{VERSION}/reto")
def reto():
    """Un nonce para firmar. De un solo uso y con caducidad."""
    n = os.urandom(16).hex()
    with abrir() as c:
        c.execute("insert into retos (reto, creado) values (?,?)", (n, time.time()))
        # Se barren los viejos aqui y no con un timer: el unico momento en que
        # esta tabla crece es este, asi que es donde toca podarla.
        c.execute("delete from retos where creado < ?", (time.time() - RETO_VIVE_S * 4,))
        c.commit()
    return {"estado": "OK", "reto": n, "vive_s": RETO_VIVE_S,
            "firma_sobre": "pseudonimo|clave_publica|reto"}


AVATAR = re.compile(r"^[a-z0-9][a-z0-9-]{0,31}$")


@app.post(f"/api/{VERSION}/profiles", status_code=201)
def crear_perfil(p: NuevoPerfil, respuesta: Response):
    if not HEX64.match(p.clave_publica):
        raise HTTPException(422, "clave_publica: 64 caracteres hexadecimales")
    # HAY FICHA si viene cualquiera de los dos campos. Se normaliza a cadena
    # para firmar, porque `None` y "" tienen que dar mensajes distintos y solo
    # uno de los dos puede viajar dentro de un texto firmado.
    hay_ficha = p.bio is not None or p.avatar is not None
    avatar = p.avatar or ""
    bio = p.bio or ""
    if avatar and not AVATAR.match(avatar):
        # El catalogo de bustos NO se valida aqui: lo publica la web
        # (`bustos.json`) y copiarlo al Agora crearia dos listas que se
        # separan el dia que se anada un busto. Lo que si es del Agora es la
        # FORMA: un identificador, no una ruta ni un texto libre.
        raise HTTPException(422, "avatar: identificador [a-z0-9-], hasta 32")
    with abrir() as c:
        motivo = quemar_reto(c, p.reto)
        if motivo:
            c.commit()
            raise HTTPException(403, {"estado": "RECHAZADO", "causa": motivo})
        ficha = (avatar, bio) if hay_ficha else None
        if not verificar(p.pseudonimo, p.clave_publica, p.reto, p.firma, ficha):
            c.commit()      # el reto se quema igual: un intento fallido lo gasta
            raise HTTPException(403, {"estado": "RECHAZADO",
                                      "causa": "la firma no cubre lo que se manda"
                                      if hay_ficha else
                                      "la firma no corresponde a esa clave publica"})
        fila = c.execute("select clave_publica from perfiles where pseudonimo=?",
                         (p.pseudonimo,)).fetchone()
        if fila:
            # Idempotente si es el MISMO par; conflicto si el pseudonimo ya es
            # de otra clave. Reintentar no puede robarle el nombre a nadie.
            if fila["clave_publica"] != p.clave_publica.lower():
                raise HTTPException(409, "ese pseudonimo ya es de otra clave")
            if hay_ficha:
                # Solo se pisa lo que venia. Mandar avatar sin bio no borra la
                # bio: son dos campos de la misma ficha, no una ficha entera.
                if p.avatar is not None:
                    c.execute("update perfiles set avatar=? where pseudonimo=?",
                              (avatar, p.pseudonimo))
                if p.bio is not None:
                    c.execute("update perfiles set bio=? where pseudonimo=?",
                              (bio, p.pseudonimo))
                c.commit()
            # 200 y no 201: no se ha creado nada. El 201 es del decorador,
            # que solo sabe del camino feliz; aqui se corrige en el camino que
            # ACTUALIZA. Un 201 en cada guardado de biografia diria «he creado
            # un perfil» una vez por pulsacion del boton.
            respuesta.status_code = 200
            return {"estado": "OK", "pseudonimo": p.pseudonimo, "nuevo": False,
                    "ficha_guardada": hay_ficha}
        try:
            c.execute("insert into perfiles (pseudonimo, clave_publica, creado_en, "
                      "firma_verificada, bio, avatar) values (?,?,?,1,?,?)",
                      (p.pseudonimo, p.clave_publica.lower(), time.time(),
                       p.bio, p.avatar))
            c.commit()
        except sqlite3.IntegrityError:
            # La clave publica es UNIQUE: el choque que queda es esa misma
            # clave pedida con otro pseudonimo.
            raise HTTPException(409, "esa clave publica ya tiene otro pseudonimo")
    return {"estado": "OK", "pseudonimo": p.pseudonimo, "nuevo": True,
            "firma_verificada": True, "ficha_guardada": hay_ficha}


@app.get(f"/api/{VERSION}/profiles/{{huella}}")
def ficha(huella: str):
    """La ficha publica. `huella` es el pseudonimo O la clave publica entera.

    Las dos porque las dos son la huella para quien mira desde la web:
    `auth.js` llama «la huella completa» a la clave publica en hexadecimal y es
    lo que `profile.html` ensena en su <details>, mientras que el pseudonimo es
    lo que se ve en la cabecera y lo que se comparte. Obligar a elegir una
    obligaria a la web a saber cual, y la web tiene las dos a mano.

    NO PIDE FIRMA: es una ficha PUBLICA, y todo lo que devuelve ya es publico
    por definicion --el pseudonimo se deriva de la clave, la clave es publica y
    la biografia se escribe para que se lea. Exigir firma para leer convertiria
    un perfil publico en uno privado sin decirlo.
    """
    with abrir() as c:
        campo = "clave_publica" if HEX64.match(huella) else "pseudonimo"
        valor = huella.lower() if campo == "clave_publica" else huella
        f = c.execute(f"select pseudonimo, clave_publica, creado_en, bio, avatar "
                      f"from perfiles where {campo}=?", (valor,)).fetchone()
        if not f:
            raise HTTPException(404, {"estado": "NO_DATA",
                                      "causa": f"no hay perfil con esa {campo}"})
        sel = c.execute("select agente, cuando from selecciones where pseudonimo=? "
                        "order by cuando desc limit 1", (f["pseudonimo"],)).fetchone()
    return {
        "estado": "OK",
        "pseudonimo": f["pseudonimo"],
        "clave_publica": f["clave_publica"],
        "creado_en": f["creado_en"],
        "bio": f["bio"],
        "avatar": f["avatar"],
        "companero": sel["agente"] if sel else None,
        # LAS MEDIDAS NO SE INVENTAN. Un `scores: 0` aqui se leeria como
        # «midio cero veces» cuando lo cierto es que este nodo no tiene el
        # ledger: son dos cosas distintas y la diferencia es el proyecto
        # entero. Va `null` con la causa al lado, como ya hace la web.
        "scores": None,
        "scores_causa": "el Agora no guarda el ledger firmado: las medidas "
                        "viven en ledger.jsonl y todavia no llega ninguna "
                        "linea firmada de nadie",
    }


@app.get(f"/api/{VERSION}/agents")
def agentes():
    d = catalogo()
    lista = sorted(d["agentes"], key=lambda a: a["orden"])
    return {"estado": "OK", "nota": d["nota"],
            "disponibles": sum(1 for a in lista if a["disponible"]),
            "total": len(lista), "agentes": lista}


@app.post(f"/api/{VERSION}/agents/select")
def elegir(s: Seleccion):
    d = catalogo()
    porid = {a["id"]: a for a in d["agentes"]}
    a = porid.get(s.agente)
    if not a:
        raise HTTPException(404, f"no hay ningun companero '{s.agente}'")
    if not a["disponible"]:
        # 409 y no 400: la peticion es valida, lo que no existe es el
        # companero. Y se devuelve la causa, que es lo que el usuario necesita.
        raise HTTPException(409, {"estado": "NO_DATA", "agente": s.agente,
                                  "causa": a.get("causa", "no disponible")})
    with abrir() as c:
        fila = c.execute("select clave_publica from perfiles where pseudonimo=?",
                         (s.pseudonimo,)).fetchone()
        if not fila:
            raise HTTPException(404, "ese perfil no existe: crealo primero")
        motivo = quemar_reto(c, s.reto)
        if motivo:
            c.commit()
            raise HTTPException(403, {"estado": "RECHAZADO", "causa": motivo})
        # Se firma contra la clave que YA esta guardada, no contra una que
        # venga en la peticion: si no, elegir companero por otro seria mandar
        # su pseudonimo con la clave propia.
        if not verificar(s.pseudonimo, fila["clave_publica"], s.reto, s.firma):
            c.commit()
            raise HTTPException(403, {"estado": "RECHAZADO",
                                      "causa": "la firma no es de quien dice ser ese perfil"})
        c.execute("insert into selecciones (pseudonimo, agente, cuando) values (?,?,?)",
                  (s.pseudonimo, s.agente, time.time()))
        c.commit()
    return {"estado": "OK", "pseudonimo": s.pseudonimo, "agente": s.agente,
            "adaptador": a["adaptador"], "nombre": a["nombre"]}


@app.get(f"/api/{VERSION}/threads")
def hilos():
    """El tablon. Devuelve lo que HAY, y dice cuanto es.

    `community.html` lee esto por `board-fuentes.js`, que comprueba
    `Array.isArray(d.hilos)` y nada mas. Por eso viaja tambien
    `hilos_reales`: una lista vacia y una lista que no llego se ven igual en
    la pantalla, y la web necesita el dato para escribir la frase --no puede
    salir de aqui ya escrita, porque aqui no hay idioma.

    OJO AL EFECTO, QUE ES REAL: hasta hoy esta ruta daba 404 y la web caia a
    `threads.json`, sus hilos de EJEMPLO. En cuanto responda 200 con cero
    hilos, el tablon se ensenara VACIO, porque vacio es lo que hay. Es la
    misma regla que el propio `threads.json` declara en su cabecera: fingir
    actividad en un foro sin comunidad es la mentira mas vieja de internet.

    NO HAY POST. Escribir en el tablon exige moderacion, limites de ritmo y
    una decision sobre que se hace con lo que se publica; nada de eso esta
    firmado, y abrir la escritura antes que esa decision seria abrir un buzon
    publico sin saber quien lo vacia.
    """
    with abrir() as c:
        filas = c.execute("select tipo, titulo, autor, cuando, respuestas "
                          "from hilos order by cuando desc limit 200").fetchall()
    return {"estado": "OK", "hilos_reales": len(filas),
            "escritura": "cerrada: el Agora todavia no modera",
            "hilos": [dict(f) for f in filas]}


init()


# --- PROXY A OLLAMA Y CORS -------------------------------------------------
#
# ESTE BLOQUE VOLVIO DEL NODO, no se escribio aqui. Lo anadio el Soberano a
# mano sobre `la-fragua` el 2026-09-01 para que la portada pudiera hablar con
# el modelo del rack, y el repo no se entero: durante dos dias el artefacto
# versionado NO era lo que corria. Se recupera integro salvo una cosa.
#
# LA UNICA COSA: la direccion de la Ollama viaja por entorno y no escrita
# aqui. En el nodo era una IP de tailnet literal, y la guardia de higiene la
# marca [IP-TAILNET] -- una regla que ni `guardia:permitir` puede eximir
# (D8_JAMAS). Este repo tiene remoto publico. Sin `OLLAMA_HOST` puesto, el
# proxy NO adivina un destino: contesta 503 diciendo que falta, que es
# preferible a arrancar apuntando a una maquina que igual no es la que se
# queria.
import os as _os

import httpx
from fastapi import Request
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    # Un origen exacto por entrada. `http://localhost:*` NO es un comodin
    # valido para CORS y el navegador nunca lo casa: estaba en el nodo y aqui
    # se deja fuera en vez de arrastrar una entrada que no hace nada. Para
    # probar en local se anade el puerto concreto.
    allow_origins=["https://preceptoros.org"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["Content-Type"],
)

OLLAMA_HOST = _os.environ.get("OLLAMA_HOST", "").rstrip("/")


@app.post("/api/generate")
async def proxy_ollama_generate(request: Request):
    """Contrato de Ollama, tal cual. La web ya lo habla; no se inventa otro."""
    if not OLLAMA_HOST:
        raise HTTPException(503, {"estado": "NO_DATA",
                                  "causa": "OLLAMA_HOST no esta puesto en el entorno",
                                  "remedio": "exportarlo antes de arrancar uvicorn"})
    cuerpo = await request.json()

    async def trozos():
        async with httpx.AsyncClient(timeout=120.0) as cliente:
            async with cliente.stream("POST", f"{OLLAMA_HOST}/api/generate",
                                      json=cuerpo) as r:
                async for t in r.aiter_bytes():
                    yield t

    return StreamingResponse(trozos(), media_type="application/x-ndjson")
