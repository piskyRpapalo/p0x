---
id: mapa-evolutivo-p0x
titulo: El Mapa — los frentes de P0X y sus puertas
tipo: operativo
clase: operativo
version: 0.1.0
estado: propuesta
editor_autorizado: carbono
dominio: coordinacion-frentes
metrica_exito: "cada frente conoce su fase, su puerta siguiente y sus dependencias; ninguna decisión estructural se toma fuera del mapa sin enmienda registrada"
umbral_reedicion: "cada cruce de puerta o cambio de fase actualiza el mapa en el mismo pase"
presupuesto_kb: 16
n_medicion: 1
enlaces:
  - instrucciones-p0x
  - orquesta-modelos-p0x
  - doctrina-ai-interna
  - doctrina-evales-transplante
  - proyecto-reflejos
  - manual-del-soberano
descripcion_niveles:
  basico: "El plano general: qué proyectos hay, en qué fase está cada uno, y qué puerta hay que cruzar para que avance. Nada avanza por entusiasmo; todo avanza por prueba."
  medio: "Mapa de coordinación de los seis frentes de P0X con fases, puertas de evidencia y dependencias cruzadas; el PC Soberano como cerebro central en graduación G0-G4."
  experto: "Doctrina de coordinación: gradiente de autonomía ejecutiva bajo rito de evales, simetría de soberanía como ley de diseño de la red de nodos, y gradiente de actuación física A0-A2 separado del invariante de firma."
actualizado: 2026-07-18
---

# EL MAPA DE P0X
### Seis frentes, un cerebro conectivo, puertas de evidencia
*Propuesto por el Preceptor a petición del Soberano (18-jul-2026). El Soberano canoniza. Rige el Protocolo del MD Evolutivo.*

> **Una frase.** P0X no es N proyectos: es un organismo cuyos frentes comparten órganos — el PC Soberano como cerebro central, `mente/` como memoria única, el Nexo como ventana — y donde cada puerta se cruza por evidencia (telemetría, evales, validación física), jamás por decreto.

---

## §0 · EL PRINCIPIO ORGANIZADOR

1. Cada frente vive en una **fase**, tiene una **puerta** siguiente y dependencias declaradas. Toda decisión estructural nombra su frente y su puerta; si no encaja en el mapa, primero se enmienda el mapa (con motivo y changelog).
2. **Regla anti-fragmentación:** si dos frentes necesitan lo mismo (un esquema de datos, una pieza, un agente), se construye UNA vez y se referencia por ID. El mapa existe para que la mano izquierda sepa lo que hace la derecha.
3. **Herencia del suelo:** IronClaw, soberanía del dato, grounding y honestidad sin hype rigen en los seis frentes sin excepción. Este mapa no crea permisos nuevos; ordena los existentes.

## §1 · LOS SEIS FRENTES (estado 18-jul-2026)

| # | Frente | Qué es | Fase hoy | Puerta siguiente |
|---|---|---|---|---|
| F1 | **El PC Soberano** | Cerebro central de cómputo y comunicación (Beelink SER9 Max, 64GB) | Day-0: primer arranque | **G0** — SO + bench + fila de Orquesta |
| F2 | **Chat P0X** | Acceso a la AI local con filosofía P0X (aprendizaje y desarrollo humano) | Diseño de alfa | **Alfa hermanos** vía OpenWebUI |
| F3 | **Hexelion físico** | Impresora + piezas paramétricas del jardín, validadas por la física | Espera hardware (Bambu llega 24-28 jul) | **Test de tolerancias** |
| F4 | **Gemelo casa-jardín** | Mapa de la casa + sensores + cuidado del jardín asistido | Diseño de esquema de datos | **Esquema canonizado** + M5 Fase 4 |
| F5 | **Voz pública** | Posts/LinkedIn redactados por agentes Hexelion, publicados por el carbono | Manual asistido | **Primer post** con flujo propose→firma |
| F6 | **Red de nodos soberanos** | Comunidad DePIN solar-punk con human-in-the-loop | Horizonte declarado | **No se construye** hasta F2-beta validada |

## §2 · F1 — LA GRADUACIÓN DEL PC SOBERANO (el control total se gana, no se declara)

**El destino:** la AI del PC Soberano escribe y ejecuta en el rack; el carbono verifica órdenes y resúmenes; Claude Code queda para lo que exceda al modelo local; Claude app (el Preceptor) queda en chat, verificación y doctrina — que ya es su sitio según la Orquesta ("jamás ejecuta en el rack"). **El camino:** el patrón de puertas de la casa (Reflejos R0-R3, rito de transplante) aplicado a un rol ejecutivo.

- **G0 · Cuerpo** (hoy): Ubuntu Server 24.04, Tailscale, Ollama con `qwen3-coder:30b` (tag explícito; `num_ctx` demostrado por dato — jamás el default de 256K). Bench CPU vs Vulkan como línea base en `mente/telemetria/`. Fila propuesta en ORQUESTA_MODELOS §1. Hostname: `pc-soberano` (el nombre completo para la prosa; el corto para las máquinas — y para no confundir al Soberano de carne con el de silicio en los textos).
- **G1 · Ojos**: acceso SSH de **solo-lectura** a fragua/torre/vigía. Misiones: diagnósticos, inventarios, resúmenes de estado. **Eval de cruce:** 10 diagnósticos verificados por el carbono con cero dato inventado — grounding perfecto o no cruza.
- **G2 · Manos que proponen**: genera diffs, scripts y patches como artefactos versionados; los aplica CC o el carbono. **Eval:** 10 artefactos aplicados sin corrección mayor.
- **G3 · Manos supervisadas**: ejecuta en el rack heredando la disciplina de CC (Doctrina AI Interna §4): git obligatorio, backup antes de tocar la cara visible, PARA-y-reporta, commit por bloque. **Eval:** 5 misiones con rollback limpio disponible y reporte contrastado fiel.
- **G4 · Sustitución rutinaria**: toma las misiones rutinarias de Claude Code. El token de frontera queda para arquitectura, doctrina y lo que el local no alcance — **medido, no supuesto** (comparativa de tasa de éxito local vs CC en misiones equivalentes).

**Harness agéntico** (decisión de G0→G1, por bench): candidatos **Qwen Code** (agente terminal optimizado para Qwen3-Coder), **OpenCode** y **Aider** — los tres sobre Ollama. Se elige con 5 misiones read-only idénticas y métrica dura: aciertos, alucinaciones, tokens, minutos.

**Invariantes en todos los gates:** jamás firma valor (IronClaw) · `num_ctx` demostrado · telemetría por misión · reporte legible en español (el valor jamás viaja comprimido) · un job pesado a la vez · toda salida hacia el carbono es verificable contra el estado real.

## §3 · F2 — CHAT P0X (de hermanos a comunidad)

**Alfa (hermanos, ya):** OpenWebUI en el PC Soberano, ligado **solo al tailnet**; una cuenta por hermano. El system prompt v0 es un **STUB honesto** hasta que el corpus de psicología esté procesado (la mecánica se deriva, no se decreta), con cuatro principios operables desde hoy: guiar al esquema (que el usuario ordene su proyecto por escrito), retrieval de lo suyo (que no pierda resultados), gestión de recursos (sugerir la herramienta gratuita adecuada — Gemini u otra específica — cuando toque, según su hardware), y cerrar cada sesión con un paso pequeño siguiente.

**El patrón mini-códice** (la mecánica del "no perder el tracking"): cada usuario tiene su propia colección aislada. Al cierre de sesión, el chat propone un **delta de tu proyecto** ("hoy avanzaste X, decidiste Y, queda Z") que el usuario aprueba o corrige — el lazo Observar de P0X aplicado a cada humano. Su memoria es suya: **exportable y borrable**, como el Códice del Soberano. La soberanía o es simétrica o es marketing.

**Contrato de datos del hermano** (visible en el primer login, cinco líneas): qué se guarda, dónde vive físicamente (este rack, Lisboa), quién puede leerlo, cómo se exporta, cómo se borra.

**Beta (pocas personas, solo tras telemetría de alfa):** entrada por **invitación con aval humano** — el grafo de confianza ES la verificación de humanidad en esta fase; la atestación por hardware soberano es horizonte F6, no requisito. Aviso real: con no-familiares, David pasa a ser responsable del tratamiento (GDPR) — minimización, consentimiento explícito, derecho a borrado. No es burocracia: es la legitimidad del producto.

## §4 · F3 — HEXELION FÍSICO (la física como juez)

1. **Estándar de ingeniería:** la Parte 4 del documento HEXELION (patrón repositorio, type hints, docstrings Google, TDD con pytest) se propone como canon para todo pipeline Python del sistema. Las piezas tienen su propio juez: checks dimensionales en CI + validación física en la Bambu.
2. **Flujo de pieza:** prompt → `.scad` paramétrico → print → validación física (tolerancias, encaje, resistencia) → registro en `mente/` con fotos y medidas. **Nada se publica sin haber existido.**
3. **El experimento tomate** (que "más tomates" sea dato, no anécdota): n=1 no prueba causalidad. Diseño mínimo honesto: misma variedad, mismo sustrato, misma agua (medida por sensores), maceta control vs air-pruning, mismo sol (BH1750 como testigo). Métrica: gramos cosechados + estado radicular al final. Una temporada, un resultado citable — y si el resultado es "no hay diferencia", se publica igual.

## §5 · F4 — GEMELO CASA-JARDÍN

1. **Esquema primero:** zonas de la casa → dispositivos → sensores → series temporales. El mapa de la casa entra a `mente/` como esfera con front-matter; las series viven en telemetría. La decisión de motor de series (Redis streams vs InfluxDB vs alternativa) se delibera **con volumen real medido**, no antes.
2. **Ingesta:** M5 Fase 4 (pendiente) + los ESP32/BH1750/BME680 nuevos + NPK 8-in-1 cuando llegue (11-19 ago). **El Vigía no se reasigna:** los SDR se quedan donde están; el doc HEXELION proponía otra cosa y se descarta.
3. **Gradiente de actuación física A0-A2** (separado del invariante de firma: la bomba no firma valor, pero puede inundar la terraza): **A0** propose-only — la AI recomienda, el carbono actúa. **A1** timers aprobados — Shelly/MOSFET con horario firmado por el carbono. **A2** auto acotado — solo tras ≥4 semanas de propuestas A0/A1 validadas, con límites duros de caudal/tiempo, histéresis, y kill-switch físico. El riego automático se gana como el control total: por historial. Los reflejos del jardín heredan el patrón de Reflejos (sensor→umbral→acción protectora, sin LLM en el lazo, el Monje narra post-hoc).

## §6 · F5 — VOZ PÚBLICA

Los agentes Hexelion redactan (posts, LinkedIn, fichas MakerWorld); el carbono edita y publica. Mismo patrón propose→firma de todo P0X, con registro de lo publicado en `mente/`. Puerta previa a cualquier publicación **monetizada**: lectura de la cláusula IP del contrato vigente — diez minutos que aseguran F3 y F5 enteros, porque las cláusulas típicas cubren lo que se **crea y publica durante** el empleo, no solo lo que genera ingresos.

## §7 · F6 — RED DE NODOS SOBERANOS (horizonte con condiciones)

**La visión del Soberano:** nodos conectados con dos canales — *qué proyecto puede ayudarte a construir este nodo* y *qué puede ofrecer* (cómputo, contacto privado, datos físicos verificados) — una comunidad solar-punk a distancia con human-in-the-loop como ground truth, que guarda datos de la realidad física.

**Condiciones de arranque (ninguna cruzada hoy):**
1. F2-beta validada con personas fuera de la familia (telemetría de uso real, no promesas).
2. Identidad por **grafo de invitación** (humanos avalan humanos) antes que cualquier atestación por hardware — la atestación llega cuando haya red que atestar.
3. **Simetría de soberanía como ley de diseño:** cada nodo guarda su códice local; al servidor central solo viaja señal **consentida, minimizada y agregada**, exportable y borrable por su dueño. Si toda la memoria de la red viviera en un solo servidor, habríamos reconstruido lo que combatimos — con mejores intenciones, que es como siempre empieza.
4. Tokenización sigue descartada (canon jul-2026): el incentivo de alfa y beta es valor de uso — la ayuda humana compartida remotamente ES el incentivo — no especulación.

## §8 · DEPENDENCIAS (qué desbloquea qué)

G0 del PC Soberano → F2-alfa y G1 · Bench + evales G1-G3 → G4 (sustitución rutinaria de CC) · M5 Fase 4 → ingesta F4 · Bambu (24-28 jul) → tolerancias F3 → primer item (Clip Evolutivo) · Corpus procesado → system prompt P0X v1 (F2) + mecánica Repasar · Cláusula leída → F5 monetizada + Partes 1/3 de HEXELION · F2-beta OK → diseño F6 · NPK 8-in-1 (11-19 ago) → jardín instrumentado completo.

## §9 · CHANGELOG

- **0.1.0 (2026-07-18)** · Propuesta inicial del Preceptor a petición del Soberano: seis frentes con fases y puertas, graduación G0-G4 del PC Soberano bajo el patrón de puertas de la casa, mini-códice y contrato de datos en F2, experimento tomate en F3, gradiente A0-A2 en F4, condiciones de F6. Pendiente de canonización.
