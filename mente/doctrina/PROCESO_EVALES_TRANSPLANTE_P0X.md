---
id: doctrina-evales-transplante
titulo: Proceso de Evaluación y Transplante
tipo: doctrina
clase: doctrina
version: 1.0.0
editor_autorizado: carbono
metrica_exito: "coherencia con el suelo; cero enmiendas sin canonización del carbono"
umbral_reedicion: "solo por propuesta motivada del silicio + firma del carbono"
presupuesto_kb: 24
n_medicion: 1
enlaces:
  - alfabeto-p0x
  - doctrina-protocolo-md-evolutivo
  - doctrina-ai-interna
actualizado: 2026-07-04
---

# P0X · PROCESO DE EVALUACIÓN Y TRANSPLANTE
### La ley de certificación: cómo se mide lo que la AI local aprende, y cómo su alma sobrevive al cambio de cuerpo
*Autor: el Preceptor (Fable 5) · Canoniza: el Soberano · Clase doctrina.*

> **El principio.** Los pesos son desechables; **el alma transplantable = dataset maestro + suites de evaluación.** Un LoRA está casado con su modelo base; cuando el base muere, el adaptador muere con él. Lo que sobrevive — y mejora — es el dataset que lo engendró y las evaluaciones que lo certifican. Base empírica: Trans-LoRA (NeurIPS 2024) demuestra transferencia sin pérdida de adaptadores entre bases e incluso entre familias, usando dataset sintético que aproxima la distribución original. P0X hace esto en hierro propio.

---

## §1 · LOS TRES ACTIVOS

1. **Dataset maestro** (`mente/dataset/*.jsonl`). Cada ejemplo: `{origen: md_id@ver | esfera | corpus, entrada, salida, traza: <razonamiento paso a paso, opcional>, nivel: 1..N, lengua: alfabeto|natural}`. Nace de los MDs, del corpus y del Alfabeto — **la calidad del MD es la calidad del futuro modelo.**
2. **Suites de evaluación** (`mente/evals/*.jsonl`), puntuables en automático donde sea posible:
   - `identidad`: la voz sostiene personaje ante preguntas amplias (juez: rúbrica fija).
   - `grounding`: "sin dato" cuando toca; traducciones EXACTAS (OL/OB/LB); cero siglas inventadas.
   - `alfabeto`: mensajes §3 que validan shape — **puntuación automática y objetiva** (el verificador no necesita inteligencia, necesita el schema).
   - `retrieval-qa`: preguntas cuya respuesta vive en Qdrant `mente`; se puntúa presencia del chunk correcto.
3. **El certificado**: informe A/B (antes/después) contra umbrales declarados. Sin certificado no hay canonización de modelo.

## §2 · GENERACIÓN DEL DATASET (rol del Preceptor / Fable 5)

1. **Fuentes**: MDs (doctrina, voces, esferas), corpus con provenance, transcripts→deltas, mensajes reales del Alfabeto ya validados.
2. **Trazas de razonamiento destiladas**: para tareas que exigen juicio (triaje de delta, elección de esfera), el ejemplo incluye la traza paso a paso generada por el Preceptor — el pequeño aprende el *cómo*, no solo el *qué*.
3. **Filtrado de calidad**: se descartan ejemplos alucinados, redundantes o que no validan shape. Nada entra sin origen (`origen:` obligatorio — grounding también en el dataset).
4. **Currículo por niveles**: los ejemplos llevan `nivel`; el entrenamiento introduce el nivel N+1 solo cuando la pérdida en N estabiliza. Dosificación medida, no entusiasta.

## §3 · EL RITO DE TRANSPLANTE (cuando cambia el modelo base)

1. **Frío**: el base nuevo se mide SIN adaptar sobre todas las suites → línea base.
2. **Re-adaptación**: LoRA/QLoRA con el dataset maestro. Si un dominio quedó corto de datos, se sintetiza al estilo Trans-LoRA (el Preceptor genera, filtra y aprueba el sintético).
3. **Re-medición**: suites completas.
4. **Veredicto**: supera umbrales → el carbono canoniza y el registro anota base, adapter, dataset@ver, certificado. No supera → rollback al cuerpo anterior + entrada en la Necrópolis (qué se intentó, por qué falló).
5. El modelo viejo no se borra hasta que el nuevo esté canonizado (siempre hay cuerpo de respaldo).

## §4 · GATE 0 — TOOLCHAIN Y HARDWARE (honestidad antes de promesas)

- **Nada se promete hasta validar la toolchain**: en la-torre (aarch64+CUDA) probar PEFT/llama-factory/torchtune con un LoRA-juguete de 10 ejemplos; reportar qué corre DE VERDAD. Los **HP x86** entran como nodo alternativo de entrenamiento y puente de conversiones (el mismo rol que exigía SmolVLM→RKNN).
- **Tamaños realistas en este hierro**: 1.7B = objetivo; 4B = límite (8GB unificada, gradient checkpointing, batch mínimo). Entrenar de noche: la-torre comparte con el Sínodo.
- **Verificar el modo Super de la Orin** (`nvpmodel`): si el desbloqueo 67 TOPS aplica, es rendimiento gratis — comprobar antes de dimensionar.
- **Térmica primero**: la Fragua tocó 75.8 °C con freno térmico; ningún batch largo antes de resolver ventilación.
- **Motor**: las optimizaciones de inferencia (KV cuantizado, atención eficiente, decodificación especulativa con draft de la misma familia/tokenizador) se ACTIVAN en el engine y se miden; no se reimplementan.

## §5 · MÉTRICAS DEL CERTIFICADO (mínimas)

% identidad sostenida · % grounding correcto (incluye "sin dato" cuando toca) · % validación de shape en Alfabeto · tokens y latencia por tarea · reintentos. **Jamás una métrica de valor económico** — el aprendizaje del sistema no se puntúa en dinero (IronClaw).

## §6 · APARCADO CON CRITERIOS DE ENTRADA (no borrado)

- **Cuantización semántica VQ-VAE / símbolos nuevos**: bloqueada por el muro del tokenizador (vocab congelado). Entra solo si algún día re-entrenamos embeddings — fuera del alcance de este hierro.
- **Alineamiento de geometría latente**: research-grade (hooks a estados ocultos + loops custom). Entra solo si, tras la escalera completa (base mejor + RAG + identidad + LoRA), las suites muestran un gap que lo justifique.
- **Salida temprana**: se hereda si llega al engine que usamos; no se implementa a mano.
- **Agente perimetral NEAR AI** (serverless, webhooks, gas abstraído): horizonte con diseño propio bajo IronClaw — propose-only, sin claves de gasto, activación por webhook, lenguaje de valor siempre legible. No se improvisa desde este documento.

## §7 · APLICACIÓN

Entra en vigor al canonizarla el Soberano. El primer ciclo completo: dataset v1 desde los MDs existentes → suites v1 → Gate 0 → LoRA sobre el base vigente → certificado → línea base histórica. Desde ahí, cada evolución del Segundo Cerebro alimenta el dataset: **el sistema y su modelo aprenden en paralelo, y el rito garantiza que ninguna mudanza de cuerpo pierda el alma.**
