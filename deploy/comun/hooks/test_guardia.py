#!/usr/bin/env python3
"""Casos de prueba del guardia de higiene.

DEBEN PASAR   → prosa doctrinal legítima; el nodo aparece como sustantivo.
DEBEN BLOQUEAR→ el nodo aparece como dirección, o hay IP/ruta/dominio/clave.

Un freno con falsos positivos acaba desactivado por costumbre; eso lo convierte
en ningún freno. Estos casos son la prueba de que el freno frena lo que debe y
solo lo que debe.

    python3 test_guardia.py
"""

import sys

from guardia_higiene import escanear_lineas

# --------------------------------------------------------------------------
# DEBEN PASAR — prosa castellana con el léxico doctrinal
# --------------------------------------------------------------------------
PASAN = [
    "El Soberano decide; la sesión de frontera solo propone.",
    "soberano es el único nodo que tocas directamente.",
    "La Fragua encola el trabajo pesado y vigila su térmica.",
    "El Vigía escucha AIS y ADS-B con su SDR.",
    "La Torre aloja el Sínodo v2 con RAG.",
    "Canon del nodo (registro de decisiones del Soberano)",
    "| **soberano** (aquí) | Cerebro central de cómputo | Radeon 780M |",
    "La torre: el nodo git soberano del rack.",
    "Hexelion es la parte física; Aurelius el aprendizaje; P0X la suma.",
    "commit por bloque, push soberano.",
    "Se despliega en deploy/soberano/ según la convención del repo.",
    "La fragua y la torre se reparten el batch.",
    "El Preceptor (Fable 5) valida la doctrina fuera del rack.",
    "musculo-hp-02 no es un músculo: es un Chromebook con 7.6 GiB.",
    "Ver mente/doctrina/ORQUESTA_DE_MODELOS.md §2 para el reparto.",
    "export OLLAMA_IGPU_ENABLE=1  # backend Vulkan del Soberano",
    "ssh es el transporte; la Torre es el destino habitual.",  # prosa, no comando
    "Versión del kernel: 6.14.0-29-generic",
    "Puerto 11434 para Ollama, 8080 para el dashboard.",
    "La clave privada de firma jamás entra a este nodo.",
    "ruta de ejemplo: /home/USUARIO/p0x  # placeholder genérico",
    "connect to $HOME/p0x/bin/p0x-enqueue",
    "API_KEY=${OPENAI_API_KEY}",
    "token: <TU_TOKEN_AQUI>",
    "IP de ejemplo documental: 203.0.113.7",
    "QdrantClient(host=_Q['host'], api_key=_load_api_key(), https=False)",
    "password = os.environ['QDRANT_PASSWORD']",
    "loopback: 127.0.0.1 y ::1",
    # D34 · el loopback NO es infraestructura identificable: no dice nada de
    # que maquina es ni de que red forma parte. Casos explicitos y separados,
    # no una sola linea que los mezcle. Son guardas de regresion: ninguna
    # regla los ha capturado nunca, asi que no pueden salir en rojo antes del
    # arreglo; existen para que una futura ampliacion de las reglas de red no
    # se los lleve por delante en silencio.
    "bind 127.0.0.1 para el dashboard local",
    "escucha en ::1 (loopback IPv6)",
]

# --------------------------------------------------------------------------
# DEBEN BLOQUEAR — formas de dirección, IPs privadas, rutas, dominios, claves
# --------------------------------------------------------------------------
BLOQUEAN = [
    # nodo como dirección
    ("pisky@soberano:~/p0x$ git status", "NODO-USER-AT"),
    ("jetson@la-torre.tailb9e0f7.ts.net", "DOMINIO-PRIVADO"),
    ("scp informe.md torre:/srv/p0x/entrada/", "NODO-HOST-PATH"),
    ("rsync -av ./deploy/ fragua:~/deploy/", "NODO-HOST-PATH"),
    ("ssh soberano 'ollama ps'", "NODO-COMANDO"),
    ("ssh -p 22 jetson", "NODO-COMANDO"),
    ("curl http://fragua:11434/api/tags", "NODO-HOST-PATH"),
    ("origin\tssh://jetson@la-torre/~/hexelion.git", "NODO-USER-AT"),
    ("  HostName la-torre.tailb9e0f7.ts.net", "DOMINIO-PRIVADO"),
    ("Host la-torre", "NODO-SSH-CONFIG"),
    ("ping el-vigia.local -c 3", "DOMINIO-PRIVADO"),
    ("apunta a vigia.internal desde el rack", "NODO-DOMINIO"),
    ("[pisky@soberano ~]$ uname -a", "NODO-USER-AT"),
    # IPs privadas
    ("tailnet 100.81.82.34", "IP-TAILNET"),
    ("IP 100.81.82.34  <!-- guardia:permitir doc interna, no se publica -->", "IP-TAILNET"),  # D8_JAMAS nunca se exime
    ("la-fragua responde en 100.82.94.83:6333", "IP-TAILNET"),
    ("gateway 192.168.1.1", "IP-RFC1918"),
    ("bind 10.0.0.5", "IP-RFC1918"),
    ("docker net 172.17.0.2", "IP-RFC1918"),
    # rutas y usuarios
    ("cat /home/pisky/p0x/mente/doctrina/README.md", "RUTA-HOME"),
    ("WorkingDirectory=/home/pisky/hexelion", "RUTA-HOME"),
    ("cd ~pisky/.ssh", "RUTA-HOME"),
    ("ssh -l pisky torre", "NODO-COMANDO"),
    # dominios de red privada
    ("email: soberano@p0x.local", "DOMINIO-PRIVADO"),
    ("resolver: nexo.lan", "DOMINIO-PRIVADO"),
    ("magic dns: tailb9e0f7.ts.net", "DOMINIO-PRIVADO"),
    # claves y tokens
    ("-----BEGIN OPENSSH PRIVATE KEY-----", "CLAVE-PRIVADA"),
    ("ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIKq3mS0nR7wQ2vB5xY8pL1dTgH4uJ6cF",
     "CLAVE-PUBLICA-SSH"),
    ("GH_TOKEN=ghp_A1b2C3d4E5f6G7h8I9j0K1l2M3n4O5p6Q7r8", "TOKEN-PROVEEDOR"),
    ("ANTHROPIC=sk-ant-api03-QQQwwweeerrrtttyyyuuuiiiooo", "TOKEN-PROVEEDOR"),
    ("aws: AKIAIOSFODNN7EXAMPLQ", "TOKEN-PROVEEDOR"),
    ('api_key: "8f14e45fceea167a5a36dedd4bea2543"', "SECRETO-ASIGNADO"),
    ("password=Tr0ub4dor&3xKw7bHq99", "SECRETO-ASIGNADO"),
    # D18 · caso rojo: la exencion de D8 por ruta local NO puede tapar
    # un token. Con el codigo anterior esta linea no daba hallazgo.
    ("ruta /home/pisky/p0x y token "
     "ghp_A1b2C3d4E5f6G7h8I9j0K1l2M3n4O5p6Q7r8",
     "TOKEN-PROVEEDOR"),
    # D34 · PUNTO CIEGO DE RUTAS ABSOLUTAS · UN CASO ROJO POR PREFIJO.
    # La regla cubria /home y nada mas: los otros cinco prefijos salian del
    # arbol sin un solo hallazgo. Un prefijo sin su caso rojo es un prefijo
    # que nadie ha demostrado que la regla cubra.
    # /tmp queda FUERA por decision firmada (falsos positivos); se revisa en
    # R02 con datos. No se anade aqui por simetria estetica.
    ("cat /home/pisky/p0x/mente/doctrina/ORQUESTA.md", "RUTA-HOME"),
    ("respaldo montado en /mnt/nvme-1tb/p0x", "RUTA-HOME"),
    # Este caso vivia en PASAN hasta 2026-08-12. La enmienda de D34 lo
    # convierte en bloqueo: es una ruta absoluta del sistema, y que la frase
    # que la rodea sea prosa no la hace menos ruta. Movido PASAN -> BLOQUEAN
    # (endurecer). D23 prohibe el movimiento inverso, no este.
    ("Usa el árbol /srv/p0x en el nodo remoto.", "RUTA-HOME"),
    ("binario instalado en /opt/ollama/bin/ollama", "RUTA-HOME"),
    ("logs en /var/log/aurelius-interfaz.log", "RUTA-HOME"),
    ("usb del Soberano montado en /media/pisky/RESPALDO", "RUTA-HOME"),
]

# Excepción declarada: el pragma desactiva la línea, con motivo a la vista.
PRAGMA_OK = [
#     "IP 100.81.82.34  <!-- guardia:permitir doc interna, no se publica -->",  # MOVIDO A BLOQUEAN: D8_JAMAS nunca se exime
]


def main() -> int:
    fallos = 0

    print("── DEBEN PASAR " + "─" * 50)
    for texto in PASAN:
        h = escanear_lineas("doc/prueba.md", [(1, texto)])
        if h:
            fallos += 1
            print(f"  FALLO (falso positivo) · {texto}")
            for x in h:
                print(f"           ↳ {x}")
        else:
            print(f"  ok  · {texto[:68]}")

    print("\n── DEBEN BLOQUEAR " + "─" * 47)
    for texto, regla_esperada in BLOQUEAN:
        h = escanear_lineas("doc/prueba.md", [(1, texto)])
        if not h:
            fallos += 1
            print(f"  FALLO (falso negativo) · {texto}")
        else:
            regla = h[0].split("[")[1].split("]")[0]
            marca = "ok " if regla == regla_esperada else "ok*"
            if regla != regla_esperada:
                print(f"  {marca} · [{regla}] (esperaba {regla_esperada}) "
                      f"{texto[:44]}")
            else:
                print(f"  {marca} · [{regla}] {texto[:56]}")

    print("\n── PRAGMA DE EXCEPCIÓN " + "─" * 42)
    for texto in PRAGMA_OK:
        h = escanear_lineas("doc/prueba.md", [(1, texto)])
        if h:
            fallos += 1
            print(f"  FALLO (pragma ignorado) · {texto}")
        else:
            print(f"  ok  · {texto[:68]}")

    print("\n── EXENCIÓN DEL CORPUS PROPIO " + "─" * 35)
    h = escanear_lineas("deploy/comun/hooks/test_guardia.py",
                        [(1, "tailnet 100.81.82.34")])
    if h:
        fallos += 1
        print("  FALLO · el corpus del guardia no está exento")
    else:
        print("  ok  · deploy/comun/hooks/ exento (contiene fugas a propósito)")

    total = len(PASAN) + len(BLOQUEAN) + len(PRAGMA_OK) + 1
    print(f"\nRESULTADO: {total - fallos}/{total} casos correctos, "
          f"{fallos} fallo(s)")
    return 1 if fallos else 0


if __name__ == "__main__":
    sys.exit(main())
