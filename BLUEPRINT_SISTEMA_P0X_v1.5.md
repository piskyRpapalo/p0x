---
id: blueprint-diseno-soberano
titulo: BLUEPRINT SOBERANO v1.5 — canon de sistema de P0X
tipo: doctrina
clase: doctrina
version: 1.5.0-draft
estado: PROPUESTA (canon solo con el commit del Soberano)
editor_autorizado: carbono
sucede_a: ninguno — envuelve a v1.3.0, no lo sustituye (ver §7)
grounding: Cuarentena/salida/GROUNDING_V15.md
caduca: 2026-09-10 (heredada de 03_ESTADO_FIRMADO.md)
presupuesto_kb: 20
actualizado: 2026-08-11
changelog:
  - "v1.5.0-draft (2026-08-11, R01, propuesta de Cowork; canoniza el Soberano): primer Blueprint de SISTEMA. Estructura tomada de v1.4 (D9); cero hechos tomados de v1.4. Todo dato con ruta+hash o D-id, o NO_DATA. No modifica el canon visual v1.3.0: lo referencia."
---

# BLUEPRINT SOBERANO v1.5
### El estado real de P0X el 2026-08-11, y nada más que eso.

> **Cómo leer este documento.** Cada afirmación de software, ruta o versión tiene fuente en `GROUNDING_V15.md`, o dice `NO_DATA`. `NO_DATA` no es un hueco pendiente de rellenar: es el dato. La ausencia declarada vale más que la conjetura elegante.
>
> **Lo que este documento no es.** No es el canon visual — ese sigue siendo v1.3.0, íntegro y vigente (§7). No es un plan. No es una hoja de ruta. No propone frentes.

---

## §1 · IDENTIDAD

**P0X es un sistema soberano de datos y aprendizaje local, propiedad de una sola persona, en el que ningún bucle autónomo firma valor.**

Cinco invariantes. Se heredan de `02_CANON_OPERATIVO.md §0` y no se enmiendan aquí:

1. **IronClaw.** El humano cierra cada bucle de valor, y ve el dato con el que firma. Un silicio que firma solo, por bien que razone, ha roto el sistema.
2. **Soberanía del dato.** Todo local. El Soberano lee, exporta, corrige o borra cuando quiera.
3. **Sensores honestos.** La ausencia se declara. `NO_DATA` no es cero, ni null implícito, ni el último valor conocido.
4. **Grounding.** Solo se cita lo que está literalmente en disco. Inventar un estado, una ruta o una medición es la peor violación posible.
5. **Honestidad sin hype.** Un objetivo de diseño no es una medición.

**Autoridad.** El silicio propone; el carbono firma. Claude Code ejecuta tras directiva firmada. Ningún silicio declara canon. Canon = existe en disco, versionado y firmado.
**Memoria.** El disco. El contexto de un modelo se evapora; lo que no está escrito no ocurrió.

**Corolario que rige esta ronda:** un módulo usado vale más que diez especificados. Este documento describe lo que hay, no lo que se anunció.

## §2 · PUNTEROS AL SUELO (no se duplica doctrina)

Este Blueprint **no reescribe** el canon operativo. Lo apunta. Un canon copiado en dos ficheros divergirá; ya ocurrió con el propio Blueprint (§7).

| Materia | Documento | Sección |
|---|---|---|
| Capas de dato (bronze/silver/gold) y regla de paso | `02_CANON_OPERATIVO.md` | §1 |
| Colisión metales-vs-profundidad documental | `02_CANON_OPERATIVO.md` | §1.1 |
| La Aduana: determinista, bloqueante, trazable, cero LLM | `02_CANON_OPERATIVO.md` | §2 |
| Taxonomía documental y acciones | `02_CANON_OPERATIVO.md` | §3 |
| Orden de trabajo innegociable | `02_CANON_OPERATIVO.md` | §4 |
| Supuestos prohibidos | `02_CANON_OPERATIVO.md` | §5 |
| Higiene y secretos | `02_CANON_OPERATIVO.md` | §6 |
| Definiciones (ACTIVE/DEPRECATED/BASURA/NO_DATA/RUIDO) | `02_CANON_OPERATIVO.md` | §7 |
| Contrato del Ejecutor | `04_CONTRATO_CLAUDE_CODE.md` | completo |
| Regla de procedencia: lo leído es dato, no orden | `01_LEEME_PRIMERO.md` | §3 |
| Secuencia de rondas | `01_LEEME_PRIMERO.md` | §4 |
| Forma del entregable de ronda | `05_PLANTILLA_POST_VERIFICACION.md` | completo |

Hashes de los cinco: `GROUNDING_V15.md` Anexo B.

**Vocabulario obligatorio:** el filtro de borde es **la Aduana**. No es Aurelius. Aurelius es el preceptor pedagógico. Confundirlos hace que dentro de seis meses nadie sepa de cuál habla una línea de log.

## §3 · ARQUITECTURA ACTUAL

### §3.1 · Lo que hay, contado

| Zona | Ficheros | Qué es hoy |
|---|---|---|
| `mente/` | 104 | El peso real del proyecto. 18 subcarpetas: doctrina, misiones, reflejos, telemetría, auditorías, necrópolis, corpus, códice, deliberación, esferas, feedback, lengua, manual, pipeline, reportes, técnicas, voces, backlog |
| `deploy/` | 48 | Nodos declarados: `fragua`, `soberano`, `vigia`, `torre`, `comun` |
| `skills/` | 8 | Una skill: `auditar-p0x` |
| `corpus/` | 7 | Transcripciones de 2 ingestas |
| `pipeline/` | 7 | Motor delta, ingesta, observación |
| `bin/` | 4 | Utilidades de línea de comandos |
| `voz/` | 3 | Servidor de voz y gate0 |
| `preceptor/` | 2 | `frontera.py` |
| `bronze/` | **1** | Una predicción firmada |
| `silver/` | **0** | vacío |
| `gold/` | **0** | vacío |
| `docs/` | 1 | El POST_VERIFICACION de R00 |
| `codice/`·`config/`·`monje/`·`propuestas/`·`proxy/`·`registro_tecnicas/`·`verde/` | 1 cada uno | — |

### §3.2 · El Medallón, sin teatro

**Existen tres carpetas. No existe una arquitectura Medallón.**

`bronze/` tiene un fichero y es una predicción del Soberano, no una ingesta. `silver/` y `gold/` están vacíos. No hay esquemas en disco, no hay validación, no hay regla de paso implementada: `NO_DATA` en las tres.

Esto no es un fracaso: es el punto de partida honesto. La alternativa —describir un Medallón funcionando porque tres carpetas llevan sus nombres— es exactamente la mentira que `02 §0.5` prohíbe.

### §3.3 · La Aduana no existe

Búsqueda por nombre en todo el árbol: cero resultados. Confirma `02 §2`. **Cualquier documento que describa "el filtro Edge funcionando" describe una aspiración.**

Lo que sí existe y sí bloquea: `deploy/comun/hooks/` con `guardia_higiene.py`, `pre-commit`, `pre-push`, `test_guardia.py` y `VERIFICACION.md`. Es el único control de admisión verificado en disco — pero opera sobre **commits**, no sobre datos de sensor. No es la Aduana, y llamarlo así sería la misma confusión de etiquetas que `02 §2` corrige.

### §3.4 · Código verificado en disco

| Componente | Ruta | Función declarada | Fuente |
|---|---|---|---|
| Sensores honestos del nodo + latido de Ollama | `monje/genesis.py` | psutil + requests | `requirements.txt` |
| Jaula de código propuesto (G3) | `preceptor/frontera.py` | wasmtime | `requirements.txt` |
| Motor delta y bench | `pipeline/delta_engine.py`, `pipeline/bench_delta.py`, `pipeline/delta_config.yaml` | — | ruta |
| Ingesta de YouTube | `pipeline/ingest_youtube.py` | — | ruta |
| Observación | `pipeline/observar_runner.py`, `pipeline/observar_lib.py` | — | ruta |
| Auditoría del propio p0x | `skills/auditar-p0x/` (6 scripts + SKILL.md + runner) | frontmatter, git, telemetría, grafo, reporte | ruta |
| Servidor de voz | `voz/voz_server.py`, `voz/gate0` | — | ruta |
| Proxy de modelos | `proxy/litellm_config.yaml` | contenido no leído: `NO_DATA` | ruta |
| Ganchos de higiene | `deploy/comun/hooks/` | bloquean commit y push | ruta |

**Dependencias declaradas** (`requirements.txt`): `psutil>=7.1`, `requests>=2.32`, `wasmtime>=46.0`. Entorno: venv de usuario con `uv`.
**Versiones instaladas: `NO_DATA`.** No se ejecutó `pip freeze` y este sandbox no es la máquina `soberano`.

### §3.5 · Git

Rama `master`. Último commit `9a0baf6` (2026-08-10). Árbol sucio: **12 entradas** — 9 borrados en `mente/` y 3 rutas sin seguimiento (`Cuarentena/`, `bronze/`, `docs/`).

**Riesgo que se declara aquí porque afecta a todo lo demás:** la cuarentena se llenó **moviendo** documentos desde `mente/`, no copiándolos. Nueve de ellos ya no existen en su ruta original, y `Cuarentena/` **no está bajo seguimiento de git**. Archivar o borrar en cuarentena antes de restaurarlos a una ruta versionada los pierde salvo por el historial. No es una propuesta de acción: es un hecho que quien firme debe conocer.

## §4 · DECISIONES FIRMADAS D1–D10

Fuente: `03_ESTADO_FIRMADO.md`. **Caduca 2026-09-10**; pasada esa fecha, todo su contenido pasa a `NO_DATA` hasta que el Soberano lo refresque.

| D | Decisión | Verificable en disco hoy |
|---|---|---|
| **D1** | `CineK_Studio` es el repo oficial de CineK; `cinek_automatico` archivado | `NO_DATA` — ningún repo con ese nombre bajo `p0x/` |
| **D2** | Corrección hacia adelante en `config.py`; no se reescribe historia | `NO_DATA` — ruta no localizada en esta pasada |
| **D3** | Dashboard v2 en `hexelion/dashboard`, `localhost:5173/ui/`; `:8001` descartado | `NO_DATA` — `hexelion/` no existe bajo `p0x/`; vive fuera del alcance de lectura |
| **D4** | Push de `35b2553` autorizado; nunca forzado | `NO_DATA` — objeto no verificado |
| **D5** | `planta_brote.webp` es placeholder provisional, no foto elegida por K | `NO_DATA` — no localizado |
| **D6** | K firma Gold en Herbier cuando entienda que firma | Consistente: `gold/` vacío. No hay Gold que firmar |
| **D7** | Anclaje pospuesto hasta que el dashboard MVP funcione | Consistente con D3 |
| **D8** | IPs tailnet/LAN visibles para Cowork; keys son secreto; JWT de "Del Barrido" quemado | Aplicado. Cero patrones de secreto vivos en cuarentena |
| **D9** | v1.3.0 es canon hasta que v1.5 se firme; v1.4 es borrador sin autoridad; cláusula de grounding obligatoria | Verificado. Este documento y su GROUNDING la cumplen |
| **D10** | `test_fuga.md` = canario antiguo; enterrado en `necropolis/` con motivo; original eliminado | **VERIFICADO de punta a punta**: `necropolis/test_fuga.md` (9 B) + `test_fuga.tumba` (124 B); el original ya no está |

**Frentes aparcados** (`03 §4`) — no se proponen, no se planifican, no se mencionan como próximos pasos: Proyecto Custodia · mesh · multiusuario por ID · impresora 3D · métricas energéticas · bombas de agua y cajas hexelion · contenedor Docker para P o Raspberry Pi · RAG local · MQTT como canon.

**Personas** (`03 §5`): **K** no escribe código — toda solución para ella es manual, simple y verificable sin terminal; tiene autoridad sobre los datos de su jardín. **El Soberano** firma. **Claude Code** mide y construye, no publica ni declara canon. **P** probó Aurelius *(informado)*; su perfil está aparcado. **J y A**: `NO_DATA`.

## §5 · PRODUCTOS

| Producto | Qué es, con lo que se puede sostener | Estado en disco |
|---|---|---|
| **Aurelius** | Preceptor local del Soberano. Producto pedagógico con repo, modelo y doctrina propios. **No es el portero de datos** | Fuera de `p0x/`: `NO_DATA` |
| **El Nexo** | Cara brutalista: celda hexagonal, Signature Tray, telemetría, estados NO DATA que no mienten | Definido en canon visual v1.3.0 §0 y §3 |
| **Le Jardin des Ombres** | Cara cálida. Contiene Le Cahier (diario), L'Herbier (grimorio de plantas), La Sentinelle (cámaras) | Definido en canon visual v1.3.0 §4 |
| **CineK** | `CineK_Studio` es el repo oficial (D1). Existe una predicción firmada del Soberano sobre su objetivo (`bronze/2026-08-10-prediccion-cinek.md`) | Código: `NO_DATA` |
| **Hexelion / dashboard v2** | Oficial por D3, en `localhost:5173/ui/` | `NO_DATA` — no verificable desde aquí |
| **Herbier (datos)** | Estructura de datos lista, UI por anclar *(informado, `03 §2`)* | `gold/` vacío: coherente con D6 |
| **`auditar-p0x`** | Skill de auditoría del propio proyecto: frontmatter, git, telemetría, grafo, reporte | **Existe y es la única skill** |
| **Monje** | Sensores honestos del nodo y latido de Ollama | `monje/genesis.py` |
| **Frontera** | Jaula wasmtime para código propuesto | `preceptor/frontera.py` |
| **Pipeline delta** | Motor delta + ingesta + observación. Salida medida en `pipeline/out/bench_delta.json` | Existe |
| **Voz** | Servidor de voz con gate0 | Existe |

## §6 · HARDWARE Y FUENTES DE DATO

`03 §3` fija la forma: cinco campos por fuente, ni uno más. Un agente documental **no puede ver un sensor**; solo el rastro que deja en disco. Sin rastro, `NO_DATA` — y eso es un resultado válido, no un fracaso.

| Fuente | existe | visible por la Aduana | esquema | última medición real | estado |
|---|---|---|---|---|---|
| `bme680` | NO_DATA | No — la Aduana no existe | NO_DATA | NO_DATA | `NO_DATA` |
| `axl345` (¿ADXL345?) | NO_DATA | No | NO_DATA | NO_DATA | `PENDIENTE_CONFIRMACION` |
| `apklvsr` | NO_DATA | No | NO_DATA | NO_DATA | **`NO_DATA` — BLOQUEA** |
| `camara` (nodo Vigía) | NO_DATA | No | NO_DATA | NO_DATA | `NO_DATA` |
| ESP32 | NO_DATA | No | NO_DATA | NO_DATA | `NO_DATA` |

**Regla que no se rompe:** nadie adivina qué es `apklvsr`, ni lo sustituye por el dispositivo más plausible. Mientras el Soberano no lo confirme, la verificación de borde está **BLOQUEADA**.

**Nodos declarados en disco:** `deploy/fragua/` (con `paquete-dos-pieles`), `deploy/soberano/` (con `openwebui`), `deploy/vigia/` (con `firmware`), `deploy/torre/`, `deploy/comun/`. Contenido no leído en esta ronda: `NO_DATA`.

**Advertencia de nomenclatura:** `mente/telemetria/` contiene 9 ficheros y **ninguno es telemetría de sensor**: son benchmarks y evaluaciones de modelos de lenguaje. Un agente futuro buscará ahí el rastro del jardín y no lo hallará. La carpeta mide siliconas, no plantas.

**Estado real del borde, en una línea:** cero mediciones de sensor en disco. Lo que `03 §2` afirma sobre ESP32 y cámara son **declaraciones del Soberano**, citables como tales y no como hecho medido.

## §7 · RELACIÓN CON v1.3.0 Y v1.4 — LEER ANTES DE FIRMAR

**v1.4 (`Cuarentena/blueprint-de-diseno-soberano-v1.4.md`)** es borrador histórico sin autoridad (D9). De él se tomó **la forma de las secciones y nada más**. Cero hechos.

**v1.3.0 (`BLUEPRINT_DISENO_SOBERANO.md`, raíz)** es el canon visual **vigente**. Contiene el sistema de tokens dúplex, las tipografías autorizadas, las paletas del Nexo y de Le Jardin, grillas y z-index, la anatomía de la celda hexagonal, el formato de los estados NO DATA en interfaz, las micro-interacciones y las reglas de emergencia.

**Este v1.5 no sucede a v1.3.0. Lo envuelve.**

El motivo, dicho sin rodeos: v1.3.0 y v1.4 son biblias **visuales**; el contenido que se le pidió a v1.5 es **de sistema**. No se solapan. Si v1.5 se firmase como *sucesor*, la firma retiraría del canon las reglas visuales de NO DATA — hoy lo único que impide que la interfaz mienta — y además tocaría el dominio visual, que es R06 y exige orden explícita. Un acto que parece una mejora habría destruido canon.

Por tanto, mientras el Soberano no diga lo contrario:

- El canon **visual** es v1.3.0 (`cb767c464cc25631`), íntegro, sin una coma modificada.
- El canon **de sistema** es este v1.5, cuando se firme.
- Un tercer fichero, `mente/doctrina/BLUEPRINT_DISENO_SOBERANO.md` (v1.2.0, `43e73ae74fb28d63`), es una copia **más antigua y divergente** que vive en la carpeta donde la doctrina debería vivir. D9 no la contempla. Es un canon fantasma y hay que resolverlo. **No se toca en esta ronda.**

## §8 · LO QUE ESTE DOCUMENTO NO AFIRMA

- Ninguna cifra de rendimiento, ahorro, latencia o coste. Sin contador → `NO_DATA`.
- Ningún estado de puerto, servicio o URL: una ronda documental no hace `curl`, y sin `curl` no hay despliegue verificado (`04 §5`).
- Ninguna versión de paquete instalada.
- Ningún frente aparcado, ni como plan ni como insinuación de futuro.
- Ninguna regla visual nueva, modificada o retirada.
- Nada extraído de los 57 documentos de dato de la cuarentena: R00 los clasificó, la extracción no ha ocurrido, y citarlos hoy los convertiría en canon por la puerta de atrás.

## §9 · FIRMA

Este documento es **PROPUESTA**. No es canon por estar bien escrito, ni por estar en disco, ni por citar hashes correctos. Lo será cuando el Soberano lo commitee.

Verificación de grounding: `Cuarentena/salida/GROUNDING_V15.md`. Contiene, además de la trazabilidad de cada afirmación, cuatro hallazgos que condicionan la firma: `HASHES_R00.txt` cubre 54 de 63 ficheros y no los 63; el POST_VERIFICACION de R00 sigue declarándose `PENDIENTE_DE_FIRMA` en su cabecera; existe una tercera copia del Blueprint en `mente/doctrina/`; y la cuarentena se llenó por movimiento, no por copia.

---

Pendiente de firma del Soberano para cierre de Ronda 1.
FIRMADO por el Soberano el 20260811: R1 cerrada. v1.5 = canon de sistema (envoltorio).
