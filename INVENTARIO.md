# INVENTARIO · la web y la app, pieza por pieza

**Fecha: 2026-09-05.** Escrito para que la sesión siguiente **no repita
trabajo ya hecho** y pueda ir directa a lo que no está optimizado. Todo lo de
aquí está contado de los ficheros, no recordado.

Dos productos distintos, y no se confunden nunca:

- **La web** (`~/preceptoros-web` → `preceptoros.org`) es la **puerta**: guía
  para romper la barrera técnica, y donde nace la comunidad.
- **La app** (`~/p0x/preceptor` → repo `PreceptorOS`) es el **taller**: mide
  la IA en tu máquina y convierte lo que le cuentas en memoria tuya.

---

# PARTE 1 · LA WEB

## 1.1 · Las páginas

**56 páginas: siete por idioma, ocho idiomas** (es · en · fr · pt · it · de ·
ru · el). Más la raíz `/`, que es el selector de idioma.

| Página | Qué es | Piezas que la componen |
|---|---|---|
| `index.html` | **La portada.** Cabecero, esfera, chat con el rack, atajos, ficha del modelo, pie honesto | ver 1.2 |
| `instalar.html` | Los pasos reales de instalación, la instalación de la web como app, el enlace a la última versión y el catálogo de modelos con el mínimo para un teléfono de 8 GB | `#pwa-puerta` `#descargas` `#modelos-descarga` `#android` `#atasco` |
| `benchmark.html` | **LoRAtelier**, el Libro de Pruebas: elegir motor, medirlo, y de dónde sale la tabla | `#tabla` `#probador` `#medida-json` `#local-ai` `#motor` |
| `community.html` | **El Ágora**: anuncios oficiales y tablón de hilos | `#anuncios` `#hilos` |
| `onboarding.html` | Cuatro pasos de entrada: qué es, privacidad, descarga, código de vinculación | `#ob-que` `#ob-privacidad` `#ob-descarga` `#ob-vincular` `#ob-codigo` `#ob-voz` |
| `playground.html` | **Probador de privacidad**: pegas texto sucio y ves qué tacha la frontera | `#sucio` `#limpio` `#sanear` `#auditoria` |
| `profile.html` | Tu ficha: identidad, avatar, biografía, medidas y contribuciones | `#perfil-identidad` `#perfil-avatar` `#perfil-bio` `#perfil-medidas` `#perfil-contribuciones` `#perfil-compartir` |

**La raíz `/`** es su propia página: el busto despertando, el nombre, ocho
nubes violeta con canto dorado —una por lengua, todas iguales— y la fórmula
`Knowledge + Tools + Sovereignty` en verde, sólo en inglés.

## 1.2 · La portada, de arriba abajo

Todo vive dentro de **un solo marco de bronce** (`main:has(#chat)`), que es lo
que engloba el lugar de trabajo entero.

**El cabecero** (`#cabezal`)
- `.marca` — «Preceptor**OS**» con canto de bronce en la letra, más los iconos
  de GitHub y LinkedIn.
- `#identity` — sin sesión, un icono de persona que abre un popover nativo con
  el aviso de que la clave no se recupera. Con sesión, una línea fina: nombre
  (enlaza al perfil) y firma corta de seis dígitos.
- `.lateral-boton` (rueda) — abre `#panel-ajustes`: idioma, piel clara/oscura,
  pantalla completa y la cola de firma con su punto rojo de aviso.
- `.cab-solar` — **la nube de la pila**: pastilla violeta honda con canto
  dorado, una pila que se carga de violeta a oro, «Powered» en verde y la
  declaración solar en oro.
- `#cab-nav` — las cuatro puertas: INICIO · LORATELIER · COMUNIDAD · INSTALAR.
  Violeta con canto dorado, a tamaño mínimo.
- **Escritorio:** marca izquierda, los dos mandos gemelos en la esquina
  superior derecha. **Teléfono:** dos renglones — marca con sus iconos, y
  debajo la cuenta con la rueda a la derecha.

**La esfera** (`.presentacion` · Capa 4)
Cuelga del cabecero, anclada a la derecha, empezando **por debajo** de los dos
mandos para no taparlos. Tres tiras de animación con su aritmética firmada:
reposo 122,5 % · pensando 612,5 % (cinco láminas) · habla 490 % (cuatro bocas),
todas con desplazamiento 27,78 %. **Pensar y hablar son dos cosas**: el ojo se
mueve mientras genera, la boca sólo cuando llega texto. Al pensar se enciende
en **neón** y saca la nube «Activando modelo». Cada 25-40 s hace un gesto suelto
para que la pantalla no parezca rota.

**La placa del chat** (`#chat` · Capa 1)
- `#dialogo` — la conversación. Nace abajo y empuja hacia arriba; el texto se
  **desvanece con una máscara** al llegar al cabecero.
- `.chat-abajo` — pegajosa al fondo: el campo con su pista («Escribe aquí para
  hablar con X», plantilla con hueco por lengua) y los dos mandos en círculo,
  **sólo dibujo**: enviar relleno, micrófono hueco.
- `#chat.pleno` — Capa 5, pantalla completa, se sale por el aspa o con Escape.

**Los atajos** (`#atajos`) — tres de escritura más los ocho comandos de
servicio (`/instalar`, `/perfil`, `/dataset`, `/script`, `/eco`, `/formatos`,
`/auditar`, `/frontera`), todos con la misma figura.

**El cuadro de especificaciones** (`#especificaciones`) — **una caja, no tres
cosas sueltas**: quién te habla y para qué sirve, el motor (`#brain`), la
velocidad medida por backend, y las ocho nubes de compañero, a la vista y sin
tener que abrir nada.

**El pie honesto** — las cifras de pruebas, peticiones externas y tope por
fichero.

**El telón** — el despertar: siete fotogramas en 1,2 s y la cortina cayendo a
1,8 s. **Bloquea las capturas headless** (ver 1.7).

## 1.3 · Las dieciocho hojas de estilo

Cada una manda sobre un asunto, y el **orden de carga es la autoridad real**:
a igual especificidad gana la última.

| Hoja | B | De qué manda |
|---|---|---|
| `base.css` | 12 247 | Canon visual v4.0. Tokens, tipografía, botones, campos, el mármol |
| `movil.css` | 2 823 | Lo mismo, en un teléfono |
| `canon.css` | 10 888 | Anexo firmado: R-WIDGET, R-TIPOGRAFÍA, la escala de capas, el canto dorado del nombre |
| `chat.css` | 9 014 | Lo que **pinta** el chat: badge, corrección, cantos, pantalla completa |
| `escribir.css` | 12 636 | Lo que se **toca** para mandar un turno: campo, atajos, los dos mandos |
| `placa.css` | 12 588 | Cuánto **mide** la placa y quién se desplaza. Aquí vive el reparto con el teclado abierto |
| `cara.css` | 12 592 | La cara y su aritmética |
| `senal.css` | 4 826 | Lo que la cara **dice** esperando: neón y nube |
| `widget.css` | 13 899 | Cabecero, cristal de los paneles, y **el marco único** |
| `puertas.css` | 9 105 | Las cuatro puertas y el cabecero de las interiores |
| `cabezal.css` | 6 812 | El cabecero en pantalla estrecha |
| `esquina.css` | 14 987 | **Dónde** caen los mandos, la cuenta, y a qué altura nace la cara |
| `mandos.css` | 6 604 | **Cómo** se pintan esos mandos y la pila solar |
| `panel.css` | 15 105 | El mueble de los desplegables y la cola de firma |
| `nubes.css` | 8 439 | Lo que va **dentro**: las nubes de compañero y la ficha |
| `tema.css` | 5 729 | El tema oscuro, trasplantado de la app |
| `agora.css` | 6 402 | Tablón y LoRAtelier |
| `onboarding.css` | 1 938 | El onboarding |

## 1.4 · Los guiones

**42 ficheros**, de los que **8 son papeles de modelo** (`prompts-<lang>.js`,
uno por lengua) y **no son interfaz**.

*Chat y compañeros:* `chat.js` (el turno) · `chat-router.js` (elegir compañero)
· `chat-panel.js` (mandos y teclado del móvil) · `senal.js` (la cara como
sensor y la nube de espera) · `comandos.js` (los ocho servicios) ·
`corregir.js` (corregir una respuesta) · `hub.js` (cabecero y catálogo) ·
`hub-cola.js` (cola de firma y piel).

*Motor y medida:* `engine.js` · `localai.js` · `rack.js` · `state.js` ·
`medidas.js` · `meter.js` · `benchmark.js` · `fallback.js` (el JSON que te
llevas a otra IA).

*Identidad y perfil:* `auth.js` · `profile.js` · `profile-obra.js`.

*Páginas:* `onboarding.js` · `instalar-descargas.js` · `playground.js` ·
`sanitize.js` · `board.js` · `board-anuncios.js` · `board-fuentes.js` ·
`nav.js` (cabecero de las interiores).

*Casa:* `pwa.js` · `ambient.js` · `voice.js` · `copiar.js`.

## 1.5 · Los datos

`hub.json` (catálogo de agentes) · `hub-textos.json` (sus textos en 8 lenguas)
· `modelos.json` · `medidas.json` (velocidad, con contrato de máquina) ·
`instalar.json` · `nav.json` · `servicios.json` · `anuncios.json` ·
`threads.json` · `counters.json` · `bustos.json` · `manifest.webmanifest`.

## 1.6 · Lo visual

`public/assets/` pesa **3,9 MB de los 4,7 MB del sitio**, y **2,1 MB son
`assets/caras/`** — las tiras de animación de la esfera y el telón. El resto
son iconos, el mármol con vetas violeta (`marble-violet.webp` y su gemelo
oscuro), el canto de metal (`edge-violet.png`) y los bustos 3D del catálogo.

`docs/img/` tiene cuatro capturas **regeneradas el 2026-09-05** contra la
versión desplegada: `puerta` · `chat` · `install` · `phone`.

## 1.7 · Las reglas, y las trampas

**Las reglas del gate** (`test_web.py` 76/76 · `arnes_sw.mjs` 21/21):

1. **16 KiB por fichero.** Al pasarse **se parte por asunto; nunca se recorta
   un comentario** — son la documentación de esta casa. Hoy se partió siete
   veces.
2. **Paridad de idiomas**: toda clave `T.algo` existe en las ocho portadas.
3. **Contraste medido**, con la medida escrita al lado.
4. **Cero peticiones externas al cargar.**
5. **Un hueco se llama hueco**, con su causa.

**Las cinco trampas que ya mordieron:**

- **El guardián lee los comentarios como código.** Nombrar un radio o un
  `backdrop-filter` en la frase que explica por qué *no* se usan pone el gate
  rojo. Seis veces hoy. Se reformula la frase, no se toca el guardián.
- **El caché del navegador enseña código viejo.** La única forma fiable de
  mirar un cambio es **servir en un puerto nuevo**.
- **El telón bloquea las capturas headless**: el tiempo virtual de Chrome no
  adelanta su retardo. Se fotografía sirviendo una copia de `public/` con el
  bloque `.telon` quitado.
- **`display:contents` anula el `order` del envoltorio.**
- **Un `top` no gana a un margen: se suman.**

---

# PARTE 2 · LA APP

## 2.1 · La interfaz

`interface/` pesa 268 KB en doce ficheros.

| Fichero | Tamaño | Qué es |
|---|---|---|
| `dashboard.html` | 18 KB | **La pantalla principal**: cabecero con busto, chat, y seis cajones |
| `dashboard.css` | **83 KB** | Todo su aspecto |
| `dashboard.js` | **85 KB** | Todo su comportamiento |
| `app.html/.css/.js` | 34 KB | La app envuelta |
| `compass.css/.js` | 16 KB | La Brújula de Aprendizaje |
| `privacy_toggle.*` | 7,5 KB | El interruptor de privacidad |
| `sw.js` | 2,8 KB | El worker |

**Los seis cajones**: `camino` (rutas de aprendizaje) · `memoria` ·
`proyectos` · `frontera` (qué tacha antes de salir) · `medicion` (la tabla de
velocidad) · `perfil`.

Otras piezas visibles: `#telon` y `#velo` (el despertar) · `#busto` con sus
estados · `#lateral` con su `#lateral-boton` · `#atajos` · `#escribir` con
`#dicho`, `#mandar` y `#hablar` · `#espejo` · `#fusion` · `#eleccion` ·
`#manifiesto-texto`.

## 2.2 · El motor

**80 ficheros Python: 39 módulos y 41 suites de prueba.** Uno por uno los
módulos hacen una cosa:

*El agua (memoria):* `memory.py` · `manifest.py` · `preceptoros.py` (la
conversación de recuperación en siete pasos) · `hilos.py` · `proyectos.py`.

*El turno:* `conversacion.py` · `herramientas.py` (lo que la base ya sabe,
puesto delante del modelo) · `narrador.py` · `interprete.py` · `corredor.py`.

*La frontera:* `frontera.py` (Wasmtime) · `output_guard.py` · `guardrails.py`
· `fuga.py` · `sanitize` en el lado web.

*Medida y cerebro:* `afinado.py` (hot-swap con rollback) · `metricas.py` (las
once métricas de la norma) · `compass.py` · `estado.py`.

*Identidad y carácter:* `huella.py` · `caracter.py` · `path.py` · `andamio.py`.

*Casa:* `casa.py` · `entorno.py` · `descarga.py` · `captura.py` · `oido.py` ·
`silencio.py` · `soberania.py` · `lore.py`.

`bin/` tiene los lanzadores: `preceptoros-servicio`, `preceptoros-pwa`,
`instalar-android`, `instalar-pc`, `crear-acceso-directo-android`,
`eco-remoto`, y los enlaces con el nombre viejo (`aurelius-*`) que siguen
funcionando.

`docs/` guarda cuatro documentos: `ANALISIS_DOCTRINAL_v1_2.md` ·
`CANON_NIVELES.md` · `COMPASS.md` · `SOBERANIA.md`.

**Gate:** `bin/pruebas` — 617 en verde.

---

# PARTE 3 · LO QUE ENCONTRÉ MAL MIENTRAS DOCUMENTABA

Cinco cosas. Ninguna se ha tocado: van como **propuesta**, con su coste.

### 1 · Tres guiones que no carga nadie · **S**
`hitos.js` (2 050 B), `manifiesto.js` (1 400 B) y `pie.js` (2 458 B) están en
`public/assets/` y **ninguna de las 56 páginas los enlaza**. Son 5,9 KB de
código muerto que además el gate vigila, mide y sirve.
*Fix propuesto:* comprobar el historial por si su página vuelve, y si no,
borrarlos dejando una línea en el commit que diga de qué página eran.

### 2 · El onboarding promete una descarga que no existe · **S**
`onboarding.html` tiene un paso 3 «Descarga la app» y un paso 4 «Tu código de
vinculación». Pero `instalar.html` declara, con su NO_DATA y su fecha, que **no
hay ninguna release publicada** y que el enlace da 404. Dos páginas del mismo
sitio dicen cosas distintas sobre el mismo hecho, y la que promete es la que
ve primero quien llega.
*Fix propuesto:* que el paso 3 lea el mismo dato que `instalar-descargas.js` ya
consulta, en vez de afirmarlo por su cuenta. Un solo sitio decide si hay
descarga.

### 3 · La app no tiene tope por fichero · **L**
`dashboard.css` pesa **83 KB** y `dashboard.js` **85 KB**: cada uno es cinco
veces el tope entero de la web. La doctrina de «se parte por asunto, no se
recorta» está escrita y probada en la web y **no se ha aplicado nunca aquí**.
No es cosmética: un fichero de 85 KB es un fichero que nadie relee, y en este
árbol los comentarios son la documentación.
*Fix propuesto:* no partirlo de golpe. Medir primero cuántos asuntos lleva
dentro cada uno, y cortar por el más evidente —probablemente los seis cajones—
antes de fijar ningún número.

### 4 · El catálogo de compañeros habla una sola lengua · **M**
`hub.json` lleva **un `name` y una `function` por agente**, sin variantes: «El
Instalador» sale igual en la portada alemana, la rusa y la griega. Con la
función ahora pintada en la ficha del modelo —donde antes vivía escondida en un
`title`— esto se ve mucho más que ayer.
*Fix propuesto:* es **decisión de contenido, no técnica**: puede que sean
nombres propios y no deban traducirse. Si se traducen, el sitio natural es
`hub-textos.json`, que ya está partido por lengua.

### 5 · `medidas.json` no tiene el campo del que depende · **S**
La marca «sin firmar» se pinta ahora si `d.firma` no existe. Hoy nunca existe,
así que la marca sale **por ausencia y no por medida**. Y los cuatro NO_DATA
con su `que` y su `causa` viven en ese fichero y **no se pintan en ningún
sitio**: estructura real sin uso.
*Fix propuesto:* que el enjambre local escriba `firma` al volcar la media
horaria. Y decidir sobre los cuatro huecos: o se pintan en alguna parte, o se
retiran del fichero.

---

*Gate al escribir esto: web `test_web.py` 76/76 · `arnes_sw.mjs` 21/21 · app
`bin/pruebas` 617/617.*
