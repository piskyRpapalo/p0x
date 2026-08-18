---
id: lore-evolutivo-base-nombres
titulo: "Lore evolutivo · base de nombres del modo campaña"
tipo: operativo
clase: doctrina
version: 1.0.0
sistema: MVP
estado: PROPUESTA · pendiente de firma
scopes: P2 producto · P3 preceptor (ausente) · P1 referencia · D doctrina
actualizado: 2026-08-19
---

# LORE EVOLUTIVO · BASE DE NOMBRES
### El reglamento del juego cuya mecánica es la doctrina ya probada.

**La ley bidireccional, tal como la fijó el Soberano:** *si el Narrador lo dice, el código lo
mide; si el código lo mide, el Narrador lo puede decir.*

**Y lo que esa ley obliga a decir antes de la primera tabla.** `cara.py::progreso_camino`
mide hoy **dos** de los ocho peldaños: `M0` desde el perfil y `M2` desde recuerdos y sello.
`M1` está declarado `"no_medible"` con su motivo escrito —el cerebro no vive dentro del
producto— y **`M3`, `M4`, `M5`, `M6` y `M7` están fijos en `"sin_empezar"`**: ninguna línea
los calcula. Seis de ocho no se miden. Sus nombres entran igual en esta base, marcados, para
que se vea qué falta construir; el Narrador no puede pronunciarlos como estado hasta que algo
los mida.

Todo lo de aquí sale de `find`/`grep` sobre el árbol el 2026-08-19.

---

## §1 · LA TABLA MAESTRA

### 1.1 · Mecánicas — funciones que se disparan en campaña

| interno | alias_narrativo | scope | fuente_real | prueba_narrativa |
|---|---|---|---|---|
| `memory.cruzar_frontera` | **La Cicatriz** | P2 | tree | «Algo quiso salir. Lo miré, y queda escrito qué lo paró.» |
| `memory.escribir_engrama` | **Inscribir una Piedra** | P2 | tree | «Queda inscrito con tus palabras. No las he tocado.» |
| `memory.leer_engrama` | **Recordar** | P2 | tree | «Esto lo escribiste tú.» |
| `memory.proponer_borrador` | **El Cuaderno se abre** | P2 | tree | «Te propongo esto. No es tuyo hasta que lo firmes.» |
| `memory.promover_a_engrama` | **El Aprendiz firma la Piedra** | P2 | tree | «Lo has firmado. Ahora es memoria.» |
| `memory.descartar_borrador` | **El Aprendiz tacha** | P2 | tree | «Tachado. La hoja se queda: tachar no es arrancar.» |
| `memory.leer_borradores` | **Leer el Cuaderno** | P2 | tree | «Esto es lo que te he propuesto y sigue esperando.» |
| `memory.registrar_salida` | **Dejar Huella** | P2 | tree | «Queda la huella de lo que salió.» |
| `memory.resumen_salidas` | **El Registro de Huellas** | P2 | tree | «Esto salió, y esto se paró. Puedes enseñarlo entero.» |
| `memory.exportar` | **Llevarse la Piedra** | P2 | tree | «Aquí está, redactado. Es tuyo y se va contigo.» |
| `memory.importar` | **Piedra de otro sitio** | P2 | tree | «Viene de otra máquina. Conserva de dónde vino.» |
| `memory.archivar` / `desarchivar` | **Guardar / Devolver a la luz** | P2 | tree | «No se borra. Se guarda, y vuelve cuando la llames.» |
| `memory.vista_arbol` | **El Árbol de Piedras** | P2 | tree | «Así se sostiene lo que llevas.» |
| `memory.vista_recuento` | **La Cuenta** | P2 | tree | «Tantas piedras, tantos huecos declarados.» |
| `memory.recuento_huecos` | **Los Huecos** | P2 | tree | «Esto sigue sin contestar. No es un fallo: es una pregunta abierta.» |
| `memory.escribir_enlace` | **Tender un Sendero** | P2 | tree | «Estas dos se tocan, y ya lo dice el mapa.» |
| `memory.respaldar` / `restaurar` | **La Copia Lejana** | P2 | tree | «Una copia al lado del original no es una copia.» |
| `memory.asegurar_tablas` | **Ensanchar la Casa** | P2 | tree | «Tu memoria es más vieja que esto. Le he hecho sitio sin tocar nada.» |
| `memory.mision_completa` | **El Sello** | P2 | tree | «Está sellado.» |
| `hilos.abrir` | **Abrir un Sendero** | P2 | tree | «Queda abierto. No hace falta cerrarlo hoy.» |
| `hilos.cerrar` | **Cerrar un Sendero** | P2 | tree | «Cerrado.» |
| `hilos.reabrir` | **Volver al Sendero** | P2 | tree | «Vuelve a estar abierto. Nadie te ha quitado el sitio.» |
| `hilos.aviso_sin_cerrar` | **El Sendero espera** | P2 | tree | «Hay senderos abiertos. El más viejo lleva un tiempo.» |
| `cara.progreso_camino` | **El Peldaño** | P2 | tree | «Estás aquí, y esto es lo que se puede medir de aquí.» |
| `fusible.inspeccionar` | **El Fusible** | P2 | tree | «Eso tiene forma de algo que quema.» |
| `fusible.preparar_respuesta` | **El Fusible salta** | P2 | tree | «No paso eso. La forma es peligrosa.» |
| `traza.generar` | **La Traza** | P2 | tree | «Qué entró, qué regla saltó, y qué decidí. Nada más.» |
| `guardrails.redactar_salida` | **El Velo** | P2 | tree | «Va cubierto. Digo la clase y cuántas veces, nunca el trozo.» |
| `andamio.ensamblar` | **Levantar el Andamio** | P2 | tree | «Te monto la pregunta. Léela antes de usarla.» |
| `andamio.marcar_inspeccionado` | **Mirar el Andamio** | P2 | tree | «Lo has mirado. Ahora puede salir.» |

### 1.2 · Entidades — tablas que son conceptos del mundo

| interno | alias_narrativo | scope | fuente_real | prueba_narrativa |
|---|---|---|---|---|
| `engrams` | **Las Piedras** | P2 | tree | «Lo que has inscrito.» |
| `borradores` | **El Cuaderno del Game Master** | P2 | tree | «Lo que te he propuesto. Ninguna es tuya hasta que la firmes.» |
| `links` | **Los Senderos entre Piedras** | P2 | tree | «Lo que has decidido que se toca.» |
| `hilos` | **Las Sagas abiertas** | P2 | tree | «Lo que empezaste y sigue vivo.» |
| `hilos_eventos` | **La Crónica del Sendero** | P2 | tree | «Abierto, cerrado, reabierto. Los tres siguen ahí.» |
| `salidas` | **Las Huellas** | P2 | tree | «Todo lo que cruzó, y todo lo que no.» |
| `profile` | **El Espejo del Aprendiz** | P2 | tree | «Esto es lo que me has dicho de ti. Lo demás está en blanco, y se ve.» |

### 1.3 · Leyes del mundo — invariantes con su rojo

| interno | alias_narrativo | scope | fuente_real | prueba_narrativa |
|---|---|---|---|---|
| V6 · `test_traza` | **La Cicatriz no miente** | P2 | tree | «Lo que se paró deja marca. Lo que se paró no se guarda.» |
| U7 · `test_hilos` | **El Nombre Protegido** | P2 | tree | «Tu sendero sale, pero su secreto va cubierto.» |
| P-a/P-d · `test_puerta` | **No hay puerta trasera** | P2 | tree | «Solo hay una salida, y pasa por delante de ti.» |
| P-f · `test_puerta` | **Tu «no» no se anota** | P2 | tree | «Has dicho que no. Eso es tuyo, y no queda escrito.» |
| B-b · `test_borradores` | **Solo el Aprendiz firma la Piedra** | P2 | D69 · tree | «Yo no puedo firmarla. Para eso estás tú.» |
| B-c · `test_borradores` | **Tachar no es arrancar** | P2 | D69 · tree | «La hoja tachada se queda.» |
| D67 | **Lo que sale, sale cubierto** | D | tree | «Nombro lo que voy a descubrir, y decides tú, una por una.» |
| Cero DELETE | **Nada se arranca** | P2 | tree | «Aquí no se borra. Se archiva.» |
| `NO_DATA` | **El Silencio Honesto** | D | tree | «No lo sé. Eso también es un dato.» |

### 1.4 · Pedagogía — el andamiaje, con su cita

| interno | alias_narrativo | scope | fuente_real | prueba_narrativa |
|---|---|---|---|---|
| `dry_run_obligatorio` · Sweller 1988 | **El Ensayo en Seco** | D | teach | «Antes de que pase de verdad, mira lo que va a pasar.» |
| `fallo_como_ramificacion` · Kapur 2008 | **El Fallo abre camino** | D | teach | «No ha salido. Y por aquí se sigue.» |
| `ancla_objetivo_macro` · Sweller/Chandler | **La Estrella Fija** | D | teach | «Esto es a lo que ibas. Sigue ahí.» |
| `scaffolding_fading` · Wood/Bruner/Ross 1976 | **El Andamio que se retira** | D+P2 | teach | «Ya no hace falta que te lo explique.» |
| Roediger & Karpicke 2006 | **Recordar en voz alta** | D | teach | «Dímelo tú antes de que te lo diga yo.» |

### 1.5 · Los peldaños del Camino

| interno | alias_narrativo | scope | fuente_real | ¿lo mide el código? |
|---|---|---|---|---|
| `M0` El Tótem | **El Tótem** | P2 | tree | **Sí** · perfil: `device` y `name` |
| `M1` El Fuego | **El Fuego** | P2 | tree | **No** · declarado `"no_medible"`, con motivo |
| `M2` El Agua | **El Agua** | P2 | tree | **Sí** · recuerdos + sello |
| `M3` El Refugio | **El Refugio** | P2 | tree | **No** · fijo en `"sin_empezar"` |
| `M4` La Señal | **La Señal** | P2 | tree | **No** · fijo en `"sin_empezar"` |
| `M5` El Pacto | **El Pacto** | P2 | tree | **No** · fijo en `"sin_empezar"` |
| `M6` El Bastión de Cobre | **El Bastión de Cobre** | P2 | tree | **No** · fijo en `"sin_empezar"` |
| `M7` La Tierra | **La Tierra** | P2 | tree | **No** · fijo en `"sin_empezar"` |

---

## §2 · LAS FRASES DEL NARRADOR, PELDAÑO A PELDAÑO

Una por peldaño, en los dos idiomas, con el registro del arquetipo: cortas, llanas, sin
listas ni exclamaciones, dichas para ser leídas en voz alta.

**Las dos primeras se pueden decir hoy. Las seis siguientes no**, y van marcadas: pronunciar
un estado que nada mide es exactamente la barra de carga falsa que `cara.py` dice no querer
ser.

**M0 · El Tótem** — *medible*
> You put your name to this. Nothing here moves until you do.
> Le has puesto tu nombre. Aquí no se mueve nada hasta que lo haces tú.

**M1 · El Fuego** — *no medible, y se dice*
> There is no way for me to tell from here whether the fire is lit. I will not guess.
> Desde aquí no puedo saber si el fuego está encendido. No lo voy a suponer.

**M2 · El Agua** — *medible*
> The first stone is cut. What you wrote stayed exactly as you wrote it.
> La primera piedra está tallada. Lo que escribiste quedó como lo escribiste.

**M3 · El Refugio** — `NO_DATA` *(nada lo mide)*
> Six rooms, and none of them asks you to hurry.
> Seis salas, y ninguna te pide prisa.

**M4 · La Señal** — `NO_DATA`
> Something of yours crossed, and you saw it leave.
> Algo tuyo cruzó, y lo viste salir.

**M5 · El Pacto** — `NO_DATA`
> You left a path open. Open is a state, not a debt.
> Dejaste un sendero abierto. Abierto es un estado, no una deuda.

**M6 · El Bastión de Cobre** — `NO_DATA`
> Something was stopped. The mark stays; what was stopped does not.
> Algo se paró. Queda la marca; lo parado, no.

**M7 · La Tierra** — `NO_DATA` *(y el andamio no se retira: sin implementar)*
> From here on I explain less, because you need it less.
> A partir de aquí explico menos, porque te hace menos falta.

---

## §3 · EL GUIÓN DE LA REVELACIÓN

Al firmar M7. Una declaración, sin prosa.

> The campaign is over. What you have is not a certificate: it is a body — a memory that
> does not lie, a border you can see, and a notebook you are the only one who signs.
> Now the question. What problem of your own is worth solving?

> La campaña se acabó. Lo que tienes no es un diploma: es un cuerpo — una memoria que no
> miente, una frontera que se ve, y un cuaderno que solo firmas tú.
> Ahora la pregunta. ¿Qué problema tuyo vale la pena resolver?

**Y la línea que la sigue, que es la que hace game master al Narrador** (R5: no propone
dominio):

> I will not tell you what to build. I will tell you what just happened, every time.
> No te voy a decir qué construir. Te voy a decir qué acaba de pasar, cada vez.

---

## §4 · CONTRADICCIONES DECLARADAS

**1 · Seis de ocho peldaños no se miden.** `M1` es `"no_medible"` declarado; `M3`–`M7` están
fijos en `"sin_empezar"` en `cara.py::progreso_camino`. La campaña que describe el modo tiene
ocho actos y el código puntúa dos. Por la ley bidireccional, el Narrador **no puede** narrar
M3–M7 como estado hasta que exista lo que los mida. Sus nombres quedan en la tabla como
encargo, no como mecánica.

**2 · La campaña asigna los peldaños distinto que el árbol.** El flujo del Soberano pone la
fuga de seis salas en M2 y el silencio en M3. El árbol dice lo contrario: `memory.py` se
declara *«M2 · el Agua · la memoria»*, `cara.py` *«M2 · la cara»*, y `fuga.py` *«M3 ·
HEGEMONIKON»* con sus seis salas; el `CAMINO` de `cara.py` nombra M3 = El Refugio. Además,
`progreso_camino` mide M2 con recuerdos y sello, que es memoria, no fuga. **Manda el árbol**,
o se cambia el árbol a propósito y con commit — pero no las dos cosas a la vez.

**3 · El andamio no se retira.** M7 es *Scaffolding Faded* en el diseño (platzi §3.11,
`teaching_kernel.yaml`), y **no hay código que lo haga**. Hoy el peldaño final del juego es
una promesa.

**4 · Subagentes contra IronClaw.** Un game master que ejecuta con subagentes que escriben y
promueven sin firma humana viola el suelo. El Narrador propone en el Cuaderno; firmar es del
Aprendiz, siempre.

**5 · Servidor local contra D68, framework contra biblioteca estándar.** Ya declaradas en
`SDD_TRANSCRIPCION_EXTERNA.md` §4. El lore no las puede narrar como si fueran del árbol.

**6 · La cita no dice lo que la hipótesis necesita.** El encargo apoya el RPG en Roediger &
Karpicke 2006. Ese trabajo sostiene la **práctica de recuperación y el espaciado**; no dice
nada sobre rol narrativo ni sobre protagonismo. Y el mismo `teaching_kernel.yaml` trae a
Sweller, cuya teoría predice que una narrativa que no sea *germane* **añade** carga, no la
baja. La hipótesis del Soberano puede ser cierta —está bien planteada y él mismo la sostiene
sin decretarla—, pero hoy su fuerza de evidencia es `heuristica_campo`, no la de un trabajo
firmado. Por la regla de `mente/corpus/_INDICE.md`, entra con `fuente` y `evidencia_fuerza`
honestos o no entra. **Esto no tumba el modo campaña: le pone su etiqueta.**

---

## §5 · NO_DATA

- **Qué mide M3–M7.** No existe. Es la primera pieza a construir si el modo campaña va en serio.
- **Qué cuenta como «firmar M7»** para disparar la revelación y el retiro del andamio.
- **Dónde vive el Narrador en el código.** No hay módulo narrador; hoy los textos están en
  `textos.py` y en `CARA_TEXTOS` de `cara.py`. La capa de alias no existe.
- **El corpus de psicología** sigue **vacío a propósito**: *«es el encargo, no el resultado»*.
  ZDP, currículum en espiral, Piaget y Papert tienen cero apariciones verificadas y **no se
  usan**.
- **El Preceptor (P3) no existe.** Todo lo de esta base vive en P2 y funciona sin él.
- **La campaña promete «hiciste», no «aprendiste».** `LIMITES_DEL_CRITERIO.md` §b: los
  criterios miden el continente, y no se compensa.

---

> `clase=doctrina`, estado PROPUESTA. Ni `LORE.md` ni `ARQUETIPO.md` se han tocado.
> Nada es canon hasta el commit del Soberano.
