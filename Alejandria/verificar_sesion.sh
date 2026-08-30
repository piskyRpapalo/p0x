#!/usr/bin/env bash
# verificar_sesion.sh · el cierre de sesion. OBLIGATORIO.
#
# Si esto no corre, el Ojo se queda STALE y la sesion siguiente arranca a
# ciegas -- o peor, arranca creyendo un documento que envejecio. Hoy se midio
# el coste de eso: seis tareas dadas por pendientes que ya estaban hechas, y
# cuatro servicios dados por rotos que estaban sanos.
#
# Cinco pasos, en este orden y no en otro:
#   1. medir el metal            (recolector.py --completo)
#   2. renderizar el snapshot    (informe.py)
#   3. absorber y calcular delta (continuidad.py absorber)
#   4. regenerar el arranque     (continuidad.py bootstrap)
#   5. delta.md + resumen.html   (resumen.py)
#   6. el digesto del Enlace     (digesto.py) -> acta + Ojo + continuidad.db
#
# El paso 3 va DESPUES del 1 porque el delta se calcula contra la instantanea
# anterior de la base: hay que meter la nueva para saber que cambio. Y el 4 va
# despues del 3 porque el arranque se genera de la base ya actualizada.
set -uo pipefail

RAIZ="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CONT="$HOME/p0x/preceptor-internal/continuidad"

# El nombre de sesion es el primer argumento QUE NO SEA UNA BANDERA.
#
# Antes era `${1:-...}` a secas, y eso convertia la primera bandera en el
# nombre: llamar `verificar_sesion.sh --email --a x@y.z` dejaba
# SESION="--email", que viajaba a los pasos 3, 5 y 6 como
# `--sesion --email` y argparse lo cortaba con «expected one argument».
#
# El fallo no tumbaba el cierre -- `paso()` declara y sigue -- asi que los tres
# pasos que escriben la continuidad, el resumen y el digesto caian a la vez y
# el cierre terminaba diciendo que habia fallado, sin mas. Un cierre a medias
# es exactamente como se pierde la linea.
SESION=""
MODO="--completo"
EMAIL=()
while [ $# -gt 0 ]; do
  case "$1" in
    --rapido) MODO="--rapido" ;;
    --email)  EMAIL+=(--email) ;;
    --a=*)    EMAIL+=(--a "${1#--a=}") ;;
    # `--a valor` separado por espacio, que es como se teclea de verdad.
    --a)      shift; [ $# -gt 0 ] || { echo "🔴 --a sin dirección" >&2; exit 2; }
              EMAIL+=(--a "$1") ;;
    -*)       echo "🔴 bandera desconocida: $1" >&2; exit 2 ;;
    *)        [ -z "$SESION" ] && SESION="$1" ;;
  esac
  shift
done
SESION="${SESION:-$(date +%Y-%m-%d)-sesion}"

echo "🏛  Cierre de sesión · $SESION"
echo

fallo=0
paso () {  # paso <rotulo> <comando...>
  local rotulo="$1"; shift
  printf '· %s\n' "$rotulo"
  if ! "$@"; then
    # Un paso que falla se DECLARA y no detiene el cierre: perder el resto del
    # cierre porque uno de cinco pasos fallo es exactamente como se pierde la
    # linea. Se sigue, y el fallo viaja en el reporte.
    echo "  🔴 falló: $rotulo"
    fallo=1
  fi
  echo
}

paso "1/6 · midiendo el metal"        python3 "$RAIZ/recolector.py" $MODO --historial
paso "2/6 · renderizando el snapshot" python3 "$RAIZ/informe.py"
paso "3/6 · absorbiendo el delta"     python3 "$CONT/continuidad.py" absorber --sesion "$SESION"
paso "4/6 · regenerando el arranque"  python3 "$CONT/continuidad.py" bootstrap
paso "5/6 · delta y resumen"          python3 "$RAIZ/resumen.py" --sesion "$SESION" "${EMAIL[@]+"${EMAIL[@]}"}"
# El 6 va el ULTIMO porque lee lo que dejaron los cinco anteriores: el
# estado.json del 1 y los deltas del 3. Traducir antes de medir seria traducir
# la sesion anterior.
paso "6/6 · el Enlace traduce"        python3 "$RAIZ/digesto/digesto.py" --sesion "$SESION"

echo "─────────────────────────────────────────"
if [ "$fallo" -eq 0 ]; then
  echo "✅ Cierre completo. La línea no se pierde."
else
  echo "🔴 Cierre con fallos declarados arriba. Revísalos antes de irte."
fi
echo "   snapshot : $RAIZ/ALEJANDRIA_ESTADO_ACTUAL.md"
echo "   delta    : $RAIZ/delta.md"
echo "   arranque : $CONT/bootstrap_continuidad.md"
echo "   digesto  : $RAIZ/digesto/  ·  acta: $RAIZ/mensajes/mensajes.jsonl"
echo "   el Ojo   : http://127.0.0.1:8790/"
exit "$fallo"
