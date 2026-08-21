# HEXELION · contexto archivado · no es acción

> **PRIVADO · Nivel 2.** Archivado el **2026-08-21** para cuando el Dominio 1
> cierre la Fase 3. **Nada de esto se ejecuta ahora.** El producto público no
> conoce este fichero.

## §1 · Roadmap firmado · V4 → V1 → V2 → V3

Firmado por el Soberano el 2026-08-21, con el orden invertido respecto al
original y por el motivo medido:

| | Vector | Por qué ahí |
|---|---|---|
| 1º | **V4 · auto-canonización** | Ataca la causa raíz medida: 3 609 tokens contra 5,9 M de parámetros. |
| 2º | **V1 · Sínodo con `llama.cpp`** | Voces baratas sobre un base cargado una vez. **No Punica: es CUDA y aquí no hay NVIDIA.** Prerrequisito del V2. |
| 3º | **V2 · compresión** | Solo paga si V1 decide **no** fusionar. Con fusión, el teléfono recibe 2,3 GB con adapter de 22 MiB o de 2 MiB, igual. |
| 4º | **V3 · long-context** | Destino Beelink, no Doogee: 8k de prompt a 5,25 tok/s son ~26 min solo de leer. |

**Detalle de calendario, señalado en `DECISION_A_O_B.md` §4:** la regla «nada se
ejecuta hasta cerrar Fase 3» y la dependencia «Fase 3 necesita datos, los datos
necesitan V4» se bloquean entre sí. V4 necesita ser excepción explícita, no un
salto silencioso.

## §2 · Fuentes VERIFICADAS · ya usadas en el sprint

**`obra/superpowers` — metodología agentiva, *writing-good-tests*.**
Las tres reglas están **aplicadas y con resultado medible** en
`pruebas/guardian_tester.py`:

- *Falsifiabilidad*: cada uno de los 12 casos lleva su campo `ruptura`, que
  nombra qué se rompe si falla.
- *No string-presence*: descartó el grep y obligó a la medida por elección entre
  dos continuaciones, comparando log-verosimilitud media por token.
- *Change-detector*: es la que dio el hallazgo de la ronda. Cruzar contra el base
  reveló que 5 de 12 casos son **redundantes** —no miden el LoRA, miden a
  Qwen3— y que EC-2.4 es una **regresión**. Sin esta regla, el informe habría
  dicho «3/5, 1/4, 2/3» y nadie habría visto que el adapter empeoró el fusible.

**`alan2207/bulletproof-react` — arquitectura robusta, `AGENTS.md`.**
Aplicable cuando se publique `EVALUATION_DOCTRINE.md`.

## §3 · Fuentes DECLARADAS POR TERCEROS · sin verificar en este nodo

Marcadas según la regla 9 del `PRECEPTOR.md`: lo que dijo un tercero va con su
fecha y **no sostiene ninguna decisión** hasta que alguien lo comprueba y anota
con qué.

- **Gentleman Programming** (`Gentleman.Dots`, `gentle-ai`, `engram`) —
  `SIN VERIFICAR`, declarado 2026-08-21. Comunidad hispana, configuración local
  de herramientas de IA.
- **Platzi** (`topic:platzi-course`) — `SIN VERIFICAR`, declarado 2026-08-21.
  Educación técnica hispana, contenido modular.
- **EU AI Act · Reglamento (UE) 2024/1689** — `SIN VERIFICAR`, declarado
  2026-08-21. Se citan transparencia (Art. 50), supervisión humana (Art. 14),
  robustez (Art. 15) y trazabilidad (Art. 12) para alto riesgo.
  **No he leído el texto legal desde este nodo y no confirmo ni la numeración ni
  el alcance de los artículos.** Antes de que una sola decisión de producto se
  apoye en esto, lo lee alguien con el reglamento delante — y si hay
  consecuencias legales reales, un jurista, no un modelo.

## §4 · Cuándo se usa cada cosa

| Fuente | Momento |
|---|---|
| Gentleman · Platzi | Al diseñar comunidad alrededor de Aurelius · post-Fase 4, post-release |
| EU AI Act | **Solo si** Aurelius pasa a evaluar o recomendar de forma que afecte al acceso a oportunidades educativas o laborales. Hoy es un compañero de memoria y no entra en esa categoría. |
| `AGENTS.md` de bulletproof-react | Al publicar `EVALUATION_DOCTRINE.md` en el repo público |

**Observación sobre el disparador del AI Act**, para que no se cruce sin darse
cuenta: hoy el producto mide un Camino de ocho peldaños y dice dónde estás. Eso
es progreso propio, y no afecta al acceso de nadie a nada. **La línea se cruza
el día que ese progreso se enseñe a un tercero** —un empleador, una escuela— o
se convierta en credencial. Merece ser una decisión consciente y con fecha, no
una consecuencia de haber añadido una función de exportar.

## §5 · `EVALUATION_DOCTRINE.md` · NO_DATA

Sigue citado como congelado, esperando corrección de dos divergencias y decisión
sobre publicar el tester. **El fichero no existe en este nodo.** Busqué en todo
el home. Sin él delante no puedo corregir nada ni opinar sobre su publicación.

Si vive en otra máquina, se trae; si se perdió, se declara perdido. Lo que no
puede seguir es citado como congelado sin que nadie sepa dónde está.
