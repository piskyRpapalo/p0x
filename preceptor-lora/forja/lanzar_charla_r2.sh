#!/bin/bash
# RONDA 2 de La Charla. Dos cambios sobre la ronda 1, y los dos salen de medida:
#
# 1 · EL CORPUS YA NO LLEVA CIFRAS CON UNIDAD. La ronda 1 estaba llena de
#     «cuatro gigas», «ocho de RAM», «dieciseis bits»: el modelo no aprendio los
#     numeros, aprendio LA FORMA de soltar uno con seguridad, y decia «250 MB»
#     donde el system prompt decia otra cosa tres lineas mas arriba. Ahora lo
#     impide una regla del validador, no la memoria de quien escriba.
#
# 2 · ENTRAN LOS ATAJOS, que se olvidaron en la ronda 1 y son lo que distingue
#     al producto: las conductas que los botones de la web disparan. Los prompts
#     son LITERALMENTE los de `cerebros.json`.
#
# Y MENOS PASOS. La ronda 1 hizo 300 sobre 150 muestras --dos epocas-- y
# sobreajusto: perdida 0,72 y la lengua rota. El adaptador de 100 pasos
# conservaba la voz. Aqui se va a ~una epoca, no dos.
set -u
FORJA="$HOME/p0x/preceptor-lora/forja"
PY="$HOME/.venvs/aurelius-forja/bin/python"
cd "$FORJA" || exit 1
for par in "base:sft_charla_base_v1.jsonl:150" "multilang:sft_charla_multilang_v1.jsonl:100"; do
  nombre="${par%%:*}"; resto="${par#*:}"
  fichero="${resto%%:*}"; pasos="${resto#*:}"
  echo "=== r2-$nombre · $pasos pasos · $(date +%H:%M:%S) ==="
  "$PY" train_cuentacuentos_lora.py --ejecutar \
      --dataset "../data/$fichero" \
      --salida "../adapters/charla_${nombre}_r2" \
      --pasos "$pasos" --hilos 8 --techo-c 80 --respiro-s 20 \
      > "training_charla_${nombre}_r2.log" 2>&1
  echo "=== r2-$nombre codigo $? · $(date +%H:%M:%S) ==="
done
