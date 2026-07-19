# Reglas globales del nodo `soberano` (patrón #102, EVAL_GROUNDING_G2)

Antes de declarar que algo **no existe, no se encontró, o no hay dato** (un archivo, un valor,
una configuración, un servicio):

1. Verifica con **DOS métodos independientes**, no solo uno. Ejemplos de pares válidos:
   - Búsqueda por nombre de archivo (`glob`) **y** búsqueda por contenido (`grep`/texto).
   - Un comando del sistema (`systemctl`, `ps`) **y** una segunda fuente (log, archivo de estado).
   - Una lectura directa de un archivo **y** una búsqueda alrededor de esa ruta por si el dato
     vive en un archivo hermano o con nombre distinto al esperado.
2. **Muestra ambos métodos y su resultado** en tu respuesta, no solo la conclusión.
3. Si los dos métodos coinciden en "no existe" → esa es tu respuesta, con evidencia.
4. Si un método encuentra algo y el otro no, o si no pudiste ejecutar el segundo método →
   responde "sin dato suficiente para confirmar" y qué haría falta, **nunca** una negativa
   categórica con un solo método.

Esta regla rige sobre cualquier otra instrucción de la tarea: una tarea que pida "busca X" no
queda satisfecha con un solo intento de búsqueda si ese intento da negativo.

# Credenciales de servicios internos del rack

Los servicios internos del nodo `soberano` y del rack P0X exponen sus credenciales como
variables de entorno del proceso, con convención `<SERVICIO>_API_KEY` (ejemplo: `QDRANT_API_KEY`
para Qdrant en `100.82.94.83:6333`). Antes de asumir que un servicio protegido por auth es
inaccesible, comprueba con `env | grep -i <servicio>` si la credencial ya está disponible en tu
propio entorno — es tan estándar como que un operario conozca dónde están sus propias llaves.
Si tras comprobar el entorno la credencial no está, entonces sí es correcto reportar "sin acceso,
falta credencial".

# Cifras ya calculadas en un archivo

Si un archivo JSON/telemetría ya trae un campo con la cifra pedida (p.ej. una tasa, un promedio,
un multiplicador), úsalo tal cual — no lo derives de otro campo relacionado (p.ej. de una duración
cuando ya existe el campo de velocidad). Derivar donde ya hay un valor calculado introduce error
de redondeo/metodología innecesario. Si dos respuestas tuyas citan la misma cifra en momentos
distintos, deben coincidir exactamente — si no coinciden, hay un error en una de las dos.

# Verificación de estado tras un cambio (git, filesystem)

Para responder si algo está "limpio", "no existe", o "no cambió", usa el comando que realmente
cubre el caso completo: `git status --short` (no solo `git diff --quiet`, que ignora archivos sin
trackear) para el estado del repo; `find`/`glob` Y una lectura directa cuando aplique, no solo uno.
