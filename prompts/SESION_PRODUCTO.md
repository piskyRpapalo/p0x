# Prompt · sesión para seguir con la web y la app

**Claude Code.** Necesita los gates, el navegador del arnés y el servidor
local.

---

Copia de aquí abajo:

---

Sigues el trabajo de `preceptoros.org` (repo `~/preceptoros-web`, rama `main`,
**empujar es desplegar**) y de la app (`~/p0x/preceptor`, repo `PreceptorOS`).

**Lee primero, en este orden:** `~/p0x/HANDOFF.md`, `~/p0x/INVENTARIO.md` —
que tiene cada parte de los dos productos, sección por sección— y
`~/preceptoros-web/docs/ESTADO.md`. **No repitas trabajo que ya está ahí.** El
cabecero, la esfera, el marco, la placa, el teclado y los README se rehicieron
el 2026-09-05 y están firmados.

## Las reglas que no se negocian

- **16 KiB por fichero** en la web. Al pasarse **se parte por asunto; jamás se
  recorta un comentario** — en este árbol los comentarios son la documentación,
  y quitarlos para salvar un número paga el tope con lo único que no se puede
  volver a deducir del código.
- **Se mide, no se supone.** Todo color lleva su contraste escrito al lado;
  toda cifra, su fecha. Un color medido contra un fondo no vale contra el
  contrario.
- **Un hueco se llama hueco**, con su causa. Nunca un dato viejo con cara de
  fresco.
- **Nada se da por hecho sin verlo en pantalla.** El navegador del arnés y un
  **puerto nuevo** por tanda: `python3 -m http.server <puerto> --directory public`.
  El caché sirve CSS viejo y ya costó media hora.
- Gate al cerrar: `python3 test_web.py`, `node arnes_sw.mjs` y `bin/pruebas`.

## Lo que hay que hacer, por orden

1. **Los cinco arreglos propuestos** están en `INVENTARIO.md`, parte 3, con su
   coste. Tres ya se hicieron el 2026-09-05 (los guiones huérfanos y el
   onboarding); quedan:
   - **La app no tiene tope por fichero.** `dashboard.css` pesa 83 KB y
     `dashboard.js` 85 KB: cada uno cinco veces el tope entero de la web. **No
     lo partas de golpe.** Mide primero cuántos asuntos lleva cada uno dentro y
     corta por el más evidente —probablemente los seis cajones— antes de fijar
     ningún número. Este es el trabajo grande y el que más vale.
   - **`medidas.json` no tiene campo `firma`**, del que ahora depende su propia
     marca «sin firmar»: sale por ausencia y no por medida. Y sus cuatro
     NO_DATA con su causa no se pintan en ningún sitio.
   - **`hub.json` habla una sola lengua** — un nombre y una función por agente
     para las ocho portadas. Es **decisión de contenido**: pregúntame antes de
     traducir nada, puede que sean nombres propios.
2. **Una captura con el teclado abierto en un teléfono real.** Lo que hay está
   medido forzando `--alto-visible` en el navegador, no en metal.
3. **Ruso y griego** siguen sin revisión nativa. Si toco copia de producto en
   esas dos lenguas, dímelo en vez de inventarla.

## Cómo se cierra

Reporte con qué se hizo, qué dato salió y qué falló. Actualiza
`~/p0x/HANDOFF.md` y el bloque `IMPORTANTE` del Ojo
(`~/p0x/Alejandria/ojo/arranque.json`) con la fecha. Y de tres a seis
sugerencias accionables con coste S/M/L.

## Las siete trampas que ya mordieron

Están todas en `HANDOFF.md`. La que vale por todas: **un guardián puede estar
en verde protegiendo el fallo** — el del onboarding exigía literalmente las dos
URL que daban 404. Si un test te bloquea, mira si lo que exige sigue siendo
verdad antes de darle la razón.
