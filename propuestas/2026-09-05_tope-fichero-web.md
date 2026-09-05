# Enmienda propuesta · el tope por fichero de la web

**Documento destino:** `mente/doctrina/METRICAS_NORMA.md`
**Estado:** propuesta. `editor_autorizado: carbono` — solo el Soberano canoniza.
**Propone:** sesión de frontera, 2026-09-05, con medición.
**Aplicado ya en código:** sí, commit `35bd29b` en `preceptoros-web` (gate 76/76).
El código y la doctrina van desacoplados a propósito: el gate ya protege el
número, y esta enmienda es para que el número tenga dueño doctrinal.

---

## Texto propuesto para añadir a la Norma de Métricas

> ### El tope por fichero de la web · 16 KiB
>
> Ninguna pieza servida por `preceptoros-web` —`.html`, `.css`, `.js`, `.json`,
> `.webmanifest`— pasa de **16.384 B en disco**. La cifra es pública: se anuncia
> en las tres portadas y en el README, así que cambiarla es cambiar una promesa
> y se cambia en los cinco sitios a la vez.
>
> **De dónde sale, porque una cifra publicada tiene que ser reproducible.** Un
> fichero debe llegar en un solo viaje de red. La ventana inicial de congestión
> son ~14 KB en el cable; se reparte y se le da a un fichero la mitad —varios se
> piden en paralelo y comparten ese primer vuelo—: 7 KB. Estos ficheros
> comprimen 2,43x medido, así que 7 KB de cable son 17,4 KB de disco, que se
> redondean a la baja al binario limpio.
>
> **Cómo se comprueba:** `test_cada_fichero_bajo_el_tope` mide el disco y
> `test_ningun_fichero_gasta_medio_viaje_de_red` comprime y mide el cable. El
> segundo existe porque el primero es un proxy: el ratio de 2,43x es una media,
> y deja de valer en cuanto entra algo que comprime mal.
>
> **Cuándo se reedita:** cuando un fichero pase de 7 KB comprimido, o cuando la
> carga inicial de la portada pase de 200 KB en disco (hoy son 161,5 KB en 26
> ficheros). Cualquiera de las dos obliga a volver a esta cuenta, no a subir el
> número.

---

## Los datos, para que la enmienda se pueda auditar

| medida | valor | cómo |
|---|---|---|
| ficheros vigilados | 77 | `find public -type f` por sufijo |
| peso en disco | 458.360 B | `stat` |
| peso comprimido | 188.656 B | `gzip -9` |
| ratio medio | **2,43x** | disco / comprimido |
| prosa por fichero | **43 %** | comentarios / total, sobre los 10 mayores |
| carga inicial de la portada | 161,5 KB · 26 ficheros | portada + sus css + sus js |
| el que más gasta hoy | `sw.js` · 4.516 B comprimidos | 63 % de su reparto de 7 KB |
| mayor fichero en disco | 10.237 B | margen de 6.147 B con el tope nuevo |

## Por qué se propone, en una frase

El tope de 10 KB no acotaba la red —gastaba menos de un tercio del primer
viaje—: acotaba cuánto se puede razonar por escrito, y con el 43 % del fichero
en prosa eso dejaba ~5.850 B de código. La consecuencia se vio el mismo día:
seis rondas limando comentarios propios para volver bajo el tope, que es lo
contrario de «se parte, no se recorta».

## Qué desbloquea para el futuro

`sw.js` gana 6,1 KB — a ~22 B por línea de precache, sitio para ~270 ficheros
más. Hasta hoy, partir un fichero por asunto costaba una ranura de precache que
no había: un `capas.css` se escribió y se deshizo el mismo día porque su
etiqueta dejaba `sw.js` en 10.244 B. **A partir de aquí se puede separar sin
negociar con el tope**, que es la condición para cualquier refactorización seria
de `hub.js`, `chat-panel.js` y las hojas del cabezal.
