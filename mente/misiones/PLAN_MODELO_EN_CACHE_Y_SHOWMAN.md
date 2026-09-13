# El Modelo en Caché y el Showman

> **Estado: PROPUESTA · 2026-09-13.** El plan original que pidió el Soberano no
> apareció en el disco de este nodo — se buscó por nombre y por contenido y no
> está. Esto se escribe desde lo que el ecosistema **ya mide**, y espera su
> corrección. Lo que aquí lleve cifra, la lleva medida.

---

## I · El problema, en una viñeta

Hay un pueblo con un molino. El molino muele bien, muele barato y muele con sol.
Pero está en lo alto del cerro, y el camino hasta él **a veces no existe**.

Cuando el camino está, todo el pueblo tiene pan.

Cuando no está, el pueblo se queda mirando el cerro. Y lo peor no es quedarse sin
pan: es **no saber si el molino se ha parado o si es el camino el que falta**.

El molino es el rack. El camino es el túnel. Y la página, hoy, lo dice con estas
palabras suyas: *«el rack no contestó; el túnel público aún no está levantado»*.

Dice la verdad. Pero la dice **después**, cuando ya has escrito tu pregunta.

---

## II · Las dos piezas

### El Modelo en Caché · *el saco de harina de la despensa*

No es un molino de repuesto. Es **un saco de harina**: pequeño, ya molido, en tu
propia despensa. No hace pan fino y no pretende hacerlo. Hace **pan del día que
el camino no está**.

**Qué es, sin metáfora:** un modelo pequeño que vive en el navegador, cacheado
por el service worker, y que responde cuando el rack no contesta.

**Lo que resuelve, medido:**

| hoy | con el saco |
|---|---|
| el rack contesta → bien | igual de bien |
| el rack no contesta → `NO_DATA` y la pregunta se pierde | el saco contesta, **diciendo que es el saco** |

**La regla que no se negocia:** el saco **siempre dice que es el saco**. Nunca se
hace pasar por el molino. Una respuesta de caché etiquetada como si viniera del
rack sería exactamente la mentira que este proyecto existe para no decir — y
además rompería el Libro de Pruebas, donde cada cifra lleva su máquina dentro.

**Lo que NO es:**
- No descarga nada sin que lo pidas. La web es la puerta, no el taller.
- No sustituye a la app. El taller sigue abajo.
- No es «offline-first». Es **offline-honesto**: funciona sin camino y lo dice.

### El Showman · *el pregonero de la plaza*

En la plaza del pueblo hay un pregonero. No muele, no reparte, no decide. Su
oficio entero es **que la plaza sepa qué está pasando** — y en un pueblo que
presume de no esconder nada, ese oficio no es adorno: es la mitad del contrato.

**Qué es, sin metáfora:** la capa que enseña, en la propia página y antes de que
preguntes, **quién te va a contestar, desde dónde, y qué cuesta**.

**Lo que enseña, y todo de lo que ya se mide:**

| lo que dice | de dónde sale |
|---|---|
| quién contesta | `brain` · el modelo servido, con su tag explícito |
| desde dónde | rack · caché · navegador. Tres sitios, tres promesas distintas |
| a cuánto | `tok/s` del Libro de Pruebas, **con su carga base** |
| qué le falta | el `que_falla` de su ficha, con el mismo peso que el `que_hace` |

**Por qué «inteligente» y no un cartel:** porque cambia con el estado. Si el
camino está, dice el molino. Si no está, dice el saco **y por qué**. Si no hay
ninguno, dice `NO_DATA` con su causa, que es lo que ya hace — pero lo dirá
**antes de que escribas**, no después.

---

## III · Cómo encaja con lo de hoy

Esto no es un sistema nuevo: son dos piezas que se enchufan donde ya hay enchufe.

| pieza | se apoya en | ya existe |
|---|---|---|
| el saco en la despensa | `sw.js` · caché versionada con su huella | sí |
| decir de dónde viene | `paneles.json` · ficha por cerebro, con `que_falla` | sí |
| la cifra con su máquina | `ledger.jsonl` · 7 modelos firmados con su carga base | sí |
| que el cambio llegue | la huella del service worker atada a lo publicado | sí |
| que no mienta | el gate: una página no puede ofrecer algo y desmentirlo | sí |

**Y una pieza que falta:** la caché del modelo tiene su propio tope. `sw.js` está
a **64 bytes** de su límite de red y el sitio entero pesa 4,84 MB. Un modelo, por
pequeño que sea, no cabe en esa caché: necesita la suya, con su propio nombre y
su propia purga. Eso es trabajo, no un flag.

---

## IV · El orden, y por qué ése

1. **El pregonero primero.** No cuesta descarga, no cuesta caché, y arregla lo
   que hoy duele: enterarse *después* de escribir. Se apoya entero en datos que
   ya existen.
2. **El saco después.** Exige decidir qué modelo, cuánto pesa, y quién paga esa
   descarga. Son tres decisiones del Soberano, no tres líneas.

Al revés sería raro: tener harina en casa y no saber si hay camino.

---

## V · Lo que no se sabe

- **NO_DATA · qué modelo va en el saco.** Ni tamaño, ni nombre, ni si el
  navegador de un móvil de 8 GB lo aguanta. Sin medirlo en un aparato real —y el
  Doogee está por cable— cualquier cifra aquí sería inventada.
- **NO_DATA · cuánto tarda el primer token desde caché.** El Libro de Pruebas
  tiene `ttft_ms` en `NO_DATA` para los siete modelos porque no se midió. Esta
  pieza lo necesita, y es la primera medición que pide el plan.
- **NO_DATA · el plan original del Soberano.** No está en este disco. Si aparece,
  manda él y esto se recicla.

---

> *En el cerro sigue el molino, y sigue moliendo con sol.*
> *Abajo, en la despensa, hay un saco pequeño para los días sin camino.*
> *Y en la plaza, alguien que dice en voz alta cuál de los dos te está dando el pan.*
> *Eso es todo el plan. Lo demás es harina.*
