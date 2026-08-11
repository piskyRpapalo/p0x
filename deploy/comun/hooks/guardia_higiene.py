#!/usr/bin/env python3
"""Guardia de higiene P0X — escáner de fugas de infraestructura.

Regla del proyecto: nada que identifique la infraestructura sale a un
repositorio público. Direcciones de red, nombres de host **como dirección**,
usuarios en ruta, rutas absolutas del sistema, dominios de red privada, claves
o tokens.

Los nombres de nodo (Soberano, Fragua, Vigía, Torre) son léxico de doctrina y
aparecen legítimamente en prosa castellana. Por eso NO se busca la palabra
suelta: se buscan FORMAS DE DIRECCIÓN — las maneras en que un nombre de máquina
aparece de verdad en un fichero.

Modos:
    guardia_higiene.py --diff            lee un diff unificado por stdin
    guardia_higiene.py --files F [F...]  escanea ficheros completos

Salida: una línea por hallazgo `RUTA:LINEA: [REGLA] texto`. Código de salida 1
si hay hallazgos, 0 si no.

Escape declarado: una línea que contenga `guardia:permitir <motivo>` se ignora.
Es desviación mínima aditiva declarada, no un silenciador genérico.
"""

from __future__ import annotations

import argparse
import re
import sys

# --- Decisiones firmadas que permiten patrones especificos (D8, D10) ---
#
# D18: la exencion se evalua POR REGLA, nunca sobre la linea completa. Antes,
# un patron de D8 en cualquier parte de la linea eximia la linea ENTERA: un
# token ghp_ pasaba sin reportarse si la linea mencionaba /home/pisky/. Una
# comprobacion que detecta y deja pasar no es comprobacion (04_CONTRATO §3.7).
DECISIONES_FIRMADAS = {
    'D8': {
        'reglas': frozenset({
            'IP-RFC1918',
            'RUTA-HOME',
            'DOMINIO-PRIVADO',
            'NODO-URL',
            'NODO-HOST-PATH',
        }),
        'patrones': [
            r'/home/pisky/',
            r'10\.\d+\.\d+\.\d+',
            r'192\.168\.\d+\.\d+',
            r'localhost',
            r'tailscale',
            r'soberano\.',
            r'fragua:',
        ],
    },
    'D10': {
        'reglas': frozenset({'TOKEN-PROVEEDOR'}),
        'patrones': [
            r'AKIAIOSFODNN7EXAMPLQ',
            r'ghp_[A-Za-z0-9]+_FIXTURE',
        ],
    },
}

# Suelo duro de D8: estas reglas no se eximen por una ruta local ni por una
# mencion de red. D10 conserva la potestad de eximir TOKEN-PROVEEDOR, pero
# solo con sus dos patrones literales de fixture.
D8_JAMAS = frozenset({'TOKEN-PROVEEDOR', 'IP-TAILNET', 'CLAVE-PRIVADA'})

# D23: la exencion documental solo aplica a los entregables donde el Soberano
# autorizo citar rutas e IPs. Fuera de estas dos carpetas manda
# 04_CONTRATO_CLAUDE_CODE §3.5: cero rutas de usuario, cero IPs de tailnet.
# D8 no autoriza commits con rutas o IPs en el resto del arbol.
RUTAS_CANON_D23 = re.compile(
    r"(?:^|/)(?:Cuarentena/salida|docs/post_verificacion)/"
)

assert not (DECISIONES_FIRMADAS['D8']['reglas'] & D8_JAMAS), (
    'D8 no puede eximir TOKEN-PROVEEDOR, IP-TAILNET ni CLAVE-PRIVADA (D18)'
)


def es_permitido_por_canon(linea, regla_id):
    """Decision firmada que exime a ESTA regla en ESTA linea, o None.

    `regla_id` es obligatorio a proposito: sin valor por defecto, cualquier
    llamada al estilo antiguo revienta con TypeError en vez de eximir en
    silencio. Ver D18.
    """
    for d_id, decision in DECISIONES_FIRMADAS.items():
        if regla_id not in decision['reglas']:
            continue
        for p in decision['patrones']:
            if re.search(p, linea):
                return f'PERMITIDO-POR-{d_id}'
    return None

# --- Léxico de nodos (más largo primero, para que la alternancia no trunque) --
NODOS = (
    r"musculo-hp-0[0-9]|la-fragua|el-vig[ií]a|la-torre|soberano|fragua|"
    r"vig[ií]a|torre|jetson|beato"
)
# Cuentas de sistema que nunca son léxico doctrinal en posición de dirección.
USUARIOS = r"pisky|jetson|soberano|ubuntu|root|admin"

PLACEHOLDERS = re.compile(
    r"XXX|<[A-Za-z_]|\$\{|\$[A-Z_]{3,}|EJEMPLO|EXAMPLE|REDACT|PLACEHOLDER|"
    r"TU_|YOUR_|FIXME|NODO_|USUARIO\b|USER\b|\.\.\.",
    re.IGNORECASE,
)

PRAGMA = re.compile(r"guardia:permitir\s+\S")

# Ficheros que SON el corpus de prueba del propio guardia: contienen fugas
# a propósito. Escanearlos sería morderse la cola.
EXENTOS = re.compile(r"(^|/)deploy/comun/hooks/")


def _r(p: str) -> re.Pattern:
    return re.compile(p, re.IGNORECASE)


# (id, descripción, patrón)
REGLAS: list[tuple[str, str, re.Pattern]] = [
    # ---------------------------------------------------------------- redes --
    (
        "IP-TAILNET",
        "IP del rango privado de la red superpuesta (100.64.0.0/10)",
        _r(r"\b100\.(?:6[4-9]|[7-9][0-9]|1[01][0-9]|12[0-7])"
           r"\.[0-9]{1,3}\.[0-9]{1,3}\b"),
    ),
    (
        "IP-RFC1918",
        "IP de red privada (RFC1918)",
        _r(r"\b(?:10\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}"
           r"|192\.168\.[0-9]{1,3}\.[0-9]{1,3}"
           r"|172\.(?:1[6-9]|2[0-9]|3[01])\.[0-9]{1,3}\.[0-9]{1,3})\b"),
    ),
    (
        "DOMINIO-PRIVADO",
        "nombre de dominio de red privada",
        _r(r"\b[A-Za-z0-9-]+\.(?:ts\.net|lan|internal|home\.arpa)\b"
           r"|\btail[a-z0-9]{6,}\b"
           r"|[@/]\s*[A-Za-z0-9-]+\.local\b"
           r"|\b(?:" + NODOS + r"|p0x|hexelion|aurelius)\.local\b"),
    ),
    # -------------------------------------------------- rutas y usuarios ----
    (
        "RUTA-HOME",
        "ruta absoluta al directorio del usuario",
        # Los placeholders (/home/USUARIO, /home/$USER) los filtra PLACEHOLDERS
        # sobre el texto capturado; no van en un lookahead porque IGNORECASE
        # haría que `[A-Z]{3,}` casara también con minúsculas reales.
        _r(r"/home/(?![<$\{])[A-Za-z0-9._-]+"
           r"|~(?:" + USUARIOS + r")\b"
           r"|[A-Z]:\\Users\\[A-Za-z0-9._-]+"),
    ),
    # -------------------------- nodo EN FORMA DE DIRECCIÓN (no la palabra) --
    (
        "NODO-USER-AT",
        "nodo como destino de conexión (usuario@host)",
        _r(r"\b[A-Za-z0-9._-]+@(?:" + NODOS + r")\b"),
    ),
    (
        "NODO-HOST-PATH",
        "nodo seguido de dos puntos y ruta o puerto (host:/ruta, host:puerto)",
        _r(r"\b(?:" + NODOS + r")(?:\.[A-Za-z0-9.-]+)?:(?:/|~|[0-9]{2,5}\b)"),
    ),
    (
        "NODO-DOMINIO",
        "nodo dentro de un dominio de red",
        _r(r"\b(?:" + NODOS + r")\.(?:ts\.net|local|lan|internal|tail[a-z0-9]+)"),
    ),
    (
        "NODO-COMANDO",
        "nodo como argumento de un comando de conexión remota",
        _r(r"\b(?:ssh|scp|rsync|sftp|mosh|ssh-copy-id|ssh-keyscan|telnet)\s+"
           r"(?:-{1,2}[A-Za-z0-9-]+(?:[= ]\S+)?\s+)*"
           r"(?:[A-Za-z0-9._-]+@)?(?:" + NODOS + r")\b"),
    ),
    (
        "NODO-SSH-CONFIG",
        "nodo declarado en configuración SSH (Host/HostName)",
        _r(r"^\s*(?:Host|HostName)\s+\S*(?:" + NODOS + r")\S*\s*$"),
    ),
    (
        "NODO-URL",
        "nodo dentro de una URL",
        _r(r"\b[a-z][a-z0-9+.-]*://[^\s/'\"]*\b(?:" + NODOS + r")\b"),
    ),
    (
        "NODO-PROMPT",
        "prompt de terminal copiado (usuario@host …$)",
        _r(r"[\[(]?[A-Za-z0-9._-]+@(?:" + NODOS + r")\b[^\n]{0,60}?[$#]"),
    ),
    (
        "USUARIO-FLAG",
        "usuario del sistema en posición de argumento",
        _r(r"(?:^|\s)(?:-l|-u|--user(?:name)?[= ]|User\s+|useradd\s+|sudo\s+-u\s+)"
           r"(?:" + USUARIOS + r")\b"),
    ),
    # --------------------------------------------------- claves y tokens ----
    (
        "CLAVE-PRIVADA",
        "bloque de clave privada",
        _r(r"-----BEGIN (?:[A-Z0-9 ]+ )?PRIVATE KEY-----"),
    ),
    (
        "CLAVE-PUBLICA-SSH",
        "clave pública SSH completa (identifica la máquina)",
        _r(r"\bssh-(?:rsa|ed25519|dss)\s+AAAA[0-9A-Za-z+/=]{20,}"),
    ),
    (
        "TOKEN-PROVEEDOR",
        "token con forma de credencial de proveedor",
        _r(r"\bgh[pousr]_[A-Za-z0-9]{16,}"
           r"|\bgithub_pat_[A-Za-z0-9_]{20,}"
           r"|\bsk-(?:ant-)?[A-Za-z0-9_-]{20,}"
           r"|\bAKIA[0-9A-Z]{16}\b"
           r"|\bxox[baprs]-[A-Za-z0-9-]{10,}"
           r"|\bed25519:[0-9A-Za-z]{40,}"),
    ),
    (
        "SECRETO-ASIGNADO",
        "variable con nombre de secreto y valor literal",
        _r(r"\b(?:api[_-]?key|secret(?:_key)?|access[_-]?token|auth[_-]?token"
           r"|password|passwd|contrase[nñ]a|private[_-]?key)\b"
           # El valor debe ser un literal: se descartan llamadas a función
           # (api_key=_load_api_key()) y lecturas de entorno.
           r"\s*[:=]\s*(?!os\.|process\.|getenv|_load|load_|None\b|null\b)"
           r"[\"']?(?![A-Za-z_][A-Za-z0-9_.]*\s*\()[^\s\"',;]{12,}"),
    ),
]


def escanear_lineas(ruta: str, lineas: list[tuple[int, str]]) -> list[str]:
    """Devuelve hallazgos `ruta:linea: [REGLA] texto` para las líneas dadas."""
    if EXENTOS.search(ruta):
        return []
    # La exencion de D8/D10 vive solo en las carpetas de entregable (D23).
    canon_d23 = bool(RUTAS_CANON_D23.search(ruta))
    hallazgos: list[str] = []
    for num, texto in lineas:
        if PRAGMA.search(texto):
            continue
        for rid, _desc, patron in REGLAS:
            m = patron.search(texto)
            if not m:
                continue
            if PLACEHOLDERS.search(m.group(0)):
                continue
            # La exencion se consulta AQUI, con la regla que acaba de saltar.
            # El `continue` sigue recorriendo REGLAS: una linea con una IP
            # privada eximida y ademas un token se reporta por el token.
            if canon_d23 and es_permitido_por_canon(texto, rid):
                continue
            recorte = texto.strip()
            if len(recorte) > 160:
                recorte = recorte[:157] + "…"
            hallazgos.append(f"{ruta}:{num}: [{rid}] {recorte}")
            break  # una regla por línea basta para bloquear
    return hallazgos


CAB_FICHERO = re.compile(r"^\+\+\+ (?:b/)?(.+?)(?:\t.*)?$")
CAB_HUNK = re.compile(r"^@@ -[0-9]+(?:,[0-9]+)? \+([0-9]+)(?:,[0-9]+)? @@")


def escanear_diff(texto: str) -> list[str]:
    """Escanea SOLO las líneas añadidas de un diff unificado.

    Las líneas eliminadas no se miran: borrar una fuga no es cometerla. El
    gancho anterior escaneaba el diff entero y bloqueaba también los borrados.
    """
    hallazgos: list[str] = []
    ruta = "(desconocido)"
    n = 0
    pendientes: dict[str, list[tuple[int, str]]] = {}
    for linea in texto.splitlines():
        m = CAB_FICHERO.match(linea)
        if m:
            ruta = m.group(1)
            if ruta == "/dev/null":
                ruta = "(borrado)"
            continue
        m = CAB_HUNK.match(linea)
        if m:
            n = int(m.group(1))
            continue
        if linea.startswith("+++") or linea.startswith("---"):
            continue
        if linea.startswith("+"):
            pendientes.setdefault(ruta, []).append((n, linea[1:]))
            n += 1
        elif linea.startswith("-") or linea.startswith("\\"):
            continue
        else:
            n += 1
    for ruta, lineas in pendientes.items():
        hallazgos.extend(escanear_lineas(ruta, lineas))
    return hallazgos


def escanear_ficheros(rutas: list[str]) -> list[str]:
    hallazgos: list[str] = []
    for ruta in rutas:
        try:
            with open(ruta, "r", encoding="utf-8", errors="replace") as fh:
                lineas = [(i, l.rstrip("\n")) for i, l in enumerate(fh, 1)]
        except (OSError, IsADirectoryError):
            continue
        hallazgos.extend(escanear_lineas(ruta, lineas))
    return hallazgos


def main() -> int:
    ap = argparse.ArgumentParser(description="Guardia de higiene P0X")
    ap.add_argument("--diff", action="store_true",
                    help="leer un diff unificado por stdin")
    ap.add_argument("--files", nargs="*", default=None,
                    help="escanear ficheros completos")
    args = ap.parse_args()

    if args.diff:
        hallazgos = escanear_diff(sys.stdin.read())
    elif args.files is not None:
        hallazgos = escanear_ficheros(args.files)
    else:
        ap.error("indica --diff o --files")
        return 2

    for h in hallazgos:
        print(h)
    return 1 if hallazgos else 0


if __name__ == "__main__":
    sys.exit(main())
