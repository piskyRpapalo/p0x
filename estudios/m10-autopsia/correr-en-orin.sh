#!/usr/bin/env bash
# El bucle de estudio, para correr EN EL ORIN NANO. Desde soberano no vale.
#
# POR QUE AQUI Y NO ALLA: el paso (c) --el guion determinista-- ya corrio en
# soberano y su JSON esta al lado, con el gate en verde. Lo que NO se puede
# hacer desde soberano son los pasos (b), (d) y (e): el modelo tiene que ser el
# del Orin, y sobre todo el consumo tiene que medirlo el Orin. Un tokens/W
# medido en un Ryzen y publicado como del Orin seria una cifra inventada con
# cara de medicion, que es justo lo que este rack lleva cuatro puertas cazando.
set -euo pipefail

AQUI="$(cd "$(dirname "$0")" && pwd)"
JSON="$AQUI/m10-inventario.json"
# `qwen3:8b-instruct` NO EXISTE: el registro devuelve 404. El tag real es
# `qwen3:8b` (HTTP 200), comprobado contra registry.ollama.ai antes de tirar
# cinco gigas. Desviacion declarada respecto al encargo.
#
# El canon prohibe los tags pelados porque apuntan a variantes Thinking con
# razonamiento no desactivable. Aqui `qwen3:8b` SI es hibrido y pensaria por
# defecto -- por eso abajo va `--think false`, que esta version de ollama
# (0.11.4) si acepta. Comprobado, no supuesto.
MODELO="${MODELO:-qwen3:8b}"

echo "== 0 · el gate, antes de nada =="
python3 "$AQUI/autopsia.py" --salida "$JSON"

echo "== 1 · la maquina, antes que la cifra =="
uname -srm
# El Orin publica su consumo por INA3221 en el bus i2c del propio modulo.
# Se busca por NOMBRE, jamas por indice: el numero de hwmon cambia entre
# arranques y leer el indice equivocado da una cifra de otro sensor.
RAIL=""
for h in /sys/bus/i2c/drivers/ina3221/*/hwmon/hwmon*/; do
  [ -d "$h" ] && RAIL="$h" && break
done
if [ -n "$RAIL" ]; then
  echo "INA3221: $RAIL"
  for f in "$RAIL"in*_label; do
    [ -e "$f" ] || continue
    n="$(basename "$f" _label)"; n="${n#in}"
    echo "  $(cat "$f"): $(cat "$RAIL/curr${n}_input" 2>/dev/null || echo NO_DATA) mA"
  done
else
  echo "INA3221: NO_DATA · sin sensor de raíl visible; el consumo saldrá NO_DATA"
fi

echo "== 2 · el modelo =="
command -v ollama >/dev/null || { echo "PARA: no hay ollama en el Orin"; exit 2; }
ollama list | grep -q "${MODELO%%:*}" || ollama pull "$MODELO"

echo "== 3 · el modelo INTERPRETA el JSON (no lo produce) =="
# --verbose para que ollama imprima eval_count y eval_duration: de ahi salen
# los tokens/s reales, medidos, en vez de estimados.
ollama run "$MODELO" --verbose --think false \
  "Eres el analista de una autopsia de hardware. Te doy un JSON MEDIDO por un
guion determinista. NO inventes ni un dato que no este en el JSON; si algo
falta, escribe NO_DATA con su causa. Produce en espanol y en Markdown:
(1) una ficha tecnica de autopsia, (2) un prompt reutilizable para futuros
intentos de liberacion OTA, (3) una entrada para LA_NECROPOLIS.md con causa,
intento y reemplazo. Presta atencion especial al campo gemelo.aviso: si el
gemelo no es concluyente, dilo en la ficha, porque la ficha vieja lo daba por
prueba del chip.

JSON:
$(cat "$JSON")" | tee "$AQUI/ficha-autopsia.md"

echo
echo "== 4 · firma =="
echo "La firma Ed25519 la hace el Orin, NO soberano: el canon prohibe que una"
echo "clave de firma de atestacion viva en soberano (solo SSH auth-only)."
echo "Salida esperada: ~/p0x/Alejandria/digesto/m10-em2-autopsia-<TS>.jsonl"
