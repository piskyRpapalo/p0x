# Traspaso · sesión del 2026-09-04

Para la sesión que venga detrás. Lee esto entero antes de tocar nada, y después
lee **el Ojo del Soberano** (abajo, sección «dónde inspirarse»).

**Estado de los gates al cerrar:** `bin/pruebas` → **VERDE · 594/594** ·
`test_web.py` → **74/74**. Los dos verdes y estables.

---

## Lo primero: cinco cosas de la lista de pendientes ya están hechas

El encargo de cierre las daba por pendientes. No lo están, y arrancar a
rehacerlas sería trabajo perdido:

| se creía pendiente | estado real | commit |
|---|---|---|
| Web · trasplante de estilo, oscuro por defecto | **hecho** | `b1a7287` |
| Web · `manifiesto.html` como novena página | **hecho**, con el techo a 9 firmado | `351ae47` |
| Web · sitemap por-idioma | **hecho** | `fd4b122` |
| App · barra del explorador, `dvh` / safe-areas | **hecho** | `68ba96f` |
| App · centrar la cara de la presentación | **hecho**, con criterio firmado | `20dbf1e` |

Lo que sí queda está en «Lo que falta», más abajo.

---

## Lo hecho en esta sesión

### El fallo que más importaba: un `NO_DATA` inventado

El panel decía **«no hay ningún modelo cargado (ollama ps vacío)»** mientras un
`llama-server` con **7,6 GB residentes** llevaba siete horas y media
contestando. Una ausencia inventada es peor que una cifra mal puesta: un
`NO_DATA` con su causa escrita *parece* rigor, y nadie lo mira dos veces.

La causa era una sola autoridad — el MVP no sirve por Ollama. Ahora se pregunta
a las dos. Y al arreglarlo se destapó otro que nadie había visto porque hacía
falta que el runner fuese pequeño: se elegía «el mayor proceso residente» de
toda la máquina, y en un escritorio eso es el navegador. Ahora se elige **por
nombre**, con suelo de 512 MiB. `17cc26d`

### Los otros cuatro fallos que ninguna prueba veía

1. **El tema, a medias en el teléfono.** Seis variables —el fondo entre ellas—
   estaban en el bloque de `prefers-color-scheme` y no en el de `[data-tema]`.
   En el escritorio no se veía porque allí el sistema ya pedía oscuro. Hay
   prueba nueva que compara los dos bloques.
2. **`pintarEstado` tenía una segunda coerción de idioma** igual a la que ya se
   había corregido en `cargarPerfil`, y corre en cada pulso: pisaba a la otra.
   Se elegía portugués, se guardaba bien, y volvía a castellano sin que nada lo
   dijera.
3. **`elige_idioma` se usaba y nunca llegó al diccionario.** La pantalla salió
   con las cajas y sin título. La prueba de simetría no lo caza: compara los
   idiomas entre ellos, y los tres carecían de ella por igual. **Prueba nueva**:
   toda clave usada debe estar declarada.
4. **Los cajones dependían de `requestAnimationFrame`.** Con la pestaña en
   segundo plano el navegador no dispara ninguno: el cajón quedaba presente y
   sin transformar, comiéndose los toques de lo que hay debajo.

Y una quinta, ajena al idioma: **`test_idioma.py` caso 0 tenía la misma cicatriz
que `test_cara.py`** y nadie la había arreglado ahí — fotografiaba el directorio
entero de la memoria. Acotado igual: `memory.db` y su `-wal`, fuera el `-shm`,
que lo tocan los lectores. `6b57f84`

### La cara

- **Las cinco láminas de `pensamiento`**, encuadradas contra reposo con una sola
  transformación. Venían como placas de croma —la familia que ya vació una
  cara— así que se midió el resultado: 3.072 a 4.506 píxeles con color cada
  una. Ninguna vacía. `753e098`
- **Pensar y hablar dejan de ser lo mismo**: antes la boca se movía mientras el
  modelo generaba, durante minutos, sin haber dicho nada.
- **La tira de tres** y luego el **reposo en violeta fijo**: el fotograma verde
  tenía 91 píxeles con color frente a 1.005–2.674 de los otros — el croma se
  llevó su brillo. `a95845c`
- **El encuadre del telón**, con el criterio firmado: *el diámetro del círculo
  pasa por los ojos, casi todo el pelo dentro, la peana un poco cortada.*

### Ajustes

Pantalla completa (**Capa 5**, que sí pisa la Capa 4), aspa, **tema como
interruptor** llamado «piel», **cuaderno como interruptor** que hoy decide si el
modelo recibe el harness o la pregunta viaja sola, los tres campos del harness
con límite razonado (500 caracteres: el 5 % de la ventana daría 2.185, pero se
manda entero en cada turno y los modelos pequeños reparten peor la atención), y
el Manifiesto servido **desde el disco** — sin enlace a la web, que el canon
prohíbe. `5197137` `eb692b9` `20dbf1e` `78cd930`

### Idiomas y tema

**Portugués completo en la app** —128 claves más los ocho peldaños del Camino en
`cara.py`, sin los cuales salía traducida menos el Camino— y **oscuro por
defecto**, puesto en el marcado para que no haya destello claro antes de que
corra el javascript. `5a55f1b`

### Web

- **`chat-router.js` partido**: estaba a **14 bytes** del techo. La costura se
  eligió por asunto, no por tamaño. Y produjo una regresión que se vio en el
  navegador: `listo()` se llama síncrono, así que el orden de carga quedó al
  revés del natural — primero el mueble, luego el rótulo. `47f54fb`
- **Los papeles del modelo fuera del marcado**: 2,4 KB de aire por portada.
  `fr/index.html` estaba a 36 bytes de su techo. `328cc1c`
- **La lista de idiomas se descubre del disco** y ya no se escribe en once
  sitios. Sin esto, una carpeta `pt/` habría contado como siete páginas de
  contenido y el techo habría saltado por una lista, no por crecer. `500c02a`
- **Trasplante de estilo**, **`manifiesto.html`**, **iconos separados** (eran el
  mismo fichero byte a byte, con la misma etiqueta) y **la frase solar
  unificada** en una sola clave. `b1a7287` `351ae47` `b72c846` `328cc1c`

---

## Lo que falta, en orden

### 1 · App · las herramientas, conectadas a la base

**Es lo más importante que queda.** Hoy el panel lateral ofrece cinco entradas
que abren cajones que ya existen —Medición, Camino, Memoria, Proyectos,
Frontera— pero **no hay herramientas conectadas a la base de datos**.

Lo que hay que construir y comprobar, en este orden:

1. Que crear el **primer recuerdo** sea sencillo para quien entra: hoy la
   memoria se llena sola con los turnos, pero no hay un gesto claro de «guarda
   esto».
2. Que después de ese primer recuerdo el **harness de herramientas funcione**:
   que el modelo pueda usar lo que hay en memoria y proyectos.
3. Comprobarlo en metal, no por lectura.

Ahí está la tesis del producto, dicha por el Soberano: **los LoRA se entrenan
para la forma de la base que la app crea** — leen sus títulos, y por eso un
modelo pequeño puede abarcar más. El interruptor «personalizada / sin
personalizar» existe para que esa diferencia se **note**, y hoy está construido
pero sin herramientas detrás que la hagan grande.

### 2 · App · rematar el linkeo

Repasar que nada quede huérfano: enlaces internos y herramientas. El panel
lateral y la rueda cubren los seis cajones (comprobado uno a uno), pero conviene
un barrido cuando entren las herramientas nuevas.

### 3 · Web · la carpeta `pt/`

Está **empezada y aparcada a propósito**. Se creó con la portada traducida y se
retiró el mismo día: **rompe 25 pruebas**. No es un fallo del gate — es que el
criterio de idiomas se descubre del disco, así que en cuanto existe la carpeta
todo lo que es por idioma reclama el suyo.

`preceptoros-web/traducciones/LEEME-pt.md` lleva **la lista exacta**, escrita por
las pruebas al caer y con el nombre del test que exige cada pieza. La portada ya
traducida está en `traducciones/pt-index.html.pendiente`.

**Y el hallazgo que vale para las cuatro lenguas siguientes:** la portada tiene
**dos bloques de traducción**, no uno. Traducir solo el que lleva `id="i18n"`
deja castellano dentro de la página portuguesa. **Unifícalos antes de traducir.**

### 4 · Web · los otros cuatro idiomas

Italiano, alemán, ruso y griego, después del portugués y con la misma lista.

---

## Dónde inspirarse

**La referencia visual del trasplante es el Ojo del Soberano**, la página local:

```bash
python3 ~/p0x/Alejandria/ojo/ojo.py --arranque
```

Vive en `~/p0x/Alejandria/ojo/` (`ojo.html`, `ojo.css`, `vivo.html`) y se sirve
en `:8790`. **Léela antes de tocar el estilo de la web.** El trasplante que ya
está hecho tomó de la app el mármol oscuro, los aros de bronce y el canto
dorado; el Ojo es de donde sale el resto del lenguaje.

---

## Cómo se trabaja aquí (lo que esta sesión aprendió a base de rojos)

- **La guardia de mayúsculas tumbó el gate seis veces**, siempre por palabras de
  énfasis en mis propios comentarios. En `interface/` no hay ninguna palabra de
  cuatro mayúsculas seguidas que no sea una política declarada. El énfasis se
  pone con la frase.
- **Al tocar `dashboard.html`, `.css` o `.js`, se sube el número de `sw.js`.** El
  Doogee devolvió la cara vieja una vez por no hacerlo. La marca `?v=` de las
  hojas no lo cubre: el que se sirve de la caché es el HTML, que no lleva marca.
- **Tamaño y paradas de una tira son el mismo número visto de dos formas.**
  Tocar uno sin el otro hace que la figura camine — y eso no se ve en una
  captura fija, se ve en la animación.
- **El css puede elegir qué trozo se ve, no dónde está dibujada la figura.**
  Cuando la ventana no llega, se mueve la lámina.
- **Medir antes de escribir, y medir el resultado.** Cada número de esta sesión
  —el 8 % de la cara, los 500 caracteres, los 12 píxeles del telón, el suelo de
  512 MiB— salió de una cuenta o de una medida, y las dos veces que discreparon
  mandó la pantalla.
- `preceptor/` **es repo propio**, dentro de `p0x`. Son tres repos, no uno.
