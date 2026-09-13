# El Alquimista · lo que ya existe, y lo que de verdad falta

**Acta de recuperación.** 2026-09-08. Entrada del Soberano adaptada al terreno,
no copiada. Nada de esto está implementado bajo el nombre de Alquimista; lo que
sí está, se nombra abajo con el fichero donde vive.

---

## 0 · El hallazgo que cambia el encargo

**El Alquimista no es un módulo nuevo. Es una voz del canon, con papel escrito
desde antes.** `DISCURSO_FUNDACIONAL_P0X.md` lo define así:

> *Transmutador que lee la cadena sin tocarla; consejo, nunca Intent. NEAR
> mainnet/testnet keyless (saldos, cosecha), asesoría INFORMACIÓN-no-ejecución;
> custodia el camino NEAR AI (org ALCHEMIST, créditos de inferencia).*

Y `ALFABETO_P0X.md` lo lista entre las voces del Sínodo, junto a `monje`,
`vocero`, `berserker`, `escriba` y `enlace`.

Así que esto no se crea: **se recupera**. Y recuperar obliga a mirar si el papel
nuevo cabe en el viejo. En un punto, no cabe — está en §3.

---

## 1 · El histórico con NEAR, medido y no recordado

Buscado hoy en todo el árbol. Lo que hay:

| qué | dónde | estado |
|---|---|---|
| Doctrina de seguridad NEAR | `mente/esferas/near-ai.md` | escrita, v1.0.0, 2026-07-04 |
| Cuenta `hexelion.near` | mainnet · org ALCHEMIST | declarada, con $5 de crédito de inferencia |
| Separación crédito ≠ liquidez | esfera §0 | *«Jamás se mezclan en un bucle»* |
| Auto top-up | esfera §0 | **OFF**, y así se queda por doctrina |
| Incidente de identidad | `propuestas/2026-08-24_faro_identidad.md` | el Faro declaraba `hexelion.near` (mainnet) corriendo en testnet |

Y lo que **no** hay, dicho como corresponde:

> **`mente/telemetria/` no contiene NI UNA medida de NEAR.** Cero ficheros, cero
> líneas. Hay doctrina escrita y no hay histórico de pruebas.

**El Faro de `la-fragua` no responde hoy:** su `/health` devuelve `000`.  <!-- guardia:permitir acta propose-only sobre ese nodo, sin ruta ejecutable --> Si alguien recuerda pruebas contra ese servicio, no están aquí y
el servicio no está en pie ahora mismo. **NO_DATA con causa**, que es lo que
esta casa escribe cuando no puede medir.

**Y el incidente del Faro es la lección más útil que hay en este expediente.**
Un manifiesto declaraba la identidad `hexelion.near` en un servicio que corría
en testnet y se llamaba a sí mismo `hexelion-beato-01`. La sesión que lo miró
escribió la frase que hay que llevarse: *«roza jamás firmas valor por el lado de
la identidad, no por el de la clave»*. Un Alquimista que lea saldos tiene el
mismo riesgo: **leer la cuenta equivocada es tan grave como firmar de más**.

---

## 2 · El plano · qué está construido y bajo qué nombre

Los cinco pasos del encargo, cruzados contra el árbol de hoy. El Alquimista no
es obra nueva: es **ensamblaje**.

| paso del encargo | qué existe ya | dónde | falta |
|---|---|---|---|
| **1 · Esquema de linealidad** | **hecho y probado** | `linea.py` | ampliar `TIPOS` con el vocabulario de valor |
| **2 · El Sensor** | hecho para el silicio | `metricas.py`, `medidas.py` | los sensores de cadena, que son otros |
| **3 · El Juez determinista** | hecho a medias | `cifras.py`, `output_guard.py`, `guardrails.py` | las reglas de valor, y `explicar()` en una frase |
| **4 · Prompt del Propositor** | patrón ya probado | `preceptor-lora/forja/prueba_fuego_charla.py` | el prompt, y sus sensores de sabotaje |
| **5 · Interfaz de firma** | **registrada** como línea de investigación | `loratelier.json` → `supervision-humana` | dibujarla |

**Paso 1, en detalle, porque es el que sostiene todo lo demás.** `linea.py`
cumple la especificación del encargo campo a campo: identificador, marca de
tiempo, tipo de vocabulario cerrado, carga útil JSON, y **huella del evento
anterior encadenada**. Sin `update` y sin `delete`. El estado es el pliegue.
`verificar()` caza la manipulación parcial y dice en cuál evento. Y hay prueba
de lo que **no** garantiza: rehacer la cadena entera cuadra.

Lo único que le falta para servir al Alquimista es vocabulario. Hoy `TIPOS` es
`turno · veredicto · correccion · consentimiento · revocacion · rectificacion ·
importacion · sello · soberania`. El encargo pide `propuesta · firma · ejecucion
· cancelacion · fallo`. **Entra como ampliación aditiva** — nada de lo escrito
cambia de significado.

Con un matiz que no es de forma: `cancelacion` no es un tipo nuevo, es lo que
esta casa ya llama **rectificación**, y `fallo` es lo que llama **cicatriz**.
Antes de añadir palabras conviene ver si el hueco ya tenía nombre.

---

## 3 · Donde el encargo choca con el canon · y hay que decidir

**El Preparador, tal como está descrito, va más lejos de lo que la voz permite.**

El encargo dice: *«el sistema solo prepara el blob de la transacción; nunca la
firma ni la envía»*. Es prudente y respeta la firma humana. Pero el canon del
Alquimista dice *«lee la cadena sin tocarla; consejo, nunca Intent;
INFORMACIÓN-no-ejecución»*, y el canon del nodo dice:

> *Jamás firmas valor. Ninguna clave privada de firma (NEAR, ed25519 de
> atestación/valor) entra a este nodo.*

Preparar un blob **no es firmar**, y eso es cierto. Pero tampoco es *consejo*:
es fabricar el objeto que mueve valor y dejarlo a un clic. La distancia entre
«informar» y «tener la transacción hecha esperando» es exactamente donde un
sistema deja de ser asesor.

**No lo bloqueo, y no lo absorbo. Se declara y lo decides tú.** Tres salidas,
las tres defendibles:

1. **Enmendar el canon del Alquimista**, dejando escrito que prepara pero no
   firma ni envía, con el límite dicho. Es una D-entrada firmada por el carbono.
2. **Mover el Preparador fuera de `soberano`** — que prepare quien pueda tener
   material de valor cerca, y que este nodo solo informe. Encaja sin tocar nada.
3. **Quedarse en consejo**: el Alquimista dice qué haría y el carbono construye
   la transacción con sus herramientas. Es lo que el canon dice hoy.

Mi lectura, y es solo eso: la 2 conserva las dos doctrinas sin enmendar
ninguna, y la 1 es la que menos fricción tiene si el trabajo va a ser diario.

---

## 4 · Los nombres del enjambre

Tres de los cinco **ya son de la casa** y se quedan: **el Sensor** (así se
llaman los de la Prueba de Fuego), **el Juez** (`captura.juzgar` guarda el
veredicto *con juez nombrado*, y distingue carbono, modelo y determinista) y
**el Enjambre** (está en el léxico).

**Propositor**, **Validador** y **Preparador** son nuevos. No son mitología
inventada —describen lo que la función hace, que es lo que el molde permite—
pero conviene decir que entran hoy, para que la próxima sesión no los tome por
canon viejo. Si merecen otro nombre, es una entrada que firmas tú.

---

## 5 · El orden, y por qué este y no el del encargo

El encargo pide no saltar pasos, y tiene razón. Pero el paso 1 ya está, así que
el orden real empieza en otro sitio:

1. **Ampliar `TIPOS` con el vocabulario de valor** — aditivo, con `cancelacion`
   y `fallo` mirando antes si ya se llaman rectificación y cicatriz. **(S)**
2. **Los sensores de cadena.** Solo lectura, `NO_DATA` con causa, y sin bloquear
   nada si el servicio no responde — que es hoy el caso del Faro. **(M)**
3. **Las reglas del Juez, en texto lógico antes que en código.** Y una
   `explicar()` que devuelva UNA frase: un juez que no sabe decir por qué
   rechazó no se puede auditar. **(M)**
4. **El prompt del Propositor**, con sus sensores de sabotaje desde el primer
   día — el patrón de la Prueba de Fuego ya demostró que una corrida puede salir
   verde sobre una cifra inventada. **(M)**
5. **La pantalla de firma**, que ya tiene su hueco declarado en el LoRAtelier
   como `supervision-humana` (AI Act art. 14). **(M)**

**Y antes de todo eso, una medición que no cuesta nada:** ¿responde algo de la
cadena desde este nodo? Hoy el Faro da `000`. Un enjambre construido sobre un
sensor que no tiene qué leer es un enjambre que no se puede probar.

---

## 6 · Lo que este documento NO decide

- Si el Preparador vive aquí (§3).
- Si `hexelion.near` sigue siendo la identidad correcta, después del incidente
  del Faro. Nadie lo ha vuelto a verificar desde el 2026-08-24.
- Qué recursos entran en el alcance. El encargo nombra Accurast y MAST; **no hay
  ni una línea sobre ellos en este árbol**, así que entran como NO_DATA hasta
  que alguien los mida.
