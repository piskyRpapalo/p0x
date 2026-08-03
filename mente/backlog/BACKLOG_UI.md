---
id: backlog-ui-p0x
clase: operativo
version: 1.1.0
fecha: 2026-08-02
metrica: bloques cerrados con evidencia / bloques abiertos; cero medio-estados podridos
umbral: se re-edita solo con reporte de CC o firma del Soberano; nunca por sensación
presupuesto_kb: 24
n_medicion: 1
visibilidad: privado (contiene rutas by-id y nombres de nodo — jamás a repo público)
---

# BACKLOG UI / SOFTWARE · HEXELION + AURELIUS + LE JARDIN

**Creado:** 2026-08-02
**Estado del proyecto:** ABIERTO. Pausa de atención por preparación de entrevista.
**Duración de la pausa:** indeterminada.

> **Casa autoritativa:** repo `p0x` (privado), ruta `mente/backlog/BACKLOG_UI.md`.
> `hexelion/CLAUDE.md` y `aurelius/CLAUDE.md` llevan un puntero de una línea a esta
> ruta. El documento **no** se copia a repos públicos: contiene rutas `by-id`,
> nombres de nodo y deuda interna.

---

## 0 · Cómo se usa este documento

Este archivo vive en el repo. No en la cabeza del Soberano ni en el contexto de
ningún modelo. Es la fuente autoritativa del trabajo pendiente de interfaz.

**Diseño para pausa de duración desconocida.** Los bloques NO son un sprint
secuencial. Cada uno es **atómico**: se puede ejecutar solo, deja el sistema en
estado coherente, y si resulta ser el último que se hace en meses, valió la pena
por sí mismo. No hay medio-estados que se pudran.

El orden es de mayor a menor apalancamiento, no de dependencia.

### Prompt de reactivación

Esto es lo único que hay que pegar en Claude Code al volver. Nunca más un muro
de texto:

```
Lee BACKLOG_UI.md en la raíz del repo.
Ejecuta el BLOQUE <N>, solo ese.
Respeta las INVARIANTES de la sección 1 y las prohibiciones del bloque.
Reporta en el FORMATO DE REPORTE (máx 12 líneas).
Actualiza el estado del bloque en este documento.
PARA. No encadenes bloques.
```

---

## 1 · Invariantes (aplican a todos los bloques)

- **Higiene Dura**: `tsc --noEmit` = 0 · sin lint nuevo · 0 pageerrors · sin
  dependencias nuevas sin justificar · cero IPs, hostnames, usuarios en ruta,
  wallets o identificadores de clave en nada que se publique.
- **Honest Sensors**: ningún widget muestra estado sin declarar antigüedad del
  **dato** (no del render). Ante la duda, `NO DATA`. Nunca un estado vacío que
  se parezca a un estado sano.
- **IronClaw**: propose-only en infraestructura. CC no despliega, no reinicia
  servicios en producción, no ejecuta `git push`. Propone; el Soberano firma.
- **Editar `src/`, nunca `dist/`.**
- **Commits atómicos**, uno por fix, mensaje descriptivo. Sin push.
- **Regla de parada**: ante ambigüedad, PARA y pregunta. No adivines.

### Formato de reporte (obligatorio, máximo 12 líneas)

```
RONDA <id> · <repo>@<rama>
HECHO      <hash> · <una línea por commit>
BLOQUEADO  <ítem> ← <dependencia exacta>
DECIDE     <pregunta en una línea, o "nada">
BACKLOG_UI.md actualizado: sí/no
```

La narrativa larga va a este documento, no al chat. El presupuesto de contexto
del Soberano es un recurso finito y es el cuello de botella real del proyecto.

---

## BLOQUE 0 · Régimen e higiene

**Estado:** ✅ hecho · 2026-08-02 (0.1 CLAUDE.md hexelion+aurelius · 0.2 Códice
inventariado, LIMPIO sin cambios · 0.3 CI anti-iframe en aurelius · 0.4
docs/INVENTARIO.md en hexelion · 0.5 puntero desde PENDIENTES.md)
**Coste:** S · **Apalancamiento:** alto (reduce el coste de todo lo demás)

0.1 · Escribir el FORMATO DE REPORTE en `CLAUDE.md` de cada repo.

0.2 · **Verificar el Códice** (público, con nombre real — riesgo asimétrico).
Comprobar qué existe realmente en `codice-emancipacion-atomica`:
- `CODICE.md` — **¿contiene el texto del "Anclaje del Carbono"**, o sigue el
  "Teorema de Incompletitud Termodinámica" con la afirmación TRNG?
  La afirmación *"el carbono es el único TRNG"* es **falsa** (existen TRNG de
  hardware: ruido térmico, osciladores en anillo, RNG cuánticos). Si sigue ahí,
  reportar de inmediato — es lo único público con una afirmación errónea.
- ¿Se eliminó la "Paradoja de Optimización II" (cláusula 99.9%, "Decibelios de
  Supervivencia")?
- ¿Se eliminaron los hashes truncados de los bloques PoW?
- ¿Existen `PRIOR_ART.md`, `CHANGELOG.md`, `verify_pow.sh`, abstract en inglés,
  sección "Condiciones de Refutación"?
- ¿Sigue apareciendo la fecha de nacimiento en el encabezado de autoría?
**No corregir nada.** Solo reportar el inventario.

0.3 · **Check de CI que prohíba `<iframe>` en Aurelius.** El bug de recursión
costó tres rondas. `camino.html` sigue existiendo como página standalone, así
que la vía de regresión sigue abierta. `grep` que falle el build.

0.4 · **Inventario de hardware** en `docs/INVENTARIO.md`: los dos seriales de
dongle (post-EEPROM), qué banda/antena lleva cada uno, en qué nodo vive, y el
`by-id` completo del M5Stack. Pedido cinco veces, nunca escrito.

0.5 · Puntero desde `PENDIENTES.md` a este documento.

---

## BLOQUE 1 · Puente M5Stack → redis

**Estado:** 🟢 escrito+probado (CC) · 2026-08-02 · **deploy pendiente del Soberano**
(IronClaw). `ingest_m5.py` (`216ca9e`) + `deploy/vigia/m5-bridge.service` + check en
`preflight.sh` (`54a9019`). TTL 30s = STALE≠MISSING. `--self-test` verde. Falta:
instalar en El Vigía + correr la prueba de honestidad (parar 60s → NO DATA).
**Coste:** M · **Apalancamiento:** máximo — desbloquea Dashboard **y** Le Jardin
con una sola pieza de trabajo.

**Situación:** el M5Stack emite JSON a 115200 en El Vigía. El endpoint del
gateway existe. La Sentinelle de Le Jardin está cableada. Falta el servicio
intermedio.

### Spec

- Leer **siempre** por `/dev/serial/by-id/usb-Hades2001_M5stack_6952B20639-if00-port0`.
  **Nunca `ttyUSB0`**: la numeración cambia con el orden de enumeración USB, y en
  La Fragua `ttyUSB0` es el UPS GreenCell gestionado por NUT.
- `stty ... raw -echo -hupcl clocal`. **Abrir el serie assertea DTR/RTS y puede
  reiniciar la placa.** `-hupcl` lo evita.
- Publicar en `hexelion:telemetry:m5:last`.

### ⚠️ Trampa crítica: STALE ≠ MISSING

Una clave de redis persiste después de que el M5Stack muera. El gateway la leería
tan contento y La Sentinelle mostraría **telemetría fantasma congelada con aspecto
de dato fresco**. Es el mismo fallo que casi ocurre con `aircraft.json`.

**Obligatorio:** cada publicación lleva timestamp, y el consumidor declara la
antigüedad. O TTL en la clave, o edad visible en la UI. Preferiblemente ambos.

### Criterios de aceptación

- Unit de systemd, `enabled`, con `Restart=on-failure` + `StartLimitBurst` /
  `StartLimitIntervalSec` para que **falle ruidosamente** en vez de entrar en
  crash-loop silencioso (precedente: 30.000 reintentos de `aurelius-interfaz`
  sin que nadie se enterara).
- **Prueba de honestidad**: parar el puente 60 s → La Sentinelle y el panel del
  dashboard deben pasar a `NO DATA`. Si siguen mostrando el último valor, el
  bloque no está hecho.
- `preflight.sh` incorpora la comprobación del puente.

**Prohibido:** desplegar. CC escribe y prueba; el Soberano instala y arranca.

---

## BLOQUE 2 · Second Brain pasivo

**Estado:** ✅ hecho · 2026-08-03 · opción (a): portada congelada (0 rAF libre) +
deriva transform CSS (GPU) · pointer-events:none · pausa en visibilitychange ·
reduced-motion estático · FULL interactivo misma pestaña. Medido (task time hilo
principal, misma página): 7.76% → 2.73% de un núcleo (~5pp del grafo eliminados;
residual = resto del Nexo). % por-proceso en la Pantalla Soberana = NO DATA.
Commits: `e5570e8` (+ `b0c0735` reconcilia test Sentinelle). tsc=0 · 412 verde.
**Coste:** M

**Objetivo:** en la portada del dashboard, no interactivo, con movimiento suave y
continuo. Visualizador ambiental, no herramienta.

### Restricción de presupuesto energético

Esto correrá 24/7 en la Pantalla Soberana, en un rack donde se miden vatios y hay
un agente cuyo trabajo entero es la austeridad. Una simulación force-directed a
60 fps fija un núcleo permanentemente. **No se acepta.**

### Spec

Implementación — elegir y justificar:
- **(a) PREFERIDA**: layout precalculado una vez + deriva lenta por `transform`
  CSS (compositado en GPU, coste de CPU ≈ 0).
- **(b)** Simulación a ≤4 fps con throttling explícito.
- **Prohibido** `requestAnimationFrame` a tasa libre.

Comportamiento:
- `pointer-events: none` en la versión de portada. Sin hover, drag, tooltip ni
  selección.
- Pausa completa en `visibilitychange` (pestaña oculta = 0 trabajo).
- Respeta `prefers-reduced-motion`: si está activo, estático.
- El movimiento no saca nodos fuera del recuadro.
- Botón FULL → página completa e interactiva, **misma pestaña**. Prohibido
  `window.open` y `target="_blank"` (es el patrón que causó el bug del drawer).

### Criterio de aceptación

Uso de CPU del proceso del navegador con el widget visible y en reposo, **medido**
antes y después. Objetivo < 2% de un núcleo. Si no se alcanza, decirlo — dato
medido o `NO DATA`, nunca estimación maquillada.

---

## BLOQUE 3 · Mapa fijo — verificar y completar

**Estado:** ✅ hecho · 2026-08-03 · commit `31dd268`. Verificado con evidencia y
completado: (1) interacción deshabilitada (drag/scroll/dblclick/touch/box/keyboard)
— faltaban, ahora `false`; (2) `BBOX_LISBOA`/`LIMITES_LISBOA` exportados + `maxBounds`
+ `fitBounds` (ya no un setView mágico); (3) el chip declara antigüedad del DATO
(`last_msg_age_s`), no la cadencia del poll. OK sin tocar: FULL=fullscreen misma
pestaña; solo ADS-B+AIS. tsc=0 · test nuevo verde.
**Coste:** S

### Verificar primero, con evidencia

- ¿Están deshabilitados `scrollWheelZoom`, `doubleClickZoom`, `dragging`,
  `touchZoom`, `boxZoom` y `keyboard`? ¿Se quitaron los controles de zoom?
- ¿El bbox es una **constante nombrada y exportada**, o un número mágico
  incrustado? (valor: lat 38.40–39.00 N, lon −9.60 a −8.70 W)
- ¿El badge declara antigüedad del **DATO** o cadencia de **render**? El widget
  llegó a mostrar `POLL · 1s` cuando eso era el render. Son cosas distintas y
  confundirlas es un sensor deshonesto.
- ¿El clic al mapa completo navega en la **misma pestaña**?
- ¿Se filtran solo entidades ADS-B y AIS?

Completar lo que falte. Un bloque de verificación puede cerrarse sin cambios si
todo está bien — eso también es un resultado.

---

## BLOQUE 4 · La Pizarra (terminal) — Aurelius

**Estado:** ✅ hecho · 2026-08-03 · commit aurelius `d40f0d0`. Modal EN LÍNEA (sin
iframe/página/ruta), cliente-side, cero endpoint de ejecución. FS ficticio + 12
comandos; no-impl → "not on the slate yet" (no inventa); badge permanente; chrome
de slate; COPIAR→terminal real; scaffolding fading (demostrados en localStorage,
solo si corren sin error → deja de explicar, solo propone). Verificado en vivo.
**Coste:** L

**Contexto:** el Soberano pidió abrir una shell real del PC del usuario. Se
descartó: darle manos al modelo destruye el suelo de IronClaw, y la cadena de
ataque ya existe (M2 hace que el usuario meta `.md` no confiables para RAG →
inyección → ejecución). La Pizarra es la alternativa, y es **pedagógicamente
superior**: no puedes destruir tu máquina mientras aprendes.

### Restricción arquitectónica absoluta

- Componente del **documento único** de Aurelius. **NO** página. **NO** iframe.
  **NO** ruta.
- **Cero endpoint de ejecución en el backend.** No crearlo ni desactivado, ni
  comentado, ni "para más adelante". Lo que no existe no se puede explotar.
- Todo cliente-side. Filesystem ficticio en memoria.

### Comportamiento

- Set inicial de comandos: `ls cd pwd cat mkdir touch echo grep head tail wc tree`
- **Comando no implementado → "no está en la pizarra todavía".**
  **PROHIBIDO inventar salidas plausibles.** Una salida falsa enseña algo falso,
  y el usuario lo llevará a su terminal real. Honest sensors aplica a la simulación.
- Badge permanente y visible: `PIZARRA · simulación · no ejecuta nada`.
- Chrome visualmente **distinto** de una terminal real. Si el usuario cree que
  ejecuta de verdad, el fallo es tan grave como la shell real, solo que al revés:
  confiará en una salida inventada.

### El puente es el punto, no el añadido

Cada lección cierra con botón **COPIAR** + *"ahora hazlo de verdad en tu terminal"*.
La Pizarra enseña; la terminal real hace. Sin ese puente, la Pizarra produce
gente que sabe operar una simulación.

### Scaffolding fading — el mecanismo

**Este es el único sitio de todo el sistema donde la Parte IV del Códice tiene
implementación.** Es la razón de que este bloque exista.

Registro local de comandos demostrados por el usuario. Cuando un comando se
demuestra, **Aurelius deja de explicarlo y pasa a solo proponerlo**. El andamio
cae por comando, medido, no por sensación.

---

## BLOQUE 5 · Deuda menor de Aurelius

**Estado:** 🟡 parcial · 2026-08-03 · **5.1 ✅** densos [DERIVADO] por roofline
(aurelius `6f9cb98`) · **5.4 ✅ decisión firmada**: la sonda física se queda
CONGELADA (paso en M3 + M7 horizonte) — sin cambio de código, es el estado
correcto · **5.2 (i18n huérfanas) y 5.3 (modo presentación en la cara) DIFERIDOS**
(coste medio; fuera del presupuesto de tokens de esta sesión).
**Coste:** S cada uno · pueden hacerse sueltos

5.1 · **`[DERIVADO]` en `oraculo.js`.** Los modelos densos siguen marcados
`[NO APLICABLE]`, que es sobre-corrección: la velocidad de un denso es derivable
por modelo roofline (`tok/s ≈ ancho_banda ÷ tamaño_modelo × η`, η≈0.7–0.8).
`NO DATA` aplica cuando no sabes; aquí sí sabes, por deducción. Etiqueta
`[DERIVADO]` mostrando fórmula y ancho de banda asumido.
Referencias: `aurelius_face.html:395`, `camino.js:226`.

5.2 · **i18n huérfanas.** Títulos y misiones FR/ES hardcodeados en camino, fuera
del diccionario. Ligado a #168/#172.

5.3 · **Modo presentación en la cara de Aurelius** (incl. `camino.html`), para
capturar el drawer abierto con módulos y sin fugas. El drawer ya está cerrado,
así que esto está desbloqueado.

5.4 · **Duplicación de la sonda física.** Existe como paso dentro de M3
(`missions.ts:115`, congelado) **y** como misión M7. Es el mismo patrón de
fractura que se acaba de limpiar. Requiere decisión del Soberano.

---

## BLOQUE 6 · Le Jardin des Ombres

**Estado:** 🟡 mayormente hecho · 2026-08-03 · **6.2 ✅** Restructurer 100% frontend
(Opción B firmada, sin IA/backend) — hexelion `82eeed6` · **6.3 ✅** verificado: "Jeux"
= la École con Quiz real (error-boundaried), no placeholder · **6.1 ⚠️** La Sentinelle
muestra NO DATA HONESTO (verificado); el dato real NO fluye aún: **gap de infra** — el
puente M5 escribe en el redis LOCAL de El Vigía, pero el gateway (fragua) lee su propio
redis (127.0.0.1). Propuesta (Soberano/infra): que `telemetry_m5` del gateway lea el
redis de El Vigía, o sincronizar la clave. · **6.4** roadmap: Le Jardin = Fase 4 del
proyecto; su fase interna dentro de las 6 = NO DATA (sin doc de roadmap propio a mano).
**Coste:** S una vez desbloqueado

**Nota:** este proyecto es el único que hace honest sensors **en francés y sin
que nadie se lo pidiera** — *capteur à venir*, *fiches de démonstration*. La
doctrina se transfirió sola. Merece registrarse.

6.1 · Verificar que La Sentinelle pinta datos reales una vez el Bloque 1 esté
desplegado. Y la prueba de honestidad: parar el puente → debe volver a
*capteur à venir*, no congelar el último valor.

6.2 · **Botón "Restructurer"** — ¿qué hace? Si llama a un modelo, es la única
superficie de Le Jardin donde entra IA y necesita su propia declaración honesta:
qué sale del dispositivo, a dónde, y consentimiento antes de enviar. Si es local,
declararlo también.

6.3 · ¿"Jeux" está conectado o es placeholder?

6.4 · ¿En qué fase del roadmap de seis está el proyecto?

---

## BLOQUE 7 · La Pizarra (bandeja) — más adelante

**Estado:** ⬜ diferido por decisión del Soberano
**Coste:** M

Pipeline visual fuera del chat: artefactos crudos sin voz del Preceptor,
sugerencias de prompt, listas destinadas a programas externos, icono de alarma
con estado de tótems y contenido por revisar, titular y archivar documentos.

**⚠️ Solapamiento a resolver ANTES de construir:**
- La cola de revisión **ya existe** en Hexelion: `TRAY` en cabecera + panel
  OBSERVE con `PENDING_REVIEW` / `ACCEPTED` / `ERROR` y botón `review`.
  O comparten componente, o son cosas distintas y se llaman distinto.
- "Titular y archivar documentos con persistencia local" **es M3 El Refugio**.
  Construirlas por separado deja dos almacenes de estado que divergen.

La idea fuerte que sí es original y hay que conservar: **un espacio donde el
artefacto aparece crudo, sin narrar, sin el marco del Preceptor.** Casi todas las
interfaces de IA envuelven todo en voz del modelo.

---

## BLOQUE 8 · Verificación cruzada — OSIRIS, Jurado, Alquimista

**Estado:** ⬜ pendiente (nuevo, firmado 2026-08-02)
**Coste:** L · **Apalancamiento:** alto — es la tesis del sistema, no un panel más.

**Por qué existe:** tres paneles llevan meses en `NO DATA`. La honestidad ya estaba;
lo que falta es el órgano. HEXELION se justifica por la *verificación cruzada*: sin
ella, OSINT es un feed de titulares y el Jurado un adorno.

### Regla de orden — innegociable

**El jurado antes que el feed.** Encender OSINT sin criterio de corroboración
sustituye un panel honesto que dice `NO DATA` por un panel que *parece saber*. Eso
es peor que el silencio: la fuente ya está declarada `no confiable`.

### 8.1 · Inventario (primero, sin encender nada)

En el HP correspondiente, reportar **medido, no recordado**: qué es exactamente el
OSIRIS instalado (repo/origen, versión, commit), qué lenguaje y runtime, si arranca,
qué dependencias externas exige (claves de API, red saliente, cuotas), qué formato
emite, y si el feed GDELT que consume sigue vivo. Si algo no se puede determinar,
`NO DATA` — nunca "parece que sí".

### 8.2 · El Jurado (define qué es corroboración)

Especificar el contrato **antes** de escribir código: qué cuenta como fuente
independiente, cuántas hacen falta, qué se hace con la contradicción (¿el veredicto
correcto puede ser `en disputa`?), y cuánto dura un veredicto antes de caducar. Un
veredicto sin fecha de caducidad es un recuerdo falso con retraso.

### 8.3 · Alchemist Advisory

Declarar si es abstención por diseño (el Alquimista se calla cuando no hay margen)
o feed muerto. Si es abstención, el panel debe decir **`SIN RECOMENDACIÓN`**, no
`NO DATA`: son estados distintos y confundirlos deshonra al sensor.

### Suelo aplicable

IronClaw: nada de lo que salga de este bloque firma valor. El Jurado **informa** el
juicio del Soberano. Y ningún veredicto entra a la mente/Códice sin clic humano —
la regla de cero falsos recuerdos aplica igual a lo que viene de fuera.

**Prohibido:** desplegar, abrir red saliente nueva, o pintar cualquier dato en el
dashboard antes de que 8.2 esté firmado.

---

## BLOQUE 9 · El agente que aletea — diagnóstico

**Estado:** ⬜ pendiente (nuevo, firmado 2026-08-02)
**Coste:** S · **Apalancamiento:** medio · alto valor doctrinal.

`6/6 agentes activos` → `5/6` → `6/6`, aproximadamente cada hora.
`hexelion_gateway.py:1635/1699`.

**Se elimina la causa. NO el indicador.** Si al terminar el bloque el contador ya no
parpadea *porque se suavizó el contador*, el bloque está fallado y hay que revertirlo.

### 9.1 · Instrumentar antes de tocar

Registrar cada transición con: timestamp UTC completo, **qué agente concreto** cae,
cuántos segundos dura la caída, y qué devolvió el healthcheck (timeout / excepción /
respuesta negativa). Sin ese log no hay diagnóstico, solo teoría.

### 9.2 · Hipótesis primaria, falsable

**El minuto es la prueba.** Si las caídas caen cerca del **minuto :07** de cada hora,
el sospechoso es el timer del Alquimista (`OnCalendar=*:07`, propose-only): el
proceso arranca, compite por CPU o toma el lock, y el healthcheck del gateway expira
justo ahí. Segundo sospechoso si el minuto no encaja: el pacing térmico (pausa
preventiva ≥78 °C) alargando una llamada más allá del timeout.

**Refutación:** si los minutos están dispersos, ambas hipótesis caen y toca mirar
reciclado de conexión / expiración de caché horaria en el propio gateway.

### 9.3 · Arreglo

Casi con seguridad el arreglo correcto **no** es un timeout más largo, sino
distinguir *ocupado* de *caído*. Un agente que tarda no es un agente ausente: el
panel debería poder decir `OCUPADO`. Proponer, no desplegar.

---

## BLOQUE 10 · Orden de misiones y rito de La Tierra

**Estado:** ⬜ pendiente (nuevo, firmado 2026-08-02)
**Coste:** M

### 10.1 · Medir precede a firmar — por prerrequisito, no por renumeración

Los identificadores `M0…M7` son **etiquetas**, no un orden. El orden vive en un grafo
de prerrequisitos. Renombrar volvió a costar caro (`M3_Baluarte_Cobre`→M6) y el
guardián de canon existe precisamente por eso.

**Implementación:** campo `requiere: [...]` en cada misión; el desbloqueo lo calcula
el grafo. La misión de la firma declara que **requiere La Tierra**. El número deja de
significar orden en toda la UI (nada de "misión 5 de 7" implicando secuencia).

### 10.2 · El rito de La Tierra — predicción previa

*"Rito horizonte por diseñar"* se resuelve con el mecanismo del Apéndice B:

1. El usuario **predice** la lectura del sensor (temperatura, presión, lo que sea)
   y la escribe. Sin predicción no se desbloquea la medición.
2. Se mide de verdad, con hardware real.
3. Se muestra el **hueco** entre predicción y medición — el hueco es la lección
   (efecto de generación, dificultades deseables; Bjork, ya citado en `PRIOR_ART.md`).
4. Solo entonces el dato se firma.

**Por qué este orden es doctrinalmente correcto:** firmar antes de medir es firmar la
palabra de otro. La Tierra es el primer momento en que el usuario produce un dato que
no existía antes de él; es el único punto donde *"doy fe"* tiene referente propio.
Ese es el rito, y es el mismo movimiento que IronClaw hace con el valor.

### 10.3 · Sonda única

La sonda física vive **solo** en M7. En M3 queda enlace, no paso ejecutable.
`missions.ts:115` congelado → CC propone diff, el Soberano firma.

---

## APÉNDICE A · Decisiones — FIRMADAS 2026-08-02

1. **Tres paneles en `NO DATA` permanente** → **DEUDA, se levanta.** Veredicto del
   Soberano: hay OSIRIS instalado en uno de los HP y el sistema entero está montado
   para verificación cruzada. Pasa a **BLOQUE 8**, con la condición de orden que
   allí se detalla: *el jurado antes que el feed*.
2. **El agente que aletea** → **se elimina la CAUSA, no el indicador.** Pasa a
   **BLOQUE 9**. Prohibido suavizar, promediar o silenciar el contador: eso sería
   fabricar un sensor deshonesto encima de un sensor honesto.
3. **Pedagogía de M7 / orden M5–M7** → **decidido: medir precede a firmar, y el
   orden se cambia por prerrequisitos, NO renumerando.** Ver 5.4 y BLOQUE 10.
4. **Sonda física duplicada** → **una sola sonda, y vive en M7 La Tierra.** En M3
   queda referencia, no paso ejecutable. `missions.ts:115` está congelado: CC
   **propone diff**, el Soberano firma.
5. **Temario LLM** → **cuatro correcciones aprobadas** (Apéndice B), obligatorias
   antes de integrarlo.
6. **`~/aurelius-lora/`** → **EN ESPERA** por decisión del Soberano hasta cerrar el
   resto de bloques. No se monta, no se toca, no aparece en reportes.

---

## APÉNDICE B · Correcciones al temario LLM — APROBADAS 2026-08-02

Las cuatro son obligatorias antes de integrar el temario. El Soberano las firmó
completas: el error doctrinal, el mecanismo que falta y las tres menores.

**Error doctrinal, obligatorio corregir.** El temario dice que la inyección de
prompts *"se mitiga tratando toda entrada externa estrictamente como texto
inerte"*. Eso es el **suelo falso** que ya se corrigió en `SAFE_PROMPTS.md`: la
demarcación es una capa, no un suelo. Si Aurelius lo enseña así, forma usuarios
que se creen protegidos por una capa que cede. El suelo es arquitectónico: el
modelo no tiene manos.

**Mecanismo que falta: predicción previa.** Un tooltip bien cronometrado sigue
siendo exposición, no recuperación. Antes de que el Oráculo muestre la RAM que
pide un modelo, Aurelius pregunta cuánta cree el usuario que es. El hueco entre
predicción y medición es donde ocurre el aprendizaje — efecto de generación y
dificultades deseables (Bjork), ya citado en `PRIOR_ART.md`.

**Tres menores:**
- LLaMA es open-*weight* con licencia restrictiva, no "ecosistema de pesos
  abiertos" sin más. Es la lección que llevó a elegir Qwen.
- RLHF: los humanos **ordenan** respuestas, se entrena un modelo de recompensa,
  y el RL va contra ese modelo — no contra los humanos directamente.
- **Falta calibración**: por qué un modelo está seguro cuando se equivoca. Es el
  concepto más importante para un principiante con modelo local, porque sin él
  confía justo en el momento en que no debe.

---

## APÉNDICE C · Cerrado con prueba (no revisitar)

Drawer de recursión (`c7816f6`: 10 ciclos, 104 nodos, desvío 0.00%, 0 iframes) ·
Canon M3 = Refugio (`ddddfb5`, `5acecb0`) · CI guardián de canon (`14f916f`) ·
M6 Baluarte (`91a591c`) · M7 La Tierra (`31597cf`) · rename `M3_Baluarte_Cobre`→M6
(`bddfe78`) · hijack DVB blacklisteado · EEPROM reprogramada · AIS vivo en El
Vigía · aviones pintando en tiempo real · M5Stack identificado a 115200 emitiendo
JSON · `preflight.sh` (`2305858`) · poller compartido resuelto · Aurelius
empujado por HTTPS.

*Un capítulo entero. Se registra antes de mirar lo que falta.*

---

## CHANGELOG

### v1.1.0 · 2026-08-02
- **Causa de la enmienda:** el documento existía como canon en el contexto del
  Preceptor y **nunca se escribió a disco**. CC paró correctamente (Regla de Parada
  §1) al no encontrarlo. La lección se canoniza en la nota de abajo.
- Front-matter §2 añadido (contrato del Protocolo del MD Evolutivo).
- Casa autoritativa declarada: `p0x/mente/backlog/`. Punteros desde los otros repos.
- Apéndice A: seis decisiones firmadas por el Soberano; deja de ser una lista de
  espera y pasa a ser un registro.
- BLOQUE 8 (verificación cruzada / OSIRIS+Jurado), BLOQUE 9 (aleteo del agente) y
  BLOQUE 10 (orden de misiones + rito de La Tierra) creados a partir de esas firmas.
- Apéndice B marcado como aprobado.

### v1.0.0 · 2026-08-02
- Creación. Bloques 0–7, invariantes, formato de reporte, apéndices A/B/C.

---

## NOTA · Lección de la ronda H+ (no repetir)

Este documento declara en su sección 0 que *"vive en el repo, no en el contexto de
ningún modelo"*. Durante una ronda entera **no fue cierto**: el Preceptor lo trataba
como canon y CC no podía leerlo.

**Regla derivada:** ningún artefacto es canon hasta que existe en disco, commiteado.
Lo que solo vive en un contexto es una propuesta, por bien redactada que esté. El
Preceptor **propone artefactos**; el Soberano los **escribe y firma**. Si el
Preceptor cita un documento que CC no puede abrir, el fallo es del Preceptor.
