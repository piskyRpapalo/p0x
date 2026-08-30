#!/usr/bin/env bash
# volcar_estado.sh · snapshot del sistema para una sesion nueva.
#
# Ahora es una CAPA FINA sobre recolector.py + informe.py. Antes media por su
# cuenta, y medi­a mal: preguntaba a `systemctl --user` por una unidad de
# sistema, usaba `is-active` en oneshots (donde «inactive» es el estado sano),
# y filtraba el inventario de modelos por nombre -- lo que escondia justo los
# modelos con nombre nuevo y hacia que el mismo fichero dijese 8 modelos en una
# seccion y 7 doce lineas mas abajo.
#
# Tambien tenia un bug de forma que multiplicaba el ruido:
#     cmd >> "$OUT" || echo "- NO_DATA: ..." >> "$OUT"
# Cuando `cmd` IMPRIME y ademas devuelve != 0 (que es exactamente lo que hace
# `systemctl is-active` con una unidad parada), se escribian LAS DOS COSAS. Por
# eso el snapshot llevaba «inactive» y «NO_DATA: api-guia no esta activa» en
# lineas consecutivas, contradiciendose consigo mismo.
#
# La leccion, y por eso este fichero ya no mide: una sola medicion, dos
# formatos. Dos codigos midiendo lo mismo divergen, y divergen en silencio.
set -euo pipefail

RAIZ="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

MODO="--completo"
[[ "${1:-}" == "--rapido" ]] && MODO="--rapido"

python3 "$RAIZ/recolector.py" "$MODO" --historial
python3 "$RAIZ/informe.py"

echo "✅ Estado volcado en $RAIZ/ALEJANDRIA_ESTADO_ACTUAL.md"
