#!/usr/bin/env bash
# Gate 0 · voz local del Sínodo — síntesis de prueba con métricas (misión PULIR+VOZ B3).
# 100% local (Piper/ONNX en la fragua); NO desplegado: solo genera clips para
# el veredicto del Soberano. Corre encolado en tsp (nice/ionice los pone tsp).
set -u
VOZ_DIR=/mnt/nvme/p0x/voz
VENV=$VOZ_DIR/.venv-piper/bin/python
OUT=$VOZ_DIR/gate0
MET=$OUT/metricas.txt
mkdir -p "$OUT"

temp() { awk '{printf "%.1f", $1/1000}' /sys/class/thermal/thermal_zone0/temp; }

declare -A FRASES=(
  [monje]="Soberano, la fragua está a setenta y seis grados y el UPS sostiene la carga. El cuerpo primero."
  [alquimista]="El tesoro de mainnet marca uno coma noventa y cinco NEAR. Leo la cadena sin tocarla."
  [sindato]="Sin dato en telemetría M cinco. La ausencia es la verdad, no la relleno."
)

{
echo "# Gate 0 Piper · $(date -u +%FT%TZ) · fragua zone0 antes: $(temp)°C"
for modelo in es_ES-sharvard-medium es_ES-davefx-medium; do
  onnx=$VOZ_DIR/modelos/$modelo.onnx
  echo ""
  echo "== $modelo ($(du -h "$onnx" | cut -f1)) =="
  for clip in monje alquimista sindato; do
    wav=$OUT/${modelo#es_ES-}_${clip}.wav
    /usr/bin/time -v "$VENV" -m piper -m "$onnx" -f "$wav" \
      -- "${FRASES[$clip]}" 2> "$OUT/.time_tmp"
    wall=$(grep 'Elapsed (wall' "$OUT/.time_tmp" | awk '{print $NF}')
    rss=$(grep 'Maximum resident' "$OUT/.time_tmp" | awk '{print $NF}')
    cpu=$(grep 'Percent of CPU' "$OUT/.time_tmp" | awk '{print $NF}')
    dur=$("$VENV" - "$wav" <<'PY'
import sys, wave
w = wave.open(sys.argv[1]); print(f"{w.getnframes()/w.getframerate():.2f}")
PY
)
    echo "clip=$clip wall=${wall}s audio=${dur}s rss=${rss}KB cpu=${cpu} wav=$wav"
  done
done
rm -f "$OUT/.time_tmp"
echo ""
echo "# fragua zone0 después: $(temp)°C"
} | tee "$MET"
