# LoRAtelier · especificación pulida

**Qué es esto.** La visión y la estructura las firmó el Soberano; están aceptadas y no se tocan: el
flujo progresivo, los bloques desde datos, los tres niveles, el cuestionario guiado, los tests de sí
o no, las valoraciones, la pregunta abierta central y el espíritu IKEA. **Lo que cambia aquí es lo
que el texto daba por cierto sobre el rack y no lo es**, más el enfoque del primer entrenamiento en
Mistral, que es europeo y de licencia Apache 2.0.

Todo lo de abajo está medido el 2026-09-06. Nada implementado.

---

## A · Los siete fallos, con su evidencia

### A1 · 🔴 «El modelo firma el primer recuerdo» — eso rompe IronClaw

El paso siete del flujo dice que el modelo firma. **Un modelo no firma nunca.** Silicio propone,
carbono firma: la firma es de la persona, con su clave Ed25519, que en esta web ya existe
(`auth.js`, firma de 64 bytes, `ed25519:<128 hex>`).

**Corrección:** el modelo **compone** el primer recuerdo y lo **propone**; la persona lo firma con un
gesto explícito, o lo guarda sin firmar. Un recuerdo sin firma es válido y es local; lo que no puede
existir es un recuerdo firmado sin que alguien haya firmado.

### A2 · Los modelos asignados a la Categoría 1 no existen donde se van a buscar

`Ministral 3 14B Reasoning 2512` y `Ministral 3 8B Reasoning 2512`: **`ministral` devuelve 404 en la
biblioteca de Ollama.** No hay forma de traerlos por la vía que el rack usa. Lo que sí existe,
comprobado hoy, con su tamaño real en Q4:

| Modelo real | Tamaño Q4 | Dónde cabe |
|---|---|---|
| `mistral:7b-instruct-v0.3` | **4,4 GB** | portátil normal, 8 GB de RAM |
| `mistral-nemo:12b-instruct-2407` | **7,1 GB** | equipo holgado, 16 GB |
| `mistral-small3.2:24b-instruct-2506` | **15 GB** | el Beelink del Soberano, con sitio de sobra |
| `magistral:24b-small-2506` | ~15 GB | es el **de razonamiento** — ver A3 |

### A3 · El modelo «Reasoning» es justo el que no se quiere en un bucle

El texto pide razonamiento extendido para el cuentacuentos. El canon del nodo ya midió lo que cuesta:
**45 tokens de pensamiento invisible para responder una sola palabra**, y a 5 tok/s eso es tiempo de
pared en cada turno. Un cuentacuentos que hace esperar deja de contar el cuento.

**Corrección:** el cuentacuentos usa el **Instruct**, no el reasoning. `magistral` se reserva para
tareas donde el razonamiento se paga a gusto — análisis de resultados, no bienvenida.

### A4 · Los idiomas no son tres ni seis: son ocho, y son un impuesto

El sitio tiene **ocho**: `de, el, en, es, fr, it, pt, ru`, cada uno con su papel en
`assets/prompts-<idioma>.js`. El gate exige paridad de claves entre ellos.

Esto no es una ventaja del plan: es su mayor coste oculto. El cuestionario guiado (5 tipos de
pregunta), los 8 tests de sí o no, las 6 dimensiones de valoración y la pregunta abierta suman
**decenas de cadenas nuevas × 8 idiomas**. Escribirlas es el trabajo; olvidarlas pone el gate en rojo.

**Corrección:** el bloque nace **con un solo cuestionario y cuatro tests**, no con el catálogo
completo. Se amplía cuando haya probadores que justifiquen la traducción, no antes.

### A5 · Las medias comunitarias son NO_DATA por construcción, y hoy no se pueden escribir

Medido contra el Ágora en vivo:

```
/api/v1/threads  → 200  {"hilos_reales": 0, "escritura": "cerrada: el Agora todavia no modera"}
/api/v1/medidas  → 404
```

Y `threads.json` lo dice por escrito: *«todavía no hay comunidad: fingir actividad en un foro vacío
es la mentira más vieja de internet»*.

O sea: **cero contribuyentes, escritura cerrada a propósito, y ningún endpoint donde acumular tests
ni valoraciones.** Un sistema de medias sobre n=0 que no enseñe la n es exactamente la mentira que el
proyecto declara no cometer.

**Corrección, en dos partes:**
1. Toda media viaja **con su n al lado**, siempre. Con n=0 se pinta `NO_DATA · sé el primero`, no un
   cero ni una barra vacía.
2. Los tests y valoraciones se guardan **primero en local** (firmados por la persona si quiere), y se
   envían cuando exista `/api/v1/medidas` y la escritura se abra. El aporte no se pierde: espera.

### A6 · «No hay botón de descarga sin artefacto firmado» significa que hoy no hay ningún botón

La regla tres es correcta y hay que aplicarla entera: **hoy no existe ni un solo LoRA publicado con
hash**. Los que hay viven en `preceptor-lora/salida` (803 MB), sin publicar.

**Corrección:** el LoRAtelier **nace sin descargas**, con todos los bloques en `en estudio` o
`en entrenamiento` y su causa. Eso no es una página vacía: es la página honesta, y es la que hace
creíble el primer botón cuando aparezca.

### A7 · Dos memorias distintas, que el texto trata como una

El cuestionario dice guardar en «la memoria local». Hay dos, y no son la misma:

| | dónde vive | qué guarda |
|---|---|---|
| `memory.db` | la máquina de la persona, en el MVP | la conversación, el Camino, los recuerdos |
| el navegador | la web | lo que el visitante responde en el LoRAtelier |

La web **no tiene memoria del visitante**. Un cuestionario respondido en preceptoros.org no llega a
`memory.db` salvo que la persona se lleve el artefacto y lo importe.

**Corrección:** el cuestionario del LoRAtelier produce un **fichero de personalización** que la
persona descarga junto al artefacto. Ese fichero es el puente entre la web y su máquina. Si además
tiene perfil firmado, se le guarda; si no, se lo lleva y ya está.

---

## B · Una corrección a favor: el rack sí sirve cerebro

Medido hoy, y **desmiente el comentario de `rack.js`** —que declara el túnel pendiente— y también lo
que este mismo cuaderno dijo ayer:

```
POST https://api.preceptoros.org/api/generate   →  200 · "NO_DATA." desde preceptor-v7
```

El túnel funciona para inferencia. `/api/tags` sigue en 404, así que **la web no puede listar los
modelos del rack**, solo pedirle un turno al que ya sabe nombrar. El cuentacuentos servido desde el
rack **no está bloqueado**.

---

## C · El primer entrenamiento: Mistral, y lo que Mistral no cubre

**Por qué Mistral.** Europeo, Apache 2.0, disponible por la vía que el rack ya usa, y con tres
escalones que cubren de un portátil normal al Beelink. Es una decisión de soberanía tanto como
técnica, y se sostiene con las cifras de A2.

**El reparto propuesto:**

| Escalón | Modelo | Q4 | Para qué |
|---|---|---|---|
| Rack (cuentacuentos servido) | `mistral-small3.2:24b-instruct-2506` | 15 GB | la voz de la web, servida por el túnel |
| Usuario con equipo normal | `mistral:7b-instruct-v0.3` | 4,4 GB | el mismo personaje en su máquina |
| Usuario con equipo holgado | `mistral-nemo:12b-instruct-2407` | 7,1 GB | más calidad, 128k de contexto |

**Y lo que hay que decir en voz alta: Mistral no llega al escalón bajo.** El más pequeño son 4,4 GB
en Q4, que **no cabe en un teléfono de 4 GB**. La familia no tiene nada por debajo. Tres salidas, y
la elección es del Soberano:

1. **Cuantizar más** (Q3/Q2 del 7B). Baja de tamaño con coste de calidad — **a medir, no a suponer**.
2. **Aceptar que el escalón bajo no es Mistral** y usar otra familia ahí, diciéndolo.
3. **Dejar el escalón bajo en NO_DATA** hasta que haya medición en el Doogee.

La opción 3 es la honesta mientras no haya medida, y no impide empezar por arriba.

**El primer LoRA, concreto:** bienvenida sobre `mistral:7b-instruct-v0.3`, con el corpus de doctrina.
Se elige el 7B y no el 24B para el **primer** entrenamiento por una razón medida: el nodo afina por
CPU en 553 s y 445 s con modelos pequeños, y esa vuelta corta es lo que permite iterar. El 24B se
sirve; el 7B se entrena.

---

## D · Las categorías, corregidas

Del texto llegaron tres de las cinco. Se ajustan así, y las dos que faltan quedan pendientes de que
el Soberano las escriba.

### 1 · La Bienvenida
**Problema humano:** entender qué puedo hacer con mi máquina sin leer documentación. *(intacto)*
**Modelo:** `mistral-small3.2:24b-instruct-2506` en el rack · `mistral:7b-instruct-v0.3` en local.
**Cambios:** fuera el reasoning (A3). El modelo **propone** el primer recuerdo; firma la persona (A1).

### 2 · El Medidor
**Problema humano:** las specs de marketing no son mediciones. *(intacto, y es el mejor de los tres)*
**Modelo:** `mistral:7b-instruct-v0.3`. Sustituye a SmolLM3 por coherencia europea; si se quiere el
escalón de 4 GB aquí, aplica lo de C.
**Cambios:** «compara con la media comunitaria» pasa a **«compara con la media comunitaria, con su
n»**, y con n=0 dice `NO_DATA · sé el primero` (A5). Esta categoría es la que más se apoya en algo que
ya existe: el benchmark y `medidas.json`, cuyo contrato ya declara *«la web solo lee»*.

### 3 · La Memoria de Aprendizaje
**Problema humano:** la educación personalizada como archivo local, no como suscripción. *(intacto)*
**Modelo:** aquí **no toca Mistral todavía**. Multimodal y 262k de contexto son requisitos de otra
familia, y mezclarlos con el primer entrenamiento dispersa el esfuerzo.
**Cambios:** esta categoría **entra como visión**, no en la primera tanda. Y su memoria es
`memory.db`, del MVP — o sea que vive en la app, no en la web (A7).

---

## E · Lo que se mantiene entero

No se toca nada de esto, porque es lo bueno del texto:

- **Bloques desde datos**: añadir una línea es añadir un registro, nunca tocar lógica.
- **Los tres niveles**: utilidad humana → estado y contribución → ficha técnica. Con una salvedad:
  la regla de «la capa pública no menciona modelos» choca con `instalar.html`, que **ya los nombra**
  porque deriva su catálogo de `modelos.json`. Dos páginas del mismo sitio no pueden decir cosas
  distintas sobre lo mismo: o la regla se acota al LoRAtelier, o se revisa Instalar. **Decisión del
  Soberano.**
- **El cuestionario guiado**, con sus cinco tipos, interrumpible, con progreso y con resumen antes de
  confirmar. Es la pieza más fuerte del documento.
- **Los tests de sí o no y las valoraciones de 0 a 10**, opcionales y siempre ofrecidos.
- **La pregunta abierta central** — *¿qué debería saber el modelo dentro de sus capacidades?*—, que
  es la mejor idea del texto: convierte cada uso en corpus.
- **El autocompletado visible y editable**: nada de magia; se ve de dónde sale cada dato.
- **El versionado de plantillas** y que la personalización del usuario **nunca se sobreescriba**.
- **El espíritu IKEA**: el montaje le pertenece a quien lo monta.

---

## F · Presupuesto: dónde cabe todo esto

El tope es **16 KB por fichero** (`TOPE_FICHERO`), y `benchmark.html` está en 9.270 B. Todo lo nuevo
—render de bloques, niveles, cuestionario, tests, valoraciones, autocompletado— no cabe en un
fichero. Se parte por lo que es, como ya hizo el chat al partirse en `engine.js`, `fallback.js` y
`chat-router.js`:

| Fichero nuevo | De qué es dueño |
|---|---|
| `loratelier.json` | los bloques, como datos. Añadir línea = añadir registro |
| `taller.js` | render de bloques y los tres niveles |
| `taller-cuestionario.js` | los cinco tipos de pregunta, el progreso y el resumen |
| `taller-retorno.js` | tests de sí o no, valoraciones, pregunta abierta, y la cola local |

Y **cero páginas nuevas**: el presupuesto sigue en 9/9 y el LoRAtelier ya tiene la suya
(`benchmark.html`).

---

## G · Orden de implementación, reordenado por lo que desbloquea

El orden del texto es correcto salvo que empieza por donde no se puede acabar. Este empieza por lo
que ya se sostiene:

1. **`loratelier.json` con los bloques en `en estudio`** y su causa. Sin descargas (A6). Es la página
   honesta y se puede publicar hoy.
2. **Render por niveles** desde ese fichero.
3. **El primer LoRA de bienvenida** sobre `mistral:7b-instruct-v0.3`, entrenado en el nodo.
4. **Firma y hash del artefacto** — el mecanismo Ed25519 existe para texto; falta aplicarlo a un
   binario.
5. **Descarga con verificación de hash**, que ya tiene algo que descargar.
6. **Plantilla de instrucciones** editable y borrable línea a línea.
7. **Cuestionario guiado**, con su fichero de personalización descargable (A7).
8. **Resumen de comprensión** antes de confirmar.
9. **Autocompletado visible**, con su origen a la vista.
10. **Retorno**: cuatro tests, tres dimensiones de valoración, la pregunta abierta. **En cola local**
    mientras el Ágora no acepte escritura (A5).
11. **Medias con su n**, cuando exista `/api/v1/medidas`.
12. **Versionado de plantillas** con el feedback acumulado.
13. **Tests de extremo a extremo** en el gate de la web.
14. **Nada a producción sin firma humana.**

---

## H · Lo que necesita firma antes de empezar

1. **El escalón bajo** (C): cuantizar más, otra familia, o NO_DATA hasta medir en el Doogee.
2. **Modelos en la capa pública** (E): ¿la regla se acota al LoRAtelier o se revisa Instalar?
3. **Abrir la escritura del Ágora** exige moderación, y hoy está cerrada a propósito. Sin esa
   decisión, el retorno de la comunidad se queda en cola local — que funciona, pero no acumula.
4. **Las dos categorías que faltan** de las cinco.
