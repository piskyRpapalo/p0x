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
#
# El paso 3 va DESPUES del 1 porque el delta se calcula contra la instantanea
# anterior de la base: hay que meter la nueva para saber que cambio. Y el 4 va
# despues del 3 porque el arranque se genera de la base ya actualizada.
set -uo pipefail

RAIZ="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CONT="$HOME/p0x/preceptor-internal/continuidad"

SESION="${1:-$(date +%Y-%m-%d)-sesion}"
MODO="--completo"
EMAIL=()
for arg in "$@"; do
  case "$arg" in
    --rapido) MODO="--rapido" ;;
    --email)  EMAIL+=(--email) ;;
    --a=*)    EMAIL+=(--a "${arg#--a=}") ;;
  esac
done

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

paso "1/5 · midiendo el metal"        python3 "$RAIZ/recolector.py" $MODO --historial
paso "2/5 · renderizando el snapshot" python3 "$RAIZ/informe.py"
paso "3/5 · absorbiendo el delta"     python3 "$CONT/continuidad.py" absorber --sesion "$SESION"
paso "4/5 · regenerando el arranque"  python3 "$CONT/continuidad.py" bootstrap
paso "5/5 · delta y resumen"          python3 "$RAIZ/resumen.py" --sesion "$SESION" "${EMAIL[@]+"${EMAIL[@]}"}"

echo "─────────────────────────────────────────"
if [ "$fallo" -eq 0 ]; then
  echo "✅ Cierre completo. La línea no se pierde."
else
  echo "🔴 Cierre con fallos declarados arriba. Revísalos antes de irte."
fi
echo "   snapshot : $RAIZ/ALEJANDRIA_ESTADO_ACTUAL.md"
echo "   delta    : $RAIZ/delta.md"
echo "   arranque : $CONT/bootstrap_continuidad.md"
echo "   el Ojo   : http://127.0.0.1:8790/"
exit "$fallo"
