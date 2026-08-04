#!/usr/bin/env bash
# cerebro-local-arranca.sh · levanta el cerebro local del nodo `soberano`.
#
# Bloque SOBERANO-1 (2026-08-04). Autorizado por el Soberano: qwen3-coder,
# num_ctx 16384, backend Vulkan.
#
# POR QUÉ ESTE SCRIPT EXISTE: hasta hoy el cerebro local se levantaba a mano en
# un terminal, sin registro. Se perdía el log de arranque, moría al cerrar la
# ventana, y nadie podía reproducir la invocación exacta. Esto la fija.
#
# ---------------------------------------------------------------------------
# LOS DOS BINARIOS Y POR QUÉ IMPORTA CUÁL (medido 2026-08-04)
#
#   1. El llama-server que trae Ollama expone POST /v1/messages (Anthropic
#      nativo) — la cadena vive en su libllama-server-impl.so. Es el único que
#      sirve para el arnés de Claude Code.
#   2. El build b10068 de soberano-bench hace Vulkan, pero /v1/messages NO
#      aparece en NINGÚN fichero suyo. Con él, Claude Code no habla.
#
# Parecían excluyentes. No lo son: el binario de Ollama TAMBIÉN hace Vulkan si
# se le señala el backend con GGML_BACKEND_PATH apuntando al FICHERO .so — no al
# directorio, que es el error que devuelve la lista de dispositivos vacía:
#   GGML_BACKEND_PATH=<dir>/vulkan            -> "cannot read file data: Is a directory"
#   GGML_BACKEND_PATH=<dir>/vulkan/libggml-vulkan.so -> Vulkan0: AMD Radeon 780M
# Por eso este script usa el binario de Ollama CON el backend Vulkan explícito:
# se queda con el endpoint Anthropic Y con la aceleración.
# ---------------------------------------------------------------------------
set -euo pipefail

OLLAMA_LIB="${P0X_OLLAMA_LIB:-/usr/local/lib/ollama}"
GGUF="${P0X_GGUF:-$HOME/soberano-bench/models/Qwen3-Coder-30B-A3B-Instruct-Q4_K_M.gguf}"
PUERTO="${P0X_PUERTO:-8080}"
NUM_CTX="${P0X_NUM_CTX:-16384}"     # autorizado por el Soberano (Bloque SOBERANO-1)
NGL="${P0X_NGL:-999}"               # todas las capas a la GPU
LOG="${P0X_LOG:-$HOME/.cache/p0x/cerebro_local_arranque.log}"

VK="$OLLAMA_LIB/vulkan/libggml-vulkan.so"
BIN="$OLLAMA_LIB/llama-server"

die() { printf '\n  ABORTA · %s\n\n' "$1" >&2; exit 1; }

[ -x "$BIN" ]  || die "no encuentro el llama-server de Ollama en $BIN"
[ -f "$GGUF" ] || die "no encuentro el modelo en $GGUF"
[ -f "$VK" ]   || die "no encuentro el backend Vulkan en $VK (¿instalación de Ollama incompleta?)"

# Un solo cerebro a la vez: dos modelos de 18GB no caben en 57GB de RAM.
if curl -sf -m 3 "http://127.0.0.1:$PUERTO/health" >/dev/null 2>&1; then
  die "ya hay algo sirviendo en el puerto $PUERTO. Párralo antes: no caben dos modelos en RAM."
fi

# Comprobar que Vulkan enumera ANTES de cargar 18GB, no después.
if ! GGML_BACKEND_PATH="$VK" LD_LIBRARY_PATH="$OLLAMA_LIB" \
     "$BIN" --list-devices 2>/dev/null | grep -q 'Vulkan'; then
  die "el backend Vulkan no enumera ningún dispositivo. Revisa el acceso a /dev/dri (ACL) antes de seguir."
fi

mkdir -p "$(dirname "$LOG")"
printf 'Levantando el cerebro local:\n  modelo  : %s\n  num_ctx : %s\n  ngl     : %s\n  log     : %s\n\n' \
  "$(basename "$GGUF")" "$NUM_CTX" "$NGL" "$LOG"

nohup env GGML_BACKEND_PATH="$VK" LD_LIBRARY_PATH="$OLLAMA_LIB" \
  "$BIN" -m "$GGUF" --host 127.0.0.1 --port "$PUERTO" \
  -c "$NUM_CTX" -ngl "$NGL" > "$LOG" 2>&1 &

# El log de arranque queda en fichero: la vez anterior se perdió por vivir en un pty.
for _ in $(seq 1 60); do
  if curl -sf -m 2 "http://127.0.0.1:$PUERTO/health" 2>/dev/null | grep -q ok; then
    printf 'Listo. /health responde ok. Arranque registrado en %s\n' "$LOG"
    exit 0
  fi
  sleep 2
done
die "no respondió /health en 120s. Mira $LOG"
