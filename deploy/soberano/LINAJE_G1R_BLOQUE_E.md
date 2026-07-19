# Linaje del dashboard — diff conceptual · Misión G1-R, Bloque E (2026-07-19)

## Corrección honesta sobre el reporte de El Yacimiento

En `mente/deliberacion/INDICE_ARCHIVO_HISTORICO.md` afirmé, con "alta confianza", que el handoff
del 14-jul (`P0X_ Dashboard soberano local-first.zip`) era "el antecedente directo" del
dashboard/Jardin vivo. **Verificado ahora a fondo: esa afirmación era prematura y probablemente
incorrecta.** Se corrige aquí con evidencia, no se deja la afirmación original sin contraste.

## Método

Extraído el handoff a scratch (`/tmp/.../handoff_14jul/`, fuera de `mente/`, sin fusionar nada).
Su `GUIDE.md` (116 líneas) especifica identificadores concretos y verificables: funciones
(`applyMood()`, `emblemSVG()`, `openBook()/closeBook()`), objeto `MOODS`, endpoints
(`/api/cortex`, `/api/plants`), nombres de los 3 juegos (Le Docteur, La Devinette, Le Trivial),
sección `L'HERBIER`, estados humor (`sereine`/`soif`/`alerte`). Se buscó cada uno, literal, en
todo el repo `hexelion` (rama `nexo-carbono-dashboard-20260623`, la real — no `main`, ver
`AUDITORIA_G1.md`).

## Resultado: cero coincidencias

| Identificador del handoff | ¿Aparece en el repo vivo? |
|---|---|
| `applyMood`, `emblemSVG`, `MOODS` | No |
| `Le Docteur`, `La Devinette`, `Le Trivial` | No |
| `sereine`, `L'HERBIER`, `openBook` | No |
| `api/cortex`, `api/plants` | No |
| `honest-sensors` (el principio, no la implementación) | Sí (2 archivos) |
| `SIGNATURE TRAY` | Sí (1 archivo) |

Los dos conceptos que SÍ sobrevivieron (honest-sensors, signature tray) son principios de
doctrina, no código del handoff — pudieron llegar por cualquier vía, no prueban lineage directo.

## El hallazgo real: el Jardin vivo no tiene una fuente única clara, y su código React no está en git

- `dashboard-v9/indoor.html` (352 líneas, título real: **"El rincón verde"**) es una implementación
  **distinta y más simple** — sin Cortex, sin humor, sin juegos, sin francés. No es el "Jardin des
  Ombres" que PENDIENTES.md describe en la sesión del 12-jul (#76-80: Cortex, herbier, francés,
  paleta violeta) ni el `jardin.html` del handoff del 14-jul.
- Las capturas `dashboard-v9/screenshots/jardin-v2-arcade.png`, `jardin-v2-herbier.png`,
  `jardin-v2-sentinelle.png` **prueban que un "Jardin v2" con arcade y herbier existió/existe**
  visualmente — pero su código fuente no aparece en ningún `.html`/`.jsx` de este repo.
- `dashboard/` (el directorio que debería tener el build React del dashboard vivo) está
  **prácticamente vacío en git** — solo `.vite/deps/_metadata.json` y `.vite/deps/package.json`
  quedaron trackeados (cache de build, no código fuente), aparentemente de forma accidental en el
  commit `6a4bb3f` ("recuperación tras pérdida de historial"). **El código fuente real del
  dashboard/Jardin que hoy corre no está versionado en ningún sitio accesible desde `soberano`.**

Esto es más urgente que la pregunta original de "qué push se perdió": no es solo que una versión
antigua no llegó a producción — es que **la versión que sí está en producción podría no tener
respaldo en git en absoluto**, más allá de lo que quede en el propio disco de `la-fragua`.

## Candidatos, re-ordenados con la evidencia real

1. **[nuevo, el más urgente] Recuperar/versionar el código fuente real del Jardin/dashboard
   desplegado en `la-fragua`** — sea cual sea su stack (React del `dashboard/` vacío, o algo más
   reciente), antes de que otro "pérdida de historial" se lo lleve sin copia. Esto requiere SSH a
   fragua (no autorizado en esta misión) o que David copie el directorio real a `deploy/fragua/`.
2. El handoff del 14-jul sigue siendo **material de referencia útil, no adoptado**: los 3 juegos
   con cabeceras SVG ya dibujadas (Le Docteur/Devinette/Trivial) y el contrato de API
   honest-sensors completo (`/api/env`, `/api/system`, `/api/energy`, `/api/harvest`,
   `/api/treasury`, `/api/watch`, `/api/plants`, `/api/cortex`) son un diseño completo que David
   podría decidir adoptar — o descartar conscientemente — para lo que falte del Jardin real.
3. Los tres troncos de dashboard más antiguos (Nexo, Tejo·AIS, Terminal) del reporte de El
   Yacimiento siguen siendo arqueología de baja urgencia frente a este hallazgo — se degradan de
   prioridad.

## Corrección a `mente/deliberacion/INDICE_ARCHIVO_HISTORICO.md`

Se deja esta nota aquí en vez de reescribir el índice original (append-only, el silicio no borra
su propio rastro): la sección "Contraste con el dashboard vivo hoy" de ese documento sobrestimó la
confianza del vínculo 14-jul → vivo. Este documento (`LINAJE_G1R_BLOQUE_E.md`) es la corrección
vigente.
