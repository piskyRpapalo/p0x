# checkpoint · triaje

Un solo trabajo: decir a que clase pertenece una consulta, en una palabra, del
vocabulario cerrado `simple | codigo | analisis | conversacional`.

**Modelo:** `preceptor-cazanido-v3:llama3.2` (2 GB). Elegido por medida, no por peso.

| # | criterio | falla si |
|---|---|---|
| A | Se queda en el vocabulario | Devuelve una palabra que no es una de las cuatro. Medido: `llama3.2:3b` invento «Interactivo» |
| B | Clasifica, no se niega | Contesta `NO_DATA` pudiendo clasificar. Medido: `preceptor-v7:llama3.2-1.0` responde `NO_DATA.` a TODO |
| C | Una palabra, sin prosa | Explica su eleccion. El triaje se consume por codigo: la prosa es ruido que hay que parsear |
| D | Etiqueta `arnes: triaje` | No declara de que arnes viene su medida |

## Por que este espacio existe

Porque el enrutador decide **quien contesta**, y un enrutador que se equivoca hace que
se culpe al modelo de destino por un fallo que fue del reparto. Aqui se mide al que
reparte.

## La regla que este espacio hereda del enrutador

**Determinista primero.** El modelo de triaje solo entra cuando la heuristica no se
moja. Preguntar a un LLM lo que decide una regla es pagar por una respuesta que ya
tenias, y ademas introduce una alucinacion posible donde no habia ninguna.

## Fuente

- **estado:** 🔴 `NO_DATA · sin conversaciones`
- **causa:** el espacio nace hoy. Se llenara cuando el enrutador empiece a registrar
  sus decisiones con el veredicto de si acerto.
- **arnes:** `triaje`
