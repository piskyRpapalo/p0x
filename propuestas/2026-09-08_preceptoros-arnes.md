# PreceptorOS como ARNÉS · propuesta al Soberano

**Estado:** PROPUESTA · sin firmar · 2026-09-08
**Alcance:** `soberano` (este nodo) y el contrato que después viaja al resto
**Origen:** encargo del Soberano — *«PreceptorOS es un Harness adaptable múltiple
(AI local y AI externa, mismo nodo, mismo objetivo)»*

---

## 0 · La tesis, en una frase

Hoy PreceptorOS es **una app que una persona usa**. La propuesta es que sea
**el arnés por el que pasa toda inteligencia que trabaje en este rack** — la
local y la de frontera — con el mismo contrato para las dos.

Lo que lo hace viable no es una idea nueva: es que **el contrato ya existe y
está escrito**, sólo que en el sitio equivocado. `CLAUDE.md` lleva desde julio
diciendo qué puede y qué no puede hacer un cerebro según `P0X_BRAIN`:

> Si `P0X_BRAIN=local`: no tocas canon. No propones enmiendas de doctrina. No
> emites veredictos de arquitectura. **Si detectas algo que la merece, lo anotas
> como hallazgo y PARAS.**

Esa disciplina existe **para mí** y no existe para los modelos que corren en el
rack. Nadie se la ha dado. La propuesta es bajarla del arnés de Claude Code al
arnés de PreceptorOS, donde puede aplicarse a los dos.

---

## 1 · La base de datos: lo utilitario y lo matemático

### 1.1 · La unidad de coste, medida

En este nodo la cifra que manda no es el disco. Es el **prompt**:

| | medido | fuente |
|---|---|---|
| prompt, Vulkan | **67,17 tok/s** | `llama-bench`, 2026-08-25 |
| generación, Vulkan | 4,63 tok/s | ídem |
| ventana del cerebro local | 65.536 | firmado 2026-09-04 |

De ahí sale el número que debería gobernar el diseño entero:

> **1.000 tokens de contexto ≈ 15 segundos de pared, antes de generar una sola
> palabra.**

Un recuerdo que se recupera y no se usa no es «ruido»: es **quince segundos por
cada mil tokens** que alguien está esperando delante de una pantalla. En el
cerebro local de `cc-local` esto ya está medido en su forma extrema: **454 s
esperando el primer token**, con el cliente al 1,1 % de CPU — no colgado,
leyendo su preámbulo.

### 1.2 · Lo que hay hoy, medido

`memory.buscar()` (memory.py:892):

```python
def buscar(c, consulta, incluir_archivados=False, limite=50):
    ...
    sql += " order by rank limit ?"
```

Ordena por BM25 —que es lo correcto— y después **corta por FILAS**. Cincuenta
filas pueden ser 300 tokens o 12.000; el código no lo sabe y no lo pregunta.
**No hay presupuesto de tokens en ninguna parte del árbol.**

Esa es la única pieza que falta para que la recuperación deje de ser una
consulta y pase a ser una **decisión de coste**.

### 1.3 · La función objetivo

Recuperar no es «traer lo que casa». Es resolver:

> maximizar la información traída, **sujeto a un presupuesto de tokens**.

Es una mochila (*knapsack*), y como toda mochila necesita que cada pieza declare
su **valor** y su **peso**. El peso es trivial —tokens del engrama—. El valor
es lo que hay que construir, y se descompone en tres factores que ya tienen
evidencia en este repo:

```
valor(e) = relevancia(e,q) · frescura(e) · unicidad(e)
peso(e)  = tokens(e)
```

**relevancia** — ya la da BM25. No hay que inventarla.

**frescura** — un engrama sin verificar desde hace tres meses no vale lo mismo
que uno comprobado ayer. El Ojo ya lo sabe: cada entrada de su glosario lleva
`donde_verlo`, un comando que la comprueba. Eso no es documentación: es una
**prueba ejecutable por engrama**. La propuesta es que `engrams` gane
`verificado_en` y `verificado_con`, y que el valor decaiga con el tiempo desde
la última verificación. Un recuerdo que nadie puede comprobar debería hundirse
solo.

**unicidad** — y aquí está la evidencia más dura, y es del propio Ojo:

> *«Esta entrada estaba TRES VECES en este glosario con tres redacciones
> distintas. Tres verdades sobre el mismo hecho es exactamente lo que este rack
> lleva un mes pagando.»*

Tres copias del mismo hecho cuestan tres veces su peso y aportan una vez su
valor — y además **discrepan**, que es peor que no estar. Un engrama casi
idéntico a otro que ya entró en la mochila debe valer casi cero.

### 1.4 · Lo que hay que construir, en orden de coste

1. **`recuperar(consulta, presupuesto_tokens)`** — el mismo BM25, cortando por
   presupuesto y no por filas. Es la pieza más barata y la que más devuelve.
2. **`verificado_en` / `verificado_con`** en `engrams`, con el decaimiento.
   Convierte el glosario del Ojo de prosa a sensor.
3. **Deduplicación al escribir**, en la aduana: `/api/anidar` ya no se fía del
   cliente; que tampoco se fíe de que el hecho sea nuevo. Un candidato con
   solapamiento alto contra un engrama vivo se propone como **fusión**, no como
   alta.
4. **Una prueba de presupuesto en el gate**: para un banco de consultas reales,
   el contexto devuelto no pasa de N tokens y contiene la respuesta. Sin esa
   prueba, todo lo anterior envejece en silencio.

### 1.5 · Lo que supone a nivel usuario

Esto no es higiene de base de datos. Es lo único que separa dos productos:

- Sin presupuesto: la memoria **crece** y el producto **se ralentiza con el
  uso**. Quien más lo usa, peor lo tiene. Eso mata un producto local.
- Con presupuesto: la memoria crece y **el coste por turno se queda plano**,
  porque lo que entra al modelo está acotado por diseño. El usuario nota que su
  aparato no se degrada — que es exactamente la promesa que la nube no puede
  hacer.

**Lo semántico se queda fuera a propósito**, y el comentario de `memory.py` ya
tiene razón: embeddings rompen la promesa de biblioteca estándar. La propuesta
no la toca. Lo que sí se puede hacer sin salir de la stdlib es lo de arriba —
presupuesto, frescura, unicidad — y **es donde está casi toda la ganancia**,
porque hoy el problema no es que se recupere lo equivocado: es que se recupera
sin límite.

---

## 2 · La disciplina: de «no borres» a «conoce tu alcance»

### 2.1 · El vocabulario que ya existe

Este proyecto ya sabe decir «no lo sé» de tres maneras, y las tres son honestas:

- **`NO_DATA`** — el dato no está, y se dice con su causa.
- **el Kill Switch pedagógico** — el modelo local delega en el usuario para que
  vaya a cazar la respuesta fuera y la traiga al Nido.
- **la web sin motor** — te da el JSON para que te lo lleves a la IA que ya
  tengas, en vez de quedarse en blanco.

Los tres son el mismo gesto: *no fingir, y decir por dónde se sigue*.

### 2.2 · Lo que falta: `NO_CAPAZ`

Falta el cuarto, y es el que pide el encargo: **esta tarea me excede, y en este
rack hay quien puede.**

No es un mensaje de error. Es un **traspaso estructurado**:

```json
{
  "estado": "NO_CAPAZ",
  "por_que": "reescritura de doctrina · fuera del alcance de un cerebro local",
  "hallazgo": "<lo que SÍ he averiguado, que no se tira>",
  "sugiere": "frontera",
  "porque_ese": "capacidad declarada en capacidades.json · tarea=doctrina"
}
```

Tres cosas lo hacen distinto de rendirse:

1. **El hallazgo viaja.** El trabajo hecho no se pierde: es exactamente lo que
   ya manda el canon — *«lo anotas como hallazgo y PARAS»*.
2. **No elige por su cuenta.** Nombra a quién le toca **según una tabla
   medida**, no según lo que crea de sí mismo. Un modelo pequeño juzgando su
   propia capacidad es la alucinación de la que venimos.
3. **Queda escrito.** Cada `NO_CAPAZ` es una fila. Y la serie de esas filas es
   la telemetría que dice qué le falta al rack — que es lo que decide el
   siguiente LoRA. *El sistema aprende de lo que no supo hacer.*

### 2.3 · La tabla de capacidades

Hoy `cerebros.json` mide **velocidad** por modelo (`prompt`, `generacion`,
`carga_s`) y eso ya viaja a la web. Lo que no existe es capacidad **por tarea**.

La propuesta es `capacidades.json` con el mismo contrato que el resto de esta
casa: **medido o `NO_DATA`, nunca supuesto**. Una fila por (modelo, tarea), con
su fecha, su banco de prueba y su resultado. Y la regla dura, que es la que
evita que esto se convierta en marketing interno:

> Un modelo no declara lo que puede hacer. **Lo declara la medida**, y si no hay
> medida hay `NO_DATA` — que se lee como «no encaminar aquí», no como «vale».

### 2.4 · Y por qué esto es el arnés

Con esas dos piezas —presupuesto de contexto y traspaso declarado— PreceptorOS
deja de ser una app y pasa a ser lo que el encargo dice: **el mismo contrato
para la IA local y para la externa**. Yo recibo mi arranque por la misma puerta
que el modelo de 3B recibe el suyo; los dos escribimos por la misma aduana; los
dos declaramos lo que no podemos. La diferencia entre nosotros deja de estar en
el código y pasa a estar donde debe: **en la tabla de capacidades**.

---

## 3 · Perfiles: Soberano1..N, y el borde

El encargo: un **perfil del Soberano** que controle la web directamente, listo
en modo EDGE para conectar Claude Code, y abierto a que los usuarios enchufen
sus propias IAs locales. *«Los siguientes usuarios que guarden su nombre irán
así llamados por defecto en orden de entrada, hasta que ellos decidan
cambiarlo.»*

### 3.1 · Una tensión que hay que decidir antes de escribir código

Hoy la identidad de la web es **soberana y sin servidor**: `auth.js` genera una
clave Ed25519 no extraíble en el navegador y el apodo **se deriva** de ella:

```js
return 'Tester-' + hex(h).slice(0, 4).toUpperCase();
```

Derivado significa: nadie puede pedir un nombre que ya sea de otro, y **no hace
falta registro**.

**«Orden de entrada» rompe eso.** Un ordinal exige que alguien sepa quién fue el
primero — es decir, un registro compartido. No hay forma de tener las dos cosas
a la vez, y prefiero decirlo ahora que descubrirlo a mitad.

Tres salidas, y la recomendación:

| | qué es | qué cuesta |
|---|---|---|
| **A** · ordinal en el rack | el rack asigna el número **al conectar** | deja de ser sin-servidor **para quien conecta**, que es quien ya decidió conectar |
| **B** · ordinal local | cada aparato se numera a sí mismo | dos usuarios serían «Soberano1» los dos. No sirve |
| **C** · derivado + ordinal opcional | sigues siendo `Soberano-A3F9` sola; al conectarte al rack recibes tu ordinal | dos nombres para la misma persona |

**Recomiendo A, y con una frontera dicha:** el ordinal lo da el rack **solo a
quien se conecta al rack**. Quien use PreceptorOS a solas nunca pide un número y
nunca lo necesita — la promesa de «sin cuentas» sigue entera para él. El ordinal
no es identidad: es **orden de llegada a una comunidad**, y esa comunidad tiene
un sitio físico. Registrar quién llegó primero a un sitio no contradice que no
haya cuentas; fingir que se puede numerar sin registro, sí.

### 3.2 · El perfil como dimensión, no como fichero

Y esto responde a la pregunta que te dejé abierta ayer. Preguntaba entre **una
base con espacio de nombres** o **dos ficheros**. Tu visión la contesta: en
cuanto hay Soberano1..N, la dimensión no es `origin='ojo'` — es **`quien` ×
`origin`**. Con dos ficheros, cada usuario nuevo sería un fichero nuevo y
volveríamos al problema del que venimos.

**Una base. Dos columnas de espacio de nombres.** Y `data/users/me` como el
único camino a lo privado, igual que ya hace el resto de la casa.

---

## 4 · La regla permanente que pides (propuesta de canon)

> **Toda ronda cerrada termina con una propuesta de ahorro.** Antes de las
> SUGERENCIAS, el reporte al Soberano incluye —si la hay— una herramienta o un
> cambio que haga que PreceptorOS local **gaste menos tokens** o **afiance su
> estructura interna**. Con su coste (S/M/L) y con la medida que la justifica.
> Si en esa ronda no la hay, se dice: *«sin propuesta de ahorro esta ronda»*.
> Una regla que solo se cumple cuando hay algo que decir se convierte en una
> regla que se cumple inventando.

---

## 5 · Etapas

| | qué | reversible |
|---|---|---|
| **0** | el puente: `glosario.json` → `engrams` con `quien`/`origin`; el gate exige que las dos fuentes digan lo mismo | sí, entero |
| **1** | `/api/arranque` en la app. Mi sesión arranca por ahí. **Yo paso a ser el primer usuario diario** | sí |
| **2** | `recuperar(consulta, presupuesto)` + la prueba de presupuesto en el gate | sí |
| **3** | `verificado_en` y la deduplicación en la aduana | migración aditiva |
| **4** | `capacidades.json` medido y `NO_CAPAZ` con su tabla | sí |
| **5** | perfiles Soberano1..N y el borde | decisión 3.1 primero |
| **6** | el Ojo-Vivo como vista de la app; el perfil `soberano` separado del producto | sí |

Las etapas 0-3 no necesitan ninguna decisión nueva. La 5 necesita la de 3.1.

---

## 6 · Lo que NO propongo, y por qué

- **No propongo embeddings.** Rompen la stdlib y el grueso de la ganancia está
  antes.
- **No propongo que el rack decida por el usuario.** `NO_CAPAZ` *sugiere*; quien
  encamina es el arnés, y el usuario ve el traspaso.
- **No propongo meter la telemetría del rack en el producto.** Vatios, tailnet y
  gates entran como **perfil `soberano`**, cargado solo en este nodo. Si entran
  como función, todo el que instale la app se lleva código del rack dentro y se
  rompe la promesa de que no habla con la red.
