# Propuesta · `POST /api/v1/corrections` en la-fragua

**Nodo destino:** la-fragua (`~/agora`) · **Origen:** soberano · **Fecha:** 2026-08-31
**Estado:** PROPUESTA. No se ha aplicado nada. Requiere firma del carbono.

## Por que esto es una propuesta y no un despliegue

`~/agora` no existe en soberano: se comprobo. Vive en la-fragua, y el canon del
nodo dice, con estas palabras, *«propose-only hacia otros nodos: cualquier cambio
que afecte a fragua/torre/vigia sale como artefacto propuesto en `p0x/propuestas/`,
nunca se aplica por SSH desde aqui sin mision explicita para ese nodo»*.

Se pregunto al Soberano si este encargo ERA esa mision explicita. Respondio que no:
sale como propuesta. Queda escrito para que dentro de seis meses nadie tenga que
reconstruir por que el endpoint no se subio el mismo dia que se escribio el boton.

## Que hay ya construido, y donde

El eslabon [2] **ya funciona** en `preceptoros-web` (commit `1d27ae6`):
`public/assets/corregir.js` firma el par y lo guarda en IndexedDB
(`preceptoros-bronce` / `correcciones`). **No tiene salida de red, y el gate lo
comprueba**: cero `fetch`, cero `XMLHttpRequest`, cero `sendBeacon`, medido sobre
el codigo con los comentarios quitados.

Es decir: el combustible ya se recoge. Lo que falta es la puerta por la que sale
—y esa puerta no se abre hasta que D1 y D2 esten firmadas.

## El contrato

```
POST /api/v1/corrections
Content-Type: application/json
```

```json
{
  "par": {
    "prompt":      "…",
    "respuesta":   "…",          // el RECHAZADO
    "correccion":  "…",          // el ELEGIDO
    "corregido":   "2026-08-31T06:41:00.000Z",
    "modelo":      "…",
    "idioma":      "es",
    "motivo":      "…",
    "consent":     0,
    "origen":      "preceptoros.org"
  },
  "firma":     "ed25519:<128 hex>",
  "publica":   "<clave publica en hex>",
  "autor":     "Tester-A3F9",
  "algoritmo": "Ed25519"
}
```

**El objeto que se verifica es `par` serializado con `JSON.stringify` tal cual.**
Mismo objeto, misma firma. La firma va **entera**: 64 bytes, 128 caracteres hex.
`auth.js` ya rechaza cualquier otra longitud, y el servidor debe hacer lo mismo —
una firma recortada es un adorno con nombre de garantia.

### Respuestas

| Codigo | Cuando |
|---|---|
| `201` | firma valida, escrito en Bronze. Devuelve el sha256 de la linea, para que quien envio pueda comprobar que llego lo que mando |
| `400` | JSON mal formado, o falta un campo del esquema |
| `401` | la firma no verifica contra `publica` |
| `413` | por encima del tope de tamano (ver abajo) |
| `503` | Bronze no escribible. **Nunca 200 con la escritura fallada** |

## Las cuatro reglas que no se negocian

1. **Bronze es append-only.** `correcciones.jsonl`, una linea por par, nunca se
   edita ni se borra. Es la misma disciplina que `latido.py` impone con cuatro
   disparadores de SQLite: no una convencion que dependa de quien escriba el
   proximo parche a las tres de la manana.
2. **`consent` llega en 0 y el servidor NO puede subirlo.** Solo el carbono lo
   sube, y lo sube en otro sitio. Un endpoint que pueda otorgarse consentimiento
   a si mismo no es un endpoint, es un agujero.
3. **Jamas se guarda el prompt crudo de un tercero sin su firma.** Sin firma
   valida no se escribe nada: no hay ruta que meta texto anonimo en Bronze. El
   par firmado ES el unico formato de entrada.
4. **Cero PII derivada.** No se registra IP, ni User-Agent, ni cabecera de
   idioma, ni marca de tiempo del servidor distinta de la que el par ya trae. Un
   log de acceso que guarde IPs convierte esto en telemetria por la puerta de
   atras, que es exactamente lo que el producto existe para no hacer.

## Topes, y por que existen

- **32 KB por par.** Medido: los pares reales del MVP estan tres ordenes de
  magnitud por debajo. Un tope generoso que igualmente impide que alguien use
  Bronze como almacen.
- **Cola maxima: NO_DATA.** Es **D3**, y D3 es del carbono. Hasta que se firme,
  el endpoint no debe aceptar concurrencia sin limite: se propone `1` en
  serie y que la cola se PUBLIQUE, porque LorAtelier dice que un atelier vende
  proceso y por eso publica la cola. Una cola oculta es una cifra que nadie
  puede reproducir.

## Como se apaga

Una bandera en la configuracion del Agora: `corrections: no` devuelve `503` con
causa declarada. Nada mas. Si hace falta mas de una linea para apagarlo, esta
mal construido.

## Donde encaja en la cadena

```
[2] corregir.js (navegador, firma Ed25519)   ← construido, sin salida de red
[3] POST /api/v1/corrections  → correcciones.jsonl (Bronze)   ← ESTA PROPUESTA
[4] Bronze → Silver (dataset por modelo_base × skill)         ← NO EXISTE
[5] forja/entrenar_lora.py + pruebas/guardian_tester.py (12 edge cases)  ← YA ESCRITO
[6] modelos.json  (derivado de los Modelfile + Ollama)  ← construido
[7] la web ensena el LoRA y sus metricas → vuelve a [1]
```

**CORRECCION (2026-08-31, posterior a la primera version de este documento):**
la primera redaccion decia que `curador.py` era el eslabon [4] y que por tanto
«tres de los siete eslabones ya estaban escritos». **Es falso, y el error es
mio.** `preceptor-internal/agentes/bucles/curador.py` lee `engrams` y `links`:
es higiene de la memoria --duplicados y enlaces rotos--, y no toca ni una
correccion. Comparte nombre con el Curador que `LORATELIER_P0X.md` describe
para el flywheel, y ese parecido fue lo que me confundio.

Lo que SI estaba escrito y desconectado son dos cosas, no tres: el esquema del
par (`preceptor/captura.py`, tabla `turnos`) y la Forja
(`preceptor-lora/forja/entrenar_lora.py` + los 12 edge cases de
`pruebas/guardian_tester.py`).

Asi que faltan DOS piezas entre el navegador y un LoRA, no una: este endpoint,
y un curador de correcciones que no existe todavia. Decirlo importa porque la
version anterior de este documento hacia parecer el camino mas corto de lo que
es.

## Estado de pruebas

| Pieza | Estado |
|---|---|
| `corregir.js` firma y guarda | **PROBADO** por gate (60 passed, 948 subtests) |
| Ausencia de salida de red | **PROBADO** sobre el codigo sin comentarios |
| Verificacion Ed25519 en servidor | **NO PROBADO** · no existe todavia |
| Escritura en Bronze | **NO PROBADO** · no existe todavia |
| Extremo a extremo navegador→fragua | **NO PROBADO** · falta este endpoint |

## Lo que esta propuesta NO autoriza

No autoriza encender el envio en la web. Aunque este endpoint se construya y
funcione, `corregir.js` sigue sin salida de red hasta que D1 y D2 esten
firmadas. Construir la puerta no es abrirla.
