👁️ OJO DEL SOBERANO · MANIFIESTO DEL BUILDER

PreceptorOS · redactado el 2026-09-04

Esto no es un folleto. Es la declaración de qué promete este taller, qué cuesta y qué
todavía no sabe hacer. Cada afirmación viene con el sitio donde se comprueba, porque un
manifiesto que solo afirma es propaganda.

La regla que gobierna el documento entero: si una capacidad no está medida, se declara
como ausente y con su causa. Un hueco declarado vale más que una cifra plausible del orden
de magnitud equivocado, porque a la cifra plausible nadie la mira dos veces.

---

## I · Soberanía del Silicio

El límite lo pone tu hardware, no la factura de nadie. No hay cuota por turno, ni ventana
que caduque, ni precio por pensar. Mientras tu máquina esté encendida y sea tuya, el
trabajo continúa. Eso es lo que quiere decir "tokens infinitos".

**Tu Ojo local es la base de datos que construyes con tu uso.** No es un panel de control
ni una carpeta de configuración: es tu segundo cerebro, viviendo en tu disco. Cada turno
que guardas, cada corrección que haces, cada proyecto que abres se queda ahí y se puede
buscar. Esa base crece contigo y no existe en ningún otro sitio — no hay copia en un
servidor, no hay respaldo ajeno, no hay nadie más que pueda leerla.

Se comprueba en: `preceptor/memory.py` (la base con búsqueda de texto completo),
`preceptor/captura.py` (cómo entran los turnos), y el fichero real en
`~/.preceptoros/memory.db`.

Ahora tienes una herramienta, adáptala a tu ser. Las habilidades que aprendas por el
camino, compártelas. Mientras te inspiras, comparte con los demás tus encuentros,
herramientas y conocimiento.

**Y el reverso, que es lo que hace honesta la frase.** Infinito no quiere decir gratis:
quiere decir que el precio lo pagas en silicio y no en suscripción. Tu máquina tiene un
techo — de memoria, de velocidad, de contexto — y ese techo es real. Un modelo puede no
caber. Una respuesta puede tardar minutos.

Que el sistema te diga "no cabe en tu memoria" en vez de "se ha agotado tu plan" es
exactamente la diferencia que defiende este documento: un límite físico se ve, se mide, y
se puede cambiar comprando memoria. Un límite comercial solo se acata.

Corolario para quien construye: antes de cargar un modelo grande, mide. `ollama ps` dice
qué hay cargado ahora mismo en tu máquina; sin modelo cargado no hay cifra de consumo, y
el tamaño del fichero en disco no la sustituye. Eso está implementado, no sugerido:
`preceptor/metricas.py`, funciones `_modelos_cargados()` y `_rss_del_runner()`.

---

## II · El Harness, no el Oráculo

Las IAs de este taller son compañeros dentro del silicio. No son una autoridad a la que se
consulta: son una herramienta que trabaja a tu lado, en tu máquina.

**Su inteligencia nace de lo que hay en el rack local** — el tuyo, o el que te preste la
puerta de entrada mientras montas el tuyo. No saben de la nube. Saben de lo que les enseñas
en tu propio entorno: los documentos que traes, las correcciones que haces, la memoria que
construyes. Un compañero de taller conoce el taller.

Eso tiene una consecuencia que conviene aceptar antes de empezar: **cuando este taller no
sabe algo, lo dice.** No inventa para no quedar mal. El "no lo sé" no es una disculpa, es
una herramienta — te dice dónde está el borde de lo que tienes, y te deja a ti la decisión
de traerlo. Un compañero que rellena huecos con adornos te cuesta más tiempo del que te
ahorra.

**Los datos no salen sin consentimiento explícito**, y eso no es una promesa: es código
escrito y probado. Tres piezas lo sostienen, y ninguna es una intención.

**`guardrails.py`** — el filtro que sanea antes de que nada salga. Cuatro políticas
centrales, y están escritas con ese nombre en el fichero: `API_KEY`, `PRIVATE_KEY`,
`SSH_PUBLIC_KEY`, `ASSIGNED_SECRET`.

**`soberania.py`** — el guardián de permisos, con una regla que no admite matices: ante
cualquier duda, no. Sin fichero, con el fichero roto, con el disco mudo, con una capacidad
que nadie declaró — todos esos caminos terminan en el nivel cero, y ninguno termina en una
excepción. Que no lance importa tanto como que devuelva cero: un módulo de permisos que
revienta deja al que llama decidiendo por su cuenta dentro de un `except`, y ahí es donde
se cuelan los permisos que nadie concedió.

**`frontera.py`** — la celda para código propuesto: memoria acotada, procesador acotado por
combustible determinista, sin sistema de ficheros y sin red. Un bucle infinito muere por
falta de combustible en vez de colgar tu máquina, y ningún estado sobrevive de una
propuesta a la siguiente.

El silicio propone dentro de la celda; el carbono firma fuera.

---

## III · Comunidad de Constructores

Este proyecto existe para romper barreras de aprendizaje. No para vender una herramienta:
para enseñar una forma de trabajar y entregarla entera.

**Lo que se replica no es el código, es la metodología.** El Soberano construyó su Ojo —su
segundo cerebro, su forma de medir, su disciplina de no dar nada por supuesto— y lo que
este proyecto hace es hacerlo accesible para que cualquiera construya el suyo. No un clon
del suyo: el tuyo, con tus dominios, tus fuentes y tus proyectos.

**El viaje, tal y como está diseñado:**

**1. Llegas a la web, y te la llevas.** La primera IA que te habla desde el rack te explica
la filosofía de la comunidad: qué es esto, por qué existe, y qué puedes construir aquí. No
te pide una cuenta — te pide instalar la web progresiva en tu aparato. Se queda como un
icono más, funciona como una aplicación y no depende de que vuelvas a escribir una
dirección. Es la puerta de entrada y el guía: máxima facilidad para comunicarse, sin decidir
nada todavía.

**2. Instalas el taller.** La segunda IA —la que vive en la barra desplegable violeta de la
web— te dice cómo instalar la app local y usarla. Te acompaña paso a paso hasta que tienes
tu propio modelo corriendo en tu máquina. Aquí cambia el papel: máxima transparencia para
personalizar. Misma estética, mismo lenguaje, y tú al mando — eliges tu modelo, mides tu
hardware, ves tus métricas y empiezas a construir tu base de datos. Lo que en la web era una
demostración, aquí es tu taller.

**Acabas con dos iconos en el aparato, y es a propósito.** El primero es la puerta: te
explica, te acompaña y habla con el rack. El segundo es tu taller: no habla con nadie y
guarda lo tuyo. Son dos cosas distintas con dos promesas distintas, y por eso no se funden
en una — el día que la puerta y el taller compartan icono, la promesa de «esto no sale de tu
máquina» deja de poder señalarse con el dedo.

**3. Construyes mientras estás con nosotros.** El objetivo no es que instales y te vayas: es
que desarrolles tu propia IA local mientras formas parte de la comunidad. La app te guía
para que aprendas a personalizar prompts, leer métricas, entender tu hardware, configurar tu
perfil como usuario, declarar tus habilidades como persona y tus objetivos en la base de
datos. Todo eso alimenta el modelo local: cuanto más usas la app, más te conoce, y más
puedes transformarla si lo deseas. Las herramientas que construyas bajo esta filosofía son
compartibles y aplicables con instrucciones simples.

**4. La app te aconseja.** Cuando tu base de datos crece y tu hardware lo permite, la app te
sugiere cambiar el modelo o probar otro. No te obliga: te muestra qué hay disponible para tu
máquina y tú decides. El límite lo pone tu silicio, no una suscripción.

**5. Compartes tu medida.** Cuando acabas el tutorial, la app te pide que envíes un hash con
la prueba del modelo en tu máquina y un comentario tuyo diciendo para qué lo has usado o qué
mejora uno respecto a otro. Eso va al tablón de la web, llamado **LoRAtelier benchmark's**:
un espacio donde las medidas son comparables de verdad porque vienen de la máquina real, no
de un laboratorio.

Se comprueba en: la puerta de entrada y sus páginas (`preceptoros-web/public/`, con portada,
instalación, comunidad, comparativa, primeros pasos, banco de pruebas y perfil), el paquete
comparable de `preceptor/metricas.py`, y el tablón LoRAtelier benchmark's, que vive por
idioma en `preceptoros-web/public/{es,en,fr}/benchmark.html`.

Dos precisiones, porque este documento no cita lo que no existe. **La segunda IA de la barra
violeta está diseñada, no construida**: es la Capa 3 de la interfaz y todavía no se puede
señalar con el dedo. Y **LoRAtelier benchmark's es el nombre nuevo del banco de pruebas que
ya está ahí** — un renombrado de lo que hoy se llama comparativa, no una página aparte.

**Lo que se comparte es metodología, jamás datos crudos.** La separación está construida,
no solo enunciada: la aplicación funciona sin red y no enlaza a la web. Un enlace saliente
dentro de una herramienta que promete funcionar sin internet sería una ruta a la red justo
en el sitio donde se prometió que no la había. Al revés sí: la web puede hablar del
producto.

**Si bifurcas esta aplicación no creas un competidor: creas un nodo compatible.** No hay
licencia que perseguir ni servidor central del que depender, porque no hay servidor
central. La comunidad crece cuando cada usuario se convierte en nodo, no cuando cada
usuario se convierte en cliente.

---

## IV · Consentimiento Soberano

Nada de lo que escribas sale de tu máquina si no lo mandas tú. Cuando compartas métricas se
manda un identificador y un paquete agregado — nunca el contenido de tu base de datos,
nunca texto de tus conversaciones, nunca un fragmento "de ejemplo".

**El paquete agregado ya existe y tiene forma fija:** los once campos de
`preceptor/metricas.py`, diseñados como unidad de comparación entre máquinas. Son
magnitudes —nombre y base del modelo, memoria residente del proceso que sirve, ventana de
contexto, tokens por segundo, latencia del primer token, temperatura— y ninguna de ellas
contiene texto tuyo.

Dos detalles de ese paquete enseñan cómo está pensado todo lo demás.

**El hueco declarado.** El campo de memoria de vídeo sale como `NO_DATA` en una máquina con
gráfica integrada, y con la razón escrita al lado: una gráfica integrada comparte la memoria
del sistema y no tiene memoria propia, así que eso ya está contado en el campo del proceso
que sirve. Un cero ahí no sería un dato bajo — sería una magnitud que no existe. El
`NO_DATA` es la herramienta que separa "no lo hay" de "es cero", y esas dos cosas no son la
misma.

**Lo que se deja fuera a propósito.** El vatiaje del enchufe no entra en el paquete: mide el
rack entero, no el modelo, y meterlo dentro rompería la comparabilidad con cualquier paquete
que venga de una máquina sin enchufe medido.

### Lo que este taller todavía NO hace, y hay que decirlo aquí

**No hay firma criptográfica.** El plan de misión pedía una huella Ed25519 y no la hay, por
una razón que se sostiene: la biblioteca estándar de Python no trae Ed25519, y traerlo
exige o una dependencia pesada —que además no existe en el Termux del cliente— o escribir
la primitiva a mano, que es criptografía sin auditar. Las dos rompen las reglas que
sostienen este producto.

Lo que hay es la **Huella Soberana (SHA256)**: un `sha256` de una semilla aleatoria local de
32 bytes, nacida de `os.urandom` y de nada más — no del nombre de usuario, no del nombre de
la máquina, no de la dirección física de la tarjeta de red. Eso importa más de lo que
parece: una huella derivada del entorno haría que dos instalaciones de la misma máquina
dieran la misma —o sea, que la persona fuera rastreable entre ellas— y que dos personas con
el mismo modelo de portátil fueran indistinguibles.

**La Huella no es una clave.** No firma nada, no autentica nada y no da acceso a nada. Es un
nombre pseudónimo y estable para una instalación.

Se llama por su nombre y no por el del plan porque llamar Ed25519 a un sha256 sería mentir
sobre la primitiva justo en la pantalla que promete transparencia. Firmado por el Soberano
el 2026-09-02: "la doctrina valora la corrección técnica sobre la consistencia con un error
pasado". Está probado en `test_huella.py`, que existe precisamente para que el nombre no
vuelva a resbalar.

El día que haga falta firmar de verdad hará falta otra cosa, y será una decisión aparte —
no una función que ya estaba aquí y "servía".

Y la línea de doctrina que esto respeta al llamarse como se llama: jamás se firma valor.
Ninguna clave privada de firma entra en este nodo.

Se comprueba en: `preceptor/huella.py` (las primeras treinta líneas explican esto entero) y
`preceptor/test_huella.py`.

---

## V · Lo que este manifiesto no promete

**No promete que sea rápido.** Un modelo local en una máquina de escritorio genera a unos
pocos tokens por segundo. Eso se mide, se enseña y no se maquilla.

**No promete que lo sepa todo.** Sabe lo que le has traído. Cuando no sabe, lo dice.

**No promete cero mantenimiento.** Un taller se cuida. Los procesos que trabajan solos se
vigilan, y uno que lleva días sin dar señal tiene que verse como lo que es, no esconderse
detrás de un indicador en verde.

**No promete privacidad por confianza.** La promete por arquitectura, y la arquitectura se
puede leer: `guardrails.py`, `soberania.py`, `frontera.py`, `huella.py`.

---

## Cómo se comprueba este documento, en tu máquina

    cd ~/p0x/preceptor && bin/pruebas | tail -5    # la suite entera, en verde
    free -h && ollama ps                            # tu memoria y qué tienes cargado
    grep -n "VENTANA_MEDIDA" metricas.py            # la ventana que está medida
    sed -n '1,30p' huella.py                        # por qué no se llama Ed25519

Si alguna de esas cuatro cosas deja de cuadrar con lo escrito arriba, manda la máquina y no
el documento: se corrige el manifiesto.

---

*Pendiente de firma del Soberano.*
