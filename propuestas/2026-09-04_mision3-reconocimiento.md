# Misión 3 · reconocimiento en metal antes de construir nada

**Estado:** RECONOCIMIENTO HECHO, plan propuesto. Nada construido todavía.
Autorizada por el Soberano el 2026-09-04 («iniciar la Misión 3 una vez los
límites de peso estén resueltos por el local»).

## El hallazgo que cambia la misión

El glosario del Ojo describe la Misión 3 como **«LO QUE FALTA»**: sacar El
Camino y La Brújula a la interfaz, hacer la pestaña de Perfil Local y las
herramientas de visión de LoRAs. Medido hoy contra el MVP vivo en `:8740`,
**los tres puntos ya están construidos y funcionando**. La entrada del glosario
describe el plan de hace dos días, no el disco de hoy.

| lo que el glosario da por pendiente | lo que hay, medido el 2026-09-04 |
|---|---|
| 1 · El Camino y La Brújula en `app.html` y `dashboard.html` | **VIVO.** Las dos páginas cargan `compass.js?v=39` y `compass.css?v=39`. `GET /api/camino` → 200 con los ocho peldaños (M0–M2 núcleo, M3–M7 opcionales) y sus estados; `?modo=camino` y `?modo=detalle` → 200 los dos; `/assets/compass.svg` → 200. **Visto en pantalla:** la rosa de ocho segmentos pintada, con la aguja, los peldaños coloreados por estado y el rango BRONCE debajo |
| 2 · Pestaña «Perfil Local»: clave pública y elección entre los 8 bustos | **VIVO.** `#cajon-perfil` con «Tu huella soberana» (`212b d4ba 23e1 847d`) y su nota, «Tu cara» con **16 botones** de avatar en dos familias (8 bustos + 8 ojos). Las 16 imágenes cargan: 200 y bytes reales, de 6.152 a 23.844 B |
| 3 · Elegir un LoRA y ver sus métricas con `metricas.py` | **VIVO.** `#cajon-medicion` con `#med-modelo`, `#med-tabla`, `#med-norma` y el selector de cerebro `#cer-opciones`. `GET /api/metricas` → 200 |
| 4 · PROHIBIDO rutear a la web desde la app | **SE CUMPLE.** `app.html` y `dashboard.html` sólo enlazan rutas locales |

Conclusión: la Misión 3 **no es una misión de construcción**. Es una de
verificación y pulido, y es mucho más barata de lo que su ficha promete.

## Lo que sí faltaba, y ya está arreglado

Buscando el trabajo pendiente apareció un defecto real en esa misma superficie,
corregido hoy en `a6719ef`: desde `cajon-camino`, **tres cajones llevaban la
clave i18n del cajón anterior** (`camino`←`la_frontera`, `perfil`←`el_camino`,
`proyectos`←`perfil`). No se veía porque `dashboard.js` escribe esos títulos dos
veces y el segundo bucle los pisaba con el correcto. Un fallo enmascarado por
una redundancia no está arreglado: está esperando a que alguien retire la
redundancia por parecer redundante.

## Lo que propongo como Misión 3 de verdad

En orden de valor por esfuerzo. **Nada de esto está hecho ni empezado.**

1. **Cerrar el hueco de idioma que el arreglo destapó** (coste S). Los rótulos
   ahora apuntan a `el_camino`, `perfil` y `proyectos`. Falta comprobar que las
   tres claves existen en los **tres** idiomas y que `test_idioma.py` las cubre;
   si alguna falta, el título saldrá vacío en ese idioma en vez de mal, que es
   distinto pero tampoco es bueno.
2. **Probar la superficie en el Doogee** (coste S). Todo lo de arriba está visto
   en un navegador de escritorio. La app promete teléfono: `visualViewport` está
   cableado (`dashboard.js:934`, `dashboard.css:58`) pero **no se ha visto con
   un teclado Android abierto**. Es medida, no construcción, y el aparato está
   enchufado.
3. **`no_medible` no debe leerse como cero** (coste M). `M1 · El Fuego` sale hoy
   con estado `no_medible`, y la doctrina de la Brújula dice que ese valor
   «viaja marcado» para que nadie lo lea como «no ha hecho nada». Falta
   comprobar que la rosa lo DIBUJA distinto de `sin_empezar`. Si los dos
   segmentos se ven igual, la distinción existe en el JSON y no en la pantalla,
   que es donde importa.
4. **Decidir qué hace el rango** (coste M, y es decisión del Soberano, no mía).
   La rosa anuncia «BRONCE» y el glosario tiene una entrada `Bronze · Silver ·
   Gold`. Qué sube de rango, y si eso desbloquea algo, es mecánica pedagógica —
   fuera del alcance de una sesión de silicio, y del cerebro local con más razón.

## Cómo se comprueba todo lo de arriba

    ~/p0x/preceptor/bin/preceptoros-servicio estado     # vivo · responde 200
    curl -s 'http://127.0.0.1:8740/api/camino?modo=detalle' | head -c 300
    curl -s -o /dev/null -w '%{http_code}\n' http://127.0.0.1:8740/api/metricas
    cd ~/p0x/preceptor && bin/pruebas                   # exigido: VERDE 590/590

Y una trampa medida hoy: el servidor del MVP **no implementa `HEAD`** —
devuelve `501 Not Implemented`. Comprobar un asset con `fetch(u,{method:'HEAD'})`
da 501 en los dieciséis avatares y parece que están todos rotos. Con `GET` los
dieciséis dan 200. Medir con el método equivocado fabrica una avería que no
existe.
