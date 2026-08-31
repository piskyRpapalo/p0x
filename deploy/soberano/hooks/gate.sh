#!/usr/bin/env bash
# El gate como LEY, no como memoria.
#
# Hook PostToolUse: tras cada escritura, corre el gate del repo que se ha
# tocado. Si cae, sale con 2 -- que es como un hook le dice al modelo «esto
# esta rojo, no sigas». No depende de que nadie se acuerde de correr pytest.
#
# Por que un script y no una linea en settings.json: la linea no se puede
# leer, ni probar, ni versionar. Esto vive en el repo y se ejecuta a mano
# igual que lo ejecuta el hook -- si un dia falla, se depura como codigo.
set -uo pipefail

# Derivadas de $HOME: una ruta de home incrustada solo vale en la maquina
# donde se escribio, y este fichero esta versionado para todo el rack.
WEB="$HOME/preceptoros-web"
MVP="$HOME/p0x/preceptor"

# La ruta llega en el JSON del hook por stdin. jq no esta garantizado en este
# nodo, asi que se saca con python3, que si es doctrina de la casa.
ENTRADA="$(cat)"
RUTA="$(printf '%s' "$ENTRADA" | python3 -c '
import json,sys
try: d=json.load(sys.stdin)
except Exception: print(""); raise SystemExit
i=d.get("tool_input") or {}
print(i.get("file_path") or i.get("notebook_path") or i.get("command") or "")
' 2>/dev/null)"

fallo=0
informe=""

# El gate de la web tarda 0,25 s: se corre entero, sin filtrar por fichero.
# Filtrar por fichero es justo como se cuela una rotura cruzada.
if printf '%s' "$RUTA" | grep -q "preceptoros-web"; then
  if ! salida="$(cd "$WEB" && timeout 300 python3 -m pytest test_web.py -q 2>&1)"; then
    informe+=$'GATE WEB EN ROJO\n'"$(printf '%s' "$salida" | tail -25)"$'\n'
    fallo=1
  else
    # NO se llama a contadores.py aqui, y la razon esta MEDIDA (2026-08-31):
    # `contadores.py` solo mide el Agora, asi que borra `pruebas_app` y
    # `pruebas_web` de counters.json y deja el gate ROJO en dos pruebas.
    # Quien mide de verdad es `p0x/bin/coherencia-publica.py`, que corre los
    # dos gates -- y ademas reescribe la linea de credenciales de las tres
    # portadas, que van a 311 B del tope. Eso no puede pasar como efecto
    # secundario de cada tecla: es un acto deliberado antes del commit.
    if printf '%s' "$RUTA" | grep -q "preceptoros-web/public/"; then
      informe+=$'recuerda antes del commit: python3 ~/p0x/bin/coherencia-publica.py --si\n'
    fi
    informe+="gate web VERDE · $(printf '%s' "$salida" | tail -1)"$'\n'
  fi
fi

if printf '%s' "$RUTA" | grep -q "p0x/preceptor/"; then
  if ! salida="$(cd "$MVP" && timeout 600 python3 -m pytest -q 2>&1)"; then
    informe+=$'GATE MVP EN ROJO\n'"$(printf '%s' "$salida" | tail -25)"$'\n'
    fallo=1
  else
    informe+="gate MVP VERDE · $(printf '%s' "$salida" | tail -1)"$'\n'
  fi
fi

[ -n "$informe" ] && printf '%s' "$informe" >&2
exit $((fallo * 2))
