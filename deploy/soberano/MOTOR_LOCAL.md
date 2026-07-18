# Motor local · soberano (Misión G0, 2026-07-18)

## Modelo

`qwen3-coder:30b` (Q4_K_M, 18GB en disco) vía Ollama. Modelo previo (`llama3:8b-instruct-q8_0`,
pre-existente en el nodo antes de esta misión) borrado por decisión explícita del carbono.

Layout de almacenamiento: `/usr/share/ollama/.ollama/models` (servicio corre bajo el usuario de
sistema `ollama`, home `700` — `pisky` está en el grupo `ollama` pero sin `x` heredado en el
directorio home del servicio, así que no hay lectura directa de los blobs sin sudo. No bloquea el
uso vía API; sí bloqueó el plan original de apuntar `llama-bench` directo al blob para el Bloque D
— desviación declarada allí). Espacio en NVMe tras el pull: 39GB usados de 915GB (831GB libres).

## `soberano-coder` (Modelfile en este mismo directorio)

`FROM qwen3-coder:30b` explícito (nunca un tag pelado — footgun documentado en `CLAUDE.md`).
`num_ctx 16384` inicial, `temperature 0.2` / `top_p 0.9` (uso previsto: coding/tareas
deterministas), `repeat_penalty 1.1`.

## Huella de RAM medida (num_ctx=16384, modelo cargado, backend CPU)

- `ollama ps`: 20GB reportados por Ollama, 100% CPU (sin backend GPU configurado aún — se decide
  en el Bloque D por bench, no por intuición).
- `systemctl show ollama -p MemoryCurrent`: **36.7 GiB** reales en el cgroup del servicio con el
  modelo cargado (peso 18GB + KV cache a 16384 ctx + overhead del runtime).
- Sistema total: 57GiB RAM. Con el servicio cargado, `free -h` reporta ~33GiB aún disponibles
  (cache reclamable incluido).
- **Margen para subir `num_ctx` en el futuro**: hay margen real para al menos duplicar el contexto
  (~32k) sin agotar RAM, pero eso debe volver a medirse por dato cuando se necesite — no asumir
  escalado lineal exacto del KV cache sin remedir.

## Smoke test (español, vía `/api/generate`, `stream:false`)

Prompt: *"Explica en dos frases qué es un nodo soberano en una red de cómputo local."*

- `total_duration`: 19.45s (incluye carga en frío del modelo a memoria — primera invocación tras
  `ollama create`)
- `prompt_eval_count`: 30 tokens · `prompt_eval_duration`: 0.30s
- `eval_count`: 78 tokens · `eval_duration`: 3.13s → **24.9 tok/s** en generación pura (CPU)
- Respuesta coherente y en español, sin errores.
