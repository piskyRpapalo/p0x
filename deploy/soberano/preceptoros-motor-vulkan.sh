#!/usr/bin/env bash
# El motor de PreceptorOS, por la GPU. Envoltorio de nodo, NO cambio de producto.
#
# POR QUE EXISTE
# --------------
# `conversacion.motor_llama` construye su orden sin `-ngl`: el producto es
# portatil y no puede suponer que hay GPU. En ESTE nodo si la hay, y el binario
# del PATH (`~/.local/bin/llama-completion` -> b10488) **no tiene backend
# Vulkan**. Apuntar el producto al binario bueno sin `-ngl` seguiria corriendo
# en CPU: la GPU estaria delante y sin usar.
#
# Este envoltorio pone las tres cosas que el producto no puede poner por si
# mismo, y no toca ni una linea de `aurelius/`:
#
#   1. LD_LIBRARY_PATH -> las .so del build Vulkan viven junto al binario
#   2. -ngl 99         -> las capas a la Radeon 780M
#   3. --reasoning off -> ver la nota de abajo
#
# MEDIDO EL 2026-08-25, mismo prompt, -n 80, el 4B del producto:
#
#   CPU    (~/.local/bin/llama-completion)   19,23 tok/s  ·  6,2 s de pared
#   Vulkan (este envoltorio)                 27,25 tok/s  ·  3,9 s de pared
#                                            x1,42           -37 % de espera
#
# Y con el 27B (`Qwen3.8-27B-Uncensored`): 4,32 tok/s · **25 s por turno**.
# Seis veces mas lento, y el producto **carga el modelo entero en cada turno**
# (proceso hijo por D68, no hay servidor que lo mantenga caliente). Por eso el
# 27B no es el cerebro por defecto de la cara: es un modelo de bucle nocturno,
# no de conversacion.
#
# CORRECCION AL CANON, medida hoy: `deploy/soberano/CLAUDE.md` afirma que
# «llama-completion de este build NO tiene --reasoning off». Es falso en los
# dos binarios de este nodo -- b10068 (Vulkan) y b10488 (PATH) exponen
# `-rea, --reasoning [on|off|auto]`. Comprobable con `--help | grep reasoning`.
# Se apaga aqui porque el pensamiento invisible es tiempo de pared, y la cara
# tiene un tope de 80 tokens que el modelo no debe gastarse pensando.
set -euo pipefail

VULKAN="${PRECEPTOROS_VULKAN:-$HOME/p0x/soberano-bench/bin/llama-b10068-bin-ubuntu-vulkan-x64/llama-b10068}"
BINARIO="$VULKAN/llama-completion"
CAPAS="${PRECEPTOROS_NGL:-99}"

# Se PARA en vez de caer a CPU en silencio. Un motor que va a un tercio de
# velocidad sin decirlo no lo nota nadie hasta que alguien mira el reloj.
[ -x "$BINARIO" ] || { echo "[motor-vulkan] no esta el binario Vulkan en $VULKAN" >&2; exit 2; }

export LD_LIBRARY_PATH="$VULKAN${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}"
exec "$BINARIO" -ngl "$CAPAS" --reasoning off "$@"
