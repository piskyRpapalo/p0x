---
id: tecnica-reflejo-vibracion
titulo: "Reflejo-vibracion — el sismógrafo casero del rack"
tipo: tecnica
clase: operativo
nivel: vivo
enlaces:
  - proyecto-reflejos
  - reflejo-termico-m5
  - ia-fisica
metrica_exito: "evento 'movimiento detectado' en <10s ante manipulación física del M5/rack; 0 falsos positivos con la placa quieta (ruido medido Δ|g|≤0.0615)"
umbral_reedicion: "recolocación física del M5, o falsos positivos/negativos observados en episodios reales"
actualizado: 2026-07-11
descripcion_niveles:
  basico: "Un acelerómetro nota si alguien mueve o golpea el equipo y lo anuncia en la consola — un sismógrafo casero que delata la mano ajena."
  medio: "Reflejo determinista #3 (Pista A): el ADXL345 publica aceleración xyz cada 5s; si el cambio de |g| entre lecturas supera 0.25g dispara 'movimiento detectado' (REFLEX). Rearme tras 3 lecturas quietas (<0.10g). Umbral calibrado con la placa quieta: ruido máx 0.0615g → 0.25 = 4× margen."
  experto: "Arco: Δ|g| entre lecturas consecutivas de Redis m5:last (magnitud vectorial; el offset absoluto del sensor ~2.32g no importa, se detecta CAMBIO). Calibración 2026-07-11 (18 muestras quietas): Δ|g| máx 0.0615, media 0.0235, σ|g| 0.021 → disparo 0.25 (~4× máx, ~12σ), quietud <0.10, rearme N=3. Tras silencio del sensor se re-siembra el baseline (evita falso disparo al volver). Runner compartido reflejo_m5_watch.py; unit reflejo-m5.service PROPUESTA. Futuro: fechado con el RTC del M5 (ya en hora de Lisboa, #30)."
---

# Reflejo-vibracion

**Reflejo determinista #3** (Pista A) — el sismógrafo casero. Detecta la mano
ajena, el golpe o el temblor: cualquier Δ|g| brusco en el ADXL345 del M5.

- **Sensor**: ADXL345 (el-vigia) → Redis `hexelion:telemetry:m5:last`.
- **Disparo**: `Δ|g| ≥ 0.25 g` entre lecturas consecutivas (dato: ruido en
  reposo máx 0.0615 g, medido 2026-07-11 — margen 4×, ~12σ).
- **Rearme**: 3 lecturas seguidas con `Δ|g| < 0.10` (quietud sostenida).
- **Acción**: evento "movimiento detectado" (REFLEX ámbar) + `reflejos.jsonl`.
  Solo aviso, jamás valor. Tras silencio del M5 se re-siembra el baseline
  (ausencia ≠ dato; volver del silencio no dispara).
- **IronClaw**: sin LLM en el lazo. Arco en `reflejo_m5_watch.py` (compartido).
