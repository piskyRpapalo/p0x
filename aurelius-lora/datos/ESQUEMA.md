# Esquema del dataset · `data/lora_dataset.jsonl`

Un objeto JSON por línea, UTF-8, sin BOM. **Nada de esto sale de casa (P4).**

## Campos comunes

| Campo | Tipo | Regla |
|---|---|---|
| `id` | str | Único. Formato `<origen>/<idioma>/<clave>`. Es la clave de deduplicado. |
| `clase` | str | `canon` · `preferencia` · `negativo`. |
| `idioma` | str | `en` · `es`. **Nunca mezclados dentro de un registro.** |
| `origen` | str | Fichero del que salió, con su commit. Sin esto un registro es un rumor. |
| `huella` | str | sha256 de los primeros 16 bytes del contenido normalizado. Detecta duplicados que cambiaron de `id`. |
| `peso` | float | 1.0 por defecto. |

## `clase: canon` — la voz del producto (P1 primario)

```json
{"id":"textos/es/charla_cabecera","clase":"canon","idioma":"es",
 "origen":"aurelius@de6577d:textos.py","huella":"…","peso":1.0,
 "mensajes":[{"rol":"persona","contenido":"…"},{"rol":"aurelius","contenido":"…"}],
 "par":"textos/en/charla_cabecera"}
```

`par` apunta al registro paralelo del otro idioma. **P3:** cada clave de
`textos.py` produce **dos** registros, `en` y `es`, y cada uno declara su pareja.
Un registro sin pareja es un fallo del guardián, no un caso aceptable: es
exactamente cómo una de las dos columnas se queda atrás.

## `clase: preferencia` — las correcciones del Soberano (P1 secundario)

```json
{"id":"correccion/es/0007","clase":"preferencia","idioma":"es",
 "origen":"sesion 2026-08-20","huella":"…","peso":2.0,
 "prompt":"…","elegido":"…","rechazado":"…",
 "motivo":"el rechazado usa voseo en una sesion declarada es"}
```

`motivo` es obligatorio y va en castellano. Un par de preferencia sin motivo no
se puede auditar seis meses después, y un dataset que no se puede auditar es
justo lo que este proyecto no firma.

## `clase: negativo` — lo que no se hace

Mismo cuerpo que `preferencia`, con `elegido` vacío: solo se marca la forma a
evitar y por qué.

> ### `NO_DATA` · las tres familias
>
> P1 dice «las tres familias de fallos del sprint como negativos». **La
> enumeración exacta no llegó a esta sesión y no la invento.** Los candidatos
> que sí medí, para que firmes tres (o los sustituyas):
>
> 1. **Registro equivocado** — voseo (*«¿Qué querés saber primero?»*) en una
>    sesión declarada `es`.
> 2. **Cantar verde sin mirar** — `bin/pruebas` dice `VERDE 241/241` viendo 13
>    de 26 suites.
> 3. **Rellenar en vez de declarar** — dar por verificado lo que dijo un
>    tercero (el apéndice del borrador del Preceptor).
>
> Lectura alternativa, por si te referías a los tres fallos de primer arranque
> del commit `de6577d`: el saludo con el texto de cierre · las banderas que
> prometían crear la memoria sin preguntarlo · el idioma preguntado dos veces.
> Son fallos de código, no de voz — sirven peor como negativos de un LoRA.
>
> `construir_dataset.py` deja el hueco declarado y **no rellena ninguno**.

## Lo que el guardián rechaza (Fase 1)

1. `id` duplicado, o `huella` repetida con `id` distinto.
2. Registro `canon` sin `par`, o con `par` que no existe.
3. Desequilibrio EN/ES mayor del 5 % — rompe P3.
4. Cualquier ruta local, IP privada, clave o token en el contenido: se pasa
   `guardrails.py` del producto sobre **cada** registro. El dataset es el alma
   y el alma no lleva dentro la casa.
5. Vocabulario de control del rack (nombres de nodos, proyectos internos):
   misma regla que `LORE.md` §1.
6. Contenido vacío, o más largo que el tope declarado.
