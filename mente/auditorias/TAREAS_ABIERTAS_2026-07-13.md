<!-- Documento-snapshot de la misión INVENTARIO TOTAL (2026-07-13).
     Sin front-matter §2 a propósito: fotografía del backlog para el rediseño,
     no un MD evolutivo del grafo. Fuentes: mente/feedback/PENDIENTES.md
     (96 filas), git status de los 4 repos, y verificación en vivo de hoy.
     NOTA DE MÉTODO: en PENDIENTES "firmada" = David la APROBÓ en la bandeja
     (vaciado del 07-12), NO que esté hecha. Aquí listo solo lo que sigue
     abierto; lo que verifiqué como cerrado de facto lo digo. -->

# TAREAS ABIERTAS DE SOFTWARE · 2026-07-13

Cerradas de facto detectadas hoy (no las cuento abajo): **#24** pubkey del
Vigía (hecha 07-06, keyless verificado), **#70** feed vivo desde el Vigía (el
feed actual YA ES el ustreamer del Vigía), **#8** index-en (decidida: borrada),
y los 2 jobs de OBSERVAR en revisión (bandeja de deltas = 0).

---

## 1 · TÉCNICAS — CC puede hacerlas solo (propose-only donde toque)

| id | Qué es | Coste | Estado | ¿Bloquea algo? |
|---|---|---|---|---|
| #67 | Flush del think_filter en el chat del Sínodo v2 (bug vivo: se traga la cola de 7 chars al final del stream) | S | firmada | calidad visible del chat |
| #58 | Análisis VLM del diario verde en asíncrono — todos los registros dicen `pendiente-VLM` | M | firmada | el valor real de `/verde` |
| #72 | Parada limpia del gateway con el relay MJPEG (`TimeoutStopSec`/graceful-shutdown; hoy 90 s → SIGKILL) | S | firmada | despliegues sin sobresaltos |
| #74 | Jardin Fase 1 — La Sentinelle (motor: SensorSource+sim, Le Filtre con histéresis/cooldowns/horas silenciosas, Journal, Fenêtre scanlines, Fantôme 4 estados) | M | firmada | roadmap del Jardin (F2+) |
| #78 | La voz cita el herbier (retrieval top-k al grounding del chat FR) | M | firmada | **BLOQUEADA por #77** (mano de David) |
| — | Commitear/decidir los diffs pendientes: gateway (13 líneas) + audit tools + Trivial del Jardin (incluye `npm run build` para que Trivial exista en `/jardin/`) | S | detectada hoy (git) | Trivial invisible hasta el build |
| #64 | Primer pase de modularización del gateway (monolito >4000 líneas con ~30 backups `.bak` en el repo) | L | firmada | mantenibilidad de todo |
| #19 | Dejar de trackear `disk_nodes.json`/`vessel_db.sqlite` (churn de pollers; repo perpetuamente sucio) | S | firmada | higiene git |
| #22 | Bug del grafo `g.d3AlphaTarget is not a function` (vendor vs API) — parcheado en una pasada previa, verificar que no reapareció y alinear vendor | S | firmada | consola limpia |
| #34 | Auditar el resto de llamadas force-graph en second-brain | S | firmada | — |
| #12 | Calibrar umbrales del motor delta con corpus real (0.82/0.55 provisionales) | M | firmada | calidad de OBSERVAR |
| #31 | Resto de la cota de tokens en síntesis largas (fix aplicado; falta calibrar con corpus) | S | hecha-parcial | — |
| #16 | Whisper small vs medium en la Fragua (medir RAM/tiempo/calidad para talks largas) | M | firmada | pipeline OBSERVAR |
| #7 | Fallback digno en la Fragua (evaluar por suite qwen3:1.7b u otro pequeño como chat model) | M | firmada | chat cuando la Torre no está |
| #6 | Vocero: deshornear números OMIE del few-shot (115 € fijo invita a precios rancios) | S | firmada | honestidad del Vocero |
| #21 + #29 | Voz del Sínodo siguiente pase: elegir voz (David escucha clips) + voz por agente + pre-síntesis en background | M | firmadas | experiencia del Sínodo |
| #61 | `/tareas` y `/verde` en `audit_overlaps.py` | S | firmada | cobertura del auditor |
| #55 + #63 | Barrido de secretos como hook pre-push COMPLETO en hexelion-public (dos filas, un mismo trabajo — unificar) | S | firmadas | seguridad del push público (#62) |
| #35 | Vista de cadena navegable para el Faro | M | firmada | — |
| #36 | Selector de tema en la UI (verde/violeta) | M | firmada | destino de la preview :8009 |
| #38 | Servir previews de branch sin symlinks | S | firmada | — |
| #39 | Modo "solo órganos" del Second Brain para capturas públicas | S | firmada | README público |
| #42 | Revivir el patrón `@sleeping`/`BATTERY_FLAG` (el envoltorio, no el arbitraje) | M | firmada | — |
| #43 | Verificar `HEXELION_REENCARNACION.md` contra la realidad (pre-P0X/NVMe) | S | firmada | #50 |
| #50 | Runbook `REENCARNACION_P0X.md` nuevo | M | firmada | #53 (drill) |
| #44 | Rescatar el `_ESTADO.md` por dominio (snapshot NEXUS) | M | firmada | — |
| #45 | Crear la esfera `historia-p0x` + nodos-hito | M | firmada | — |
| #60 | Retención de `.backups/` (60 días o N=200) | S | firmada | disco/higiene |
| #65 | "ADR al cierre" como paso del rito | S | firmada | gobernanza pública |
| #66 | Sección de atestación en el README público (screenshot saneado de /proof) | S | firmada | #62 |
| #69 | Captura periódica al conectar la webcam local (timer → `/api/verde/captura`) | S | firmada | diario más denso |
| #51 | Re-sync periódico del RTC del M5 — **deriva −13 min medida hoy**; con la pubkey keyless (#24) esto ya es automatizable por CC | S | firmada | timestamps honestos del M5 |
| #68 | Adoptar la bandeja de firma explicable (PROPUESTA_27) | M | firmada | legibilidad de /tareas |
| — | Diagnóstico del bug CUDA en La Torre (nvmap; la residencia depende de esto — el diagnóstico es técnico, el paste final es de David) | M | memoria 07-12 | #4 |
| — | ADXL345: eje z clavado en −2.048 g (tope de rango) — revisar escala/orientación | S | detectada hoy | honestidad del sensor |

## 2 · MANO DE DAVID — hardware, pastes, decisiones

| id | Qué es | Coste | ¿Bloquea algo? |
|---|---|---|---|
| #4 | Instalar la residencia del cerebro en La Torre (1 paste; `deploy/torre/` listo) — antes: resolver el bug CUDA | S (paste) | voces 1.5b, Sínodo estable |
| #47 | Habilitar el watcher reflejo-bateria 24/7 (paste patrón #4) — hoy los reflejos solo viven ARMADOS sin unit | S (paste) | reflejos de verdad 24/7 |
| — | Habilitar el timer 15 min de cosecha/asesoría del Alquimista (PROPUESTO desde junio) — la asesoría lleva ~20 días congelada | S (paste) | dato NEAR fresco en el Nexo |
| #75 | Broker MQTT en el Vigía + flashear los ESP32 del jardín (decisión previa: Arduino vs ESPHome) | M | Jardin Fase 4 (sensores reales) |
| #77 | Soltar los .md de herbología en `verde/herbier/` (no están en el rack; la enciclopedia los espera) | S | #78 y el Grimoire entero |
| #76 | Validar el francés con Krista (todas las líneas de copy + cámara las escribió el silicio) | S | canon del Jardin |
| #71 | Sesión de tono de la voz del Jardin con David y su esposa | S | — |
| #73 | Encuadre físico de la cámara (hoy ve el rincón, no solo las plantas) | S | privacidad/calidad del feed |
| #62 | OK al push público del README (hexelion-public espera; #55/#63/#66 son sus prerequisitos técnicos) | decisión | presencia pública |
| #52 | Copia física de secretos (H1 del runbook — LA pieza que falta) | S | supervivencia ante desastre |
| #53 | Drill de Reencarnación (H3) | M | validar #50 |
| — | `bridge_config.json` del solar (token HA; interino nube Anker SOLO forecaster, jamás Faro) | S | widget SOLAR, forecaster |
| #36/#37 | Decisión de tema ya tomada (verde; #37 descartada) → decidir si se apaga la preview :8009 o se mantiene como banco de pruebas del selector | decisión | limpieza |
| #3 | El teléfono: sensor antes que granja (RTSP/GPS/barómetro vs Acurast lite) | decisión | — |
| #13 | Revisar los `descripcion_niveles` generados | S | calidad del grafo |

## 3 · HORIZONTE — sembrado, no empezado

| id | Qué es | Coste | Nota |
|---|---|---|---|
| #1 | Gate 0 en los HP (x86): llama-factory/PEFT + LoRA-juguete de 10 ejemplos | M | primera piedra del camino dataset→Gate0→corpus→NEAR AI |
| — | Dataset maestro desde material real (incidente nvmap, fix checkpoint, esfera ia-fisica) | L | la formulación #2 fue descartada; el horizonte del marco sigue vivo |
| — | Corpus de psicología del aprendizaje → la mecánica pedagógica SE DERIVA de él (corpus vacío = mecánica STUB) | L | — |
| — | NEAR AI bajo IronClaw | L | — |
| — | dots.tts (voces clonadas zero-shot) en El Oráculo — GPU necesaria, SSH del Oráculo cerrado | L | Fase 0 investigada 06-15 |
| — | Medidor DC soberano para el solar (objetivo 2026-07-15; la nube Anker es interina) | M | 🔒 cloud jamás toca el Faro |
| — | P3b: benchmark de colocación en La Torre (CUDA 3.4×/4.5× medido) — reevaluar tras resolver el bug CUDA | M | plan de remediación Hexelion |
| — | Pantalla Soberana (el kiosco del Jardin #80 fue descartado; la pantalla en sí sigue en el horizonte) | M | — |

---

**Resumen honesto**: el backlog técnico real son ~35 tareas (mayoría S/M);
las tres que más valor desbloquean por euro de esfuerzo son #58 (VLM del
verde), #67 (think_filter) y el trío de pastes de David (residencia Torre +
watcher + timer del Alquimista) que convierten tres sistemas "preparados" en
sistemas vivos.

*Fuentes: PENDIENTES.md (96 filas al 2026-07-13), git status/log de hexelion,
p0x, jardin-des-ombres y hexelion-lab, sondas en vivo de la misión INVENTARIO
TOTAL.*
