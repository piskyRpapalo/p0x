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

from fastapi import FastAPI, HTTPException
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
        -- Los retos: uno por peticion, y se queman al usarse. Guardarlos en la
        -- base y no en memoria es lo que hace que un reinicio no invalide los
        -- que hay en vuelo -- y que dos procesos no se contradigan.
        CREATE TABLE IF NOT EXISTS retos (
          reto TEXT PRIMARY KEY, creado REAL NOT NULL,
          usado INTEGER NOT NULL DEFAULT 0);
        """)
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


def verificar(pseudonimo, clave_publica, reto, firma):
    """Ed25519 sobre `pseudonimo|clave_publica|reto`. Falla CERRADO.

    Los tres campos van en el mensaje a proposito: firmar solo el reto dejaria
    reusar esa firma para otro pseudonimo, y firmar solo el pseudonimo la
    dejaria valer para siempre.
    """
    mensaje = f"{pseudonimo}|{clave_publica.lower()}|{reto}".encode("utf-8")
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


@app.post(f"/api/{VERSION}/profiles", status_code=201)
def crear_perfil(p: NuevoPerfil):
    if not HEX64.match(p.clave_publica):
        raise HTTPException(422, "clave_publica: 64 caracteres hexadecimales")
    with abrir() as c:
        motivo = quemar_reto(c, p.reto)
        if motivo:
            c.commit()
            raise HTTPException(403, {"estado": "RECHAZADO", "causa": motivo})
        if not verificar(p.pseudonimo, p.clave_publica, p.reto, p.firma):
            c.commit()      # el reto se quema igual: un intento fallido lo gasta
            raise HTTPException(403, {"estado": "RECHAZADO",
                                      "causa": "la firma no corresponde a esa clave publica"})
        try:
            c.execute("insert into perfiles (pseudonimo, clave_publica, creado_en, "
                      "firma_verificada) values (?,?,?,1)",
                      (p.pseudonimo, p.clave_publica.lower(), time.time()))
            c.commit()
        except sqlite3.IntegrityError:
            # Idempotente si es el MISMO par; conflicto si el pseudonimo ya es
            # de otra clave. Reintentar no puede robarle el nombre a nadie.
            fila = c.execute("select clave_publica from perfiles where pseudonimo=?",
                             (p.pseudonimo,)).fetchone()
            if fila and fila["clave_publica"] == p.clave_publica.lower():
                return {"estado": "OK", "pseudonimo": p.pseudonimo, "nuevo": False}
            raise HTTPException(409, "ese pseudonimo ya es de otra clave")
    return {"estado": "OK", "pseudonimo": p.pseudonimo, "nuevo": True,
            "firma_verificada": True}


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


init()
