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

`cerebro_local.jsonl` (append-only, fuera de git — Bloque 12, 2026-08-04): una línea por sesión
delegada al cerebro local (`bin/cc-local`, `P0X_BRAIN=local`), escrita **a mano al cerrar sesión**;
hoy no hay proceso que la escriba sola:

```json
{"fecha":"<YYYY-MM-DD>","tarea":"i18n huérfanas Aurelius","cerebro":"local","pasadas":3,"minutos":25,"gate_ok":true,"ctx_pico":18400,"nota":"tres pasadas para lo que en frontera es una"}
```

- `cerebro`: `local` | `frontera` — se anotan **ambos** para que la comparación tenga contra qué.
- `pasadas`: intentos hasta pasar el gate. Es el número honesto: si el local necesita tres donde la
  frontera necesita una, el ahorro se ha movido al tiempo del Soberano y hay que verlo aquí.
- `gate_ok`: `tsc --noEmit` = 0 **y** tests en verde. Sin eso el trabajo no existe.
- `ctx_pico`: contexto máximo consumido en la sesión — insumo directo para re-elegir `num_ctx`.

Consumidor previsto: la reedición del reparto de cerebros documentado en
`deploy/soberano/CLAUDE.md` («El reparto de cerebros»). Sin estas líneas, ese reparto solo podría
re-decidirse de memoria — que es justo lo que la sección existe para impedir. **Fichero vacío a
fecha de hoy**: el Bloque 12 abortó en A2 y no llegó a haber sesión delegada que registrar.

Consumidor previsto: las mediciones n≥20 de los umbrales de reedición de
`mente/voces/*.md` (métrica_exito / umbral_reedicion) y el A/B del Alfabeto
(`mente/lengua/ALFABETO_P0X.md` §6, que usa su propio `lengua.jsonl` aquí mismo).
