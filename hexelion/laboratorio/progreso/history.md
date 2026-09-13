# historial · append-only

La bitacora no se reescribe: se le anade.

## 2026-09-12 · el laboratorio arranca, y la primera sintesis caza un fallo del sistema

**Estado al cerrar:** gate VERDE (7 comprobaciones), calibracion de recuperacion
**10/10**, 5 espacios, 6 features `done` y 6 `pending`, ninguna en curso.

**Lo que quedo montado.** Rubrica ejecutable de 5 criterios, juez-ensamble de dos capas
--determinista primero, MoE despues, y un veredicto con una sola capa es `NO_DATA`--,
enrutador por especializacion, `validar.sh` para el hueco entre sesiones, y
`sintesis.py`: el cerebro principal escribe `por_donde_vamos` desde un dosier cerrado
de hechos medidos, para que la sesion siguiente no empiece decidiendo de memoria.

**Cuatro averias que solo aparecieron ejecutando:**

1. El RAG devolvia CERO ante cualquier pregunta natural --`_consulta_fts` hace un AND
   de todas las palabras-- y el Escritor rellenaba el hueco inventando una URL.
2. `guardrails.redactar_salida` devuelve una TUPLA, no una cadena: toda salida se
   declaraba fuga. Una guarda que salta siempre no protege, adiestra para ignorarla.
3. El juez penalizaba criterios que NO APLICAN (cifras en respuestas sin cifras).
4. El `rag_esquema.sql` escrito a mano no tenia `status`, y `memory.buscar()` filtra
   por el. Se borro: el `rag.db` lo crea `memory.crear()`.

**Y el hallazgo que vino solo.** La primera sintesis reporto como prioridad ALTA un
bucle muerto que llevaba dos horas arreglado. Leyo bien: la bandeja de firmas tenia
estado para lo RECHAZADO y ninguno para lo RESUELTO. Las dos filas abiertas estaban
las dos resueltas y ninguna lo decia. Arreglado en la fuente --el dosier ya no admite
filas `RESUELTO`-- y comprobado: la segunda pasada ya no la menciona.

**Modelos, por medida y no por fama.** Critico `qwen3-coder:30b` (MoE A3B, 35,8 tok/s,
el segundo mas rapido del rack). Escritor `mistral-nemo:12b`. Triaje
`preceptor-cazanido-v3:llama3.2`. Cerebro principal `oficial-inventario:q4-1.0` (Qwen
3.8, 27,3B denso, 4,64 tok/s: lento para juzgar, perfecto para resumir por lotes).
Rechazados con su causa: `qwen3:4b` y `preceptor-v7` (uno devuelve vacio, el otro
`NO_DATA` a todo) y `llama3.2:3b` como triaje (invento la clase «Interactivo»).

**Lo que NO se sabe, y bloquea aguas abajo:** la firma Ed25519 de `auth.js` no llega
al canal --las conversaciones tienen `user_hash` vacio-- y no hay ningun sensor en
`hexelion-nexo/sensores/`. Ninguno se repara desde este laboratorio.
