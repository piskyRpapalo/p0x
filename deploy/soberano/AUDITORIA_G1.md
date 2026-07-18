# Auditoría de conexiones propuestas · Misión G1, Bloque B (2026-07-18)

## Método y adaptación declarada

`run_audit.sh` (skill auditora) asume rutas de `la-fragua` — no ejecutable limpio desde `soberano`.
Adaptación: auditoría en modo lectura vía **HTTP directo** a los servicios de `la-fragua`
(gateway `:8001`, Qdrant `:6333` con `QDRANT_API_KEY` provista por el carbono y verificada byte
a byte antes de usarla) más el repo git ya clonado — sin SSH a fragua (no autorizado en esta
misión). Node existence se verificó contra los `id:` de front-matter reales del repo (fuente de
verdad más directa que el `second_brain.json`, que es `mente/grafo/second_brain.json`,
gitignorado y solo regenerable en fragua).

## Hallazgo previo (afecta a todo lo demás): `hexelion.git` estaba en la rama equivocada

En G0 se clonó y quedó fijado en `origin/main`. **`main` está abandonada desde 2026-06-21**
(commit `a668ccd`) — **54 commits por detrás** de `nexo-carbono-dashboard-20260623`, que es donde
vive todo el desarrollo real desde entonces (último commit `0918fb9`, 2026-07-14 — literalmente
el fix de #22). Existe también el tag `dashboard-estable-20260711` sobre esa misma línea. La rama
`dashboard-honestidad-20260622` también está estancada.

**Corregido en esta misión**: `~/hexelion` ahora apunta a `nexo-carbono-dashboard-20260623`. Sin
este cambio, media auditoría de abajo habría dado falsos negativos (código "no encontrado" que en
realidad sí existe y está desplegado, solo que no en la rama `main`).

## Carril 1 · Grafo/Observar

13 jobs de Observar vía `/api/observar/jobs`: 9 `accepted`, 3 `pending_review`, 1 `error`.

- **Deltas CONEXIÓN en aceptados**: 7 de 9 tienen sección `## Conexiones propuestas` con
  contenido real (2 no la tienen — versión de pipeline anterior, 0 conexiones que verificar, no es
  un fallo). Verificados ~74 nodos citados en `toca:` contra los `id:` reales del repo + rutas de
  Qdrant.
  - **1 referencia rota real**: en `cU6TFqoyHh8-20260714202112` una conexión cita
    `instrucciones-p0` (falta la `x` final) — la sección se corta a mitad de token justo ahí en el
    propio `delta_md` (4598 caracteres, verificado byte a byte). Es un artefacto del
    clasificador del pipeline (corte de generación), ya aceptado al grafo. Inofensivo para un
    lector humano, pero técnicamente una arista a un nodo que no existe.
  - `corpus/_INDICE.md` (citado en 2 deltas) **sí existe** — vive en `mente/corpus/_INDICE.md` y
    está indexado en Qdrant con contenido real; la ruta en el delta omite el prefijo `mente/`
    (convención del indexador, no un error).
  - Chunk citations verificadas por muestreo contra Qdrant (`[near-ai#5]`, `[near-ai#6]`, etc.):
    reales, `esferas/near-ai.md` tiene los 12 chunks (0-11) indexados.
- **Necrópolis → grafo: 0 fugas confirmadas.** Las 3 entradas de `mente/necropolis/` (incluida
  `mito-fundacional-organismo-20260711`, con contenido narrativo extenso) se buscaron por `id` y
  por texto distintivo contra los 358 puntos completos de la colección `mente` en Qdrant — cero
  coincidencias. El guardia de la skill auditora funciona.

## Carril 2 · PENDIENTES de voces/agentes vs estado vivo

Muestra de 8 entradas `hecha`/`FIRMADO` verificadas contra el repo (rama correcta) y HTTP:

| # | Sugerencia | Veredicto | Evidencia |
|---|---|---|---|
| 25 | Contratos §2 en 8 ficheros | **implementada-bien** | commit `3f8952e` existe con el mensaje declarado |
| 26 | Primera poda §4.4 | **implementada-bien** | commit `17f90d5` existe con el mensaje declarado |
| 60 | `prune_backups.py` | **implementada-bien** | `bin/prune_backups.py` existe en el repo |
| 61 | `/tareas` y `/verde` en `audit_overlaps.py` | **implementada-bien** (solo en la rama correcta) | `tools/audit_overlaps.py` en `nexo-carbono-dashboard-20260623`, líneas 26-27 confirman ambas páginas — **ausente en `main`**, causaba falso negativo |
| 22 | `d3AlphaTarget` comentario engañoso | **implementada-bien** (solo en la rama correcta) | `assets/vendor/force-graph.min.js` define `d3AlphaTarget` (1 match) — commit `0918fb9` es el fix, en `nexo-carbono-dashboard-20260623` — **ausente en `main`** |
| 67 | Flush del `think_filter` Sínodo v2 | **implementada-bien** (solo en la rama correcta) | `_make_think_filter` y 7 sitios `flush=done` en `hexelion_gateway.py` — **ausente en `main`**; probado en vivo contra `/api/indoor/chat` (SSE responde limpio, sin truncar, aunque el modelo de fallback usado en la prueba no emite `<think>` así que no prueba el filtro en sí) |
| 72 | `TimeoutStopSec=15` en la unit del gateway | **no verificable desde soberano** | la unit systemd del gateway no está versionada en NINGUNA rama del repo (confirma la SUGERENCIA #89 de G0) — requiere SSH a fragua |
| 24 | Pubkey `pi@el-vigia` | **no verificable desde soberano** | la clave usada en esa misión no está autorizada para el par SSH de este nodo; requeriría autorización nueva bajo el invariante #1 de G1 |

**Ninguna entrada resultó `implementada-mal` u `obsoleta`** en esta muestra — el problema no era
la calidad del trabajo, era que **la mitad de las verificaciones apuntaban a la rama vacía**.

## Tareas correctivas propuestas (a PENDIENTES.md, estado=propuesta)

Ver `mente/feedback/PENDIENTES.md`, sección 2026-07-18 · misión G1: `[aud:hexelion-main-stale]`,
`[aud:gateway-unit-not-versioned]` (reitera #89 con más evidencia).
