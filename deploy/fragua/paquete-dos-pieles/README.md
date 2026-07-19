# PAQUETE DE DEPLOY ÚNICO · misión LAS DOS PIELES

Destino: `la-fragua` (gateway HEXELION). **Propose-only**: nada de esto se aplica por SSH desde
`soberano` — viaja por git y lo aplica el carbono (o una misión con mandato explícito en fragua)
en la sesión de deploy. Cada ítem lleva su verificación; la secuencia completa del swap vive en
`05-swap.md`.

Los patches 01 y 04 se verificaron **en frío** (cicatriz PROPUESTA_29): aplicados en orden sobre
el gateway base `cfae84b` producen byte a byte el HEAD `60d2023` de `hexelion.git`.

| # | Ítem | Estado | Verificación tras aplicar |
|---|---|---|---|
| 01 | `01-serve-from-git.patch` — mount único `/ui` → `<repo>/dashboard/dist`; aliases FileResponse `/dashboard`, `/tareas`, `/jardin` bajo `UI_CARA=dos-pieles` (swap OPT-IN; sin la env todo lo legado queda intacto); `JARDIN_DIST`/`UI_DIST` por env | **listo** (commits `2791c7f`+`60d2023`) | `grep -c DOS_PIELES hexelion_gateway.py` → 4 · `curl -o /dev/null -w '%{http_code}' :8001/ui/` → 200 |
| 02 | `PROPUESTA_28_observar_fuentes_web.patch` (vive en `p0x/mente/auditorias/`) — fallback web en `resolve_video_id` | **sigue vivo**: 422 reproducido en vivo 2026-07-19 | `curl -X POST :8001/api/observar/ingest -d '{"url":"https://wiki.bambulab.com/en/a1-mini"}'` → deja de ser 422 (202 si hay transcript cacheado) |
| 03 | #98 — validación post-generación de IDs de conexión (regex contra léxico real) antes de aceptar una CONEXIÓN | **sigue vivo**: arista rota `instrucciones-p0` confirmada en el delta `cU6TFqoyHh8-20260714202112` — el diseño queda propuesto en el reporte de misión (no es código de esta fase) | `curl :8001/api/observar/delta/cU6TFqoyHh8-20260714202112 \| grep -c 'instrucciones-p0[^x]'` → 0 tras saneo |
| 04 | `04-jardin-notes.patch` — `/api/jardin/notes` GET/POST: persistencia del Cahier en `verde/cahier_notes.json` (upsert por id, escritura atómica, vacío honesto) | **listo** (commit `abec9e0`) | `curl -s :8001/api/jardin/notes` → `{"notes": [], "total": 0, ...}` · humo POST en `05-swap.md` |
| 05 | El dist final versionado en `hexelion.git` (`1fa2ea1`, 17 archivos) + `05-SHA256SUMS` + `05-swap.md` (backup previo + Playwright verde como condición de la ley) | **listo**: 172/172, 0 flaky (4 viewports) sobre este mismo build | `(cd dashboard/dist && sha256sum -c 05-SHA256SUMS)` → 17 OK · secuencia completa en `05-swap.md` |
