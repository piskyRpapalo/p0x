---
id: obs-scraper-bambu-a1mini-20260718
titulo: "Bambu Lab A1 Mini — documentación oficial (manual, mantenimiento, troubleshooting)"
tipo: observacion
capa_codice: factual
enlaces:
  - esfera-edge-ai
nivel: stub
origen: externo-fuente
fuente: "web:wiki.bambulab.com"
url: "https://wiki.bambulab.com/en/a1-mini"
fecha_captura: "2026-07-18T21:58:23Z"
licencia: "© 2026 Bambu Lab, todos los derechos reservados (aviso en pie de página de wiki.bambulab.com) — uso interno de referencia para F3, no redistribuible públicamente"
actualizado: 2026-07-18
---

# Bambu Lab A1 Mini — documentación oficial

> **FOCO:** conocimiento técnico de la A1 Mini para que aterrice a tiempo con la llegada de la
> impresora (24-28 jul). Scraper v1 (crawl4ai + markitdown + Chonkie), 30 páginas del dominio
> oficial `wiki.bambulab.com/en/a1-mini`, sin salir de esa sección.

## Lo nuevo

- "Regular maintenance can minimize wear and extend the printer's lifespan while also lowering
  the risk of a print failure." — [maintenance/period-maintenance]
- "It's crucial to power off the printer before conducting any maintenance work, including work
  on the printer's electronics and tool head wires." — [maintenance/period-maintenance]
- "The recommended ambient temperature of the A1 mini is 10℃ - 30℃ (50°F - 86°F). The
  recommended humidity level is under 85%." — [manual/faq]
- "It is not recommended to use stainless steel nozzles for printing materials that contain
  carbon fiber or glass fiber... if you replace the nozzle with a hardened steel material, you
  can print CF-based filaments on the A1 mini." — [manual/faq]
- "There are 2 timing belts on the A1 mini printer... During the calibration process, the A1
  mini performs a frequency scan to determine whether the belts need to be retensioned." —
  [maintenance/belt_tension]
- "The A series printers are equipped with the build plate position detection function... the
  printer can detect whether the user has placed the build plate properly before the printing
  starts." — [manual/build-plate-detection]
- Causas típicas de atasco de hotend/nozzle: filamento con temperatura de transición vítrea baja
  (heat creep), diámetro de filamento inconsistente, residuos en el filamento, partículas de
  filamentos con fibra de carbono/purpurina, purga incompleta entre filamentos incompatibles
  (PLA↔PC, ASA↔TPU). — [troubleshooting/nozzle-clog]

## Lo que ya sabías

Ninguno — dominio nuevo (`esfera-edge-ai` es lo único remotamente adyacente; verificado que no hay
puntos existentes en Qdrant con "bambu", "a1 mini", "impresora 3d" ni "filamento" antes de este
scraper: 0 de 358).

## Conexiones propuestas

Ninguna detectada contra nodos existentes — es la semilla de una esfera nueva
(`esfera-impresion-3d`, propuesta, no creada en esta misión: crear esferas nuevas es acto del
carbono/Preceptor, no de una sesión de scraping).

## Telemetría del pipeline

- Páginas crawleadas: 30 / 30 (tope alcanzado, dominio único `wiki.bambulab.com`, prefijo
  `/en/a1-mini` respetado en todo momento)
- Chunks (Chonkie, `RecursiveChunker`, chunk_size=512): 891
- Caracteres markdown totales (tras MarkItDown): 337 948
- Tiempo de crawl: 37.13s
- Temperatura de fragua durante embeddings: **N/A — este pipeline corrió íntegramente en
  `soberano`, no en fragua** (ver nota de bloqueo abajo). No hubo carga de embeddings en fragua
  que medir en esta misión.

## Nota de bloqueo — por qué este delta no está en `/api/observar/pendientes`

`POST /api/observar/ingest` se probó con esta URL exacta ANTES de construir el scraper (verbatim):

```
curl -X POST http://100.82.94.83:8001/api/observar/ingest -d '{"url":"https://wiki.bambulab.com/en/a1-mini/user-guide", ...}'
→ 422 {"detail":"no se pudo resolver el video_id de la URL"}
```

Causa raíz: `pipeline/observar_lib.py:resolve_video_id()` y todo el esquema de `job_id`
(`{video_id}-{timestamp}`) asumen YouTube — el pipeline entero (`ingest_youtube.py`,
`observar_runner.py`) fue diseñado para transcripciones de vídeo, no para documentación web. No es
un bug puntual: es una limitación de diseño real, y ampliarlo (aceptar `source_id` genérico,
enrutar a un fetcher no-YouTube) es un cambio en el orquestador central de Observar que usan las 6
voces y todas las misiones futuras — exactamente lo que la Doctrina AI Interna §4.3 dice que CC no
reescribe por iniciativa propia. Este documento (y su [ESTRATEGIA_TESTNET.md]-equivalente para
Observar) es la propuesta; el Preceptor la valida y el despliegue real en fragua es mano de David
o una sesión CC-fragua dedicada.

**Fallback usado (declarado en el brief de G1):** la ruta de archivo/transcript. Este `delta.md` y
`out/paginas.json` (30 páginas con markdown + chunks completos) quedan listos en
`soberano-bench/scraper/out/` para que, una vez desplegado el fix, se re-suban vía la API real y
generen su propio `job_id` con el ciclo ACCEPT/DISCARD normal. Hasta entonces, este documento
espera revisión directa del carbono fuera del lazo Observar automático.
