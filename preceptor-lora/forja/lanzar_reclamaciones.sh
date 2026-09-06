#!/bin/bash
# Los dos entrenamientos EN SECUENCIA, no en paralelo: cada uno pico 17,4 GB de
# RAM y en esta maquina hay 38. Dos a la vez es el OOM del segundo, o de los dos.
set -u
FORJA="$HOME/p0x/preceptor-lora/forja"
PY="$HOME/.venvs/aurelius-forja/bin/python"
cd "$FORJA" || exit 1
for par in "en:sft_reclamaciones_en_v1.jsonl" "multilang:sft_reclamaciones_multilang_v1.jsonl"; do
  nombre="${par%%:*}"; fichero="${par#*:}"
  echo "=== $nombre · $(date +%H:%M:%S) ==="
  "$PY" train_cuentacuentos_lora.py --ejecutar \
      --dataset "../data/$fichero" \
      --salida "../adapters/reclamaciones_${nombre}_v1" \
      --pasos 200 --hilos 8 --techo-c 80 --respiro-s 20 \
      > "training_${nombre}.log" 2>&1
  echo "=== $nombre terminado con codigo $? · $(date +%H:%M:%S) ==="
done
