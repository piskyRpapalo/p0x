---
id: plan-cierre-hexelion
titulo: Plan de cierre de p0x/hexelion + preparación del despliegue del BLOQUE 9
tipo: operativo
clase: operativo
editor_autorizado: silicio-telemetria
actualizado: 2026-08-04
---

# Plan de cierre · ronda HP-HEXELION-1 (2026-08-04)

> **ACTUALIZACIÓN · ronda HEXELION-CLOSE-1 (2026-08-04, mismo día).**
> **BLOQUE 9 DESPLEGADO** en La Fragua y verificado: unidad `active`, `NRestarts` estable en 0 con
> el mismo PID, `/api/sinodo` sirviendo, dashboard en pie. La trampa del §2 era real y se cumplió
> tal cual: el `git pull` **no habría entrado** porque `hexelion_gateway.py` estaba modificado sin
> commitear en La Fragua (dos URLs cableadas sustituidas por `{AIS_BASE}`, trabajo del Soberano
> nunca commiteado). Se apartó con `stash`, se hizo el `pull` y se **reaplicó**; conviven los dos
> cambios, sin conflictos y `py_compile` OK. Copia de seguridad previa en `/tmp` del nodo.
> Ese cambio **sigue sin commitear** y debería commitearse antes de que otro `pull` lo pise.
> **La clave `hexelion:sinodo:flaps` aún no existe**, y es lo correcto: solo se escribe cuando hay
> una transición. La prueba de honestidad (§2) sigue pendiente y necesita ≥2 h de ventana.
> HP-01 queda **inhabilitado**; HP-02 **limpio** y reconvertido a nodo de rack. Detalle de nodos en
> `hexelion/DEPIN_INVENTORY.md` (sección 2026-08-04).

Todo lo de aquí está **medido hoy**, no recordado. Higiene: sin IPs ni claves; los nodos van por
nombre y los comandos exactos (con usuario y host) viven en el reporte al Soberano, no versionados.

## 0 · Lo que el reconocimiento cambió respecto de lo que creíamos

Tres supuestos del canon cayeron al medirlos:

1. **`musculo-hp-02` no es un músculo.** `sys_vendor=Google`, `product=Dratini`: es un Chromebook
   reconvertido a Debian 12. Intel i5-10310U, **7.6 GiB de RAM**, disco eMMC, **sin GPU**,
   governor `powersave`. No puede alojar toolchain de entrenamiento ni servir un modelo de 30B.
   El canon (`CLAUDE.md`, «musculo-hp-01/02 (x86) · Toolchain de entrenamiento») está desfasado.
2. **`musculo-hp-02` NO es OSIRIS.** No hay `/opt/osiris`, `/srv/osiris` ni `~/osiris`; el home
   está vacío y no hay unidad alguna de p0x/hexelion. Solo dos contenedores ajenos al rack:
   `uptime-kuma` (sano, :3001) y `earn_sdk` (`titanhub/earn-sdk`, `restart=no`).
3. **OSIRIS vive en `musculo-hp-01`**, que la tailnet reporta **offline desde hace 10 días**. Eso
   concuerda con la URL que el gateway consume para GDELT. El motivo real no es «Tailscale no
   resuelve la IP»: el nodo lleva 10 días fuera de la tailnet y no responde a ICMP.

## 1 · Estado real por bloque, con la dependencia que lo bloquea

### BLOQUE 1 · M5 → Redis · **NO desplegado, y lo que hay en su lugar está roto**

Lo esperado era «instalar el puente». Lo medido es peor y más interesante:

- El Vigía **ya corre** `p0x-m5-ingest.service` (activo desde el 02-ago 17:45) ejecutando
  `~/p0x-telemetry/ingest_m5.py` — **otro fichero** que el del BLOQUE 1 (106 líneas frente a 111;
  md5 distinto). El M5 está conectado y visible por `by-id`.
- Ese puente lleva desde entonces **en bucle de reintento**: `[ingest_m5] Redis caído: Timeout
  connecting to server; reintento en 10s`. **No fluye ni un dato.**
- Escribe a `REDIS_HOST = "localhost"` **cableado a fuego**. La directriz firmada del 6.1 exige lo
  contrario: el puente publica en el Redis de **La Fragua**, que es donde lee el gateway.
- Único rastro en Redis: `hexelion:telemetry:m5:scan`, **sin TTL**, rancia del 02-ago. Es
  exactamente el antipatrón que la casa prohíbe: una clave que sobrevive sin declarar antigüedad.
- La versión del BLOQUE 1 (`216ca9e`) **sí** es la correcta: `HEX_REDIS_HOST` por entorno y
  `SETEX` con TTL 30s, de modo que si el M5 calla la clave expira y el gateway ve `sin_dato`.

**Conflicto a resolver antes de desplegar:** los dos puentes leen el mismo `/dev/ttyUSB0`. No
pueden convivir. Desplegar el BLOQUE 1 exige **parar y deshabilitar** `p0x-m5-ingest.service`
primero, y borrar la clave `:scan` huérfana. Un despliegue ingenuo choca con el puerto serie.

**Próxima acción:** parar el puente viejo · instalar `ingest_m5.py` + `m5-bridge.service` con
`HEX_REDIS_HOST` apuntando a La Fragua · prueba de honestidad.

### BLOQUE 6 · Le Jardin · **bloqueado por el 1**

6.1 no se puede verificar sin datos reales del M5, y hoy no hay ninguno. 6.2/6.3 cerrados; 6.4
seguirá `NO DATA` sin doc de roadmap. **Próxima acción:** ninguna hasta que el 1 esté vivo.

### BLOQUE 8 · OSIRIS · **bloqueado por hardware ausente, no por trabajo**

8.1 exige inventariar OSIRIS *medido*: repo, versión, commit, runtime, claves, cuotas. Vive en
`musculo-hp-01`, offline 10 días. **Ninguna cantidad de trabajo desde aquí lo desbloquea.**
8.2 (contrato del Jurado) está firmado y **no depende de OSIRIS**.

**Próxima acción:** separar 8.3 (escribir el motor del Jurado contra el contrato firmado) del
inventario 8.1, que queda congelado hasta que el nodo vuelva. Decisión del Soberano.

### BLOQUE 9 · El agente que aletea · **listo para desplegar, con una trampa**

`68a39a8` está **empujado** y contiene solo `hexelion_gateway.py` (+36 líneas). Pero:

- El clon de La Fragua está en `a33eb07`, **18 commits por detrás**. `a33eb07` es ancestro de
  `68a39a8`, así que basta `git pull`.
- **La trampa:** `hexelion-gateway.service` está **en bucle de fallo desde hace ~44 h**
  (`restart counter 16026`, ~1.4 s de CPU por intento). Lo que de verdad sirve el :8001 es un
  proceso **manual** lanzado con `setsid` el 02-ago desde una sesión interactiva, fuera de
  systemd (`session-877.scope`).
- Causa del bucle, reproducida ejecutando el `ExecStart` exacto a mano:
  `ERROR: [Errno 98] error while attempting to bind on address ('0.0.0.0', 8001): address already
  in use`. No es el footgun del PATH: `uvicorn` **sí** es importable por `/usr/bin/python3` (0.29.0).

**Por qué importa:** un despliegue ingenuo (`git pull` + `systemctl restart`) habría parecido
correcto y **no habría desplegado nada** — el proceso manual seguiría sirviendo el código viejo, y
el diagnóstico del parpadeo se habría hecho sobre un gateway sin instrumentar.

**Próxima acción:** ver §2.

### BLOQUE 10 y 5.4 · Sonda física · **decisión, no trabajo**

5.4 dice «congelada, sin cambio de código»; 10.3 dice «solo M7, en M3 queda enlace → CC propone
diff». Verificado en `aurelius/src/missions.ts`: el paso de la sonda **sigue** dentro de M3 y M7
existe. **5.4 está superado por 10.3.** Hasta que el Soberano firme cuál vale, no se toca.

## 2 · Despliegue del BLOQUE 9 — preparado, NO ejecutado

Orden obligatorio. El paso 2 es el que nadie habría escrito sin medir.

1. **Traer el código** (18 commits, incluye `68a39a8`): `git pull` en `~/hexelion` de La Fragua.
2. **Retirar el proceso manual** que retiene el :8001 — sin esto, el paso 4 vuelve al bucle.
   Se identifica por `setsid ... uvicorn hexelion_gateway:app`, y **no** cuelga de systemd.
3. **Verificar que el código nuevo está en disco**: `grep -c _instrumentar_sinodo` debe pasar de
   `0` a ≥1 en `hexelion_gateway.py`.
4. **Arrancar por la unidad** (`hexelion-gateway.service`), que ya está `enabled` y solo fallaba
   por el puerto ocupado. Confirmar `active (running)` y que `NRestarts` deja de subir.
5. **Comprobar que sirve**: `/api/sinodo` responde y el dashboard sigue en pie.

### Prueba de honestidad del BLOQUE 9 (se corre DESPUÉS del deploy)

El bloque se aprueba o se falla por esto, no por que el panel se vea bien:

- **Qué se mide:** las transiciones que escribe `_instrumentar_sinodo` en `hexelion:sinodo:flaps`
  — timestamp UTC, **qué voz concreta** cae, cuántos segundos, y qué devolvió el healthcheck.
- **Ventana:** al menos 2 h, para cruzar dos veces el minuto `:07`.
- **Hipótesis falsable (9.2):** si las caídas se agrupan cerca del **minuto :07**, el sospechoso es
  el timer del Alquimista. Si los minutos salen **dispersos**, esa hipótesis y la del pacing
  térmico caen, y toca mirar reciclado de conexión o caché horaria del gateway.
- **Criterio de fallo del bloque, innegociable:** si al terminar el contador ya no parpadea
  **porque se suavizó el indicador** (timeout más largo, periodo de gracia), el bloque está
  **fallado** y se revierte. Se elimina la causa, no el síntoma. Un agente que tarda no es un
  agente ausente: el estado correcto sería `OCUPADO`, no `caído`.

## 3 · Dos bucles de fallo que nadie estaba mirando

Salieron de paso y ninguno pertenece a un bloque abierto:

- **La Fragua** · `hexelion-gateway.service`: **16.026** reinicios (~44 h), ~1.4 s de CPU cada uno.
- **El Vigía** · `dump1090.service`: **18.063** reinicios.

Ambos en nodos con vigilancia térmica declarada. Es consumo continuo y ruido en el journal que
tapa señales reales.
