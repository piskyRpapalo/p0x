---
id: tecnica-reflejo-bateria
titulo: "Reflejo-bateria — UPS en batería pausa la cola batch"
tipo: tecnica
clase: operativo
nivel: vivo
enlaces:
  - proyecto-reflejos
  - energia-solar
  - edge-ai
metrica_exito: "al entrar la UPS en OB/LB la cola batch (tsp) deja de arrancar trabajo nuevo en < 20s, sin oscilar en el borde, y rearma sola al volver OL estable"
umbral_reedicion: "cambio de UPS/driver NUT, cambio del mecanismo de la cola, o un episodio real que revele un fallo del arco"
actualizado: 2026-07-11
descripcion_niveles:
  basico: "Si se va la luz y el sistema pasa a funcionar con la batería, este reflejo frena automáticamente los trabajos pesados en cola para no gastar batería en tareas que pueden esperar. Cuando vuelve la corriente, los reanuda solo."
  medio: "Watcher determinista que lee el estado de la UPS por NUT (OB=en batería, LB=batería baja, OL=en red) y, al disparar, pone la cola batch (task-spooler) en 0 slots para que no arranque trabajo nuevo. Con histéresis: rearma solo tras varias lecturas OL seguidas, no en un parpadeo. Sin LLM en el lazo."
  experto: "Arco espinal (Pista A del Proyecto Reflejos): sensor→umbral→acción protectora→consola, sin córtex. Sensor real vía `upsc greencell` (honest-sensors); máquina de estados ARMADO↔DISPARADO con un solo disparo por episodio y rearme tras N lecturas OL consecutivas (anti-oscilación). Acción: compuerta+hold sobre task-spooler (ocupa el único slot, frena nuevos, respeta el job en curso) porque `tsp -S 0` no pausa (mínimo 1 slot); se libera al rearmar. Evento a la Bitácora Live (Redis `hexelion:bitacora:live`, etiqueta REFLEX ámbar) y registro estructurado en `mente/telemetria/reflejos.jsonl`. El servicio es propose-only (unit `deploy/fragua/reflejo-bateria.service`, no habilitada)."
---

# Reflejo-bateria

**Reflejo determinista #1 de la Pista A** (el Reflejo-0 es el pacing térmico #20).
Protege la autonomía del rack: cuando la UPS pasa a batería, los trabajos pesados
encolados pueden esperar; no tiene sentido drenar la batería en un job de 40 min
de Whisper mientras el Faro/Gateway (valor) deben seguir vivos.

## Disparo (sensor real — honest-sensors)
- Fuente: NUT, `upsc greencell` (driver `blazer_usb`, pollinterval 15s).
- Variable: `ups.status`. **Dispara** si contiene `OB` (on battery) o `LB`
  (low battery). **Rearme** cuando vuelve a `OL` (online) de forma estable.
- Se leen además `battery.charge` e `input.voltage` para el campo `valor` del
  registro (no deciden; solo contextualizan el evento).

## Umbral e histéresis (que no oscile en el borde)
- Estados: `ARMADO` (OL) ↔ `DISPARADO` (OB/LB).
- `ARMADO → DISPARADO`: a la **primera** lectura OB/LB. Un solo disparo por
  episodio (mientras siga DISPARADO no repite la acción).
- `DISPARADO → ARMADO` (rearme): solo tras **N lecturas OL consecutivas**
  (`REARME_OL_CONSECUTIVAS`, por defecto 3 ≈ 45s con sondeo de 15s). Un parpadeo
  OL aislado NO rearma.

## Acción protectora (jamás valor)
- Al disparar: **compuerta + hold**. Se crea `/tmp/reflejo-bateria.hold` y se
  encola una compuerta (`tsp -L reflejo-hold`) que ocupa el único slot (FIFO)
  mientras exista el hold. Así la cola batch no arranca ningún trabajo NUEVO; el
  que esté en curso se respeta (no se mata).
- Al rearmar: se retira el hold; la compuerta sale de su bucle (~3s), libera el
  slot y la cola vuelve a arrancar trabajo.
- **Por qué no `tsp -S 0`**: task-spooler impone mínimo 1 slot ("You should set
  at minimum 1 slot"); `-S 0` no pausa. La compuerta es el patrón idiomático y
  medido (test 2026-07-11: PROBE-C esperó detrás de la compuerta y solo corrió
  al liberar el hold).
- Idempotente: si el watcher reinicia con la UPS aún en OB, no encola una
  segunda compuerta (comprueba si ya hay una viva). `/tmp` es efímero: un reboot
  limpia hold+compuerta y el watcher renace ARMADO.

## Registro y consola
- Evento a la **Bitácora Live** (Redis `hexelion:bitacora:live`, tipo `reflex`,
  etiqueta **REFLEX** ámbar en el dashboard).
- Registro estructurado en **`mente/telemetria/reflejos.jsonl`**:
  `{ts, reflejo, disparo, valor:{status,battery_charge,input_voltage}, accion, ms}`.

## Fuera del arco (IronClaw)
- El watcher es un **proceso autónomo**: ni el gateway ni ningún LLM están en el
  lazo. El **Monje NARRA** este reflejo si se le pregunta (dato de su contrato),
  post-hoc; jamás lo ejecuta ni lo decide.
- Servicio = **propose-only**: unit `deploy/fragua/reflejo-bateria.service`
  PROPUESTA, no habilitada (veto clasificador al silicio; firma del Soberano).

## Arco
- Watcher: `deploy/fragua/reflejo_bateria_watch.py`
- Test vivo (sin cortar corriente real): `--test-seq OB,OB,OL,OL,OL` inyecta la
  secuencia en la MISMA máquina de estados; las acciones reales SÍ se ejecutan.
