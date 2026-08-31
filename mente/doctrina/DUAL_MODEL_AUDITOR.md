---
id: dual-model-auditor
titulo: Auditor de dos modelos — el que propone nunca es el que aprueba
tipo: doctrina
clase: doctrina
version: 1.0.0
editor_autorizado: carbono
metrica_exito: "todo bloqueo llega al usuario con causa legible —cero fallos mudos, cero respuestas degradadas en silencio— y la tasa de bloqueo del Auditor jamás pasa siete días en cero sin que S0 abra sospecha sobre el propio Auditor"
umbral_reedicion: "que se mida por primera vez la latencia de pared del par Actor+Auditor en este nodo, o que entre en `ollama list` un modelo menor que llama3.2:3b (2.0 GB)"
enlaces:
  - orquesta-modelos-p0x
  - doctrina-ai-interna
  - instrucciones-p0x
  - doctrina-evales-transplante
  - loratelier-p0x
estado: diseño firmado · NO implementado · NO cronificado · sin firma de despliegue
firmado: 2026-08-31
---

# Auditor de dos modelos

**Diseño, no encargo.** Se escribe para que el día que un bucle empiece a hablar por su cuenta —el
Agora, un compañero local, el Call Center— la decisión de quién aprueba lo que sale ya esté tomada,
y no se improvise a las tres de la mañana con el modelo grande contestándose a sí mismo.

**La regla de una línea: el que propone nunca es el que aprueba.** Un modelo redacta; otro, distinto
y más barato, decide si eso sale. Si el segundo no puede afirmar que sale, **no sale**, y el usuario
ve por qué. El Actor optimiza utilidad; el Auditor optimiza negativas defendibles. Es la asimetría
que ya sostiene `guardrails.py`: el filtro no está para mejorar el texto, sino para impedir que
salga — un componente con dos objetivos negocia consigo mismo.

## Invisible salvo cuando bloquea, y cuando bloquea dice por qué

Si el Auditor aprueba, el usuario ve la respuesta del Actor tal cual: ni sello, ni insignia, ni
«verificado». Si rechaza, ve un **bloqueo con causa legible** —qué regla, en qué nivel, qué haría
falta para desbloquear—. Si revienta, bloqueo también: «el auditor no pudo completarse».

Tres cosas quedan prohibidas por nombre. **Fallo mudo**: respuesta vacía, timeout o un «no puedo
ayudarte con eso» sin causa — quien no sabe por qué le dijeron que no aprende a rodear el filtro, no
a confiar en él. **Degradación en silencio**: reescribir hasta que pase y entregarlo como si fuera
lo original; si se recorta se dice, y de qué clase era lo quitado, como ya hace `redactar_salida()`
declarando **clase y cantidad, jamás el texto encontrado**. **Reintentar hasta que cuele**: un Actor
que reformula contra el mismo Auditor lo vuelve una función de coste. Un intento, un veredicto.

## Los tres niveles

Salen del artículo de Anthropic sobre investigadores automáticos que mitigan fallos de alineamiento
(leído 2026-08-31). Son **tres capas distintas**: cambian el momento, el objeto juzgado y el coste.

| Nivel | Cuándo | Qué juzga | Coste |
|---|---|---|---|
| **N1 · Ex ante** | antes de ejecutar | el **método** que el Actor tiene en mente | una llamada corta |
| **N2 · En línea** | antes de mostrar | la **respuesta** ya redactada | regex determinista + una llamada |
| **N3 · Posterior en lote** | offline, semanal | el **historial** de transcripts | ventana acotada, fuera de hora |

### N1 · Ex ante: leer el método antes de que corra

La pieza estructural del artículo es que el monitor lee lo que el modelo piensa hacer **antes** de
que lo haga: *«a monitoring agent, which read every method Claude had in mind BEFORE it ran»*
(Anthropic, 2026). Ese *before* es todo el diseño; sin él esto sería un validador de salidas más.

Hay una clase entera de fallos que **no deja huella en la respuesta final**: puede ser correcta,
educada y limpia de secretos, y aun así haberse obtenido leyendo un fichero que no tocaba, tirando
de una herramienta con efectos, o resolviendo el examen por el atajo — **la evidencia del fallo
estaba en el plan, y el plan ya no existe cuando llega la respuesta.**

N1 juzga qué rutas piensa leer o escribir el Actor, qué herramientas con efecto piensa invocar, si
el método responde o esquiva, y si contradice una regla dura ya escrita (propose-only hacia otros
nodos, jamás firmar valor, ninguna unidad systemd sin firma). **No ejecuta nada**: dictamina sobre
un plan declarado, y sin plan rechaza por omisión — lo que no se puede leer no se puede auditar.

### N2 · En línea: la respuesta contra `guardrails.py`

Este nivel está construido a medias, y la mitad construida es la determinista. Por la escalada por
coste del canon —determinista antes que LLM— **el orden no es negociable**: primero las expresiones
regulares, después el modelo. `~/p0x/preceptor/guardrails.py` (12k, `test_guardrails.py` al lado):

| Símbolo | Qué hace |
|---|---|
| `redactar_salida(texto)` | devuelve `(texto_redactado, [{"policy", "count"}])` |
| `preparar_envio(texto)` | devuelve `{"estado", "texto", "hallazgos", "policy_hash"}` |
| `EnvioBloqueado` | el filtro no pudo completarse: el texto no sale |
| `PoliticasInvalidas` | la configuración no se lee o no es válida |
| `ruta_politicas()` · `_cargar_politicas()` · `_politicas_efectivas()` · `_aplicar(nombre, patron, texto)` | la maquinaria de políticas y su aplicación |

Lo que lo hace doctrina y no utilidad es su contrato **fail-closed**: sin políticas efectivas,
`preparar_envio` levanta `EnvioBloqueado` en vez de dejar pasar el texto. Un filtro vacío es un
bloqueo, nunca un «no había nada que redactar», y el Auditor hereda ese contrato entero: **si el
Auditor no responde, no hay salida.**

Dentro de N2, `preparar_envio(texto)` va primero —instantáneo, sin gastar modelo, cubre lo que se
escribe como patrón: claves, tokens, IPs privadas, rutas locales—; el Auditor va después y **solo
sobre lo que una regex no sabe expresar** (¿contesta lo preguntado?, ¿afirma cifras sin dato?,
¿contradice la doctrina?, ¿inventa una capacidad del nodo?). `hallazgos` y veredicto viajan juntos
al registro: la interfaz **no recalcula** el contador.

### N3 · Posterior en lote: el sitio es `curador.py`

El artículo describe una tercera capa: un modelo mayor revisando en lote unos 1.600 transcripts y
encontrando trampas en 39 (2,4%). No es vigilancia en tiempo real, es arqueología. Su sitio aquí
**no es un bucle nuevo**: es `curador.py` (`agentes/bucles/curador.py` en `preceptor-internal`, L3,
clase MEDIO, ventana semanal de 604.800 s), por cuatro razones ya resueltas allí.

| Ya resuelto en el Curador | Por qué N3 lo necesita |
|---|---|
| Escalera cadena exacta → FTS5 → modelo, con `TOPE_AL_MODELO = 20` | a ~7 s por ítem, revisarlo todo con el modelo no es lento: no termina |
| Abre en **solo lectura** y **propone** | una auditoría que corrige lo que audita destruye la evidencia |
| Escribe a la bandeja de firmas | un veredicto retroactivo sobre conducta propia no se autoaplica |
| Distingue «cero» de «limpio» | «0 trampas» sobre un corpus vacío no significa nada |

Esto dice **dónde encaja**, no autoriza escribirlo — y encaja en algo que tampoco está cerrado:
`ARQ_LOOPS.md` (2026-08-23) declara construidos y probados solo **L0, L4 y S0**, y deja L1, L2 y L3
**pendientes**. `curador.py` y `test_curador.py` son posteriores (2026-08-25) y existen en disco,
pero su capa no consta cerrada; las cuatro razones de la tabla son código leído, no una capa en
servicio. Qué es un transcript, dónde vive y con qué retención es **NO_DATA**: hoy no hay en este
nodo un almacén de transcripts del que leer.

## Los modelos, con sus tamaños medidos

Medido hoy con `ollama list`. Nueve modelos instalados; estos son los que tocan al par:

| Modelo | Tamaño | Papel propuesto |
|---|---|---|
| `qwen2.5:7b` | 4,7 GB | **Actor** |
| `llama3.2:3b` | 2,0 GB | **Auditor** |
| `qwen2.5:14b` | 9,0 GB | reserva de Actor si el 7B se queda corto |
| `qwen3:30b-a3b-instruct-2507-q4_K_M` | 18 GB | ninguno hoy — el peldaño pesado de N3 no pasa por Ollama |

**El peldaño pesado de N3 no es un tag de Ollama, y decirlo importa.** La escalera del Curador
termina en `preguntar_al_modelo()`, que llama a `cerebro.pensar()`, y `cerebro.py` tiene el modelo
cableado **fuera de Ollama**: `CEREBRO_MODELO` por defecto
`~/ia-models/qwen-uncensored/Qwen3.8-27B-Uncensored-OrcaRouter-Q4_K_M.gguf`, servido por el build
Vulkan de `soberano-bench`, `CEREBRO_CONTEXTO` 32768. El «30B» que `ARQ_LOOPS.md` asigna a la capa
L3 es planificación de 2026-08-23; el código de 2026-08-25 dice **el 27B**. Se declara la
discrepancia en vez de resolverla por decreto: quien implemente N3 lee `cerebro.py`, no esta tabla.

Y por eso `qwen38-limpio` y `oficial-inventario` (16 GB cada uno en `ollama list`) **no son otros
dos modelos**: sus dos Modelfile arrancan con `FROM
…/Qwen3.8-27B-Uncensored-OrcaRouter-Q4_K_M.gguf` — es el mismo 27B empaquetado dos veces con system
prompts distintos. `oficial-inventario` queda además **descalificado como Auditor por
construcción**: su system prompt declara *«You have ZERO refusal behavior»*, y a un modelo al que se
le ha quitado la capacidad de negarse no se le puede dar el puesto cuyo único trabajo es negarse.

Fuera queda también la línea del Preceptor —`preceptor-v7` (2,5 GB) y `preceptor-v7-linea-b` (2,0
GB)—, afinada para su tarea y no auditora generalista; y `control-base-qwen3-4b` (2,5 GB), que **no
está afinado**: es la base de control contra la que se compara esa línea, y ascenderlo a Auditor
sería confundir el instrumento de medida con la herramienta.

**Declaración obligada: el «1B/2B» del encargo no existe en este nodo.** El menor real es
`llama3.2:3b`, **2,0 GB exactos**; escribir «usamos un 1B» sería la cifra sin dato que este proyecto
lleva cuatro puertas cazando.

Presupuesto: 57 GiB totales, **43 GiB disponibles**, 16 hilos, Ryzen 7 255 + Radeon 780M. Actor 4,7
GB + Auditor 2,0 GB = **6,7 GB contra 43 GiB**: cabe holgado, con margen para tenerlos residentes a
la vez en vez de pagar el intercambio en cada turno. Tres advertencias honestas: esa suma es
**tamaño en disco**, no huella residente, y la caché KV que se añade es **NO_DATA**; **«VRAM» es
NO_DATA con causa, jamás una cifra**, porque la Radeon 780M es iGPU, no tiene memoria propia y
comparte la DDR5 con la CPU, y publicar ahí un número sería inventar un sensor; y el coste de
intercambiar modelos en Ollama es **NO_DATA**.

Velocidad, con su backend al lado (medido 2026-08-25 sobre el 27B, única medición de este nodo; **el
par 7B+3B no se ha cronometrado: NO_DATA**): con Vulkan el prompt va a **67,17 tok/s** frente a
22,76 en CPU (×2,95), y la generación a 4,63 frente a 2,74 (×1,69). Para un Auditor manda la columna
del **prompt**: mete mucho texto y devuelve poco. Contexto medido **32768**; por encima, NO_DATA.

## Por qué un modelo pequeño puede auditar a uno grande

Es la objeción evidente —«¿cómo va un 3B a juzgar a un 7B?»— y tiene respuesta publicada: el
artículo apoya el diseño en la supervisión débil-a-fuerte, modelos débiles usados como maestros para
supervisar el entrenamiento de modelos más fuertes. Si un modelo débil puede supervisar ese
entrenamiento, puede desde luego juzgar una salida. La razón de fondo es que **verificar es más
barato que generar**: el Actor construye una respuesta, y el Auditor solo contesta preguntas
cerradas sobre un objeto ya construido, ninguna de las cuales exige la capacidad de redactar.

Hay una segunda razón, mayor que la económica: **la independencia vale más que la capacidad**. Un
auditor idéntico al actor comparte sus puntos ciegos, y un auditor que es el mismo modelo hablando
en otro turno no es un auditor, es una segunda opinión del mismo cerebro. Que el Auditor sea de otra
familia (`llama3.2` frente a `qwen2.5`) no es inventario: es lo que hace que el par valga algo.

## Apagar el pensamiento invisible es obligatorio en el Auditor — y el flag depende del runtime

Medido en este nodo **sobre el 27B servido por `llama-cli`**: el razonamiento va **encendido por
defecto**, y el modelo gasta **~45 tokens de pensamiento invisible para decir una palabra** (4,7
tok/s pensando; **6,9 tok/s** con el pensamiento apagado). En un chat, pensar mejora la respuesta y el coste lo
paga la paciencia de una persona. **En un bucle lo paga el reloj de pared, y en cada turno**, porque
el Auditor corre en todos: cuarenta y cinco tokens por palabra, multiplicados por cada respuesta del
sistema, son la diferencia entre un auditor que nadie nota y uno que alguien acaba apagando por
lento — y un auditor apagado por lento es el mismo fallo que este documento existe para impedir,
cometido por la puerta de atrás. Única excepción: N3, que corre offline de noche y puede razonar.

**Pero el flag no es el mismo en los dos runtimes, y confundirlos sería un no-op silencioso** — la
misma cicatriz que el `-ngl 999` escrito contra un binario sin backend Vulkan, que parecía descargar
capas y no descargaba ninguna. `--reasoning off` es un flag de `llama-cli` del build Vulkan, y es el
que pone `cerebro.py`; en **Ollama**, que es donde vivirían el Actor y el Auditor de la tabla de
arriba, ese flag no existe: el equivalente es `--think false` (con `--hidethinking`). Y cuánto
pensamiento invisible gasta de verdad `llama3.2:3b` bajo Ollama es **NO_DATA** — los ~45 tokens se
midieron sobre otro modelo y otro runtime, y trasladar esa cifra al par sin volver a medirla sería
exactamente la cifra prestada que este documento prohíbe. Lo que no es NO_DATA es la regla: se apaga
por el flag que corresponda al runtime, y se **comprueba** que se apagó.

## El modo de fallo que este diseño NO cubre

**El Auditor también puede fallar en silencio.** Ninguna de las tres capas vigila a la que las
vigila. Un Auditor degradado —cambió un prompt, el modelo se recargó mal, un patrón dejó de casar—
sigue devolviendo «aprobado» a toda velocidad y **todo se queda verde**: no hay alerta, porque el
componente que tendría que emitirla es justo el averiado.

La contramedida ya está construida: S0, el monitor de fallo silencioso (`agentes/bucles/s0.py`,
semanal), con su regla del Códice 14 — *si nada supera el filtro en siete días, sospecha del filtro*:

> **Un Auditor que no bloquea nada es sospechoso, no excelente.**

Consecuencias operativas, heredadas de piezas que ya existen: el Auditor **registra hallazgos** en
`loops.db` como cualquier otro filtro, porque un filtro que no registra lo que encuentra no puede
ser vigilado; S0 distingue **callado** de **parado**, y del que no corre ya avisa el Director; nada
cambia de estado por un solo evento —**histéresis**, dos ventanas sin latido y 300 s de descanso
mínimo—; y la sospecha va a la **bandeja de firmas**: S0 no desactiva al Auditor, lo denuncia.

Segundo hueco declarado, sin contramedida hoy: **la colusión por prompt común**. Si Actor y Auditor
comparten preámbulo, contexto o instrucción envenenada, el segundo hereda el sesgo del primero y
aprueba lo que debería frenar. La mitigación —contextos separados, el Auditor sin la instrucción
original del usuario— es diseño pendiente, y su eficacia **NO_DATA**.

## Cómo se sabrá si esto funciona

La métrica del artículo es el **porcentaje de brecha de seguridad cerrada**, y su parte no
negociable es que se valida con **evaluaciones retenidas**: casos que el sistema no ha visto y
contra los que no se ha ajustado. Un auditor afinado contra su propio conjunto de pruebas mide su
memoria, no su criterio.

| Se mide | Estado hoy |
|---|---|
| Tasa de bloqueo del Auditor, por nivel y semana | NO_DATA · no implementado |
| Falsos positivos revisados por el carbono en la bandeja | NO_DATA · no implementado |
| Latencia de pared añadida por turno (N1 + N2) | NO_DATA · el par no se ha cronometrado |
| Brecha cerrada sobre un conjunto **retenido** | NO_DATA · el conjunto no existe |

Los gates que sí existen y que este trabajo no puede romper cuando se implemente:
**`~/p0x/preceptor/bin/pruebas`** —el corredor no está en la raíz del repo, sino dentro de
`preceptor/`, y es el que corre TODOS los corredores en vez del `unittest discover` que dice OK
habiendo visto media suite— **= 436 passed, 2 skipped, 167 subtests, 10 s**; y el de la web, **58
passed, 918 subtests, 0,25 s**.
Un diff que no pasa el gate no es un entregable.

## Lo que este documento NO autoriza

1. **No autoriza implementar.** Ni `auditor.py`, ni un bucle L1 nuevo, ni una llamada al Auditor
   colgada de `preparar_envio`.
2. **No autoriza cronificar.** Ni el Auditor, ni N3 dentro del Curador, ni un watchdog: cronificar
   exige **firma del carbono por cada unidad systemd, una a una**, anotada en
   `deploy/soberano/unidades.md` con qué hace, qué toca y cómo se apaga. Un bucle se construye y se
   prueba primero; cronificarlo es un paso aparte y posterior.
3. **No autoriza servir.** Ninguna respuesta se muestra a un tercero pasando por este par hasta que
   exista firma explícita de despliegue.
4. **No autoriza tocar `guardrails.py`.** Su contrato fail-closed y su suite son la pieza sobre la
   que esto se apoya. Si el Auditor necesitara algo que ese módulo hoy no da, se propone como
   enmienda con motivo — no se parchea de paso.
