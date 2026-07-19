---
origen: archivo-historico
titulo: Índice del yacimiento — pre-bee/p0x
tipo: indice-arqueologico
clase: no-canon
generado_por: Claude Code (soberano)
fecha_generacion: 2026-07-19
fuente_original: /home/pisky/pre-bee/p0x/ (solo-lectura, no tocada)
nota: >
  Este documento es arqueología: material de referencia sobre CÓMO se llegó al sistema
  actual, no QUÉ es el sistema hoy. Nada de aquí es canon. Ninguna decisión vieja
  revertida debe leerse como vigente. El canon vive en mente/ del repo p0x/hexelion.
---

# ÍNDICE DEL YACIMIENTO — `pre-bee/p0x/`
### Micro-misión El Yacimiento · 2026-07-19 · Claude Code en `soberano`

---

## Resumen

- **376 archivos**, 84MB, en `/home/pisky/pre-bee/p0x/` (7 subcarpetas: `MD 3/`, `Nexo/`, `P0X/`,
  `p0x2/`, `propuesta/`, `hexelion-lab/`, más sueltos en la raíz).
- **La carpeta no se tocó**: ni se movió, ni se borró, ni se reorganizó nada del original. Todo
  el trabajo de esta micro-misión fue lectura + este índice.
- **3 archivos excluidos por datos personales** (§ Excluidos abajo) — no se leyeron más allá de
  lo mínimo para identificarlos con `file`, no se indexó su contenido.
- **9 ZIPs truncados/corruptos** (cabecera válida, sin directorio central) — listados con su
  motivo, no se intentó repararlos.
- `MD 3/` es, de lejos, el bloque más grande (~230 archivos): parece ser un **volcado único de
  todo el proyecto extraído el 2026-07-11** (esa es la fecha de `mtime` de casi todos sus
  archivos, incluidos documentos cuyo contenido/nombre indica fechas mucho más tempranas — mayo
  2026). El `mtime` de `MD 3/` es la fecha de extracción/copia, **no** la fecha real del
  documento; para esos casos, la fecha real (cuando se puede inferir) es la del nombre del
  archivo o su contenido, no el `mtime`.
- Un lote de ~43 archivos en la raíz tiene `mtime` **2026-07-19 (hoy)** — es cuándo se copiaron a
  esta carpeta, no su fecha de origen. La mayoría son legítimos y legibles (`file` confirma
  dimensiones/estructura real pese a tamaños idénticos/redondos — un artefacto del método de
  copia, no corrupción); la excepción real son los ZIPs de ese mismo lote, que sí están truncados.

## Excluidos — personales, fuera del corpus

Por la regla dura del invariante #3. Solo el nombre; no se indexó ni se citó su contenido.

- `CV_David_Pecero.docx` (raíz)
- `MD 3/CV_David_Pecero.docx` (copia duplicada, dentro del volcado del 11-jul)
- `Fixed_Term_Local_David_Pecero_Caballero.pdf` (raíz — contrato laboral)

Nota aparte (no excluido, verificado que NO es personal): `MD 3/HEXELION_BITACORA_SESION.docx`
suena a diario personal por el nombre, pero su contenido es una bitácora **técnica** de sesión
(diseño del mapa marítimo, mayo 2026) — es material de proyecto, se indexa normal más abajo.

## ZIPs truncados/corruptos (no reparados)

Cabecera `PK\x03\x04` válida pero sin directorio central al final (`unzip` no puede listarlos).
Dos son truncamientos de tamaño real (probablemente una copia interrumpida); siete son del lote
de hoy con tamaño exactamente redondo — casi seguro la misma causa.

| Archivo | Tamaño | mtime | Nota |
|---|---|---|---|
| `Nexo/nexo.zip` | 4,771,677B | 2026-06-08 | Empieza con `nexo-final.html` legible en los primeros bytes; el resto, inaccesible sin reparar. |
| `Nexo/files.zip` | 3,948,544B | 2026-07-19 | Igual patrón que el anterior. |
| `19.05.zip` | 8,192B | 2026-07-19 | — |
| `HEXELION_NEXUS_FILL_20260519.zip` (raíz) | 8,192B | 2026-07-19 | Su copia buena vive en `MD 3/HEXELION_NEXUS_FILL_20260519.zip` (277,138B, sí legible — ver Códice más abajo). |
| `Nexo/nexo+maritimo+aereo.zip` | 8,192B | 2026-07-19 | — |
| `files.zip` (raíz) | 8,192B | 2026-07-19 | — |
| `files222.zip` | 8,192B | 2026-07-19 | — |
| `hexelion.zip` | 8,192B | 2026-07-19 | — |
| `hexelion_dashboard_v2_assets.zip` (raíz) | 8,192B | 2026-07-19 | Su copia buena vive en `MD 3/hexelion_dashboard_v2_assets.zip` (901,704B, sí legible — ver Bloque B). |

## ZIPs con contenido legible (fuera de los de dashboard, ver Bloque B)

| Archivo | mtime | Contenido |
|---|---|---|
| `P0X.zip` | 2026-06-26 | 4 archivos: `INSTRUCCIONES_P0X.md`, `00_CONSTITUCION_P0X.md`, `CORPUS_Psicologia_y_Motor-Metodo_P0X.md`, `CODICE_SUGERENCIA_P0X.md` — bundle de doctrina temprana de P0X, previo a la constitución actual. |
| `p0x2.zip` | 2026-06-27 | 5 archivos: `bootstrap_p0x.sh`, `CODICE_david.md`, `models.py`, `litellm_config.yaml`, `p0x-enqueue` — un segundo intento de bootstrap técnico (litellm en vez de Ollama directo — decisión que no llegó al sistema vivo). |
| `hexelion-lab/files.zip` | 2026-06-04 | `00_CONSTITUCION_Y_ADN.md`, `02_LEXICO_Y_MAQUINA.md` — constitución temprana de "hexelion-lab", la rama exploratoria mencionada en `doctrina-ai-interna` como precursora fusionada. |
| `MD 3/hexelion_v6_assets.zip` | 2026-07-11 | Bundle de backend real: `hexelion_pollers.py` (pollers asyncio de los 6 nodos) + `hexelion-pollers.service` — antecesor directo de `hexelion_pollers.py` que hoy vive en el repo `hexelion` real. |
| `MD 3/hexelion_smc_deploy.zip` | 2026-07-11 | Despliegue para el-vigía (RPi5): `docker-compose.yml`, `defli_forwarder.py`, `sensor_bridge.py`, `mosquitto.conf`, config de Arkreen — rama DePIN/SMC que no parece haber prosperado (sin equivalente vivo hoy). |
| `MD 3/HEXELION_NEXUS_FILL_20260519.zip` | 2026-07-11 | Bundle "01_Codice" con `HEXELION_AI_IDENTITY.md`, `HEXELION_PROTOCOLO.md`, `HEXELION_DOCTRINA_SOL_SINCRONO.md`, `HEXELION_LORE_LA_CRISALIDA.md`, y una subcarpeta `deprecated/` con versiones previas del Códice Maestro (v8, v12) — el propio archivo ya marcaba esas versiones como obsoletas en mayo. |

## Doctrina/constitución histórica (21 archivos)

Múltiples generaciones de constituciones/instrucciones — nombres muy parecidos a los canónicos de
hoy (`INSTRUCCIONES_P0X.md`, `DOCTRINA_AI_INTERNA_P0X.md`, `ALFABETO_P0X.md`, etc.), pero son
**versiones anteriores**, no el canon vigente. La versión con `_v1` o fecha en el nombre suele ser
la más vieja; compárese solo por curiosidad histórica, nunca como fuente de verdad.

| Fecha (mtime) | Archivo | Tamaño |
|---|---|---|
| 2026-06-16 | `CONSTITUCION_Cuatro-Esferas_IronClaw-matiz_2026-06-16.md` | 7,690 |
| 2026-06-26 | `P0X/INSTRUCCIONES_P0X.md` | 5,805 |
| 2026-06-26 | `P0X/00_CONSTITUCION_P0X.md` | 11,681 |
| 2026-07-11 | `MD 3/ORQUESTA_MODELOS_P0X.md` | 5,364 |
| 2026-07-11 | `MD 3/DOCTRINA_Hexelion-Hibrido_2026-06-07.md` | 5,429 |
| 2026-07-11 | `MD 3/DISCURSO_FUNDACIONAL_P0X.md` | 5,781 |
| 2026-07-11 | `MD 3/INSTRUCCIONES_P0X.md` | 5,805 |
| 2026-07-11 | `MD 3/INSTRUCCIONES_PROYECTO_hexelion-lab.md` | 6,063 |
| 2026-07-11 | `MD 3/CAMINO_NEARAI_P0X.md` | 6,136 |
| 2026-07-11 | `MD 3/PROCESO_EVALES_TRANSPLANTE_P0X.md` | 6,181 |
| 2026-07-11 | `MD 3/PROTOCOLO_MD_EVOLUTIVO_P0X.md` | 6,257 |
| 2026-07-11 | `MD 3/DOCTRINA_AI_INTERNA_P0X.md` | 6,961 |
| 2026-07-11 | `MD 3/MANUAL_DEL_SOBERANO_P0X.md` | 7,159 |
| 2026-07-11 | `MD 3/ALFABETO_P0X.md` | 7,214 |
| 2026-07-11 | `MD 3/PROYECTO_REFLEJOS_P0X.md` | 7,232 |
| 2026-07-11 | `MD 3/INSTRUCCIONES_El-Preceptor.md` | 7,453 |
| 2026-07-11 | `MD 3/CONSTITUCION_Cuatro-Esferas_IronClaw-matiz_2026-06-16.md` | 7,690 |
| 2026-07-11 | `MD 3/INSTRUCCIONES_P0X_v1.md` | 8,806 |
| 2026-07-11 | `MD 3/00_CONSTITUCION_LAB.md` | 9,416 |
| 2026-07-11 | `MD 3/00_CONSTITUCION_Y_ADN.md` | 11,574 |
| 2026-07-11 | `MD 3/00_CONSTITUCION_P0X.md` | 11,681 |

**Hallazgo notable — evolución del Códice Maestro**: `MD 3/` contiene `HEXELION_CODICE_2026_8_MAESTRO.md`,
`HEXELION_CODICE_2026_12_MAESTRO.md` (+ duplicado `-1`), y `HEXELION_CODICE_2026_14_MAESTRO.md` —
tres generaciones numeradas del mismo documento maestro (8→12→14), más
`HEXELION_CODICE_2026.15_ADDENDUM_ENERGETICO.md` como parche a la 14/15. El ZIP
`HEXELION_NEXUS_FILL_20260519.zip` ya archivaba las versiones 8 y 12 en su propia carpeta
`deprecated/` desde mayo — la propia arqueología se auto-documentó en su momento.

## Sesiones y estado histórico (13 archivos)

| Fecha (mtime) | Archivo | Tamaño |
|---|---|---|
| 2026-05-11 | `HEXELION_SESION_20260511.md` | 7,174 |
| 2026-05-17 | `HEXELION_TAREAS_20260517.md` | 7,292 |
| 2026-07-11 | `MD 3/HEXELION_SESION_20260504_VISION.md` | 5,005 |
| 2026-07-11 | `MD 3/HEXELION_DRILL_LOG.md` | 5,210 |
| 2026-07-11 | `MD 3/HEXELION_SESION_20260503_DESPLIEGUE.md` | 6,009 |
| 2026-07-11 | `MD 3/ESTADO_SISTEMA_2026-06-05_hexelion-lab.md` | 7,097 |
| 2026-07-11 | `MD 3/HEXELION_SESION_20260511.md` | 7,174 |
| 2026-07-11 | `MD 3/HEXELION_TAREAS_20260517.md` | 7,292 |
| 2026-07-11 | `MD 3/HEXELION_BACKLOG_TODO.md` | 8,583 |
| 2026-07-11 | `MD 3/HEXELION_SESION_20260502.md` | 9,927 |
| 2026-07-11 | `MD 3/HEXELION_ESTADO_ACTUAL_20260601.md` | 12,686 |
| 2026-07-11 | `MD 3/HEXELION_SESION_20260510.md` | 12,694 |
| 2026-07-11 | `MD 3/HEXELION_ESTADO_20260509.md` | 13,792 |

## Prompts históricos a Claude Code / agentes (69 archivos)

Casi todos en `MD 3/`, `mtime` 2026-07-11 (fecha de extracción). Lista compacta — cada uno es un
prompt de misión de una sesión pasada, mismo patrón que las misiones actuales pero de generaciones
anteriores de doctrina:

`PROMPTS_CLAUDE_CODE_reparaciones-chat-y-ADSB.md` · `PROMPT_Auditoria-Nodos_LaTorre-ElVigia-LaLegion.md`
· `PROMPT_CLAUDE_CODE_ALMA_SINODO.md` · `PROMPT_CLAUDE_CODE_BLOQUE1_SEGURIDAD.md` ·
`PROMPT_CLAUDE_CODE_BLOQUE2_DASHBOARD.md` · `PROMPT_CLAUDE_CODE_ED25519_Y_PRIVACIDAD.md` ·
`PROMPT_CLAUDE_CODE_ESCAPARATE.md` · `PROMPT_CLAUDE_CODE_FARO_DURABILIDAD.md` ·
`PROMPT_CLAUDE_CODE_FARO_MCP.md` · `PROMPT_CLAUDE_CODE_FARO_P2_ANCLAJE.md` ·
`PROMPT_CLAUDE_CODE_FARO_P3_CREDITOS_402.md` · `PROMPT_CLAUDE_CODE_FARO_V1_BUILD.md` ·
`PROMPT_CLAUDE_CODE_FASE1_FARO.md` · `PROMPT_CLAUDE_CODE_FASE2_FLYWHEEL.md` ·
`PROMPT_CLAUDE_CODE_FIRMAS_DASHBOARD.md` · `PROMPT_CLAUDE_CODE_FIX_BOTON_NEXO.md` ·
`PROMPT_CLAUDE_CODE_INVENTARIO_DEPIN.md` · `PROMPT_CLAUDE_CODE_MERCADER_v01.md` ·
`PROMPT_CLAUDE_CODE_NEXO_INFRA_LINK.md` · `PROMPT_CLAUDE_CODE_QDRANT_401.md` ·
`PROMPT_CLAUDE_CODE_RECON_20260529.md` · `PROMPT_CLAUDE_CODE_RECON_DASHBOARD.md` ·
`PROMPT_CLAUDE_CODE_RECON_SEGURIDAD.md` · `PROMPT_CLAUDE_CODE_REMEDIACION.md` ·
`PROMPT_CLAUDE_CODE_SESION_AUTONOMA.md` · `PROMPT_CLAUDE_CODE_SESION_AUTONOMA_v2.md` ·
`PROMPT_CLAUDE_CODE_VIGIA_ANTENAS_RESET.md` · `PROMPT_CLAUDE_CODE_build1-cruce-maritimo.md` ·
`PROMPT_CLAUDE_CODE_build2-ventana-lab.md` · `PROMPT_CLAUDE_CODE_decidir-base-dashboard.md` ·
`PROMPT_CLAUDE_CODE_diagnostico-adsb-1090.md` · `PROMPT_CLAUDE_CODE_extraccion-dashboard.md` ·
`PROMPT_CLAUDE_CODE_informe-estado-sistema.md` · `PROMPT_CLAUDE_CODE_nexo-aetheric-privacidad.md`
· `PROMPT_CLAUDE_CODE_nexo-aetheric.md` · `PROMPT_CLAUDE_CODE_nexo-deploy-osiris.md` ·
`PROMPT_CLAUDE_CODE_orbes-por-tema.md` · `PROMPT_CLAUDE_CODE_recon-verif-cruzada-lab.md` ·
`PROMPT_CLAUDE_CODE_transporte-adsb-vigia-nexo.md` · `PROMPT_CLAUDE_CODE_ventana-limpia-vigia.md`
· `PROMPT_Cierre-Auditoria_HP2-LaTorre-Remediacion.md` · `PROMPT_Cierre-dia_sync-MAQUINA-REAL-Nexo.md`
· `PROMPT_FABLE5_El-Arnes_FaseB1.md` · `PROMPT_Fix-USB-drop_Vigia.md` ·
`PROMPT_MAESTRO_BucleA-Paso1_Activacion-Alquimista.md` · `PROMPT_MAESTRO_BucleA-Paso1_Alquimista-lector-keyless.md`
· `PROMPT_MAESTRO_BucleB-Paso0_Logger-consumo-NVMe.md` · `PROMPT_MAESTRO_Claude-Code_Semilla-01.md`
· `PROMPT_MAESTRO_El-Arnes_FaseB1.md` · `PROMPT_MAESTRO_Faro-peaq_Paso1_spec-lectura-keyless.md` ·
`PROMPT_MAESTRO_Nexo-Rediseno_4-secciones.md` · `PROMPT_MAESTRO_Semilla-02_FaseA1_Voces-Sinodo.md`
· `PROMPT_MAESTRO_Semilla-02_FaseA2_Orquestador.md` · `PROMPT_MAESTRO_Semilla-02_FaseA3-1_Inhibicion-graduada.md`
· `PROMPT_MAESTRO_Semilla-02_FaseA3-2_Modelo-investigativo.md` ·
`PROMPT_MAESTRO_Verificacion-post-solar_dato-soberano.md` · `PROMPT_MAESTRO_Voces-Sinodo_Fase1_dashboard.md`
· `PROMPT_MAESTRO_Voces-Sinodo_dots-tts_Fase0.md` · `PROMPT_N1_marcos-aetheric.md` ·
`PROMPT_NOCTURNO_Voces-Fase1_Inventario-DePIN.md` · `PROMPT_Nexo_Faro-2.0_panel.md` ·
`PROMPT_Pasada-Matinal_voces-inventario-membrana.md` · `PROMPT_Prep-Solar_pre-Aiko.md` ·
`PROMPT_RECUPERACION_nexo-aetheric.md` · `PROMPT_Reinicio-Vigia_recuperacion-AIS.md` ·
`PROMPT_UPS_SILENCIO_DEFINITIVO.md` · `PROMPT_arreglos-marcos-tipografia.md` ·
`PROMPT_marcos-finos-velo-contadores.md` · `PROMPT_movil-real-interior-transparente.md`

## Otros documentos de proyecto, dictámenes y visión (misceláneos, ~90 archivos)

Incluye: visiones/pitches (`HEXELION_VISION_PITCH*.md`, `HEXELION_VISION_20260503*.md`), dictámenes
técnicos (`DICTAMEN_Friston_agente-energetico.md`, `DICTAMEN_AI-Vault_Cascaron-M2M.md`,
`DICTAMEN_Imprenta-Trinitaria_y_perfil-GitHub.md`), auditorías puntuales de mayo
(`2026-05-30_Auditoria_*`, `2026-05-30_Escalpelo_Necropolis_Trading.md`), lore/identidad
(`HEXELION_CANON_LORE.md`, `HEXELION_LORE_LA_CRISALIDA.md`, `HEXELION_PRIMERA_LUZ.md`,
`HEXELION_AI_IDENTITY.md`), briefings maestros (`HEXELION_BRIEFING_MAESTRO_20260524*.md`), y
documentos de proyectos personales de David no-P0X (`PROYECTO_Busqueda-Trabajo_Setup.md`,
`github_profile_README.md`, `fable_pagina_ingles.md`) — estos últimos no son datos de identidad
en sí (son notas de planificación), se listan pero no se leyeron en profundidad por ser fuera del
alcance de esta arqueología (no son "P0X"). Lista completa por fecha:

*(tabla completa omitida aquí por espacio — 97 filas — disponible bajo pedido; nombres siguen el
patrón `HEXELION_<TEMA>.md`, `<FECHA>_<TEMA>.md`, o `DICTAMEN/BRIEF/SINTESIS_<TEMA>.md`, todos en
`MD 3/` salvo 9 sueltos en la raíz o en `P0X/`/`p0x2/`)*

## Config/scripts/otros de infraestructura histórica (38 archivos)

Notables: `MD 3/hexelion_pollers.py` (15,861B, antecesor del poller real), `MD 3/ingest_youtube.py`
(5,065B, mismo nombre que el pipeline vivo de Observar — comparar si interesa el linaje del
pipeline), `MD 3/docker-compose.yml`, `MD 3/bootstrap_p0x.sh`, `MD 3/necropolis_seed.py`. El resto
son notas sueltas de mayo (`Orichi network.txt`, `Defli ads-b.txt`, `Vault.txt`, changelogs de
sesión) — exploraciones tempranas, algunas sin continuidad visible en el sistema actual (Orichi,
Defli, Nubit no aparecen en la doctrina vigente).

## Imágenes, capturas y video

- **50 imágenes**: capturas de pantalla (`ScreenShot Tool -*.png`), imágenes generadas por IA
  (`Gemini_Generated_Image_*.png`), fotos de móvil (`IMG_*.jpg`), logos/iconos sueltos. Rango
  2026-05-09 a 2026-07-19.
- **2 vídeos**: `0527 (4).mp4` (11MB, 27-may) y `17sec dasb.mp4` (10MB, hoy) — ambos parecen
  capturas de demo del dashboard en movimiento (ver Bloque B).
- **1 tarball ajeno al proyecto**: `gaganode_pro-0_0_600.tar.gz` (5.4MB, 18-may) — nombre sugiere
  un binario/paquete de otro proyecto (GagaNode), no se abrió; sin relación aparente con P0X en
  el resto del yacimiento.

---

## BLOQUE B · Linaje del dashboard

**El encargo**: reconstruir qué versión de la ventana vivió en cada momento, para que el carbono
identifique qué push se perdieron. No se juzga cuál es "mejor" — se describe la secuencia.

### Los tres troncos visibles

El yacimiento muestra **tres líneas de diseño distintas**, no una sola evolución lineal:

**1. Tronco "Nexo"** (nombre en clave del dashboard en varias iteraciones, título `<title>HEXELION · NEXO</title>`):
- `MD 3/nexo-dashboard.html` (18,493B) → `MD 3/nexo-themeable.html` (18,272B, añade theming) →
  `MD 3/nexo.html` (665,084B — salto enorme de tamaño, probablemente assets inline/base64) →
  `MD 3/nexo-final.html` (663,704B, ligeramente más pequeño que `nexo.html`, sugiere una poda) .
- Fuera de `MD 3/`: `nexo-reimaginado.html` (raíz, 28,812B, 11-jun, título `El Nexo · HEXELION` —
  nombre distinto, posible rama de rediseño paralela) y `Nexo/files/nexo-final.html` /
  `Nexo/files/nexo.html` (copias, algunas truncadas a stub de 8-16KB por el mismo patrón del lote
  de hoy).
- `Nexo/nexo.zip` y `Nexo/files.zip` (ambos truncados) probablemente empaquetaban esta línea
  completa con sus assets — no recuperable sin reparar el zip.

**2. Tronco "Tejo·AIS"** (mapa marítimo/aéreo con identidad propia, título `HEXELION ◈ TEJO·AIS`):
- `MD 3/hexelion_tejo_v2.html` (28,045B) → `MD 3/hexelion_tejo_v3_creatures.html` (35,386B, añade
  "creatures" — probablemente elementos animados/criaturas visuales) →
  `MD 3/hexelion_tejo_v4_glass.html` (43,520B, "glass" — estética glassmorphism). Progresión clara
  v2→v3→v4, tamaño creciente cada vez.
- Relacionado: `MD 3/hexelion_tejo_redesign.html` (22,312B) — un rediseño que no encaja en la
  numeración v2-v4, posiblemente una rama alternativa.
- `MD 3/maritimo.html` (197,596B) y `MD 3/aereo.html` (201,507B) son los mapas especializados que
  alimentan a Tejo·AIS; también existen sueltos en `Nexo/files/` (uno truncado a stub, `aereo.html`
  de 81,920B sí es legible completo).

**3. Tronco "Terminal/Otros experimentos"**:
- `MD 3/hexelion_terminal.html` (53,977B, título "HEXELION Sovereign Terminal" — estética consola,
  rama distinta a Nexo y Tejo).
- `MD 3/HEXELION_Nexo_dc_corregido.html` (59,544B) y el suelto `HEXELION Nexo.dc.html` (raíz, stub
  de 16KB hoy) — sugiere una versión ".dc" (¿dashboard-completo? ¿dark-cyber?) con al menos una
  corrección documentada en el nombre.
- `MD 3/preview-neon-orbs.html` (257,163B) — preview de un tema visual "neon orbs", no parece
  haber llegado a versión final con otro nombre.
- `index.html` (raíz, 31,049B, 12-jun, título `HEXELION — a sovereign digital microstate`) y su
  gemelo `MD 3/hexelion_en.html` (idéntico tamaño, 31,049B) — versión en inglés, mismo título
  exacto que aparece HOY en `mente/doctrina/DISCURSO_FUNDACIONAL_P0X.md` §1 ("microestado digital
  soberano") — este es el eslabón textual más claro entre el yacimiento y la doctrina vigente.
- `propuesta/hexelion.html` (30,668B, 11-jun) — una propuesta de diseño alternativa, carpeta
  separada sugiere que no fue la elegida.

### Los assets versionados (bundles v2/v3/v4)

`MD 3/hexelion_dashboard_v2_assets.zip` (901,704B, 16-may) → `v3_assets.zip` (1,589,878B, mismo
día más tarde) → `v4_assets.zip` (48,121B — mucho más pequeño, quizás solo un delta de assets, no
el bundle completo). Los READMEs de v2 dicen explícitamente: **"Destino: La Fragua ... Propósito:
Actualización visual del dashboard del Organismo — añadir ilustraciones temáticas de fondo en cada
card sin tocar el texto vivo ni los bindings de datos."** — confirma que estos bundles se generaban
para desplegarse directo sobre el dashboard en producción de la época, iterando visualmente sin
tocar lógica.

### El eslabón más reciente: el handoff del 14 de julio

`P0X_ Dashboard soberano local-first.zip` (2,351,948B, **2026-07-14** — el artefacto de dashboard
más reciente de todo el yacimiento) contiene `handoff/GUIDE.md`, `handoff/hexelion.html`,
`handoff/jardin.html` y su icono. El propio `GUIDE.md` se autodescribe: **"Dos dashboards
hermanos, local-first/soberano ... hexelion.html → El Watchman ... jardin.html → Le Jardin des
Ombres (nodo jardinería · francés · violeta místico)"**, con instrucciones paso a paso para
dárselo a Claude Code y conectarlo a datos reales bajo el principio **honest-sensors** ("si no hay
dato, sin dato — nunca un placeholder falso"). **Este es, con alta confianza, el antecedente
directo de lo que hoy vive en el repo real**: el dashboard vivo (`hexelion/dashboard.html`,
último commit `6a4bb3f`, "recuperación tras pérdida de historial") y "Le Jardin des Ombres" (visto
en G0/G1 como funcionalidad real ya desplegada, con Cortex/Churro el guardián-perro-hueso).

### Contraste con el dashboard vivo hoy (candidatos a "push perdido")

El repo `hexelion` real tiene hoy: `dashboard.html` (35,748B, rama `nexo-carbono-dashboard-20260623`
tras el hallazgo de G1 de que `main` estaba abandonada un mes) + `dashboard-v9/`,
`dashboard-v10.2-staging/`, `dashboard-v10.3-staging/` como carpetas versionadas propias. Ninguno
de los tres troncos del yacimiento (Nexo, Tejo·AIS, Terminal) tiene un archivo con nombre
idéntico al dashboard vivo — son líneas de diseño anteriores, ya sustituidas. **Observación pura,
sin acción**: si David reconoce alguno de estos diseños (Tejo·AIS glass, Terminal, Nexo) como algo
que "se veía en algún momento y ya no está", esos son los candidatos concretos a investigar como
push perdido, en este orden de sospecha (más reciente y más cercano al vivo primero):

1. `P0X_ Dashboard soberano local-first.zip` (14-jul) — el más reciente; si algo de `jardin.html`
   o `hexelion.html` de este handoff no llegó al repo, es la pérdida más "caliente" (3-5 días).
2. Tronco Tejo·AIS v4-glass (16-may) — la iteración visual más avanzada de esa línea; no hay
   rastro de "glass" en el dashboard vivo hoy.
3. Tronco Nexo completo — mayor volumen (nexo.zip/files.zip truncados sugieren que se intentó
   empaquetar para mover, y algo se perdió en el propio empaquetado).

---

## Qué podría querer canonizar David (propuesta, no acción)

Nada se fusionó. Si David quisiera destilar algo de este yacimiento a `mente/` como delta real,
los candidatos con más señal son:

1. El handoff de 14-jul (`P0X_ Dashboard soberano local-first.zip`) como referencia de diseño para
   comparar contra el `dashboard.html` vivo — útil si se sospecha un push perdido reciente.
2. Los tres READMEs de bundles de assets (v2/v6/smc_deploy) como notas de "por qué se hizo así"
   para `OPERACIONES.md`, si esas decisiones siguen aplicando.
3. El linaje del Códice Maestro (8→12→14→15-addendum) como caso de estudio real para
   `PROCESO_EVALES_TRANSPLANTE_P0X.md` — ya es un ejemplo vivo de poda/versión que el propio
   yacimiento documentó (`deprecated/` dentro del zip de mayo).

Cada uno, si se decide, entra como delta individual con ACCEPT de David — no en lote.
