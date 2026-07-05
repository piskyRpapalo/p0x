---
id: feedback-pendientes
titulo: Pendientes — sugerencias del Preceptor al Soberano
tipo: operativo
clase: operativo
version: 1.0.0
editor_autorizado: silicio-telemetria
dominio: gobernanza-sugerencias
metrica_exito: "100% de sugerencias de cada reporte anexadas aquí con estado; 0 sugerencias perdidas entre sesiones"
umbral_reedicion: "cualquier reporte cuyas sugerencias no consten aquí en 24h"
presupuesto_kb: 16
n_medicion: 10
changelog:
  - fecha: 2026-07-04
    autor: silicio-telemetria
    version_anterior: null
    version_nueva: 1.0.0
    hipotesis: >
      Un registro único append-only con estado evita que las sugerencias de los
      reportes se pierdan entre límites de sesión. Predicción: 0 sugerencias
      re-propuestas por olvido a partir de hoy.
    dato: "línea base — creado por mandato del Soberano (Bloque T, 2026-07-04)"
    veredicto: "primera línea base"
enlaces:
  - doctrina-protocolo-md-evolutivo
actualizado: 2026-07-05
---

# PENDIENTES · SUGERENCIAS DEL PRECEPTOR
### Registro operativo: cada reporte anexa sus sugerencias con `estado: pendiente`; el Soberano las marca `hecho` o `descartado`. El silicio anexa, jamás borra.

**Formato de entrada:** `fecha · sugerencia (una frase) · coste S/M/L · estado`

---

## ZONA EVOLUTIVA

### 2026-07-04 · reporte Preceptor Local (sesión anterior, aprobadas por el Soberano)

| # | Sugerencia | Coste | Estado |
|---|---|---|---|
| 1 | **Gate 0 en paralelo, en los HP (x86):** instalar llama-factory/PEFT en un HP y correr el LoRA-juguete de 10 ejemplos esta semana — define qué hierro entrena antes de que exista el dataset, sin tocar el rack | S | pendiente |
| 2 | **Dataset v1 sin esperar GPU:** generar los primeros 200-300 ejemplos desde los MDs existentes (voces, doctrina, alfabeto, esferas) — trabajo de texto puro; el activo transplantable empieza a existir hoy | M | pendiente |
| 3 | **El teléfono: sensor antes que granja:** pesarlo como sensor (cámara RTSP para visión Fase 2, GPS/barómetro para el Vigía) antes de dedicarlo 24/7 a Acurast lite; si entra Acurast → patrón Mastchain exacto (read-only en dashboard, bond/claims = mano del Soberano) | S | pendiente |

### 2026-07-04 · reporte Preceptor Local — Reactivación 2 (root cause CUDA + certificación)

| # | Sugerencia | Coste | Estado |
|---|---|---|---|
| 4 | **Instalar la residencia del cerebro en la-torre (1 paste):** CC tiene VETO de política para instalar persistencia remota; los artefactos están en `deploy/torre/` con instrucciones. Sin esto la auto-recuperación tras reboot depende del primer chat (ruleta nvmap). Comando: ver cabecera de `deploy/torre/modelo_residente.sh` | S | pendiente |
| 5 | **journald persistente en la-torre** (`sudo mkdir -p /var/log/journal && sudo systemctl restart systemd-journald`): el incidente 13:40 no dejó journal consultable; hoy el rastro vive solo en `~/ollama.log` (drop-in) y syslog | S | pendiente |
| 6 | **Vocero: deshornear los números OMIE del few-shot** (115.00 €/MWh fijo en el MD invita a citar precios rancios) — tras línea base n=20 del Protocolo §3 | S | pendiente |
| 7 | **Fallback fragua digno:** qwen2.5:1.5b tarda 190-230 s en denso y garabatea síntesis doctrinal; evaluar por suite qwen3:1.7b o el instruct-2507 pequeño como OLLAMA_CHAT_MODEL | M | pendiente |
| 8 | **Decidir `dashboard-v9/index-en.html`** (variante EN del Nexo sin trackear, no consta intención): trackear o borrar | S | pendiente |
| 9 | **Suite de recarga semanal en la-torre** (cron propuesto: 1 ciclo restart+reclaim+carga con log): vigila que la receta siga 2/2 cuando cambien kernel/ollama/modelo | M | pendiente |

### 2026-07-05 · reporte MISIÓN OBSERVAR + Consolidación Global

| # | Sugerencia | Coste | Estado |
|---|---|---|---|
| 10 | **Cablear los sensores del M5** (BME680/ADXL345/RTC al Grove): el bus I2C está físicamente vacío (`i2c_scan found=[]` verificado); toda la cadena M5→Redis→gateway→dashboard→Monje está viva esperando el primer dato real | S | propuesta |
| 11 | **Pubkey SSH de el-vigia sigue caída** (acceso solo por password): restaurar `authorized_keys` del Pi elimina el password del camino y permite retirar sshpass | S | propuesta |
| 12 | **Calibrar umbrales del motor delta con corpus real:** tras 5-10 videos aceptados, revisar los scores crudos persistidos en `delta.json` de cada job y ajustar `umbral_ya_sabido/umbral_nuevo` (hoy 0.82/0.55 provisionales) | M | propuesta |
| 13 | **Revisar los `descripcion_niveles` generados** (marcador `generado_por: cc-pendiente-revision` en esferas y `niveles_doctrina.yaml`): leerlos una vez y quitar el marcador a los que valgan | S | propuesta |
| 14 | **GitHub público: crear remote + push** de `~/hexelion-public/` (git init hecho, checklist de sanitización 0 hits, README = versión pública del Discurso): decisión y cuenta del Soberano | S | propuesta |
| 15 | **Job queue: vigilar la anomalía tsp E-Level -1** (job 16 murió sin correr, sin log; re-encolado funcionó): si se repite, considerar migrar la cola OBSERVAR a systemd-run o a un worker propio | M | propuesta |
| 16 | **Whisper medium para talks técnicas:** el transcript small de la charla de prueba tiene huecos audibles; medir small vs medium en la fragua (RAM/tiempo/calidad) para videos largos | M | propuesta |

### 2026-07-05 · reporte Reactivación 3 — cierre OBSERVAR E2E + Consolidación

| # | Sugerencia | Coste | Estado |
|---|---|---|---|
| 17 | **M5: el bus I2C sigue vacío TRAS el cableado** (scan fresco post-reset RTS: `found=[]`): revisar físicamente el Grove — que SDA/SCL caigan en los pines que escanea el firmware, alimentación 3.3V vs 5V, y cable bien asentado; el LED del RTC solo indica potencia, no bus. Amplía la #10. | S | propuesta |
| 18 | **Timer de la asesoría del Alquimista**: `asesor_cron.py` cita `OnCalendar=*:07` pero el `.timer` nunca se staged (solo existe el `.service`); crearlo espejo del de la Cosecha y aprobarlo | S | propuesta |
| 19 | **hexelion: dejar de trackear `disk_nodes.json`/`vessel_db.sqlite`** (`git rm --cached` + gitignore): runtime churn de pollers que mantiene el repo perpetuamente sucio; el criterio ya está escrito en el .gitignore de p0x | S | propuesta |
| 20 | **Ventana térmica para OBSERVAR largos**: la fragua se asienta en 81–85°C bajo inferencia sostenida; el checkpoint de fase ya evita rehacer trabajo, pero encolar por defecto los videos largos en horas frías (cron nocturno) o añadir ventilación activa ampliaría el margen del guard >80°C | M | propuesta |
