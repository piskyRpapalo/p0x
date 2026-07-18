# Scraper v1 · Misión G1, Bloque C (2026-07-18)

## Salud del tramo URL→job (verificado ANTES de construir nada)

```
curl -X POST http://100.82.94.83:8001/api/observar/ingest \
  -d '{"url":"https://wiki.bambulab.com/en/a1-mini/user-guide", ...}'
→ 422 {"detail":"no se pudo resolver el video_id de la URL"}
```

**Causa raíz** (código, no conjetura): `pipeline/observar_lib.py::resolve_video_id()` solo sabe
resolver YouTube (regex + `yt-dlp --print id`, que también es solo-vídeo). Todo el esquema de
`job_id` (`{video_id}-{timestamp}`) y el pipeline (`ingest_youtube.py`, `observar_runner.py`)
nacieron para transcripciones de vídeo — nunca se diseñaron para documentación web. No es un bug
puntual reparable en una línea sin tocar el orquestador central que usan las 6 voces.

**Fix propuesto, no desplegado**: `mente/auditorias/PROPUESTA_28_observar_fuentes_web.patch`
(`git apply --check` OK). Añade un tercer fallback a `resolve_video_id()`, aditivo y sin tocar el
camino YouTube: si ya existe un `transcript.txt` cacheado en `corpus/web-<hash-url>/`, lo usa. Cero
llamadas de red nuevas. Requiere `git apply` + reinicio del gateway en fragua — mano de David o
sesión CC-fragua, per Doctrina AI Interna §4.3 (CC no reescribe el orquestador por iniciativa).

**Fallback usado en esta misión** (declarado en el brief): la ruta de archivo/transcript. Ver
abajo.

## Stack y ejecución

`crawl4ai` (fetch + render JS vía Chromium/Playwright, instalado sin sudo con
`playwright install chromium`, sin `--with-deps` porque eso pide `apt`) + `markitdown` (HTML→MD
limpio) + `chonkie` (`RecursiveChunker`, chunk_size=512). Todo instalado con `uv venv` en
`soberano-bench/scraper/.venv` — no toca el resto del sistema.

Fuente única: `wiki.bambulab.com/en/a1-mini` (dominio y prefijo verificados en cada enlace antes
de encolarlo — cero salidas del scope). Tope 30 páginas, alcanzado exacto.

## Telemetría del pipeline (`mente/telemetria/scraper_bambu_g1.json`)

| Métrica | Valor |
|---|---|
| Páginas crawleadas | 30 / 30 (tope) |
| Chunks (Chonkie) | 891 |
| Caracteres markdown (tras MarkItDown) | 337 948 |
| Tiempo de crawl | 37.13s |
| Temperatura de fragua durante embeddings | N/A — pipeline corrió en `soberano`, no en fragua (el fix aún no está desplegado, así que fragua no procesó nada de esto todavía) |

## Entregable

- `mente/deliberacion/delta_bambu_a1mini.md`: delta con procedencia completa (`origen`, `url`,
  `fecha_captura`, `licencia` — `© 2026 Bambu Lab, todos los derechos reservados`), 8 claims reales
  citados por página, comparación contra la mente (0 coincidencias previas de "bambu"/"a1
  mini"/impresión 3D en los 358 puntos de Qdrant — dominio genuinamente nuevo).
- `corpus/web-f198e5722c/transcript.txt` + `meta.tsv`: las 30 páginas completas, en la ruta exacta
  que el patch #28 espera (`corpus/web-<hash-url>/transcript.txt`) — si se aplica y despliega el
  fix, este job puede resolverse sin volver a scrapear.
- **No está en `/api/observar/pendientes`** todavía — motivo declarado arriba. Espera revisión
  directa del carbono fuera del lazo automático, o el despliegue del patch #28 para entrar por la
  vía normal.
