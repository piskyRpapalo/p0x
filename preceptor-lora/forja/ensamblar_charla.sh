#!/bin/bash
# La cadena de tres pasos, que ya se conocia y aqui queda escrita en vez de
# tecleada: entrenar -> convertir a GGUF -> `ollama create`. Ollama no come lo
# que `peft` escribe, y el conversor NO vive en `preceptor-lora/llama.cpp` -- ahi
# solo hay un `build`. Vive en `~/.llama.cpp`, y darlo por sabido cuesta el rato
# de buscarlo otra vez.
set -eu
RAIZ="$HOME/p0x/preceptor-lora"
PY="$HOME/.venvs/aurelius-forja/bin/python"
CONV="$HOME/.llama.cpp/convert_lora_to_gguf.py"
cd "$RAIZ"
for par in "base:preceptor-charla-base-v1:charla-base" \
           "multilang:preceptor-charla-multi-v1:charla-multi"; do
  nombre="${par%%:*}"; resto="${par#*:}"
  gguf="${resto%%:*}"; mf="${resto#*:}"
  adap="adapters/charla_${nombre}_v1"
  [ -f "$adap/adapter_model.safetensors" ] || { echo "FALTA $adap · no entreno"; exit 1; }
  echo "=== $nombre · convirtiendo ==="
  "$PY" "$CONV" "$adap" --outtype f16 --outfile "$adap/${gguf}.gguf"
  ls -l "$adap/${gguf}.gguf"
  echo "=== $nombre · ollama create ==="
  ollama create "preceptor-charla-${nombre%lang}:v1" -f "modelfiles/${mf}.Modelfile"
done
ollama list | head -5
