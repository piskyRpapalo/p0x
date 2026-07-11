<!-- Artefacto de auditoría (como AUDIT_2026-07-05.md): SIN front-matter YAML a
propósito, para que build_graph NO lo proyecte como nodo. El esquema de nodos
propuesto vive en el Bloque 5 y es PROPUESTA, no ejecución.
Generado: 2026-07-11 · Fable 5 · read-only sobre ~/P0X · cero fabricación. -->

# ARQUEOLOGÍA P0X
### Auditoría read-only de `~/P0X` (157 MB, 459 ficheros) — la historia del proyecto contada por sus archivos
*Pase de LECTURA + SÍNTESIS. No se movió, borró ni editó nada de `~/P0X`. Movimiento 2 (dashboard/voces) queda para después, con este mapa en la mano.*

> **Suelo metodológico (honestidad):**
> 1. **Los mtimes NO sirven de cronología** — todo `~/P0X` fue copiado por scp el 2026-07-11, así que el filesystem miente sobre fechas. La cronología de este mapa se reconstruye desde **fechas embebidas en nombres** (`ScreenShot…20260516`, `HEXELION_SESION_20260504`), **fechas internas** de los documentos, y las tablas de hitos que el propio corpus ya llevaba (`_ESTADO.md`).
> 2. **Idea ≠ ejecutado.** Cada hallazgo marca si fue *propuesta* o *cosa que corrió*. Mucho de lo más elaborado nunca se ejecutó.
> 3. **Material personal excluido.** `CV_David_Pecero.docx` (×2), `Fixed_Term_Local_…_Caballero.pdf` (contrato), `HEXELION_BITACORA_SESION.docx` — NO se abrieron, NO se citan, NO salen de aquí. Solo se anotan como "material personal, excluido".

---

## BLOQUE 1 · INVENTARIO

### Peso por familia (nivel 1)
| Familia | Peso | Qué es |
|---|---|---|
| **Vídeos** (raíz, .mp4) | ~35 MB | Grabaciones de demo del dashboard (`17sec dasb`, `Dashboard 8Sec/5 sec`, `0527`) |
| **`Imagenes buenas/` + imágenes raíz** | ~36 MB | Branding (Gemini_Generated_Image_*, Hexelion_icono/ojos), screenshots de dashboard fechados |
| **`Nexo/` + `HEXELION_NEXUS/`** | ~19 MB | Dos "second brains": `Nexo/` (assets dashboard) y `HEXELION_NEXUS/` (KB doctrinal estructurada) |
| **`MD 3/`** | 15 MB / **197 .md** | **El archivo maestro**: casi toda la historia de prompts + doctrina |
| **`hexlab/`** | 6.3 MB | Copia de trabajo de hexelion-lab |
| **`gaganode-windows-amd64/` + tar.gz** | ~10 MB | Binario DePIN (Gaganode, Windows) — software de terceros, no doctrina |
| Resto (`files`, `files22`, `CR`, `propuesta`, `P0X`, `p0x2`, zips) | ~2 MB | Duplicados y snapshots parciales de `MD 3` |

### Tipos (histograma)
273 `.md` · 52 `.png` · 25 `.html` · 23 `.zip` · 22 `.txt` · 9 `.py` · 9 `.json` · 8 `.jpg` · 7 `.jsx` · 4 `.yaml` · 4 `.mp4` · 3 `.docx` · 2 `.exe` · 1 `.pdf`.
El corazón intelectual son los **273 markdown**; todo lo demás es soporte visual, binarios de terceros o duplicados.

### Duplicados y versiones (el ruido)
- **`MD 3/` es superconjunto.** Los directorios `files/`, `files22/`, `P0X/`, `p0x2/`, `CR/`, `propuesta/` son snapshots parciales: los mismos ficheros (`CLAUDE_CODE_DASHBOARD_V9`, `CODICE_david`, `INSTRUCCIONES_P0X`, `CLAUDE_CODE_SINODO_V1`…) aparecen 2–3 veces. Para futuras lecturas: **leer `MD 3/` y `HEXELION_NEXUS/`; ignorar el resto como copias**.
- **Cadenas de versión detectadas:**
  - Códice doctrinal: `2026_8` → `2026_12` (deprecated) → `2026_14` (vigente en NEXUS) → `2026_15_ADDENDUM_ENERGETICO`.
  - Dashboard (prompts Claude Code): `v2` → `v2_REFACTOR` → `v3` → `v4` → `VISUAL_ONLY` → `v6_pollers` → `v7_live` → `V9` → `V102` → `v10_PROMPT(_v1.1)`.
  - Dashboard (HTML render): `hexelion_tejo_redesign` → `_v2` → `_v3_creatures` → `_v4_glass`; y `nexo-dashboard` → `nexo` → `nexo-final` → `nexo-themeable` → `nexo-reimaginado`.
  - Sínodo/Semilla: `SINODO_V1` → `SINODO_FASE1` → `Semilla-01` → `Semilla-02` (`FaseA1_Voces` / `FaseA2_Orquestador` / `FaseA3-1_Inhibicion` / `FaseA3-2_Investigativo`) → `El-Arnes_FaseB1` (hay variante `PROMPT_FABLE5_…`).

---

## BLOQUE 2 · LÍNEA DE EVOLUCIÓN (cronología reconstruida)

Fuente: fechas en nombres + fechas internas + la tabla de hitos de `HEXELION_NEXUS/00_Vision_Lab/_ESTADO.md`.

| Fecha (2026) | Hito | Qué congeló / qué lo reemplazó |
|---|---|---|
| **02 May** | Despliegue inicial del rack (`SESION_20260502`) | Nace el organismo. Fragua (Orange Pi 5+) como núcleo. |
| **03 May** | `VISION_NUEVOS_ENFOQUES` | Pivote "Códice vs Protocolo → ejecutar ambos". |
| **04 May** | `SESION_VISION` | Separación en **3 Capas**: Organismo / Lisboa / Empresa. |
| **06 May** | `ANALISIS_JSON` | Triaje de JSONs externos; gaps documentados. |
| **11 May** | `SESION_20260511` | Tailscale completo. **Incidente "firmas no autorizadas"** (primera cicatriz de gobernanza). |
| **15 May** | **PUNTO CRÍTICO — Reforma Energética → "La Crisálida"** | Se asume que el organismo nace **sin batería** (Era Sol-Síncrono). Se especifican `BATTERY_FLAG`, `@sleeping`, Reencarnación Energética. |
| **17 May** | `SISTEMA_ESTADO` + `TAREAS` | Auditoría dashboard v7 + pollers v6. |
| **19 May** | **Migración a `HEXELION_NEXUS`** (00–06) | Se estructura el second-brain con el "Ciclo del Dato" (Gemini_Raw→Claude_Refined→decisión). Nacen ideas: HexelionFarm, Compute Index, Market Oracle. |
| **24 May** | **`DOCTRINA_DEL_SILENCIO` (v2026.17)** + **`PLAN_PROFESIONALIZACION`** | La auditoría revela "divergencias entre el Briefing Maestro y la realidad". Empieza el **giro sobrio**: reglas duras (mainnet STOP, confirmar destructivo, no improvisar). |
| **25 May** | `VISION_CREATIVA` | Lenguaje visual (temas, orbes, criaturas). |
| **29 May** | `RECON_20260529` | Reconocimiento del sistema real. |
| **07 Jun** | `DOCTRINA_Hexelion-Hibrido` | Modelo híbrido. |
| **12 Jun** | `EVALUACION_Faro-2.0_Economia-Maquina` | El Faro como economía-máquina (atestación + créditos). |
| **jun–jul** | Migración a **`P0X` / `El Preceptor`** (rack `/mnt/nvme/p0x/mente`) | El sistema vivo actual. `DISCURSO_FUNDACIONAL_P0X` fechado **04 Jul**. |

### Los PIVOTES grandes (cambios de rumbo, no incrementos)
1. **15 May — La Crisálida (energético).** De "organismo pleno" a "organismo sin batería que finge estar completo mediante un flag". Motivo: la batería física no llegó; en vez de bloquear, se inventó el patrón `@sleeping`/`BATTERY_PRESENT` para poder desplegar ya y "reencarnar" después. *(Ver Bloque 3.)*
2. **19 May — De carpeta suelta a NEXUS.** De prompts dispersos a un KB con dominios numerados, `_ESTADO.md` por carpeta y descartes motivados. Primer intento serio de "second brain".
3. **24 May — Profesionalización.** La auditoría encuentra que el mito iba por delante de la realidad. Arranca el endurecimiento de gobernanza (el germen de IronClaw).
4. **jun–jul — HEXELION → P0X / El Preceptor.** El giro más profundo: de "organismo cibernético soberano con voluntad" a **"motor pedagógico privado del Soberano"** con doctrina sobria, propose-only y el LLM fuera de los lazos de consecuencia. La mitología cede ante la disciplina de evidencia. *(Ver Bloque 4.)*

---

## BLOQUE 3 · IDEAS PERDIDAS (lo más valioso)

Cada una: **qué era · estado · por qué se perdió · veredicto (revivir o no, con razón).**

### 3.1 · El patrón `@sleeping` / `BATTERY_FLAG` ⭐ (el hallazgo)
- **Qué:** `HEXELION_BATTERY_FLAG_SPEC.md` (v1.0, 15 May) — una sola variable `BATTERY_PRESENT` conmuta dos Eras (SOL_SINCRONO ↔ PLENA). Decoradores `@sleeping` (código presente pero dormido, se loguea cada invocación) y `@sun_synchronous` (su simétrico). Inventario de funciones dormidas, tests, métrica Prometheus, runbook de "Reencarnación" con rollback.
- **Estado:** **idea, casi nada ejecutado** — literalmente todo el módulo energético quedó `@sleeping` esperando hardware de batería que no llegó.
- **Por qué se perdió:** dependía de batería física + medidor FoxESS DDSU666; el proyecto pivotó a P0X antes de la Reencarnación.
- **Veredicto: REVIVIR EL PATRÓN (no las tácticas).** El mecanismo "una variable conmuta era, código dormido pero versionado y observable" es elegante y reutilizable — encaja con la transición futura a batería y con `honest-sensors` (el código dormido no finge datos). **Ojo de coherencia:** las *tácticas* que envolvía (arbitraje energético, MCT-MAX cargando de red negativa **para generar ingresos**) hoy están **prohibidas por IronClaw** (los reflejos jamás tocan valor). Revivir el envoltorio, NO el arbitraje autónomo. *(Nota: mi `reflejo-bateria` de esta semana es una astilla determinista y sobria de esta visión — lee UPS OB/LB real y pausa la cola batch, sin valor, sin LLM.)*

### 3.2 · Tres oráculos de mercado parados (Gemini, 19 May)
- **HexelionFarm** (protocolo agrícola DePIN), **Hexelion Compute Index** (índice financiero sintético de precio de hardware), **Market Oracle Silicio Usado** (scraping OLX/Wallapop/eBay como "Vocero Función H").
- **Estado:** idea pura, en cola "post-Ciclo Dorado". Nunca arrancaron.
- **Por qué:** sin disparador económico; el proyecto se centró en infraestructura y luego en pedagogía.
- **Veredicto: Market Oracle = REVISABLE** (encaja con el Vocero actual como fuente de datos honesta de un mercado real). Compute Index y HexelionFarm = **dejar parados** (especulativos, lejos del núcleo actual).

### 3.3 · El esquema NEXUS (00–06 + `_ESTADO` + "Ciclo del Dato")
- **Qué:** organización por dominios numerados con snapshot fechado por carpeta (`_ESTADO.md`) y regla "descarte motivado, nunca borrado silencioso".
- **Estado:** ejecutado en mayo, **abandonado** al migrar a `mente/` (tipo-based: esfera/doctrina/voz/tecnica + Qdrant + grafo).
- **Por qué:** el `mente/` actual es más potente para búsqueda (embeddings) y grafo, pero **perdió el `_ESTADO.md` por dominio** (el snapshot "esto es lo que hay aquí hoy y qué contradice a qué").
- **Veredicto: REVIVIR UNA PIEZA** — un `_ESTADO`/snapshot por esfera-madre enriquecería la gobernanza actual (la Necrópolis ya heredó "descarte motivado"). *(Ver Bloque 5.)*

### 3.4 · Diseños de dashboard abandonados
- `hexelion_tejo_v3_creatures` (criaturas), `_v4_glass` (glassmorphism), `preview-neon-orbs` (orbes de neón), `nexo-aetheric` / `PROMPT_N1_marcos-aetheric` (tema "aetheric").
- **Estado:** HTML/prompts existen; solo el **tema aetheric** sobrevivió parcialmente (hoy hay tema sovereign/aetheric/violeta en el vivo).
- **Veredicto: MINA VISUAL para el Movimiento 2** — "glass", "creatures" y "neon-orbs" son lenguajes visuales concretos que ya se prototiparon; revisarlos antes de inventar de cero el próximo reskin.

### 3.5 · "El Mercader" (voz del Sínodo)
- **Qué:** `PROMPT_CLAUDE_CODE_MERCADER_v01` — voz de comercio M2M, primer producto DRY_RUN.
- **Estado:** propuesta; el Sínodo vivo tiene Alquimista (economía) pero no Mercader.
- **Veredicto:** probablemente **fusionado en el Alquimista**; dejar como nota histórica salvo que se quiera separar "comercio activo" de "asesoría económica".

### 3.6 · La capa de LORE (mitología operativa)
- `LORE_LA_CRISALIDA`, `PRIMERA_LUZ`, `REENCARNACION`, `AI_IDENTITY`.
- **Estado:** mayormente **abandonada** en P0X sobrio. Excepción: `REENCARNACION.md` es un **runbook operativo real** (reconstruir la Fragua en 30 min desde la "Bóveda Genoma" USB).
- **Veredicto:** el mito, a la Necrópolis con honor. **`REENCARNACION.md` merece verificarse contra la realidad actual** (¿sigue siendo válido el runbook de recuperación tras el cambio a P0X/NVMe?) — valor operativo real, no nostalgia.

---

## BLOQUE 4 · COHERENCIA FILOSÓFICA (la tarea de David)

Contraste de los **cuatro fundamentos** contra las decisiones actuales. Sin miedo.

### 4.1 · IronClaw (el LLM fuera de los lazos de valor) — **INVERSIÓN sana, pero es una inversión**
La identidad de mayo (`HEXELION_AI_IDENTITY.md`) dice literal: *"No soy una herramienta. Soy el juicio del organismo"* — un Qwen-14B como **órgano cognitivo soberano que decide** arbitraje energético, tiers, cargas. El `BATTERY_FLAG` ponía al Monje a **cargar batería de la red para generar ingresos** de forma autónoma.
Hoy **IronClaw invierte esto**: los reflejos son solo protectores, **jamás valor**, y el LLM queda **fuera del arco, solo informado**. 
→ **Veredicto:** NO es contradicción, es **maduración** — la grandiosidad ("juicio del organismo") se sobró en disciplina de seguridad. Pero es honesto nombrarlo: **el P0X actual repudia la mitología fundacional del "organismo con voluntad".** El `AI_IDENTITY.md` inmutable ya no describe al sistema vivo. *Recomendación: enterrar formalmente `AI_IDENTITY.md` en la Necrópolis con motivo, para que ningún futuro silicio lo lea como canon.*

### 4.2 · honest-sensors — **COHERENTE, y el pivote lo confirma**
El `BATTERY_FLAG` de mayo construyó lógica elaboradísima (umbrales SOC, histéresis de generación) **sobre sensores que no existían** (todo `@sleeping`). El giro a honest-sensors es exactamente la corrección: no construir mecánica sobre datos ausentes. El sistema vivo (AIS/ADS-B/UPS/M5 reales, "generacion=0 honesto" cuando el solar no reporta) es fiel. **Sin deriva aquí.**

### 4.3 · Soberanía de datos — **COHERENTE e ININTERRUMPIDA**
Hilo intacto desde `INSTRUCCIONES_El-Preceptor` ("El Códice es 100% local; el Soberano puede leerlo, exportarlo, corregirlo o borrarlo") hasta el `mente/` actual (propose-only, keyless, la voz/texto jamás sale del rack, público solo con OK explícito). El fundamento más firme del proyecto. **Sin deriva.**

### 4.4 · "La doctrina no se edita; la mecánica se deriva" — **DERIVA CORREGIDA**
En mayo la doctrina **prescribía mecánica**: el Códice y el `BATTERY_FLAG` fijaban umbrales exactos (SOC<10% Asfixia, gen>1500 Cenit, inventario de decoradores). Mezclaba lo inmutable con lo derivable. El P0X actual **separa** doctrina (no editable) de mecánica (derivada, medida, en changelog). → **La separación es una mejora real**; la deriva de mayo ya está corregida. Vigilar que no vuelva a colarse mecánica dura dentro de un MD de clase doctrina.

### Síntesis de coherencia
| Fundamento | Estado | Nota |
|---|---|---|
| Soberanía de datos | ✅ coherente | El hilo más firme, ininterrumpido |
| honest-sensors | ✅ coherente | El pivote de mayo→julio lo *confirma* |
| doctrina≠mecánica | ✅ corregida | Deriva de mayo ya resuelta; vigilar recaídas |
| IronClaw | ⚠️ inversión sana | Repudia la mitología fundacional; **enterrar `AI_IDENTITY.md`** para cerrar el bucle |

**Contradicción viva única:** documentos fundacionales inmutables (`AI_IDENTITY`, LORE) describen un organismo-con-juicio que el sistema actual **deliberadamente ya no es**. No corrompen el vivo (están en `~/P0X`, no en `mente/`), pero si alguien los reingesta como canon, reintroducen la grandiosidad que IronClaw expulsó. **Cerrar con un entierro motivado.**

---

## BLOQUE 5 · ESQUEMA PARA EL SECOND BRAIN (propuesto, NO ejecutado)

Qué de esta arqueología merece volverse nodo del grafo — el mapa de la propia historia del proyecto. **Todo esto es propuesta; nada se ejecuta en este pase.**

### Esfera-madre propuesta
- **`esfera:historia-p0x`** (tipo esfera, clase operativo) — "de HEXELION a P0X: el mapa de la propia evolución". Niveles: básico (el proyecto cambió de organismo-místico a motor pedagógico sobrio); medio (los 4 pivotes); experto (la inversión IronClaw + la corrección honest-sensors). Enlaces: `discurso-fundacional-p0x`, `doctrina-ai-interna`, `proyecto-reflejos`, `edge-ai`.

### Nodos-hito propuestos (tipo `analogia`/`operativo`, hijos de historia-p0x)
1. **`hito:la-crisalida-15may`** — el pivote energético + el patrón `@sleeping` (enlaza a `proyecto-reflejos` y `energia-solar`).
2. **`hito:profesionalizacion-24may`** — germen de IronClaw (enlaza a `doctrina-ai-interna`).
3. **`hito:hexelion-a-p0x`** — el giro organismo→pedagogo (enlaza a `discurso-fundacional-p0x`).

### Fracasos a la Necrópolis (con motivo, propuestos)
- `necropolis:ai-identity-organismo-juicio` — repudiado por IronClaw (§4.1).
- `necropolis:arbitraje-energetico-autonomo` — el Monje ya no toca valor (§4.1).
- `necropolis:lore-mitologico` — Crisálida/Primera-Luz como mito, no como canon.

### Idea de gobernanza a re-incorporar (propuesta)
- Rescatar el **`_ESTADO.md` por dominio** del esquema NEXUS (§3.3): un snapshot fechado "esto hay aquí hoy" por esfera-madre. Barato, mejora la trazabilidad del grafo.

### Lo que NO debe entrar al grafo
- Material personal (CV, contrato, bitácora .docx) — excluido por invariante.
- Binarios de terceros (Gaganode), duplicados de `MD 3`, assets de branding.

---

## CIERRE · Hallazgos priorizados

| Prioridad | Hallazgo | Acción propuesta |
|---|---|---|
| 🔴 Alta | `AI_IDENTITY.md` + LORE contradicen IronClaw | Entierro motivado en Necrópolis (que no se reingesten como canon) |
| 🟠 Media | Patrón `@sleeping`/`BATTERY_FLAG` (idea fuerte, no ejecutada) | Revivir el *envoltorio* para la futura batería; NO el arbitraje |
| 🟠 Media | `REENCARNACION.md` = runbook de recuperación real | Verificar validez contra el P0X/NVMe actual |
| 🟡 Baja | `_ESTADO.md` por dominio (gobernanza NEXUS) | Evaluar re-incorporar snapshot por esfera-madre |
| 🟡 Baja | Diseños dashboard (glass/creatures/neon-orbs/aetheric) | Mina visual para el Movimiento 2 |
| 🟡 Baja | `MD 3/` = archivo maestro; el resto son duplicados | Consolidar lectura futura en `MD 3/` + `HEXELION_NEXUS/` |

*Sugerencias formales (S/M/L, estado=propuesta) anexadas a `mente/feedback/PENDIENTES.md`. Movimiento 2 (dashboard/voces) no se toca aquí — este mapa es su prerequisito.*

*(Arqueología v1 — Fable 5, 2026-07-11. Read-only sobre `~/P0X`; cero fabricación; idea y ejecución separadas.)*
