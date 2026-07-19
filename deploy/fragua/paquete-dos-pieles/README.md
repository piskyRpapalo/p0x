# PAQUETE DE DEPLOY ÚNICO · misión LAS DOS PIELES

Destino: `la-fragua` (gateway HEXELION). **Propose-only**: nada de esto se aplica por SSH desde
`soberano` — viaja por git y lo aplica el carbono (o una misión con mandato explícito en fragua)
en la sesión de deploy de la Fase 5. Cada ítem lleva su verificación.

| # | Ítem | Estado | Verificación tras aplicar |
|---|---|---|---|
| 01 | `01-serve-from-git.patch` — `/jardin` se sirve desde `<repo>/dashboard/dist` (env `JARDIN_DIST` para transición); deploy = `git pull` + restart | listo (Fase 0) | `grep -n JARDIN_DIST hexelion_gateway.py` muestra el bloque · `curl -o /dev/null -w '%{http_code}' :8001/jardin/` → 200 |
| 02 | `PROPUESTA_28_observar_fuentes_web.patch` (vive en `p0x/mente/auditorias/`) — fallback web en `resolve_video_id` | **sigue vivo**: 422 reproducido en vivo 2026-07-19 | `curl -X POST :8001/api/observar/ingest -d '{"url":"https://wiki.bambulab.com/en/a1-mini"}'` → deja de ser 422 (202 si hay transcript cacheado) |
| 03 | #98 — validación post-generación de IDs de conexión (regex contra léxico real) antes de aceptar una CONEXIÓN | **sigue vivo**: arista rota `instrucciones-p0` confirmada en vivo en el delta `cU6TFqoyHh8-20260714202112` (1 rota vs 4 correctas) — diseño en Fase 5 | `curl :8001/api/observar/delta/cU6TFqoyHh8-20260714202112 \| grep -c 'instrucciones-p0[^x]'` → 0 tras saneo |
| 04 | `/api/jardin/notes` (POST/GET) — persistencia del Cahier | pendiente (se construye en Fase 4) | — |
| 05 | Voz única empaquetada · Nexo re-vestido · Jardin v2 · Bandeja de dos carriles (builds) | pendiente (Fases 1-4) | — |
