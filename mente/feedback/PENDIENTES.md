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

## Ronda MITOCONDRIA-F0 (el censo de reflejos) · 2026-08-04

- **(S)** **Sin acceso a la-fragua y el-vigía, F1 mediría el nodo equivocado.** Los dos
  reflejos que la misión señala como principales (pausa preventiva 78 °C y guard de lotes
  80 °C) corren en la-fragua, y `ssh` desde soberano responde `Permission denied` en ambos
  nodos. El censo los documenta desde el código versionado, no desde su runtime. Restaurar
  la pubkey de soberano en los dos (paste de una línea, mano del Soberano) es lo que
  convierte F1 en una línea base real en vez de una de laboratorio.
- **(S)** **El contador `n/6` tiene un término que nunca puede subir.** `_SINODO_ROLES`
  declara 6 roles incluido `enlace`, y en la-torre hay 5 directorios de agente y 5
  servicios: `enlace` no existe. Su clave está siempre ausente → `stale` permanente.
  Decidir: se implementa el sexto agente, o sale de la lista. Mientras tanto, cualquier
  lectura del contador arrastra un fallo fijo que no es aleteo y lo enmascara.
- **(S)** **El pulso del Sínodo no caduca, y la especificación exige que pueda.**
  `base_agent.py` publica `hexelion:sinodo:<rol>:latest` con `set` sin TTL; solo el
  histórico diario recibe `expire`. Un agente muerto conserva su última verdad para
  siempre — exactamente la trampa que §2.4 de la especificación existe para eliminar.
  Artefacto propuesto hacia la-torre, no aplicable desde aquí.
- **(M)** **`thermal_zone0` no es portable entre nodos y F1 tropezará con ello.** Medido en
  soberano: `thermal_zone0` es `acpitz` y devuelve 20 °C constantes; el sensor real de CPU
  es `k10temp` y el de iGPU `amdgpu`, ambos por `hwmon`. Cinco reflejos leen `zone0` por
  convención heredada de la Fragua. El lector único de F1 necesita descubrir su sensor por
  nodo y declarar cuál eligió, o publicará un veredicto honesto sobre un número falso.
- **(S)** **Ningún proceso con cadencia horaria fue hallado en los nodos medidos.** No hay
  `.timer` del Alquimista en la-torre (corre como servicio con tick de 300 s), y el único
  timer de usuario es el del Monje a 5 min. La hipótesis del minuto `:07` no tiene todavía
  un proceso al que señalar en lo medible. Dejar correr la instrumentación del Bloque 9 y
  traerse `hexelion:sinodo:flaps` **antes** de abrir F3.3, para que el diagnóstico llegue
  con dato y no con teoría.
- **(S)** **Decidir en qué nodo vive la primera Mitocondria.** El veredicto es por nodo,
  pero soberano tiene hoy cero reflejos P0X: ni un timer, ni un cron, ni una guarda
  embebida. Un árbitro instalado aquí en F1 no tendría a quién arbitrar en F3. La Fragua es
  donde están los consumidores; soberano es donde está el permiso de escribir código.
  Conviene fijarlo antes de F1, no después.

## Ronda SOBERANO-DECISIONES (ejecución de las 9 decisiones) · 2026-08-04

- **(S)** **Rotar las dos credenciales Titan es lo único que las revoca.** Retiré
  `DEPIN_INVENTORY.md` y redacté `INFORME_PASADA_MATINAL.md` —que tenía la misma clave y no estaba
  en tu lista—, así que el árbol de trabajo queda a cero. Pero **siguen en el historial de git de
  ambos ficheros**. Borrar no revoca: hay que rotarlas en el servicio de origen, y hacerlo aunque
  además se purgue el historial con `git filter-repo`.
- **(S)** **El modelo NO estaba expuesto, aunque lo dieras por hecho.** Estaba en `127.0.0.1`. Lo
  que respondía en el `:8080` del tailnet era open-webui, que además no tiene backend desde que
  Ollama está parado — un panel que parecía vivo. Ya está expuesto en el **8081** (el 8080 del
  tailnet lo ocupa open-webui) y **bindeado a la IP de la tailnet, no a `0.0.0.0`**: con `0.0.0.0`
  el modelo quedaría escuchando en la LAN sin autenticación alguna.
- **(S)** **La memoria de Titan es irrecuperable si se pierde ese fichero.** Vive en
  `~/memoria-titan-hp2.txt`, `chmod 600`, fuera de los tres repos. Los directorios de origen ya
  están borrados, así que **no hay segunda copia**. Si vale algo, respáldalo donde respaldes lo
  demás. Aviso honesto: dentro hay `agent_id`, `titan.info`, la unidad y el script; **no aparecían
  wallets `0x` ni las «3 cuentas»** por ningún lado — si existen, están en el panel web de Titan,
  no en disco.
- **(S)** **`uptime-kuma` queda documentado como ajeno al rack** en `hexelion/docs/NODOS_EXTERNOS.md`,
  con su puerto y la nota de que no se gestiona ni entra en el dashboard.
- **(S)** **Zombis que siguen vivos y no eran de esta ronda:** GagaNode en El Vigía (~22 MB, corre
  como *root* y comparte IP pública con HP1), el directorio GagaNode en La Fragua (23 MB) y
  `gaianet_storage` en La Torre (131 MB). Estaban en el inventario retirado; los conservé en el
  sucesor para que no se pierdan.

## Ronda HEXELION-CLOSE-1 (deploy del 9 + limpieza de HP-02) · 2026-08-04

- **(S)** **Hay credenciales en claro versionadas desde el 30-may.** `hexelion/DEPIN_INVENTORY.md`
  contiene **dos** en la tabla histórica de HP1: un API token del agente Titan y un `appKey` de
  `earn_sdk`. Viola el invariante «cero contraseñas en ficheros versionados». No las he tocado
  para no alterar el histórico de auditoría, pero **hay que rotarlas y purgarlas — y rotarlas
  aunque se purguen**, porque el historial de git ya las contiene. Los 142 MB de restos del agente
  en `/opt` de HP-02 también llevan su clave en disco.
- **(S)** **Commitea el cambio de `AIS_BASE` en La Fragua antes de que otro `pull` lo pise.** El
  deploy del 9 se encontró `hexelion_gateway.py` modificado sin commitear (dos URLs cableadas
  sustituidas por `{AIS_BASE}`). Lo aparté y lo reapliqué, así que sigue vivo pero **sigue sin
  commitear**. Es trabajo tuyo que solo existe en ese nodo.
- **(M)** **El modelo del rack no es alcanzable desde ningún otro nodo.** `llama-server` bindea
  loopback; lo que responde en el `:8080` del tailnet es open-webui, que además no tiene backend
  (Ollama está parado). Si HP-02 debe asumir verificación cruzada usando el modelo, hay que
  exponerlo a la tailnet — decisión tuya, con su coste de superficie.
- **(S)** **La prueba de honestidad del BLOQUE 9 sigue pendiente y es lo que decide el bloque.**
  El deploy solo puso el instrumento; `hexelion:sinodo:flaps` está vacío porque aún no ha habido
  transición. Hacen falta ≥2 h para cruzar dos veces el minuto `:07`. Recuerda el criterio de
  fallo: si el parpadeo desaparece **porque se suavizó el indicador**, el bloque está fallado.
- **(S)** **`legion_sol`/`legion_luna` siguen como «DePIN Worker» en el código vivo**
  (`hexelion_pollers.py:37-38`, `disk_poller.py:47-48`, `hexelion_gateway.py:334,738,2489`), y
  `OSIRIS_GDELT_URL` apunta a un nodo muerto. No lo he tocado: cambiarlo altera el runtime del
  dashboard que acabo de desplegar y merece su propio bloque con prueba.

## Ronda HP-HEXELION-1 (reconocimiento de los HP + plan de cierre) · 2026-08-04

Plan completo en [`mente/backlog/PLAN_CIERRE_HEXELION.md`](../backlog/PLAN_CIERRE_HEXELION.md).

- **(S)** **Dos bucles de fallo llevan días comiendo CPU y nadie los miraba.** La Fragua:
  `hexelion-gateway.service` con **16.026** reinicios (~44 h, ~1.4 s de CPU cada uno). El Vigía:
  `dump1090.service` con **18.063**. Ambos en nodos con vigilancia térmica declarada, y ambos
  llenando el journal de ruido que tapa señales reales. El del gateway se resuelve con el deploy
  del BLOQUE 9; el de dump1090 no tiene bloque asignado.
- **(S)** **El gateway de producción no lo gobierna systemd.** Lo que sirve el :8001 es un proceso
  lanzado a mano con `setsid` el 02-ago, fuera de systemd; la unidad lleva desde entonces fallando
  con `[Errno 98] address already in use`. Mientras siga así, ningún despliegue del gateway surte
  efecto aunque parezca que sí. Es el mismo patrón que el `llama-server` del soberano: producción
  sostenida por procesos manuales sin registro.
- **(M)** **El BLOQUE 1 no es «instalar un puente»: es sustituir uno roto.** El Vigía ya corre
  `p0x-m5-ingest.service` con **otro** `ingest_m5.py`, cableado a `localhost` y en bucle de
  `Redis caído: Timeout` desde el 02-ago — cero datos. Deja una clave `:scan` **sin TTL** rancia,
  justo el antipatrón que la doctrina prohíbe. Los dos puentes se pelean por `/dev/ttyUSB0`, así
  que hay que parar y deshabilitar el viejo antes de desplegar el bueno.
- **(S)** **`musculo-hp-02` no es lo que dice el canon.** Es un Chromebook (`Google/Dratini`) con
  7.6 GiB de RAM, eMMC y sin GPU; no es toolchain de entrenamiento ni puede servir un 30B. Y no
  aloja OSIRIS. Corrige `CLAUDE.md` («musculo-hp-01/02 (x86) · Toolchain de entrenamiento») o
  reasigna el rol. Además tiene un contenedor ajeno al rack (`titanhub/earn-sdk`) corriendo.
- **(S)** **BLOQUE 8: separa 8.3 de 8.1 o el bloque no cierra nunca.** OSIRIS vive en
  `musculo-hp-01`, offline **10 días** según la propia tailnet. 8.1 exige medirlo y no hay forma
  desde aquí. El contrato del Jurado (8.2) está firmado y no depende de OSIRIS: 8.3 puede avanzar.
- **(S)** **El Vigía no acepta mi clave por los usuarios obvios, pero sí por `pi`.** Documentar el
  usuario de cada nodo en `~/.ssh/config` (hoy solo está la-torre) ahorraría el rastreo a ciegas
  que costó esta ronda. Y `musculo-hp-02` sigue con **Tailscale SSH** interceptando el 22, pese a
  darse por desactivado.

## Ronda SOBERANO-1 (autorización del modelo + auditoría de ramas) · 2026-08-04

- **(S)** **El despliegue del BLOQUE 1 es la piedra angular: lo esperan tres cosas.** `ingest_m5.py`
  y `m5-bridge.service` están escritos, comprometidos y con `--self-test` verde desde el 02-ago,
  sin instalar en El Vigía. Mientras no se despliegue: 6.1 no se puede verificar, la prueba de
  honestidad de La Sentinelle no se puede correr, y el BLOQUE 6 no cierra. Es el desbloqueo más
  barato del backlog. IronClaw: lo instalas tú, yo no.
- **(S)** **Contradicción real entre 5.4 y 10.3 — hay que resolverla antes de tocar misiones.**
  5.4 dice *«sonda física CONGELADA, sin cambio de código»*; 10.3 dice *«la sonda vive solo en M7,
  en M3 queda enlace, no paso ejecutable → CC propone diff»*. Una dice no toques, la otra pide
  diff. Verificado en código: el paso de la sonda **sigue** dentro de M3 y M7 existe, o sea que la
  duplicación está viva. Firmar una de las dos.
- **(M)** **BLOQUE 8: decidir si OSIRIS se recupera o se archiva.** El nodo que lo sirve está
  **inalcanzable** (SSH y endpoints medidos a cero el 03-ago), así que 8.1 no puede completarse por
  mucho que se insista: repo, versión, runtime y claves siguen NO DATA. El contrato del Jurado (8.2)
  ya está firmado y no depende de eso. Sugiero separarlos: 8.3 puede avanzar sin el feed.
- **(S)** **BLOQUE 9 está a un deploy de dejar de ser teoría.** La instrumentación está escrita y
  comprometida (`68a39a8`, `_instrumentar_sinodo` en el gateway), propose-only. Sin desplegarla, la
  hipótesis del minuto :07 no es falsable — que era justamente el punto del bloque.
- **(S)** **`~/aurelius-lora/` lleva en espera desde el 02-ago con condición de salida vaga**
  («hasta cerrar el resto de bloques»). Como el resto de bloques no cierra, la espera es indefinida.
  O se archiva o se le pone una condición medible.
- **(S)** **`ORQUESTA_MODELOS_P0X.md` sigue sin commitear y ya solo acierta a medias.** Tras hoy,
  `num_ctx 16384` y `backend Vulkan` **sí** son correctos; siguen sin serlo `base qwen3-coder:30b`
  vía Ollama (Ollama está parado; el modelo se sirve desde un gguf en disco, sin registro) y el
  harness (el envoltorio entregado es `cc-local`, de Claude Code; OpenCode sigue instalado y el
  servidor le habla, pero nadie lo ha probado contra este modelo).

## Ronda BLOQUE 12-bis (cerebro local · metal nuevo) · 2026-08-04

El Soberano movió el metal: Ollama fuera, `llama-server` a mano en su lugar. Esta tanda
**sustituye** a la de abajo, que quedó obsoleta salvo donde se diga.

- **(S)** **`Workflow` envenena el arnés — vigilar que siga mitigado.** Causa raíz medida: la
  conversión JSON-Schema→GBNF de llama.cpp expande `maxLength` a gramática de repetición explícita
  y revienta entre 1024 y 16384; `Workflow.script` declara `524288`. Sin excluir esa herramienta,
  el cerebro local **no arranca**: falla el primer turno con `400 failed to parse grammar`.
  `bin/cc-local` ya invoca `--disallowedTools Workflow`. Reevaluar si se actualiza llama.cpp.
- **(S)** **Decidir qué modelo debe ser el cerebro del arnés.** Lo que hay en RAM es
  `qwen3:30b-a3b-instruct-2507-q4_K_M` (identificado por digest), el modelo **general**. El canon
  del nodo describe `soberano-coder` construido `FROM qwen3-coder:30b`, el **especializado en
  código**, cuyo gguf sigue en disco aparte. Para un arnés de código la diferencia importa. Es
  decisión tuya: se reporta el hecho, no se elige por ti.
- **(M)** **Activar aceleración: es el mayor retorno disponible.** El servidor corre `-ngl 0`, CPU
  pura. Medido hoy: ~23.9 tok/s de generación. El bench G0 de este nodo midió Vulkan **3.28×** en
  generación y **3.58×** en proceso de prompt. En un arnés context-heavy lo que duele es el
  segundo. No he tocado el arranque: es tu mano.
- **(M)** **El servidor es efímero y sin supervisión.** Vive atado a un terminal; ya murió y
  renació una vez a mitad de esta misión, matando una petición en curso. Mientras siga así,
  cualquier trabajo delegado puede perderse sin aviso. Una unidad de usuario que lo levante
  (propose-only, no la instalo) lo volvería reproducible.
- **(M)** **No delegues inventarios al local — empieza por lo que tiene gate.** Medido en A5: 20
  minutos, una pasada, y una respuesta **incorrecta con alta confianza** («no hay claves
  huérfanas» cuando 26 de 29 lo están), con tres ficheros reales citados como prueba de
  referencias que no existen. Y el gate habría dado **verde**, porque un inventario no toca
  código. El gate protege refactors, tests y diffs; no protege inventarios ni auditorías. La
  primera delegación real debería ser algo que `tsc` y los tests puedan desmentir.
- **(S)** **RAM y ventana: el margen es real pero frágil, y 32768 se queda corto.** Con el modelo
  residente quedan ~31.8 GiB de 57, y tres corridas costaron solo ~120 MiB — lo caro es tenerlo
  cargado (~30 GiB de RSS), no usarlo. Pero con escritorio activo el swap llegó a 6.4 GiB y
  MemAvailable bajó a ~17.8 GiB. Y el arnés se come el **69%** de la ventana (22.648 de 32.768) en
  una tarea trivial, porque manda ~78 KB de definiciones de herramientas por turno. El modelo da
  para más (`n_ctx_train` 262144); el techo lo pone la RAM, así que subir `-c` exige remedir.
  Nota aparte: el prefix caching está **confirmado** (`input_tokens` 32→1), o sea que hay caché
  real que perder — el footgun de `CLAUDE_CODE_ATTRIBUTION_HEADER` aplica aquí, y sigue sin
  activar según tu regla: solo si se mide degradación.

## Ronda BLOQUE 12 (cerebro local para el arnés) · 2026-08-04 — OBSOLETA en su mayor parte

Misión **abortada en A2**: el endpoint existe, el motor local no. Sugerencias (coste S/M/L):
- **(S)** **Decidir cuál de los dos Ollama manda.** Hoy conviven un `ollama serve` lanzado a mano
  bajo el usuario interactivo (es el que responde en loopback, y su almacén está **vacío**) y el
  servicio systemd —parado y `disabled` desde el 04-ago 02:06— que apunta al almacén del usuario de
  sistema, el que sí tenía modelos. Mientras haya dos, toda misión que dependa del motor local es
  una lotería según cuál esté vivo. Elegir uno, y que el otro no arranque.
- **(M)** **Reconstruir el motor local.** No existe manifest de `soberano-coder` en ningún almacén,
  ni la base `qwen3-coder:30b` que su Modelfile declara en el `FROM`; el único manifest superviviente
  es `qwen3:30b-a3b-instruct-2507-q4_K_M`. Reconstruirlo exige un pull de ~18GB. No lo he hecho: es
  mutación de estado no mandatada y sustituto silencioso de lo que la misión daba por existente.
- **(S)** **Revisar el `llama-server` huérfano.** Proceso ajeno a esta misión ocupando **35 GB RSS**
  (58% de la RAM), CPU puro (`-ngl 0`), lanzado desde un terminal el 04-ago 02:09. No lo he tocado
  (IronClaw). Mientras viva, ninguna medición de huella de RAM en este nodo es limpia.
- **(M)** **Ejecutar A2 de verdad** cuando el motor vuelva: huella, tok/s y tiempo de carga a 16384
  vs 32768, tres corridas, con `ollama ps` anotando backend CPU/GPU antes de empezar. Solo entonces
  crear la variante `soberano-coder-cc` con `num_ctx` elegido por dato. **No he creado la variante**:
  sin medición, elegir contexto sería un decreto por intuición, justo lo que la doctrina prohíbe.
- **(S)** **Bind del servicio.** El drop-in de systemd fija `OLLAMA_HOST` a la IP del tailnet, así que
  el servicio **no** escucha en loopback. `bin/cc-local` usa loopback por defecto e higiene dura (cero
  IPs versionadas): con el servicio activo hay que exportarle `P0X_OLLAMA_URL`. Valorar añadir bind de
  loopback para que el envoltorio funcione sin variable de entorno.
- **(S)** **A5 sigue pendiente**: smoke con las i18n huérfanas de Aurelius (Bloque 5.2) y comparación
  honesta contra el coste en frontera — incluido el caso incómodo de que el local necesite tres
  pasadas donde la frontera necesita una. Un ahorro que mueve el coste al tiempo del Soberano no es
  un ahorro, y hasta que se mida no sabemos cuál de los dos es.

## Ronda BLOQUE 13 (mapa tipado + bitácora) · 2026-08-04

Sugerencias accionables (coste S/M/L):
- **(✅ RESUELTO)** Paleta marítima: el Soberano decidió 5 familias visuales (no 8),
  con tokens EXISTENTES. HSC pasó a fila de tabla. Ver
  `propuestas/2026-08-04_paleta-maritima-blueprint.md`.
- **(S · opcional)** Formalizar en §2.2 del Blueprint la excepción declarada: los
  marcadores del Unified Map usan {vocero, amber, phosphor, danger, text-dim} como
  familias visuales (voz/danger como relleno, que §2.2 no contemplaba). Hoy es una
  desviación firmada; una línea en §2.2 la vuelve canon en vez de excepción.
- **(M)** Bitácora del día PERSISTENTE: hoy vive en memoria del cliente (se pierde al
  recargar; declarado honestamente). Moverla a redis con clave diaria + TTL a 00:00 local
  la haría sobrevivir a recargas/reinicios. Requiere ingesta/gateway en La Fragua → infra,
  propose-only (IronClaw): sale como artefacto, no se despliega desde aquí.
- **(M)** Refinar los rangos ICAO militares (`RANGOS_MIL_ICAO` en `tiposBuque.ts`): hoy
  es una heurística sembrada y NO exhaustiva (US/UK/FR). Contrastar con una tabla de
  asignaciones ICAO revisada antes de confiar en el MIL? de aeronaves. La doctrina (nunca
  afirmar, solo inferir con método) ya está; falta cobertura de rangos.

## Ronda METODO-1 (Fase 1 del Método Aurelius) · 2026-08-04

Contexto: se implantó la Fase 1 de `AURELIUS_METODO_v1.txt` en el repo `aurelius`
(auditoría de conformidad, el Anclaje, la advertencia eléctrica y sus tests). La
auditoría midió 28 mecanismos: **22 CUMPLE · 6 REESCRIBIBLE · 0 DESCARTAR**.

Sugerencias accionables (coste S/M/L):

- **(M)** **El Camino bloquea el avance, y eso contradice el contrato del Abecedario.**
  El hallazgo más serio de la auditoría, y está en dos capas: `_avanzar()` en el
  servidor sólo deja abierto el módulo actual, y `MissionStatus` admite `"locked"`
  como valor legítimo, así que el tipo permite expresar lo que la doctrina prohíbe
  (§2.2: «el sistema NUNCA bloquea el avance… el usuario es un adulto»). La
  conversión ya está escrita en `docs/AUDITORIA_METODO_v1.md`: marcar **sin base
  medida** y recordarlo al abrir, en vez de cerrar la puerta. Es el `[aur:moratoria]`
  del arsenal, vivo en el código.

- **(S)** **`camino.html` arrastra una copia inline de `camino.js`.** Casi 400 líneas
  duplicadas: la página standalone tiene su propia implementación y el drawer de la
  cara carga el módulo. Pueden divergir en silencio y nadie se enteraría hasta que
  las dos digan cosas distintas. El Anclaje se construyó evitando esto a propósito
  (una sola implementación, la página la carga). Arreglarlo es sustituir el bloque
  inline por un `<script src>`.

- **(S)** **Conectar la autodeclaración de nivel del onboarding con el Anclaje.**
  En M0 el usuario declara si es principiante/intermedio/avanzado y eso fija la
  profundidad para siempre, sin contrastarse jamás con nada. Es exactamente la
  mitad izquierda del Anclaje —una confianza declarada— recogida y tirada. Pasarla
  como primera entrada del registro no le pide nada nuevo al usuario y le devuelve,
  cuando haya cinco resultados, cuánto acertó al declararse.

- **(M)** **La advertencia eléctrica está construida pero no tiene tema al que
  engancharse.** El componente, el registro (`tema-2`, `tema-3`, `mision-2`) y el
  punto de montaje están listos; ningún tema existe todavía porque la Fase 1 no
  autoriza construirlos. Queda por decidir dos cosas cuando llegue el TEMA 2: si la
  vista genérica de tema llama a `montar()` siempre, y si conviene un check de CI
  que falle cuando un tema del registro se pinte sin advertencia. Hoy la garantía
  es arquitectónica (no hay interruptor); un check la volvería mecánica.

- **(S)** **Hay un test rojo que el CI no ve.** `movil.spec.ts:34` falla —la cara
  desborda 12 px en horizontal a 360 px— y falla igual en el HEAD anterior a esta
  ronda, así que es deuda previa, no regresión. Pasa desapercibido porque el
  workflow sólo corre `--project=escritorio-1280`. O se arregla el desbordamiento o
  se amplía el CI a un viewport móvil; dejarlo así es peor que las dos, porque el
  test existe y nadie lo mira.

- **(S · decisión del Soberano)** **Publicar o no el cementerio de archivados.**
  `ARSENALAURELIUS_SUGERENCIAS.txt` trae su propio PROMPT BLOQUEADO: la decisión de
  si el registro de los 31 descartados se publica es tuya y no está tomada. Está
  commiteado en `docs/` del repo público pero **sin push**, así que todavía no es
  público. El Preceptor recomienda publicarlo con la cabecera «REGISTRO DE
  ARCHIVADOS — NADA DE LO QUE SIGUE SE VA A CONSTRUIR» en la primera línea; esa
  cabecera **no** se ha añadido, porque la tarea prohibía reformatear los documentos.

## Backlog de UI/software (autoritativo)
El trabajo pendiente de **interfaz** (Hexelion · Aurelius · Le Jardin) vive en su
propio documento: **[`mente/backlog/BACKLOG_UI.md`](../backlog/BACKLOG_UI.md)**
(bloques atómicos 0–10, formato de reporte, invariantes). Este `PENDIENTES.md`
sigue siendo el registro de sugerencias/deuda general; el de UI se gestiona allí.

### 2026-08-08 · Cierre de CMP (Compose Multiplatform)

| # | Sugerencia | Coste | Estado |
|---|---|---|---|
| 175 | **CMP (Compose Multiplatform Desktop/JVM)** | M | **CANCELADO** |
| *Motivo:* Se canonizó un frente completo antes de escribir una línea de código. El coste fue una ronda de reconciliación. |
| *Lección:* No canonizar arquitectura sin experimento previo en disco. |
| *Reemplazo:* React 18 + Vite 6 declarado stack canónico único para dashboards. |

### 2026-08-09 · Ronda CARAS-PUBLICAS-1 (frenos de publicación)

Las cinco tareas de la ronda quedaron hechas. Lo que sigue es lo que la ronda
destapó y no le tocaba resolver.

- **(S · decisión del Soberano, y bloquea a las demás)** **El repositorio
  público sirve hoy el repo privado entero.** `piskyRpapalo/-hexelion-public`
  es PUBLIC y su `master` es la punta de `p0x`, `mente/` incluida; la cara
  sanitizada de 10 commits fue sustituida por empuje forzado y ya no existe
  como rama. Ninguna otra sugerencia de esta lista tiene sentido antes de
  decidir esto. Las opciones son tres y son excluyentes: pasar el repo a
  privado, republicar la cara sanitizada, o declarar la exposición aceptada.
  Medido en `mente/auditorias/RECONCILIACION_HEXELION_2026-08-09.md`.

- **(S)** **Separar los remotos de `p0x`.** El repo privado tiene `origin` **y**
  `github` apuntando a la misma URL pública, y ningún remoto al host git del
  rack — al contrario de lo que dice el canon («`p0x` empuja a la Torre»). Un
  `git push` sin argumentos publica. Reapuntar `origin` al rack y dejar el
  remoto público con un nombre que se lea como advertencia.

- **(M)** **Corrección hacia adelante de los 64 hallazgos publicados.** 29
  ficheros, sobre todo IPs de la red superpuesta (25) y rutas absolutas al
  directorio del usuario (24). Inventario con fichero y línea en
  `mente/auditorias/PUBLICADO_2026-08-09.md`. No se hizo aquí porque toca
  doctrina viva y esta ronda no construía. Depende de la decisión anterior:
  si el repo pasa a privado, baja de prioridad; si sigue público, es urgente.

- **(S)** **Retirar `mente/test_fuga.md`.** Un fichero de prueba con el nombre
  del nodo suelto, confirmado, deshecho y recolado por un `pull` la noche del
  8 al 9 de agosto. Está publicado y no sirve para nada: el corpus de pruebas
  del guardia vive ahora en `deploy/comun/hooks/test_guardia.py`.

- **(S)** **Enseñar al guardia a leer enlaces simbólicos.** Lee contenido, no
  `readlink`. `mente/codice/CODICE_david.md` apunta a una ruta absoluta de un
  nodo anterior, está roto, y esa ruta viaja publicada sin que ninguna regla
  la vea.

- **(M)** **Llevar el guardia a CI.** El gancho vive en `.git/hooks/`, no se
  clona, y `--no-verify` no deja rastro. Un job que ejecute
  `guardia_higiene.py --files` sobre el árbol completo en cada push al
  repositorio público convierte el freno en algo que no depende de que la
  máquina de turno lo tenga instalado.

### 2026-08-10 · Descarte firmado · MCP de GitHub

- **DESCARTADO por firma del Soberano, 2026-08-10.** **No se instala el MCP de
  GitHub**, ni con token de solo lectura. Motivo: `mente/EQUIPO_AI_LOOP.md` §1
  declara que el Ejecutor no puede empujar, y que ese límite es mecánico — «no
  puede empujar porque el sistema no le deja, no porque se lo pidieran
  amablemente». Un servidor MCP de GitHub le daría una vía de escritura al
  remoto que **no pasa por `git push`** y que por tanto los ganchos no frenan.
  Es doctrina, no preferencia: no se reabre sin enmienda de §1. El resto de la
  ronda MCP-1 queda en `deploy/soberano/MCP.md`.

### 2026-08-16 · Cierre técnico de aurelius-mvp · sugerencias

Misión: PASO 1–6 del cierre técnico (`guardar_perfil`, `EXCEPCIONES.md`,
`LIMITES_DEL_CRITERIO.md`, intérprete en la cabecera, rango de Python, push).
Resultado: VERDE 224/224 en 3.14.4 y en 3.10.12, empujado a `origin/main`
(`5a86cc6`). Estado de las seis: **ABIERTAS**.

- **S1 · La corrección del PASO 1 es preventiva, no reparadora. Que conste en
  el acta antes de que se cuente al revés.** (Coste S.) `profile` tiene hoy
  exactamente tres columnas — `key`, `value`, `updated_at` — y el
  `INSERT OR REPLACE` de `fuga.py:802` las nombraba **las tres**. Medido: hoy
  no perdía ningún dato. Lo que se arregló es que dejara de haber dos
  escritores y que la sentencia siga siendo correcta el día que `profile` gane
  una columna; el caso 22 simula ese día con una columna `extra`. Sostener
  «se corrigió una pérdida de datos» sería afirmar más de lo que la sección
  sostiene.

- **S2 · `aurelius.py` no lo importa ninguna suite.** (Coste M.) Son 21 KB y
  es el punto de entrada del producto — `main()`, `arranque()`, `sesion()`,
  `ofrecer_m3()` —, y hasta esta misión **cero** ficheros de prueba lo
  importaban (`grep -l "import aurelius" test_*.py` daba vacío).
  `test_interprete.py` es lo primero que lo arranca, y solo como subproceso y
  solo para `--view`. Encaja con el PROMPT 2 de la cola pero es más agudo: no
  es que las suites fabriquen el dato, es que ahí no hay suite.

- **S3 · Medir 3.11, 3.12 y 3.13 y convertir el intervalo en puntos.**
  (Coste S.) El README declara hoy dos medidas reales y dice explícitamente
  que lo de en medio se infiere. Con `uv` instalado eso deja de costar nada:
  `uv python install 3.12.x` y la tanda con un shim de `PATH` — así se hizo
  la medida de 3.10.12 de esta misión, en menos de dos minutos y sin sudo.
  Tres puntos más y el intervalo deja de ser una inferencia.

- **S4 · El inventario que planifica una misión se verifica con `git grep`
  antes de firmarla.** (Coste S.) §2 del artefacto de cola daba
  `guardar_perfil` como inexistente — correcto — pero el PASO 1 añadía que
  «`memory.py` tiene `leer_perfil` y no tiene su pareja». La pareja existía:
  `escribir_perfil`, en `memory.py:237`, ya con `ON CONFLICT`, con más de 20
  llamantes. Ejecutar el PASO 1 al pie de la letra habría creado un segundo
  escritor con la misma semántica y otro nombre, que es peor que el problema
  que venía a resolver. Es la misma clase de error que la cicatriz de las
  claves relayadas: un dato del árbol que pasa por un resumen intermedio.

- **S5 · La cifra del README se puede quedar vieja en silencio.** (Coste S.)
  Decía `12/12 tests green` para una suite que llevaba 24 casos, y `217` para
  un árbol que ya iba por otro número. Se corrigieron a mano en esta misión;
  a mano se volverán a quedar viejas. `bin/pruebas` ya imprime el total: un
  modo `--comprobar-readme` que compare el total impreso con el que afirma el
  README, y falle si divergen, cierra la vía.

- **S6 · Las anclas de sabotaje acoplan las suites a líneas exactas del
  producto.** (Coste S.) Editar `fuga._volcar_pendiente` estuvo a punto de
  invalidar un ancla de `test_fuga.py`. **El mecanismo aguantó** — verifica
  que el ancla aparezca una vez y rechaza el sabotaje si no —, así que esto
  no es un fallo abierto sino un coste de mantenimiento que conviene tener
  contado antes de que sean veinte anclas en vez de diez.

## Misión · Dashboard local de Aurelius (PyWebView) · 2026-08-16

- **S1 · El gerente `aurelius-m1/aurelius` tiene tres rutas viejas cableadas a
  `$HOME`.** (Coste S.) `llama-cli`, el `.gguf` y `ARQUETIPO.md` se mudaron
  dentro del repo privado y el wrapper se quedó apuntando al home. Invocado a
  mano moría con `FileNotFoundError` antes de generar un token; el dashboard lo
  sortea dándole su propio `HOME`, y se pusieron dos enlaces para la vía CLI.
  Son dos parches para un literal: la corrección de verdad es un `RAIZ`
  configurable en el wrapper. Mientras no se haga, cualquier tercer llamante
  vuelve a tropezar con lo mismo.

- **S2 · La cara habla por `fetch` con un servidor que en local no existe.**
  (Coste M.) `aurelius_face.html` fue escrita contra `:8050` + ollama: cinco
  rutas `/api/*` y los `.json` de config. El dashboard las reconduce con un
  *user script*, que funciona pero es un doble de un contrato que nadie ha
  escrito. Si la cara va a tener dos transportes —servidor y proceso—, merece
  una capa de transporte declarada en un sitio, y no un shim que persigue por
  detrás cada `fetch` nuevo que se añada.

- **S3 · `lsof -i -p <pid>` sin `-a` no comprueba lo que parece.** (Coste S.)
  Los filtros de `lsof` se combinan con OR: el comando de verificación de D75
  lista los sockets de toda la máquina y da por «violado» un proceso que no
  tiene ninguno. Aquí salieron firefox, open-webui y el propio agente. Todo
  guion de verificación de D75 que ande por el repo debería llevar `-a`, y
  conviene comprobar los que ya existen.

- **S4 · `about:blank` levanta un servidor HTTP en pywebview.** (Coste S.)
  `is_local_url()` lo trata como url local y arranca el servidor interno en
  `:42001` — un `LISTEN` real, D75 roto sin que nadie lo pida. `file://` está
  excluido y no lo dispara. Queda anotado como footgun del arnés, no del
  código: cualquier futura ventana PyWebView en el rack debe nacer con `html=`
  o con `file://`, nunca con `about:blank`.

- **S5 · La Fetch API no lee `file://`, y el ajuste que parece cubrirlo no lo
  cubre.** (Coste S.) `ALLOW_FILE_URLS` mapea a `allow_file_access_from_file_urls`,
  que vale para XHR y no para `fetch()`. El síntoma fue mudo y caro de leer: la
  cara pintaba «point Aurelius at your model» con el modelo respondiendo a su
  lado, porque `cargarConfig()` fallaba en silencio y caía al literal de último
  recurso. Cualquier página servida por `file://` en el rack tiene este agujero.

- **S6 · `models.json` quedó modificado en el repo público y sin commit.**
  (Coste S.) El `default` pasó al 4B y se añadió su entrada, con los números
  medidos en este nodo (2.33 GB reales, no los 2.5 estimados). Es un cambio al
  producto público decidido desde una misión del canon privado: necesita commit
  propio en `aurelius`, en su rama, con el criterio de `hardware_verified` del
  propio manifiesto revisado — el 30B sigue marcado `true` y ya no es el default.

### 2026-08-17 · P3 · SECURITY.md y descubribilidad del repo público · sugerencias

- **S1 · El repo `piskyRpapalo/aurelius` está publicado sin `description` ni
  `topics`.** (Coste S.) Medido con `gh repo view --json description,repositoryTopics`:
  `description` es cadena vacía, `repositoryTopics` es `null`, `homepageUrl` vacío.
  Un repo así no aparece en la búsqueda de GitHub por tema ni en los listados de
  lenguaje: solo lo encuentra quien ya conoce la URL. Es el freno de publicación
  más barato de quitar del backlog. **No se ha cambiado** — la misión pedía solo
  reporte.

- **S2 · `SECURITY.md` promete plazos que nadie vigila.** (Coste S.) El fichero
  compromete acuse en 7 días, valoración en 14 y arreglo en 90. No hay ningún
  filtro, etiqueta ni recordatorio sobre `davidpecero@gmail.com` que haga sonar
  esos relojes. Una promesa de seguridad incumplida es peor que no tenerla:
  autoriza al que reporta a publicar sin esperar, y así está escrito en el propio
  fichero.

- **S3 · No hay canal cifrado publicado para reportes.** (Coste M.) `SECURITY.md`
  dice «si quieres cifrado, escríbelo en claro y lo acordamos», que es un
  compromiso honesto pero obliga al reportante a mandar el primer contacto en
  claro. Publicar una clave pública (o activar *private vulnerability reporting*
  de GitHub, que es coste S y no necesita clave) cierra el hueco.

- **S4 · El alcance declarado nombra superficies que nadie ha auditado.**
  (Coste L.) El fichero pone dentro de alcance la censura en la frontera
  (`--export`), la descarga del cerebro/voz del primer arranque y el HTML
  generado por `cara.py`. Declarar alcance no es haberlo revisado: convendría una
  pasada propia sobre esos tres puntos —integridad verificada de la descarga,
  inyección en `cara.html`, fugas en el export— antes de que la encuentre un
  tercero.

- **S5 · Dos commits ajenos aterrizaron en `main` durante esta misión.**
  (Coste S.) Entre la lectura inicial del repo y el commit de `SECURITY.md`
  entraron `6a921c0` (descarga desde unsloth) y `131a48b` (README del MVP v1)
  desde otra sesión. No hubo conflicto y `SECURITY.md` va solo en su commit, pero
  dos sesiones escribiendo a la vez sobre `main` del repo público es una colisión
  que la próxima vez puede no ser limpia. Falta convención de bloqueo o de rama
  por misión.

## Sugerencias de la misión P1 (README del MVP v1) · 2026-08-17

| # | Sugerencia | Coste |
|---|-----------|-------|
| S1 | Cablear la fila llama-cli del README o marcarla "coming soon". La verificación muestra cero referencias a `llama-cli` en el árbol (no a "llama", que sí aparece 59 veces en español: «se calcula al llamar», «el código no llama a hash»). El README insinúa una conversación con el modelo que el árbol todavía no puede sostener. | S |
| S2 | `test_memory.py` (25/25) y el total del árbol (225/225, `bin/pruebas`, 13 suites) conviven en la misma sección del README. Un lector rápido lee dos verdades y sospecha de ambas. Una línea que las relacione lo arregla. | S |
| S3 | El README es bilingüe de facto (cuerpo inglés, `## Verificación` español). O se parte en README.md / README.es.md, o se asume la mezcla explícitamente — hoy parece un descuido y no lo es. | M |
| S4 | Medir la conversación cuando llama-cli exista, en la máquina del Soberano y con `ollama ps` anotado, para que la primera cifra de latencia que entre al README nazca con fuente. | M |
| S5 | Añadir una fila más a la tabla de intérpretes desde una segunda máquina física. Hoy cuatro de las seis filas comparten hardware, y el README ya lo confiesa — cerrar la confesión vale más que ampliarla. | L |
| S6 | Patrón de verificación: el hallazgo original verificó "cero referencias a llama" con un grep en inglés sobre un corpus comentado en español, y el comando citado devolvía 59, no 0 — la conclusión era correcta por accidente. Verificar en un idioma lo que está escrito en otro ya tiene cicatriz en este nodo (las claves relayadas). Documentar la lección. | S |

Corrección declarada sobre el encargo: S2 llegaba como «`test_descarga.py` (225)». Es falso —
`test_descarga.py` tiene 18 pruebas; las 225 son del árbol entero vía `bin/pruebas` (README:154-158,
13 suites). Se anexa el dato medido, no el recibido: este fichero es memoria, y una cifra con la
fuente equivocada envenena la siguiente misión que la lea.

### 2026-08-19 · Patrón de verificación · lo que un test mide de verdad

**Un test que se rompe cuando el código mejora medía la forma, no la propiedad.**

Cicatriz concreta: el caso 14 de `test_cara.py` («en instalación limpia el Camino está a cero
y no finge progreso») comparaba el **dict entero** de cifras contra
`{"perfil": 0, "recuerdos": 0, "sello": False}`. Al hacer medibles las side quests M3–M6, el
diccionario ganó cuatro contadores legítimos —salas, huellas, senderos, cicatrices— y el caso
se puso rojo. El código había mejorado y la prueba lo llamó fallo.

Lo que el caso quería sostener era *«en limpio, ningún contador miente»*. Eso se comprueba
recorriendo los valores, no fijando las claves. Reescrito así, admite contadores nuevos y
además vigila algo que antes no miraba: que ningún peldaño sea obligatorio y opcional a la vez.

**Cómo se reconoce el fallo antes de cometerlo:** si la aserción cita una estructura completa
—un dict, una lista ordenada, una cadena entera— probablemente está midiendo la forma. La
pregunta que lo desarma es *¿qué frase en castellano quiero que siga siendo verdad?*, y luego
comprobar esa frase. `assertEqual(cifras, {...})` no es una frase; «ningún contador miente en
limpio» sí.

Hermano del patrón #S6 del 2026-08-17 (verificar en un idioma lo que está escrito en otro): en
los dos casos la prueba pasaba o fallaba por una razón distinta de la que decía su nombre.

### 2026-08-20 · Cierre del sprint B5/B7 en el Doogee · sugerencias

Sesión de frontera sobre `aurelius` en `de6577d`. Línea base **344 pruebas / 26 suites**,
verde. B5 y B7 cerrados por el Soberano; B6 queda en `NO_DATA` (su definición nunca llegó a
la sesión). Las licencias se resuelven en el paquete posterior, por decisión del Soberano —
no se anexan aquí como pendiente sino como dato de estado.

- **S1 · Cada turno de `--charla` recarga el modelo entero.** (Coste M.) Medido en el Doogee
  S110 sobre `de6577d`: turno 1 **379,0 s**, turno 2 **326,4 s**. El segundo no fue más barato
  que el primero, así que no hay ventaja de caliente: `llama-completion` se lanza como hijo en
  cada turno y paga los 2,3 GiB cada vez. El segundo turno costó cinco minutos y medio para
  devolver tres palabras («¿Qué instalaste?»). Si el motor puede quedarse residente entre
  turnos, el producto cambia de categoría; si no puede, la promesa pública tiene que decir
  minutos y no tok/s.

- **S2 · Falta la cifra que siente la persona.** (Coste S.) `conversacion.py` documenta
  `2,93 ± 0,38 tok/s` de generación en este teléfono. Esa cifra describe el motor; la que
  describe la experiencia es **5,4–6,3 min por turno**, y hoy no está escrita en ningún sitio
  del árbol. Anexarla junto a la otra, con su máquina, como manda la casa.

- **S3 · `bin/pruebas` corre 13 de las 26 suites y dice `VERDE 241/241`.** (Coste M.) Las
  otras 13 —`andamio`, `borradores`, `conversacion`, `costura`, `frontera`, `fusible`,
  `hilos`, `identidad`, `narrador`, `puente`, `puerta`, `recuperacion`, `traza`— suman **103
  pruebas que ese corredor no ve**. 241 + 103 = 344. Un corredor que canta verde sobre el 70 %
  del árbol es peor que no tenerlo, porque da permiso para no mirar. O se completan las suites,
  o `bin/pruebas` imprime en rojo cuántas deja fuera.

- **S4 · Instrumentos: un proceso zombi se queda el puerto y el nuevo muere en silencio.**
  (Coste S.) Ocurrió **dos veces en una sola sesión**, en los dos extremos del túnel: el oyente
  de `eco-remoto` en 8900 (el eco del teléfono se escribió en el fichero de una sesión anterior,
  y el registro nuevo salió vacío pese a que el teléfono decía «enviado»), y el puente en 8734
  del propio Doogee (arrancado en otra sesión con `--cara` relativo, devolvía `500
  FileNotFoundError` mientras el mío moría sin poder atarse). En los dos casos el síntoma
  mintió: parecía un fallo del producto y era un cadáver ocupando el puerto. Los instrumentos
  deberían morir ruidosamente al no poder atarse, no en `/dev/null`.

- **S5 · `adb input text` no acepta acentos.** (Coste S.) Un solo carácter acentuado lanza
  `NullPointerException` en `InputShellCommand.sendText` y **no teclea nada** — el fallo es
  limpio, pero solo si se comprueba después. Hermano de la cicatriz de las claves relayadas: el
  canal intermedio corrompe lo que pasa por él. Documentar junto a las tres trampas de adb.

- **S6 · Voseo en una sesión declarada `es`.** (Coste S.) La primera respuesta que un
  desconocido recibió del producto fue «¿Qué **querés** saber primero?». El idioma se eligió
  como español y el registro salió rioplatense. No es un fallo de corrección, es un fallo de
  quién parece estar hablando.

Corrección declarada sobre la herencia recibida: llegaba como «el Doogee tiene el producto
instalado, el cerebro verificado y la voz, **con memoria recién nacida**». Falso — la memoria
**no existía**: el primer arranque estaba detenido en la pregunta de idioma y `~/.aurelius/`
estaba vacío. Se creó en esta sesión. Se anexa el dato medido, no el recibido.

### 2026-08-21 · adb · trampa nº4, con incidente

- **S1 · `input text` con comillas anidadas abre el selector de ficheros del
  sistema.** (Coste S.) Cuarta trampa de adb, y la primera que expone datos
  ajenos al trabajo. Al intentar enviar un `python3 -c "..."` con comillas
  escapadas a Termux, el escapado se rompió y Android abrió
  `com.google.android.documentsui` con documentos personales del Soberano en
  pantalla — una factura y un pedido. No se abrió ninguno, no se exploró, se
  retrocedió, se trajo Termux al frente y **se borraron las capturas que los
  contenían**. `KEYCODE_BACK` no cerró el selector; lo que funcionó fue lanzar
  Termux con `monkey`. **Regla: nada de comillas anidadas por `input text`.** Lo
  que no quepa en una línea sin comillas se escribe a fichero y se ejecuta por
  nombre, o no se envía.

## 2026-08-23 · Verificación del plan v1.1 (informe: INFORME_VERIFICACION_v11.md)

- (S) Firmar el orden nuevo: historial del tablero (B.1) ANTES de toda la Fase A.
- (S) `--modelo` en `aurelius.py --charla` — 1 h, desbloquea el 30B en el Beelink.
- (S) Reescribir el §II del plan: el intent de Termux NO puede ejecutar comandos desde
  el navegador (Chrome no tiene `com.termux.permission.RUN_COMMAND`). Camino real:
  abrir Termux con MAIN/LAUNCHER + comando al portapapeles.
- (M) Taller Nivel 1 con `--json-schema`: medido viable en Beelink (10 s) y Doogee (2m13s).
  Sin reintentos ni prompt-hack.
- (M) `PRAGMA user_version` con pruebas de migración sobre copias reales de memoria.
- (L) Retirar A.4 (pathlib) o degradarlo: 335 usos en 43 ficheros, beneficio estético.
- Decisión pendiente del Soberano: tag `v1.0.0` (no creado) y si el reparto
  gratis/pago se publica o se queda en la forja.

## 2026-08-24 · Verificación cruzada de v3.1 (docs en `aurelius-internal/docs/`)

- **S1 · El guardián de higiene no está instalado en `aurelius-internal`.** (Coste S.) Es el
  repo que **sí está en GitHub** y el que más documentación de infraestructura contiene
  (nodos, puertos, rutas del Faro). `p0x` sí lo tiene y esta misma sesión lo comprobó en
  carne propia: bloqueó dos veces la propuesta del Faro por IPs de tailnet y por `host:puerto`.
  El repo protegido es el que no se publica; el publicado va desnudo. `bin/p0x-instalar-ganchos`
  ya existe.

- **S2 · Tres clones de `aurelius` con tres HEAD distintos, y dos arrastran el blob.**
  (Coste M.) `~/p0x/aurelius` está limpio en `4f2f64e`; `~/p0x/aurelius-mvp` tiene `main`
  clavada en `0fb9784` (ahead 60/behind 60, `.git` 36 MB) y el Doogee está en `0fb9784` con
  `ashly_zhao.md` de 3.541.100 bytes vivo en su pack. **Un `push` desde cualquiera de los dos
  resucita la línea entera** y deja el ticket a GitHub Support en papel mojado. La purga
  remota no vale mientras haya quien reponga el objeto.

- **S3 · La regla de higiene systemd sigue sin llegar al repo.** (Coste S.) *«no se crean
  servicios systemd sin aprobación explícita del Soberano»* + *«`systemctl list-units` al
  cerrar cada sesión»* está en el archivo, citada por `ARQ_LOOPS.md`, y no está ni en
  `CLAUDE.md` ni en `mente/`. Esta sesión recibió orden de cronificar siete bucles «porque es
  mecánico» y paró por leer `ARQ_LOOPS.md`, no por leer la doctrina. La próxima puede no
  leerlo.

- **S4 · `bin/pruebas` sigue certificando el 73 % del árbol.** (Coste M.) Medido hoy: 282/282
  en 17 suites, y 103 pruebas más en las 13 que el corredor no declara. Total real **385/385
  en 30 suites**. La deuda S3 del 2026-08-21 no ha cambiado de fondo, solo de numerador
  (241 → 282). O se completan las suites, o el corredor imprime en rojo cuántas deja fuera.

- **S5 · Una crítica del Preceptor entró como enmienda sin comprobarse contra el código.**
  (Coste S.) «La tabla `hilos` no existe» era falsa (`memory.py:111` y `:117`, con
  `test_hilos.py` en verde) y v3.1 la aceptó sin abrir el fichero. **Un documento que corrige
  hacia el error es peor que uno que calla.** Regla que se propone: ninguna enmienda de
  inventario se firma sin el `grep` que la sostiene, pegado al lado.

- **S6 · `aurelius-internal/` figura como `??` sin seguimiento dentro de `p0x`.** (Coste S.)
  Es el mismo pie del que salió `9368dc8 chore: sacar el gitlink accidental de aurelius/`.
  Merece decisión explícita —`.gitignore` o submódulo— antes de que un `git add -A` lo
  resuelva por su cuenta.
