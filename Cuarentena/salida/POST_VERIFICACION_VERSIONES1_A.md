# POST_VERIFICACION · VERSIONES1 · AGENTE A
Misión: cerrar VERSIONES 1 — registrar en disco once decisiones firmadas y enmendar la guardia.
Fecha: 2026-08-12
Dominio: decisiones-en-disco + guardia-higiene
Estado: FIRMADO (2026-08-12, con ajustes — ver §POSDATA)
Firmante: Soberano

## 1 · RESUMEN

Las once decisiones **D31–D41 están en disco**, anexadas literalmente desde el
bloque sellado, sin renumerar ni reescribir una sola línea previa. El rojo
previo dio las once `AUSENTE` exigidas; los seis verdes posteriores pasaron.

La guardia cubre ahora los seis prefijos de ruta absoluta, con un caso rojo por
prefijo demostrado en rojo **antes** del arreglo. Suite **71/71, EXIT=0**.

Tres cosas que el Soberano debe leer antes de firmar: un caso que vivía en
`PASAN` tuvo que moverse a `BLOQUEAN`; la enmienda cambió qué regla reporta en
un caso preexistente; y la extensión destapó que el skill de auditoría apunta a
una **raíz que no existe**.

Nada publicado, nada borrado, sin `git push`, sin tocar `.git/`, sin escribir en
`aurelius-mvp`.

## 2 · HECHO

- **PASO 0** · hash del anexo sobre la región entre marcadores, leído del sitio
  único. Coincide con la referencia. Sin divergencia, sin incidente.
- **PASO 1** · rojo previo capturado **antes** de cualquier escritura.
- **PASO 2** · bloque `D31–D41` extraído entre marcadores de
  `Cuarentena/salida/ENTRADAS_D31_D41.md` y anexado por redirección. **No
  transcrito** por mí en ningún punto: `sed … >> destino`.
- **PASO 3** · los seis verdes.
- **PASO 4** · enmienda de la guardia, test rojo primero.
- **PASO 5** · archivo de razonamiento creado **fuera de git**.
- **PASO 6** · auditor chat→disco creado y ejecutado.

**NO ejecutado, explícito:** ningún `git add`, `commit`, `push`, `checkout`,
`rm`, `mv`. Nada dentro de `.git/`. Nada en `aurelius-mvp` (que no existe en
disco). No se tocó `run_audit.sh` — el auditor nuevo queda suelto, ver §7.
No se rellenó D24. No se renumeró nada.

**Respaldo antes de tocar:** copia de `03_ESTADO_FIRMADO.md` (sha256
`7228eeaf5dcff967…`) fuera del repo antes del PASO 2. Reversión en §9.

## 3 · MEDIDO

| Medición | Resultado | Comando |
|---|---|---|
| Hash del anexo, región entre marcadores | `0939b9ea…b5d3` — **idéntico** a la referencia | `sed -n '/LECCIONES:INICIO/,/LECCIONES:FIN/p' … \| sha256sum` |
| Rojo previo | **11** líneas `AUSENTE`, D31…D41 | bucle `seq 31 41` del PASO 1 |
| Bloque de origen | 89 líneas, **11** D-ids, envuelto en líneas en blanco | `sed -n '/BLOQUE:INICIO/,/BLOQUE:FIN/p' \| sed '1d;$d'` |
| Líneas del firmado | 182 → **271** (+89) | `wc -l` antes/después |
| Naturaleza del cambio | `182a183,271` · **0 líneas suprimidas o reescritas** | `diff respaldo actual \| grep -c '^<'` → `0` |
| Verde 1 · bucle del PASO 1 | **0** líneas | idem PASO 1 |
| Verde 2 · `grep -c '^## D'` | 22 → **33** (+11) | `grep -c '^## D' …` |
| Verde 3 · hash del anexo en el firmado | **1** línea, `200:` — dentro de D32 (193–203) | `grep -n '0939b9ea1568df12' …` |
| Verde 4 · `2026-09-12` | **4** (umbral ≥4) | `grep -c '2026-09-12' …` |
| Verde 5 · D-ids duplicados | **vacío** | `grep -oE '^## D[0-9]+' \| sort \| uniq -d` |
| Verde 6 · hueco D24 | **0** ocurrencias — no se rellena | `grep -c '^## D24 ' …` |
| Suite guardia · **ROJO previo** | **66/71, 5 fallo(s), EXIT=1** | `python3 test_guardia.py` |
| Suite guardia · **VERDE posterior** | **71/71, 0 fallo(s), EXIT=0** | idem, tras la enmienda |
| Casos rojos por prefijo | 6 (`/home /mnt /srv /opt /var /media`); los 5 nuevos en rojo antes | sección D34 de `BLOQUEAN` |
| Loopback | `127.0.0.1` y `::1` en `PASAN`, verdes | sección D34 de `PASAN` |
| Auditor chat→disco | 41 esperados · 40 en disco · 33 cabecera + 7 tabla · **EXIT=0** | `python3 skills/auditar-p0x/scripts/audit_dids.py` |
| Rutas absolutas en `skills/auditar-p0x` | **3**, exactamente las que D34 predijo | `guardia_higiene.py --files $(find skills/auditar-p0x -type f)` |
| Raíz que citan esas 3 rutas | **no existe**; `/mnt` vacío; `P0X_ROOT` sin definir | `ls -d …`, `ls /mnt`, `echo $P0X_ROOT` |
| Guardia sobre lo que escribí | **EXIT=0** | `--files audit_dids.py 03_ESTADO_FIRMADO.md` |
| Guardia sobre **este** entregable, 1ª pasada | **EXIT=1, 5 hallazgos** (predije 2) | `--files POST_VERIFICACION_VERSIONES1_A.md` |
| Guardia sobre **este** entregable, tras 5 pragmas declarados | **EXIT=0** | idem |

## 4 · CRÍTICO

**a · Un caso migró de `PASAN` a `BLOQUEAN`, y no es un detalle de forma.**
`test_guardia.py` afirmaba que `"Usa el árbol /srv/p0x en el nodo remoto."`  <!-- guardia:permitir cita-literal-del-caso-de-test-D34 -->

debía **pasar**. La enmienda de D34 dice que debe **bloquear**. Las dos cosas no
pueden ser ciertas. Lo moví a `BLOQUEAN` conservando el texto literal y dejando
el motivo escrito junto al caso. D23 prohíbe mover `BLOQUEAN → PASAN` porque
eso es rendirse; este movimiento es el contrario y endurece. **Aun así lo
señalo, porque es una afirmación firmada que hoy dice lo opuesto a lo que
decía**, y esa reversión la firma el Soberano, no yo.

**b · La enmienda cambió qué regla reporta en un caso preexistente.**
`scp informe.md torre:/srv/p0x/entrada/` reportaba `NODO-HOST-PATH`; ahora  <!-- guardia:permitir cita-literal-del-caso-de-test-D34 -->

reporta `RUTA-HOME` y la suite lo marca `ok*`. **Sigue bloqueando: el resultado
de seguridad no cambia.** La causa es que `RUTA-HOME` va antes en `REGLAS` y el
`break` se la lleva. **No abre agujero**, y esto sí lo verifiqué en vez de
suponerlo: ambas reglas están en el conjunto eximible de D8, y la exención se
evalúa por regla con `continue`, así que una regla eximida no detiene el
recorrido — el suelo `D8_JAMAS` sigue intacto. **No reescribí la expectativa
del test para que dijera `RUTA-HOME`**: adaptar el test al código es
exactamente el vicio que D23 nombra. El `ok*` queda visible como señal.

**c · El skill de auditoría apunta a una raíz muerta.** Las tres rutas que D34
predijo en `skills/auditar-p0x` no son solo higiene: citan una raíz que **no
existe en este nodo**, y `P0X_ROOT` no está definido, así que
`audit_lib.py` cae a ese valor por defecto.  <!-- guardia:permitir ruta-de-hallazgo-D34, no se publica -->
Consecuencia probable: los cuatro auditores deterministas de `run_audit.sh` no
están auditando este árbol. **No lo he confirmado ejecutándolos** — fuera del
alcance de esta misión. Es un frente propio, no un parche de pasada.

**d · Consecuencia de la enmienda que conviene saber antes de firmar.** D8 exime
`RUTA-HOME` en `Cuarentena/salida` y `docs/post_verificacion`, pero sus patrones
literales solo cubren el prefijo del home. Un entregable que cite una ruta bajo
`/srv`, `/opt`, `/var`, `/mnt` o `/media` **ya no queda exento y bloqueará el
commit**. No he ampliado los patrones de D8 — ampliar una exención es
debilitarla, y nadie me lo pidió.

**Y lo comprobé en mi propia carne, con una cifra que no esperaba.** Escribí este
párrafo prediciendo el efecto y puse **dos** pragmas donde creí que hacían falta.
Al correr la guardia sobre el entregable en su ruta de destino: **EXIT=1, cinco
hallazgos**. Faltaban tres. La predicción era correcta en la dirección y corta en
la magnitud — citar los casos de test como evidencia es precisamente lo que
multiplica las citas de ruta, y un informe honesto sobre rutas absolutas está
obligado a contener rutas absolutas. Resuelto con cinco `guardia:permitir`
declarados y motivo a la vista; **EXIT=0** verificado después. Lo dejo escrito
porque es el dato más útil de esta sección: **la regla 7 aplicada a sí misma
falló al primer intento**, y solo la verificación en el destino lo detectó.
Estimar el efecto de tu propia enmienda no es medirlo.

## 5 · BLOQUEADO

- Commit de todo lo anterior ← firma del Soberano.
- Reparación de las 3 rutas muertas en `skills/auditar-p0x` ← decisión: es un
  frente propio (§8 no lo pregunta; va como sugerencia en §7).
- Contenido de D24 ← memoria del Soberano. No hay rastro en disco.
- Cableado del auditor nuevo en `run_audit.sh` ← firma; cambia el código de
  salida de un punto de entrada compartido.

## 6 · NO_DATA

- **D24**: si existió y se perdió, o si nunca existió. **No es distinguible
  desde el disco.** Anotado con fecha de descubrimiento en el archivo de
  razonamiento. No se rellena, no se renumera.
- Si los cuatro auditores de `run_audit.sh` funcionan hoy: no ejecutados.
- Si `/mnt/nvme` fue alguna vez la raíz real o es un residuo de otra máquina.  <!-- guardia:permitir ruta-de-hallazgo-D34, no se publica -->
- Estado del frente B (`aurelius-mvp`): no existe en disco. No lo he tocado ni
  mirado más allá de confirmar su ausencia.
- Si el `ok*` preexistente de `vigia.internal` (`DOMINIO-PRIVADO` en vez de  <!-- guardia:permitir cita-literal-del-caso-de-test-preexistente -->

  `NODO-DOMINIO`) y el de la línea de D18 (`RUTA-HOME` en vez de
  `TOKEN-PROVEEDOR`) importan: **son anteriores a esta sesión**, ambos bloquean
  correctamente, no los toqué.

## 7 · PARA CLAUDE CODE

| # | Tarea | Prio | Riesgo | Dependencia |
|---|---|---|---|---|
| 1 | Resolver las 3 rutas muertas de `skills/auditar-p0x`: sustituir el literal por `P0X_ROOT` con fallback a la raíz real, y **ejecutar los 4 auditores** para ver qué llevan sin auditar | alta | medio — puede destapar deuda vieja | firma |
| 2 | Cablear `audit_dids.py` en `run_audit.sh` | media | bajo — cambia el `rc` del entrypoint | firma |
| 3 | Registro de puntos ciegos de la guardia (D35): fichero de lo que **NO** cubre, obligatorio releer al tocarla | media | bajo | — |
| 4 | Metatest de D35: batería roja de agujeros ya cerrados (D18, D34), ejecutada al modificar la guardia | media | bajo | 3 |

**Prompt sugerido para 1:** *«En `skills/auditar-p0x`, los tres literales de raíz
apuntan a un directorio inexistente y `P0X_ROOT` no está definido. Sustitúyelos
por `P0X_ROOT` con fallback a la raíz real del repo, ejecuta los cuatro
auditores, y reporta qué encuentran. No corrijas lo que encuentren: repórtalo.»*

Ninguna de las cuatro abre un frente aparcado de §4 del estado firmado.

## 8 · DECISIÓN PARA EL SOBERANO

**¿Firmas la enmienda de la guardia tal como está — con el caso `/srv` movido de
`PASAN` a `BLOQUEAN`, el `ok*` de `scp torre:/srv/…` dejado a la vista sin  <!-- guardia:permitir cita-literal-del-caso-de-test-D34 -->

reescribir su expectativa, y los patrones de exención de D8 SIN ampliar (lo que
obliga a un `guardia:permitir` declarado en todo entregable que cite una ruta
bajo los cinco prefijos nuevos)?**

## 9 · CIERRE

- **Destino propuesto:** `docs/post_verificacion/POST_VERIFICACION_VERSIONES1_A.md`.
- **Ficheros tocados** (ninguno commiteado):
  - `Cuarentena/03_ESTADO_FIRMADO.md` — +89 líneas, solo anexado.
  - `deploy/comun/hooks/guardia_higiene.py` — regla de ruta + `revisar_antes_de`.
  - `deploy/comun/hooks/test_guardia.py` — 6 casos rojos, 2 `PASAN`, 1 movido.
  - `skills/auditar-p0x/scripts/audit_dids.py` — **nuevo**.
- **Fuera de git** (no se commitea nunca, por diseño):
  `~/.local/share/p0x/razonamiento/ARCHIVO_RAZONAMIENTO.md` — cabecera «memoria,
  no canon», lista D1–D41 entre marcadores, hueco D24 con fecha.
- **Reversión**, por orden y sin pérdida:
  1. `03_ESTADO_FIRMADO.md`: `git checkout --` (nada estaba commiteado) o
     restaurar el respaldo previo al PASO 2.
  2. Guardia y batería: `git checkout -- deploy/comun/hooks/`.
  3. `audit_dids.py`: fichero nuevo sin rastro en git; se borra o se archiva.
  4. Archivo de razonamiento: vive fuera de git; inerte si nada lo lee.
- **Nada se archiva ni se borra en esta ronda.** `ENTRADAS_D31_D41.md` se
  conserva: es la fuente del bloque anexado y su valor de prueba no caduca al
  haberse consumido.

---

## §POSDATA · LO QUE PASÓ DESPUÉS DE LOS SEIS PASOS

**33 es el número correcto de esta ronda.** Las mediciones de §3 son de
D31–D41 y su `grep -c '^## D'` = 33 es exacto. Lo que sigue ocurrió después, y
se escribe aquí para que ninguna cifra de §3 quede desmentida por el disco.

**D42 · anexado y revertido el mismo día.** El Soberano ordenó anexar
`D42 · PODA ESTACIONAL` con texto literal (271 → 277, `271a272,277`, 0
supresiones, cabeceras 33 → 34). Se señaló que **D40 ya era esa decisión**, y
con más contenido: indicador firmado, criterio operativo de relectura y fecha
de la primera poda. El Soberano revirtió. Restauración verificada **IDÉNTICA**
al estado post-D41; D40 nunca se tocó; el número **no se reutiliza**.

Corrección de aritmética que conviene dejar escrita, porque volverá a morder:
al revertir, el conteo vuelve a **33**, no a 34. `^## D` cuenta solo cabeceras,
y **D1–D7 viven como filas de tabla**, no como cabeceras. El rango real es
D8–D41 = 34 ids, menos el hueco D24 = **33**. El total de D-ids en disco es
**40** (33 cabeceras + 7 filas).

**D43 · la lección, fuera del anexo sellado.** Para no invalidar el hash que
D32 registra, la lección de los falsos positivos en prosa entró como decisión
propia en vez de como fila del anexo. Verificado tras anexarla: el sello del
anexo sigue dando `0939b9ea…b5d3` y D32 no se enmendó. Conteo final: **34**
cabeceras (33 + D43).

**Dos huecos, y no son la misma clase de hueco.** D24 es `NO_DATA` porque **no
se sabe** qué fue. D42 es `NO_DATA` porque **se sabe exactamente** qué fue y se
decidió que no fuera. Ambos quedan anotados en el archivo de razonamiento con
su causa y su fecha; el auditor los informa sin bloquear.

**Defecto menor, declarado:** el texto canónico de D43 contiene la cadena
`guardia:permitir declarado`, que casa con el patrón del pragma. Esa línea
queda **permanentemente sin escanear** por la guardia. No oculta nada —es
prosa sobre prefijos—, pero la decisión que obliga a declarar pragmas se
auto-exime por accidente. Se declara en vez de dejarlo de sorpresa.

## §TRANSITOS

**Hora de arranque:** `2026-08-12 01:27:57 WEST` (`date`, en el nodo).
**Hash del anexo, leído del sitio único** `Cuarentena/salida/ANEXO_LECCIONES_CRUZADAS.md`:
`0939b9ea1568df12407c7808cf469ee803d08dfcaeaa0da14cfb0ab01cfcb5d3` — **coincide**
con la referencia de la orden. Sin divergencia dentro ni fuera de marcadores;
sin incidente que registrar.

| # | Origen | Destino | Verificación **en el destino** | Estado |
|---|---|---|---|---|
| 1 | Anexo de lecciones (sitio único) | esta sesión | `sha256sum` sobre la región entre marcadores, recalculado aquí | **VERDE** |
| 2 | Bloque `D31–D41` de `ENTRADAS_D31_D41.md` | `03_ESTADO_FIRMADO.md` | 6 verdes del PASO 3 + `diff` con 0 supresiones | **VERDE** |
| 3 | **Lección del punto ciego (L1) → spec de B** | `aurelius-mvp` | **NO EJECUTADO.** Los seis prefijos y la exclusión de `/tmp` viajan a B por el anexo, no por mi mano | **PENDIENTE** |
| 4 | Decisiones en conversación | disco | rojo previo 11 `AUSENTE` → verde posterior 0 | **VERDE** |
| 5 | Lista de D-ids esperados | archivo fuera de git | auditor chat→disco ejecutado en el destino, EXIT=0 | **VERDE** |

**Fila 3 · la lección del punto ciego, y por qué no la aplico yo.** L1 del anexo
fija que la regla de ruta cubra `/home /mnt /srv /opt /var /media` **desde su
primer test**, con `/tmp` fuera por decisión firmada. En este lado eso ya es
código: seis prefijos, seis casos rojos, cinco demostrados en rojo antes del
arreglo. La lección que cruza a B **no es la lista de prefijos** — es lo que
costó descubrirla: el punto ciego llevaba ahí desde el origen de la guardia y se
usó como criterio de publicabilidad *precisamente porque estaba probada*. Una
suite en verde mide lo que alguien pensó en cubrir, nunca lo que olvidó.

Y esta ronda produjo un dato que B necesita y que el anexo todavía no dice:
**extender la regla creó un falso positivo inmediato** — una frase de prosa
legítima que citaba `/srv/p0x` pasó a bloquear. Es el coste real de la  <!-- guardia:permitir cita-literal-del-caso-de-test-D34 -->

lección, medido, no anticipado. **No lo he escrito en el anexo ni tocado B**:
la orden dice que un hallazgo que cruza es PARO y reporte, no parche. Queda en
§8 del Soberano decidir si esa fila entra al anexo antes de que B escriba su
primer test, porque llegar tarde le cuesta a B la misma ronda que me costó a mí.

**Lectura del propio §TRANSITOS:** de cinco tránsitos, cuatro verificados en
verde en el destino y uno deliberadamente sin ejecutar. La tabla vale por la
tercera fila: es la única que cruza a otro agente, y es la única que no he
tocado.
