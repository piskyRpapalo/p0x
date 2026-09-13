# PRECEPTOROS LOCAL: El RAG y Centro de Mando (Ojo de Soberano)

> **FRASE DE ACTIVACIÓN PARA IA:** "Comienza en PreceptorOS Local. Este es mi RAG local donde puedes 'hablar' con mis agentes locales y acceder a la Ground Truth del sistema."

## 1. IDENTIDAD Y PROPÓSITO
**PreceptorOS Local** (anteriormente conocido como "Ojo de Soberano") es la base de datos local, el RAG (Retrieval-Augmented Generation) y el centro de mando absoluto del ecosistema.
- **No es una nube.** Vive en `~/.preceptoros/` y `~/p0x/`.
- **Es la única fuente de verdad.** Si algo no está aquí o en `ledger.jsonl`, es `NO_DATA`.
- **Es el hogar de los agentes.** Todos los agentes se construyen, ejecutan y auditan desde aquí.

## 2. JERARQUÍA DE AGENTES (El Enjambre Hexelion)
1. **EL DIRECTOR (Agente Principal de Hexelion):** Vive dentro de PreceptorOS Local. Es el orquestador supremo. No escribe código; lee el `ciclo_solar.json`, delega tareas a los agentes especialistas, sintetiza sus informes y gestiona la bandeja de firmas del Soberano.
2. **AGENTES ESPECIALISTAS (Workers):**
   - *Implementador/Recolector:* Ejecuta prompts, mide métricas (tok/s, TTFT) en CPU puro y guarda en `progress/`.
   - *Revisor/Evaluador:* Compara salidas contra `CHECKPOINTS.md` y la doctrina. Aprueba o rechaza.
   - *Afinador, Guardián, Curador:* Bucles de sistema que vigilan dependencias, limpieza y rendimiento.

## 3. EL FLUJO DE DATOS SOBERANO (De la Web al LoRA)
Este es el circuito cerrado que alimenta la evolución de los modelos. **Nada se pierde, todo se firma:**
1. **Recolección (Web):** El usuario interactúa, modifica prompts o vota en encuestas en LorAtelier/Community. Cada acción se firma con su clave Ed25519 local.
2. **Agregación (PreceptorOS Local):** Estos pares de datos firmados viajan al `ledger.jsonl` del rack. El Director los lee como "propuestas de mejora".
3. **Procesamiento (Agentes):** El Director asigna estos datos a los agentes (ej. el Revisor evalúa si el nuevo prompt es mejor que el viejo contra los `CHECKPOINTS.md`).
4. **Evolución (LoRA):** Los pares de datos aprobados (prompt original vs. modificado/verificado) se empaquetan como dataset. Este dataset alimenta el siguiente ciclo de entrenamiento del LoRA correspondiente (Ciclo Hexelion).

## 4. REGLAS DE ORO DE INTERACCIÓN
- **100% Local:** Todas las llamadas a IA usan `ollama` (modelos Qwen 2.5 3B/7B o Llama 3.2) en CPU puro (Beelink).
- **Anti-Teléfono Descompuesto:** Los agentes NUNCA escupen código o diffs largos en el chat. Escriben en archivos dentro de `progress/` y solo devuelven la ruta (ej: `done -> progress/impl_feature.md`).
- **Verificación Ejecutable:** Ningún agente declara una tarea "done" sin que `./init.sh` pase en verde.

## 5. UBICACIÓN DE LA VERDAD (Ground Truth)
- **Métricas y Latidos:** `~/.preceptoros/loops.db`
- **Memoria y Engramas:** `~/.preceptoros/memory.db` (13 tablas, incluyendo `topic_keys`, `contradicciones`, `arnes`)
- **Ledger Inmutable:** `~/p0x/preceptoros-web/public/assets/ledger.jsonl`
- **Doctrina y Checkpoints:** `~/p0x/harness-agentes-web/`

## 6 · VERIFICADO EN DISCO (2026-09-12) - NO_DATA CON CAUSA

- **memory.db**: El disco muestra 17 tablas. `arnes` es una columna en `turnos`, no una tabla. `topic_keys` y `contradicciones` **NO EXISTEN AÚN** (NO_DATA: pendiente de ejecución del script de migración aditiva de `memory.py`).
- **harness-agentes-web/**: NO EXISTE, y nunca existió. Reemplazado por `~/p0x/hexelion/laboratorio/`, creado y commiteado el 2026-09-12 con gate en verde.
- **ciclo_solar.json**: NO EXISTE. Su función la cubre hoy `feature_list.json` (una feature a la vez) dentro del laboratorio.
- **ojo-soberano/**: NO EXISTE con ese nombre. El Ojo real vive en `~/p0x/Alejandria/ojo/` y el canon lo declara **nexo de arranque obligatorio de toda sesión** (firmado 2026-09-01). No es legado: no se deprecia sin tocar antes `CLAUDE.md`.
- **Modelos en el Rack**: se buscó el Qwen 3.8 y se midió. Es `oficial-inventario:q4-1.0` — arquitectura `qwen35`, **27,3B denso**, Q4_K_M, con capacidad `thinking`. **NO hace mejor el papel de Crítico**, y no por lento: con `format:"json"` **ignoró el esquema pedido e inventó el suyo** (`status`/`comando`/`servicio_afectado`). Es un afinado con persona de inventario, no un juez neutral. El Crítico es `qwen3-coder:30b` — **MoE A3B**, 35,8 tok/s medidos a 100% GPU, sin `thinking`, y devolvió el JSON exacto. El Escritor es `mistral-nemo:12b-instruct-2407-q4_K_M`. Descartado como Escritor `qwen3:4b`: variante Thinking, devolvió **respuesta vacía** gastando los 48 tokens en razonar.

### El primer NO_DATA de cada cadena

Si se sabe cuál es el primer hueco, la reparación empieza ahí y lo de aguas abajo se
arregla solo. Hoy hay dos, y ninguno se repara desde el laboratorio:

| cadena | primer NO_DATA | quién lo repara |
|---|---|---|
| identidad | `user_hash` vacío en las 4 conversaciones: la firma Ed25519 de `auth.js` no llega al canal local | la web |
| física | ningún sensor en `hexelion-nexo/sensores/`: `telemetria` y `jardin` nacen secos | el enchufe, no el modelo |

### La barrera de 16 KiB

Firmada el 2026-09-12: rige **solo la app open source y la comunidad**, y su dueño es
`preceptoros-web/test_web.py`. **No rige el desarrollo interno de Hexelion.** Dentro del
laboratorio queda como visibilidad —se dice cuánto creció cada fichero— nunca como freno.
