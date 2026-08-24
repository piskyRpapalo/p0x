#!/bin/bash
# Chat local con Qwen 3.8-27B Uncensored Q4_K_M.
#
# CAMBIOS DEL 2026-08-25, todos medidos:
#
#  - Se usa el binario de `soberano-bench`, que SI trae backend Vulkan. El de
#    `~/.local/bin/llama-cli` devuelve `(none)` en --list-devices: es CPU pura.
#  - `-ngl 99` de verdad. Antes ponia `-ngl 999` contra un binario sin GPU: un
#    no-op SILENCIOSO que aparentaba descargar capas sin descargar ninguna.
#    Medido: prompt 22,8 -> 67,2 tok/s (x2,95), generacion 2,74 -> 4,63 (x1,69).
#  - `-c 32768` MEDIDO, no supuesto. El modelo declara 262K, pero eso es su
#    ficha, no el techo de esta maquina. 32K carga y corre con la GPU llena y
#    50 GB de RAM libres. Subirlo exige volver a medir, no suponer.
#
# El razonamiento se deja ENCENDIDO aqui a proposito: esto es un chat, y para
# conversar el modelo piensa mejor. Para los BUCLES es al reves -- ahi va
# `--reasoning off`, porque a 5 tok/s cada token de pensamiento invisible es
# tiempo de pared. Medido: «responde solo: listo» gasto 45 tokens de
# pensamiento con el defecto y cero con el flag (4,7 -> 6,9 tok/s).
set -uo pipefail

VULKAN="$HOME/p0x/soberano-bench/bin/llama-b10068-bin-ubuntu-vulkan-x64/llama-b10068"
MODELO="$HOME/ia-models/qwen-uncensored/Qwen3.8-27B-Uncensored-OrcaRouter-Q4_K_M.gguf"

if [ ! -x "$VULKAN/llama-cli" ]; then
  echo "PARADA: no esta el binario Vulkan en $VULKAN" >&2
  echo "        Sin el, esto correria en CPU a un tercio de velocidad sin decirlo." >&2
  exit 1
fi
if [ ! -f "$MODELO" ]; then
  echo "PARADA: no esta el modelo en $MODELO" >&2
  exit 1
fi

echo "[*] Qwen 3.8-27B Uncensored (Q4_K_M) · Vulkan sobre Radeon 780M"
echo "[*] Medido: 67 tok/s de prompt · 4,6 tok/s de generacion · contexto 32K"
echo "[*] Escribe tu mensaje. /exit para salir."
echo ""
cd "$(dirname "$MODELO")"
LD_LIBRARY_PATH="$VULKAN" exec "$VULKAN/llama-cli" \
  -m "$MODELO" \
  -ngl 99 \
  -c 32768 \
  --temp 0.7 \
  -n 4096 \
  --no-display-prompt
