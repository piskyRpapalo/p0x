---
id: tecnica-reflejo-termico-m5
titulo: "Reflejo-termico-m5 — calor ambiente anómalo dispara aviso"
tipo: tecnica
clase: operativo
nivel: vivo
enlaces:
  - proyecto-reflejos
  - reflejo-bateria
  - patron-era-energetica
metrica_exito: "aviso REFLEX en <10s cuando el ambiente del rack supera 40°C; 0 falsos positivos en operación normal (baseline 30.3°C); rearme solo con frío sostenido"
umbral_reedicion: "cambio de ubicación del M5, verano que acerque la baseline al umbral, o un episodio real que lo desmienta"
actualizado: 2026-07-11
descripcion_niveles:
  basico: "Un termómetro real vigila el aire del rack. Si se calienta de forma anómala, avisa en la consola al instante — sin pensar, como retirar la mano del fuego."
  medio: "Reflejo determinista #2 (Pista A): el BME680 del M5 publica temp_c cada 5s vía Redis; a ≥40°C dispara aviso REFLEX ámbar con histéresis (rearme a ≤38°C sostenido 3 lecturas). Umbral derivado del dato: baseline medida 30.29±0.01°C. Sin LLM; solo aviso."
  experto: "Arco: Redis hexelion:telemetry:m5:last (TTL 30s, honest-sensors: clave vencida = M5 callado = NO dispara, ausencia≠dato) → máquina ARMADO↔DISPARADO en deploy/fragua/reflejo_m5_watch.py (runner compartido con reflejo-vibracion: 1 poll, 2 arcos) → consola Bitácora + mente/telemetria/reflejos.jsonl. Calibración 2026-07-11: 18 muestras, media 30.29°C σ0.010 → disparo 40.0 (baseline+10, >>3σ), rearme 38.0 (histéresis 2°C), N=3. Complementa al guard térmico de CPU (Reflejo-0 #20, 80°C en la fragua): este mide el AMBIENTE, aquel el silicio. Unit reflejo-m5.service PROPUESTA."
---

# Reflejo-termico-m5

**Reflejo determinista #2** (Pista A). El Reflejo-0 (#20) vigila el silicio de
la fragua (80°C, pacing); este vigila el **aire** — un incendio incipiente, un
ventilador muerto o un verano brutal se ven antes en el ambiente.

- **Sensor**: BME680 en el M5 (el-vigia) → Redis `hexelion:telemetry:m5:last`.
- **Disparo**: `temp_c ≥ 40.0°C` (dato: baseline 30.29±0.01°C medida 2026-07-11).
- **Histéresis**: rearme solo a `≤ 38.0°C` sostenido (3 lecturas ≈ 15s).
- **Acción**: aviso REFLEX ámbar a consola + registro en `reflejos.jsonl`.
  Solo aviso (jamás valor). Ausencia de sensor NO dispara (ausencia ≠ dato).
- **IronClaw**: sin LLM en el lazo; el Monje lo narra post-hoc si se le pregunta.
- **Arco**: `deploy/fragua/reflejo_m5_watch.py` (runner compartido con
  `reflejo-vibracion` — 1 poll, 2 máquinas independientes).
