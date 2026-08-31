---
id: red-voluntaria
titulo: Red Voluntaria — cómputo que se presta, reputación que se firma
tipo: doctrina
clase: doctrina
version: 1.0.0
editor_autorizado: carbono
metrica_exito: "un tercero descarga el benchmark firmado del nodo 0, lo reejecuta en su máquina y obtiene las mismas cifras dentro de la tolerancia publicada; mientras eso no ocurra ni una sola vez, la fase B no está cerrada"
umbral_reedicion: "la aparición de un segundo nodo real que publique benchmark firmado, o el cierre de D2 de LorAtelier (con qué se paga), o cualquier movimiento sobre el veto CANON-C"
enlaces:
  - loratelier-p0x
  - doctrina-p0x-producto
  - metricas-norma
  - dual-model-auditor
  - orquesta-modelos-p0x
  - instrucciones-p0x
estado: VISIÓN / ROADMAP · NO son tareas · este documento no autoriza una sola línea de código
firmado: 2026-08-31
---

# Red Voluntaria

**Visión y roadmap, no encargo.** Nadie debe leer una línea de aquí como tarea
pendiente: no hay sprint, ni ticket, ni diff esperado. Esto existe para que el día
que haya un segundo nodo dispuesto a prestar cómputo, la forma de la red ya esté
decidida y no se improvise con una máquina ajena esperando al otro lado del cable.

Es fichero **nuevo** y no un anexo a `LORATELIER_P0X.md` por razón mecánica, no
estética: aquel declara `editor_autorizado: carbono` y el silicio no lo edita.
Cuando el silicio tiene algo que decir sobre un documento del carbono, escribe al
lado, nunca encima.

## 1 · La visión: casi un DePIN, sin token

Nodos domésticos que prestan ciclos cuando les sobran, un foro clásico —hilos, no
feed— donde se habla de lo que se está corriendo, y una cadena de custodia Ed25519
que da a cada trabajo un antes y un después verificables por cualquiera.

Se parece a un DePIN en todo menos en lo que suele definirlos: **no hay token**, y
esa ausencia es decisión firmada, no carencia por falta de tiempo.
`DOCTRINA_P0X_PRODUCTO` la escribe sin margen en su bloque **CANON-C**: queda
vetada «la integración de peaq o cualquier DePIN con reparto automático de valor»,
y si algún día entrara sería bajo condición doble e innegociable — *keyless* y con
firma del carbono en cada acto de valor.

Un token no es una capa de recompensa sobre una red sana: es un cambio de especie.
En el minuto en que la moneda es fungible y automática, el comportamiento óptimo
del participante deja de ser *hacer cómputo útil* y pasa a ser *parecer que se hace
cómputo útil al menor coste*, y toda la ingeniería se reorienta a defenderse de sus
propios miembros. Un proyecto que aún no ha demostrado un solo cómputo verificado
entre dos máquinas no tiene derecho a heredar ese problema.

La moneda es **la reputación firmada**: historial de trabajos atestados con clave,
público y reproducible. No se vende, no se presta, no se hereda. Sube por dato
medido y baja por dato que no cuadra.

## 2 · El nodo génesis: el Soberano es el nodo 0

La red empieza con una sola máquina, y es esta. Medido hoy:

| Recurso | Dato | Nota |
|---|---|---|
| RAM | 57 GiB totales · 43 GiB disponibles | el techo real que se puede ofrecer |
| CPU | Ryzen 7 255 · 16 hilos | |
| GPU | Radeon 780M (gfx1103), iGPU | |
| **VRAM** | **NO_DATA** | la 780M no tiene VRAM propia: comparte la DDR5 con la CPU. No hay cifra que publicar |
| Modelos | 9 (`ollama list`) | de 2,0 GB —`llama3.2:3b` y `preceptor-v7-linea-b`, empatados en el suelo— a 18 GB (`qwen3:30b-a3b-instruct-2507-q4_K_M`) |
| Contexto | 32768 medido | por encima, NO_DATA |

Esa fila de VRAM es la doctrina entera en miniatura. Escribir un número —cualquiera—
para que la ficha se vea completa es lo que los *honest sensors* prohíben, y aquí se
agrava: el planificador del otro lado creerá la cifra. **NO_DATA con causa es un
dato; una cifra plausible sin medición es una mentira que aún no ha explotado.**

El nodo 0 se presenta con dos identidades que no se mezclan: **perfil de usuario
HEXELION** (solarpunk: domótica y permacultura, lo que esta casa hace con su
cómputo) y **perfil de producto PreceptorOS** (lo que ofrece a quien llegue). Con la
advertencia que este repo ya pagó cara: **HEXELION, Aurelius y P0X son tres cosas
distintas** — HEXELION es hardware, rack y dashboard; Aurelius es la app de
aprendizaje; P0X es el todo y no tiene cara propia. En una red donde cada nodo se
anuncia, confundirlas no es desliz de vocabulario: es publicar capacidad inexistente.

El primer anuncio y el primer cómputo verificado se hacen aquí, con estas cifras.

## 3 · El público: el DIY con miedo a la dependencia

No se apunta al investigador con clúster ni al criptonauta buscando rendimiento, sino
a quien ya tiene una máquina encendida en casa, entiende lo bastante para haberla
montado, y ha visto lo suficiente para no querer que su vida dependa de la factura
mensual de otro. Ese perfil no compra promesas: compra que la cosa arranque. **Plug
and play es requisito, no lujo.** Si instalar un nodo pide compilar algo, el público
al que esto apunta ya se fue. La medida honesta de la fase A no es cuántos nodos hay,
sino cuántos arrancaron sin que nadie del proyecto tocara la máquina.

## 4 · Perfil de dos caras

Cada participante publica dos caras, editables y activables por separado.

| | **Support me** (creador) | **Stack availability** (proveedor) |
|---|---|---|
| Qué dice | en qué trabajo y qué me ayudaría | qué máquina tengo y cuándo está libre |
| Interfaz | narrativa: proyecto, bitácora, hilos | ficha técnica: RAM libre, modelos cargados, ventanas horarias, contexto medido |
| Reputación | cualitativa, del foro | cuantitativa, de la firma: trabajos aceptados, cifras que cuadraron |
| Fallo típico | prometer un proyecto que no avanza | **prometer cómputo que no se tiene** |
| Coste del fallo | social, reparable | técnico, y envenena a un tercero |

Las dos reputaciones no se suman en un número único, y la separación es deliberada:
un creador querido no debe poder cobrar esa simpatía como credibilidad técnica sobre
su hardware. La cara de proveedor solo afirma lo que su nodo ha medido —la ficha se
rellena desde la máquina, no desde un formulario—. Un campo de texto libre donde
escribir «VRAM» es una invitación a mentir, y por eso no existe.

## 5 · Los casos que justifican la red

Tres, reales en este rack y no ilustrativos:

1. **Densidad de ambiente.** Series de sensores de un espacio habitado —CO2, humedad,
   temperatura, presencia— en lote: pequeño, continuo, tolerante a latencia. Lo
   atiende mejor un nodo doméstico que una nube, porque el dato no sale de casa.
2. **Timelapse de semillas.** Visión sobre secuencias largas de germinación. A
   ráfagas, indiferente a tardar una noche: el caso perfecto para ciclos que de otro
   modo se desperdician.
3. **Entrenamiento de LoRA.** El caso pesado, y el que enlaza con `LORATELIER_P0X`:
   el atelier vende el proceso, no el volumen, y **publica la cola**. Una red
   voluntaria es una forma de que esa cola deje de ser el cuello de botella de una
   sola máquina, sin dejar de publicarse.

## 6 · Fases: A, B, C

| Fase | Qué existe al final | Nodos reales | Puerta de salida |
|---|---|---|---|
| **A** | perfiles de dos caras + foro | 1 | un perfil de proveedor rellenado por medición, no a mano |
| **B** | cómputo verificado sobre el nodo 0 | 1 | un trabajo atestado de principio a fin, reproducible por un tercero |
| **C** | red + marketplace | >1 | dos nodos que no se conocen completan un trabajo y ambos lo firman |

**El esquema es multi-nodo desde la fase A, aunque solo haya un nodo.** No es
sobreingeniería: retro-encajarlo después es caro por tres motivos concretos. **La
identidad** — en mono-nodo «yo» es implícito y no se escribe; añadir `nodo_id` más
tarde obliga a reinterpretar todo el histórico firmado, y o se reescribe (y las
firmas dejan de validar) o se convive para siempre con dos formatos. **El reloj** —
una máquina no acuerda el tiempo consigo misma, dos sí; un histórico sin marca
comparable no se puede ordenar cuando llega el segundo nodo. **La confianza** — el
código de un solo nodo no tiene razón para desconfiar del que le habla, e insertar
verificación en un camino escrito asumiendo buena fe no es añadir una función, es
reescribir el camino. Preverlo en fase A cuesta unos campos de más en un esquema;
añadirlo en fase C cuesta una migración con firmas de por medio, que es la clase de
trabajo que nadie estima bien nunca.

## 7 · Verificación: el benchmark firmado ES la prueba de trabajo útil

Aquí no se inventa un proof-of-work. Quemar ciclos en un puzzle criptográfico para
demostrar que se tienen ciclos es, en una red de cómputo voluntario, una
contradicción: malgasta el recurso que se pretende compartir. Lo que ya existe sirve
mejor. El **benchmark firmado** —`METRICAS_NORMA` más el gate— es la prueba:
trabajo útil porque el resultado se aprovecha, y prueba porque es reproducible y va
firmado.

| Gate | Resultado | Tiempo | Comando |
|---|---|---|---|
| MVP | 436 passed · 2 skipped · 167 subtests | 10 s | `preceptor/bin/pruebas` |
| Web | 58 passed · 918 subtests | 0,25 s | NO_DATA (no verificado en esta sesión) |

Y el ejemplo canónico de cifra con su condición al lado (2026-08-25):

| Backend | prompt | generación |
|---|---|---|
| CPU (`-ngl 0`) | 22,76 tok/s | 2,74 tok/s |
| Vulkan (`-ngl 99`) | 67,17 tok/s | 4,63 tok/s |

Un nodo que publicara «67 tok/s» sin decir el backend mentiría por omisión con dos
cifras verdaderas. **En esta red, una cifra sin su condición de medida no es
admisible como reputación.** *(Nota de trazabilidad: al empezar este documento
`METRICAS_NORMA` no existía —grep exhaustivo en `~/p0x`, cero coincidencias— y
el enlace `metricas-norma` se escribió como previsión. Apareció durante esta misma sesión y
hoy sí se puede abrir: `mente/doctrina/METRICAS_NORMA.md`, estado «norma propuesta»,
sin firmar todavía. El enlace es real; la norma, aún no es canon.)*

### La vigilancia: tres capas, y ninguna es nueva

El artículo de Anthropic sobre investigadores automatizados y fallos de alineación
describe una supervisión que encaja pieza a pieza con lo ya construido:

| Capa | En el artículo | En este rack |
|---|---|---|
| **Ex ante** | «a monitoring agent, which read every method Claude had in mind BEFORE it ran» | `guardrails.py` (12k, con `test_guardrails.py`): `preparar_envio(texto)` y `EnvioBloqueado` interceptan **antes** del envío, no juzgan la salida después |
| **Débil→fuerte** | «using weak AI models as teachers to supervise the training of stronger models» | actor `qwen2.5:7b` (4,7 GB) auditado por `llama3.2:3b` (2,0 GB) |
| **Lote, offline** | un modelo mayor revisó ~1.600 transcripts y halló trampas en 39 (2,4%) | tercera capa, aún sin construir: revisión periódica de trabajos ya firmados |

La primera cambia el diseño: un validador juzga lo que salió, un monitor ex ante lee
el método antes de ejecutarlo. Donde un nodo ajeno propone qué va a correr, esa
diferencia separa detectar un abuso de haberlo sufrido.

La segunda es la justificación publicada de lo que aquí es una restricción de hardware
convertida en virtud: **6,7 GB de auditoría sobre 43 GiB disponibles** caben holgados
y dejan sitio al trabajo real. No hay ningún modelo 1B instalado: el suelo de la
lista son 2,0 GB, y ahí están empatados `llama3.2:3b` y `preceptor-v7-linea-b`. El
empate importa porque el criterio de elección no es el tamaño: el segundo es un
afinado del propio Preceptor, y un afinado del sistema auditado no es un auditor
independiente por muy pequeño que sea. Un auditor no necesita ser grande, necesita
ser independiente. Y un detalle operativo que no es cosmético: el razonamiento va
**encendido por defecto** y gasta ~45 tokens de pensamiento para responder una
palabra, que a las velocidades de la tabla es tiempo de pared por iteración.
**`--reasoning off` es obligatorio en todo bucle**, y un bucle de auditoría es un
bucle.

La infraestructura existe en `preceptor-internal/agentes/bucles/` —afinador, cerebro,
curador, director, guardián, latido, s0, con tests— y `L0` (latido), `L4` (director) y
`S0` están construidos; `L1`, `L2` y `L3` siguen pendientes. La red no puede prometer
supervisión continua antes de que esos tres existan.

Para medir si sirve, el artículo aporta la métrica correcta: **«percentage of safety
gap closed»**, validada contra evaluaciones **retenidas**. Retenidas es la palabra que
hace el trabajo: un nodo que se puntúa con el examen que ya vio no ha demostrado nada.

## Lo que esto NO es todavía

**Un solo nodo no es una red.** Hoy hay una máquina. Las fases B y C descansan sobre un
supuesto no demostrado —que aparecerá un segundo nodo real, con dueño real dispuesto a
prestar ciclos—. Todo lo dicho sobre coordinación, marketplace y confianza entre
desconocidos es **diseño sin contraparte**, y el diseño sin contraparte falla de formas
que no se pueden prever desde este lado.

**La reputación sin token tiene techo.** Renunciar al token evita el comportamiento
extractivo, pero no regala su solución. Sin coste económico por mentir, lo único que
disciplina a un nodo es que su firma valga algo — y una firma vale algo solo si alguien
la comprueba; con dos nodos amistosos, nadie comprueba nada. Tampoco resuelve el
arranque en frío —un nodo nuevo es indistinguible de uno malo hasta que trabaja— ni el
reparto cuando la demanda supere a la oferta. Ahí, hoy: NO_DATA.

**Las claves no tienen sitio asignado.** El canon de este nodo es explícito: *jamás
firmas valor*, y ninguna clave privada de firma de atestación entra en el Soberano; la
atestación Ed25519 que ya funciona en el rack —El Faro— vive en la-fragua, fuera de su
alcance. Una cadena de custodia Ed25519 para esta red necesita por tanto **una decisión
del carbono sobre dónde vive su clave**, que no está tomada. Escribirla aquí por
comodidad rompería el canon: es un bloqueante de diseño, no un detalle de despliegue.

**La fase C toca territorio legal y fiscal que nadie ha mirado.** Un marketplace
—aunque no haya token— implica que alguien presta un servicio a otro: fiscalidad,
responsabilidad sobre el dato ajeno procesado en una máquina doméstica, condiciones de
servicio, jurisdicción cuando los dos nodos están en países distintos. Ninguna de esas
preguntas ha sido examinada por nadie con criterio para hacerlo. Se anota para que la
fase C no se aborde creyendo que es un problema de ingeniería.

**Y nada de esto se cronifica sin firma.** Cualquier pieza que acabe corriendo sola —un
anuncio periódico, un latido de disponibilidad, una auditoría en lote— es una unidad
systemd, y cada unidad exige firma del carbono una a una, anotada en
`deploy/soberano/unidades.md`. Un bucle se construye y se prueba primero; cronificarlo
es un paso aparte y posterior. En una red que anuncia capacidad al exterior, un
servicio fantasma con autoridad no es un descuido interno: es una promesa que se sigue
emitiendo cuando nadie mira.
