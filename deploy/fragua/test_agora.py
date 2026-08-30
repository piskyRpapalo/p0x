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

print(f"\n{'VERDE' if not fallos else 'ROJO'} · {7 - len(fallos)}/7")
sys.exit(1 if fallos else 0)
