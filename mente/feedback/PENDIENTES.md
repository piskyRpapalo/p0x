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
| 14 | **GitHub público: crear remote + push** de `~/hexelion-public/` (git init hecho, checklist de sanitización 0 hits, README = versión pública del Discurso): decisión y cuenta del Soberano | S | **hecha 2026-07-05** (OK del Soberano + push verificado; ver #23) |
| 15 | **Job queue: vigilar la anomalía tsp E-Level -1** (job 16 murió sin correr, sin log; re-encolado funcionó): si se repite, considerar migrar la cola OBSERVAR a systemd-run o a un worker propio | M | propuesta |
| 16 | **Whisper medium para talks técnicas:** el transcript small de la charla de prueba tiene huecos audibles; medir small vs medium en la fragua (RAM/tiempo/calidad) para videos largos | M | propuesta |

### 2026-07-05 · reporte Reactivación 3 — cierre OBSERVAR E2E + Consolidación

| # | Sugerencia | Coste | Estado |
|---|---|---|---|
| 17 | **M5: el bus I2C sigue vacío TRAS el cableado** (scan fresco post-reset RTS: `found=[]`): revisar físicamente el Grove — que SDA/SCL caigan en los pines que escanea el firmware, alimentación 3.3V vs 5V, y cable bien asentado; el LED del RTC solo indica potencia, no bus. Amplía la #10. | S | **verificada (2026-07-06): David cableó; scan I2C ve `0x53` ADXL345 / `0x57`+`0x68` DS3231 / `0x76` BME680; sensors {bme680,adxl345,rtc}=true, telemetría viva. Nota: RTC arranca en 2000-01-01 — falta fijar hora (sub-tarea #30).** |
| 18 | **Timer de la asesoría del Alquimista**: `asesor_cron.py` cita `OnCalendar=*:07` pero el `.timer` nunca se staged (solo existe el `.service`); crearlo espejo del de la Cosecha y aprobarlo | S | propuesta |
| 19 | **hexelion: dejar de trackear `disk_nodes.json`/`vessel_db.sqlite`** (`git rm --cached` + gitignore): runtime churn de pollers que mantiene el repo perpetuamente sucio; el criterio ya está escrito en el .gitignore de p0x | S | propuesta |
| 20 | **Ventana térmica para OBSERVAR largos**: la fragua se asienta en 81–85°C bajo inferencia sostenida; el checkpoint de fase ya evita rehacer trabajo, pero encolar por defecto los videos largos en horas frías (cron nocturno) o añadir ventilación activa ampliaría el margen del guard >80°C | M | propuesta |

### 2026-07-05 · reporte misión PULIR + VOZ

| # | Sugerencia | Coste | Estado |
|---|---|---|---|
| 21 | **Voz del Sínodo, siguiente pase (si la calidad te vale)**: escucha los 6 clips de `voz/gate0/` y elige voz (sharvard vs davefx); el cableado sería un endpoint `/api/voz/di` en la fragua con Piper residente (~250MB RAM, latencia ~1s) + botón ▶ por respuesta en el Sínodo | M | propuesta |
| 22 | **Bug preexistente del grafo**: `g.d3AlphaTarget is not a function` (force-graph.min.js local vs API usada; presente ya en el backup pre-riel) — no rompe el render pero ensucia consola; alinear versión del vendor o quitar la llamada | S | propuesta |
| 23 | **GitHub público — único paso restante**: crear el repo vacío `piskyRpapalo/hexelion-public` en github.com (la SSH key del rack autentica pero no puede CREAR repos); el remote ya está configurado y el push es inmediato. Alternativa: `! gh auth login` en sesión | S | **hecha 2026-07-05**: push verificado a `piskyRpapalo/-hexelion-public` (master 69d15f4); OJO guion inicial en el nombre — renombrar a `hexelion-public` en Settings (redirige solo) |

### 2026-07-05 · auditoría automática (skill auditar-p0x)

| # | Tarea propuesta | Coste | Estado |
|---|---|---|---|
| A1 | **pasada de poda §4.4: enterrar reglas sin evidencia en changelog** — `mente/voces/alquimista.md` (PODA: 4.2KB > presupuesto 4KB — poda obligatoria (§4.4)) [aud:PODA:mente/voces/alquimista.md] | M | propuesta |
| A2 | **pasada de poda §4.4: enterrar reglas sin evidencia en changelog** — `mente/voces/enlace.md` (PODA: 4.2KB > presupuesto 4KB — poda obligatoria (§4.4)) [aud:PODA:mente/voces/enlace.md] | M | propuesta |
| A3 | **pasada de poda §4.4: enterrar reglas sin evidencia en changelog** — `mente/voces/escriba.md` (PODA: 4.1KB > presupuesto 4KB — poda obligatoria (§4.4)) [aud:PODA:mente/voces/escriba.md] | M | propuesta |
| A4 | **pasada de poda §4.4: enterrar reglas sin evidencia en changelog** — `mente/voces/monje.md` (PODA: 5.9KB > presupuesto 4KB — poda obligatoria (§4.4)) [aud:PODA:mente/voces/monje.md] | M | propuesta |
| A5 | **completar el contrato §2 (campos del carbono: que los fije David)** — `mente/doctrina/DISCURSO_FUNDACIONAL_P0X.md` (contrato-evolutivo-incompleto: clase=doctrina sin: metrica_exito, umbral_reedicion, presupuesto_kb, n_medicion, changelog) [aud:contrato-evolutivo-incompleto:mente/doctrina/DISCURSO_FUNDACIONAL_P0X.md] | S | propuesta |
| A6 | **completar el contrato §2 (campos del carbono: que los fije David)** — `mente/doctrina/DOCTRINA_AI_INTERNA_P0X.md` (contrato-evolutivo-incompleto: clase=doctrina sin: metrica_exito, umbral_reedicion, presupuesto_kb, n_medicion, changelog) [aud:contrato-evolutivo-incompleto:mente/doctrina/DOCTRINA_AI_INTERNA_P0X.md] | S | propuesta |
| A7 | **completar el contrato §2 (campos del carbono: que los fije David)** — `mente/doctrina/INSTRUCCIONES_P0X.md` (contrato-evolutivo-incompleto: clase=doctrina sin: metrica_exito, umbral_reedicion, presupuesto_kb, n_medicion) [aud:contrato-evolutivo-incompleto:mente/doctrina/INSTRUCCIONES_P0X.md] | S | propuesta |
| A8 | **completar el contrato §2 (campos del carbono: que los fije David)** — `mente/doctrina/ORQUESTA_MODELOS_P0X.md` (contrato-evolutivo-incompleto: clase=doctrina sin: metrica_exito, umbral_reedicion, presupuesto_kb, n_medicion, changelog) [aud:contrato-evolutivo-incompleto:mente/doctrina/ORQUESTA_MODELOS_P0X.md] | S | propuesta |

### 2026-07-05 · auditoría automática (skill auditar-p0x)

| # | Tarea propuesta | Coste | Estado |
|---|---|---|---|
| A1 | **completar el contrato §2 (campos del carbono: que los fije David)** — `mente/doctrina/PROCESO_EVALES_TRANSPLANTE_P0X.md` (contrato-evolutivo-incompleto: clase=doctrina sin: metrica_exito, umbral_reedicion, presupuesto_kb, n_medicion, changelog) [aud:contrato-evolutivo-incompleto:mente/doctrina/PROCESO_EVALES_TRANSPLANTE_P0X.md] | S | propuesta |
| A2 | **completar el contrato §2 (campos del carbono: que los fije David)** — `mente/doctrina/PROTOCOLO_MD_EVOLUTIVO_P0X.md` (contrato-evolutivo-incompleto: clase=doctrina sin: metrica_exito, umbral_reedicion, presupuesto_kb, n_medicion, changelog) [aud:contrato-evolutivo-incompleto:mente/doctrina/PROTOCOLO_MD_EVOLUTIVO_P0X.md] | S | propuesta |
| A3 | **completar el contrato §2 (campos del carbono: que los fije David)** — `mente/esferas/near-ai.md` (contrato-evolutivo-incompleto: clase=operativo sin: metrica_exito, umbral_reedicion, presupuesto_kb, n_medicion, changelog) [aud:contrato-evolutivo-incompleto:mente/esferas/near-ai.md] | S | propuesta |
| A4 | **completar el contrato §2 (campos del carbono: que los fije David)** — `mente/lengua/ALFABETO_P0X.md` (contrato-evolutivo-incompleto: clase=operativo sin: changelog) [aud:contrato-evolutivo-incompleto:mente/lengua/ALFABETO_P0X.md] | S | propuesta |
| A5 | **correr gen_niveles.py sobre la esfera (marcar cc-pendiente-revision)** — `mente/grafo/second_brain.json` (esfera-sin-niveles: esfera `esfera-ia-fisica` sin descripcion_niveles (gen_niveles.py pendiente sobre ella)) [aud:esfera-sin-niveles:mente/grafo/second_brain.json] | S | propuesta |
| A6 | **commit del cambio (el commit ES el registro, §5)** — `p0x:mente/auditorias/` (mente-sin-commit: cambio en la mente sin commitear (??)) [aud:mente-sin-commit:p0x:mente/auditorias/] | S | propuesta |
| A7 | **commit del cambio (el commit ES el registro, §5)** — `p0x:mente/feedback/PENDIENTES.md` (mente-sin-commit: cambio en la mente sin commitear (M)) [aud:mente-sin-commit:p0x:mente/feedback/PENDIENTES.md] | S | propuesta |
| A8 | **push al remote soberano (paracaídas)** — `hexelion` (push-pendiente: 1 commits sin empujar a origin/nexo-carbono-dashboard-20260623 (paracaídas caído)) [aud:push-pendiente:hexelion] | S | propuesta |

### 2026-07-05 · reporte misión SKILL AUDITORA

| # | Sugerencia | Coste | Estado |
|---|---|---|---|
| 24 | **Pubkey el-vigia (cierra #11, paste de 1 línea — el clasificador vetó al silicio instalarla, patrón #4)**: `ssh pi@el-vigia "mkdir -p ~/.ssh && echo '$(cat ~/.ssh/id_ed25519.pub)' >> ~/.ssh/authorized_keys && chmod 700 ~/.ssh 600 ~/.ssh/authorized_keys"` — te pedirá el password una última vez; después sshpass se retira | S | **hecha (2026-07-06): pubkey instalada, `ssh -o BatchMode=yes pi@el-vigia` keyless OK; sshpass retirado.** |
| 25 | **Contrato §2 de las 6 doctrinas en una sesión**: los campos que faltan (metrica_exito/umbral/presupuesto/n_medicion) son del carbono; decidirlos en lote (30 min) cierra 12 de las 20 importantes de AUDIT_2026-07-05 de una vez. **DIFF LISTO (2026-07-06, misión VENTANA VIVA): `mente/auditorias/PROPUESTA_25_contratos.patch` (8 ficheros, tabla defaults doctrina + operativos justificados; `git apply --check` OK) — leer preámbulo y aplicar con `git apply`** | S | **hecha (FIRMADO por el Soberano 2026-07-06, commit `3f8952e`).** |
| 26 | **Primera PODA §4.4 del sistema (4 voces sobre presupuesto)**: el silicio puede PROPONER el diff de poda por voz (reglas sin evidencia en changelog) para tu firma — estrena el lazo completo propose→carbono→ejecuta. **DIFF LISTO (2026-07-06, misión VENTANA VIVA): `mente/auditorias/PROPUESTA_26_poda.patch` (qué sale y por qué en el preámbulo; contrato M5 del monje respetado + enmienda presupuesto 4→6 solo monje; `git apply --check` OK)** | M | **hecha (FIRMADO por el Soberano 2026-07-06, commit `17f90d5`).** |
| 27 | **Paste unit p0x-voz (residente: 681ms vs 3705ms frío, ~272MB RAM)** — el clasificador vetó al silicio instalar el servicio persistente (patrón #4): `sudo cp /mnt/nvme/p0x/deploy/fragua/p0x-voz.service /etc/systemd/system/ && sudo systemctl daemon-reload && sudo systemctl enable --now p0x-voz`. Mientras, hay un proceso manual niced vivo (muere en reboot); sin él la voz funciona en frío <4s | S | **hecha (2026-07-06): unit instalada, `enable --now`; `systemctl is-active p0x-voz`=active, `:8021/salud` ok, síntesis vía gateway con `x-voz-residente: 1`. Sobrevive reboot.** |
| 28 | **Runtime JS para yt-dlp (deno)**: yt-dlp 2026.06 avisa "YouTube extraction without a JS runtime has been deprecated" — hoy funciona, pero futuras versiones pueden perder formatos. `sudo apt install deno` o el paquete oficial; verificar con un ingest corto | S | propuesta |
| 29 | **Voz por agente + pre-síntesis**: mapa agente→voz (p.ej. monje=davefx, alquimista=sharvard) en /api/voz + disparar síntesis en background al llegar cada respuesta del chat — con el cache, el ▶ sonaría al instante (latencia percibida ~0) | M | propuesta |

### 2026-07-07 · cierre VENTANA VIVA (bug REDUCE del vídeo largo)

| # | Sugerencia | Coste | Estado |
|---|---|---|---|
| 30 | **Fijar la hora del RTC del M5** (arranca en 2000-01-01): el DS3231 (`0x68`/`0x57`) ya está en el bus pero sin hora — un `set` una vez desde el-vigia (o al arrancar `p0x-m5-ingest`) y queda con batería. Sin esto los timestamps del sensor son basura si algún día se usan como reloj soberano. | S | propuesta |
| 31 | **Cota dura de tokens en las síntesis largas del pipeline** (hecho parcial): la sección "## Lo nuevo" de REDUCE reventó `timeout=1800` con el vídeo de 19,7 min (28 claims NUEVO en un solo prompt). Arreglado esta sesión: `nuevos[:30]` + `num_predict=1024` en `render` + `timeout→2400` (`delta_engine.py`). PENDIENTE calibrar si 30/1024 es el punto óptimo con corpus real y si MAP/CLASSIFY necesitan la misma cota en vídeos de >30 min. | S | **hecha-parcial (2026-07-07): fix aplicado; falta calibrar con corpus.** |
