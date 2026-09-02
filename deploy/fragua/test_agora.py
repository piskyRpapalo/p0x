#!/usr/bin/env python3
"""Pruebas del Agora contra la API viva. Se corren EN la-fragua.

Aqui viven porque aqui esta `pynacl`: firmar de verdad es la unica forma de
comprobar que la verificacion sirve. Una prueba que simulara la firma estaria
comprobando el simulador.

    ~/venvs/agora/bin/python test_agora.py
"""
import json
import sys
import urllib.error
import urllib.request

from nacl.signing import SigningKey

BASE = "http://127.0.0.1:9002/api/v1"


def pide(ruta, cuerpo=None):
    datos = json.dumps(cuerpo).encode() if cuerpo is not None else None
    req = urllib.request.Request(BASE + ruta, data=datos,
                                 headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=10) as r:
            return r.status, json.loads(r.read())
    except urllib.error.HTTPError as e:
        return e.code, json.loads(e.read() or b"{}")


def firma_de(sk, pseudo, pub, reto):
    return sk.sign(f"{pseudo}|{pub}|{reto}".encode()).signature.hex()


fallos = []


def caso(nombre, cond, detalle=""):
    print(f"  {'ok   ' if cond else 'FALLO'} {nombre}" + (f" · {detalle}" if detalle else ""))
    if not cond:
        fallos.append(nombre)


sk = SigningKey.generate()
pub = sk.verify_key.encode().hex()
yo = "Tester-FIRMA"

# 1 · el camino honrado
_, r = pide("/reto")
reto = r["reto"]
c, r = pide("/profiles", {"pseudonimo": yo, "clave_publica": pub, "reto": reto,
                          "firma": firma_de(sk, yo, pub, reto)})
caso("perfil con firma valida", c == 201 and r.get("firma_verificada") is True, f"HTTP {c}")

# 2 · el reto no se puede reusar
c, r = pide("/profiles", {"pseudonimo": yo + "2", "clave_publica": pub, "reto": reto,
                          "firma": firma_de(sk, yo + "2", pub, reto)})
caso("un reto usado se rechaza", c == 403 and "una sola vez" in str(r), f"HTTP {c}")

# 3 · firma corrupta
_, r = pide("/reto"); reto = r["reto"]
mala = firma_de(sk, yo, pub, reto)
mala = ("0" if mala[0] != "0" else "1") + mala[1:]
c, r = pide("/profiles", {"pseudonimo": "Tester-MALA", "clave_publica": pub,
                          "reto": reto, "firma": mala})
caso("firma corrupta se rechaza", c == 403, f"HTTP {c}")

# 4 · la clave de OTRO: se firma con la propia y se manda la ajena
otra = SigningKey.generate()
_, r = pide("/reto"); reto = r["reto"]
c, r = pide("/profiles", {"pseudonimo": "Tester-LADRON",
                          "clave_publica": otra.verify_key.encode().hex(),
                          "reto": reto,
                          "firma": firma_de(sk, "Tester-LADRON",
                                            otra.verify_key.encode().hex(), reto)})
caso("firmar con la clave de otro se rechaza", c == 403, f"HTTP {c}")

# 5 · elegir companero, firmado
_, r = pide("/reto"); reto = r["reto"]
c, r = pide("/agents/select", {"pseudonimo": yo, "agente": "instalador",
                               "reto": reto, "firma": firma_de(sk, yo, pub, reto)})
caso("elegir companero con firma valida", c == 200 and r.get("adaptador"), f"HTTP {c}")

# 6 · elegir por otro, con la propia clave
_, r = pide("/reto"); reto = r["reto"]
c, r = pide("/agents/select", {"pseudonimo": yo, "agente": "instalador",
                               "reto": reto,
                               "firma": firma_de(otra, yo, pub, reto)})
caso("elegir en nombre de otro se rechaza", c == 403, f"HTTP {c}")

# 7 · el catalogo sigue siendo honesto
c, r = pide("/agents")
caso("catalogo 1 de 8", r.get("disponibles") == 1 and r.get("total") == 8,
     f"{r.get('disponibles')}/{r.get('total')}")


# --- El Agora que la web ya llama · perfiles con ficha y tablon -------------
#
# Estos casos son TDD: se escribieron antes que los endpoints. `profile.html` y
# `community.html` estan desplegadas y hoy caen a NO_DATA porque estas tres
# rutas no existen. Lo que se comprueba aqui es el contrato que esas dos
# paginas ya hablan, no uno nuevo inventado para la ocasion.

# 8 · el tablon existe y dice CUANTOS hilos reales hay
c, r = pide("/threads")
caso("GET /threads responde con lista", c == 200 and isinstance(r.get("hilos"), list),
     f"HTTP {c}")

# 9 · y no finge actividad: si no hay comunidad, el contador es 0 y se declara
caso("el tablon declara sus hilos reales",
     r.get("hilos_reales") == len(r.get("hilos", [])),
     f"hilos_reales={r.get('hilos_reales')} len={len(r.get('hilos', []))}")

# 10 · la ficha del perfil creado arriba, por pseudonimo
c, r = pide(f"/profiles/{yo}")
caso("GET /profiles/<pseudonimo>", c == 200 and r.get("pseudonimo") == yo, f"HTTP {c}")

# 11 · «huella» es tambien la clave publica entera: es como la llama auth.js
#      («la huella completa») y es lo que ensena profile.html en su <details>.
c, r = pide(f"/profiles/{pub}")
caso("GET /profiles/<clave_publica>", c == 200 and r.get("pseudonimo") == yo, f"HTTP {c}")

# 12 · quien no existe es 404, no una ficha vacia
c, r = pide("/profiles/Tester-NADIE")
caso("perfil desconocido es 404", c == 404, f"HTTP {c}")

# 13 · guardar bio y avatar. La firma cubre el CONTENIDO, no solo la identidad
_, r = pide("/reto"); reto = r["reto"]
BIO = "## Quien soy\n- Mido cosas\n- No invento numeros"
AV = "ojo"
msg = f"{yo}|{pub}|{reto}|{AV}|{BIO}"
c, r = pide("/profiles", {"pseudonimo": yo, "clave_publica": pub, "reto": reto,
                          "bio": BIO, "avatar": AV,
                          "firma": sk.sign(msg.encode()).signature.hex()})
caso("guardar bio y avatar firmados", c == 200 and r.get("nuevo") is False,
     f"HTTP {c}")

# 14 · y la ficha los devuelve
c, r = pide(f"/profiles/{yo}")
caso("la ficha devuelve bio y avatar",
     r.get("bio") == BIO and r.get("avatar") == AV,
     f"avatar={r.get('avatar')}")

# 15 · LA TRAMPA. Una firma de los TRES campos de siempre no puede colar una
#      bio: si valiera, cualquiera con un reto firmado podria escribir en la
#      ficha de otro sin firmar lo que escribe.
_, r = pide("/reto"); reto = r["reto"]
c, r = pide("/profiles", {"pseudonimo": yo, "clave_publica": pub, "reto": reto,
                          "bio": "bio inyectada", "avatar": AV,
                          "firma": firma_de(sk, yo, pub, reto)})
caso("firma sin contenido no puede escribir bio", c == 403, f"HTTP {c}")

# 16 · y no la escribio
c, r = pide(f"/profiles/{yo}")
caso("la bio anterior sigue intacta", r.get("bio") == BIO, f"bio={str(r.get('bio'))[:20]}")

# 17 · las medidas NO se inventan: el Agora no tiene ledger, y lo dice
c, r = pide(f"/profiles/{yo}")
caso("scores es NO_DATA con causa",
     r.get("scores") is None and bool(r.get("scores_causa")),
     str(r.get("scores_causa"))[:40])

# 18 · un avatar que no es un identificador se rechaza en la puerta
_, r = pide("/reto"); reto = r["reto"]
malo = "../../etc/passwd"
msg = f"{yo}|{pub}|{reto}|{malo}|"
c, r = pide("/profiles", {"pseudonimo": yo, "clave_publica": pub, "reto": reto,
                          "bio": "", "avatar": malo,
                          "firma": sk.sign(msg.encode()).signature.hex()})
caso("avatar con forma invalida se rechaza", c == 422, f"HTTP {c}")


print(f"\n{'VERDE' if not fallos else 'ROJO'} · {18 - len(fallos)}/18")
sys.exit(1 if fallos else 0)
