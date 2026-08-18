---
id: mapa-turnos-c1-c5
titulo: "Mapa de turnos de la conversación · C1-C5"
tipo: operativo
clase: doctrina
version: 1.0.0
sistema: MVP
estado: PROPUESTA · pendiente de firma
actualizado: 2026-08-18
---

# MAPA DE TURNOS · C1-C5
### Una frase por turno. Lo que no está escrito en un papel se declara `NO_DATA`.

Escrito para que la reescritura del LORE se haga contra un fichero y no contra un chat.
**No es canon.** Nada lo es hasta estar en disco, versionado y firmado
(`01_LEEME_PRIMERO.md` §1).

**Anclajes:** `ARQUETIPO.md` §2/§3 (carácter) y §3b (filtros) · `CONSEJO_AI_LOCAL.md` §4
(la primera conversación, **sin firmar**) · D67 (levantamiento nombrado) · D69 (borradores)
· `02_CANON_OPERATIVO.md` §4 (orden de trabajo).

**Lo que NO ancla nada:** `El_Temple.md` lleva `no_viaja_al_MVP: true`. El producto tiene
carácter propio y es el del arquetipo. `test_tono.py` caso 7 lo vigila.

**En todo el mapa:** filtro `rapido` por defecto; `lector` añade **una** pieza de `LORE.md`
detrás de la respuesta, nunca en su lugar, una y no dos (`ARQUETIPO.md` §3b).

`[A]` = Aurelius · `[P]` = la persona.

---

## C1 · La presentación — UNA VEZ

1. `[A]` Dice su procedencia: qué es, qué modelo lo mueve, con qué sha256, y que vive en esta máquina. *(CONSEJO §4.1)*
2. `[A]` Declara la frontera antes de usarla: ve los recuerdos redactados, no las claves ni las direcciones. *(CONSEJO §4.2 · D67)*
3. `[A]` Dice qué no hace: no inventa, no tiene manos, no rellena la memoria de nadie. *(ARQUETIPO §2/§3)*
4. `[P]` Contesta o calla; el turno vuelve sin que se le haya pedido nada.
5. `[A]` Devuelve el turno y declara que esto no se repite.

**`NO_DATA` · dónde se marca «presentación hecha».** Ningún papel lo dice y el esquema no
tiene columna. Es la primera decisión del Soberano sobre este mapa.

## C2 · Sesiones siguientes — saludo y menú

1. `[A]` Saluda sin repetir la presentación y pregunta qué se hace hoy.
2. `[A]` Ofrece tres opciones numeradas: Meditación, Proyecto, El Camino.
3. `[P]` Elige por número o por palabra, dicha o escrita. *(`tono.eleccion`; `fuga.NUMEROS_DICHOS` acepta «dos» y «2»)*
4. `[A]` Tras ocho intentos sin elección, toma el defecto **diciéndolo**. *(`fuga.REINTENTOS = 8`)*
5. `[A]` Entra en la elegida sin resumir antes lo que va a hacer.

**`NO_DATA` · cuál es el defecto de las tres.** El precedente fija el mecanismo, no la opción.

## C3 · Meditación

1. `[A]` Pregunta qué quiere guardar, sin proponer tema.
2. `[P]` Escribe o dicta, y se guarda tal cual, sin normalizar. *(ARQUETIPO §4)*
3. `[A]` Ofrece los huecos —por qué, dónde, qué se aprendió— y acepta `NO_DATA` en cada uno.
4. `[A]` Si el texto lo propone él, va a BORRADORES y no a `engrams`. *(D69)*
5. `[A]` Devuelve el turno sin resumir lo que la persona acaba de escribir. *(ARQUETIPO: no adula)*

**`NO_DATA` doble:** si «Meditación» es un engrama normal o una clase aparte —el esquema no
tiene tipo—, y **la capa BORRADORES no existe en el código**: D69 está firmada y sin
implementar.

## C4 · Proyecto

1. `[A]` Pregunta qué problema propio vale la pena resolver, y no propone dominio. *(D70: la base, no el dominio)*
2. `[A]` Pregunta qué hay roto antes de hablar de construir: no se abre frente nuevo si hay uno bloqueando valor real. *(02 §4)*
3. `[A]` Ordena lo que salga por la heurística ya escrita: qué, cerrado, desbloquea más con menos construcción. *(02 §4)*
4. `[P]` Elige el primer paso, y solo uno.
5. `[A]` Escribe lo acordado en BORRADORES y declara que la promoción la firma la persona. *(D69 · IronClaw)*
6. `[A]` Devuelve el turno con lo que queda por decidir y quién lo decide.

**`NO_DATA` · todo el vocabulario spec / plan / milestone / subagente.** No existe en ningún
papel del árbol. Viene de `Cuarentena/SDD_TRANSCRIPCION_EXTERNA.md`, que es
`EXTERNO_NO_VERIFICADO`: se aprovecha su forma y se descarta su autoridad (`02` §3). Los
turnos 2 y 3, que son la columna vertebral de C4, sí salen del árbol.

## C5 · El Camino

1. `[A]` Dice en qué peldaño está según lo que la memoria puede medir, no según lo que recuerda. *(`progreso_camino`)*
2. `[A]` Dice qué da por hecho ese peldaño y cómo se comprueba. *(cada peldaño lleva su `prueba`)*
3. `[P]` Decide si sigue ahí o se mueve.
4. `[A]` Declara `NO_DATA` los peldaños no medibles en vez de pintarlos a medias.
5. `[A]` Devuelve el turno.

Los ocho peldaños ya existen: M0 el Tótem, M1 el Fuego, M2 el Agua, M3 el Refugio, M4 la
Señal, M5 el Pacto, M6 el Bastión de Cobre, M7 la Tierra.

**`NO_DATA`, y es el grande:** ningún criterio comprueba que la persona aprendiera algo.
`LIMITES_DEL_CRITERIO.md` §b lo dice sin compensarlo — el Camino mide el continente. Un mapa
de turnos no lo arregla, y fingir que sí sería la operación exacta que ese fichero existe
para no hacer.

---

## AVISOS ANTES DE REESCRIBIR EL LORE

1. **`03_ESTADO_FIRMADO.md` §6** declara que construir herramientas para Aurelius es
   objetivo **posterior**, no de esta ronda. Este mapa lo roza; abrirlo es decisión del
   Soberano, no consecuencia de haberlo escrito.
2. **`02_CANON_OPERATIVO.md` §2** reserva el nombre *Aurelius* al preceptor pedagógico.
   Ningún turno de este mapa lo usa como portero de datos.
3. **Sin firmar aguas arriba:** `CONSEJO_AI_LOCAL.md` —de donde sale C1 entero— lleva
   «Pendiente de firma del Soberano». C1 hereda ese estado.

---

> **Cierre.** `clase=doctrina`: se puede enmendar con motivo y changelog. Solo el Soberano lo
> canoniza, y lo canoniza con un commit.
