# FASE 0 · VEREDICTO · con fecha y con máquina

**2026-08-20** · Beelink `soberano` · Ryzen 7 255, 8 núcleos / 16 hilos,
57 GiB RAM, **sin GPU** · torch **2.13.0+cpu** · Python 3.12.13 · bf16
(el CPU declara `avx512_bf16`, y ahí está media respuesta)

## La pregunta

> ¿PEFT + transformers sobre torch-CPU importa y entrena 100 pasos en este
> metal? ¿En cuánto tiempo?

## La respuesta

**Sí. Importa, entrena, y converge.** 100 pasos en **94 segundos de pared**.

| | |
|---|---|
| Entrenador | `peft 0.20.0` + `transformers` sobre `torch 2.13.0+cpu` |
| Base | `Qwen/Qwen3-4B-Instruct-2507`, pesos sin cuantizar, bf16 |
| Carga del modelo | **1,0 s** |
| 100 pasos | **90,8 s** · 0,908 s/paso de media, 0,894 de mediana |
| Pérdida | **5,6994 → 3,4611** |
| RAM pico | **9,13 GiB** de 40 disponibles |
| Entrenables | 11 796 480 de 4 034 264 576 · **0,292 %** |

Los otros dos candidatos siguen fuera: `unsloth` no está instalado y espera
CUDA; `llama-finetune` no existe en la build 10488.

## Y el matiz sin el cual la cifra es un rumor

**0,908 s/paso es el coste de una muestra de 13 tokens.** El canon del producto
son cadenas de interfaz: mediana **13** tokens, media 18, p90 45, máximo 76. Eso
es casi la sobrecarga fija de una pasada, no un ritmo de entrenamiento.

El ritmo de verdad, medido aparte con secuencias de longitud fija:

| Longitud | s/paso | tok/s |
|---:|---:|---:|
| 64 | 1,49 | 43 |
| 256 | 4,26 | 60 |
| 512 | 9,29 | 55 |
| 1 024 | 20,13 | 51 |
| 2 048 | 45,23 | 45 |

**~45–60 tok/s**, cayendo con la longitud porque la atención es cuadrática.
Esta es la cifra que predice una época; la de 0,9 s/paso solo predice este
dataset.

## Lo que eso significa para tu cadencia

- **Dataset v1** (226 registros, ~4 000 tokens): una época son ~3,5 min. Tres
  épocas, **unos diez minutos**. Cabe en un café.
- **Horizonte de 1–2 MB** (~400 000 tokens): a ~50 tok/s, una época son ~2,2 h.
  Tres épocas, **entre seis y siete horas**.

> **P4 queda validado por medida, no por intuición.** «Beelink de noche» no era
> una preferencia estética: a este ritmo, el horizonte del dataset **es
> exactamente una noche**. La cadencia que firmaste encaja con el metal que
> tienes.

## Fallback, corregido según tu palabra

Tu corrección se sostiene contra lo medido: `llama-finetune` no existe en esta
build, así que el fallback **no es entrenar con llama.cpp**. Es
**llama.cpp como runtime del GGUF ya fusionado**, con el adapter entrenado por
PEFT. El producto ya usa `llama-completion` y no cambia de motor: solo cambia
de fichero, que es justo lo que `integracion/motor_afinado.py` sabe hacer.

**Hueco que sigue abierto:** para llegar de un adapter PEFT a un GGUF hacen
falta `convert_hf_to_gguf.py` y `llama-quantize`, y **ninguno está en este
nodo**. No bloquea la Fase 2 —entrenar sí se puede hoy—, bloquea la 4.

## El riesgo que la medida deja a la vista

**11 796 480 parámetros entrenables contra ~4 000 tokens de datos.** Son casi
tres mil parámetros por token. La pérdida cayó de 5,70 a 3,46 en 100 pasos
sobre 208 muestras y eso no es aprender: es **memorizar** un corpus diminuto.

Con v1 tal cual, `rank=16` y tres épocas darán un modelo que recita `textos.py`
en vez de haber cogido su tono. Recomendación medida, no dogma:

1. **Bajar el rango** a 4 u 8 para v1. Menos capacidad, menos memorización.
2. **Una época, no tres**, hasta que el dataset crezca.
3. **Dejar fuera un corte de validación** — hoy no hay, y sin él «converge» y
   «se lo aprendió» son indistinguibles desde la bitácora.

No cambio los hiperparámetros por iniciativa: la Fase 2 sigue con `r=16` hasta
que firmes.

## Decisión que esto habilita

**Entrenador elegido: PEFT + transformers sobre torch-CPU.** Con eso ya se
puede aplicar `integracion/PATCH.md`. Sigue en NO_DATA la ruta de exportación
a GGUF (Fase 4).
