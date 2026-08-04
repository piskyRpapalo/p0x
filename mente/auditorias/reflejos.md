# CENSO DE REFLEJOS — La Mitocondria, fase F0

Fecha de medición: 2026-08-04 (soberano, WEST).
Misión: `mente/misiones/MISION_MITOCONDRIA_P0X.md` · Contratos:
`mente/doctrina/mitocondria/MITOCONDRIA_ESPECIFICACION.txt`.

Inventario de todo lo que hoy **lee un sensor** o **toma una decisión de carga** en el
rack. Cada afirmación lleva el comando o el fichero:línea que la produjo. Lo que no se
pudo determinar con un comando está en la sección NO DATA, no completado por patrón.

Rutas anonimizadas: relativas al repo (`p0x/…`, `hexelion/…`) o con `~`. Cero
direcciones de red, cero FQDN de tailnet, cero usuarios en ruta. Los nombres de nodo
(soberano, la-torre, la-fragua, el-vigía) son vocabulario de canon ya versionado.

---

## 0 · CONDICIONES DE LA MEDICIÓN

Registro de backend al arranque de sesión, como manda el canon del nodo:

    $ ollama ps
    NAME  ID  SIZE  PROCESSOR  CONTEXT  UNTIL
    → ningún modelo cargado en soberano durante el censo. Sin inferencia local
      compitiendo: las lecturas térmicas de esta sesión son de reposo.

Intérpretes (los pide la especificación §1.1, para F1):

    $ python3 -VV                        → soberano:       Python 3.14.4
    $ ssh la-torre 'python3 -V'          → la-torre:       Python 3.10.12
    $ ssh musculo-hp-02 'python3 -V'     → musculo-hp-02:  Python 3.11.2

Alcance alcanzado por nodo (`ssh -o BatchMode=yes -o ConnectTimeout=8 <nodo>`,
solo comandos de lectura, aprobado por el Soberano para este censo):

| Nodo | Medido en vivo | Cómo |
|---|---|---|
| soberano | SÍ | local |
| la-torre | SÍ | SSH solo-lectura (clave en `~/.ssh/config`) |
| musculo-hp-02 | SÍ | SSH solo-lectura |
| la-fragua | **NO** | `Permission denied (publickey,password)` |
| el-vigía | **NO** | `Permission denied (publickey,password)` |
| musculo-hp-01 | **NO** | `tailscale status` → `offline, last seen 10d ago` (canon: inhabilitado) |

**Consecuencia y es la más importante de este censo:** la-fragua es donde corren los
dos reflejos que la misión señala como principales (pausa preventiva y guard de lotes)
y no se pudo medir en vivo. Todo lo que se afirma de la-fragua sale del **código
versionado**, no de su runtime. Está marcado en la columna «Verificación».

---

## 1 · TABLA DE REFLEJOS

Columna «Umbral vive en»: `CÓDIGO` = literal incrustado · `CONFIG` = fichero de
configuración · `UNIDAD` = unidad del supervisor · `ENTORNO` = variable de entorno.

| # | Reflejo · dónde vive | Sensor / fuente exacta | Cadencia | Decisión y sobre qué actúa | Umbral | Umbral vive en | Nodo | Verificación |
|---|---|---|---|---|---|---|---|---|
| R1 | **Pausa preventiva térmica pre-LLM** · `p0x/pipeline/observar_runner.py:44-58` (`pausa_termica`) | `/sys/class/thermal/thermal_zone0/temp` vía `p0x/pipeline/observar_lib.py:24,38-42` (`leer_temp_c`) | Antes de **cada** llamada LLM (inyectada en `delta_engine`, `observar_runner.py:105`); dentro de la espera relee cada 10 s (`:53`) | Bloquea la llamada al modelo hasta enfriar o agotar el tope. No aborta el job | pausa ≥ **78.0 °C**, reanuda ≤ **74.0 °C**, tope **240 s** (`:27,:28,:29`) | CÓDIGO | la-fragua | código versionado (runtime NO medido) |
| R2 | **Guard térmico de trabajos por lotes** · `observar_runner.py:37-41` (`guard_termico`) | idéntica a R1: `thermal_zone0` vía `leer_temp_c` | Al inicio del job, entre fases, y cada 10 llamadas LLM (docstring `:7`) | `raise Recalentado` → **re-encola** el job, estado `requeued_thermal`, máx **3** re-encolados (`:26,:62-67`) | **TMAX = 80.0 °C** (`:25`) | CÓDIGO | la-fragua | código versionado (runtime NO medido) |
| R3 | **Cola de trabajos** · `p0x/bin/p0x-enqueue` | ninguna (no lee sensor) | Por invocación | Serializa a **1 trabajo pesado a la vez** y lo lanza con `nice -n 19 ionice -c3` | `TS_SLOTS=1` | ENTORNO con default incrustado (`:9`) | la-fragua | script versionado; **`tsp`/`ts` NO instalado en soberano, la-torre ni musculo-hp-02** (`command -v tsp ts`) |
| R4 | **Monje P0X (auditoría de viabilidad)** · `p0x/monje/genesis.py` | `psutil.sensors_temperatures()` con preferencia `coretemp/k10temp/zenpower/cpu_thermal/acpitz` (`:82-99`), `psutil.sensors_battery()` (`:56`), `cpu_percent(interval=1.0)` (`:113`), `virtual_memory()` (`:115`) | **`OnBootSec=2min`, `OnUnitActiveSec=5min`** (`~/.config/systemd/user/p0x-monje.timer` en la-torre) | Publica semáforo `viabilidad_roh` = `optimo\|templado\|peligro_termico` (`:141-159,:174`). **No actúa sobre nada**: es reporte | peligro **80.0 °C**, templado **65.0 °C**, ahorro batería **20.0 %** (`:26,:27,:28`) | CÓDIGO | la-torre | MEDIDO: `systemctl --user list-timers` + `cat p0x-monje.timer/.service` |
| R5 | **Agente Monje del Sínodo** · `~/hexelion_sinodo/monje/agent.py` (la-torre) | `max()` de **todas** las `/sys/class/thermal/thermal_zone*/temp` (`:16-26`, psutil roto en Jetson), `cpu_percent(0.5)`, `virtual_memory().percent`, `disk_usage("/")`, UPS vía NUT (`:40-61`) | **`tick_interval_seconds = 30`** (`:31`) | Emite alertas y fija `status = "active" if not alerts else "degraded"` (`:118`) → **es lo que alimenta el contador de agentes** | cpu crítico **75**, cpu warning **65**, gpu **80**, ram **90 %**, disco **90 %**, ups batería **30 %** | **CONFIG** (`~/hexelion_sinodo/config/sources.yaml:20-28`) con **defaults incrustados de respaldo** en `agent.py:79,96,103` | la-torre | MEDIDO por SSH |
| R6 | **Agentes Alquimista / Vocero / Escriba / Berserker** · `~/hexelion_sinodo/<rol>/agent.py` (la-torre) | fuentes externas (HTTP, TimescaleDB). **No leen sensor de hardware** | ticks **300 s** (alquimista `:24`), **300 s** (vocero `:16`), **120 s** (escriba `:17`), **600 s** (berserker `:30`) | Cada uno fija su `status` active/degraded (p.ej. alquimista `:93`) → alimenta el contador | no numérico: derivado de "hubo datos o no" | CÓDIGO | la-torre | MEDIDO por SSH; los 5 servicios `active` (`systemctl is-active hexelion-sinodo-*`) |
| R7 | **Publicación del pulso del Sínodo** · `~/hexelion_sinodo/common/base_agent.py:56-60` | — | Tras cada tick de cada agente | `redis.set("hexelion:sinodo:<rol>:latest", …)` — **sin TTL**. Define cuándo un agente "existe" para todo el rack | — | — | la-torre → Redis en la-fragua | MEDIDO por SSH |
| R8 | **Contador de agentes / roster** · `hexelion/hexelion_gateway.py:775-796` (`/api/sinodo`) | 6 claves `hexelion:sinodo:<rol>:latest` en Redis | Por petición HTTP del dashboard | Clave ausente → `status: "stale"`. Es el `n/6` que aletea | — | CÓDIGO (lista `_SINODO_ROLES`, `:774`) | la-fragua (gateway) | código versionado + roster remoto medido |
| R9 | **Instrumentación de aleteo (Bloque 9)** · `hexelion_gateway.py:802-830` (`_instrumentar_sinodo`) | el propio roster de R8 | En cada lectura del roster | Registra transición por voz con **minuto** (`"min"`, `:812`) a log y a `hexelion:sinodo:flaps` (500 máx). **Solo observa** | — | — | la-fragua | código versionado |
| R10 | **Pollers de nodos** · `hexelion/hexelion_pollers.py` | ping ICMP, `tcp_probe`, y **SSH remoto a el-vigía que hace `cat /sys/class/thermal/thermal_zone0/temp`** (`:266-270`) | **`POLL_INTERVAL_SEC = 15`** (`:27`), claves con **`KEY_TTL_SEC = 60`** (`:29,:394-409`) | `_derive_health` → `online\|degraded\|offline`; alimenta `/api/health/nodes` | **latencia > 300 ms → degraded** (`:338`) | CÓDIGO, con override por ENTORNO (`HEX_POLL_INTERVAL`, `HEX_KEY_TTL`) | la-fragua | código versionado (runtime NO medido) |
| R11 | **Vigilia** · `hexelion/hexelion_vigilia.py` | `/sys/class/thermal/thermal_zone0/temp` (`:76`), load average, disco, precio OMIE | **`INTERVAL = 60`** s (`:17`) | Empuja alertas warn/critical a Redis y fija etiqueta de estado de CPU (`:79-90`) | **TEMP_WARN 70.0**, **TEMP_CRIT 80.0**, **LOAD_WARN 6.8**, **DISK_WARN 85**, **OMIE_HIGH 150.0** (`:20-24`) | CÓDIGO | la-fragua | código versionado (runtime NO medido) |
| R12 | **Bitácora y Status** · `hexelion/hexelion_bitacora.py:93`, `hexelion/hexelion_status.py:49` | `/sys/class/thermal/thermal_zone0/temp` | NO DATA (ver §3) | Solo formatean y reportan. **Sin umbral, sin decisión de carga** | ninguno | — | NO DATA | código versionado |
| R13 | **reflejo-bateria** · `p0x/deploy/fragua/reflejo_bateria_watch.py` + `reflejo-bateria.service` | NUT `upsc` → `ups.status`, `battery.charge`, `input.voltage` (`:67-88`) | bucle con `--poll` (`:248`); unidad `Restart=always RestartSec=15` | Máquina de estados OB/LB → acción protectora + línea REFLEX | tokens **OB / LB** (no numérico) (`:90-98`) | CÓDIGO | la-fragua | **propuesto, NO habilitado** (`mente/feedback/PENDIENTES.md` #47) |
| R14 | **reflejo-termico-m5 y reflejo-vibracion** · `p0x/deploy/fragua/reflejo_m5_watch.py` + `reflejo-m5.service` | BME680 `temp_c` y ADXL345 `\|g\|`, leídos **desde Redis** con TTL, no del bus (`:149-159`) | **`POLL_S = 5`** (`:34`); unidad `Restart=always RestartSec=15` | Aviso REFLEX al Soberano con histéresis. **No para trabajo** | disparo **40.0 °C** / rearme **38.0 °C**; Δ\|g\| disparo **0.25 g**, quieto **0.10 g**, rearme **3** lecturas (`:36-41`) | CÓDIGO | la-fragua | artefacto versionado; runtime NO medido |
| R15 | **disk-poller** · `hexelion/deploy/hexelion-disk-poller.timer` + `.service` | `hexelion/disk_poller.py` | **`OnUnitActiveSec=15min`** | NO DATA (ver §3) | NO DATA | — | NO DATA | unidad versionada; no instalada en ningún nodo medido |
| R16 | **verde-captura** · `p0x/deploy/fragua/verde-captura.timer` | — | **`OnCalendar=*-*-* 08:20:00` y `20:20:00`** | Tarea programada. Si consulta carga antes de arrancar: NO DATA | ninguno hallado | UNIDAD (la cadencia) | la-fragua | unidad versionada; runtime NO medido |
| R17 | **prune-backups** · `p0x/deploy/fragua/prune-backups.timer` | — | **`OnCalendar=Sun *-*-* 04:30:00`** | Poda de backups. Sin consulta de carga | ninguno | UNIDAD (la cadencia) | la-fragua | unidad versionada; runtime NO medido |

**Recuento.** 17 entradas. **12 leen un sensor o una fuente de estado**; 5 son cola o
tarea programada sin lectura de sensor. **7 llevan umbral numérico incrustado en
código** (R1, R2, R4, R10, R11, R13 —tokens—, R14). **1 solo tiene sus umbrales en
configuración** (R5), y aun ese conserva defaults incrustados de respaldo. **0 umbrales
viven en una unidad del supervisor.**

---

## 2 · HALLAZGOS QUE EL CENSO OBLIGA A REGISTRAR

Hechos medidos, no interpretaciones. Ninguno se corrige en F0.

**H1 · En soberano no hay ni un solo reflejo P0X.** `systemctl list-timers --all` → 20
timers, todos de distribución. `systemctl --user list-timers --all` → 3, todos de
distribución. `crontab -l` → *no crontab for pisky*. `/etc/cron.hourly/` vacío. Las
únicas unidades propias son `aurelius-interfaz.service` y `open-webui.service`, y
ninguna lee un sensor ni decide carga. El árbitro que F1 escriba aquí no tiene hoy
consumidores locales.

**H2 · `thermal_zone0` no es el sensor de CPU en soberano.** Medido:

    /sys/class/thermal/thermal_zone0  type=acpitz     temp=20000   (= 20.0 °C)
    /sys/class/thermal/thermal_zone1  type=iwlwifi_1  temp=42000
    /sys/class/hwmon/hwmon3           name=k10temp    ← CPU real (Ryzen)
    /sys/class/hwmon/hwmon7           name=amdgpu     ← iGPU real

Los reflejos R1, R2, R10, R11 y R12 leen `thermal_zone0` por convención. En la-fragua
(RK3588) esa zona sí es la del SoC; en soberano devolvería **20 °C constantes**, un
sensor deshonesto por accidente. `zone0` no es portable entre nodos del rack.

**H3 · El pulso del Sínodo no caduca.** `base_agent.py:57` usa `redis.set(...)` sin TTL
sobre `hexelion:sinodo:<rol>:latest`. Solo el histórico diario recibe `expire` (`:59`).
Es la ausencia que la especificación §2.4 exige que pueda ocurrir, y aquí no ocurre.

**H4 · El sexto agente no existe.** `_SINODO_ROLES` declara 6 roles
(`hexelion_gateway.py:774`), incluido `enlace`. Medido en la-torre: hay **5**
directorios de agente (`alquimista berserker escriba monje vocero`) y **5** servicios,
todos `active`. No hay `enlace` ni en disco ni en systemd. Por R8, su clave está
ausente → `stale` permanente. El contador `n/6` tiene un término que nunca puede subir.

**H5 · El timer del Alquimista no existe como unidad.** La misión y `BACKLOG_UI.md:493`
señalan `OnCalendar=*:07` como sospechoso primario del aleteo horario. Medido:
`ls /etc/systemd/system/*.timer` en la-torre → *No such file or directory*; el único
timer de usuario es `p0x-monje.timer` (5 min, no horario). El Alquimista corre como
servicio `Type=simple` con `tick_interval_seconds = 300`. `PENDIENTES.md` #18 ya
constaba: «el `.timer` nunca se staged (solo existe el `.service`)».
**Ningún proceso con cadencia horaria fue hallado en los nodos medidos.** No se
concluye nada aquí: el diagnóstico del minuto es trabajo de F3.3, con el dato de
`hexelion:sinodo:flaps` que R9 ya está recogiendo.

**H6 · `tsp` no está instalado en ningún nodo medido.** `command -v tsp ts` → ausente en
soberano, la-torre y musculo-hp-02. La cola R3 solo puede estar viva en la-fragua, que
no se pudo medir.

**H7 · musculo-hp-02 está limpio.** Cero timers de usuario, cero cron, cero unidades
P0X en `/etc/systemd/system` (solo `sshd` y `wol`). Coherente con el canon del nodo.

---

## 3 · NO DATA

Lo que no se pudo determinar con un comando, y qué haría falta exactamente.

| Qué falta | Por qué no se pudo | Qué haría falta |
|---|---|---|
| Runtime de la-fragua entero: qué unidades tiene instaladas, cuáles están `active`, si R1/R2/R3/R10/R11/R13/R14/R16/R17 corren de verdad y con qué cadencia real | `ssh la-fragua` → `Permission denied (publickey,password)` | Clave pública de soberano autorizada en la-fragua, o una misión de censo para ese nodo ejecutada allí |
| Runtime de el-vigía: sus reflejos propios, el ingest del M5, la cadencia real de sus sensores | `ssh el-vigia` → `Permission denied (publickey,password)`. `PENDIENTES.md` #11/#24 ya registran esta pubkey como caída y luego repuesta; hoy vuelve a fallar | Restaurar `authorized_keys` en el-vigía (paste de una línea, mano del Soberano) |
| Runtime de musculo-hp-01 | `tailscale status` → `offline, last seen 10d ago`. Canon: inhabilitado, no recuperable en remoto | Acceso físico al nodo |
| Cadencia de R12 (`hexelion_bitacora.py`, `hexelion_status.py`) y de R15 (`disk_poller.py`) | No hay unidad que los dispare en ninguno de los tres nodos medidos; `grep` de `INTERVAL/sleep/schedule` en ambos ficheros → sin resultados | Medir en la-fragua, o confirmar que se invocan a mano / desde el gateway |
| Umbral y decisión de R15 (`disk_poller.py`) | El fichero no se leyó: fuera del alcance mínimo de F0, y su unidad no está instalada en ningún nodo medido | Una lectura del fichero cuando su nodo sea medible |
| Si R16 (`verde-captura`) consulta carga antes de arrancar | Solo se leyó su `.timer`; el `.service` y el script no se auditaron | Leer `verde-captura.service` y su script en la-fragua |
| Valor por defecto de `--poll` en R13 | El `argparse` se leyó parcialmente (`:214,:248`); el default no quedó capturado | `grep -n "poll" -A2` sobre `reflejo_bateria_watch.py` |
| Dónde vive físicamente Redis y con qué configuración de persistencia | `redis-cli` no está instalado en soberano; `base_agent.py` apunta a un host de la-fragua | Medir en la-fragua |
| Qué proceso, si alguno, tiene cadencia horaria en el rack | Ninguno hallado en los 3 nodos medidos (H5); los dos no medidos son precisamente donde podría estar | Censo de runtime en la-fragua y el-vigía |
| Umbral de `edad_lectura` excesiva y periodo de lectura del futuro árbitro | La especificación §1.4 y §5.2 los declaran NO DATA hasta F1/F2 | Siete días de `metabolismo.jsonl` |

---

## 4 · LO QUE ESTE CENSO **NO** HIZO

Ningún reflejo fue modificado, ningún servicio desplegado ni reiniciado, ningún push.
Los accesos remotos fueron exclusivamente de lectura (`cat`, `ls`, `grep`,
`systemctl list-*`, `systemctl is-active`). No se escribió nada en la-torre ni en
musculo-hp-02.
