# El RAG de un espacio · por que aqui NO hay un esquema

Hubo un `rag_esquema.sql` en este directorio durante media hora y estaba **mal**.

`memory.buscar()` filtra por `e.status='activo'`, y aquel esquema escrito a mano no
tenia columna `status`. Habria creado una base con pinta de valida contra la que
`recuperar()` revienta -- que es peor que no tenerla, porque el fallo aparece el dia
que alguien confia en ella.

**El `rag.db` de cada espacio lo crea `memory.crear(ruta)`**, y asi hereda gratis el
esquema exacto que `recuperar()` espera, el FTS5 con sus disparadores, el diario WAL
(un corte de luz no corrompe el fichero) y los permisos `0600` desde el primer byte.

Es la Regla de Oro aplicada donde duele: *no reinventes lo que ya vive*. El RAG de
esta casa es `preceptor/memory.py:1013 recuperar()`, con presupuesto de tokens y con
la bandera `completo` que dice lo que dejo fuera. Reescribirlo peor no era una opcion.
