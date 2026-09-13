# Libro de optimizaciones · lo que el silicio vio y el carbono no tenía por qué ver

**Append-only.** Cada entrada es una mejora que se hizo **sin preguntar**, porque
preguntarla habría costado más atención de la que vale, y **todas se revierten con
un comando** que está escrito aquí al lado.

## Por qué existe

Orden del Soberano, 2026-09-13, y merece citarse entera porque define el contrato:

> *«debes suplir las mejoras básicas que yo no veo... si puedes enseñar algo al
> sistema desde tu posición, lo dejas registro localizable sin preguntar. hay
> demasiado de tu razonamiento que vale oro y no me da tiempo a leer... al final
> del trabajo me lo dices, y si no me gusta algo, revertimos.»*

Lo que hace falta para que eso no se convierta en un cheque en blanco son tres
cosas, y las tres son la estructura de este fichero:

1. **Localizable.** Un hallazgo que vive en un mensaje de chat se pierde en la
   siguiente sesión. Aquí no.
2. **Reversible una por una.** No «revertir la sesión»: revertir *esa* decisión,
   con su comando, sin tocar las demás.
3. **Con la lección separada del cambio.** El cambio caduca; la lección no. Por eso
   cada entrada dice *qué se aprendió* aparte de *qué se tocó* — y es esa parte la
   que alimenta al RAG y, más adelante, al LoRA.

## Cómo se revierte

Cada entrada trae su comando. El general, para una entrada con commit propio:

    cd ~/p0x && git revert --no-edit <sha>

Para una optimización que viaja dentro de un commit mayor, la entrada dice el
fichero y la línea exacta que hay que devolver.

---

## 2026-09-13 · Laboratorio

### L1 · El GC de LoRAs archivaba tres capacidades enteras
**Qué vi.** «Deja los 5 más recientes», por fecha pura, se llevaba
`reclamaciones_en`, `reclamaciones_multilang` y `cuentacuentos_mistral` —las
**únicas copias** de tres capacidades— para conservar `charla_base` v1, v2 y r2.
**La lección.** La recencia no es identidad. Un recolector que ordena por fecha
trata «otra versión de lo mismo» y «lo único que sabe hacer X» como equivalentes,
y siempre sacrifica lo raro, que es justo lo irreemplazable.
**Qué hice.** Reparto en dos pasos: primero se salva la más reciente de **cada
familia** (el nombre sin el sufijo `_v<n>`/`_r<n>`), y solo después se llenan
huecos por fecha. Si hay más familias que plazas, **aborta** y decide el carbono.
**Revertir.** `git revert --no-edit 10f88c5` (revierte turnos.py también), o
quitar `familia()` y `reparto()` de `hexelion/laboratorio/gc_loras.py` y volver a
`xs[:quedan], xs[quedan:]`.

### L2 · Una pasada en seco envenenaba el gate del 5%
**Qué vi.** El ciclo `--seco` se registraba en `laboratorio_runs` como `dataset`,
igual que uno real. La siguiente comparación de degradación se habría hecho contra
un ensayo.
**La lección.** Un ensayo que deja la misma huella que la función real deja de ser
un ensayo. Medir en seco es útil; que la medida *mande* no.
**Qué hice.** `evento='dataset_seco'` cuando es seco, y `ultimo_ciclo()` filtra por
`dataset`. La fila 16 de `loops.db`, mal etiquetada por mí, se reetiquetó diciéndolo.
**Revertir.** En `turnos.py`, volver a `aud.anota(espacio, "dataset", ...)`.

### L3 · El Guardián citaba pruebas que no existían
**Qué vi.** `granite3-dense:8b` rechazó la única fila buena del laboratorio diciendo
«contiene una instrucción de no seguir». No la contenía: la instrucción era **mía**,
del prompt, y el modelo la leyó como parte de lo juzgado.
**La lección.** A un modelo que acusa se le pide **prueba citable**, y la cita se
verifica contra el texto de forma determinista. Afinar el prompt hasta que acierte
es adivinar; exigir la cita es medir. Es el mismo criterio que la rúbrica aplica a
las cifras: sin procedencia, no cuenta.
**Revertir.** En `turnos3_guardian` de `turnos.py`, borrar el bloque que comprueba
`cita` contra el texto.

### L4 · El Guardián corre el primero, no el tercero
**Qué vi.** Un texto hostil cazado en tercer lugar ya ha gastado Bibliotecario y
Analista: unos 40 s de rack para acabar en la basura igual.
**La lección.** Una puerta que deja pasar y examina después no es una puerta.
**Revertir.** En `ciclo()` de `turnos.py`, devolver la llamada a `turno3_guardian`
detrás de `turno1_bibliotecario` y `turno2_analista`.

---

## 2026-09-13 · Web

### W1 · `corregir.js` estaba a 90 bytes de su techo
**Qué vi.** Tras dos arreglos, el fichero quedó en 16.294 B de 16.384. El siguiente
arreglo no habría cabido.
**La lección.** Un fichero al límite no admite ni una corrección, y la siguiente
corrección siempre llega. En esta casa se parte antes que recortar comentarios,
porque los comentarios son la documentación.
**Qué hice.** `bronce.js` se lleva el almacén de pares y la puerta de salida;
`corregir.js` baja a 13.571 B. Y el almacén pasa a tener **un solo dueño**, que es
como se evita que dos ficheros abran la misma base con su propia idea de la versión.
**Revertir.** `git -C ~/preceptoros-web revert --no-edit 3a9c3e8`.

### W2 · La guarda se quedó vigilando la puerta por la que ya no pasa nadie
**Qué vi.** Al mudar el almacén a `bronce.js`, el test de no-egreso siguió mirando
solo `corregir.js`. **Siguió verde sin guardar nada.**
**La lección.** Cuando el código se muda, la guarda se muda con él. Un test que pasa
sobre un fichero vacío de riesgo es peor que no tenerlo: da tranquilidad falsa.
**Qué hice.** El test recorre ahora los dos ficheros.
**Revertir.** En `test_web.py`, volver al bucle sobre un solo fichero.

### W3 · El `origen` no decía de qué página venía
**Qué vi.** `origen: 'preceptoros.org'` a secas. Con dos páginas produciendo pares
—portada y LoRAtelier— eso ya no identifica nada.
**La lección.** Dos poblaciones distintas en la misma columna no son una media: son
dos cosas mezcladas, y contaminan las dos. Es el mismo motivo por el que existe
`arnes`.
**Revertir.** En `corregir.js`, quitar `+ location.pathname`.

### W4 · Desplegar no era publicar — y no avisaba nadie
**Qué vi.** Tres ficheros nuevos llegaron al servidor (`curl` los traía con sus
bytes exactos, 200) y **la página ejecutaba los viejos**: el service worker servía
un shell cacheado días antes, con su `VERSION` sin tocar. Al Doogee le pasaba lo
mismo y yo lo había diagnosticado como «un botón sin rótulo».
**La lección, y es la más cara de la sesión.** Desde el navegador, un shell viejo se
ve **idéntico** a un fallo de estilos. Por eso hace falta un test y no buenos ojos.
Y la consecuencia es la peor de su especie: el cambio llega a quien entra por
primera vez y **no** llega a quien ya conocía el sitio, o sea a los testers.
**Qué hice.** `config/sw-huella.txt` guarda el sha256 de todo `public/` menos
`sw.js` junto a la versión que le corresponde. Si cambia un byte y la versión no,
el gate se pone rojo y **dice la huella nueva para pegarla**.
**Revertir.** `git -C ~/preceptoros-web revert --no-edit fbd6cab`.

---

## 2026-09-13 · Búnker

### B1 · El espejo estaba escrito a mano y habría vuelto a invertirse
**Qué vi.** El comentario decía «el sprite base mira a la derecha» —cierto de la
hoja vieja—. La hoja nueva declara `mirada_base: "izquierda"`.
**La lección.** Un hecho del *dato* escrito como constante en el *código* es una
bomba de relojería con la fecha puesta en el siguiente cambio de dato. Ese fallo
concreto ya había costado dos correcciones en pantalla.
**Revertir.** En `bunker.js`, volver a `sp.style.transform = sentido < 0 ? "scaleX(-1)" : ""`.

### B2 · Los rótulos se pisaban
**Qué vi.** Dos habitantes arrancaban a un cuarto de sala; los nombres, al doble de
tamaño desde que se pidió, miden más que eso. Se leía «AFINADOR:REBRO».
**La lección.** Cambiar el tamaño de una etiqueta cambia la geometría de lo que la
rodea, y eso no se ve en el código: se ve en pantalla. **Mirar la captura no es
opcional.**
**Revertir.** En `bunker.js`, quitar `carrilA()` y volver a las dos cuentas separadas.

---

## 2026-09-13 · Repositorio

### W5 · Un comentario dentro del objeto firmado rompía la app
**Qué vi.** El gate del MVP acusó a la web de escribir un campo llamado *«boton
vive tambien en el Benchmark eso ya no identifica nada»*. No era un campo: era un
comentario mío, en bloque, **dentro** del objeto literal que se firma.
**La lección.** Un objeto que otro programa parsea no es solo código: es una
**interfaz**, y dentro de una interfaz los comentarios no son gratis. El contrato
entre web y app se lee con un parser ingenuo, y eso hay que saberlo antes de
escribir dentro.
**Revertir.** `git -C ~/preceptoros-web revert --no-edit a042cc6`.

### A1 · El guardián acusaba al sitio que no era
**Qué vi.** El parser de `test_importar.py` parte líneas por `:` y solo salta las
que empiezan por `//`. Un bloque `/* */` entra como si fuera un campo.
**La lección.** Un guardián que se equivoca de culpable es **peor que uno
ausente**: manda a arreglar el sitio que no era, y cuesta un rato entender que el
acusado es el parser. Que un test esté rojo no prueba dónde está el fallo.
**Revertir.** `cd ~/p0x/preceptor && git revert --no-edit c1f85d6`.

### C1 · Me equivoqué con el curador, y queda escrito
**Qué vi.** `systemctl list-timers` daba `LAST 2026-09-06` para `curador.timer`, y
lo tomé por un bucle muerto hace una semana.
**La lección.** Era falso: su ventana es de 604.800 s — es un bucle **semanal**, y
última 2026-09-06 + siete días = hoy. Leí un `LAST` viejo sin mirar la ventana. Un
«lleva una semana sin correr» no significa nada hasta saber cada cuánto debía
correr. **Lo que sí quedó medido**, y es real: el 55% de las salidas del curador
son frenadas por carga, y esa carga la provocaron mis propias tandas de 27B/30B.
El observador altera lo observado.
**Revertir.** Nada que revertir: no se tocó código. La entrada está aquí porque
una corrección que solo vive en el chat se pierde, y la siguiente sesión repetiría
la alarma.

### R1 · `p0x` podía irse a GitHub de un `git push` distraído
**Qué vi.** El remoto `origin` de `p0x` apunta a un GitHub **público** y estaba
configurado para push. Un `git push origin master` habría publicado 58 commits de
doctrina interna, inventario de nodos y estructura de bucles.
**La lección.** Una salida peligrosa que solo la disciplina evita, tarde o temprano
se usa. Se cierra en la configuración, no en la costumbre.
**Qué hice.** `pushurl` de `origin` apunta a `NO-PUSH://p0x-no-va-a-github`: cualquier
push a GitHub falla en voz alta. Y existe la rama `publico`, con los 476 ficheros de
idea y **cero ejecutables**, para cuando se decida publicar.
**Revertir.** `cd ~/p0x && git remote set-url --push origin https://github.com/piskyRpapalo/p0x.git`
