---
id: metricas-norma
titulo: La Norma de Métricas — un solo esquema para la web y para la app
tipo: doctrina
clase: doctrina
version: 1.0.0
editor_autorizado: carbono
metrica_exito: "cero cifra publicada (web o app) que no sea reproducible por su campo `como`; cero campo relleno con 0 cuando el estado real es NO_DATA; los dos paquetes comparables se diferencian solo en hardware, nunca en normas"
umbral_reedicion: "que se mida un `num_ctx` distinto de 32768 en este nodo, que aparezca hardware con VRAM dedicada en el rack, o que se cierre D2 de LorAtelier (qué se paga con datos firmados)"
enlaces:
  - loratelier-p0x
  - doctrina-p0x-producto
  - orquesta-modelos-p0x
  - instrucciones-p0x
estado: norma propuesta · el esquema es canon en cuanto el carbono lo firme; ninguna implementación depende todavía de él
firmado: 2026-08-31
---

# La Norma de Métricas

**Qué es esto.** Un esquema único de once campos que la web y la app rellenan
igual, para que dos personas con dos máquinas distintas pongan sus números al
lado y la comparación signifique algo. No es un formato nuevo: es el que
`counters.json` ya usa, extendido a inferencia y declarado norma.

**Por qué ahora.** El 2026-08-30 las tres portadas anunciaban «526 pruebas en
verde» y ningún comando daba 526. `bin/coherencia-publica.py` existe por eso, y
su lección está en su cabecera: *no se arregla escribiendo el número bueno a
mano, porque a mano vuelve a derivar*. Se arregla convirtiendo la cifra en una
medición. Esta norma extiende esa cirugía a todo lo que el producto vaya a decir
de sí mismo.

## Regla cero: el esquema que hay sirve, y no se inventa otro

**Dónde vive cada cosa, porque son dos repos.** Todo lo que este documento cita
como `counters.json`, `contadores.py`, `meter.js`, `chat.js` y `auth.js` está en
**`~/preceptoros-web/`** (los tres últimos bajo `public/assets/`), no en `~/p0x`.
Solo `bin/coherencia-publica.py` y `preceptor/guardrails.py` son de `~/p0x`. La
medición cruza repos a propósito y la comprobación es local a cada uno; quien
implemente esta norma tiene que saberlo antes de buscar un fichero donde no está.

`~/preceptoros-web/public/counters.json` publica hoy nueve métricas con esta
forma exacta:

```
{ "clave": …, "estado": "MEDIDO", "valor": …, "unidad": …, "como":  … }
{ "clave": …, "estado": "NO_DATA", "valor": null, "unidad": …, "causa": … }
```

Cinco claves, dos estados, y la asimetría deliberada: `como` cuando hay medición
(cómo reproducirla), `causa` cuando no la hay (por qué no). **Esta norma
reutiliza ese esquema tal cual.** No añade estados, no añade claves, no renombra
nada: un campo de inferencia es una entrada más del mismo array `metricas`, con
el mismo sobre exterior (`esquema`, `fecha`, `ultima_lectura`, `nota`). Decirlo
explícito importa porque el impulso al escribir doctrina es diseñar un formato
propio y bonito — que sería un segundo formato que mantener, dos validadores, y
el día que divergieran la web publicando una cosa y la app otra: literalmente el
fallo del que venimos. La regla que gobierna el relleno también es prestada, la
de `contadores.py` palabra por palabra: *«Nunca un 0 decorativo — un cero que en
realidad significa "no lo sé" es la mentira más barata que hay»*. Con su
corolario en `coherencia-publica.py`: un gate en rojo **no publica cifra**.

## Los once campos

| campo | unidad | estado | fuente exacta |
|---|---|---|---|
| `modelo_nombre` | texto | MEDIBLE | `ollama list`, columna NAME, **tag completo**. Nunca pelado: el canon del nodo prohíbe `modelo:latest` porque apunta a variantes Thinking con razonamiento no desactivable. En el nodo hay 9 modelos, p.ej. `qwen3:30b-a3b-instruct-2507-q4_K_M` |
| `modelo_base` | texto | MEDIBLE · **obligatorio** | El `FROM` del Modelfile del adaptador, o el nombre del modelo del que se derivó. Ver sección propia |
| `modelo_tamano_gb` | GB | MEDIBLE | `ollama list`, columna SIZE. Medido hoy: `qwen2.5:14b` 9.0 · `preceptor-v7-linea-b` 2.0 · `control-base-qwen3-4b` 2.5 · `preceptor-v7` 2.5 · `qwen2.5:7b` 4.7 · `llama3.2:3b` 2.0 · `qwen38-limpio` 16 · `oficial-inventario` 16 · `qwen3:30b-a3b-instruct-2507-q4_K_M` 18 |
| `consumo_ram_mb` | MiB | MEDIBLE | RSS del proceso runner con el modelo **cargado**, no el tamaño del fichero. `ollama ps` para identificar el runner, `VmRSS` de `/proc/<pid>/status` para la cifra. En este hardware absorbe lo que en otro sería VRAM (ver `vram_mb`) |
| `tokens_sesion` | tokens | MEDIBLE · **norma fija** | Contador del bucle, acumulado sobre los turnos de la sesión. El valor de la norma se declara en el paquete; ver sección propia |
| `ventana_contexto` | tokens | MEDIBLE · **norma fija** | El `num_ctx` realmente pasado al runtime, no el que declara la ficha del modelo. En este nodo, **32768 medido** (2026-08-25, `-c 32768` con `-ngl 99` carga y responde). Por encima: NO_DATA |
| `tokens_por_segundo` | tokens/s | MEDIBLE **si el motor declara tokens** | Web: `meter.js`, `d.tokens / (d.ms / 1000)` del evento `preceptor:turno`. App/bench: `llama-bench -p 128 -n 32 -r 1` (las tres banderas, tal como se midió el 2026-08-25: cambiar `-r` cambia la cifra), dos cifras separadas (prompt y generación), nunca promediadas |
| `latencia_primer_token_ms` | ms | MEDIBLE · NO_DATA si no hubo trozo | `chat.js`: `ttft = t1 - t0`, con `t1` puesto en el primer chunk. Si el motor no emitió ninguno, `ttft` es `null` y `meter.js` lo declara — no lo convierte en cero |
| `temp_cpu_c` | grados C | MEDIBLE | `/sys/class/hwmon/<h>/temp1_input` del hwmon cuyo `name` es `k10temp` (milésimas de grado; dividir entre 1000). **Se busca por `name`, jamás por índice**: hoy es `hwmon3`, y esa numeración no es estable entre arranques |
| `vram_mb` | MiB | **NO_DATA siempre en este hardware** | Ver sección propia. El hueco existe; el valor no |
| `duracion_ms` | ms | MEDIBLE | `chat.js`: `ms = performance.now() - t0`, emitido en `preceptor:turno` junto a `ttft`, `tokens` y `via` |

Cuatro campos ya viajan hoy en el evento `preceptor:turno` (`ttft`, `ms`,
`tokens`, `via`). El resto son huecos declarados: existen en el esquema antes
que en el código, para que nadie improvise nombre ni unidad al rellenarlos.

## `tokens_sesion` y `ventana_contexto` son NORMAS FIJAS

Los otros nueve campos describen **lo que pasó**. Estos dos describen **bajo qué
condiciones se dejó que pasara**, y por eso se fijan antes de medir en vez de
leerse después. Un tok/s sin ventana declarada no es un dato: es una
anécdota. Con `num_ctx` de
2048 el mismo modelo en la misma máquina va más rápido que con 32768 porque hace
menos trabajo; si una persona corrió a 2048 y otra a 32768, la tabla comparativa
miente aunque ambas hayan medido honestamente. Igual con `tokens_sesion`: una
sesión de 200 tokens no llegó a llenar la ventana; una de 20.000 arrastra todo
el historial en cada turno y paga por él.

**La norma, entonces:** un paquete declara sus dos valores fijos *antes* de la
corrida, y solo son comparables entre sí los que declaran los mismos dos. No hay
normalización posterior ni «ajustado a»: normas distintas, tablas distintas. En
este nodo la única ventana con derecho a norma es **32768**, porque es la única
medida. El modelo declara 262K; eso es su ficha, no el techo de esta máquina, y
el canon ya avisa de que ese default cuelga runtimes de este tamaño. Subirla
exige volver a medir, no suponer.

Misma familia: `--reasoning off` es obligatorio en todo bucle que produzca
métricas. Con el razonamiento encendido —el default— el modelo gastó ~45 tokens
de pensamiento invisible para responder «listo». Dos paquetes que difieran en
eso no son comparables, y el apagado parece mejor motor cuando solo es mejor
configuración. Si un paquete no declara el estado del razonamiento, **su
`tokens_por_segundo` es NO_DATA**, no un número con asterisco.

## `modelo_base` es obligatorio, y no es burocracia

Un LoRA no es un modelo: es una diferencia. Y este nodo ya tiene el caso sobre
el disco, medido hoy con `ollama show --modelfile`, no como hipótesis:

| modelo | `ADAPTER` | blob del `FROM` |
|---|---|---|
| `preceptor-v7` (2.5 GB) | sí | `sha256-bbfa887855d5` |
| `preceptor-v7-linea-b` (2.0 GB) | sí | `sha256-dde5aa3fc5ff` |
| `control-base-qwen3-4b` (2.5 GB) | **no** | `sha256-bbfa887855d5` |

Léase despacio. Los dos adaptadores llevan el mismo apellido —`preceptor-v7`— y
**no comparten base**: son blobs distintos. Y `control-base-qwen3-4b` no tiene
adaptador ninguno y arranca del **mismo blob exacto** que `preceptor-v7`: por eso
es su control legítimo, y solo el suyo. Poner el tok/s de esas dos «líneas» en la
misma tabla y llamarlo «comparar dos LoRAs» sería comparar dos cosas distintas y
darles el mismo nombre — con el agravante de que el nombre invita a hacerlo.
Sin `modelo_base`, el flywheel de LorAtelier —BRONZE → SILVER →
GOLD— no puede decidir nada: la doble puerta (doctrina + aceptación del usuario)
juzgaría como mejoras lo que son cambios de base. Por eso el campo no admite
vacío: si no se sabe cuál fue, el paquete entero sale NO_DATA con causa `base
desconocida`, jamás con el campo en blanco.

## `vram_mb`: NO_DATA con causa, siempre, en este hardware

La Radeon 780M (gfx1103) es una **iGPU**. No tiene memoria propia: comparte la
DDR5 con la CPU. No hay cifra de VRAM que leer porque no hay VRAM que medir —
hay una única piscina de 57 GiB (43 GiB disponibles hoy) que CPU y GPU se
reparten. De ahí las dos decisiones:

1. **El campo se declara igual.** El hueco tiene que existir, o el día que entre
   hardware con VRAM dedicada alguien le inventará otro nombre y los paquetes
   viejos y nuevos dejarán de casar.
2. **Se rellena NO_DATA con causa,** literalmente: *«iGPU Radeon 780M sin memoria
   dedicada: comparte la DDR5 con la CPU. No hay VRAM que medir; el consumo real
   está en `consumo_ram_mb`»*.

Escribir `0` sería el «cero decorativo» que `contadores.py` prohíbe en su primer
párrafo: un «no lo sé» disfrazado de lectura, y aquí peor que en la web, porque
un 0 de VRAM se lee como «este modelo no usa GPU» — falso: Vulkan sí la usa y se
nota (prompt 67,17 tok/s contra 22,76 en CPU pura, ×2,95; generación 4,63 contra
2,74, ×1,69). Aviso para quien lo implemente: **sí existe** un hwmon `amdgpu`
con `temp1_input`. Da la temperatura de la iGPU, y no da su memoria. Que un
sensor exista no convierte en medible una propiedad que el hardware no tiene —
la misma trampa que ya costó cuatro rojos falsos en el rack.

## La firma del paquete, y por qué el envío es otra puerta

Un paquete se firma **Ed25519** con el mismo trato que ya usa
`public/assets/auth.js`: clave privada no exportable en IndexedDB como
`CryptoKey`, y firma sobre el **JSON canónico** del objeto — mismo objeto, misma
firma. Va entera: 64 bytes, 128 caracteres hexadecimales, prefijo `ed25519:` y
algoritmo declarado al lado. Ese fichero lleva su cicatriz escrita: hubo una
versión que calculaba los 64 bytes y tiraba 48, mostrando 16 caracteres y unos
puntos suspensivos. Parecía una firma. **Una firma recortada es un adorno con
nombre de garantía.** Y la separación que sostiene todo lo demás:

| | Qué es | Quién la abre |
|---|---|---|
| **Puerta 1 · medir** | Leer sensores y escribir el paquete, en local | El bucle, solo |
| **Puerta 2 · firmar** | Sellar el paquete con la clave del usuario | El usuario, con su llave |
| **Puerta 3 · enviar** | Que el paquete salga de la máquina | El usuario, **cada vez** |

Medir no es enviar. Un paquete firmado y nunca enviado es perfectamente válido:
sirve para compararse contra uno mismo, la mayoría del uso real. El envío es
**siempre opcional** y **siempre otra puerta**, porque el producto se vende sobre
esa distinción y no puede desmentirla en su propia telemetría. Cuando se abra la
puerta 3, el paquete pasa por `guardrails.py` (ya en
`~/p0x/preceptor/`), que redacta claves, tokens, IPs privadas y rutas locales.
La interfaz real es `preparar_envio(texto)` sobre `redactar_salida(texto)`, con
`EnvioBloqueado` como contrato duro —si el filtro no puede completarse, **no hay
envío**; un fallo jamás se lee como «no había nada que redactar»— y
`PoliticasInvalidas` para la configuración ilegible. Un `consumo_ram_mb` es
inofensivo, pero el `como` que lo acompaña puede traer una ruta de casa: por eso
pasa por el filtro el paquete entero, no solo sus valores.

## El benchmark firmado ya es prueba de trabajo útil

No hace falta inventar un proof-of-work: un paquete firmado **es uno**, y mejor
que el criptográfico clásico.

| | Proof-of-work clásico | Benchmark firmado |
|---|---|---|
| El trabajo | hash sin significado | inferencia real que alguien quería de todos modos |
| Qué prueba | que se gastó electricidad | que ese modelo corrió a esa velocidad en ese hardware |
| Verificable por | repetir el hash | repetir la corrida con las mismas normas |
| Residuo | ninguno | una fila de una tabla comparativa que sirve a terceros |

La corrida cuesta lo que cuesta —a 4,63 tok/s de generación el tiempo de pared
es real y no se falsifica gratis— y la reproduce cualquiera con el mismo
hardware y las mismas dos normas fijas. Falsificar un paquete exige o la clave
privada del usuario, o poseer de verdad una máquina que dé esos números: en el
segundo caso el paquete es correcto, que es justo lo que se quería. Es lo que
hace creíble el Benchmark público del Agora, y ya lo dice la cabecera de
`meter.js`: *las cifras de la tabla salen de gente que midió, no de una ficha
técnica*.

## Lo que esta norma NO decide

- **Qué se hace con un paquete enviado.** Depende de D2 de LorAtelier (¿se paga
  con dinero, con datos firmados, o ambos?). Mientras D2 siga abierta, la puerta
  3 no se construye: pedir datos sin saber qué se hará con ellos es justo lo que
  LorAtelier prohíbe.
- **Umbrales de aceptación.** Aquí se dice cómo se mide, no qué es «bueno». Un
  umbral es decisión de producto y lo firma el carbono.
- **Cronificar la recogida.** Un recolector periódico es una unidad systemd:
  exige firma del carbono **por cada unidad**, una a una, anotada en
  `deploy/soberano/unidades.md`. Se construye y se prueba primero; cronificar es
  un paso aparte y posterior.
- **Cifras que no tengo.** `temp_cpu_c` en carga sostenida, `consumo_ram_mb` de
  cada uno de los 9 modelos, y cualquier `ventana_contexto` por encima de 32768:
  **NO_DATA**, causa `no medido todavía en este nodo`.
