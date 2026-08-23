# INFORME DE VERIFICACIÓN · PLAN v1.1 + EL TALLER

**Fecha:** 2026-08-23 · **Nodo:** soberano (Beelink) · **Metal secundario:** Doogee S110 vía Tailscale
**Encargo:** verificar el plan que llega de conversaciones con IA externas, asegurar el mejor MVP, y
separar lo público de lo que se construye en el Beelink para aprender Python con Aurelius local.

> Nada de este informe se apoya en lo que el plan afirma. Cada veredicto lleva el comando que lo
> produjo o la fuente oficial que lo dice. Donde no pude medir, lo digo.

---

## 0 · RESUMEN EN UNA PANTALLA

| # | Afirmación del plan | Veredicto | Impacto |
|---|---|---|---|
| 1 | Licencia: LICENSE es Apache y el README dice MIT | ✅ **CIERTO Y PEOR** | **Ya corregido**, commit `0fb9784` |
| 2 | «Probablemente `llama-completion` no soporta salida estructurada» | ❌ **FALSO** | **Sí la soporta. Medido en las dos máquinas** |
| 3 | Intent de Termux: `org.termux.RUN_COMMAND` | ❌ **FALSO** | La acción es `com.termux.RUN_COMMAND` |
| 4 | El intent abre la terminal desde el navegador | ❌ **NO PUEDE** | Chrome no tiene el permiso. **Tumba el §II** |
| 5 | Ruta `/usr/bin/aurelius` en Termux | ❌ **NO EXISTE** | Verificado en el Doogee |
| 6 | MCP: servidor stdlib de 100 líneas, 8-12 h | ⚠️ **OBSOLETO** | La revisión vigente cambió el modelo |
| 7 | «4 implementaciones de puertos = 4 bugs» | ⚠️ **SON 3, Y NO SE UNIFICAN** | 2 son bash, 1 python |
| 8 | FTS5 para búsqueda (B.2) | ✅ **VIABLE** | Disponible en ambas máquinas |
| 9 | `--import` no existe (B.3) | ✅ **CIERTO** | Asimetría real |
| 10 | Historial en el tablero (B.1) | ✅ **CIERTO** | **Debería ser la prioridad 1** |
| 11 | `aider --read` existe | ✅ **CIERTO** | Fuente oficial |
| 12 | `pathlib` en 2 h (A.4) | ❌ **IRREAL** | 335 usos en 43 ficheros |

---

## 1 · LA LICENCIA · confirmado, y era más grave de lo que dice el plan

**Lo que el plan dice:** «El fichero LICENSE contiene Apache-2.0 completo. El README dice MIT.»
**Lo que hay:** cierto, y además un documento afirmaba lo contrario por escrito.

`LICENSE` es el Apache-2.0 completo desde el commit `11acf6e` del **2026-08-19**. Ese commit tocó
`LICENSE` **y nada más** — verificado con `git show --name-only 11acf6e`. Durante cuatro días el
repositorio ha entregado Apache-2.0 mientras siete sitios prometían MIT: `README.md` (badge y
sección), `pyproject.toml` (texto y clasificador OSI), `MARCA.md`, `RELEASE_v1.0.md`, `ASSETS.md`
(dos menciones) y `assets/badges/code.svg`.

**El hallazgo que el plan no vio.** El **2026-08-22** se «corrigió» `MANIFIESTO.md` escribiendo:

> *«Corregido el 2026-08-22. Esta linea decia `Apache-2.0`, y en este arbol no existe ninguna
> licencia Apache: `LICENSE` es MIT»*

Era falso al escribirlo — llevaba tres días siendo Apache. La corrección se hizo **de memoria y no
mirando el fichero**, que es exactamente el fallo que ese documento existe para impedir. Queda como
cicatriz fechada con la frase falsa citada dentro: borrarla dejaría el agujero sin señal.

**Estado:** reconciliado y commiteado (`0fb9784`), 282/282 en verde.

**Lo que NO toqué y conviene que sepas:** `aurelius.py:81` dice `licencia="MIT"` y **debe seguir
diciéndolo** — es la licencia del modelo de voz de Piper, un hecho sobre la pieza de otro. Un
`sed` global habría publicado una licencia ajena equivocada.

**Nota legal honesta:** quien ya recibió el código creyéndolo MIT lo tiene bajo MIT para esa
versión; el cambio rige de aquí en adelante. Ambas son permisivas, Apache añade concesión de
patentes y requisitos de aviso. No hace falta fichero `NOTICE` (Apache-2.0 no lo exige; solo obliga
a propagarlo si existe).

---

## 2 · LA CORRECCIÓN MÁS VALIOSA · el motor SÍ hace salida estructurada

**Lo que el plan dice:** *«Opción B (si no soporta structured outputs, **más probable**): usar
prompt estricto estilo Simon Willison… máximo 2 intentos si falla la validación.»*

**Lo que hay:**

```
-j,  --json-schema SCHEMA       JSON schema to constrain generations
-jf, --json-schema-file FILE    File containing a JSON schema
     --grammar GRAMMAR          BNF-like grammar to constrain generations
```

`llama-completion` **sí** restringe la generación por esquema, a nivel de muestreador. No es «pedir
por favor y validar»: es que **los tokens que romperían el esquema no se pueden emitir**. La
diferencia importa — la opción B tiene una tasa de fallo distinta de cero y necesita reintentos; la
opción A no puede producir JSON mal formado.

### Medido con el modelo real, no leído del `--help`

| Máquina | Modelo | Tiempo | Resultado |
|---|---|---|---|
| Beelink | Qwen3-4B Q4_K_M | **10,2 s** | JSON válido, tres claves correctas |
| Doogee S110 | Qwen3-4B Q4_K_M | **2 min 13 s** | JSON válido, tres claves correctas |
| Beelink | Qwen3-Coder-30B-A3B Q4_K_M | **49,2 s** | JSON válido, código con docstring y manejo de errores |

Y un detalle que ahorra trabajo: el binario añade `[end of text]` al final, pero
**`conversacion.limpiar()` ya lo quita**. Probado: `json.loads(conversacion.limpiar(crudo))` parsea
sin tocar nada.

> **Consecuencia para el Taller Nivel 1:** desaparecen el prompt-hack, la validación con
> reintentos y el caso «JSON inválido». La implementación es `-jf esquema.json` + `limpiar()` +
> `json.loads()`. Menos código, sin rama de fallo, y determinista.

Nota: el Doogee tarda **menos** en esto (2m13s) que en un turno de charla (5-8 min medidos ayer),
porque la salida es corta y acotada. El Taller es **más rápido que conversar** en el teléfono.

---

## 3 · LO QUE TUMBA EL §II · el intent de Termux no puede hacer lo que el plan pide

Tres errores encadenados, del menor al que rompe el diseño.

**a) La acción está mal escrita.** El plan usa `org.termux.RUN_COMMAND`. La documentación oficial
dice `com.termux.RUN_COMMAND`. Con la cadena del plan no pasa nada, ni un error visible.

**b) Falta un requisito que el plan no menciona.** Termux exige `allow-external-apps=true` en
`~/.termux/termux.properties`, *«regardless of if the executable path is inside or outside the
~/.termux/tasker/ directory»*. En el Doogee **no está puesto** — comprobado.

**c) El que rompe el diseño.** `RunCommandService` se declara con
`android:permission="com.termux.permission.RUN_COMMAND"`. Ese permiso lo tiene que tener **la
aplicación que llama**, declarado en su manifiesto. Cuando la llamada nace de un enlace en una
página web, **la aplicación que llama es Chrome**, y Chrome no declara ese permiso ni puede.

**Una página web no puede ejecutar comandos en Termux por intent. Punto.** No es un ajuste que se
active una vez: es que el emisor equivocado nunca tendrá el permiso.

**d) Y la ruta no existe.** `/data/data/com.termux/files/usr/bin/aurelius` — comprobado en el
teléfono: `No such file or directory`. No hay ningún `aurelius` en el `PATH` de Termux; los
ejecutables viven en `~/aurelius/bin/`.

### Lo que SÍ se puede hacer (propuesta, no aplicada)

1. **Abrir Termux sin ejecutar nada** — el intent `MAIN`/`LAUNCHER` no pide permiso alguno. La
   página abre Termux, y el comando va **en el portapapeles**. El carbono pega y pulsa intro. Eso
   no es un parche: es HITL de verdad, y es más honesto que un botón que ejecuta.
2. **El portapapeles como camino principal, no como respaldo.** `navigator.clipboard.writeText()`
   funciona siempre, en PWA y en pestaña. El plan lo pone de plan C; debería ser el plan A en
   Android.
3. **En PC el protocolo `aurelius://` sí es viable** — es el patrón de `vscode://`, y ahí el
   diálogo del sistema operativo es el primer HITL, tal como dice el plan. **No verificado por mí**:
   no he registrado ni probado un handler `.desktop`. Queda como pendiente medible.

---

## 4 · MCP · viable, pero el plan está escrito contra una revisión vieja

La revisión vigente de la especificación es **2026-07-28** — el plan la cita bien en §VIII. Pero el
código del §VI devuelve `"protocolVersion": "2024-11-05"`, y eso no es un descuido cosmético:

- La revisión actual dice que **«servers do not initiate JSON-RPC requests»**.
- Y sobre todo: *«**Earlier** protocol revisions established a connection-scoped session with an
  `initialize` handshake»* — en pasado. Ahora los metadatos de protocolo viajan **en cada petición**,
  en campos `_meta.io.modelcontextprotocol/*`.

El transporte **stdio sigue existiendo** y sigue siendo *«newline-delimited JSON-RPC over a byte
stream»*, así que la idea es sólida y es implementable en biblioteca estándar. Lo que no se sostiene
es el atajo: los tutoriales de «servidor MCP en 100 líneas» que el plan cita describen el modelo
**anterior**. Funcionarían por la vía de compatibilidad hacia atrás, no por la vigente.

**Veredicto:** Nivel 3 sigue siendo viable y sigue siendo v1.2. La estimación de 8-12 h asume copiar
una receta conocida; con la revisión vigente hay que leer la especificación. Súbelo a 16-20 h o
acepta implementar deliberadamente la era antigua y depender del *fallback*.

---

## 5 · LA DEUDA TÉCNICA · lo que resiste una medición y lo que no

**A.1 · Puertos.** El plan dice «4 implementaciones = 4 bugs recurrentes». Son **tres**:
`bin/instalar-pc` (bash + curl), `bin/aurelius-servicio` (bash + curl) y `empaquetado/lanzador.py`
(python `connect_ex`). Y aquí está lo que el plan no vio: **dos son bash y una es Python**. Un
módulo `bin/gestion-puerto.py` no las unifica — obligaría a los instaladores bash a lanzar un
proceso Python para preguntar por un puerto, que es peor que los dos `curl` de dos líneas que ya
tienen. Además **no encontré los «bugs recurrentes»**: no hay incidencias ni cicatrices que los
documenten. Refactor especulativo. **Recomiendo posponerlo hasta que un fallo real lo pida.**

**A.2 · Migraciones.** Real y con matiz. Hoy `memory.crear()` hace `executescript` del esquema más
un `ALTER TABLE` en `try/except OperationalError`. Es aditivo y silencioso: funciona, pero no deja
constancia de en qué versión está una memoria, y ya hay **tres** patrones distintos de creación de
tablas conviviendo (`memory.crear`, `proyectos.asegurar`, y las tablas que monta la fuga).
`PRAGMA user_version` ordena eso. **Vale la pena, con cuidado extremo**: es el único punto de este
plan que puede corromper la memoria de una persona, que es lo único que este producto promete no
hacer nunca.

**A.4 · pathlib.** El plan estima 2 h. Medido: **335 usos de `os.path` en 43 ficheros**, frente a 9
ficheros que ya usan `pathlib`. No es un `sed`: cada uso es una decisión sobre rutas, en un producto
cuyo valor es no perder un fichero. Coste real de un día largo, beneficio estético, riesgo de
regresión en la parte que más duele. **Recomiendo NO hacerlo**, o hacerlo solo en ficheros nuevos y
dejar que el resto migre cuando se toque por otra razón.

**A.5 · Versionado de API.** Cierto: 11 rutas `/api/…` sin versión. Coste real ~1 h, beneficio real
el día que cambie un JSON. Barato. **Adelante.**

**A.3 · excepciones.py.** La corrección del plan (raíz, no `laminas/`) es correcta —`laminas/` es
para las láminas de arte, y ahí vive `recortar.py`, que no es producto. Pero **no encontré
evidencia** de que el manejo actual de errores falle. `conversacion.py` ya distingue `SinCerebro` de
`SeAgotoElTiempo`, que es justo la distinción que importa. Prioridad baja.

**A.6 y A.7 · Logs y métricas.** No hay logs estructurados (solo `AURELIUS_PWA_LOG`, texto plano) ni
tabla de métricas. Ciertos. Pero cuidado con A.7: una tabla `metrics` dentro de `memory.db` mezcla
telemetría con memoria de una persona en el fichero que el README promete que puedes llevarte. Si se
hace, **fichero aparte**.

---

## 6 · LO QUE FALTA EN EL PLAN

**B.1 · El historial es lo más urgente del documento entero, y está en la Fase B.** Hoy el tablero
**no carga historial**: abres Aurelius y la conversación está vacía aunque los turnos estén
guardados en la memoria. Es lo primero que nota cualquiera en el primer minuto, y contradice de
frente el argumento del producto — *«recuerda lo que le dices»* y al abrir no hay nada. Ninguna
tarea de la Fase A se nota tanto. **Debería ir antes que toda la deuda técnica.**

**Falta `--modelo` en la terminal.** `bin/aurelius-pwa` acepta `--modelo <ruta>`, pero
`aurelius.py --charla` resuelve el cerebro a una ruta fija más el registro de afinado. Para aprender
Python en el Beelink con un modelo grande, la terminal es justo donde lo quieres. Es una hora de
trabajo y desbloquea todo el §7 de este informe.

**El tag `v1.0.0`.** No lo he creado. Lo dejo a tu firma: un `v1.0.0` es inmutable en la práctica, y
tenerlo apuntando a un árbol cuya licencia acabo de reconciliar merece que lo decidas despierto. Con
tu palabra lo creo local en un minuto.

---

## 7 · LA DIFERENCIACIÓN · MVP público vs Aurelius local en el Beelink

Esto es lo que pediste separar, y la medición lo separa sola.

### La misma app, dos cerebros, dos productos distintos

| | Doogee (4B) | Beelink (4B) | Beelink (30B Coder) |
|---|---|---|---|
| Snippet con esquema | 2 min 13 s | 10,2 s | 49,2 s |
| Calidad medida | factorial recursivo, sin validación | correcto, con guardas | **docstring, `Args`/`Returns`, `try/except`, ejemplo de uso** |
| Sirve para | recordar, consultar, un snippet suelto | uso diario cómodo | **aprender de verdad** |

El 30B ya está en el Beelink (`~/p0x/soberano-bench/models/Qwen3-Coder-30B-A3B-Instruct-Q4_K_M.gguf`,
18,5 GB). Con 57 GB de RAM cabe de sobra. **No hay que construir nada para tenerlo: hay que
permitir apuntarlo**, que es la hora de trabajo del `--modelo` de arriba.

### La línea de separación que propongo

**Va al MVP público** — lo que se sostiene con el 4B en un teléfono:

- Historial en el tablero (B.1) · **prioridad 1**
- Búsqueda FTS5 (B.2) · verificado disponible en ambas máquinas
- `--import` simétrico (B.3)
- Taller Nivel 1 con `--json-schema` · **medido viable incluso en el Doogee**
- `--modelo` en la terminal · barato y es la puerta de todo lo demás
- Versionado de API (A.5) · barato
- Migraciones con `user_version` (A.2) · con cuidado

**Se queda en el Beelink, para que aprendas Python con Aurelius local** — lo que necesita músculo:

- **El 30B como cerebro por defecto en tu instalación.** No es una funcionalidad nueva: es un
  `--modelo` y un `cerebro.json`. El mecanismo de afinado que ya existe (pieza al lado, huella
  propia, rollback por preferencia) sirve tal cual.
- **El Taller con revisión de código**, no solo generación. Un 4B genera un snippet; un 30B lee lo
  que escribiste y te dice por qué falla. Esa es la diferencia entre una herramienta y un preceptor.
- **El Camino de Python como proyecto tuyo.** Aquí está la pieza bonita, y ya existe: el arquetipo
  tiene prohibido proponer el tema (`conversacion.py:277`, *«nunca propongas el tema ni el dominio:
  no es tuyo»*). Tú traes Python; él lo recorre contigo, una pregunta cada vez, y **mide** dónde
  estás desde tu propia memoria en vez de suponerlo. No hay que programar pedagogía: hay que darle
  el cerebro que aguante la conversación.
- **Nivel 2 (Aider) y Nivel 3 (MCP).** Ambos son de escritorio por naturaleza. `aider --read` está
  confirmado y funciona con un fichero de contexto; el MCP necesita la especificación vigente.

**Criterio de la línea, en una frase:** *entra en el público lo que un teléfono puede cumplir; se
queda en el Beelink lo que necesita un cerebro que un teléfono no puede cargar.* Es un criterio
medible, no una opinión — y es el mismo que ya usa el producto cuando declara «no medible» en vez de
pintar una barra.

### Sobre el «producto de pago»

No he creado `docs/VIABILIDAD_MVP_VS_PAGO.md` **en el repositorio público**, y quiero decirte por
qué antes de que lo firmes. Publicar hoy un documento que reparte funciones entre gratis y pago,
antes de que exista ninguna función de pago, le dice a quien llega que hay un muro más adelante.
Ese README acaba de ganar su argumento siendo honesto sobre lo que no hace; un roadmap de paywall al
lado le quita fuerza. **Propongo:** el reparto vive en la forja (este informe lo contiene), y al
público se le dice lo que hay cuando haya algo. Si prefieres publicarlo, lo escribo en cuanto lo
firmes — es tu decisión, no mía.

---

## 8 · SUGERENCIAS

1. **(S) Firmar el orden nuevo: B.1 primero.** El historial antes que toda la Fase A. Es lo único
   de la lista que un desconocido nota en sesenta segundos.
2. **(S) `--modelo` en `aurelius.py --charla`.** Una hora. Desbloquea el 30B en el Beelink sin
   tocar nada más, y no rompe el teléfono.
3. **(S) Reescribir el §II con el mecanismo que existe:** abrir Termux con `MAIN`/`LAUNCHER` +
   comando al portapapeles. Y decidir si «Frontera» se convierte en «Taller» **antes** de que la
   barra de cinco iconos entre en una captura del README.
4. **(M) Taller Nivel 1 con `--json-schema`.** Sin reintentos, sin prompt-hack. Medido viable en
   las dos máquinas. Es la tarea con mejor relación valor/riesgo del plan.
5. **(M) `PRAGMA user_version` con pruebas de migración sobre copias reales**, no sobre memorias de
   juguete. Es el único punto que puede corromper lo que el producto promete no corromper.
6. **(L) Retirar A.4 (pathlib) del plan** o degradarlo a «solo en ficheros nuevos». 335 usos en 43
   ficheros por un beneficio estético, en la parte que más duele si se rompe.

---

## 9 · FUENTES

- Termux `RUN_COMMAND` — https://github.com/termux/termux-app/wiki/RUN_COMMAND-Intent
- Termux, divulgación de vulnerabilidades (permiso del servicio) —
  https://termux.dev/en/posts/security/2022/02/15/termux-apps-vulnerability-disclosures.html
- MCP, especificación vigente 2026-07-28 — https://modelcontextprotocol.io/specification/
- MCP, transportes (stdio, y el cambio de modelo de sesión) —
  https://modelcontextprotocol.io/specification/2026-07-28/basic/transports
- Aider, `--read` para ficheros de contexto — https://aider.chat/docs/usage/conventions.html
- `llama-completion --help`, build 10488 (commit `9d77fa172`) en soberano — medido, no citado.

**Lo que NO verifiqué y no debe darse por cierto:** el protocolo `aurelius://` en PC (no registré
ningún handler `.desktop`); el comportamiento real de un `intent://` disparado desde una PWA en modo
standalone; y si `aider` acepta `--model ollama/qwen3-coder` con la versión que instalarías (la
página de conventions no lo cubre).
