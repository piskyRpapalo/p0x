#!/bin/bash
# HEXELION 2026-07-04 — residencia del cerebro del Sínodo en la-torre.
# PROPUESTO, NO HABILITADO (doctrina propose-only: el carbono instala).
#
# Root cause medido del incidente CUDA (reporte Preceptor Local 2026-07-04):
# nvmap (error 12) NO desaloja page cache; cada carga del modelo es una ventana
# de fallo. Cura: cargar UNA vez en condiciones ingenierizadas (reclaim anon
# previo) y mantener residente (keep_alive=-1). Techo medido: num_ctx=6144 con
# FA+KV q8_0+num_batch 256 (8192 NO cabe: pesos 2.4G + KV 0.6G + compute 0.3G + blob 2.7G
# en page cache que nvmap no desaloja > 7.6G RAM).
#
# INSTALACIÓN (jetson@la-torre, sin sudo — todo es espacio de usuario):
#   cp modelo_residente.sh ~/bin/ && chmod +x ~/bin/modelo_residente.sh
#   echo 'ExecStartPost=-%h/bin/modelo_residente.sh' >> ~/.config/systemd/user/ollama.service.d/hexelion.conf
#   systemctl --user daemon-reload && systemctl --user restart ollama
# (opcional, vigilancia continua cada 5 min: ver modelo-residente.timer adjunto)
set -u
MODELO="qwen3:4b-instruct-2507-q4_K_M"
CTX=6144
LOG="$HOME/modelo_residente.log"
ts() { date "+%F %T"; }

# espera a que ollama responda (hasta 60 s — útil como ExecStartPost)
for i in $(seq 12); do
  curl -s -m 4 localhost:11434/api/tags >/dev/null 2>&1 && break
  sleep 5
done

# ¿ya residente? entonces no hay nada que hacer
if curl -s -m 5 localhost:11434/api/ps | grep -q "\"name\":\"$MODELO\""; then
  exit 0
fi

echo "$(ts) modelo NO residente — reclaim + recarga" >> "$LOG"
# reclaim: asignación anónima de 5.2G fuerza al kernel a desalojar cache/swap;
# al salir el proceso queda free real para los nvmap alloc de la carga.
python3 - <<PY >> "$LOG" 2>&1
a=[bytearray(256*1024*1024) for i in range(21)]
print("reclaim", len(a)*256, "MB ok")
PY

for intento in 1 2 3; do
  R=$(curl -s -m 300 localhost:11434/api/generate -d "{\"model\":\"$MODELO\",\"prompt\":\"ok\",\"stream\":false,\"keep_alive\":-1,\"options\":{\"num_ctx\":$CTX,\"num_batch\":256,\"num_predict\":2}}")
  if echo "$R" | grep -q "\"done\":true"; then
    echo "$(ts) recarga OK (intento $intento)" >> "$LOG"
    exit 0
  fi
  echo "$(ts) intento $intento falló: $(echo "$R" | head -c 200)" >> "$LOG"
  sleep 10
done
echo "$(ts) FALLO persistente tras 3 intentos" >> "$LOG"
exit 1
