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
| 19 | **hexelion: dejar de trackear `disk_nodes.json`/`vessel_db.sqlite`** (`git rm --cached` + gitignore): runtime churn de pollers que mantiene el repo perpetuamente sucio; el criterio ya está escrito en el .gitignore de p0x | S | **hecha de facto (verificado 2026-07-14): ambos ya gitignored, repo limpio) — CC** |
| 20 | **Ventana térmica para OBSERVAR largos**: la fragua se asienta en 81–85°C bajo inferencia sostenida; el checkpoint de fase ya evita rehacer trabajo, pero encolar por defecto los videos largos en horas frías (cron nocturno) o añadir ventilación activa ampliaría el margen del guard >80°C | M | **firmada (2026-07-12) vía dashboard** |

### 2026-07-05 · reporte misión PULIR + VOZ

| # | Sugerencia | Coste | Estado |
|---|---|---|---|
| 21 | **Voz del Sínodo, siguiente pase (si la calidad te vale)**: escucha los 6 clips de `voz/gate0/` y elige voz (sharvard vs davefx); el cableado sería un endpoint `/api/voz/di` en la fragua con Piper residente (~250MB RAM, latencia ~1s) + botón ▶ por respuesta en el Sínodo | M | **firmada (2026-07-12) vía dashboard** |
| 22 | **Bug preexistente del grafo**: `g.d3AlphaTarget is not a function` (force-graph.min.js local vs API usada; presente ya en el backup pre-riel) — no rompe el render pero ensucia consola; alinear versión del vendor o quitar la llamada | S | **hecha (2026-07-14): la llamada ya estaba retirada (0 errores de consola en /second-brain, verificado); el vendor SÍ define d3AlphaTarget — comentario engañoso corregido (`0918fb9`) — CC** |
| 23 | **GitHub público — único paso restante**: crear el repo vacío `piskyRpapalo/hexelion-public` en github.com (la SSH key del rack autentica pero no puede CREAR repos); el remote ya está configurado y el push es inmediato. Alternativa: `! gh auth login` en sesión | S | **hecha 2026-07-05**: push verificado a `piskyRpapalo/-hexelion-public` (master 69d15f4); OJO guion inicial en el nombre — renombrar a `hexelion-public` en Settings (redirige solo) |

### 2026-07-05 · auditoría automática (skill auditar-p0x)

| # | Tarea propuesta | Coste | Estado |
|---|---|---|---|
| A1 | **pasada de poda §4.4: enterrar reglas sin evidencia en changelog** — `mente/voces/alquimista.md` (PODA: 4.2KB > presupuesto 4KB — poda obligatoria (§4.4)) [aud:PODA:mente/voces/alquimista.md] | M | **firmada (2026-07-12) vía dashboard** |
| A2 | **pasada de poda §4.4: enterrar reglas sin evidencia en changelog** — `mente/voces/enlace.md` (PODA: 4.2KB > presupuesto 4KB — poda obligatoria (§4.4)) [aud:PODA:mente/voces/enlace.md] | M | **firmada (2026-07-12) vía dashboard** |
| A3 | **pasada de poda §4.4: enterrar reglas sin evidencia en changelog** — `mente/voces/escriba.md` (PODA: 4.1KB > presupuesto 4KB — poda obligatoria (§4.4)) [aud:PODA:mente/voces/escriba.md] | M | **firmada (2026-07-12) vía dashboard** |
| A4 | **pasada de poda §4.4: enterrar reglas sin evidencia en changelog** — `mente/voces/monje.md` (PODA: 5.9KB > presupuesto 4KB — poda obligatoria (§4.4)) [aud:PODA:mente/voces/monje.md] | M | **firmada (2026-07-12) vía dashboard** |
| A5 | **completar el contrato §2 (campos del carbono: que los fije David)** — `mente/doctrina/DISCURSO_FUNDACIONAL_P0X.md` (contrato-evolutivo-incompleto: clase=doctrina sin: metrica_exito, umbral_reedicion, presupuesto_kb, n_medicion, changelog) [aud:contrato-evolutivo-incompleto:mente/doctrina/DISCURSO_FUNDACIONAL_P0X.md] | S | **firmada (2026-07-12) vía dashboard** |
| A6 | **completar el contrato §2 (campos del carbono: que los fije David)** — `mente/doctrina/DOCTRINA_AI_INTERNA_P0X.md` (contrato-evolutivo-incompleto: clase=doctrina sin: metrica_exito, umbral_reedicion, presupuesto_kb, n_medicion, changelog) [aud:contrato-evolutivo-incompleto:mente/doctrina/DOCTRINA_AI_INTERNA_P0X.md] | S | **firmada (2026-07-12) vía dashboard** |
| A7 | **completar el contrato §2 (campos del carbono: que los fije David)** — `mente/doctrina/INSTRUCCIONES_P0X.md` (contrato-evolutivo-incompleto: clase=doctrina sin: metrica_exito, umbral_reedicion, presupuesto_kb, n_medicion) [aud:contrato-evolutivo-incompleto:mente/doctrina/INSTRUCCIONES_P0X.md] | S | **firmada (2026-07-12) vía dashboard** |
| A8 | **completar el contrato §2 (campos del carbono: que los fije David)** — `mente/doctrina/ORQUESTA_MODELOS_P0X.md` (contrato-evolutivo-incompleto: clase=doctrina sin: metrica_exito, umbral_reedicion, presupuesto_kb, n_medicion, changelog) [aud:contrato-evolutivo-incompleto:mente/doctrina/ORQUESTA_MODELOS_P0X.md] | S | **firmada (2026-07-12) vía dashboard** |

### 2026-07-05 · auditoría automática (skill auditar-p0x)

| # | Tarea propuesta | Coste | Estado |
|---|---|---|---|
| A1 | **completar el contrato §2 (campos del carbono: que los fije David)** — `mente/doctrina/PROCESO_EVALES_TRANSPLANTE_P0X.md` (contrato-evolutivo-incompleto: clase=doctrina sin: metrica_exito, umbral_reedicion, presupuesto_kb, n_medicion, changelog) [aud:contrato-evolutivo-incompleto:mente/doctrina/PROCESO_EVALES_TRANSPLANTE_P0X.md] | S | **firmada (2026-07-12) vía dashboard** |
| A2 | **completar el contrato §2 (campos del carbono: que los fije David)** — `mente/doctrina/PROTOCOLO_MD_EVOLUTIVO_P0X.md` (contrato-evolutivo-incompleto: clase=doctrina sin: metrica_exito, umbral_reedicion, presupuesto_kb, n_medicion, changelog) [aud:contrato-evolutivo-incompleto:mente/doctrina/PROTOCOLO_MD_EVOLUTIVO_P0X.md] | S | **firmada (2026-07-12) vía dashboard** |
| A3 | **completar el contrato §2 (campos del carbono: que los fije David)** — `mente/esferas/near-ai.md` (contrato-evolutivo-incompleto: clase=operativo sin: metrica_exito, umbral_reedicion, presupuesto_kb, n_medicion, changelog) [aud:contrato-evolutivo-incompleto:mente/esferas/near-ai.md] | S | **firmada (2026-07-12) vía dashboard** |
| A4 | **completar el contrato §2 (campos del carbono: que los fije David)** — `mente/lengua/ALFABETO_P0X.md` (contrato-evolutivo-incompleto: clase=operativo sin: changelog) [aud:contrato-evolutivo-incompleto:mente/lengua/ALFABETO_P0X.md] | S | **firmada (2026-07-12) vía dashboard** |
| A5 | **correr gen_niveles.py sobre la esfera (marcar cc-pendiente-revision)** — `mente/grafo/second_brain.json` (esfera-sin-niveles: esfera `esfera-ia-fisica` sin descripcion_niveles (gen_niveles.py pendiente sobre ella)) [aud:esfera-sin-niveles:mente/grafo/second_brain.json] | S | **firmada (2026-07-12) vía dashboard** |
| A6 | **commit del cambio (el commit ES el registro, §5)** — `p0x:mente/auditorias/` (mente-sin-commit: cambio en la mente sin commitear (??)) [aud:mente-sin-commit:p0x:mente/auditorias/] | S | **firmada (2026-07-12) vía dashboard** |
| A7 | **commit del cambio (el commit ES el registro, §5)** — `p0x:mente/feedback/PENDIENTES.md` (mente-sin-commit: cambio en la mente sin commitear (M)) [aud:mente-sin-commit:p0x:mente/feedback/PENDIENTES.md] | S | **firmada (2026-07-12) vía dashboard** |
| A8 | **push al remote soberano (paracaídas)** — `hexelion` (push-pendiente: 1 commits sin empujar a origin/nexo-carbono-dashboard-20260623 (paracaídas caído)) [aud:push-pendiente:hexelion] | S | **firmada (2026-07-12) vía dashboard** |

### 2026-07-05 · reporte misión SKILL AUDITORA

| # | Sugerencia | Coste | Estado |
|---|---|---|---|
| 24 | **Pubkey el-vigia (cierra #11, paste de 1 línea — el clasificador vetó al silicio instalarla, patrón #4)**: `ssh pi@el-vigia "mkdir -p ~/.ssh && echo '$(cat ~/.ssh/id_ed25519.pub)' >> ~/.ssh/authorized_keys && chmod 700 ~/.ssh 600 ~/.ssh/authorized_keys"` — te pedirá el password una última vez; después sshpass se retira | S | **hecha (2026-07-06): pubkey instalada, `ssh -o BatchMode=yes pi@el-vigia` keyless OK; sshpass retirado.** |
| 25 | **Contrato §2 de las 6 doctrinas en una sesión**: los campos que faltan (metrica_exito/umbral/presupuesto/n_medicion) son del carbono; decidirlos en lote (30 min) cierra 12 de las 20 importantes de AUDIT_2026-07-05 de una vez. **DIFF LISTO (2026-07-06, misión VENTANA VIVA): `mente/auditorias/PROPUESTA_25_contratos.patch` (8 ficheros, tabla defaults doctrina + operativos justificados; `git apply --check` OK) — leer preámbulo y aplicar con `git apply`** | S | **hecha (FIRMADO por el Soberano 2026-07-06, commit `3f8952e`).** |
| 26 | **Primera PODA §4.4 del sistema (4 voces sobre presupuesto)**: el silicio puede PROPONER el diff de poda por voz (reglas sin evidencia en changelog) para tu firma — estrena el lazo completo propose→carbono→ejecuta. **DIFF LISTO (2026-07-06, misión VENTANA VIVA): `mente/auditorias/PROPUESTA_26_poda.patch` (qué sale y por qué en el preámbulo; contrato M5 del monje respetado + enmienda presupuesto 4→6 solo monje; `git apply --check` OK)** | M | **hecha (FIRMADO por el Soberano 2026-07-06, commit `17f90d5`).** |
| 27 | **Paste unit p0x-voz (residente: 681ms vs 3705ms frío, ~272MB RAM)** — el clasificador vetó al silicio instalar el servicio persistente (patrón #4): `sudo cp /mnt/nvme/p0x/deploy/fragua/p0x-voz.service /etc/systemd/system/ && sudo systemctl daemon-reload && sudo systemctl enable --now p0x-voz`. Mientras, hay un proceso manual niced vivo (muere en reboot); sin él la voz funciona en frío <4s | S | **hecha (2026-07-06): unit instalada, `enable --now`; `systemctl is-active p0x-voz`=active, `:8021/salud` ok, síntesis vía gateway con `x-voz-residente: 1`. Sobrevive reboot.** |
| 28 | **Runtime JS para yt-dlp (deno)**: yt-dlp 2026.06 avisa "YouTube extraction without a JS runtime has been deprecated" — hoy funciona, pero futuras versiones pueden perder formatos. `sudo apt install deno` o el paquete oficial; verificar con un ingest corto | S | **firmada (2026-07-12) vía dashboard** |
| 29 | **Voz por agente + pre-síntesis**: mapa agente→voz (p.ej. monje=davefx, alquimista=sharvard) en /api/voz + disparar síntesis en background al llegar cada respuesta del chat — con el cache, el ▶ sonaría al instante (latencia percibida ~0) | M | **superseded (2026-07-19): decisión del Soberano — muere el mapa agente→voz, UNA sola voz para HEXELION. Se conserva la mitad viva (pre-síntesis en background + cache por hash), reimplementada single-voice en la Misión G1-R Bloque D — vía relevo del Preceptor** |

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
| 48 | **`reflejo-termico-m5` (Pista A · Reflejo #2)**: el BME680 late (temp/humedad/gas vivos) y con el RTC ya en hora sus lecturas son fechables. Watcher con el patrón de reflejo-bateria (histéresis + REFLEX + reflejos.jsonl), umbral de temperatura del rack → aviso protector. Declara su Era (`patron-era-energetica`). | M | **firmada (2026-07-12) vía dashboard** |
| 49 | **`reflejo-vibracion` (Pista A · Reflejo #3)**: ADXL345 vivo; Δ\|g\| sobre umbral → evento "movimiento detectado" a consola. Solo aviso, jamás valor (IronClaw). | M | **firmada (2026-07-12) vía dashboard** |
| 50 | **Runbook `REENCARNACION_P0X.md` nuevo (el viejo quedó obsoleto — veredicto #42)**: el genoma real de hoy = bare repos en La Torre (p0x + hexelion + lab, push verificado) + Qdrant re-derivable por ingesta. Lo que HOY no está cubierto: estado Redis, `.env`/secretos, units systemd instaladas, receta docker. Un runbook de 1 página con eso cerraría la recuperación ante desastre real. | M | **firmada (2026-07-12) vía dashboard** |
| 51 | **Re-sync periódico del RTC del M5**: el DS3231 deriva (~±2 ppm/°C). Un cron mensual en el-vigia que pare ingest → `set_rtc_m5.py` → arranque ingest (2s de ventana) mantiene #30 cerrada para siempre. Propose-only si el clasificador veta el cron. | S | **firmada (2026-07-12) vía dashboard** |

### 2026-07-11 · misión PÚBLICO SEGURO + REFLEJOS

| # | Sugerencia | Coste | Estado |
|---|---|---|---|
| 52 | **Copia física de secretos (H1 del runbook — LA pieza que falta)**: `.env` (QDRANT_API_KEY), passwords NUT, identidad tailscale y ssh NO están en git (correcto) ni en NINGUNA copia. Un USB del Soberano con esos 4 elementos cifrados (gpg simétrico basta), actualizado al cambiar un secreto, convierte la Reencarnación de teoría a garantía. Sin esto, una fragua muerta = re-provisionar secretos a mano. | S | **firmada (2026-07-12) vía dashboard** |
| 53 | **Drill de Reencarnación (H3)**: ejecutar `REENCARNACION_P0X.md` en frío sobre un SBC de repuesto (o una SD limpia), cronometrar y anotar cada paso falso en el propio runbook (su `umbral_reedicion` lo exige). El runbook de mayo murió sin drill; que este no repita la historia. | M | **firmada (2026-07-12) vía dashboard** |
| 54 | **Habilitar la unit `reflejo-m5` (paste patrón #4, hermana de #47)**: los reflejos 2+3 están probados y el panel los muestra ARMADOS, pero solo corren a demanda. `sudo cp /mnt/nvme/p0x/deploy/fragua/reflejo-m5.service /etc/systemd/system/ && sudo systemctl daemon-reload && sudo systemctl enable --now reflejo-m5`. Con #47 y esto, la médula espinal completa queda viva 24/7. | S | **descartada (2026-07-12): cambiando de lugar a proximo proyecto. — vía dashboard** |
| 55 | **Barrido de secretos como pre-push del repo público**: `tools/secret_sweep.py` ya existe y está versionado; un hook `pre-push` en hexelion-public que lo ejecute (exit≠0 = push abortado) hace imposible publicar un CRIT por descuido — la seguridad deja de depender de la disciplina de la sesión. | S | **firmada (2026-07-12) vía dashboard** |
| 56 | **Política para `dashboard-v9/screenshots/`**: ~60 capturas sin trackear acumulándose (evidencia de misiones). Decidir: (a) commitear las de evidencia por misión, (b) gitignore del directorio + evidencia solo en informes, o (c) carpeta `evidencia/` trackeada con las 2-3 clave por misión. Hoy el `git status` de hexelion es ruido permanente. | S | **firmada (2026-07-12) vía dashboard** |

### 2026-07-12 · misión TAREAS FIRMABLES + DIARIO VERDE

| # | Sugerencia | Coste | Estado |
|---|-----------|-------|--------|
| 57 | **Enchufar la webcam USB al soberano y hacer la primera captura de los 3 recipientes desde `/verde`**: el diario está vivo y honesto (hoy 503 `no-camera-detected`); en cuanto exista `/dev/video0` los botones se habilitan solos, sin reiniciar nada. La primera foto de la menta es el punto cero del registro de crecimiento. | S | **descartada (2026-07-12): in a few days. — vía dashboard** |
| 58 | **Análisis VLM del diario en asíncrono**: qwen3.5:2b tiene visión MEDIDA (54s con imagen diminuta en CPU RK3588; una 720p tardará minutos) — hoy el POST de captura espera el análisis. Mover el análisis a la cola batch (tsp) + endpoint de re-análisis por `id` (el hueco ya existe en el esquema del jsonl) para que la captura vuelva en segundos y el análisis llegue después. | M | **firmada (2026-07-12) vía dashboard** |
| 59 | **Primera sesión de vaciado de bandeja en `/tareas`**: 62 sugerencias abiertas + 13 esferas esperan firma. La herramienta ya existe (SIGN/DEFER/DISCARD con motivo, todo commiteado con backup); 20 minutos de mano del Soberano dejan la bandeja al día sin abrir una terminal. | S | **firmada (2026-07-12) vía dashboard** |
| 60 | **Retención de `/mnt/nvme/p0x/.backups/`**: cada acción de la bandeja deja un backup del MD tocado (correcto, pero crece sin límite). Una pasada de limpieza simple (conservar últimos 60 días o N=200) evita que el directorio se vuelva un vertedero invisible. | S | **hecha (2026-07-14): `bin/prune_backups.py` (keep=200/prefijo o <60d, dry-run por defecto) + timer semanal PROPUESTO en `deploy/fragua/` sin habilitar; dry-run hoy = 110 archivos, 0 a borrar (`d986c7b`) — CC** |
| 61 | **`/tareas` y `/verde` en `audit_overlaps.py`** (viewports 768/390): la bandeja de firma se usará desde el móvil del Soberano; hoy solo está auditada en desktop (audit_links 0/0/0). | S | **hecha de facto (verificado 2026-07-14): ambas ya en `audit_overlaps.py` PAGES; overlaps 0 en 768/390/android) — CC** |

### 2026-07-12 · misión LEGIBILIDAD DE FORTALEZAS

| # | Sugerencia | Coste | Estado |
|---|-----------|-------|--------|
| 62 | **OK de David al push público → los badges se encienden**: el repo local lleva CI (`d36a5be`) + ADRs (`9cf98f2`) verificados con AMBOS sweeps a 0; Actions corre en el primer push y los 2 workflows deberían salir verdes a la primera. Verificar badges en GitHub tras el push. | S | **firmada (2026-07-12) vía dashboard** |
| 63 | **Hook pre-push con el sweep COMPLETO en hexelion-public** (materializa #55): el CI público cubre los patrones genéricos; el diccionario completo (literales del rack) debe correr en local antes de cada push. `cp` de un hook de 3 líneas a `.git/hooks/pre-push`. | S | **firmada (2026-07-12) vía dashboard** |
| 64 | **Primer pase de modularización del gateway** siguiendo `docs/PLAN_MODULARIZACION_GATEWAY.md` (hexelion `cddac29`): extraer `routers/tareas.py` verbatim con diff de rutas antes/después + audits 0/0/0. Un router por pase; maritime y websockets los últimos. | M | **firmada (2026-07-12) vía dashboard** |
| 65 | **"ADR al cierre" como paso del rito**: cuando una misión canoniza una decisión mayor, el cierre incluye exportar su ADR saneado a `docs/adr/` del público — la señal de gobernanza se mantiene viva sin misiones especiales. | S | **firmada (2026-07-12) vía dashboard** |
| 66 | **Sección de atestación en el README público**: `/proof` vive en la tailnet — un reclutador no la ve. Screenshot saneado de la vitrina (con la explicación 'What this page proves') + 3 líneas en el README, tras el checklist de secretos. | S | **firmada (2026-07-12) vía dashboard** |

### 2026-07-12 · misión PUERTA VERDE

| # | Sugerencia | Coste | Estado |
|---|-----------|-------|--------|
| 67 | **Flush del think_filter en el chat del Sínodo v2**: MEDIDO en /indoor que `_make_think_filter` retiene ≤7 chars de cola y jamás los suelta — cada respuesta SSE pierde sus últimos caracteres. El fix (`flush=done`) ya existe en el filtro y /indoor lo usa; falta pasarlo en los 2 streams de `sinodo_v2_chat_stream` (2 líneas). | S | **hecha (verificado 2026-07-14): `flush=done` pasado en los 4 sitios de stream (Sínodo v2 ×2 + /api/indoor/chat ×2); test unitario del filtro real prueba que la cola sobrevive ("Bonjour le monde") y el bloque <think> se oculta ("Salut toi!") — CC** |
| 68 | **Adoptar la bandeja de firma explicable (PROPUESTA_27)**: marcadores inline `[prio:] [rev:] [doc:]` en filas NUEVAS de PENDIENTES + titular llano en /tareas (toggle basico/experto). Retrocompatible por construcción (mismo mecanismo que `[aud:]`); el diseño completo con gramática, regex y mock está en `mente/auditorias/PROPUESTA_27_signature_tray_explicable.md`. | S | **firmada (2026-07-12) vía dashboard** |
| 69 | **Captura periódica al conectar la webcam**: cuando exista `/dev/video0`, un timer (tsp o systemd) que llame a `/api/verde/captura` 1-2 veces/día por recipiente — /indoor ya muestra sola la última foto con las medidas encima; sin capturas automáticas la página depende de la mano. | M | **firmada (2026-07-12) vía dashboard** |
| 70 | **Feed vivo desde El Vigía (Opción B del brief de cámara)**: si David prefiere la cámara junto a las plantas en el Pi, hace falta ustreamer/mjpg-streamer + unit en el Vigía + proxy `/api/indoor/feed` en el gateway; el overlay de /indoor ya está listo para recibirlo sin tocar UI. | L | **firmada (2026-07-12) vía dashboard** |
| 71 | **Sesión de tono de la voz de /indoor con David y su esposa**: hoy responde el fallback 1.5b (honesto pero algo torpe: "llamar al jardinería"); la torre no carga el modelo (CUDA alloc, residencia pendiente de instalar). Probar 5-6 preguntas reales juntos y ajustar `_INDOOR_VOZ` + few-shots con sus palabras. | S | **firmada (2026-07-12) vía dashboard** |

### 2026-07-12 · misión HARDWARE VIVO + JARDIN

| # | Sugerencia | Coste | Estado |
|---|-----------|-------|--------|
| 72 | **Parada limpia del gateway con el relay MJPEG**: MEDIDO que el stop tardó 90s y acabó en SIGKILL (los streams vivos de /api/indoor/feed bloquean el shutdown de uvicorn). Añadir `TimeoutStopSec=15` a la unit o `--timeout-graceful-shutdown 10` a uvicorn. [prio:media] [rev:sí] | S | **hecha (verificado 2026-07-14): unit con `TimeoutStopSec=15` + `--timeout-graceful-shutdown 10` (backup .bak en /etc/systemd); stop cronometrado CON cliente MJPEG vivo = 10.24s "Deactivated successfully", sin SIGKILL ni 90s — CC** |
| 73 | **Encuadre y aviso de la cámara**: en el primer snapshot sales tú en el plano — la cámara ve la silla, no solo las plantas. Decisión física tuya (girarla/acercarla a las cúpulas) + una línea de aviso en /indoor "la cámara ve el rincón, no solo las plantas". Todo sigue 100% local. [prio:alta] [rev:sí] | S | **firmada (2026-07-12) vía dashboard** |
| 74 | **Jardin Fase 1 — La Sentinelle**: siguiente sesión del roadmap (SensorSource+sim con jitter, Le Filtre con histéresis/cooldowns/horas silenciosas, Journal, Fenêtre con scanlines, Fantôme 4 estados). La Fenêtre puede nacer ya conectada al feed real del Vigía. [prio:media] [rev:sí] [doc:mente/manual/unidades.md] | M | **firmada (2026-07-12) vía dashboard** |
| 75 | **Broker MQTT + flasheo de los ESP32 del jardín**: están colocados pero el rack aún no los ve (mosquitto inactivo en el Vigía, sin serie nuevo). Cuando decidas firmware (Arduino vs ESPHome — decisión 5 del roadmap), habilitar mosquitto con listener WS :9001 y flashear; la arquitectura del Jardin los espera en Fase 4. [prio:media] [rev:sí] | M | **firmada (2026-07-12) vía dashboard** |

### 2026-07-12 · misión LE JARDIN DES OMBRES — DASHBOARD PROPIO

| # | Sugerencia | Coste | Estado |
|---|-----------|-------|--------|
| 76 | **Validar el francés con Krista**: todas las líneas nuevas de copy.fr.ts + los textos del componente cámara los escribí yo — el canon del Jardin exige que el Soberano valide cada línea antes de darlas por buenas. Una lectura de 10 minutos juntos. [prio:alta] [rev:sí] | S | **firmada (2026-07-13) vía dashboard** |
| 77 | **Soltar los .md de herbología en `verde/herbier/`**: NO están en el rack (buscados en mente/, esferas, ~/P0X). La enciclopedia ya los espera — al copiarlos aparecen solos en "Pages apportées par le jardinier", sin reiniciar nada. [prio:alta] [rev:sí] | S | **firmada (2026-07-13) vía dashboard** |
| 78 | **La voz cita el herbier**: cuando existan los .md (#77), añadir sus extractos top-k al grounding de `/api/indoor/chat` idioma:fr para que La Voix responda CITANDO las páginas del jardinero — mismo patrón retrieval del Sínodo, a escala mini. [prio:media] [rev:sí] | M | **firmada (2026-07-13) vía dashboard** |
| 79 | **Bautizar al monigote y al jardín**: el guardián perro-hueso necesita nombre (propuesta canon: Churro) y "Le Jardin des Ombres" sigue siendo nombre en clave — decisión de Krista; se cambia en copy.fr.ts + CLAUDE.md, un solo sitio. [prio:baja] [rev:sí] | S | **descartada (2026-07-13): se llamará Cortext(el perro) y el jardin igual,"Le Jardin" — vía dashboard** |
| 80 | **Kiosco para Krista**: cuando la Pantalla Soberana esté viva, `chromium --kiosk http://<fragua>:8001/jardin/` convierte el Jardin en el marco permanente de la cocina/salón — cero fricción para una persona no técnica. [prio:media] [rev:sí] | S | **descartada (2026-07-13): no — vía dashboard** |

### 2026-07-13 · misión INVENTARIO TOTAL (widgets + métricas + tareas abiertas)

| # | Sugerencia | Coste | Estado |
|---|-----------|-------|--------|
| 81 | **Reconciliación de estados de esta tabla**: hay firmadas que ya están hechas de facto (#70 feed vivo = ustreamer del Vigía; #8 borrada) — una pasada anotando "hecha (evidencia)" donde corresponda, para que el contador del SYSTEM STATE cuente backlog REAL y no ruido. [prio:media] [rev:sí] [doc:mente/auditorias/TAREAS_ABIERTAS_2026-07-13.md] | S | **aprobada (2026-07-19) — vía relevo del Preceptor, misión LAS DOS PIELES: «acepto todas» del Soberano registrado** |
| 82 | **Unificar #55 y #63**: son el mismo trabajo (hook pre-push con barrido de secretos en hexelion-public) escrito dos veces; fundirlas en una y cerrarla de una vez desbloquea el prerequisito técnico de #62. [prio:media] [rev:sí] | S | **aprobada (2026-07-19) — vía relevo del Preceptor, misión LAS DOS PIELES: «acepto todas» del Soberano registrado** |
| 83 | **Investigar el eje z del ADXL345 clavado en −2.048 g**: es exactamente el tope de rango — o la escala (±2g vs ±16g) o la orientación están mal, y el reflejo-vibracion está midiendo sobre un sensor saturado. Verificar registro de config en el firmware M5. [prio:alta] [rev:sí] | S | **aprobada (2026-07-19) — vía relevo del Preceptor, misión LAS DOS PIELES: «acepto todas» del Soberano registrado** |
| 84 | **Paso 0 de la modularización (#64): sacar los ~30 `hexelion_gateway.py.bak*` del working tree** (a `.backups/` fuera del repo, tras verificar que el actual funciona) — el monolito se audita mejor sin 30 fantasmas al lado. [prio:media] [rev:sí] | S | **aprobada (2026-07-19) — vía relevo del Preceptor, misión LAS DOS PIELES: «acepto todas» del Soberano registrado** |
| 85 | **Badge de frescura uniforme en el rediseño**: casi todos los endpoints ya devuelven `ts`/`fuente` — el rediseño en Claude Design puede pintar "edad del dato" en cada widget con una sola convención, y lo congelado (asesoría 20 días) se delataría solo, sin auditorías. [prio:media] [rev:sí] [doc:mente/auditorias/INVENTARIO_WIDGETS_2026-07-13.md] | M | aplazada (2026-07-13) vía dashboard |

### 2026-07-14 · misión CIERRE JARDÍN + TAREAS TÉCNICAS

| # | Sugerencia | Coste | Estado |
|---|-----------|-------|--------|
| 86 | **Puente `pageDemandee` en `store.ts` para el nuevo Livre**: hoy Docteur/Trivial NO enlazan al Grimoire (verificado: solo desbloquean vía `debloquer`), así que el principio #2 del CLAUDE.md del Jardin ("todo juego termina en un enlace a la página con la respuesta resaltada") sigue sin cablear. Cuando se cablee, el Livre necesita saltar a la página pedida — un `pageDemandee` en el store lo resuelve sin tocar el libro. [prio:baja] [rev:sí] | S | **aprobada (2026-07-19) — vía relevo del Preceptor, misión LAS DOS PIELES: «acepto todas» del Soberano registrado** |
| 87 | **Proxy de dev en `vite.config.ts` (`/api` y `/assets` → `:8001`)**: hoy `npm run dev` da 404 en cámara, sensores y assets compartidos — solo funciona el flujo `build`+gateway. Un proxy de 6 líneas hace `dev` usable para iterar el Jardin en caliente. [prio:media] [rev:sí] | S | **aprobada (2026-07-19) — vía relevo del Preceptor, misión LAS DOS PIELES: «acepto todas» del Soberano registrado** |
| 88 | **`cortex.svg` del header con las 4 variantes de estado**: la puerta de David→Jardín muestra hoy la pose `heureux` estática (SVG plano duplicado de `CortexSVG.tsx`). Si se quiere que el icono del dashboard refleje el estado REAL de las plantas como lo hace Cortex dentro del Jardin, exportar las 4 poses + un fetch ligero a `/api/indoor/estado` en el header. [prio:baja] [rev:sí] | M | **aprobada (2026-07-19) — vía relevo del Preceptor, misión LAS DOS PIELES: «acepto todas» del Soberano registrado** |
| 89 | **Espejar la unit viva del gateway en `deploy/fragua/`**: `hexelion-gateway.service` (ya con `TimeoutStopSec=15` + graceful-shutdown, #72) vive solo en `/etc/systemd` con un `.bak`; todos los demás nodos tienen su unit registrada en `deploy/`. Copiar la unit al repo da trazabilidad y facilita el redeploy tras un reflash. [prio:baja] [rev:sí] | S | **aprobada (2026-07-19) — vía relevo del Preceptor, misión LAS DOS PIELES: «acepto todas» del Soberano registrado** |

### 2026-07-18 · misión G0 · EL CUERPO DEL SOBERANO

| # | Sugerencia | Coste | Estado |
|---|---|---|---|
| 90 | **Activar `OLLAMA_IGPU_ENABLE=1` en el servicio `ollama` de soberano**: MEDIDO por bench (`deploy/soberano/BENCH_G0.md`) que Vulkan sobre el Radeon 780M da 3.58× en pp512 y 3.28× en tg128 frente a CPU. Ollama ya detecta el dispositivo pero lo descarta explícitamente sin ese flag. Necesita sudo (`systemctl edit ollama` + `daemon-reload` + `restart`) — bloqueado en esta misión por falta de contraseña interactiva. Comandos exactos ya documentados. [prio:alta] [rev:sí] | S | **aprobada (2026-07-19) — vía relevo del Preceptor, misión LAS DOS PIELES: «acepto todas» del Soberano registrado** |
| 91 | **Redactar el contrato de datos de OpenWebUI antes de dar la primera cuenta a un hermano**: la ventana (`deploy/soberano/open-webui.service`) ya está viva y verificada solo-tailnet, pero qué pueden ver/hacer los hermanos, retención de conversaciones, etc. no existe todavía como documento — hueco real señalado también en el Manual del Soberano §4. [prio:alta] [rev:sí] [doc:mente/manual/MANUAL_DEL_SOBERANO_P0X.md] | S | **aprobada (2026-07-19) — vía relevo del Preceptor, misión LAS DOS PIELES: «acepto todas» del Soberano registrado** |
| 92 | **Revisar permisos del home del servicio `ollama` en soberano**: `/usr/share/ollama/.ollama` es `700` y bloquea incluso a usuarios del grupo `ollama` (como `pisky`) leer los blobs directamente. Si alguna misión futura necesita inspección directa de pesos (export, checksum, bench sin re-descargar de HF), un `750` con el grupo correcto lo resuelve — hoy obligó a descargar un GGUF standalone duplicado (18GB) solo para el Bloque D. Necesita sudo. [prio:media] [rev:sí] [doc:deploy/soberano/MOTOR_LOCAL.md] | S | **aprobada (2026-07-19) — vía relevo del Preceptor, misión LAS DOS PIELES: «acepto todas» del Soberano registrado** |
| 93 | **`MAPA_EVOLUTIVO_P0X.md` sigue sin existir en ningún repo del rack**: la Misión G0 lo esperaba como referencia estratégica de entrada (Bloque A) pero no llegó ni se encontró en `p0x` ni `hexelion`. Sin él, `soberano` operó toda la misión solo con la doctrina existente — funcionó, pero la referencia evolutiva declarada en el brief de la misión sigue pendiente de que David la entregue y la canonice. [prio:alta] [rev:sí] | S | **aprobada (2026-07-19) — vía relevo del Preceptor, misión LAS DOS PIELES: «acepto todas» del Soberano registrado** |
| 94 | **Decidir el script de instalación de `@qwen-code/audio-capture`**: `npm install -g @qwen-code/qwen-code` dejó ese paquete sin su install script aprobado (bloqueo de seguridad de `allow-scripts`, deliberado). Si la Misión G1 quiere evaluar la función de voz de Qwen Code, hay que revisar el script (`npm approve-scripts`) antes; si no interesa, dejarlo así es la postura correcta y no requiere acción. [prio:baja] [rev:sí] [doc:deploy/soberano/HARNESS_G0.md] | S | **aprobada (2026-07-19) — vía relevo del Preceptor, misión LAS DOS PIELES: «acepto todas» del Soberano registrado** |
| 95 | **Nodo `soberano` sin fila en `ORQUESTA_MODELOS_P0X.md`**: la doctrina (§4 de esa misma doctrina) dice que "un cerebro sin fila en la Orquesta no opera en P0X" — `soberano` ya opera (motor local, OpenWebUI, tres harnesses) pero la tabla §1 del MD de doctrina todavía no tiene su fila. Es clase=doctrina: el silicio propone, el carbono canoniza — dejo la propuesta de fila lista para que la revises, no la escribo yo directamente en el MD. [prio:media] [rev:sí] [doc:mente/doctrina/ORQUESTA_MODELOS_P0X.md] | S | **aprobada (2026-07-19) — vía relevo del Preceptor, misión LAS DOS PIELES: «acepto todas» del Soberano registrado** |

### 2026-07-18 · misión G1 · LOS OJOS DEL SOBERANO — auditoría Bloque B

| # | Sugerencia | Coste | Estado |
|---|---|---|---|
| 96 | **[aud:hexelion-main-stale] `main` de `hexelion.git` está 54 commits por detrás desde 2026-06-21** — todo el desarrollo real desde entonces vive en `nexo-carbono-dashboard-20260623` (con tag `dashboard-estable-20260711`), incluidos los fixes de #22, #61, #67 que la tabla ya daba por `hecha`. Verificar contra `main` da falsos negativos (código "inexistente" que en realidad está desplegado). Propuesta: fusionar `nexo-carbono-dashboard-20260623` a `main` y retaguear, o renombrar cuál es la rama canónica para que quien clone no tenga que descubrirlo por auditoría. [prio:alta] [rev:sí] [doc:deploy/soberano/AUDITORIA_G1.md] | S | **aprobada (2026-07-19) — vía relevo del Preceptor, misión LAS DOS PIELES: «acepto todas» del Soberano registrado** |
| 97 | **[aud:gateway-unit-not-versioned] La unit systemd del gateway de hexelion no está versionada en ninguna rama del repo** (reitera la SUGERENCIA #89 de G0 con evidencia nueva): #72 (`TimeoutStopSec=15`) es real según PENDIENTES pero no verificable desde git — solo vive en `/etc/systemd/system` de la-fragua. Copiar la unit viva a `deploy/fragua/` cierra el hueco de trazabilidad. [prio:media] [rev:sí] [doc:deploy/soberano/AUDITORIA_G1.md] | S | **aprobada (2026-07-19) — vía relevo del Preceptor, misión LAS DOS PIELES: «acepto todas» del Soberano registrado** |
| 98 | **[aud:delta-truncated-ref] Referencia rota `instrucciones-p0` (falta la "x") en el delta aceptado `cU6TFqoyHh8-20260714202112`**: el clasificador del pipeline de Observar cortó la generación a mitad de token en la última línea de "Conexiones propuestas", y esa arista rota ya entró al grafo aceptado. Inofensivo hoy (un humano lo entiende), pero si el corte ocurre en un ID más ambiguo podría crear una arista fantasma silenciosa. Añadir validación post-generación (regex de IDs válidos contra el léxico real) antes de aceptar una CONEXIÓN evitaría que se repita. [prio:baja] [rev:sí] [doc:deploy/soberano/AUDITORIA_G1.md] | S | **aprobada (2026-07-19) — vía relevo del Preceptor, misión LAS DOS PIELES: «acepto todas» del Soberano registrado** |
| 99 | **Desplegar `PROPUESTA_28_observar_fuentes_web.patch`**: `/api/observar/ingest` solo resuelve URLs de vídeo (`resolve_video_id` es YouTube-only, verificado en vivo: 422 "no se pudo resolver el video_id" con una URL de docs de Bambu Lab). El patch es aditivo, `git apply --check` OK, cero cambios al camino YouTube — añade un fallback que solo activa si ya hay un transcript pre-cacheado en `corpus/web-<hash>/`. Sin desplegarlo, cualquier scraper externo (como el de esta misión) queda fuera del lazo Observar automático. Requiere `git apply` + reinicio del gateway en fragua. [prio:alta] [rev:sí] [doc:mente/auditorias/PROPUESTA_28_observar_fuentes_web.patch] | S | **aprobada (2026-07-19) — vía relevo del Preceptor, misión LAS DOS PIELES: «acepto todas» del Soberano registrado** |

### 2026-07-18 · misión G1 · LOS OJOS DEL SOBERANO — cierre

| # | Sugerencia | Coste | Estado |
|---|---|---|---|
| 100 | **Activar `OLLAMA_IGPU_ENABLE=1` (reitera #90 de G0, con evidencia nueva)**: el duelo de harness completo del Bloque A corrió en CPU — Qwen Code no completó ninguna misión en 500s y OpenCode tardó 150-500s por misión; con el 3.28-3.58× medido en el bench, varias de esas misiones probablemente habrían completado a tiempo en Vulkan. Bloquea la lectura real de "qué tan lento es cada harness" hasta que se active. [prio:alta] [rev:sí] [doc:mente/reportes/G1_soberano_2026-07-18.md] | S | **hecha (2026-07-19): David aplicó `sudo systemctl edit ollama` con `Environment="OLLAMA_IGPU_ENABLE=1"` + `daemon-reload` + `restart`. Verificado por CC: `ollama ps` → `100% GPU`. Confirmó la ganancia real en EVAL_GROUNDING_G2 (7-107s por prueba vs 150-500s en CPU durante G1) — David** |
| 101 | **Re-evaluar Qwen Code con `-y` + Vulkan activo antes de descartarlo definitivamente**: en este duelo no completó ninguna de las 5 misiones (con o sin `-y`), pero corrió entero bajo CPU y sin el flag documentado hasta que el propio error lo reveló. No hay dato limpio todavía de si el problema es de diseño o de las condiciones de esta misión. [prio:media] [rev:sí] [doc:mente/reportes/G1_soberano_2026-07-18.md] | S | **aprobada (2026-07-19) — vía relevo del Preceptor, misión LAS DOS PIELES: «acepto todas» del Soberano registrado** |
| 102 | **Doble verificación obligatoria antes de que un harness delegado dé una búsqueda "negativa" por definitiva**: OpenCode concluyó "No configuration files with num_ctx found" en M5 tras buscar solo por patrón de nombre de archivo, cuando existían 2 valores reales localizables con un grep de contenido. No fue alucinación (no inventó datos) pero sí una conclusión insuficientemente verificada presentada con seguridad — el mismo vector que el grounding de la Doctrina AI Interna §2 ya nombra para voces pequeñas, aplicado ahora a un harness agéntico. [prio:media] [rev:sí] [doc:mente/reportes/G1_soberano_2026-07-18.md] | M | **aprobada (2026-07-19) — vía relevo del Preceptor, misión LAS DOS PIELES: «acepto todas» del Soberano registrado** |
| 103 | **Canonizar la fila de `soberano-coder` en `ORQUESTA_MODELOS_P0X.md` (reitera #95)**: seguía sin canonizar al verificar de nuevo al cierre de G1, pese a que el brief de esta misión asumía que ya estaría hecho. El texto propuesto sigue disponible en el reporte de G0. [prio:alta] [rev:sí] [doc:mente/reportes/G0_soberano_2026-07-18.md] | S | **aprobada-pendiente-carbono (2026-07-19): David intentó `git apply` + commit ("canon(orquesta): v1.1.0", `f7ceea6`), pero el apply falló silenciosamente ("corrupt patch") — verificado por CC que `ORQUESTA_MODELOS_P0X.md` NO cambió (sigue `version: 1.0.0`, sin fila). Causa raíz corregida por CC (`15ffc7c`, faltaba una línea de contexto en blanco en el patch) y re-verificado `git apply --check` OK. Sigue esperando que David reintente `git apply` + commit — vía relevo del Preceptor** |

### 2026-07-19 · EVAL_GROUNDING_G2 (puerta G1→G2 del harness)

| # | Sugerencia | Coste | Estado |
|---|---|---|---|
| 104 | **Investigar `AI_APICallError: connection refused` entre invocaciones secuenciales de OpenCode**: causó 2/10 fallos por interrupción a medio flujo (T2, T5 de `EVAL_GROUNDING_G2`), justo en el borde temporal entre una prueba y la siguiente. Hipótesis: transición de Ollama (`OLLAMA_NUM_PARALLEL=1`) al recibir una nueva conexión inmediatamente tras la anterior. Antes de reintentar la eval: añadir pausa de 5-10s entre invocaciones y/o revisar `OLLAMA_KEEP_ALIVE`. [prio:alta] [rev:sí] [doc:mente/reportes/EVAL_GROUNDING_G2_2026-07-19.md] | S | **aprobada (2026-07-19): corrección aplicada en G1-R Bloque B — vía relevo del Preceptor** |
| 105 | **Reforzar el patrón #102 por tarea, no solo vía `AGENTS.md` global**: funcionó limpio en T8 pero T1 y T9 usaron un solo método sin ningún segundo intento pese a la regla global cargada (confirmado que `~/.config/opencode/AGENTS.md` sí se lee). La regla se ignora a veces bajo presión de tarea — reforzarla en el prompt mismo de tareas que pidan negativas o estados binarios. [prio:media] [rev:sí] [doc:mente/reportes/EVAL_GROUNDING_G2_2026-07-19.md] | S | **aprobada (2026-07-19): corrección aplicada en G1-R Bloque B — vía relevo del Preceptor** |
| 106 | **Patrón de imprecisión numérica recurrente en OpenCode (visto en G1-M3 y ahora en T3/T4)**: deriva multiplicadores de campos secundarios (duraciones) en vez de usar directamente campos ya calculados, y no reconcilia cifras entre respuestas relacionadas (3.28x en T3 vs 3.235 en T4, mismo dato). Instrucción explícita de "usa el campo tal cual" cuando la tarea lo amerite, antes de un reintento. [prio:media] [rev:sí] [doc:mente/reportes/EVAL_GROUNDING_G2_2026-07-19.md] | S | **aprobada (2026-07-19): corrección aplicada en G1-R Bloque B — vía relevo del Preceptor** |
| 107 | **`EVAL_GROUNDING_G2`: 3/10, no aprueba — OpenCode sigue en G1**: causas raíz en #104-106. Reintento pendiente de aplicar esas correcciones y de decisión de David sobre el matiz de T7 (credencial disponible pero no insinuada en el prompt). [prio:alta] [rev:sí] [doc:mente/reportes/EVAL_GROUNDING_G2_2026-07-19.md] | S | **aprobada (2026-07-19): re-test en G1-R Bloque C con regla de decisión pre-registrada — vía relevo del Preceptor** |

### 2026-07-19 · micro-misión EL YACIMIENTO

| # | Sugerencia | Coste | Estado |
|---|---|---|---|
| 108 | **Investigar el push perdido más "caliente": `handoff/jardin.html` y `handoff/hexelion.html` de `P0X_ Dashboard soberano local-first.zip` (14-jul, 5 días antes de esta misión)**: es el artefacto de dashboard más reciente de todo `pre-bee/p0x/`, con un `GUIDE.md` que describe exactamente "Le Jardin des Ombres" y "El Watchman" — muy probablemente el antecedente directo del dashboard/Jardin vivo. Comparar línea a línea contra `hexelion/dashboard.html` actual antes de que la memoria de qué cambió se enfríe más. [prio:alta] [rev:sí] [doc:mente/deliberacion/INDICE_ARCHIVO_HISTORICO.md] | S | **aprobada (2026-07-19): investigado en G1-R Bloque E — vía relevo del Preceptor** |
| 109 | **Reparar (o descartar formalmente) los 2 ZIPs truncados de tamaño real: `Nexo/nexo.zip` (4.7MB) y `Nexo/files.zip` (3.9MB)**: cabecera válida, empiezan con `nexo-final.html` legible, pero falta el directorio central. Una herramienta de reparación de zip (`zip -FF`, o extraer por streaming con `python zipfile` en modo tolerante) podría rescatar contenido que hoy es inaccesible — candidato a contener el tronco "Nexo" completo con sus assets. [prio:media] [rev:sí] [doc:mente/deliberacion/INDICE_ARCHIVO_HISTORICO.md] | M | **aprobada (2026-07-19), pendiente de ejecución técnica — vía relevo del Preceptor** |
| 110 | **Decidir destino del bloque de ~90 documentos misceláneos de `pre-bee/p0x/MD 3/`** (visiones, dictámenes, briefings, lore) — ninguno es canon hoy, pero algunos (linaje del Códice Maestro 8→12→14→15, decisiones de arquitectura como litellm-vs-Ollama en `p0x2.zip`) podrían ser casos de estudio útiles para `PROCESO_EVALES_TRANSPLANTE_P0X.md` si el carbono los revisa y decide destilar algo — uno por uno, con ACCEPT explícito, nunca en lote. [prio:baja] [rev:sí] [doc:mente/deliberacion/INDICE_ARCHIVO_HISTORICO.md] | S | **aprobada-pendiente-carbono (2026-07-19): requiere revisión de David uno por uno antes de destilar nada — vía relevo del Preceptor** |
| 111 | **Purgar o archivar aparte `gaganode_pro-0_0_600.tar.gz` (5.4MB) y `._gaganode-windows-amd64`**: no tienen relación aparente con P0X en el resto del yacimiento (nombre sugiere otro proyecto, "GagaNode") — probablemente terminaron ahí por error de arrastre al copiar. Verificar con David antes de tocar nada (invariante de solo-lectura de esta misión sigue vigente). [prio:baja] [rev:sí] [doc:mente/deliberacion/INDICE_ARCHIVO_HISTORICO.md] | S | **aprobada-pendiente-carbono (2026-07-19): requiere confirmación de David antes de tocar nada (invariante de solo-lectura) — vía relevo del Preceptor** |

### 2026-07-19 · misión G1-R · LA SEGUNDA MIRADA (Y LA VOZ ÚNICA)

| # | Sugerencia | Coste | Estado |
|---|---|---|---|
| 112 | **Investigar por qué OpenCode a veces no da respuesta final tras usar herramientas** (T5 en ambas evals de grounding, y T2 de la eval original): patrón recurrente distinto de "connection refused" — corta tras una secuencia de tool calls sin sintetizar la respuesta de texto. [prio:alta] [rev:sí] [doc:mente/reportes/G1R_soberano_2026-07-19.md] | S | **aprobada (2026-07-19) — vía relevo del Preceptor, misión LAS DOS PIELES: «acepto todas» del Soberano registrado** |
| 113 | **Añadir verificación cruzada de hardware antes de nombrar un backend**: en el re-test, OpenCode identificó correctamente "100% GPU" pero inventó "CUDA/NVIDIA" (es Vulkan/AMD Radeon 780M) sin verificar con una segunda fuente (`lspci`, `journalctl`). Alucinación real, no solo imprecisión numérica. [prio:media] [rev:sí] [doc:mente/reportes/G1R_soberano_2026-07-19.md] | S | **aprobada (2026-07-19) — vía relevo del Preceptor, misión LAS DOS PIELES: «acepto todas» del Soberano registrado** |
| 114 | **Decidir la puerta post-5/10**: la regla de decisión pre-registrada de G1-R cubre "OpenCode aprueba" y "recaída → prueba Aider", pero no qué hacer cuando **ninguno de los dos** aprueba limpio (Aider: excelente en Q&A con `--read`+`--chat-mode ask`, pero sin capacidad de exploración/verificación de estado en vivo). Falta esa regla antes de la próxima eval. [prio:alta] [rev:sí] [doc:mente/reportes/G1R_soberano_2026-07-19.md] | S | **aprobada (2026-07-19) — vía relevo del Preceptor, misión LAS DOS PIELES: «acepto todas» del Soberano registrado** |
| 115 | **Versionar el código fuente real del dashboard/Jardin de producción**: verificado que `dashboard/` en git solo tiene caché de Vite, no código fuente — el Jardin que corre hoy (herbier, arcade, sentinelle, capturas `jardin-v2-*.png`) no tiene respaldo en git. Riesgo real de repetir la pérdida de `6a4bb3f`. [prio:alta] [rev:sí] [doc:deploy/soberano/LINAJE_G1R_BLOQUE_E.md] | M | **aprobada (2026-07-19) — vía relevo del Preceptor, misión LAS DOS PIELES: «acepto todas» del Soberano registrado** |

### 2026-07-19 · misión LAS DOS PIELES — PREVIO · LA BANDEJA (cartas mano-david, firma del carbono requerida)

| # | Sugerencia | Coste | Estado |
|---|---|---|---|
| 116 | **[mano-david] CANON-A · canoniza la definición de producto** — WHY: P0X = bootcamp de soberanía · Hexelion = Nivel 5; debe ser canon ANTES de cualquier apertura a terceros para que no se diluya por presión de un usuario entusiasta. ORIGIN: relevo del Preceptor → DEST: `mente/doctrina/DOCTRINA_P0X_PRODUCTO.md`. COMMANDS: `cd ~/p0x && git add mente/doctrina/DOCTRINA_P0X_PRODUCTO.md && git commit -m "canon(producto): ascienden CANON-A/B/C — commit del Soberano"` (la firma de esta carta canoniza también B y C: un solo archivo, un solo commit — declarado). VERIFY: `grep -n "CANON-A · DEFINICIÓN CANÓNICA" mente/doctrina/DOCTRINA_P0X_PRODUCTO.md && git log --oneline -1 -- mente/doctrina/DOCTRINA_P0X_PRODUCTO.md` EXPECT ▸ el grep imprime la línea del bloque y el log imprime el hash del commit del Soberano (hoy imprime vacío). [prio:alta] [doc:mente/doctrina/DOCTRINA_P0X_PRODUCTO.md] | S | **NULA** (2026-07-20, misión Reparación §4): el bloque CANON-A ya vive en el MD **commiteado** (`e018b01`); el ascenso ceremonial a canon nunca se materializó como commit separado → deuda de sesión, no bloqueo. Reabrir solo si el Soberano quiere el commit de ascenso. |
| 117 | **[mano-david] CANON-B · canoniza el VETO de OSINT sobre terceros** — WHY: fuera del producto todo OSINT sobre terceros; sobrevive solo el OSINT interno con permiso explícito. Cierra la puerta antes de abrirla a la comunidad. ORIGIN: relevo del Preceptor → DEST: mismo MD. COMMANDS: firma compartida con la carta #116 (mismo archivo, mismo commit). VERIFY: `grep -n "CANON-B · VETO: OSINT" mente/doctrina/DOCTRINA_P0X_PRODUCTO.md` EXPECT ▸ imprime la línea del bloque en el MD ya commiteado. [prio:alta] [doc:mente/doctrina/DOCTRINA_P0X_PRODUCTO.md] | S | **NULA** (2026-07-20, §4): CANON-B vive en el MD commiteado (`e018b01`); mismo caso que #116 — ascenso ceremonial no materializado, no bloqueo. |
| 118 | **[mano-david] CANON-C · canoniza el VETO de peaq/DePIN con reparto automático** — WHY: diferido al horizonte; si algún día entra, keyless + firma del carbono en cada acto de valor. Coherente con «jamás firmas valor». ORIGIN: relevo del Preceptor → DEST: mismo MD. COMMANDS: firma compartida con la carta #116 (mismo archivo, mismo commit). VERIFY: `grep -n "CANON-C · VETO: peaq" mente/doctrina/DOCTRINA_P0X_PRODUCTO.md` EXPECT ▸ imprime la línea del bloque en el MD ya commiteado. [prio:alta] [doc:mente/doctrina/DOCTRINA_P0X_PRODUCTO.md] | S | **NULA** (2026-07-20, §4): CANON-C vive en el MD commiteado (`e018b01`); mismo caso que #116 — ascenso ceremonial no materializado, no bloqueo. |
| 119 | **[mano-david] Re-entrega: commit de canonización del BLUEPRINT v1.2** — WHY: verificado hoy que el commit NO aterrizó: `mente/doctrina/BLUEPRINT_DISENO_SOBERANO.md` sigue **untracked** (`git status` → `??`); su front-matter dice «canon con el commit del Soberano». No bloquea la Fase 0, pero la construcción entera cuelga de él como única verdad visual. ORIGIN: re-entrega CC → DEST: repo `p0x` en soberano. COMMANDS: `cd ~/p0x && git add mente/doctrina/BLUEPRINT_DISENO_SOBERANO.md && git commit -m "canon(blueprint): v1.2.0 BLUEPRINT_DISENO_SOBERANO — commit del Soberano"` VERIFY: `git log --oneline -1 -- mente/doctrina/BLUEPRINT_DISENO_SOBERANO.md` EXPECT ▸ imprime un hash (hoy imprime vacío). [prio:alta] | S | **HECHA** (2026-07-20): el carbono canonizó el BLUEPRINT v1.2 en `ecfd7f6` (autor `soberano@p0x.local`, corrupción SSH limpiada), materializado en **la raíz del repo** (`BLUEPRINT_DISENO_SOBERANO.md`), no en `mente/doctrina/`. Ver nota de ubicación en el reporte de esta misión. |
| 120 | **[mano-david] Re-entrega: PROPUESTA_29 — fila de `soberano-coder` en la Orquesta (cierra #95 #103)** — WHY: un cerebro sin fila no opera (§4 Orquesta); verificado hoy que sigue sin aplicar: `git apply --check` pasa limpio y `grep soberano-coder` en el MD da cero. El intento `f7ceea6` falló en silencio («corrupt patch»); la causa raíz ya está reparada (`15ffc7c`) y re-verificada. Esta carta es además el **fixture permanente del carril interno de la Bandeja (Fase 3)**. ORIGIN: re-entrega CC → DEST: repo `p0x` en soberano. COMMANDS: `cd ~/p0x && git apply mente/auditorias/PROPUESTA_29_orquesta_soberano.patch && git add mente/doctrina/ORQUESTA_MODELOS_P0X.md && git commit -m "canon(orquesta): v1.1.0 alta soberano-coder — cierra #95 #103 (reintento, patch reparado)"` VERIFY: `grep -c "soberano-coder" mente/doctrina/ORQUESTA_MODELOS_P0X.md && grep -n "version: 1.1.0" mente/doctrina/ORQUESTA_MODELOS_P0X.md` EXPECT ▸ conteo ≥ 1 y la línea `version: 1.1.0` (hoy: 0 y `version: 1.0.0`). [prio:alta] [doc:mente/auditorias/PROPUESTA_29_orquesta_soberano.patch] | S | **LISTA PARA TU FIRMA** (2026-07-20, §4): la fila `soberano-coder` + changelog v1.1.0 quedan **escritos como edición directa** en `mente/doctrina/ORQUESTA_MODELOS_P0X.md` (sin commitear, para tu commit). Se evitó el patch por la cicatriz del corrupt-patch. NOTA HONESTA: la fila dice «backend Vulkan»; el drop-in `OLLAMA_IGPU_ENABLE=1` ya está **activo** (antes vacío), pero confirma `PROCESSOR=GPU` cargando un modelo antes de canonizar el texto como literal. |
| 121 | **[mano-david] Rescate as-built COMPLETO desde la-fragua (Fase 0, LAS DOS PIELES)** — WHY: SSH de soberano a fragua denegado (verificado: `Permission denied` para `davidpecero@` y `pisky@`); CC ya rescató por HTTP lo *servido* (Nexo v9 + dist del Jardin), pero el **fuente** del Jardin (`/home/ubuntu/jardin-des-ombres/`, src + configs, sin respaldo en git según #115) y la unit del gateway (#89/#97) solo salen con tu mano. ORIGIN: CC → DEST: `soberano:/home/pisky/rescate/`. COMMANDS (en la-fragua, usuario ubuntu): `sudo cp /etc/systemd/system/hexelion-gateway.service /tmp/ && tar czf /tmp/as-built-fuente-2026-07-19.tgz --exclude='node_modules' --exclude='dist/.vite' -C /home/ubuntu jardin-des-ombres hexelion/dashboard-v9 hexelion/assets hexelion/hexelion_gateway.py hexelion/observar_api.py hexelion/start_gateway.sh -C /tmp hexelion-gateway.service && (cd /tmp && python3 -m http.server 8899 --bind 100.82.94.83)` — avisa a CC en el chat y CC lo baja con curl y para tú el server con Ctrl-C (alternativa: `scp /tmp/as-built-fuente-2026-07-19.tgz pisky@100.81.82.34:~/rescate/`). VERIFY: `sha256sum /tmp/as-built-fuente-2026-07-19.tgz` EXPECT ▸ CC confirma el mismo hash tras recibirlo y lo commitea en `hexelion/dashboard/as-built-2026-07-19/` con procedencia. [prio:alta] [doc:mente/feedback/PENDIENTES.md#115] | S | **SUPERADA — pendiente de tu veredicto** (2026-07-20, §4): el fuente del Jardin que pedía rescatar de fragua fue **reconstruido** en `~/hexelion/dashboard/src/{jardin,nexo,shared}` (en git) durante DOS PIELES, y `hexelion/dashboard/as-built-2026-07-19/` ya existe; el rescate HTTP parcial vive en `hexelion@0a5c6ca`. El fuente crudo de fragua ya no es carga soportante. Declárala nula, o dime si aún quieres el crudo original de `/home/ubuntu/jardin-des-ombres/` como respaldo arqueológico. |

### 2026-07-19 · misión LAS DOS PIELES — CIERRE (fases 0–5 completas, 172/172)

Numeración: salta a #134 — #122–#133 pertenecen a la serie de hallazgos del brief de esta misión
(p.ej. #133 broker MQTT inexistente, referenciado en `Sentinelle.tsx`) y no tienen fila propia aquí.

| # | Sugerencia | Coste | Estado |
|---|---|---|---|
| 134 | **Endpoint real del carril comunidad de la Bandeja Ejecutiva**: el carril cuarentena (Fase 3) rinde hoy fixture declarado — falta el endpoint del gateway que sirva propuestas de la comunidad con su estado de higiene, para que la Bandeja viva de dato real en ambos carriles. [prio:media] [doc:mente/reportes/DOS_PIELES_soberano_2026-07-19.md] | M | pendiente |
| 135 | **Mémoire V1 → mini-cerebro real**: hoy teje términos compartidos entre notas del Cahier en cliente; el salto es alimentar el grafo `second_brain.json` del rack con las notas de Krista (pipeline de ingesta ya existente para `mente/`) y rendir el tejido real en el esquema violeta. [prio:media] [doc:mente/reportes/DOS_PIELES_soberano_2026-07-19.md] | M | pendiente |
| 136 | **Sembrar `verde/herbier/*.md` con Krista**: el endpoint vive y la UI retira la démo sola en cuanto haya fichas reales (#77 sigue vivo) — sesión corta con Krista eligiendo sus plantas y escribiendo las primeras fichas; cero código. [prio:alta] [doc:mente/reportes/DOS_PIELES_soberano_2026-07-19.md] | S | pendiente |
| 137 | **Flasheo de los ESP32 + broker MQTT en el Vigía (#133 del brief)**: los cuatro chips de La Sentinelle rinden «capteur à venir» hasta que exista la cadena sensor→broker→gateway; incluye decidir dónde vive el broker (vigía vs fragua) y el contrato de `/api/indoor/sensores`. [prio:media] [doc:mente/reportes/DOS_PIELES_soberano_2026-07-19.md] | L | pendiente |
| 138 | **[mano-david] La sesión de deploy en fragua** — WHY: el paquete está completo y verificado en frío; solo tu mano (o misión con mandato en fragua) puede aplicarlo. ORIGIN: CC → DEST: la-fragua. COMMANDS: seguir `deploy/fragua/paquete-dos-pieles/05-swap.md` paso a paso (backup obligatorio → código → restart SIN swap + EXPECT → swap `UI_CARA=dos-pieles` → humo del Cahier). VERIFY: los EXPECT del propio 05-swap.md, en orden. EXPECT ▸ `/dashboard`, `/jardin/` y `/tareas` sirven las pieles nuevas y `/api/jardin/notes` persiste una nota real. [prio:alta] [doc:deploy/fragua/paquete-dos-pieles/05-swap.md] | S | pendiente de firma — mano-david |

### 2026-07-19 · misión LAS TRES JOYAS Y EL SUELO EN EL CÓDIGO

| # | Sugerencia | Coste | Estado |
|---|---|---|---|
| 139 | **[mano-david] Push del README público a GitHub**: el commit `d42dc3e` (El Jardín + Teaching Kernel) espera local en `~/hexelion-public/` — soberano no tiene credenciales de GitHub. COMMANDS: `cd ~/hexelion-public && gh auth login` (o SSH key tuya) `&& git push`. Aprovechar para instalar el hook pre-push del sweep (#82, ya aprobada). VERIFY: la sección «The Garden» visible en github.com. [prio:alta] [doc:mente/reportes/TRES_JOYAS_soberano_2026-07-19.md] | S | pendiente de firma — mano-david |
| 140 | **Latido periódico del Monje**: unit+timer systemd --user que corra `genesis.py` cada N min y anexe a telemetría local (y como candidato a chip del SYSTEM STATE del Nexo vía gateway). Cicatrices aplicables: PATH de systemd (ruta absoluta `~/.venvs/p0x/bin/python`) y propose-only si el destino es fragua. [prio:media] [doc:p0x/monje/genesis.py] | M | pendiente |
| 141 | **Primer rito G3 controlado por la frontera**: una propuesta WASM real del Preceptor (algo trivial y verificable) que cruce `proponer()` y cuyo resultado firme el carbono — el ensayo del brazo de contención de IronClaw antes de que importe. [prio:media] [doc:p0x/preceptor/frontera.py] | M | pendiente |
| 142 | **Procesar el corpus de psicología por el lazo Observar**: las fuentes del kernel (Sweller, Kapur, retrieval practice) entran como documentos con delta y click del Soberano — para que las cuatro reglas tengan respaldo citable en `mente/`, no solo en el YAML. [prio:media] [doc:p0x/config/teaching_kernel.yaml] | M | pendiente |
| 143 | **Definir la métrica real de `competencia_demostrada`**: el fading necesita dato, no intuición — especificar qué cuenta como competencia demostrada en el Jardín/OpenWebUI (patrones ejecutados bien sin ayuda, errores auto-diagnosticados) antes de que ningún agente la aplique. [prio:media] [doc:p0x/config/teaching_kernel.yaml] | S | pendiente |

### 2026-07-20 · misión REPARACIÓN Y CIUDADANÍA DEL CHAT

| # | Sugerencia | Coste | Estado |
|---|---|---|---|
| 144 | **Persistir la piel del Chat tras upgrade**: `custom.css` vive dentro del paquete pip de OpenWebUI; un `uv tool upgrade open-webui` lo pisa (lo deja vacío) y el Chat vuelve al tema por defecto en silencio. Opciones: (a) symlink `static/custom.css → ~/p0x/deploy/soberano/chat-nexo.css` (sobrevive al upgrade si el upgrade no borra el symlink), o (b) hook post-upgrade que re-copie. Sin esto, la ciudadanía del Chat es frágil ante el primer `upgrade`. [prio:media] [doc:deploy/soberano/OPENWEBUI.md] | S | pendiente |
| 145 | **Tipografía exacta del Nexo en el Chat**: OpenWebUI solo trae NotoSans; IBM Plex Mono se cae a mono del sistema (límite declarado en Bloque B). Para la piel fiel: meter `IBMPlexMono-*.woff2` en `static/fonts/` + un `@font-face` dentro de `chat-nexo.css`. No hecho para no inflar el nodo con assets sin pedir — decisión del carbono si la fidelidad tipográfica lo merece. [prio:baja] [doc:deploy/soberano/chat-nexo.css] | M | pendiente |
| 146 | **Fixture de grafo para el juez visual del Second Brain**: `vite preview` no sirve `/assets/second_brain.json`, así que el Second Brain (Nexo) y el schéma violeta (Jardin) rinden vacío en las capturas — la Ley LOD (§3.4) queda verificada por lectura de código y unit, no por ojo sobre datos vivos. Versionar un `second_brain.sample.json` que el fetch use como fallback en dev haría la sopa-de-etiquetas (o su ausencia) auditable en Playwright. [prio:media] [doc:hexelion/dashboard/src/nexo/grafo/SecondBrain.tsx] | S | pendiente |
| 147 | **Tratamiento móvil del header del Nexo (390px)**: hoy el header es una tira `overflow-x:auto` (patrón legítimo, no desborda la página) pero en 390px los relojes y chips de firma quedan fuera de vista, solo alcanzables deslizando el header — la «cara que ve la gente» se lee como texto cortado («HEXELION  RA…»). Considerar ocultar los chips secundarios o envolver bajo un breakpoint móvil. NO se tocó en esta misión: cambiar la cara pública sin blueprint es acto del carbono. [prio:baja] [doc:hexelion/dashboard/src/nexo/header/header.css] | S | pendiente |
| 148 | **[mano-david] Redactar el contrato de datos de 5 líneas del Chat**: hueco real declarado desde G0 — antes de dar la primera cuenta a un hermano (§FIN paso 2) debe existir el contrato que se pega en su primer login: qué ve/hace, retención de conversaciones, qué NO sale del nodo. Sin él, la puerta del Chat no se abre a terceros aunque el admin ya exista. [prio:alta] [doc:deploy/soberano/OPENWEBUI.md] | S | pendiente de firma — mano-david |

### 2026-07-20 · misión PULIDO FINAL DEL ORGANISMO VIVO

Atendidas en esta misión (commit `7042907` de `hexelion`): **#144** (mecanismo `DATA_DIR`
externo documentado en `hexelion/chat-p0x/CHAT_P0X.md §4`), **#146** (fixture
`tests/fixtures/second_brain.json` + `tests/fase-grafo.spec.ts`, vía `page.route`),
**#147** (header móvil sin desborde, 2 tramos responsive). Jardin violeta-noche
Opción B aplicado (elección de David). Aurelius nació como repo propio `~/aurelius`.

| # | Sugerencia | Coste | Estado |
|---|---|---|---|
| 149 | **Celda "Rack Health" en el Nexo**: el canal `nodes` (`/api/health/nodes`) se sondea cada 30s con dato real pero NINGÚN componente lo consume (poll sin render). No se inventó celda (doctrina: no inventar layouts). Candidato a celda de salud del rack. [prio:baja] [doc:hexelion/dashboard/src/nexo/datos/canales.ts] | S | pendiente |
| 150 | **Contraste del readout de La Sentinelle**: en el reskin violeta-noche, los sensores sobre la caja de cámara oscura quedan legibles pero tenues (rgba(20,14,8,.55) + tinta). Subir contraste del strip. [prio:baja] [doc:hexelion/dashboard/src/jardin/sentinelle/sentinelle.css] | S | pendiente |
| 151 | **Arrancar el proxy LiteLLM (:4000) y apuntar OpenWebUI a él**: hoy OpenWebUI va directo al Ollama de soberano; el `litellm_config.yaml` (failover torre→fragua) existe pero `:4000` no responde. Cablear para failover real. [prio:media] [doc:p0x/proxy/litellm_config.yaml] | M | pendiente |
| 152 | **Extender el fixture #146 a aserciones LOD por estado/pixel**: el fixture ya da grafo estable; falta que el juez pruebe la Ley LOD real (labels por zoom <0.8 / 0.8–1.4 / >1.4). [prio:media] [doc:hexelion/dashboard/tests/fase-grafo.spec.ts] | M | pendiente |

### 2026-07-21 · PROMPT MAESTRO · cierre de deuda técnica (3 misiones)

M0 (verificación): HEAD de `hexelion` estaba en `138ab1a` con todo lo posterior a
`7042907` **commiteado pero NO desplegado** — fragua sigue sirviendo un dist viejo (el
swap del runbook `deploy/fragua/paquete-dos-pieles/05-swap.md` nunca corrió). M1
`729ded4` (ondas Second Brain + mapa direccional + OSINT), M2 `1171337` en `~/aurelius`
(cara HTML + server 8050), M3 `e4bdeab` (enlace del Puente). 240 tests verdes en cada bloque.

Hallazgo de realidad (M2): **Ollama en soberano escucha SOLO en `127.0.0.1:11434`** — la
IP del tailnet devuelve `000`. La cara servida en :8050 (tailnet) NO puede alcanzar el
modelo hasta abrir Ollama a `0.0.0.0` + `OLLAMA_ORIGINS` (requiere sudo del carbono; sin
sudo interactivo en soberano). OpenWebUI (`:8080`) sí está en el tailnet pero con AUTH y
sin api-keys → no sirve de endpoint crudo para una página estática.

| # | Sugerencia | Coste | Estado |
|---|---|---|---|
| 153 | **Abrir Ollama al tailnet (desbloquea la cara de Aurelius end-to-end)**: `sudo systemctl edit ollama` → `Environment="OLLAMA_HOST=0.0.0.0"` + `Environment="OLLAMA_ORIGINS=*"`, luego `sudo systemctl restart ollama`. Sin esto, `aurelius_face.html` cae siempre a su fallback honesto. Revisar exposición: 0.0.0.0 abre 11434 a TODA interfaz, no solo tailnet — considerar bind a la IP `100.81.82.34` en vez de `0.0.0.0`. [prio:alta] [doc:/etc/systemd/system/ollama.service] | S | pendiente |
| 154 | **Ejecutar el swap en fragua (todo lo commiteado desde `7042907` sigue sin desplegar)**: `git pull` + restart del gateway según `deploy/fragua/paquete-dos-pieles/05-swap.md`. Hasta entonces el carbono NO ve nada del pulido en el dashboard vivo. [prio:alta] [doc:p0x/deploy/fragua/paquete-dos-pieles/05-swap.md] | S | pendiente |
| 155 | **Servicio systemd `--user` para la cara de Aurelius (:8050)**: hoy `servir_interfaz.py` se arranca a mano. Unit `aurelius-cara.service` con `Restart=on-failure` y ruta absoluta a python (footgun PATH de systemd). [prio:media] [doc:aurelius/scripts/servir_interfaz.py] | M | pendiente |
| 156 | **Puente → Aurelius en pestaña nueva**: el enlace navega en la MISMA pestaña (coherente con Nexo/Jardin), pero Aurelius vive en otro puerto/app; un `target="_blank" rel="noopener"` evitaría que el carbono pierda el dashboard al cruzar. Decisión de UX pendiente de David. [prio:baja] [doc:hexelion/dashboard/src/shared/puente/Puente.tsx] | S | pendiente |
| 157 | **Frames de habla extra para la cara (visemas)**: hoy alterna 2 frames (normal↔boca-abierta) del sheet `stitch_the_solarpunk_emperor`. El sheet tiene 12 expresiones; mapear 3-4 visemas daría un habla menos robótica. [prio:baja] [doc:aurelius/src/assets/] | M | pendiente |

### 2026-07-25 · lote Capa 1 del triaje (Prompts 1-4) — commits `1924559`+`1f58172` (aurelius), `2a731e4`+`c738b72` (hexelion)

| # | Sugerencia | Coste | Estado |
|---|---|---|---|
| 158 | **Aurelius: una sola fuente de verdad del system prompt** — hoy vive en 3 sitios (`scripts/aurelius.system.txt`, la DB de OpenWebUI, y la copia embebida en `interface/aurelius_face.html`); un edit se sincroniza a mano y deriva. Que la cara HTML lea el `.txt` (fetch en build/arranque) o un paso de build que inyecte ambos. [prio:media] [doc:aurelius/interface/aurelius_face.html] | S/M | pendiente |
| 159 | **Aurelius: frame de párpado despierto (blink real)** — `Habla.png` no tiene un frame de ojos-cerrados agrietado/ámbar; el único ojos-cerrados es mármol liso sin despertar. El parpadeo actual es el dip del ojo-máquina (CSS). Un frame de párpado despierto daría un blink literal. (Parcialmente cierra #157: ya se ciclan 3 frames de boca.) [prio:baja] [doc:aurelius/interface/assets/Habla.png] | S (arte) | pendiente |
| 160 | **Aurelius: app Vite incompleta** — `src/` no tiene `index.html` ni `main.ts`; la única cara viva es el HTML standalone (:8050). Decidir: construir la app Vite (`src/bust.ts`/`missions.ts`/`ai.ts` sueltos) o canonizar la cara HTML como la oficial y retirar el scaffolding. [prio:media] [doc:aurelius/src] | M/L | pendiente |
| 161 | **Aurelius: dedup de `Habla.png`** — vive duplicado en `src/assets/` y `interface/assets/` (1.3MB ×2 en git). Symlink o una sola ubicación canónica servida. [prio:baja] [doc:aurelius/interface/assets/Habla.png] | S | pendiente |
| 162 | **Jardin: verificar el modelo del gateway para Reestructurar** — el endpoint `/api/jardin/reestructurar` usa `JARDIN_RESTRUCT_MODEL` (default `qwen3-coder:30b`). Confirmar que el host del gateway (fragua) tiene ese modelo, o exportar el env; y un test e2e del flujo cuando el gateway esté vivo (aquí solo `py_compile`, el gateway no corre en soberano). [prio:media] [doc:hexelion/hexelion_gateway.py] | S/M | pendiente |
| 163 | **Mapa: rastro persistente real** — hoy la trayectoria del avión se acumula en sesión (fixes reales observados entre sondeos; se pierde al recargar). dump1090 da snapshots, no historial. Para trayectoria histórica de verdad, el gateway debería guardar posiciones (endpoint `/api/aircraft/history` en fragua/el-vigía). [prio:baja] [doc:hexelion/dashboard/src/nexo/mapa/UnifiedMap.tsx] | M | pendiente |
| 164 | **Canonizar la Doctrina de Prompts Seguros** — el triaje §2.3 la marca como alto valor / cero riesgo; redactarla como MD en `mente/doctrina/`. (Nota del Preceptor al pie del lote Capa 1.) [prio:media] [doc:mente/doctrina/] | S | pendiente |
| 165 | **Redeploy fragua del fix del Jardin (móvil)** — el commit `96e098a` (header del Jardin sin desborde a 360px) solo llega a producción tras `git push` + `git pull` + restart del gateway en fragua. El dashboard corre en fragua, no en soberano; sin ese paso el bug de 360px sigue en la web servida. [prio:alta] [doc:hexelion/dashboard] | S | pendiente |
| 166 | **Aurelius: header móvil en 2 filas** — el fix (commit `1f48db1`) garantiza cero desborde y todo visible a 360/390, pero "Le Chemin" cae a una 2ª fila (red de seguridad `flex-wrap`). Pulir a 1 sola fila (busto/selector/Path más compactos) sin reintroducir el desborde de 36px. [prio:baja] [doc:aurelius/interface/aurelius_face.html] | S | pendiente |
| 167 | **Aurelius: instalar deps de test (red)** — se añadió `playwright.config.ts` + `tests/movil.spec.ts` (5 viewports), verificados aquí reusando la instalación de Playwright del dashboard. Falta `npm i` en `~/aurelius` (necesita red) para que `npm test` corra por sí solo y entre en CI local. [prio:media] [doc:aurelius/package.json] | S | pendiente |
| 168 | **Aurelius: i18n del Path incompleto** — con locale `es` el selector muestra "Le Chemin" (francés) y el Path (`camino.html`) tiene título/misiones hardcodeados FR/ES sin obedecer al selector. Es el Prompt 1 de la ronda siguiente; registrado aquí para no perderlo. [prio:alta] [doc:aurelius/interface/camino.html] | M | pendiente |
| 169 | **Dashboard: test explícito de táctiles ≥44px** — la suite de Aurelius comprueba táctiles ≥44px en móvil; la del dashboard aún no. Añadir a `movil-cabeceros.spec.ts` un chequeo de que los clicables de header (PROOF/TRAY/CHAT, nav del Jardin) miden ≥44px a 360/390. [prio:baja] [doc:hexelion/dashboard/tests/movil-cabeceros.spec.ts] | S | pendiente |
| 170 | **Desplegar en fragua la cola de commits de la semana** — nada de lo hecho (redirect 308 `89d8bd7`, feeds distribuidos `b77fa1a`, header compacto+grafo+plegado `f3694c9/dc129bc/478a6e9`, rutas `/ui` `1ee0aa9`, jardin móvil `96e098a`) llega a producción sin `git push` + `git pull` + restart del gateway/bridge en fragua. Es el mayor bloqueo: el UI vivo es el viejo. [prio:alta] [doc:hexelion] | S | pendiente |
| 171 | **Second Brain §2.4/§2.5 diferidos** — la animación de apertura de esferas en fullscreen (§2.4) y la edición FIRMADA de nodos del grafo (§2.5) siguen PENDIENTE (los endpoints `/api/tareas/esferas` existen para la Bandeja, no cableados al grafo). Decidir si entran o se entierran del backlog con evidencia. [prio:baja] [doc:hexelion/dashboard/src/nexo/grafo/SecondBrain.tsx] | M | pendiente |
| 172 | **Aurelius Prompt C sin ejecutar** — i18n 7 idiomas + el Path obedeciendo al selector (168) + header a 1 fila (166) + higiene de hostname visible. Es el mayor hueco de Aurelius; hoy solo en/es y el Path con título FR hardcodeado. [prio:alta] [doc:aurelius/interface] | M | pendiente |
| 173 | **Vigía SSH pubkey caída (dup de 11) bloquea el AIS distribuido** — sin `authorized_keys` en el Pi, el reset remoto del AIS (`/api/antenna/reset` feed=ais) y el deploy limpio del `ais-catcher` dependen de password. Restaurar la clave antes de cablear el AIS del Vigía. [prio:alta] [doc:deploy/vigia] | S | pendiente |
| 174 | **READMEs públicos optimizados sin ejecutar** — perfil/Hexelion/Aurelius (higiene dura: cero IPs/claves/rutas internas). El repo `hexelion-public` existe (14/23) pero la pasada de optimización SEO/LLM no se corrió. [prio:media] [doc:hexelion-public] | S | pendiente |

---

## 2026-08-01 · ESTADO CONSOLIDADO (tri-estado) — Ronda Secuencial · C0

Vista tri-estado de todo lo abierto de todas las rondas. El backlog #149–174 sigue
vigente salvo lo movido a 🟢 CERRADO aquí; los ítems que dependen de fragua / sudo / red
caen en 🟡 BLOQUEADO. Los 6 ítems nombrados por el Soberano van marcados `[NOMBRADO]`.

### 🟢 CERRADO (con la prueba que lo cierra)
- **Sprint Assets A1 · scrubber** — `tools/scrub_check.js`, commit hexelion **`4a91c2b`** (4 casos verdes; Modo A DOM + Modo B OCR falla-cerrado).
- **A2 · modo presentación** — **`cfa5a2d`**; gap OSIRIS/Legión acentuada **`6f02fde`**; present test **10/10**; captura present-mode pasa el scrubber (Modo A y B, 0 CRIT).
- **A3–A5 · 15 capturas** — `~/linkedin_assets/2026-08-01/`, scrubber **0 CRIT** en los 15 PNG (tabla en reporte del bloque).
- **A6 · READMEs firmados** — aurelius **`4f1b7e1`**, códice **`0f229da`**, hexelion **`eb918ed`** (imágenes en `docs/img/`, pies firmados por el Soberano).
- **#153 · Ollama al tailnet** — prueba: `100.81.82.34:11434/api/tags` → **200** (+ CORS).
- **#155 · servicio aurelius-interfaz (:8050)** — prueba: `systemctl --user is-enabled/is-active` → **enabled/active**, ruta absoluta a python.
- **aurelius-interfaz crash-loop** (~29 953 reinicios; huérfano `servir_interfaz.py` PID 690249 ocupaba :8050 → `[Errno 98]`) — prueba: huérfano matado, systemd rebindeó fresco (`active`), camino.html + /api/estado 200. *Endurecimiento del servicio → C4.*

### 🟡 BLOQUEADO (depende de algo externo)
- **Swap/redeploy en fragua** [#154 #165 #170] — depende de: **tu mano** (`git pull` + restart del gateway en fragua, `deploy/fragua/paquete-dos-pieles/05-swap.md`). Es el mayor bloqueo: TODO el pulido commiteado (present mode, observar, mapa, jardin móvil…) sigue sin estar vivo; el UI servido es el viejo.
- **03_map sin marcadores** — depende de: feeds ADS-B/AIS de **el-vigía** vivos → hoy `/api/antenna/health` da `ais live:false · adsb live:false`. A su vez bloqueado por el RF del Vigía (→ **C2** diagnostica).
- **Vigía SSH pubkey caída** [#173] — depende de: restaurar `authorized_keys` en el Pi (acceso/clave). Bloquea AIS distribuido + reset remoto.
- **LiteLLM :4000 failover** [#151] — depende de arrancar el proxy (failover torre→fragua).
- **Ítems que exigen sudo/red** [#167 npm i, otros] — sudo interactivo NO disponible en soberano; red requerida para instalar deps.

### 🔴 ABIERTO (accionable ya)
- `[NOMBRADO]` **1 · Bloque 1 · drawer del Camino — NO cerrado.** `aurelius_face.html` carga `camino.html` como **documento separado** vía `<iframe id="au-drawer-frame">`; camino.js/oraculo.js son docs aparte. La recursión (cara→iframe→camino) sigue disponible. → **C1** lo cierra: absorber camino.html como componente del documento único. Evidencia: iframe en aurelius_face.html + camino.html separado.
- `[NOMBRADO]` **2 · [DERIVADO] en oráculo** — `oraculo.js` (`window.AURELIUS_ORACULO`) entrega un valor **derivado** del hardware/RAM que la cara y el Camino consumen (aurelius_face.html:395, camino.js:226). Verificar que no muestre un `[DERIVADO]` donde debe ir un dato **medido** (honest sensors); si es derivado, etiquetarlo como tal o medirlo.
- `[NOMBRADO]` **3 · i18n huérfanas** — `i18n.js` define claves (`face.*`) y el Path usa `I.t("path.title")`, pero camino.html/js tienen título/misiones **FR/ES hardcodeados** que no obedecen al selector (liga con #168 #172). Auditar claves definidas-sin-uso y usos-sin-clave.
- `[NOMBRADO]` **4 · Colisión M3 / sonda-física** — "M3" sobrecargado: Path/README M3 = *The Refuge (offline)*; `firmar_artefacto.py` M3 = generación de clave Ed25519 (*El Pacto*); y `src/missions.ts:115` define una misión de **sonda física** ("fotografía una planta; la sonda la lee sin red"). La cara HTML (camino) y la app Vite (missions.ts, #160 incompleta) **divergen** en qué es M3. Unificar numeración/definición antes de construir M3+.
- `[NOMBRADO]` **5 · Poller compartido → 4 paneles STALE al mismo segundo** — `canales.ts`: cada fuente tiene su `setInterval(cadaMs)` (l.45), `useCanal` tickea a 1s (l.69), UMBRAL_STALE 30s (`bus.ts`). Si 4 paneles cuelgan del **mismo origen/cadencia**, envejecen a STALE a la vez cuando ese origen cae. Verificar si comparten fuente y si la frescura debe ser por-panel.
- `[NOMBRADO]` **6 · Agente que aletea 6/6→5/6** — `hexelion_gateway.py:1635/1699` emite "{active}/6 agentes activos"; `active` oscila 6→5 (una voz del Sínodo intermitente). Identificar cuál cae y por qué (el gateway corre en fragua; diagnosticable por curl).
- **Backlog vivo restante** — #149, #150, #152, #156–#164, #166, #168, #169, #171, #172, #174 siguen ABIERTO (accionables en soberano/repos) salvo los marcados BLOQUEADO arriba.

*Consolidado read-only (grep/systemctl/curl), sin cambios de código. Ronda Secuencial C0.*

---

## 2026-08-02 · DEPLOY · runbook exacto (Ronda G · G5)

Cuarta ronda que el trabajo queda "a un git pull de existir". Comandos, uno por
línea. Verifica primero la rama que sirve el gateway en el OPi (aquí se asume la de
trabajo). `git push` lo empuja **el Soberano** (no yo).

```
# 1 · SOBERANO — push (revisa 'ahead' con ~/hexelion/scripts/preflight.sh):
git -C ~/hexelion push origin nexo-carbono-dashboard-20260623   # preflight + gateway ADS-B + overlay mapa
git -C ~/p0x     push                                            # PENDIENTES
# aurelius: BLOQUEADO (clave GitHub, ver §G4). Registrar clave o pasar a HTTPS + scrubber ANTES.

# 2 · OPi (ubuntu@100.82.94.83) — traer el código:
cd /home/ubuntu/hexelion && git fetch origin && git checkout nexo-carbono-dashboard-20260623 && git pull

# 3 · OPi — cablear la lectura ADS-B por fichero (G2), una vez:
grep -q HEX_DUMP1090_JSON .env || echo 'HEX_DUMP1090_JSON=/run/dump1090/aircraft.json' >> .env

# 4 · OPi — reconstruir el dashboard SOLO si cambió dashboard/src (overlay del mapa, G3):
cd dashboard && npm ci && npm run build && cd ..

# 5 · OPi — reiniciar SOLO lo que cambió:
sudo systemctl restart hexelion-gateway     # toma gateway (G2) + .env
#   NO reiniciar dump1090/ais-catcher aquí: su bloqueo es el SERIAL del dongle
#   (ilegible/mismatch, ver §F1), no el código — eso es ventana de mantenimiento.

# 6 · SOBERANO — verificar:
~/hexelion/scripts/preflight.sh
```

> El mapa **no** pintará marcadores tras el deploy: dump1090 recibe 0 mensajes por el
> mismatch de serial del dongle (§F1). El deploy deja el **cable puesto** (código +
> overlay honesto); los marcadores llegan cuando se resuelva el serial en ventana de
> mantenimiento (decisión del Soberano).

## Cierre de capítulo
Documento de cierre → **`CIERRE_HEXELION.md`** (raíz de `hexelion`). *Pendiente del
contenido que pasa el Soberano aparte (Ronda G · G6); se añadirá y este puntero se
actualizará al recibirlo.*

## Ronda Apéndices (BLOQUE 8.3 + Apéndice B) · 2026-08-03

Sugerencias accionables (coste S/M/L):
- **(S)** Corregir el fallo PREVIO restante: overflow horizontal de `aurelius_face.html`
  a 360px (`tests/movil.spec.ts:34`). No es regresión de esta ronda; la suite ya
  estaba roja en móvil. Aislar el elemento que desborda y acotarlo con `max-width`.
- **(M)** Consolidar la DUPLICACIÓN de `interface/camino.js` y el `<script>` inline de
  `interface/camino.html`: hoy son copias casi idénticas del mismo módulo. Cada cambio
  (como la predicción previa de esta ronda) hay que aplicarlo dos veces → footgun. Que
  `camino.html` cargue `camino.js` como el resto, o extraer el módulo a un solo sitio.
- **(S)** `package-lock.json` de Aurelius quedó SIN commitear (lo generó `npm install`
  local para poder correr tsc/Playwright). Decidir si se versiona (recomendado: sí,
  fija deps) o se ignora — hoy el repo no traía lock.
- **(M)** Cuando se implemente el asesor del Alquimista (rama `alquimista-asesor`,
  servicio separado), que publique el dictamen de abstención explícito con TTL
  (`estado="abstiene"` + motivo + emitido/caduca) — el panel ya lo honra (§8.3).
- **(L)** Integrar el temario LLM propiamente en las misiones, atado a
  `aurelius/docs/TEMARIO_LLM.md`: llevar calibración y el marco correcto de RLHF a una
  lección temprana; hoy solo existen como canon de fuente, no como misión jugable.

## Backlog de UI/software (autoritativo)
El trabajo pendiente de **interfaz** (Hexelion · Aurelius · Le Jardin) vive en su
propio documento: **[`mente/backlog/BACKLOG_UI.md`](../backlog/BACKLOG_UI.md)**
(bloques atómicos 0–10, formato de reporte, invariantes). Este `PENDIENTES.md`
sigue siendo el registro de sugerencias/deuda general; el de UI se gestiona allí.
