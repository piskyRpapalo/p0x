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
| 1 | **Gate 0 en paralelo, en los HP (x86):** instalar llama-factory/PEFT en un HP y correr el LoRA-juguete de 10 ejemplos esta semana — define qué hierro entrena antes de que exista el dataset, sin tocar el rack | S | **firmada (2026-07-12) vía dashboard** |
| 2 | **Dataset v1 sin esperar GPU:** generar los primeros 200-300 ejemplos desde los MDs existentes (voces, doctrina, alfabeto, esferas) — trabajo de texto puro; el activo transplantable empieza a existir hoy | M | **descartada (2026-07-12): Deprecated — vía dashboard** |
| 3 | **El teléfono: sensor antes que granja:** pesarlo como sensor (cámara RTSP para visión Fase 2, GPS/barómetro para el Vigía) antes de dedicarlo 24/7 a Acurast lite; si entra Acurast → patrón Mastchain exacto (read-only en dashboard, bond/claims = mano del Soberano) | S | **firmada (2026-07-12) vía dashboard** |

### 2026-07-04 · reporte Preceptor Local — Reactivación 2 (root cause CUDA + certificación)

| # | Sugerencia | Coste | Estado |
|---|---|---|---|
| 4 | **Instalar la residencia del cerebro en la-torre (1 paste):** CC tiene VETO de política para instalar persistencia remota; los artefactos están en `deploy/torre/` con instrucciones. Sin esto la auto-recuperación tras reboot depende del primer chat (ruleta nvmap). Comando: ver cabecera de `deploy/torre/modelo_residente.sh` | S | **firmada (2026-07-12) vía dashboard** |
| 5 | **journald persistente en la-torre** (`sudo mkdir -p /var/log/journal && sudo systemctl restart systemd-journald`): el incidente 13:40 no dejó journal consultable; hoy el rastro vive solo en `~/ollama.log` (drop-in) y syslog | S | **firmada (2026-07-12) vía dashboard** |
| 6 | **Vocero: deshornear los números OMIE del few-shot** (115.00 €/MWh fijo en el MD invita a citar precios rancios) — tras línea base n=20 del Protocolo §3 | S | **firmada (2026-07-12) vía dashboard** |
| 7 | **Fallback fragua digno:** qwen2.5:1.5b tarda 190-230 s en denso y garabatea síntesis doctrinal; evaluar por suite qwen3:1.7b o el instruct-2507 pequeño como OLLAMA_CHAT_MODEL | M | **firmada (2026-07-12) vía dashboard** |
| 8 | **Decidir `dashboard-v9/index-en.html`** (variante EN del Nexo sin trackear, no consta intención): trackear o borrar | S | **decidida (2026-07-11): BORRADA — la UI ya es inglés por invariante, snapshot con 11 días de deriva (sin REFLEX/panel), nunca trackeada ni referenciada. Decisión delegada por el Soberano (misión PÚBLICO SEGURO).** |
| 9 | **Suite de recarga semanal en la-torre** (cron propuesto: 1 ciclo restart+reclaim+carga con log): vigila que la receta siga 2/2 cuando cambien kernel/ollama/modelo | M | **firmada (2026-07-12) vía dashboard** |

### 2026-07-05 · reporte MISIÓN OBSERVAR + Consolidación Global

| # | Sugerencia | Coste | Estado |
|---|---|---|---|
| 10 | **Cablear los sensores del M5** (BME680/ADXL345/RTC al Grove): el bus I2C está físicamente vacío (`i2c_scan found=[]` verificado); toda la cadena M5→Redis→gateway→dashboard→Monje está viva esperando el primer dato real | S | **firmada (2026-07-12) vía dashboard** |
| 11 | **Pubkey SSH de el-vigia sigue caída** (acceso solo por password): restaurar `authorized_keys` del Pi elimina el password del camino y permite retirar sshpass | S | **firmada (2026-07-12) vía dashboard** |
| 12 | **Calibrar umbrales del motor delta con corpus real:** tras 5-10 videos aceptados, revisar los scores crudos persistidos en `delta.json` de cada job y ajustar `umbral_ya_sabido/umbral_nuevo` (hoy 0.82/0.55 provisionales) | M | **firmada (2026-07-12) vía dashboard** |
| 13 | **Revisar los `descripcion_niveles` generados** (marcador `generado_por: cc-pendiente-revision` en esferas y `niveles_doctrina.yaml`): leerlos una vez y quitar el marcador a los que valgan | S | **firmada (2026-07-12) vía dashboard** |
| 14 | **GitHub público: crear remote + push** de `~/hexelion-public/` (git init hecho, checklist de sanitización 0 hits, README = versión pública del Discurso): decisión y cuenta del Soberano | S | **hecha 2026-07-05** (OK del Soberano + push verificado; ver #23) |
| 15 | **Job queue: vigilar la anomalía tsp E-Level -1** (job 16 murió sin correr, sin log; re-encolado funcionó): si se repite, considerar migrar la cola OBSERVAR a systemd-run o a un worker propio | M | **firmada (2026-07-12) vía dashboard** |
| 16 | **Whisper medium para talks técnicas:** el transcript small de la charla de prueba tiene huecos audibles; medir small vs medium en la fragua (RAM/tiempo/calidad) para videos largos | M | **firmada (2026-07-12) vía dashboard** |

### 2026-07-05 · reporte Reactivación 3 — cierre OBSERVAR E2E + Consolidación

| # | Sugerencia | Coste | Estado |
|---|---|---|---|
| 17 | **M5: el bus I2C sigue vacío TRAS el cableado** (scan fresco post-reset RTS: `found=[]`): revisar físicamente el Grove — que SDA/SCL caigan en los pines que escanea el firmware, alimentación 3.3V vs 5V, y cable bien asentado; el LED del RTC solo indica potencia, no bus. Amplía la #10. | S | **verificada (2026-07-06): David cableó; scan I2C ve `0x53` ADXL345 / `0x57`+`0x68` DS3231 / `0x76` BME680; sensors {bme680,adxl345,rtc}=true, telemetría viva. Nota: RTC arranca en 2000-01-01 — falta fijar hora (sub-tarea #30).** |
| 18 | **Timer de la asesoría del Alquimista**: `asesor_cron.py` cita `OnCalendar=*:07` pero el `.timer` nunca se staged (solo existe el `.service`); crearlo espejo del de la Cosecha y aprobarlo | S | **firmada (2026-07-12) vía dashboard** |
| 19 | **hexelion: dejar de trackear `disk_nodes.json`/`vessel_db.sqlite`** (`git rm --cached` + gitignore): runtime churn de pollers que mantiene el repo perpetuamente sucio; el criterio ya está escrito en el .gitignore de p0x | S | **firmada (2026-07-12) vía dashboard** |
| 20 | **Ventana térmica para OBSERVAR largos**: la fragua se asienta en 81–85°C bajo inferencia sostenida; el checkpoint de fase ya evita rehacer trabajo, pero encolar por defecto los videos largos en horas frías (cron nocturno) o añadir ventilación activa ampliaría el margen del guard >80°C | M | **firmada (2026-07-12) vía dashboard** |

### 2026-07-05 · reporte misión PULIR + VOZ

| # | Sugerencia | Coste | Estado |
|---|---|---|---|
| 21 | **Voz del Sínodo, siguiente pase (si la calidad te vale)**: escucha los 6 clips de `voz/gate0/` y elige voz (sharvard vs davefx); el cableado sería un endpoint `/api/voz/di` en la fragua con Piper residente (~250MB RAM, latencia ~1s) + botón ▶ por respuesta en el Sínodo | M | **firmada (2026-07-12) vía dashboard** |
| 22 | **Bug preexistente del grafo**: `g.d3AlphaTarget is not a function` (force-graph.min.js local vs API usada; presente ya en el backup pre-riel) — no rompe el render pero ensucia consola; alinear versión del vendor o quitar la llamada | S | propuesta |
| 23 | **GitHub público — único paso restante**: crear el repo vacío `piskyRpapalo/hexelion-public` en github.com (la SSH key del rack autentica pero no puede CREAR repos); el remote ya está configurado y el push es inmediato. Alternativa: `! gh auth login` en sesión | S | **hecha 2026-07-05**: push verificado a `piskyRpapalo/-hexelion-public` (master 69d15f4); OJO guion inicial en el nombre — renombrar a `hexelion-public` en Settings (redirige solo) |

### 2026-07-05 · auditoría automática (skill auditar-p0x)

| # | Tarea propuesta | Coste | Estado |
|---|---|---|---|
| A1 | **pasada de poda §4.4: enterrar reglas sin evidencia en changelog** — `mente/voces/alquimista.md` (PODA: 4.2KB > presupuesto 4KB — poda obligatoria (§4.4)) [aud:PODA:mente/voces/alquimista.md] | M | propuesta |
| A2 | **pasada de poda §4.4: enterrar reglas sin evidencia en changelog** — `mente/voces/enlace.md` (PODA: 4.2KB > presupuesto 4KB — poda obligatoria (§4.4)) [aud:PODA:mente/voces/enlace.md] | M | propuesta |
| A3 | **pasada de poda §4.4: enterrar reglas sin evidencia en changelog** — `mente/voces/escriba.md` (PODA: 4.1KB > presupuesto 4KB — poda obligatoria (§4.4)) [aud:PODA:mente/voces/escriba.md] | M | propuesta |
| A4 | **pasada de poda §4.4: enterrar reglas sin evidencia en changelog** — `mente/voces/monje.md` (PODA: 5.9KB > presupuesto 4KB — poda obligatoria (§4.4)) [aud:PODA:mente/voces/monje.md] | M | **firmada (2026-07-12) vía dashboard** |
| A5 | **completar el contrato §2 (campos del carbono: que los fije David)** — `mente/doctrina/DISCURSO_FUNDACIONAL_P0X.md` (contrato-evolutivo-incompleto: clase=doctrina sin: metrica_exito, umbral_reedicion, presupuesto_kb, n_medicion, changelog) [aud:contrato-evolutivo-incompleto:mente/doctrina/DISCURSO_FUNDACIONAL_P0X.md] | S | propuesta |
| A6 | **completar el contrato §2 (campos del carbono: que los fije David)** — `mente/doctrina/DOCTRINA_AI_INTERNA_P0X.md` (contrato-evolutivo-incompleto: clase=doctrina sin: metrica_exito, umbral_reedicion, presupuesto_kb, n_medicion, changelog) [aud:contrato-evolutivo-incompleto:mente/doctrina/DOCTRINA_AI_INTERNA_P0X.md] | S | propuesta |
| A7 | **completar el contrato §2 (campos del carbono: que los fije David)** — `mente/doctrina/INSTRUCCIONES_P0X.md` (contrato-evolutivo-incompleto: clase=doctrina sin: metrica_exito, umbral_reedicion, presupuesto_kb, n_medicion) [aud:contrato-evolutivo-incompleto:mente/doctrina/INSTRUCCIONES_P0X.md] | S | propuesta |
| A8 | **completar el contrato §2 (campos del carbono: que los fije David)** — `mente/doctrina/ORQUESTA_MODELOS_P0X.md` (contrato-evolutivo-incompleto: clase=doctrina sin: metrica_exito, umbral_reedicion, presupuesto_kb, n_medicion, changelog) [aud:contrato-evolutivo-incompleto:mente/doctrina/ORQUESTA_MODELOS_P0X.md] | S | propuesta |

### 2026-07-05 · auditoría automática (skill auditar-p0x)

| # | Tarea propuesta | Coste | Estado |
|---|---|---|---|
| A1 | **completar el contrato §2 (campos del carbono: que los fije David)** — `mente/doctrina/PROCESO_EVALES_TRANSPLANTE_P0X.md` (contrato-evolutivo-incompleto: clase=doctrina sin: metrica_exito, umbral_reedicion, presupuesto_kb, n_medicion, changelog) [aud:contrato-evolutivo-incompleto:mente/doctrina/PROCESO_EVALES_TRANSPLANTE_P0X.md] | S | propuesta |
| A2 | **completar el contrato §2 (campos del carbono: que los fije David)** — `mente/doctrina/PROTOCOLO_MD_EVOLUTIVO_P0X.md` (contrato-evolutivo-incompleto: clase=doctrina sin: metrica_exito, umbral_reedicion, presupuesto_kb, n_medicion, changelog) [aud:contrato-evolutivo-incompleto:mente/doctrina/PROTOCOLO_MD_EVOLUTIVO_P0X.md] | S | **firmada (2026-07-12) vía dashboard** |
| A3 | **completar el contrato §2 (campos del carbono: que los fije David)** — `mente/esferas/near-ai.md` (contrato-evolutivo-incompleto: clase=operativo sin: metrica_exito, umbral_reedicion, presupuesto_kb, n_medicion, changelog) [aud:contrato-evolutivo-incompleto:mente/esferas/near-ai.md] | S | **firmada (2026-07-12) vía dashboard** |
| A4 | **completar el contrato §2 (campos del carbono: que los fije David)** — `mente/lengua/ALFABETO_P0X.md` (contrato-evolutivo-incompleto: clase=operativo sin: changelog) [aud:contrato-evolutivo-incompleto:mente/lengua/ALFABETO_P0X.md] | S | **firmada (2026-07-12) vía dashboard** |
| A5 | **correr gen_niveles.py sobre la esfera (marcar cc-pendiente-revision)** — `mente/grafo/second_brain.json` (esfera-sin-niveles: esfera `esfera-ia-fisica` sin descripcion_niveles (gen_niveles.py pendiente sobre ella)) [aud:esfera-sin-niveles:mente/grafo/second_brain.json] | S | **firmada (2026-07-12) vía dashboard** |
| A6 | **commit del cambio (el commit ES el registro, §5)** — `p0x:mente/auditorias/` (mente-sin-commit: cambio en la mente sin commitear (??)) [aud:mente-sin-commit:p0x:mente/auditorias/] | S | aplazada (2026-07-12) vía dashboard |
| A7 | **commit del cambio (el commit ES el registro, §5)** — `p0x:mente/feedback/PENDIENTES.md` (mente-sin-commit: cambio en la mente sin commitear (M)) [aud:mente-sin-commit:p0x:mente/feedback/PENDIENTES.md] | S | aplazada (2026-07-12) vía dashboard |
| A8 | **push al remote soberano (paracaídas)** — `hexelion` (push-pendiente: 1 commits sin empujar a origin/nexo-carbono-dashboard-20260623 (paracaídas caído)) [aud:push-pendiente:hexelion] | S | **firmada (2026-07-12) vía dashboard** |

### 2026-07-05 · reporte misión SKILL AUDITORA

| # | Sugerencia | Coste | Estado |
|---|---|---|---|
| 24 | **Pubkey el-vigia (cierra #11, paste de 1 línea — el clasificador vetó al silicio instalarla, patrón #4)**: `ssh pi@el-vigia "mkdir -p ~/.ssh && echo '$(cat ~/.ssh/id_ed25519.pub)' >> ~/.ssh/authorized_keys && chmod 700 ~/.ssh 600 ~/.ssh/authorized_keys"` — te pedirá el password una última vez; después sshpass se retira | S | **hecha (2026-07-06): pubkey instalada, `ssh -o BatchMode=yes pi@el-vigia` keyless OK; sshpass retirado.** |
| 25 | **Contrato §2 de las 6 doctrinas en una sesión**: los campos que faltan (metrica_exito/umbral/presupuesto/n_medicion) son del carbono; decidirlos en lote (30 min) cierra 12 de las 20 importantes de AUDIT_2026-07-05 de una vez. **DIFF LISTO (2026-07-06, misión VENTANA VIVA): `mente/auditorias/PROPUESTA_25_contratos.patch` (8 ficheros, tabla defaults doctrina + operativos justificados; `git apply --check` OK) — leer preámbulo y aplicar con `git apply`** | S | **hecha (FIRMADO por el Soberano 2026-07-06, commit `3f8952e`).** |
| 26 | **Primera PODA §4.4 del sistema (4 voces sobre presupuesto)**: el silicio puede PROPONER el diff de poda por voz (reglas sin evidencia en changelog) para tu firma — estrena el lazo completo propose→carbono→ejecuta. **DIFF LISTO (2026-07-06, misión VENTANA VIVA): `mente/auditorias/PROPUESTA_26_poda.patch` (qué sale y por qué en el preámbulo; contrato M5 del monje respetado + enmienda presupuesto 4→6 solo monje; `git apply --check` OK)** | M | **hecha (FIRMADO por el Soberano 2026-07-06, commit `17f90d5`).** |
| 27 | **Paste unit p0x-voz (residente: 681ms vs 3705ms frío, ~272MB RAM)** — el clasificador vetó al silicio instalar el servicio persistente (patrón #4): `sudo cp /mnt/nvme/p0x/deploy/fragua/p0x-voz.service /etc/systemd/system/ && sudo systemctl daemon-reload && sudo systemctl enable --now p0x-voz`. Mientras, hay un proceso manual niced vivo (muere en reboot); sin él la voz funciona en frío <4s | S | **hecha (2026-07-06): unit instalada, `enable --now`; `systemctl is-active p0x-voz`=active, `:8021/salud` ok, síntesis vía gateway con `x-voz-residente: 1`. Sobrevive reboot.** |
| 28 | **Runtime JS para yt-dlp (deno)**: yt-dlp 2026.06 avisa "YouTube extraction without a JS runtime has been deprecated" — hoy funciona, pero futuras versiones pueden perder formatos. `sudo apt install deno` o el paquete oficial; verificar con un ingest corto | S | **firmada (2026-07-12) vía dashboard** |
| 29 | **Voz por agente + pre-síntesis**: mapa agente→voz (p.ej. monje=davefx, alquimista=sharvard) en /api/voz + disparar síntesis en background al llegar cada respuesta del chat — con el cache, el ▶ sonaría al instante (latencia percibida ~0) | M | aplazada (2026-07-12) vía dashboard |

### 2026-07-07 · cierre VENTANA VIVA (bug REDUCE del vídeo largo)

| # | Sugerencia | Coste | Estado |
|---|---|---|---|
| 30 | **Fijar la hora del RTC del M5** (arranca en 2000-01-01): el DS3231 (`0x68`/`0x57`) ya está en el bus pero sin hora — un `set` una vez desde el-vigia (o al arrancar `p0x-m5-ingest`) y queda con batería. Sin esto los timestamps del sensor son basura si algún día se usan como reloj soberano. | S | **firmada (2026-07-12) vía dashboard** |
| 31 | **Cota dura de tokens en las síntesis largas del pipeline** (hecho parcial): la sección "## Lo nuevo" de REDUCE reventó `timeout=1800` con el vídeo de 19,7 min (28 claims NUEVO en un solo prompt). Arreglado esta sesión: `nuevos[:30]` + `num_predict=1024` en `render` + `timeout→2400` (`delta_engine.py`). PENDIENTE calibrar si 30/1024 es el punto óptimo con corpus real y si MAP/CLASSIFY necesitan la misma cota en vídeos de >30 min. | S | **hecha-parcial (2026-07-07): fix aplicado; falta calibrar con corpus.** |

### 2026-07-07 · misión LINKS LIMPIOS (dashboard hexelion)

| # | Sugerencia | Coste | Estado |
|---|---|---|---|
| 32 | **`tools/audit_links.py` al flujo regular / pre-commit**: el auditor nuevo (read-only) caza links rotos, links a endpoints de datos (`/api/*` navegado) y pageerrors en las 6 páginas. Engancharlo a un pre-commit o al ciclo de auditoría evita que otro `<a href="/api/*">` se vuelva a colar sin que nadie lo note. | S | **firmada (2026-07-12) vía dashboard** |
| 33 | **`/proof` es página huérfana**: sirve en `/proof` (Proof Marketplace, 200) pero NO está enlazada desde el dashboard ni el Sínodo — nadie llega a ella navegando. Decidir: darle un acceso desde el riel (junto a LIGHTHOUSE, que es su tema) o retirar la ruta. Su back button ya se arregló (`/`→`/dashboard`). | S | **decidida (2026-07-07, épica): /proof se retira del dashboard (LIGHTHOUSE fuera, atestación → chip de cabecera); la ruta no se enlaza, no se borra del repo.** |
| 34 | **Auditar el resto de llamadas force-graph en `second-brain`**: el pageerror `g.d3AlphaTarget is not a function` era una API inexistente que abortaba `initGraph` en silencio (nadie lo veía salvo la consola). Puede haber más métodos derivados de la librería; una pasada rápida por todas las llamadas `g.d3*()`/`g.*()` confirmaría que no queda otro fallo latente. | M | **firmada (2026-07-12) vía dashboard** |
| 35 | **¿Vista de cadena navegable propia para el Faro?**: hoy "◇ VIEW CHAIN" revela el JSON de `/api/faro` inline (fetch, no navegación — doctrina cumplida). Si el Soberano quiere una página read-only dedicada de la cadena (como `/proof`), se puede construir; el visor inline cubre la inspección mínima mientras tanto. | M | **firmada (2026-07-12) vía dashboard** |


### 2026-07-07 · misión TEMA ÉPICO (branch violeta) + GRAFO + README

| # | Sugerencia | Coste | Estado |
|---|---|---|---|
| 36 | **Selector de tema en la UI** (sovereign / aetheric / violeta): hoy `applyTheme('sovereign')` está fijo en el JS de `index.html`; un toggle discreto en la cabecera dejaría a David alternar temas sin branch ni puerto aparte. Los 3 bloques `[data-theme=…]` ya existen. | S | **firmada (2026-07-12) vía dashboard** |
| 37 | **Si David elige VIOLETA → promoción**: merge de la capa de color a la rama verde (activa) + **reskin COMPLETO de `sinodo.html`/`cosecha.html`** (hoy solo llevan un *wash* de fondo; sus componentes Tailwind conservan los colores SEMÁNTICOS de las voces/badges a propósito). Sin OK, el violeta se queda en la branch `theme-violeta` (reversible). | M | **descartada (2026-07-12): violeta out — vía dashboard** |
| 38 | **Servir previews de branch sin symlinks**: el violeta vive en worktree `~/hexelion-violeta` servido con `python -m http.server :8009` + symlinks de `assets/` (el `<base>`→:8001 lleva API/assets vivos). Una ruta read-only en el gateway (`/preview/<branch>`) o un `<base>` relativo harían el preview reproducible sin andamiaje manual. | M | **firmada (2026-07-12) vía dashboard** |
| 39 | **Modo "solo órganos" del Second Brain para capturas públicas**: esta sesión hubo que reencuadrar a mano (centrar en EL NEXO + zoom) para que el README NO expusiera los títulos de esferas/doctrinas del corpus. Un toggle/param `?system-only` que oculte la nube del Códice formalizaría capturas públicas seguras. | S | **firmada (2026-07-12) vía dashboard** |
| 40 | **Decisión soberana — ¿exponer títulos del corpus en el README público?**: `hexelion-public/screenshots/second-brain-full.png` está listo (grafo completo) pero muestra nombres de docs internos (Manual del Soberano, Protocolo MD Evolutivo, Doctrina de la AI Interna, Instrucciones del Proyecto…). El README usa por defecto la versión enfocada en órganos. Decidir antes del push público. | S | **firmada (2026-07-12) vía dashboard** |

### 2026-07-11 · misión ARQUEOLOGÍA P0X (auditoría read-only de ~/P0X → `mente/auditorias/ARQUEOLOGIA_2026-07-11.md`)

| # | Sugerencia | Coste | Estado |
|---|---|---|---|
| 41 | **Entierro motivado del mito fundacional (coherencia IronClaw)**: `HEXELION_AI_IDENTITY.md` ("No soy una herramienta, soy el juicio del organismo") + LORE (Crisálida/Primera-Luz) describen un organismo-con-voluntad que el P0X actual **deliberadamente ya no es**. Viven en `~/P0X` (no corrompen el vivo), pero si se reingestan como canon reintroducen la grandiosidad que IronClaw expulsó. Crear nodo(s) Necrópolis con motivo para blindar el bucle. | S | **firmada (2026-07-12) vía dashboard** |
| 42 | **Revivir el patrón `@sleeping`/`BATTERY_FLAG` (el envoltorio, NO el arbitraje)**: `HEXELION_BATTERY_FLAG_SPEC.md` (15-may) especifica un conmutador de Era por una variable + código dormido observable — elegante y compatible con honest-sensors, útil para la transición futura a batería. Revivir el mecanismo; jamás las tácticas de arbitraje energético autónomo (prohibidas por IronClaw). Complementa a `reflejo-bateria`. | M | **firmada (2026-07-12) vía dashboard** |
| 43 | **Verificar `HEXELION_REENCARNACION.md` contra la realidad actual**: es un runbook operativo real (reconstruir la Fragua en 30 min desde la "Bóveda Genoma" USB), pero escrito pre-P0X/NVMe. Releer y actualizar/enterrar según siga siendo válido — valor de recuperación ante desastre, no nostalgia. | S | **firmada (2026-07-12) vía dashboard** |
| 44 | **Rescatar el `_ESTADO.md` por dominio (gobernanza NEXUS)**: el esquema `HEXELION_NEXUS` (may) tenía un snapshot fechado por carpeta ("esto hay aquí hoy, qué contradice a qué"). El `mente/` actual ganó búsqueda+grafo pero perdió ese snapshot. Evaluar un `_ESTADO` por esfera-madre — barato, mejora trazabilidad. | S | **firmada (2026-07-12) vía dashboard** |
| 45 | **Crear la esfera `historia-p0x` + nodos-hito (Bloque 5 del informe)**: el mapa de la propia evolución del proyecto como nodo del grafo (esfera-madre + hitos Crisálida-15may / Profesionalización-24may / HEXELION→P0X). Propuesto en el informe, no ejecutado. | M | **firmada (2026-07-12) vía dashboard** |
| 46 | **Consolidación futura de `~/P0X` (decisión del Soberano)**: `MD 3/` es superconjunto; `files/`, `files22/`, `P0X/`, `p0x2/`, `CR/`, `propuesta/` son duplicados parciales. Material personal (CV/contrato/bitácora .docx) fuera de cualquier flujo del proyecto. Para lecturas futuras basta `MD 3/` + `HEXELION_NEXUS/`. Limpieza = mano de David (este pase fue read-only). | S | **firmada (2026-07-12) vía dashboard** |

### 2026-07-11 · misión CIERRE + VENTANA DE ESTADO

| # | Sugerencia | Coste | Estado |
|---|---|---|---|
| 47 | **Habilitar el watcher reflejo-bateria 24/7 (paste patrón #4)**: el arco está probado y el panel lo muestra honesto ("proposed · not enabled") — sin la unit, el Reflejo-1 solo corre a demanda. `sudo cp /mnt/nvme/p0x/deploy/fragua/reflejo-bateria.service /etc/systemd/system/ && sudo systemctl daemon-reload && sudo systemctl enable --now reflejo-bateria`. Verificar antes: `python3 deploy/fragua/reflejo_bateria_watch.py --once`. | S | **firmada (2026-07-12) vía dashboard** |
| 48 | **`reflejo-termico-m5` (Pista A · Reflejo #2)**: el BME680 late (temp/humedad/gas vivos) y con el RTC ya en hora sus lecturas son fechables. Watcher con el patrón de reflejo-bateria (histéresis + REFLEX + reflejos.jsonl), umbral de temperatura del rack → aviso protector. Declara su Era (`patron-era-energetica`). | M | aplazada (2026-07-12) vía dashboard |
| 49 | **`reflejo-vibracion` (Pista A · Reflejo #3)**: ADXL345 vivo; Δ\|g\| sobre umbral → evento "movimiento detectado" a consola. Solo aviso, jamás valor (IronClaw). | M | **firmada (2026-07-12) vía dashboard** |
| 50 | **Runbook `REENCARNACION_P0X.md` nuevo (el viejo quedó obsoleto — veredicto #42)**: el genoma real de hoy = bare repos en La Torre (p0x + hexelion + lab, push verificado) + Qdrant re-derivable por ingesta. Lo que HOY no está cubierto: estado Redis, `.env`/secretos, units systemd instaladas, receta docker. Un runbook de 1 página con eso cerraría la recuperación ante desastre real. | M | **firmada (2026-07-12) vía dashboard** |
| 51 | **Re-sync periódico del RTC del M5**: el DS3231 deriva (~±2 ppm/°C). Un cron mensual en el-vigia que pare ingest → `set_rtc_m5.py` → arranque ingest (2s de ventana) mantiene #30 cerrada para siempre. Propose-only si el clasificador veta el cron. | S | **firmada (2026-07-12) vía dashboard** |

### 2026-07-11 · misión PÚBLICO SEGURO + REFLEJOS

| # | Sugerencia | Coste | Estado |
|---|---|---|---|
| 52 | **Copia física de secretos (H1 del runbook — LA pieza que falta)**: `.env` (QDRANT_API_KEY), passwords NUT, identidad tailscale y ssh NO están en git (correcto) ni en NINGUNA copia. Un USB del Soberano con esos 4 elementos cifrados (gpg simétrico basta), actualizado al cambiar un secreto, convierte la Reencarnación de teoría a garantía. Sin esto, una fragua muerta = re-provisionar secretos a mano. | S | **firmada (2026-07-12) vía dashboard** |
| 53 | **Drill de Reencarnación (H3)**: ejecutar `REENCARNACION_P0X.md` en frío sobre un SBC de repuesto (o una SD limpia), cronometrar y anotar cada paso falso en el propio runbook (su `umbral_reedicion` lo exige). El runbook de mayo murió sin drill; que este no repita la historia. | M | **firmada (2026-07-12) vía dashboard** |
| 54 | **Habilitar la unit `reflejo-m5` (paste patrón #4, hermana de #47)**: los reflejos 2+3 están probados y el panel los muestra ARMADOS, pero solo corren a demanda. `sudo cp /mnt/nvme/p0x/deploy/fragua/reflejo-m5.service /etc/systemd/system/ && sudo systemctl daemon-reload && sudo systemctl enable --now reflejo-m5`. Con #47 y esto, la médula espinal completa queda viva 24/7. | S | **descartada (2026-07-12): cambiando de lugar a proximo proyecto. — vía dashboard** |
| 55 | **Barrido de secretos como pre-push del repo público**: `tools/secret_sweep.py` ya existe y está versionado; un hook `pre-push` en hexelion-public que lo ejecute (exit≠0 = push abortado) hace imposible publicar un CRIT por descuido — la seguridad deja de depender de la disciplina de la sesión. | S | aplazada (2026-07-12) vía dashboard |
| 56 | **Política para `dashboard-v9/screenshots/`**: ~60 capturas sin trackear acumulándose (evidencia de misiones). Decidir: (a) commitear las de evidencia por misión, (b) gitignore del directorio + evidencia solo en informes, o (c) carpeta `evidencia/` trackeada con las 2-3 clave por misión. Hoy el `git status` de hexelion es ruido permanente. | S | **firmada (2026-07-12) vía dashboard** |

### 2026-07-12 · misión TAREAS FIRMABLES + DIARIO VERDE

| # | Sugerencia | Coste | Estado |
|---|-----------|-------|--------|
| 57 | **Enchufar la webcam USB al soberano y hacer la primera captura de los 3 recipientes desde `/verde`**: el diario está vivo y honesto (hoy 503 `no-camera-detected`); en cuanto exista `/dev/video0` los botones se habilitan solos, sin reiniciar nada. La primera foto de la menta es el punto cero del registro de crecimiento. | S | **descartada (2026-07-12): in a few days. — vía dashboard** |
| 58 | **Análisis VLM del diario en asíncrono**: qwen3.5:2b tiene visión MEDIDA (54s con imagen diminuta en CPU RK3588; una 720p tardará minutos) — hoy el POST de captura espera el análisis. Mover el análisis a la cola batch (tsp) + endpoint de re-análisis por `id` (el hueco ya existe en el esquema del jsonl) para que la captura vuelva en segundos y el análisis llegue después. | M | **firmada (2026-07-12) vía dashboard** |
| 59 | **Primera sesión de vaciado de bandeja en `/tareas`**: 62 sugerencias abiertas + 13 esferas esperan firma. La herramienta ya existe (SIGN/DEFER/DISCARD con motivo, todo commiteado con backup); 20 minutos de mano del Soberano dejan la bandeja al día sin abrir una terminal. | S | **firmada (2026-07-12) vía dashboard** |
| 60 | **Retención de `/mnt/nvme/p0x/.backups/`**: cada acción de la bandeja deja un backup del MD tocado (correcto, pero crece sin límite). Una pasada de limpieza simple (conservar últimos 60 días o N=200) evita que el directorio se vuelva un vertedero invisible. | S | aplazada (2026-07-12) vía dashboard |
| 61 | **`/tareas` y `/verde` en `audit_overlaps.py`** (viewports 768/390): la bandeja de firma se usará desde el móvil del Soberano; hoy solo está auditada en desktop (audit_links 0/0/0). | S | **firmada (2026-07-12) vía dashboard** |

### 2026-07-12 · misión LEGIBILIDAD DE FORTALEZAS

| # | Sugerencia | Coste | Estado |
|---|-----------|-------|--------|
| 62 | **OK de David al push público → los badges se encienden**: el repo local lleva CI (`d36a5be`) + ADRs (`9cf98f2`) verificados con AMBOS sweeps a 0; Actions corre en el primer push y los 2 workflows deberían salir verdes a la primera. Verificar badges en GitHub tras el push. | S | **firmada (2026-07-12) vía dashboard** |
| 63 | **Hook pre-push con el sweep COMPLETO en hexelion-public** (materializa #55): el CI público cubre los patrones genéricos; el diccionario completo (literales del rack) debe correr en local antes de cada push. `cp` de un hook de 3 líneas a `.git/hooks/pre-push`. | S | **firmada (2026-07-12) vía dashboard** |
| 64 | **Primer pase de modularización del gateway** siguiendo `docs/PLAN_MODULARIZACION_GATEWAY.md` (hexelion `cddac29`): extraer `routers/tareas.py` verbatim con diff de rutas antes/después + audits 0/0/0. Un router por pase; maritime y websockets los últimos. | M | **firmada (2026-07-12) vía dashboard** |
| 65 | **"ADR al cierre" como paso del rito**: cuando una misión canoniza una decisión mayor, el cierre incluye exportar su ADR saneado a `docs/adr/` del público — la señal de gobernanza se mantiene viva sin misiones especiales. | S | **firmada (2026-07-12) vía dashboard** |
| 66 | **Sección de atestación en el README público**: `/proof` vive en la tailnet — un reclutador no la ve. Screenshot saneado de la vitrina (con la explicación 'What this page proves') + 3 líneas en el README, tras el checklist de secretos. | S | **firmada (2026-07-12) vía dashboard** |
