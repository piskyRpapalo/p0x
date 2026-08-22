# Informe del Preceptor · 2026-08-22, segunda tanda

**El bug que priorizaste está resuelto en las dos plataformas, y probado en el
metal.** Todo lo de abajo está medido; donde no pude medir, lo digo.

`bin/pruebas`: **VERDE 278/278 · 17 suites**.

---

## §1 · El bug · «cerré Aurelius y no sé cómo volver»

| Plataforma | Antes | Ahora |
|---|---|---|
| **Android** | ningún icono; había que recordar el comando | `bin/crear-acceso-directo-android` escribe un atajo que **arranca el servidor y abre el navegador de una vez** |
| **PC** | `bin/instalar-pc` era un 404 | existe; crea el icono del menú y explica por dónde volver |
| **Ambas** | nada documentado | sección *«¿Cerraste todo y no sabes volver?»* en los cuatro documentos |

**Probado en el Doogee**, no descrito: ejecuté el atajo, el servidor arrancó y
el tablero se abrió solo. **Probado en este Ubuntu**: `desktop-file-validate` da
el `.desktop` por válido, el lanzador levanta el servidor (HTTP 200), y
`--desinstalar` quita el icono **dejando la memoria intacta** — comprobado
mirando el fichero después.

Dos detalles que salieron de sufrirlo yo:

- **`pkill -f aurelius-pwa` no caza al ejecutable empaquetado**, que se llama
  `dist/aurelius`. Me mordió cuatro veces: el proceso viejo seguía respondiendo,
  el nuevo moría al nacer, y todo parecía funcionar mientras se medía la versión
  equivocada. Está escrito en los cuatro documentos.
- **El `.desktop` no lanza el navegador directamente.** Un `.desktop` no espera;
  abriría el navegador antes de que el servidor respondiera, y la primera
  impresión del producto sería una página de error.

## §2 · Frentes cerrados

| # | Frente | Estado |
|---|---|---|
| 1 | `INSTALL_PC.md` | hecho · 119 líneas |
| 2 | `INSTALL_ANDROID.md` | hecho · 139 líneas, con la sección de reapertura en los dos idiomas |
| 3 | `CONTRIBUTING.md` | hecho · **con una corrección**, ver §4 |
| 4 | `CHANGELOG.md` | hecho · v1.0.0 con las cifras medidas |
| 5 | Topics de GitHub | **bloqueado**, ver §5 |
| 6 | `MANIFIESTO.md` | hecho · CC BY-SA 4.0 |
| 7 | `assets/tablero-en.png` | hecho · **y destapó un fallo**, ver §3 |
| 8 | Acceso directo Android | **construido y probado**, no solo propuesto |
| 9 | `bin/instalar-pc` | **construido y probado** |
| 10 | Documentar la reapertura | hecho · cuatro documentos |

## §3 · El hallazgo de la noche · la cara hablaba un solo idioma

Salió buscando la captura en inglés que pediste. El endpoint devolvía
`idioma: "en"` y **el tablero seguía en castellano**: `dashboard.js` tenía las
cadenas incrustadas, y las etiquetas del marco estaban escritas en el HTML.

Un producto que promete dos idiomas y traduce la mitad **se nota más** que uno
que no traduce. Arreglado con dos columnas, como en `textos.py`, y ahora la cara
habla el idioma que declara tu memoria. El README enseña las dos capturas y el
pie dice exactamente eso.

De paso, **el service worker volvió a servir la copia vieja** — segunda vez. La
regla ya estaba escrita en el propio fichero («al tocar el armazón, se sube el
número») y esta vez la seguí: caché v3.

## §4 · Correcciones a lo que me pasaste

**`bin/pruebas sabotaje` no existe.** Los sabotajes van en la tanda por defecto;
lo que los salta es `--rapido`. `CONTRIBUTING.md` documenta el CLI real.

**El icono del navegador no resuelve el bug.** «Añadir a pantalla de inicio» da
un icono de verdad, pero **no arranca el servidor**: si no está corriendo, el
icono abre una página que no carga. Por eso el atajo de Termux:Widget existe, y
por eso los documentos explican las dos formas y qué mitad resuelve cada una.

**Termux:Widget NO está instalado en el Doogee.** Medido. El guion lo comprueba
**por el paquete y no por la carpeta** — la carpeta la crea cualquiera, y
entonces el icono se crea y no aparece nunca, que es el peor resultado porque
parece que funcionó.

## §5 · Bloqueos

**Frente 5 · los topics de GitHub.** No puedo: los conectores de GitHub de esta
sesión necesitan autorización OAuth y esta sesión no es interactiva. Los añades
tú desde la web del repo (⚙ junto a *About*):

```
local-first  privacy  offline-ai  sqlite  pwa  llm
python  memory  self-hosted  human-in-the-loop  edge-computing
```

**El CI sigue sin verificarse.** El fichero está escrito y su matriz sale de
`interprete.py`, pero la primera vez que se sepa si pasa será tras tu push.

**El teléfono tiene el atajo pero no el resto.** Le copié por `scp` lo que hacía
falta para probar. Tras tu push conviene `cd ~/aurelius && git pull` allí, para
que deje de tener ficheros sueltos que yo puse a mano.

## §6 · Commits sin empujar

| Hash | Mensaje |
|---|---|
| `62c159a` | restore: la simetría de --backup, y no era --import |
| `2dad26e` | release: el texto de v1.0.0 |
| `daaaa43` | reabrir: el bug que sufrió el autor, y la cara que hablaba un solo idioma |
| `64a0f8f` | instalar-pc: el icono, y saber volver |

*(Los dos primeros ya estaban de la tanda anterior si no llegaste a empujarlos.)*

## §7 · Recomendaciones

1. **Empuja, y luego `git pull` en el Doogee.** Es lo que deja el teléfono
   limpio y le da el arreglo del service worker.
2. **Instala Termux:Widget** en el Doogee y toca el icono una vez. Es el único
   paso que queda para que el bug esté cerrado de punta a punta para tu madre.
3. **Los topics**, que son dos minutos y mejoran mucho quién encuentra el repo.
4. **Y una decisión que sigue abierta desde ayer:** qué significa `--import`.
   Importar texto ya redactado, o no tenerlo. Las dos son defendibles; la mala
   es tenerlo sin decir que pierde.

---

*El silicio paró donde debía. El carbono decide lo siguiente.*
