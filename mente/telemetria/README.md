# mente/telemetria — telemetría viva del Sínodo

`sinodo.jsonl` (append-only, fuera de git): una línea JSON por chat v2 del Sínodo,
escrita best-effort por `hexelion_gateway.py` (`_log_sinodo_telemetria`):

```json
{"ts":"<ISO-8601 UTC>","voz":"monje","tok_in":812,"tok_out":96,"ms":2140,"grounded":true,"rag_k":5}
```

- `tok_in`/`tok_out`: reales del chunk final de Ollama (`prompt_eval_count`/`eval_count`);
  si el stream murió antes del chunk final, estimados con `_estimate_tokens` (jamás 0 falso).
- `grounded`: el bloque CONTEXTO del Second Brain llegó no-vacío al prompt.
- `rag_k`: hits devueltos por Qdrant `mente` para la pregunta.

Consumidor previsto: las mediciones n≥20 de los umbrales de reedición de
`mente/voces/*.md` (métrica_exito / umbral_reedicion) y el A/B del Alfabeto
(`mente/lengua/ALFABETO_P0X.md` §6, que usa su propio `lengua.jsonl` aquí mismo).
