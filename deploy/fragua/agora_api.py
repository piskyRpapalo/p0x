#!/usr/bin/env python3
"""El Agora · /api/v1. Perfiles, companeros y seleccion. Corre en la-fragua.

ALCANCE, Y ES ESTRECHO A PROPOSITO
-----------------------------------
Tres endpoints y nada mas. El canon del nodo soberano dice «propose-only hacia
otros nodos»; la mision para desplegar aqui esta firmada y esta ACOTADA a esto.
Cualquier cosa que no sean estos tres caminos necesita palabra nueva.

QUE NO HACE, Y SE DICE ANTES
-----------------------------
NO verifica firmas Ed25519. Guarda la clave publica que le mandan y la trata
como un identificador, no como una prueba. Verificar exigiria una dependencia
de criptografia que hoy no esta en este venv, y meterla a escondidas seria
peor que el hueco.

Consecuencia real, y va tambien en la respuesta de la API: **cualquiera puede
crear un perfil con la clave publica de otro**. Sirve para vincular un aparato
propio, no para autenticar a nadie frente a terceros. La misma frase esta ya
en la pagina de onboarding, y aqui se repite porque quien lea la API puede no
haber leido la web.

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

# guardia:permitir es la ruta de datos del nodo de destino, no de este
# La monta el Soberano en la-fragua y es parte del contrato de este artefacto:
# un deploy/<nodo>/ que no dice donde escribe obliga a leerse el codigo para
# saberlo. Se deja como DEFECTO y no como constante: `AGORA_DATOS` la cambia.
DATOS = Path(os.environ.get("AGORA_DATOS", "/mnt/nvme/agora_db"))  # guardia:permitir ruta del nodo de destino, no de este
DB = DATOS / "agora.db"
CATALOGO = Path(__file__).resolve().parent / "agentes.json"
VERSION = "v1"

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


class Seleccion(BaseModel):
    pseudonimo: str
    agente: str


@app.get(f"/api/{VERSION}/salud")
def salud():
    with abrir() as c:
        n = c.execute("select count(*) from perfiles").fetchone()[0]
    return {"estado": "OK", "version": VERSION, "perfiles": n,
            "firmas_verificadas": False,
            "aviso": "esta API identifica, no autentica: no verifica firmas Ed25519"}


@app.post(f"/api/{VERSION}/profiles", status_code=201)
def crear_perfil(p: NuevoPerfil):
    if not HEX64.match(p.clave_publica):
        raise HTTPException(422, "clave_publica: 64 caracteres hexadecimales")
    with abrir() as c:
        try:
            c.execute("insert into perfiles (pseudonimo, clave_publica, creado_en) "
                      "values (?,?,?)",
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
            "aviso": "la firma NO se ha verificado: esto identifica, no autentica"}


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
        if not c.execute("select 1 from perfiles where pseudonimo=?",
                         (s.pseudonimo,)).fetchone():
            raise HTTPException(404, "ese perfil no existe: crealo primero")
        c.execute("insert into selecciones (pseudonimo, agente, cuando) values (?,?,?)",
                  (s.pseudonimo, s.agente, time.time()))
        c.commit()
    return {"estado": "OK", "pseudonimo": s.pseudonimo, "agente": s.agente,
            "adaptador": a["adaptador"], "nombre": a["nombre"]}


init()
