---
id: mision-mitocondria
clase: operativo
version: 1.0.0
fecha: 2026-08-04
metrica: reflejos que miden por su cuenta (objetivo → 1); transiciones espurias del contador de agentes (objetivo → 0)
umbral: no se re-edita sin el censo de F0 y sin siete días de metabolismo.jsonl
presupuesto_kb: 24
n_medicion: 7
enlaces: [doctrina-ai-interna, orquesta-modelos-p0x, backlog-ui-p0x]
---

# MISIÓN · LA MITOCONDRIA
### Un solo árbitro metabólico. Todos los reflejos preguntan; ninguno mide por su cuenta.
*Autor: el Preceptor · Canoniza: el Soberano · Ejecuta: CC*

---

## MOTIVO

Hoy el rack tiene varios reflejos que miden el mismo mundo y actúan sin saber unos
de otros: el pacing térmico previo a llamada LLM (78 °C), el guard de 80 °C en
batch, el timer del Alquimista (`OnCalendar=*:07`), los healthchecks del gateway,
la cola de `tsp`, los reflejos del M5. Cada uno lee sus propios sensores y decide
por su cuenta.

Eso no es redundancia: es **ausencia de árbitro**. Y el agente que aletea cada hora
es el síntoma visible — dos reflejos pisándose sin nadie que arbitre. El Bloque 9
diagnostica el síntoma; esta misión corrige la causa.

**Principio:** un solo lector de sensores, un solo veredicto publicado, y todos los
demás procesos **preguntan** en lugar de medir.

---

## LO QUE LA MITOCONDRIA **NO** ES (leer antes de diseñar)

- **No es tiempo real.** Nada de `SCHED_FIFO`, prioridades de kernel ni daemon en C.
  Aquí no se controla un motor: se decide si lanzar un job. Un servicio con
  systemd `Type=notify` + `WatchdogSec` da el 95 % del valor con el 5 % del riesgo.
- **No mata procesos, no apaga nada, no reinicia servicios en v1.** Publica un
  veredicto. Los consumidores obedecen. Un árbitro que además ejecuta es un único
  punto de fallo con manos.
- **No inventa funciones nuevas.** v1 consolida reflejos que ya existen. Si al
  terminar hay una capacidad que antes no estaba, la misión se desvió.
- **No toca valor.** IronClaw íntegro.

---

## EL CONTRATO (el corazón de la misión)

### Los tres estados

| Estado | Significado | Qué implica para quien pregunta |
|---|---|---|
| `LIBRE` | Hay margen térmico, de RAM y de energía | Se puede encolar y ejecutar con normalidad |
| `RESTRINGIDO` | Un recurso se acerca a su límite | No se inician trabajos pesados nuevos; los vivos terminan |
| `EMERGENCIA` | Un recurso está en su límite | Solo lo imprescindible; el resto espera |

Tres estados y no cinco: cada estado extra multiplica los casos de prueba y ninguno
de los dos que sobran corresponde a una decisión real que alguien tome hoy.

### El veredicto publicado

Una sola clave, legible por todo el rack, con **al menos** estos campos:

- `estado` — uno de los tres.
- `motivo` — qué recurso lo causó, en texto legible (`zone0=79.4C`).
- `desde` — timestamp de entrada en el estado actual.
- `edad_lectura` — antigüedad de la medición que lo sostiene, **no** del render.
- `nodo` — el veredicto es **por nodo**. La Fragua y La Torre no comparten cuerpo.

**Honest sensors, sin excepción:** si el sensor no responde, el estado es
`NO DATA`, jamás `LIBRE`. Un árbitro ciego que dice "adelante" es peor que ningún
árbitro. Y `NO DATA` se trata como `RESTRINGIDO` por el consumidor prudente.

### Histéresis asimétrica

Degradar rápido, recuperar lento. Entrar en `RESTRINGIDO` es inmediato; salir exige
que la condición se mantenga sana durante una ventana. Sin esto, el propio árbitro
oscila — y habríamos reproducido el aleteo un piso más arriba.

Los umbrales de la ventana **no se decretan**: salen de F1 con datos reales.

---

## FASES

### F0 · El censo (primero, y puede cambiar el diseño)

Inventario **medido** de todo lo que hoy lee un sensor o toma una decisión de carga
en el rack: qué proceso, qué lee, cada cuánto, qué hace con ello, y en qué fichero
y línea vive. Incluye timers de systemd, cron, guards embebidos en código y
healthchecks.

Sin este censo no hay misión: no se puede unificar lo que no está contado. Salida a
`mente/auditorias/reflejos.md`.

### F1 · El lector único

Un servicio que lee los sensores del nodo y escribe `metabolismo.jsonl` — **sin
publicar veredicto todavía y sin que nadie lo consuma**. Corre en paralelo a los
reflejos actuales durante al menos **siete días**.

Objetivo: la línea base. Cuántas veces al día se habría entrado en cada estado, con
qué duración, y qué umbrales tienen sentido en este rack y no en un rack imaginario.
Telemetría antes que opinión.

### F2 · El veredicto

Con los datos de F1, se fijan umbrales y ventanas de histéresis, **cada uno citando
la línea de telemetría que lo justifica**. El servicio empieza a publicar. Nadie lo
consume todavía.

### F3 · Migración de consumidores, de uno en uno

Cada reflejo del censo deja de medir y pasa a preguntar. **Un commit por reflejo,
verificando el comportamiento después de cada uno.** Migrar dos a la vez hace
imposible saber cuál rompió qué.

Orden sugerido: primero el guard de batch (el más aislado), luego el pacing térmico
del gateway, luego el timer del Alquimista, y los healthchecks al final.

### F4 · Retirada de las mediciones duplicadas

Solo cuando un consumidor lleva tiempo funcionando por veredicto se le quita su
lectura propia. Nunca antes. El código muerto se borra, no se comenta.

### F5 · Verificación

**El criterio de éxito de toda la misión, en una frase:**

> El contador de agentes deja de aletear **sin que nadie haya tocado el contador**.

Si el aleteo persiste, la Mitocondria no era la causa y el Bloque 9 sigue abierto —
y eso también es un resultado válido que se registra. Si el aleteo desapareció
porque alguien suavizó el indicador, la misión está **fallada** y se revierte.

---

## INVARIANTES

- Propose-only en infraestructura: CC no despliega, no reinicia, no hace push.
- Un commit por fase, mínimo; uno por consumidor migrado en F3.
- Ningún umbral sin línea de telemetría que lo justifique.
- `NO DATA` nunca se degrada a `LIBRE`.
- Español interno; nombres de estado en el código, en español, coherentes con el
  resto del rack.
- Backup antes de tocar cualquier consumidor vivo.
- PARA y reporta al final de **cada fase**. No se encadenan.

---

## PROMPT PARA CC (una fase por sesión)

```
MISIÓN · LA MITOCONDRIA, fase F<n>.
Lee mente/misiones/MISION_MITOCONDRIA_P0X.md entero antes de tocar nada,
incluida la sección "LO QUE LA MITOCONDRIA NO ES".

Ejecuta SOLO la fase F<n>. Respeta las INVARIANTES.
Si un umbral te hace falta y no tienes telemetría que lo justifique, PARA:
decretarlo por intuición es exactamente lo que esta misión existe para eliminar.

Reporta en formato de 12 líneas. Cierra con 3-6 SUGERENCIAS (S/M/L) anexadas a
mente/feedback/PENDIENTES.md. PARA. No encadenes fases.
```

---

## CHANGELOG

**v1.0.0 (2026-08-04)** · Creación. Destilado de la propuesta externa "Mitocondria
Maestra" (documento de deliberación, no canon), purgando el daemon en C con
`SCHED_FIFO`, los cinco tiers metabólicos y la cadena de kill automática. Se
conserva la forma — un árbitro, un veredicto, consumidores que preguntan — que es
donde estaba el valor.
