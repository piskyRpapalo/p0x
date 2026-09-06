# Propuesta · la app: idiomas y tres cambios · 2026-09-07

**Propose-only.** Nada de esto se ha aplicado. `preceptor` es otro repo y no se
toca sin firma. Todo lo que sigue está medido hoy, no recordado.

---

## A · Los idiomas, con el número delante

**La app habla 2 lenguas. La web habla 8.** Quien llega en portugués desde
`preceptoros.org`, instala y abre la app, se la encuentra en español.

Y no hay un catálogo de textos, hay **tres**, cada uno con su mecanismo:

| dónde | qué es | lenguas | traducible |
|---|---|---|---|
| `textos.py` | el CLI, ~110 claves | es, en | sí |
| `interface/app.js` | la pantalla de hablar | es, en | sí, `data-i18n` |
| `interface/dashboard.js` | **la pantalla principal**, 1.792 líneas | — | **no**: `dashboard.html` tiene CERO `data-i18n` |

La pantalla que más se ve es la única que no se puede traducir.

### El cuello de botella no es traducir, es una línea

`interface/app.js` termina de fijar el idioma así:

```js
document.documentElement.lang = t === textos.en ? "en" : "es";
```

Eso no es una búsqueda en un diccionario: es un **binario**. No expresa una
tercera lengua aunque le añadas los textos. Mientras esa línea siga ahí,
traducir es tirar el trabajo.

### Lo que propongo, y el orden importa

**Primero la forma, después las traducciones.** Si se meten seis lenguas en
`textos.py` tal como está, ese fichero pasa de 22 KB a ~90 KB — y la web ya
pagó exactamente esa factura: `hub-textos.json`, `instalar.json` y
`taller-<lengua>.json` existen porque *«juntar las ocho lenguas en un fichero lo
deja lleno el primer día, y en griego y ruso cada carácter cuesta el doble»*.
Repetir el error sabiendo que está documentado sería peor que cometerlo.

1. **(M) Un fichero por lengua**, como la web: `textos/<lengua>.json`, cargado
   con `json` de la biblioteca estándar — el MVP no gana dependencias. El
   `test_idioma.py` ya es de caja negra, así que sigue valiendo sin tocarlo, y
   su caso 10 —*«una traducción que falta es una clave que falta»*— pasa a
   cubrir ocho columnas en vez de dos.
2. **(S) Matar el binario** de `app.js`: `documentElement.lang = idioma`, y el
   diccionario elegido por clave.
3. **(M) Poner `data-i18n` en `dashboard.html`.** Es el trabajo real y no se
   puede saltar: sin esto, la app «traducida» sigue enseñando su pantalla
   principal en español.
4. **(L) Las seis traducciones**, y sólo entonces.

### Dos decisiones que son tuyas, no mías

- **¿Qué lenguas?** Lo coherente es las ocho de la web. Pero cada lengua nueva
  es mantenimiento para siempre, y el ruso y el griego **ya arrastran una deuda
  declarada**: ninguna sesión ha podido revisarlos con oído nativo. Añadirlos a
  la app duplica esa deuda. Yo empezaría por **pt, fr, it** —lenguas que alguien
  del entorno puede leer— y dejaría de, el, ru atados a que aparezca revisor.
- **¿Se traduce el lore?** `textos.py` dice que *«los nombres clave del lore se
  mantienen bilingües como marca»* y que el juego se narra en español por firma
  del 2026-08-19. Un nombre propio de juego traducido a ocho lenguas deja de ser
  una marca. Propongo: **la interfaz se traduce, los nombres del lore no.**

---

## B · Tres cambios que la doctrina de hoy pide

### 1 · (M) La app no sabe leer lo que la web le da

Hoy he abierto en la web la puerta de salida del aporte: arma un paquete en el
aparato, lo enseña y lo deja copiar. Y `corregir.js` ya usa **el esquema de
`preceptor/captura.py`** — la tabla `turnos`, campo a campo, a propósito, para
que no haga falta un traductor en medio.

**Pero el puente sólo va en un sentido: la app no tiene importador.** El
cuestionario y las correcciones que alguien hace en la web se quedan en el
navegador salvo que la persona se los lleve, y al llegar a la app no hay dónde
meterlos. Es el hueco que el propio LORAtelier describió y nadie ha cerrado.

Propuesta: un `importar.py` que trague ese JSON y lo escriba en `memory.db` con
sus huecos declarados, sin inventar ninguno. Es la pieza que convierte «probé la
web» en «tengo mi memoria», y hoy no existe.

### 2 · (S) El medidor produce, pero no en el formato que la web publica

`metricas.py` mide, y `medidas.json` de la web declara **cuatro huecos**: media
por hora, sha256, TTFT y firma. Los dos hablan de lo mismo y no se entienden.

Propuesta: que el medidor de la app emita exactamente el esquema que
`medidas.json` declara en su `contrato`. Coste bajo, y convierte cada tester en
una fila real el día que el tablón abra. Sin esto, «mide tu equipo y guarda el
resultado» produce un fichero que no encaja en ningún sitio.

### 3 · (S) El escudo de salida no vigila la cifra inventada

Esta madrugada los LoRA de La Charla se inventaron que *«el modelo base ocupa
unos 200 gigas»* —son 4,4— y un equipo de desarrollo al que enviar el feedback.
La app corre modelos locales con la misma familia de riesgo, y `frontera.py`
filtra a la salida.

Propuesta: que el guardia mire también **cantidades con unidad** (`N GB`, `N
tok/s`, `N días`) y las contraste con lo que la app sí sabe de la máquina. Lo
que no pueda contrastar, que lo marque en vez de dejarlo pasar. No es censura:
es la misma regla de `NO_DATA` aplicada a los números, que es por donde se
escapó hoy.

---

## C · Lo que ya está y creíamos que no

**Hay release publicada: `v1.3`, del 2026-08-31**, con `install.sh`,
`install.ps1` e `INSTALACION_ANDROID.md`. La web afirmaba que no había ninguna
—y anoche apagué el botón por creerlo— cuando la afirmación llevaba una semana
siendo falsa. Ya está corregido en `preceptoros-web`: el enlace vuelve, y el
texto dice qué hay detrás (instaladores, no un programa empaquetado).

**Lo que sigue faltando para una «versión limpia» de verdad** es un artefacto
descargable con su hash publicado al lado, que es la regla de esta casa. Hoy se
instala desde el código. Eso no es un fallo —es honesto— pero conviene no
llamarlo «descargar la app».

---

## D · Lo que NO propongo, y por qué

- **No tocar el lore ni la mecánica de misiones.** Es decisión pedagógica y no
  me corresponde.
- **No añadir dependencias.** El MVP es biblioteca estándar y esa restricción es
  la mitad de su promesa.
- **No empaquetar un binario todavía.** Sin firma ni hash publicado sería un
  botón de descarga sin artefacto firmado, que es exactamente lo que hoy hemos
  quitado de la web.
