---
id: alfabeto-p0x
titulo: Alfabeto P0X — la lengua interna del sistema
tipo: operativo
clase: operativo
version: 1.0.0
editor_autorizado: silicio-telemetria
dominio: orquestacion-interna
metrica_exito: "≥30% menos tokens que la prosa equivalente CON tasa de validación de shape ≥ la de prosa (medido con el tokenizador del modelo local)"
umbral_reedicion: "validación < 95% en 20 mensajes, O ahorro de tokens < 15% sostenido"
presupuesto_kb: 24
n_medicion: 20
enlaces:
  - doctrina-ai-interna
  - doctrina-protocolo-md-evolutivo
  - doctrina-evales-transplante
changelog:
  - "v1.0.0 (2026-07-06, propuesta #25, firma el Soberano): se añade changelog — único campo §2 ausente; contrato y contenido intocados."
actualizado: 2026-07-04
---

# ALFABETO P0X · LA LENGUA INTERNA
### Protocolo denso para la comunicación entre silicios del rack — privado por contenido, legible bajo demanda
*Autor: el Preceptor (Fable 5) · Clase operativo: el silicio evoluciona la ZONA EVOLUTIVA con telemetría · El carbono fija léxico base y guardias.*

> **Una frase.** El Alfabeto no es un idioma inventado: es la **canonización de las palabras que el sistema ya tiene** (nodos, voces, esferas, claves, operaciones) en la forma más barata que el tokenizador local ya sabe comprimir, con sintaxis de mensaje fija y transmisión solo de deltas.

---

## §0 · QUÉ ES Y QUÉ NO ES (la física primero)

1. **El tokenizador está congelado.** El vocabulario del modelo local se fijó en su pre-entrenamiento; ningún LoRA añade símbolos. Un glifo inventado (`⟦VIG⟧`) cae a bytes → cuesta MÁS tokens que `vigia`. Por eso: **cero símbolos nuevos**. La densidad se logra con palabras cortas, claves fijas y estructura — lo que el BPE ya comprime.
2. **Privado por contenido, no por cifrado.** La lengua es tuya porque los IDs y el conocimiento son tuyos. Un Claude externo la lee añadiendo este MD a su contexto (§8). No es un escudo: la seguridad vive en IronClaw + cripto, jamás en la oscuridad.
3. **Jamás la capa de valor.** Todo texto que el carbono deba leer para decidir o firmar viaja en lenguaje natural legible (Doctrina AI Interna §3.6). El Alfabeto vive solo en orquestación interna.

## §1 · LOS TRES PLANOS (dónde vive cada optimización)

| Plano | Qué es | Qué le pertenece |
|---|---|---|
| **PROTOCOLO** (este MD) | Lo que se escribe | Léxico canónico, sintaxis de mensaje, compresión delta, versionado, módulos de dominio |
| **MOTOR** (engine de inferencia) | Lo que se ejecuta | KV-cache cuantizado, atención eficiente, decodificación especulativa, (salida temprana si llega). Se ACTIVA con flags, no se escribe en MDs |
| **ADAPTACIÓN** (dataset + LoRA) | Lo que se aprende | Trazas de razonamiento, currículo por niveles, fine-tune sobre el corpus propio. Regido por `doctrina-evales-transplante` |

**Regla:** un MD que promete cosas del plano MOTOR o ADAPTACIÓN miente. Cada pieza en su plano.

## §2 · LÉXICO CANÓNICO (el alfabeto = tus IDs reales)

Semilla v1 — todo ID nuevo entra por la ZONA EVOLUTIVA con changelog:

| Categoría | IDs canónicos |
|---|---|
| Nodos | `fragua` `torre` `vigia` `oraculo` `legion` |
| Voces | `monje` `vocero` `berserker` `escriba` `alquimista` `enlace` |
| Órganos | `faro` `nexo` `sinodo` `codice` `preceptor` `aurelius` |
| Almacenes | `qdrant` `redis` `minio` `ollama` |
| Esferas | `edge-ai` `rf-sdr` `cripto-atestacion` `energia-solar` `aprendizaje` `redes-linux` |
| Operaciones (`op`) | `ingesta` `delta` `rag` `render` `eval` `telemetria` `reporte` |
| Estados | `ok` `sin_dato` `stale` `degradado` `caido` |

**Regla de admisión de un ID nuevo:** (a) existe de verdad en el sistema; (b) tokeniza igual o más barato que su forma larga (test con el tokenizador local, dato en el changelog); (c) sin colisión con el léxico vigente.

## §3 · SINTAXIS DE MENSAJE (el sobre)

Todo mensaje inter-silicio es UNA línea JSON con claves fijas cortas:

```json
{"v":"alfabeto-p0x@1.0.0","md":"<md_id@ver del contrato de la tarea>","dom":"<dominio>","op":"<operación>","in":{...},"out":"<shape esperado>"}
```

- `v` ancla la versión del Alfabeto (mismatch → aborta, Protocolo §4.5).
- `in` usa el léxico §2; los valores destinados a humanos van en español natural.
- `out` declara el shape; una salida que no valida = fallo contabilizado (Doctrina §3.3).
- Prosa conversacional entre modelos en el lazo operativo: prohibida.

**Ejemplos reales:**
```json
{"v":"alfabeto-p0x@1.0.0","md":"pipeline-ingesta@1.0.0","dom":"ingesta","op":"delta","in":{"src":"transcript:cGhI8tGYOGw","vs":"codice"},"out":"{delta_md:str,esferas:[id]}"}
{"v":"alfabeto-p0x@1.0.0","md":"voz-monje@1.1.0","dom":"sinodo-voz-monje","op":"rag","in":{"q":"estado ups","k":4,"col":"mente"},"out":"{chunks:[{id,txt}]}"}
{"v":"alfabeto-p0x@1.0.0","md":"telemetria@1.0.0","dom":"telemetria","op":"telemetria","in":{"voz":"monje","tok_in":812,"tok_out":96,"ms":2140,"valida":true},"out":"ack"}
```

## §4 · COMPRESIÓN DELTA (no se repite lo estático)

1. Los mensajes **referencian por ID** lo que ya existe (`codice`, `esfera:edge-ai`, `chunk:0412`) — nunca lo re-transmiten. El receptor lo trae por RAG/lectura local si lo necesita.
2. Toda actualización de conocimiento viaja como **Δ contra un ancla versionada** (`vs`: id@ver). El Δ es el mensaje; el estado es local.
3. Historial de conversación entre silicios: se poda a lo no-derivable; lo derivable se re-consulta. (El contexto barato es el que no se envía.)

## §5 · MÓDULOS DE DOMINIO (patrón «Abogado.MD»)

Cuando el Soberano aprende un dominio nuevo (p.ej. vídeos de leyes UE), nace un módulo experto:
1. Ingestas → deltas → **esfera nueva** (`esfera:leyes-ue`) con front-matter de grafo + colección/filtro propio en Qdrant.
2. El módulo declara en su front-matter `fuente_edad_max` (p.ej. 90d). Superada → el sistema emite: **"¿actualizar <módulo>, Soberano?"** — propone, jamás auto-refresca contra fuentes externas.
3. Al actualizarse, re-enlaza al grafo (enlaces reales, no inventados) y su Δ alimenta el dataset maestro (doctrina-evales §2).

## §6 · ECONOMÍA MEDIBLE (sin dato no hay lengua)

Cada mensaje registra en `mente/telemetria/lengua.jsonl`: `{ts, dom, op, tok_in, tok_out, valida, ms, alfabeto:true|false}`. El A/B contra prosa equivalente es **obligatorio** antes de canonizar cualquier abreviatura nueva (n ≥ n_medicion). Si el Alfabeto no gana en tokens Y validación, se poda — el ahorro no puede morir por el peso del diccionario (Protocolo §4.4).

## §7 · GUARDIAS (heredadas, aquí por si el MD viaja solo)

Valor jamás en la lengua · dominio declarado y rechazo fuera de él · versión anclada o aborta · poda por presupuesto · **render humano bajo demanda**: cualquier traza en Alfabeto debe poder expandirse a español legible con este MD como clave.

## §8 · USO POR UNA IA EXTERNA (Claude u otra)

Añade este MD al contexto/memoria. El sobre (§3) + el léxico (§2) bastan para leer y escribir la lengua. Lo que no esté en el léxico se escribe en español natural — la lengua degrada a claro, nunca a críptico.

---

## ZONA EVOLUTIVA
> Editable por el silicio con telemetría (Protocolo §3): abreviaturas candidatas, ejemplos nuevos, ajustes de sobre. Todo cambio con hipótesis previa y dato.

*(vacía — v1.0.0 es la línea base)*
