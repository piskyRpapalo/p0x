---
id: proyecto-reflejos
titulo: Proyecto Reflejos — del PIR a una base con evidencia
tipo: esfera
clase: operativo
version: 1.0.0
editor_autorizado: silicio-telemetria
dominio: investigacion-reflejos
nivel: nuevo
metrica_exito: "cada pista avanza solo por puerta superada con dato; cero afirmaciones de control latente sin hit/anti-hit medidos"
umbral_reedicion: "resultado de una puerta (R0-R3) o evidencia nueva de la literatura"
presupuesto_kb: 26
n_medicion: 1
enlaces:
  - alfabeto-p0x
  - doctrina-evales-transplante
  - edge-ai
  - orquesta-modelos-p0x
descripcion_niveles:
  basico: "Queremos que el sistema tenga 'reflejos': reacciones rápidas sin pensar en palabras. Hoy los hacemos con reglas simples y sensores reales; el sueño de controlarlos dentro del cerebro del modelo se investiga por etapas, con pruebas."
  medio: "Proyecto en tres pistas: reflejos deterministas (sensor→umbral→acción sin LLM), dataset p0xlang de intención+consenso+resultado, y probing/steering de activaciones en SLM open-weights con puertas de evidencia."
  experto: "Reformulación del PIR tras contraste con literatura: steering no-determinista (~1/3 anti-steerable), no-identificabilidad de vectores (null space del Jacobiano), lens con deriva de base, y transferencia cross-model negativa. Base construible: arcos deterministas + dataset transplantable con vectores como cache model-bound + probing gated R0-R3 con clusters semánticos re-calibrables."
actualizado: 2026-07-08
---

# PROYECTO REFLEJOS
### El PIR, pasado por el filtro de evidencia — y convertido en base escalable
*Propuesta original: el Soberano (PIR, 8-jul-2026). Veredicto y reformulación: el Preceptor. El Soberano trajo él mismo contra-evidencia (negative result de transferencia cross-model) — así se propone en P0X.*

## §0 · VEREDICTO DE EVIDENCIA (por qué el PIR literal no se firma hoy)

1. **Steering ≠ determinista**: ~1/3 de muestras se mueven en dirección CONTRARIA ("anti-steerable"); efecto y fiabilidad varían fuerte entre datasets (ICLR'25, *Understanding (Un)Reliability of Steering Vectors*). → Todo KPI de acierto mide también **anti-hit**.
2. **No-identificabilidad**: infinitas direcciones distintas producen la misma conducta (null space del Jacobiano activación→salida); que un vector funcione no prueba que sea "el circuito" (*Non-Identifiability of Steering Vectors*, 2026). → Los "Reflejos" se definen como **clusters semánticos re-calibrables** (idea del Soberano, correcta), jamás como activación exacta.
3. **La lente tiembla**: logit lens poco fiable en capas tempranas y con deriva de base; usar **tuned lens** o corrección equivalente (Belrose'23 y sucesores).
4. **Sin inyección inter-nodo**: los vectores están casados con modelo+checkpoint; la transferencia cross-model tiene resultado negativo (fuente aportada por el Soberano). Coherente con doctrina-evales: **el alma transplantable = intención+dataset+resultado; los vectores son cache del cuerpo.**
5. **Baseline honesto**: todo KPI de latencia/ancho de banda se compara contra el **Alfabeto** (ya comprimido y medido), no contra prosa verbosa.

## §1 · PISTA A — REFLEJOS DETERMINISTAS (hoy; el arco espinal)

En biología el reflejo no pasa por el córtex. Aquí tampoco: **sensor→umbral→acción protectora→evento a consola, SIN LLM en el lazo.** El pacing térmico (#20) es el Reflejo-0 ya vivo. Siguientes: `reflejo-bateria` (UPS OB/LB → pausar cola batch + aviso), `reflejo-termico-m5` (BME680 sobre umbral → aviso), `reflejo-vibracion` (ADXL345 Δ|g| → evento "movimiento detectado"). Reglas: solo acciones protectoras/operativas (jamás valor), registradas en `mente/telemetria/reflejos.jsonl`, definidas cada una en un MD operativo con umbral, acción e histéresis. El Monje los NARRA (informado post-hoc), no los ejecuta.

## §2 · PISTA B — DATASET p0xlang (el alma, desde ya)

Esquema de registro (diseño del Soberano, enmendado):
```json
{
  "intent_prompt": "…",                       // intención en claro o pseudo-p0xlang
  "synod_proposals": [ {"voz":"…","frag":"…"} ],
  "consensus_weights": {"…": 0.4},
  "latent_cache": {                            // ENMIENDA: cache ligado a cuerpo, NO portable
    "modelo": "qwen3-4b-instruct-2507@q4_K_M", // huella obligatoria estilo md@ver
    "capa": 18, "vectores_ref": "ruta/npz", "aviso": "no transferible entre modelos"
  },
  "compiled_ast": "…",                         // hexelion-lab como Compilador de Intención
  "resultado": {"valida_shape": true, "exito": true, "medidas": {"ms":…, "tokens":…}}
}
```
Lo transplantable (sobrevive a cambios de modelo): `intent + proposals + consensus + ast + resultado`. El **filtro duro v1** es la validación determinista de shape/resultado (Alfabeto `out`); el filtro por probe se gana en la Pista C. **Retroalimentación**: fallo → penaliza el peso del enlace intención→reflejo; éxito → refuerza (registro, no auto-edición de doctrina).

## §3 · PISTA C — J-SPACE PROBING (investigación con puertas, en los HP)

SLM **open-weights** (familia Qwen pequeña / Pythia) cargado con `transformers` + hooks, en los HP x86 (extiende el Gate 0 pendiente). **Nunca en el camino crítico** (regla del Soberano, canonizada): solo tareas de alta prioridad/infra cuando esté maduro.

| Puerta | Qué debe ser verdad para cruzarla |
|---|---|
| **R0 · Toolchain** | Los hooks extraen activaciones del SLM en el HP (shapes correctos, coste medido) |
| **R1 · Lectura** | Un probe (con corrección tipo tuned-lens) distingue un estado conocido (p.ej. tarea=delta vs rag) en held-out con acierto declarado |
| **R2 · Escritura** | Steering de UNA conducta en NUESTRA tarea: hit-rate Y anti-hit-rate medidos contra baseline Alfabeto; monitor de deriva aborta si la activación no coincide (failsafe del Soberano) |
| **R3 · Compilación** | Solo entonces: p0xlang → cluster semántico de activaciones, con re-calibración automática por versión de modelo |

**MoA/Sínodo (nota honesta):** las voces comparten modelo base → el intercambio latente *intra-modelo* (prefijos/estado compartido) es la esquina plausible; el inter-familia tiene resultado negativo. El consenso MoA empieza secuencial (propuestas encoladas), mismo cuerpo, personas distintas.

## §4 · KPIs (corregidos, baseline = Alfabeto)

Latent-Hit **y Anti-Hit** por cluster de tarea · Densidad lógica (ops de control/token) · Deriva (<umbral declarado, con monitor-failsafe) · Latencia y bytes vs **prompt Alfabeto equivalente** (no vs prosa) · Alineación (coseno) SOLO acompañada de éxito conductual en tarea (la similitud sola no prueba nada, §0.2).

## §5 · FRAGMENTACIÓN EN EL SECOND BRAIN

Hoy: esta esfera única. Al cruzar R1 → se escinde en `esfera:p0xlang-dataset` y `esfera:j-space`. Cada Reflejo determinista de la Pista A nace como MD operativo propio (tipo tecnica) enlazado aquí. Los fracasos de puertas van a la Necrópolis con motivo — un R2 fallido es dato, no vergüenza.

## ZONA EVOLUTIVA
> Resultados de puertas, costes medidos, literatura nueva. Cambios con hipótesis y dato (Protocolo §3).

*(v1.0.0 — archivado como proyecto; profundizar = cruzar puertas, no acumular fe)*
