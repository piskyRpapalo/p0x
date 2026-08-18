---
id: modulo-proyecto-personal
titulo: "Módulo de proyecto personal · joyas recopiladas y método"
tipo: operativo
clase: doctrina
version: 1.0.0
sistema: MVP
estado: PROPUESTA · pendiente de firma
scopes: P1 infra · P2 producto · P3 preceptor (ausente) · D doctrina
actualizado: 2026-08-18
---

# MÓDULO DE PROYECTO PERSONAL
### Las joyas del árbol, y el método que sale de ellas. Propuesta, no canon.

**Regla de scope (R8-R11).** Cada joya lleva etiqueta y cada sección declara la suya.
`P1` es infraestructura del Soberano y **no viaja al producto**. `P2` es el producto
descargable. `P3` es el Preceptor de la Beelink, que **no existe**: todo el módulo funciona
sin él. `D` es doctrina compartida: se cita, no se implementa sola.

**Antes de la primera tabla, el hallazgo que manda sobre todo lo demás:** la pedagogía real
de este árbol **no es la que pedía el encargo**. Piaget, Papert, ZPD, currículum en espiral,
construccionismo y «objetos para pensar con» tienen **cero apariciones** en todo el árbol
(`mente/`, `Cuarentena/`, `codice*/`, `aurelius-mvp/`). Lo que sí existe, medido y con cita
académica, es otro cuadro: Sweller, Kapur, Wood/Bruner/Ross y Roediger/Karpicke, en
`config/teaching_kernel.yaml`. El módulo se construye sobre lo que hay.

---

# PARTE 1 · RECOPILACIÓN DE JOYAS

## 1.1 · Pedagogía del aprendizaje

| Nombre | Fuente | Técnica | Aporte al usuario | Alineación solarpunk |
|---|---|---|---|---|
| **Ensayo en seco obligatorio** `D` | `config/teaching_kernel.yaml` · Sweller 1988 (Cognitive Load Theory) | Toda operación de escritura, borrado o flasheo **exige** simulación determinista previa. Regla de estado, no de estilo | Convierte el pánico de lo irreversible en esquema: se ve el efecto antes de pagarlo | **La latencia es el fusible**: el tiempo de pensar es obligatorio, no opcional |
| **El fallo como ramificación** `D` | `teaching_kernel.yaml` · Kapur 2008 (Productive Failure) | Un error **jamás** se presenta como estado terminal binario: se presenta como vector de diagnóstico con siguiente paso accionable | El aprendiz falla y sigue teniendo camino; el fallo enseña más que la instrucción directa | **La cicatriz no miente**: el fallo se registra y se usa, no se esconde |
| **Ancla del objetivo macro** `D` | `teaching_kernel.yaml` · Sweller/Chandler (Transient Information Effect) | El objetivo macro permanece **visible** toda la sesión: la información que desaparece no construye esquema | El usuario no pierde el norte de su proyecto entre turnos | **Local antes que global**: el norte es suyo y está a la vista |
| **Andamiaje que decae** `D`+`P2` | `teaching_kernel.yaml` · Wood, Bruner & Ross 1976; Roediger & Karpicke 2006; Collins/Brown/Newman | La verbosidad de la ayuda decae inversamente a la competencia **demostrada**, no declarada | La ayuda que no decae cría dependencia, no soberanía | **El andamiaje se retira**: el aprendiz queda solo, por diseño |
| **Los tres principios** `D` | `mente/esferas/aprendizaje.md` | Recuperación (revisión activa), espaciado (repetición distribuida), carga cognitiva (no saturar) | El método de estudio del propio proyecto | Único dominio marcado «enseña a otros» en el Códice |
| **Regla de procedencia del corpus** `D` | `mente/corpus/_INDICE.md` | Ningún principio entra sin `fuente` y `evidencia_fuerza`; enum: `meta_analisis`, `estudio_unico`, `heuristica_campo`, `n1_personal` | Enseña a distinguir una corazonada de un meta-análisis | **El aprendiz es soberano**: sabe de dónde viene lo que le enseñan |

## 1.2 · Metodología de proyectos

| Nombre | Fuente | Técnica | Aporte | Alineación |
|---|---|---|---|---|
| **Orden de trabajo innegociable** `D` | `Cuarentena/02_CANON_OPERATIVO.md` §4 | 0 verificar · 1 barrido · 2 estructura · 3 conectar lo que YA funciona · 4 arreglar lo roto · 5 pulido solo con orden. **No se abre frente nuevo si hay uno roto bloqueando valor real** | Le da un orden que no depende de su ánimo | **El juego es edificar**: se construye sobre lo que ya sostiene |
| **Heurística de prioridad** `D` | `02_CANON_OPERATIVO.md` §4 | *Qué, cerrado, desbloquea más con menos construcción.* No se prioriza lo bonito ni lo interesante | Le quita la parálisis de por dónde empezar | Edificar, no decorar |
| **Los cuatro principios operables** `P1` | `Cuarentena/MAPA_EVOLUTIVO_P0X.md` §3 (F2) | Guiar al esquema · retrieval de lo suyo · gestión de recursos · **cerrar cada sesión con un paso pequeño siguiente**. Declarado **STUB honesto**: «la mecánica se deriva, no se decreta» | Formato de sesión que no promete más de lo que hay | Declarar el andamio provisional es honestidad, no debilidad |
| **El patrón mini-códice** `P1` | `MAPA_EVOLUTIVO_P0X.md` §3 | Al cierre, se propone un **delta** («hoy avanzaste X, decidiste Y, queda Z») que el usuario **aprueba o corrige** | Cierra el lazo sin robarle la autoría | **El aprendiz promueve sus propias propuestas** |
| **Runbook como entregable** `P1` | `mente/manual/REENCARNACION_P0X.md` | Reconstruir desde cero con lo que existe HOY; métrica dura de tiempo; lo no cubierto se declara | Enseña a escribir para su yo futuro | Local, reproducible, sin depender de nadie |
| **Cuatro categorías deterministas** `P2` | `Cuarentena/aurelius-clasificacion-ideas.md` | Clasifica ideas por viabilidad física, madurez, dependencia de red y coherencia doctrinal | Roadmap honesto: lo descartado se descarta **con razón escrita** | No se promete lo que el silicio no da |
| **SDD · spec → plan → milestones** `P2` (referencia) | `Cuarentena/SDD_TRANSCRIPCION_EXTERNA.md` | Definir qué y cómo antes del código; plan derivado; metas divisibles | Vocabulario para ordenar un proyecto propio | **Se cita, no se obedece**: `EXTERNO_NO_VERIFICADO` |

## 1.3 · Filosofía solarpunk

| Nombre | Fuente | Técnica | Aporte | Alineación |
|---|---|---|---|---|
| **El silicio propone, el carbono firma** `D` | `codice-emancipacion-atomica/CODICE.md` + `README.md` | La latencia, la criptografía y el air-gap forman un muro termodinámico. No hay umbral de omisión ni cláusula de emergencia | El usuario nunca deja de ser el autor de su proyecto | **La latencia es el fusible**, literal |
| **Sensores honestos** `D` | `codice-emancipacion-atomica/README.md` | Sin dato crudo no hay hash: solo `NO DATA`. Un directorio de pruebas vacío es correcto; un hash decorativo es una violación | Le enseña que el vacío declarado vale más que el relleno | **El silencio honesto** |
| **Trayectoria, nunca juicio** `P3` | `codice/CODICE_david.md` (suelo) | «La capa de inferencia jamás contiene juicio de capacidad/valor. **Solo trayectoria**». Y: «los fracasos son datos del contexto, no faltas de la persona» | Nadie le pone nota; se le muestra su recorrido | El aprendiz es soberano, no evaluado |
| **La cicatriz** `P2` | `memory.py` `cruzar_frontera()` · V6 en `test_traza.py` | Todo bloqueo del filtro deja fila con `estado='bloqueado'`, huella y motivo — **jamás el texto crudo** | Ve qué se frenó sin que se guarde lo frenado | **La cicatriz no miente** |
| **Nombrar protege** `P2` | D67 · U7 en `test_hilos.py` | El levantamiento de un dato redactado **nombra el dato** ante la persona, por sesión, y es reversible | Aprende a decidir dato a dato, no en bloque | Consentimiento con nombre y apellidos |
| **La propuesta en borradores** `D` | D69 | Lo que propone la máquina va a BORRADORES; la promoción es acto exclusivo de la persona | Su memoria sigue siendo lo que él escribió | **El aprendiz promueve sus propias propuestas** |
| **El camino que no finge** `P2` | `cara.py:150-153` | «Un camino que muestra progreso que no puede medir es una barra de carga falsa, y el producto entero existe para no hacer eso» | Progresión M0–M7 con prueba por peldaño | Medir o declarar `NO_DATA`; nunca decorar |
| **El límite escrito** `P2` | `LIMITES_DEL_CRITERIO.md` §b | «Los 10 criterios miden el continente». Queda escrito **y no se compensa** | El módulo no le promete que aprenderá | Honestidad sin hype |

## 1.4 · Repositorios y código

Todos de `Cuarentena/capas-aurelius-jardin-v2.md` §3 — «las 11 meditaciones», rúbrica
Bronce (mecánica) / Plata (auditoría) / Oro (cómo lo absorbe Aurelius).

| Nombre | Repo | Técnica | Aporte | Estado real |
|---|---|---|---|---|
| **Engramas de cuatro campos** `P2` | gentlemanprogramming §3.10 | Unidad atómica de aprendizaje en cuatro campos: **What, Why, Where, Learned** | La forma exacta de registrar lo aprendido | **VIVE EN EL PRODUCTO**: `memory.py` esquema `engrams` tiene `what`, `why`, `where_ref`, `learned` |
| **Retiro de andamios** `P2` | platzi §3.11 | Al firmar el éxito de una misión, los andamios se archivan y se **borran físicamente** del espacio de trabajo | El paso final del módulo | Propuesto para M7. **No implementado** |
| **Sintaxis EARS** `P3` | bettatech §3.9 | `WHEN [condición] IF [precondición] THE [sistema] SHALL [acción]` — erradica la alucinación de diseño | Forma de escribir una propuesta que no se puede malinterpretar | No implementado |
| **Log incremental inmutable** `D` | llm de Simon Willison §3.5 | CLI ligero que registra cada interacción en SQLite local | El historial como subproducto, no como tarea | Análogo real: la tabla `salidas` |
| **Merkle sin demonio** `P1` | immudb §3.7 | Se **prohíbe** levantar el demonio pesado; su principio matemático se inyecta en SQLite encadenando cada hash con el anterior | Enseña a robar la idea y tirar la dependencia | `verify_pow.sh` existe en `codice-emancipacion-atomica/proofs/` |
| **Huella antes de arrancar** `P2` | llamacpp §3.1 | Validación de sha256 y firma antes de levantar nada | Nunca ejecutar lo que no se ha verificado | **VIVE**: `descarga.py` y el catálogo de piezas firmadas |
| **Veto al andamio eterno** `D` | anytype §3.2 | Veto a Electron por RAM **y por «inexistencia de destrucción de andamios pedagógicos»** | El criterio para rechazar una herramienta | Criterio, no código |

---

# PARTE 2 · EL MÓDULO

## 2.1 · Cómo la AI puede ayudarte — `scope P2`

Cuatro verdades, cada una con su mecanismo en el código, no en la prosa.

**1 · La AI no hace el trabajo: enseña a construirlo.**
El andamiaje decae con la competencia **demostrada**, no con la declarada
(`teaching_kernel.yaml`). *Ejemplo:* la primera vez que exportas, la frontera te enseña el
texto entero y te pregunta; cuando ya sabes qué mira, deja de explicártelo.

**2 · La AI propone; tú promueves.**
Lo que la máquina escribe va a BORRADORES y solo tú lo asciendes a memoria (D69, IronClaw).
*Ejemplo:* Aurelius puede redactar un recuerdo por ti; no aparece en tu memoria hasta que lo
firmas. `NO_DATA`: **la capa BORRADORES está firmada en canon y no existe en el código**.

**3 · La AI declara lo que no sabe.**
`NO_DATA` no es cero ni celda vacía: es una pregunta que nadie contestó. *Ejemplo:* un
peldaño del Camino que no se puede medir se declara, no se pinta a medias.

**4 · La AI cicatriza los bloqueos.**
Cuando el filtro frena algo, queda fila con estado, huella y motivo — **y nunca el texto
frenado** (V6). *Ejemplo:* `python3 aurelius.py --registro` enseña qué salió y qué se paró,
y se puede enseñar a cualquiera sin exponer nada.

## 2.2 · Crear tu proyecto personal — `scope P2`, método `D`

Los seis pasos heredan el orden 0–5 de `02_CANON_OPERATIVO.md` §4 (R11). Cada paso cita la
joya que lo sostiene.

**Paso 0 · Verificar antes de imaginar.** Antes de decidir qué construir, mira qué tienes ya
y qué está roto. *No se abre frente nuevo si hay uno roto bloqueando valor real.*
→ *Orden de trabajo innegociable.*

**Paso 1 · Nombrar la debilidad.** Escribe el problema **tuyo** que vale la pena resolver, en
los cuatro campos del engrama: qué, por qué, dónde, qué aprendiste.
→ *Engramas de cuatro campos* · *SDD (referencia externa)*.

**Paso 2 · Definir antes de construir.** Escribe qué debe hacer y cómo se sabrá que lo hace,
antes de una línea de código. Si puedes, en forma EARS: *cuando [condición], si
[precondición], el sistema debe [acción]*.
→ *Sintaxis EARS* · *SDD*. `NO_DATA`: el vocabulario *spec* no existe en ningún papel del árbol.

**Paso 3 · Ordenar por desbloqueo, no por gusto.** De todo lo que has escrito, elige lo que,
cerrado, desbloquea más con menos construcción. Divide en metas que quepan en una sesión.
→ *Heurística de prioridad* · *Milestones (referencia externa)*.

**Paso 4 · Ensayar en seco lo irreversible.** Toda operación que borra, escribe o sobrescribe
se simula antes. Regla de estado, no de estilo.
→ *Ensayo en seco obligatorio* (Sweller).

**Paso 5 · Probar en local, sin red.** Lo que no funciona en tu máquina, apagada la red, no
funciona: funciona el servicio de otro.
→ *Local antes que global* · D68.

**Paso 6 · Cerrar con un paso pequeño y un delta que tú corriges.** Al terminar, la sesión
propone «hoy avanzaste X, decidiste Y, queda Z» y **tú lo apruebas o lo corriges**.
→ *Patrón mini-códice* · *Ancla del objetivo macro*.

## 2.3 · Usar las joyas pedagógicas — `scope D`, aplicadas a `P2`

**Andamiaje (scaffolding).** La ayuda es alta al principio y decae con lo que demuestras.
*En Aurelius:* la frontera de salida te enseña el texto completo y te pide aprobación
explícita; es andamio, y su retirada es el peldaño M7.

**Retirada del andamiaje (Scaffolding Faded).** Al firmar el éxito, los andamios se archivan
y se borran del espacio de trabajo (platzi §3.11). *Estado real:* propuesto para M7,
**no implementado**. `NO_DATA` sobre qué cuenta como «éxito firmado».

**El fallo como ramificación.** Cuando algo se bloquea, no dice «error»: dice qué regla
disparó y qué se puede hacer. *En Aurelius:* la traza (D10) da entrada, regla y veredicto,
y el registro guarda el motivo sin el fragmento.

**Recuperación, espaciado y carga.** Repasa activamente lo tuyo, distribuido en el tiempo, y
no te satures. *En Aurelius:* tu memoria es consultable y exportable; el objetivo macro queda
a la vista para no reconstruirlo cada sesión.

**Lo que aquí NO se usa, y por qué.** La Zona de Desarrollo Próximo aparece **una sola vez**
en el árbol, en `mente/corpus/_INDICE.md`, y en una carpeta declarada **vacía a propósito**:
«es el encargo, no el resultado». Aplicarla sería decretar mecánica sin corpus, que es
exactamente lo que ese índice prohíbe.

## 2.4 · Alineación solarpunk — `scope D`

**El juego no es escapar: es edificar.** El orden 0–5 empieza por verificar y conectar lo que
YA funciona. Construir sobre lo que sostiene, no sobre lo que ilusiona.

**Local antes que global.** El producto se abre con doble clic y funciona con la red apagada;
la cara lleva dentro sprites, idiomas, recuerdos y voz. Medido: cero orígenes externos.

**La latencia es el fusible.** El muro no es moral, es físico: el ensayo en seco obligatorio
y la firma humana meten tiempo entre la propuesta y el efecto. *«La firma se exige porque es
el único componente que soporta el coste de estar equivocado»* — códice de emancipación.

**La cicatriz no miente.** Todo bloqueo del filtro deja constancia con huella y motivo, jamás
con el texto. Y la negativa de la persona **no** deja fila: se anotan los veredictos de la
máquina, no las decisiones de quien vive en ella.

**El aprendiz es soberano.** Promueve sus propias propuestas (D69), nombra lo que libera
(D67), y nadie le pone nota: la capa de inferencia narra **trayectoria, nunca juicio**.

---

# PARTE 3 · NO_DATA Y CONTRADICCIONES

## 3.1 · Pedido en el encargo, ausente en el árbol

| Concepto | Apariciones | Veredicto |
|---|---|---|
| Piaget · Papert · construccionismo · currículum en espiral · «objetos para pensar con» · asimilación/acomodación · estadios de desarrollo | **0** | `NO_DATA`. No entran al módulo |
| Vygotsky · ZDP | **1**, en `mente/corpus/_INDICE.md`, carpeta declarada vacía a propósito | `NO_DATA`. Es encargo pendiente, no doctrina |
| Superpowers · Whisper Flow · Minimax M3 | **0** en todo el árbol | `NO_DATA`. Solo existen en el mensaje del Soberano |
| React Bulletproof | **1**, y es el papel que creé hoy con la transcripción | Sin procedencia independiente. Se cita como externo |

## 3.2 · Decisiones que esperan al Soberano

1. **BORRADORES (D69) está firmada y sin implementar.** Dos de las cuatro verdades de §2.1 y
   dos pasos del método descansan en una capa que no existe en el código.
2. **Qué cuenta como «éxito firmado»** para disparar el retiro de andamios de M7.
3. **Si el vocabulario spec / plan / milestone se acuña** con entrada de canon propia, o
   se queda como préstamo citado.
4. **`03_ESTADO_FIRMADO.md` §6** declara que construir herramientas para Aurelius es objetivo
   **posterior**. Este módulo lo roza; abrirlo es decisión tuya, no consecuencia de haberlo
   escrito.

## 3.3 · Contradicciones declaradas (R7)

**1 · `capas-aurelius-jardin-v2.md` describe un Aurelius que no existe.** El documento fija
`gold_chain.jsonl`, FTS5, disparadores Merkle en C, firma Ed25519 por engrama y la ruta
`~/.aurelius-p0x/`. **Medido hoy en el producto: cero apariciones** de `fts5`, `gold_chain`,
`merkle`, `bronze` o `silver` en el código. El propio documento lo admite en su nota de
auditoría: esa ruta *«no existe en el nodo medido»*. Es diseño `P1`, no producto `P2`, y el
módulo solo toma de él lo verificado: los cuatro campos del engrama.

**2 · Subagentes contra IronClaw.** El encargo pide enseñar a «ejecutar con subagentes». Un
bucle de agentes que escribe y promueve sin firma humana viola el suelo (`02` §0.1). El
módulo enseña el paso 3 —dividir en metas— sin adoptar el ejecutor.

**3 · La estructura «production-ready» de un framework** choca con que el MVP es biblioteca
estándar sin dependencias. Se toma la idea de tener una base, no la base ajena.

**4 · El módulo promete método, no aprendizaje.** `LIMITES_DEL_CRITERIO.md` §b dice que los
criterios miden el continente y **no lo compensa**. Este módulo hereda ese límite: enseña a
ordenar un proyecto; que la persona salga sabiendo algo que no sabía **no está medido en
ninguna parte de este árbol**, y prometerlo aquí sería la operación exacta que ese fichero
existe para no hacer.

---

> **Cierre.** `clase=doctrina`, estado PROPUESTA. Nada de esto es canon hasta que el Soberano
> lo firme con un commit (`01_LEEME_PRIMERO.md` §1). Las joyas de `P1` y `P3` se citan como
> referencia y **no viajan** al producto; el módulo funciona entero sin Preceptor y sin Beelink.
