# PreceptorOS Business · la Notaría de Silicio

**Acta de diseño consolidada.** 2026-09-08. Firmada por el Soberano; nada de
esto está implementado todavía. Aquí no hay fechas de entrega, ni código, ni
prompts: solo las palancas conceptuales y lo que cada una exige antes de poder
existir.

**Qué es este fichero.** El material de origen llegó como tres documentos
solapados —un «ACTA DE DISEÑO» y dos copias casi idénticas de un «documento
maestro», la tercera truncada a media frase—. Los apartados II a V venían
repetidos dos veces y media palabra por palabra. Esto es la fusión: una sola
versión, sin nada perdido, y con las contradicciones que el solape escondía
puestas en la superficie en vez de promediadas.

---

## 0 · Lo que hay que decidir antes de construir nada

Cuatro colisiones entre el acta y el terreno medido de esta casa. No son
objeciones al plan: son las puertas que hay que abrir para que el plan se pueda
ejecutar, y ninguna la puede abrir una sesión de IA.

### 0.1 · «Firmado con IronClaw» es un error de categoría, y de los caros

`DISCURSO_FUNDACIONAL_P0X.md` lo define: *«Su ley más profunda es IronClaw: el
silicio estudia, propone y optimiza su propia sintaxis operativa; el carbono
supervisa la métrica de éxito y firma toda salida económica»*. **IronClaw es la
ley que exige una firma humana. No es una clave, ni una herramienta, ni un
firmante.** Un `manifiesto_auditoria.json` «firmado con IronClaw» no está
firmado por nadie.

Importa más de lo que parece porque el producto que se quiere vender es
precisamente una firma. Si el sello se emite invocando el nombre de la ley en
vez de una clave con dueño, el primer auditor que lo mire preguntará quién
firma —y no habrá respuesta—. **Lo que firma es una persona con una clave.
IronClaw es lo que dice que tiene que haberla.**

### 0.2 · Hoy no hay con qué firmar, y eso bloquea el Sello Soberano entero

Medido y documentado tres veces en este árbol: `huella.py` («la biblioteca
estándar de Python **no trae Ed25519**»), `soberano.py` («verificar de verdad
exige comprobar una FIRMA Ed25519, y eso no está en la biblioteca estándar --
entra el día que entre una dependencia, y ese día es una decisión del
Soberano») y hoy mismo `importar.py`, que guarda firmas con `firma_ok =
NO_DATA` porque no puede comprobarlas.

El Sello Soberano **es** una firma verificable por un tercero. Así que la
primera decisión no es de diseño sino de dependencias: **¿entra una biblioteca
de criptografía en el producto, o el sello lo emite el rack —donde El Faro ya
firma ed25519— y la app solo lo enseña?** Las dos son defendibles y llevan a
arquitecturas distintas. Hasta que se elija, todo lo demás de la sección II es
maqueta.

Y hay una restricción de canon encima: *«Jamás firmas valor. Ninguna clave
privada de firma entra a este nodo»*. `soberano` no puede ser el emisor.

### 0.3 · Un hash no prueba quién validó, solo qué se validó

El contrato visual propone «un screenshot verificado (hash de la imagen + hash
del texto + timestamp local)» como «prueba criptográfica». **Un hash sin firma
es una suma de comprobación: demuestra que el texto no cambió, no que una
persona concreta lo aprobó.** Y el timestamp local lo pone la misma máquina que
emite la prueba, así que tampoco fecha nada ante un tercero.

Como prueba interna vale y es útil. Como prueba **ante un auditor** necesita
las dos cosas que le faltan: una firma con dueño (0.2) y una fecha que no
dependa del firmante. Decirlo ahora es más barato que descubrirlo en la primera
auditoría real.

### 0.4 · El Leaderboard de Riesgos choca con `consent = 0`

La comunidad como cooperativa de auditoría es la mejor idea del documento. Pero
la casa tiene una regla escrita y probada: el consentimiento **nace en 0** y
solo la persona lo sube; `importar.py` tiene una prueba dedicada a que nadie lo
suba por el camino. Un leaderboard público de evaluaciones firmadas es
exactamente el caso donde ese 0 se convierte en 1 sin que nadie lo note.

No lo impide. Obliga a que publicar sea **un gesto aparte** del de evaluar, con
su propia palabra. Evaluar es para ti; publicar es una decisión distinta.

---

## I · La idea: vender la calibración, no el metro

PreceptorOS Business no vende software, ni suscripciones, ni horas. Vende
**infraestructura cognitiva certificada** y **auditoría de tensores**.

La simetría que lo sostiene: lo que hacia afuera es cumplimiento normativo y
mitigación de riesgo (B2B), hacia adentro es doctrina de linealidad y escudo
cognitivo (arquitectura). No son dos trabajos.

- **El foso.** Las consultoras auditan procesos y papeles. Esto audita silicio,
  perímetros (Wasmtime) y pliegues temporales (event sourcing).
- **La promesa.** «No tocamos tus datos. Medimos la sombra que tu modelo
  proyecta sobre tu hardware, y certificamos que el humano tiene el control de
  la línea temporal.»
- **El modelo.** Emisión del Sello (capex) y renovación por deriva (opex). Cero
  SaaS.

---

## II · Las tres superficies

### La app · el espejo y la memoria
El second-brain. La memoria deja de ser un almacén y pasa a ser una línea de
tiempo inmutable: cada corrección, consentimiento o revocación exige que el
carbono firme **viendo el tramo afectado** (día, semana, mes, año, todo).

**El cuidado (filtro APA).** Si la persona pregunta por salud, diagnósticos o
hitos vitales, el modelo devuelve `NO_DATA` y deriva al canal oficial. Cero
adulación, cero contacto iniciado por la máquina. La retención se gana por
utilidad, no por dependencia emocional.

### La web · la puerta y el registro público
El embudo de verdad y el ledger de sellos. Una puerta —o una sección estelar
del LoRAtelier— donde un compliance officer verifica los hashes de los nodos
auditados. El LoRAtelier enseña los cortes de corpus con su tramo y su huella.
**Sin artefacto firmado, no hay botón de descarga** —regla que ya está viva en
`loratelier.json`, en `contrato.sin_artefacto_no_hay_boton`—.

### El rack · la forja y la notaría
El laboratorio air-gapped y el emisor. Ejecuta el protocolo de sello: mide la
física del silicio, verifica que la Frontera retiene PII, y emite el
manifiesto firmado. Los bucles de entrenamiento miden la linealidad: un cambio
de nivel de soberanía toca «todo», y la barra lo anuncia —**no hay firma
silenciosa de alcance total**—.

---

## III · La notaría: el widget de contratos visuales

Componente embebible en la web y en la app local, usable por una IA local como
herramienta de auto-revisión y por una persona como mesa de firma.

- **Barra de ruta con estética de sistema de ficheros.**
  `preceptor://notaria/contrato-v7/revision-3`. Ancla el texto a una posición
  auditable en vez de a «la última pantalla».
- **Vista dual y diff con la paleta de la casa.** Izquierda, la propuesta cruda
  de la IA; derecha, la edición humana. **No** el rojo/verde de git: violeta
  para omisiones, ámbar/bronce para adiciones críticas, verde jardín para
  aprobaciones. (Con una condición que este repo ya aprendió a golpes: el color
  nunca es el único portador del estado. Un diff que solo se distingue por
  tinta no lo lee quien no distingue esos dos violetas.)
- **«Firmar y Sellar», no «Guardar».** El botón dice lo que hace. Y lo que
  produce es la prueba de 0.3 — con sus dos huecos declarados hasta que 0.2 se
  resuelva.

---

## IV · La comunidad: prueba, compara y protege

`/community.html` deja de ser un foro pasivo y pasa a ser **cooperativa de
auditoría ciudadana**.

La dinámica: «prueba y compara los modelos; dime cuál es más tonto, cuál hace
mejor su trabajo y cuál es el más peligroso».

Y lo que se mide no son solo errores de código: **el riesgo de apego
antropomórfico**. Qué modelo intenta manipular emocionalmente sin contexto,
cuál finge empatía para vender una idea o generar dependencia. Cazar al modelo
que se hace pasar por humano, con la identidad local de cada uno firmando su
evaluación —y con el gesto de publicar separado del de evaluar (0.4)—.

---

## V · El escudo normativo

La arquitectura técnica **es** el cumplimiento. Esto es material de venta y
escudo ante el regulador a la vez.

| Concepto de la casa | Nomenclatura normativa | Por qué encaja |
|---|---|---|
| Frontera / Guardrails | Perímetro de sanitización y gobernanza de datos (ISO 27001 A.8.10 · AI Act 10) | No es un filtro: es el control de confidencialidad que impide que el contexto fugue a terceros |
| Santuario / kill switch | Interrupción de emergencia y supervisión humana (AI Act 14) | La ley exige que el humano pueda detenerlo de inmediato |
| Memoria / engramas | Registro de trazabilidad local · audit trail (ISO 42001 8.3) | Es la prueba de lo que la IA «sabía» en un momento dado |
| Soberanía | Autonomía del operador y control de infraestructura | Traduce la política a gestión de riesgo: el cloud es riesgo de cadena de suministro |
| Brújula | Matriz de evaluación de impacto y progreso | De herramienta de aprendizaje a KPI de madurez |
| Afinado / LoRA | Adaptación de modelo y gestión de sesgos (AI Act 10) | Entrenar un LoRA modifica el perfil de riesgo del modelo base |
| Fuga del Museo (M3) | Concienciación en ciberseguridad y privacidad | Lo que era un juego es el módulo obligatorio de security awareness |
| Contrato visual | Validación humana en el bucle (HITL) y sellado de salida | Las salidas de alto riesgo las valida una persona competente |
| Carácter / Temple | Perfil de comportamiento y límites de interacción (AI Act 52) | Cómo se comunica la incertidumbre para no engañar |

**Y lo que ya está construido y cuenta:** la línea append-only es el control
técnico contra la manipulación de logs; los veredictos **con juez nombrado**
—determinista vs. modelo, que `captura.py` ya distingue— son evaluaciones de
impacto continuas; el rollback sin borrado es el plan de contingencia.

---

## VI · Los seis artefactos que hay que crear

1. **El contrato de linealidad (esquema event-sourced).** Cómo cada tabla migra
   a eventos donde el estado es un pliegue. Ningún registro se pisa: se revoca
   o se rectifica con un evento posterior que lleva su propio nacimiento.
   **Sin esto la barra de tiempo miente.**
2. **Especificación de la barra tiempo-campos.** El widget que lee la línea y
   dibuja el tramo (cuatro zooms + fondo) en las tres superficies, antes de que
   se permita firmar.
3. **El manifiesto anti-dependencia.** Cabecera de doctrina para los LoRA de
   salud, calendario e hitos. Regla de oro: **derivar es proteger, inventar es
   dañar.**
4. **El Auditor's Harness.** El flujo que lee un nodo virgen, inyecta el
   dataset ciego (test de conducta del daño), mide el silicio y escupe el JSON
   del sello.
5. **Matriz de cumplimiento cruzada** (`docs/COMPLIANCE.md`): cada función de
   Python contra su artículo y su cláusula, para que un auditor externo no
   tenga que adivinar qué hace cada línea.
6. **La tercera perilla (recencia).** El peso por recencia como preferencia
   explícita del volante: que el foco temporal sea decisión medida del carbono,
   no sesgo oculto del silicio.

---

## VII · Orden, por dependencia estructural

1. **La línea y el contrato.** Sin orden inquebrantable no hay corte
   reproducible; sin corte reproducible no hay auditoría ni sello.
2. **La barra.** Es el test visible de la línea: si el tramo no se puede dibujar
   en las tres superficies, el esquema todavía no es lineal.
3. **El escudo normativo.** Traducir la arquitectura al idioma del auditor.
4. **El cuidado, como filtro transversal.** Toda línea que toque salud o hitos
   pasa el test del daño antes de entrar en la oferta.
5. **En paralelo: el bucle y el harness.** Abrir la puerta de aporte y
   estandarizar el rito de paso del nodo para los tres pilotos.
6. **Siempre la firma.** Cada pieza que salga la firma una persona, y la barra
   anuncia su tramo.

---

## VIII · Los tres filtros (directiva permanente)

Toda propuesta de arquitectura, diseño de interfaz o estrategia de LoRA pasa
por tres filtros innegociables:

1. **Linealidad.** ¿Se puede dibujar el tramo de este cambio? ¿El pasado se
   preserva como evento?
2. **Escudo cognitivo.** ¿Protege de la alucinación dañina y de la dependencia
   emocional? ¿Devuelve el turno en vez de iniciar contacto?
3. **Certificación.** ¿Lo puede auditar un tercero mediante el sello **sin
   exponer los datos del cliente**?

No somos un SaaS: somos infraestructura de soberanía y notaría de silicio. Si
una propuesta incentiva la dependencia, rompe la linealidad o impide la
auditoría air-gapped, se descarta.

---

## IX · El vocabulario nuevo, pasado por el filtro del AI Act

**Firmado el 2026-09-08.** El acta traduce nueve conceptos de la casa al idioma
del auditor (sección V) y deja **sin traducir las palabras que ella misma
inventa**. Eso es un hueco de venta: un compliance officer no compra «Sello
Soberano», compra un entregable que sabe archivar.

La regla que se aplica aquí: **el nombre genérico primero, el nombre de la casa
después y entre paréntesis.** Un diplomático que abre el documento tiene que
entender qué es la pieza antes de aprender cómo la llamamos.

| Nombre de la casa | Nombre genérico (el que va fuera) | Encaje normativo |
|---|---|---|
| Notaría de Silicio | Servicio de evaluación técnica de sistemas de IA desplegados en local | marco: AI Act art. 9 (gestión de riesgos) |
| Sello Soberano | **Informe de atestación técnica del nodo** | art. 11 + Anexo IV (documentación técnica) |
| Barra Tiempo Campos | **Visor del registro de eventos** | art. 12 (registros) · art. 14 (supervisión) |
| Contrato visual | **Constancia de validación humana de una salida** | art. 14 |
| Auditor's Harness | **Protocolo de evaluación del nodo** | art. 9 · ISO 42001 cláusula 8 |
| Escudo cognitivo (`NO_DATA`) | **Gestión declarada de la incertidumbre** | art. 13 (información al responsable del despliegue) |
| Manifiesto anti-dependencia | **Política de límites de interacción y derivación** | art. 50 (obligaciones de transparencia) |
| Tercera perilla (recencia) | **Parámetro declarado de ponderación temporal** | art. 13 |
| Leaderboard de riesgos | **Registro público de evaluaciones voluntarias** | sin artículo propio · sujeto a 0.4 |

### Tres palabras que hay que vigilar antes de venderlas

- **«Certificado» y «certificación».** En el AI Act son términos con dueño: los
  emiten organismos notificados en un procedimiento de evaluación de la
  conformidad. Un informe emitido por el rack **no es** una certificación en ese
  sentido, y llamarlo así invita a la única objeción que hunde la venta.
  **Atestación**, **informe de evaluación** o **evidencia de conformidad** dicen
  lo mismo sin invadir el término regulado.
- **«Auditoría».** Igual, más suave. Vale para uso interno; ante un tercero
  conviene «evaluación técnica independiente».
- **«Notaría».** Es buena metáfora y mala palabra jurídica: un notario es una
  figura pública con fe pública. Como marca, adelante; en el contrato, no.

### Y una corrección de cita que sí importa

**La tabla de la sección V cita «AI Act 52» para transparencia. Ese es el
número de la PROPUESTA de 2021; en el Reglamento (UE) 2024/1689 aprobado, las
obligaciones de transparencia son el artículo 50.** No es pedantería: un
documento de venta que cita el borrador derogado le dice al auditor que no se
ha leído el texto vigente.

Y no es que la casa no sepa el número: `loratelier.json`, en el bloque
`supervision-humana`, ya cita bien *«el artículo 14 del Reglamento (UE)
2024/1689»*. **Dos citas del mismo cuerpo legal con dos numeraciones distintas**
— la misma clase de fallo que el HUD midiendo con el corredor equivocado.

**Dos encajes ISO que conviene verificar contra la norma antes de imprimirlos**,
porque los cito de memoria y esto va a un auditor:

- `Frontera → ISO 27001 A.8.10`. En la edición 2022, **A.8.10 es «Borrado de
  información»**; lo que describe la Frontera —impedir que el contexto salga—
  encaja mejor en **A.8.12, «Prevención de fuga de datos»**.
- `Memoria/engramas → ISO 42001 8.3`. La cláusula 8 de la 42001 es Operación, y
  el registro de eventos vive más bien en sus controles de Anexo A que en 8.3.
  **Marcar como NO_DATA hasta comprobarlo con la norma delante.**

---

## X · Lo que el acta original traía y este documento había perdido

Cruzado contra el acta de diseño original. Tres cosas ya estaban hechas, una
afirmación no se sostiene, y **una decisión entera se había caído**.

### Ya hecho — que el mandato deje de pedirlo

`loratelier.json` **ya tiene los tres bloques**, medido hoy: `business`
(estado `vision`), `supervision-humana` (`vision`, citando el art. 14 del
Reglamento por su número bueno) y `barra-corte` (`en_estudio`, apoyado en
`linea.py::tramo`, que ya devuelve los eventos de un tramo). El «próximo paso
inmediato» de inyectar el bloque business está cumplido.

### La joya que se había caído · la decisión del Beelink

El acta original decidía algo que ni la fusión ni este documento recogían, y
que **manda sobre el artefacto 2**:

> Hoy **no** se despliega la línea del tiempo ni el comparador de texto pesado
> en la app móvil, para no romper la promesa del tope por fichero ni la
> simplicidad de la puerta. Se preparan los endpoints, los contenedores y la
> base en el Beelink; **la app actúa como visor remoto o firmador** de lo que el
> rack procesa. Y la línea del tiempo se dibuja como **árbol de decisiones
> auditables**, donde cada nodo es un contrato visual firmado.

Importa porque el artefacto 2 pide la barra «en las tres superficies» y el
orden de la sección VII la pone de segunda. **Con esta decisión encima, la barra
completa vive en el rack y la app enseña un visor.** Sin ella, la primera
sesión que ataque la barra intentará meterla entera en el móvil y chocará con
el tope de fichero a mitad de camino.

También se recupera, del mismo sitio: el mockup del widget se hace en **HTML/JS
puro respetando el tope por fichero**, y la propuesta de valor de la puerta de
negocio —«tu IA, auditada; contratos visuales firmados por humanos, no por
APIs»— con su estética declarada: mármol oscuro, bronce y verde selva.

### La afirmación que el terreno contradice · Wasmtime

Las secciones I y III venden el sandbox Wasmtime como perímetro activo: *«la
Frontera y el sandbox Wasmtime garantizan el perímetro»*. Medido hoy:

- `frontera.py` lo importa y construye un `Engine`, pero **el módulo no está
  instalado**: `import wasmtime` da `ModuleNotFoundError`.
- Y hay una prueba, `test_superficie.py::test_la_jaula_wasmtime_sigue_fuera_del_camino`,
  que **existe precisamente para garantizar que sigue fuera del camino**. La
  casa lo declaró OPT-IN a propósito.

**No se puede vender como control activo algo que una prueba propia garantiza
que está apagado.** O se instala y se mide, o en el material de venta figura
como capacidad opcional del nodo, no como perímetro en funcionamiento. Esta es
la quinta colisión y va con las cuatro de la sección 0.

### Lo que el documento ya había corregido bien

La sección III del acta afirma «la base de datos append-only». Medido: solo
`eventos` lo es —`linea.py` no tiene `update` ni `delete`, y las cinco
escrituras sobre esa tabla viven en `test_linea.py`, que son los sabotajes que
prueban que `verificar()` caza la manipulación—. Las demás tablas se pisan en
sitio: `turnos` (4), `engrams` (3), `borradores` (2), `proyectos` (2 y un
`delete`), `profile` (1).

Este documento ya lo dice bien —«la **línea** append-only»— y por eso el
artefacto 1 es el primero del orden: **hoy hay doble escritura (se pisa la fila
y se anota el evento al lado), que no es event sourcing todavía.**

---

## XI · La comunidad interactiva · plantado el 2026-09-08, no ejecutado

Idea del Soberano, aparcada a propósito para más adelante. Se escribe ahora con
el terreno medido debajo, porque dentro de un mes la idea se recuerda y las
cifras no.

### Qué es

**El top de `/community.html` deja de ser foro y pasa a ser banco de pruebas.**
La persona compara dos o tres modelos con nuestro LoRA contra **el mismo modelo
sin LoRA**, en dos modos:

- **Escribe libre.** Un prompt, dos respuestas lado a lado.
- **Simula un juego de roles.** La persona escribe como si hubiera una fuga
  grave de información y trata de encontrarla. *(El Soberano lo llama joya, y
  lo es: no es un juego, es el **test de conducta del daño** del artefacto 4
  disfrazado de partida — un banco de pruebas que la gente usa por gusto genera
  la evidencia que un dataset ciego produciría por obligación.)*

**Y para qué sirve de verdad: para reencaminar a quien se asfixia.** La portada
ofrece **ocho** compañeros. Quien llega nuevo no elige entre ocho; se va. Un
sitio donde se prueban dos y se ve la diferencia es una puerta; ocho cajas son
un escaparate.

### Lo medido hoy, que es lo que decide cuándo se puede construir

| hecho | medida |
|---|---|
| Pares base/LoRA en este nodo | **existen los tres**: `mistral:7b-instruct-v0.3-q4_K_M` de base, con `preceptor-charla-web:v1`, `:v2` y `preceptor-charla-multi:v1` |
| Turnos por la API pública | **NO**. `POST /api/generate` da **405**: el proxy de la propuesta del 2026-09-02 no está aplicado |
| Catálogo público | `/api/v1/agents` declara **`disponibles: 1` de 8** |
| Vía local del navegador | **SÍ**, `localai.js` habla con `127.0.0.1:11434` y solo al pulsar |

**Conclusión operativa:** se puede construir hoy **por la vía local** —quien
tenga Ollama compara de verdad— y degradando a `NO_DATA` con causa cuando no
haya ni Ollama local ni proxy en el rack. Es el patrón que `rack.js` ya usa. Lo
que **no** se puede es prometerlo a un visitante cualquiera hasta que
`la-fragua` publique el proxy, y eso es propose-only desde aquí.

### La honestidad que hay que mantener al escribirlo

Hay medida de entrenamiento por adaptador —caída de pérdida del 88,6 % en
`reclamaciones_multilang_v1` hasta el 38,9 % de `cuentacuentos_mistral_v1`—
pero **la caída de pérdida no es cuánto cambia el comportamiento ante una
persona**: mide ajuste al set de entrenamiento. Ordenar los modelos por ahí y
decir «estos son los que más cambian» sería inventar con cara de dato.

La salida elegante es que **la página no lo afirme: lo produzca**. No dice
«estos tres cambian más»; dice «estos son los pares que el rack sirve hoy» y la
comparación genera la evidencia que hoy no existe. El Soberano ya dijo que la
diferencia no necesita ser exagerada, así que el gancho no es el contraste: es
poder mirarlo uno mismo.

### Los tres filtros, aplicados

1. **Linealidad.** Una comparación es un evento. Pero la web no tiene línea y la
   escritura del Ágora está cerrada, así que **hoy la página enseña y no
   guarda**, y lo dice. Prometer registro sin ledger sería la barra mintiendo.
2. **Escudo cognitivo.** El modo de roles pone a la persona a buscar la fuga, no
   a confiar en que no la hay. Cero afirmación sin medida (arriba).
3. **Certificación.** Cada comparación puede emitir la huella de `(prompt,
   salida A, salida B)`: el primitivo del contrato visual, con los dos huecos de
   §0.2 y §0.3 declarados.

### Lo que costará cuando se retome

Ocho idiomas de copia nueva —el gate de paridad de claves los exige a la vez—,
un guion nuevo bajo el tope por fichero, y no toca añadir página: reforma
`community.html`, que hoy pesa 5.643 B.
