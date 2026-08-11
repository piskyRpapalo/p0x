---
id: spec-d18-guardia-por-regla
titulo: Spec del refactor de la exención D8/D10 + parada por prohibición de alcance
tipo: operativo
clase: operativo
version: 1.0.0
dominio: refactor-guardia-higiene
estado: PROPUESTA · NO EJECUTADO
base: b6e0f66
actualizado: 2026-08-11
---

# SPEC · D18 · EXENCIÓN POR REGLA
### Fase 1 de la cascada: spec. No hay fase 2 ni 3 en esta sesión, y el motivo no es técnico.

---

## §0 · PARO · LA MISIÓN PIDE LO QUE EL CONTRATO ME PROHÍBE

La misión llegó en el formato de `04_CONTRATO_CLAUDE_CODE.md §9` — CONTEXTO COMPACTO / OBJETIVO / RESTRICCIONES / ENTREGA / GESTIÓN ERRORES. Es la plantilla con la que se entrega trabajo **al Ejecutor**. Yo no soy el Ejecutor.

Tres fundamentos independientes, cualquiera de ellos suficiente:

1. **Mi alcance.** `PROHIBIDO: editar código/datos productivos`. `guardia_higiene.py` y `test_guardia.py` son código productivo versionado. Mi escritura está limitada a `Cuarentena/salida/` y `Cuarentena/necropolis/`.
2. **Mi alcance, otra vez.** La misión ordena ejecutar `bin/p0x-instalar-ganchos`, que hace `install -m 755 "$FUENTE/$F" "$DESTINO/$F"` sobre `.git/hooks/` (línea 56 del script). `PROHIBIDO: modificar .git/`. La restricción de la misión «no tocar `.git/hooks/` directamente» se cumple en la letra y se rompe en el efecto: el script escribe ahí.
3. **D18, firmada, línea 132, literal:** *"Bloqueado: codigo productivo. Lo hace Claude Code tras firma, no el Preceptor."* La propia decisión que esta misión quiere resolver **me nombra y me excluye**.

Nombro las prohibiciones, como exige el contrato, y pido confirmación explícita. Si el Soberano quiere que yo edite ese fichero, hace falta una decisión firmada que amplíe mi alcance — no basta con que la misión lo dé por hecho.

**Lo que sí entrego, dentro de mi zona:** el spec y el parche exacto, `Cuarentena/salida/D18_guardia_por_regla.patch`, listo para `git apply`. Así el Ejecutor no improvisa su propia versión, que es la deriva que `04 §1` advierte que ya costó rondas.

## §1 · MEDIDO ANTES DE PROPONER

| Hecho | Cifra / valor | Comando |
|---|---|---|
| Commit base `b6e0f66` existe | tipo `commit` | `git cat-file -t b6e0f66` |
| `guardia_higiene.py` | 290 L · `5ba14f7af893a6ae` | `wc -l`, `sha256sum` |
| Reglas reales en `REGLAS` | **16** | `grep -oE '^\s+"[A-Z][A-Z0-9-]+",'` |
| `NODO-URL` y `CLAVE-PRIVADA` existen | sí, ambas | `grep -c` |
| Llamadas a `es_permitido_por_canon` | **1**, en línea 201 | `grep -n` |
| Árbol de trabajo | limpio salvo `?? bronze/` | `git status --porcelain` |

Los 16 IDs reales: `IP-TAILNET`, `IP-RFC1918`, `DOMINIO-PRIVADO`, `RUTA-HOME`, `NODO-USER-AT`, `NODO-HOST-PATH`, `NODO-DOMINIO`, `NODO-COMANDO`, `NODO-SSH-CONFIG`, `NODO-URL`, `NODO-PROMPT`, `USUARIO-FLAG`, `CLAVE-PRIVADA`, `CLAVE-PUBLICA-SSH`, `TOKEN-PROVEEDOR`, `SECRETO-ASIGNADO`. Los cinco que la misión nombra para D8 y los tres del suelo duro **existen todos**: no hubo que asumir nada.

## §2 · EL TEST YA ESTÁ ROJO. LLEVA DOS COMMITS ASÍ.

`python3 deploy/comun/hooks/test_guardia.py` → **`RESULTADO: 56/63 casos correctos, 7 fallo(s)`, EXIT=1.**

No hay que crear el test rojo: **existe y falla desde que R01 introdujo la exención por línea**. Se comprometió en `bdf2595` y otra vez en `b6e0f66` con la suite en rojo. Ese es el hallazgo más incómodo de esta ronda: el mecanismo que debía avisar avisaba, y nadie leyó su salida.

Los 7 falsos negativos actuales, con el patrón de D8/D10 que los tapa:

| Caso de `BLOQUEAN` | Regla esperada | Patrón que lo exime |
|---|---|---|
| `rsync -av ./deploy/ fragua:~/deploy/` | NODO-HOST-PATH | D8 `fragua:` |  <!-- guardia:permitir ejemplo-nodo-comando-documentacion-D8 -->
| `curl http://fragua:11434/api/tags` | NODO-HOST-PATH | D8 `fragua:` |
| `gateway 192.168.1.1` | IP-RFC1918 | D8 `192\.168\.\d+\.\d+` |
| `bind 10.0.0.5` | IP-RFC1918 | D8 `10\.\d+\.\d+\.\d+` |
| `cat /home/pisky/p0x/mente/doctrina/README.md` | RUTA-HOME | D8 `/home/pisky/` |
| `WorkingDirectory=/home/pisky/hexelion` | RUTA-HOME | D8 `/home/pisky/` |
| `aws: AKIAIOSFODNN7EXAMPLQ` | TOKEN-PROVEEDOR | D10 `AKIAIOSFODNN7EXAMPLQ` |

## §3 · EL REFACTOR NO PONE LA SUITE EN VERDE. ESTO ES LA PARADA DEL §GESTIÓN_ERRORES.

La misión dice: *"Si el test rojo no se puede hacer pasar sin romper otros tests, detenerse y reportar."* Se detiene y se reporta.

El parche se aplicó sobre copias en `/tmp` y se midió. **Antes: `56/63`, 7 fallos. Después: `58/64`, 6 fallos.**

- El caso rojo nuevo (`/home/pisky/` + `ghp_…`) **pasa**: `RUTA-HOME` salta primero, D8 la exime, el bucle **continúa** en vez de abandonar la línea, `TOKEN-PROVEEDOR` salta después y no está en las reglas de D8 → se reporta como `[TOKEN-PROVEEDOR]`. El agujero de D18, cerrado.
- **Detección recuperada de propina:** `rsync -av ./deploy/ fragua:~/deploy/` vuelve a bloquear. La regla que le corresponde es `NODO-COMANDO`, que no está entre las cinco de D8; antes la tapaba el patrón `fragua:` aplicado a la línea entera. Nadie lo pidió y aparece solo por dejar de eximir de más.  <!-- guardia:permitir ejemplo-nodo-comando-documentacion-D8 -->

Quedan **6 fallos**, y no por un defecto del parche: fallan porque la especificación de D8 que la misión fija y las expectativas de `test_guardia.py` **afirman cosas opuestas sobre las mismas líneas**.

- La misión ordena que D8 exima `IP-RFC1918`, `RUTA-HOME`, `DOMINIO-PRIVADO`, `NODO-URL`, `NODO-HOST-PATH`.
- `BLOQUEAN` afirma que `gateway 192.168.1.1`, `bind 10.0.0.5`, dos rutas `/home/pisky/…` y dos `fragua:` **deben bloquear**.
- Y `04 §3.5` dice: *"cero IPs de tailnet, cero hostnames, cero rutas de usuario, cero claves en nada publicable. Esta regla manda sobre cualquier mejora."*

Las tres no pueden ser verdad a la vez. Implementar la exención tal cual y luego mover los 6 casos de `BLOQUEAN` a `PASAN` para ver la suite en verde sería **hacer que el test se rinda ante el código**: el mismo vicio de forma que el propio D18 corrige, con otro disfraz. No lo hago por iniciativa propia.

Los 6 restantes, con la regla que dispara y el patrón de D8/D10 que la exime: `curl http://fragua:11434/api/tags` (NODO-URL ← `fragua:`) · `gateway 192.168.1.1` (IP-RFC1918 ← `192\.168\.`) · `bind 10.0.0.5` (IP-RFC1918 ← `10\.`) · `cat /home/pisky/p0x/…` y `WorkingDirectory=/home/pisky/hexelion` (RUTA-HOME ← `/home/pisky/`) · `aws: AKIAIOSFODNN7EXAMPLQ` (TOKEN-PROVEEDOR ← D10, exención correcta y deliberada).

### §3.1 · Lo que hay detrás: D8 se está leyendo más ancho de lo que se firmó

D8 dice: *"Las IPs tailnet y LAN son **visibles para Cowork**: necesarias para proponer arquitectura y filtro Edge real."*

Es una decisión sobre **qué puedo leer y citar yo en un documento**. La guardia, en cambio, es un gancho de **pre-commit**: decide qué entra al repositorio. Aplicar D8 ahí convierte «Cowork puede leer una IP privada» en «cualquier commit puede llevar rutas de usuario e IPs privadas» — una ampliación que nadie firmó y que choca de frente con `04 §3.5`.

## §4 · DOS CAMINOS COHERENTES (la decisión es del Soberano)

**Opción A — D8 es exención documental, acotada por ruta.** La exención solo aplica a los ficheros donde D8 tiene sentido (`Cuarentena/salida/`, `docs/post_verificacion/`). En el resto del árbol la guardia sigue bloqueando rutas e IPs privadas. `BLOQUEAN` se queda **intacto**, la suite va a verde con el parche más un filtro por ruta, y `04 §3.5` sigue en pie.
Coste estimado: S+ (el parche más un `EXENTOS_D8` por prefijo de ruta). Es la que recomiendo, y la recomiendo porque es la única que no enmienda el contrato.

**Opción B — D8 es exención global.** Se acepta que el repositorio lleve rutas de usuario e IPs RFC1918. Entonces hay que mover esos 7 casos de `BLOQUEAN` a `PASAN` **y enmendar `04 §3.5`**, porque hoy lo prohíbe con la fórmula más dura del contrato.
Coste estimado: S en código, L en doctrina.

En ambos casos el parche de §5 es necesario y suficiente para cerrar D18. Lo que cambia es qué se hace después con los 7.

## §5 · EL PARCHE

`Cuarentena/salida/D18_guardia_por_regla.patch`. Contra `b6e0f66`.

**Qué cambia, en tres movimientos:**

1. `DECISIONES_FIRMADAS` pasa de `d_id → [patrones]` a `d_id → {reglas, patrones}`. D8 lista sus cinco reglas; D10 solo `TOKEN-PROVEEDOR`.
2. `es_permitido_por_canon(linea, regla_id)` — el segundo parámetro es **obligatorio**, sin valor por defecto. Deliberado: si alguien vuelve a llamarla con un argumento, `TypeError` inmediato en lugar de una exención silenciosa. Se añade `D8_JAMAS = {TOKEN-PROVEEDOR, IP-TAILNET, CLAVE-PRIVADA}` y un `assert` de disyunción con las reglas de D8, que revienta al importar si alguien las mezcla.
3. En `escanear_lineas`, la consulta se mueve **dentro** del bucle de reglas, después del match y del filtro de placeholders. El `continue` sigue recorriendo `REGLAS`: una línea con una IP privada eximida y además un token se reporta por el token. Ahí está el fix.

**Nota sobre `D8_JAMAS` y D10:** el suelo duro es de D8, no global. D10 conserva la potestad de eximir `TOKEN-PROVEEDOR`, pero solo con sus dos patrones literales de fixture (`AKIAIOSFODNN7EXAMPLQ`, `ghp_…_FIXTURE`), que no coinciden con ninguna credencial viva. Si el suelo fuese global, D10 quedaría muerta sin decirlo — un efecto secundario que habría que descubrir con un test, y los efectos que se descubren con un test es porque no se declararon.

**Cómo se generó, y una confesión de método:** escribí el parche a mano primero y `git apply --check` lo rechazó — `corrupt patch at line 105`, recuentos de hunk mal calculados. Lo descarté y lo regeneré mecánicamente: copias de los dos ficheros en `/tmp`, ediciones aplicadas por script con `assert` sobre cada bloque literal a sustituir, `diff -u` entre las copias, y `git apply --check` contra el árbol real → **EXIT=0**. Lo digo porque en R02 confesé haber producido un artefacto con forma de prueba que no lo era; un parche escrito a mano y no validado habría sido el tercero de la serie.

**Verificación (la ejecuta quien aplique, no yo):**

- `git apply --check Cuarentena/salida/D18_guardia_por_regla.patch` → ya verificado: **EXIT=0**.
- `python3 deploy/comun/hooks/test_guardia.py` — esperado: **`58/64`, 6 fallos**, con el caso rojo nuevo en verde. Quien informe «suite en verde» sin haber tocado los 6 ha movido las expectativas, y eso debe verse en el diff.
- Verificado ya en `/tmp` sobre las copias: `python3 -m py_compile` de ambos ficheros compila; el escaneo directo de una línea con `/home/pisky/` + `ghp_…` reporta `[TOKEN-PROVEEDOR]`.
- `bin/p0x-instalar-ganchos` para propagar a `.git/hooks/`.
- Prueba directa del agujero: escanear en `--files` un fichero temporal fuera del repo con la línea `/home/pisky/` + `ghp_…` y comprobar que reporta `[TOKEN-PROVEEDOR]`.

**Plan de reversión:** `git checkout -- deploy/comun/hooks/guardia_higiene.py deploy/comun/hooks/test_guardia.py`. Ambos versionados en `b6e0f66`, árbol limpio, reversión de un comando. Si ya se reinstalaron los ganchos, `bin/p0x-instalar-ganchos` de nuevo tras el checkout; el script guarda `.previo` de cada gancho que sustituye (línea 53).

## §6 · NO_DATA

- Si el hook instalado hoy en `.git/hooks/` coincide con la fuente de `deploy/comun/hooks/`: no verificado (no leo `.git/`).
- Comportamiento de `escanear_diff` con el parche: no ejecutado. El parche no lo toca y comparte `escanear_lineas`, pero afirmarlo sin prueba sería exactamente lo que este documento reprocha.
- Motivo de que la suite roja se commiteara dos veces: `NO_DATA`. El gancho de pre-commit escanea higiene, no ejecuta la suite. Si eso es un hueco o una decisión, no me consta.
- Qué reglas quiso eximir D8 realmente: `NO_DATA`. D8 habla de visibilidad para Cowork y no menciona ninguna regla de la guardia. La lista de cinco viene de la misión, no de D8.

---

Pendiente de firma del Soberano para cierre de Ronda 3.
