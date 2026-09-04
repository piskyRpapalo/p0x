#!/usr/bin/env bash
# probar-teclado-doogee.sh · el punto ciego de la app, medido en un telefono.
#
# sistema: instrumento de medicion del nodo `soberano`. **No es parte del
# producto.** Vive aqui y no en `preceptor/bin/` porque depende de `adb` y de un
# aparato concreto enchufado a ESTA maquina: es capacidad del nodo, no del MVP.
#
# POR QUE EXISTE
# --------------
# `dashboard.js` ajusta la altura de la app con `visualViewport` para que el
# teclado de Android no tape el campo de escribir. Eso NO lo puede comprobar
# ningun gate: `bin/pruebas` no abre un teclado, y el navegador del arnes
# tampoco --no hay forma de emular un teclado de Android en un escritorio--.
# Durante semanas fue codigo que se creia bueno porque nadie tenia como mirarlo.
#
# Este guion lo mira. Deja tres capturas y las compara por tamano; el veredicto
# de verdad lo da el carbono abriendolas, porque lo que se juzga es si el campo
# queda encima del teclado, y eso se ve, no se calcula.
#
# LO QUE NO HACE
# --------------
# * No escribe en el chat ni manda un turno. Con el chat VACIO se comprueba que
#   el campo no queda tapado; que el chat haga scroll al ultimo mensaje exige
#   contenido y es otra prueba.
# * No toca el telefono mas alla de abrir una URL, un toque y un `BACK`.
set -uo pipefail

PUERTO="${P0X_MVP_PUERTO:-8740}"
RUTA="${P0X_MVP_RUTA:-/dashboard.html}"
SALIDA="${P0X_SALIDA:-${TMPDIR:-/tmp}/teclado-doogee}"
# Coordenadas del campo de escribir en 1080x2408. Si cambia el telefono o el
# alto de la barra de iconos, esto se vuelve a mirar en la primera captura --y
# se nota porque el teclado no se abre, no porque falle nada.
TAP_X="${P0X_TAP_X:-444}"
TAP_Y="${P0X_TAP_Y:-1914}"

die() { printf '\n  ABORTA · %s\n\n' "$1" >&2; exit 1; }
foto() { adb exec-out screencap -p > "$SALIDA/$1.png" 2>/dev/null \
         || die "no pude capturar la pantalla"; }

command -v adb >/dev/null || die "no hay adb en el PATH"
adb devices | grep -qw device || die "ningun telefono en 'device' (mira 'adb devices -l')"
curl -sf -m 5 -o /dev/null "http://127.0.0.1:$PUERTO$RUTA" \
  || die "el MVP no responde en 127.0.0.1:$PUERTO$RUTA (arrancalo con preceptoros-servicio)"

mkdir -p "$SALIDA"
# El telefono ve NUESTRO servidor en su propio localhost. Sin esto abre su
# 127.0.0.1, que es el suyo, y sale un error de conexion que parece del MVP.
adb reverse "tcp:$PUERTO" "tcp:$PUERTO" >/dev/null || die "no pude hacer 'adb reverse'"

printf 'Abriendo %s en el telefono...\n' "$RUTA"
adb shell am start -a android.intent.action.VIEW \
  -d "http://127.0.0.1:$PUERTO$RUTA" >/dev/null 2>&1
sleep 8;  foto 0-cerrado

printf 'Tocando el campo de escribir (%s,%s) para abrir el teclado...\n' "$TAP_X" "$TAP_Y"
adb shell input tap "$TAP_X" "$TAP_Y" >/dev/null 2>&1
sleep 5;  foto 1-abierto

printf 'Cerrando el teclado...\n'
adb shell input keyevent KEYCODE_BACK >/dev/null 2>&1
sleep 4;  foto 2-cerrado

printf '\nTres capturas en %s\n\n' "$SALIDA"
for f in 0-cerrado 1-abierto 2-cerrado; do
  printf '  %-12s %s bytes\n' "$f" "$(stat -c%s "$SALIDA/$f.png")"
done

# El tamano NO es el veredicto: es una pista barata. Un teclado es una mancha
# plana y comprime mucho, asi que la de en medio pesa bastante menos. Y si la
# primera y la tercera se parecen, la app volvio a su sitio al cerrarlo.
a=$(stat -c%s "$SALIDA/0-cerrado.png"); c=$(stat -c%s "$SALIDA/2-cerrado.png")
dif=$(( a > c ? a - c : c - a ))
printf '\n  cerrado vs recuperado: %s bytes de diferencia' "$dif"
if [ "$dif" -lt $(( a / 20 )) ]; then
  printf '  -> la app volvio a su sitio\n'
else
  printf '  -> MIRALAS: no volvio igual\n'
fi

cat <<'FIN'

  Lo que hay que MIRAR en 1-abierto.png, que es lo que el gate no puede:
    · el campo de escribir esta ENTERO y encima del teclado (no debajo)
    · el chat se ve por encima del campo, encogido pero presente
    · la barra de iconos del pie NO se ve: es correcto, la app mide lo visible
  Y en 2-cerrado.png: identica a 0-cerrado.png, con la barra de vuelta.
FIN
