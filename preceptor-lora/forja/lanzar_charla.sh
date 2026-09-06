#!/bin/bash
# Los dos entrenamientos de La Charla, EN SECUENCIA. La razon es la misma que en
# `lanzar_reclamaciones.sh` y sigue siendo cierta: cada run pica por encima de
# los 19 GB y el multilingue se predice en ~28. Dos a la vez es el OOM de los dos.
#
# PASOS = 2 EPOCAS, como en la ronda anterior (200 pasos sobre 100 muestras). El
# bucle recorre `textos[paso % len]`, asi que los pasos se calculan sobre el
# tamaño del fichero, no se copian del run pasado: 150 muestras -> 300 pasos.
set -u
FORJA="$HOME/p0x/preceptor-lora/forja"
PY="$HOME/.venvs/aurelius-forja/bin/python"
cd "$FORJA" || exit 1
for par in "base:sft_charla_base_v1.jsonl:300" "multilang:sft_charla_multilang_v1.jsonl:200"; do
  nombre="${par%%:*}"; resto="${par#*:}"
  fichero="${resto%%:*}"; pasos="${resto#*:}"
  echo "=== charla-$nombre · $pasos pasos · $(date +%H:%M:%S) ==="
  "$PY" train_cuentacuentos_lora.py --ejecutar \
      --dataset "../data/$fichero" \
      --salida "../adapters/charla_${nombre}_v1" \
      --pasos "$pasos" --hilos 8 --techo-c 80 --respiro-s 20 \
      > "training_charla_${nombre}.log" 2>&1
  echo "=== charla-$nombre terminado con codigo $? · $(date +%H:%M:%S) ==="
done
