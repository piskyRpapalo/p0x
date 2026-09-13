# UNIDADES ACTIVAS EN `soberano`

Registro de todo lo que corre sin que nadie mire. **Una fila por unidad, y ninguna
unidad sin fila.** Si algo corre y no está aquí, o está aquí y no corre, una de las dos
cosas es mentira y hay que averiguar cuál.

Regla que gobierna este fichero: *«no se crean servicios systemd sin aprobación explícita
del Soberano»* + *«`systemctl --user list-units` al cerrar cada sesión»*. Firmada
2026-08-24, tras dos meses en el archivo sin llegar al repo.

| unidad | qué hace | cuándo | qué toca | firmada | cómo se apaga |
|---|---|---|---|---|---|
| `guardian.timer` | Vigila que no entre en el árbol de Aurelius un `import` fuera de la biblioteca estándar | diario 04:00 (±15 min), `Persistent=true` | **Solo lee** `~/p0x/aurelius`. Escribe latidos y hallazgos en `~/.aurelius/loops.db`. `ProtectSystem=strict` + `ReadWritePaths=~/.aurelius` | 2026-08-24 · **ACTIVA**, probada a mano antes de cronificar (dejó latido) | `systemctl --user disable --now guardian.timer` |

| `curador.timer` | Higiene de la memoria: duplicados y enlaces rotos. **Propone, no toca** | domingos 05:00 (±30 min), `Persistent=true` | Abre `memory.db` en **solo lectura** (`mode=ro` en el código **y** `ReadOnlyPaths` en la unidad: dos cerrojos independientes). Escribe latidos y hallazgos | 2026-08-25 · **ACTIVA**, probada a mano y bajo systemd | `systemctl --user disable --now curador.timer` |
| `afinador.timer` | Corre `bin/pruebas` entera y vigila **que la tanda siga midiendo**: recuento a la baja, suites que caen del corredor, cobertura que se ensancha, sabotajes ciegos | diario 03:00 (±15 min), `Persistent=true` | **Solo lee** `~/p0x/aurelius`. Escribe latidos y hallazgos en `~/.aurelius/loops.db`. `Nice=10` + `IOSchedulingClass=idle` para no competir con la persona | 2026-08-25 · **ACTIVA**, probada a mano y bajo systemd (87 s, dejó latido) antes de cronificar | `systemctl --user disable --now afinador.timer` |
| `preceptoros-pwa.service` | La cara (PWA) en `127.0.0.1:8740`, vía `bin/preceptoros-servicio` | `Type=simple` + `Restart=always`, permanente | Escribe `~/.preceptoros/pwa.log` | 2026-08-25 · **FIRMADA** como `aurelius.service`; **renombrada por el Soberano el 2026-09-04**. Verificada tras el renombrado: `active running`, `NRestarts=0`, cara HTTP 200 | `systemctl --user disable --now preceptoros-pwa.service` |
| `10-motor-vulkan.conf` | **Drop-in.** Apunta el motor del turno al envoltorio Vulkan en vez del binario CPU del PATH | con la unidad; no añade disparo propio | Solo pone `PRECEPTOROS_MOTOR`. Mismo modelo (el 4B), misma memoria, mismo puerto | 2026-08-25 · firmado y **ACTIVO** (un turno real en 4 s por `/api/charla`). 🔴 **HUÉRFANO desde el renombrado del 2026-09-04** — ver abajo | `rm ~/.config/systemd/user/preceptoros-pwa.service.d/10-motor-vulkan.conf && systemctl --user daemon-reload && systemctl --user restart preceptoros-pwa.service` |

| `director.timer` | **Meta-bucle (L4).** Lee los latidos, reparte la cola de ventanas y **marca muertos** a los bucles que fallan dos ventanas seguidas. Propone, no ejecuta: lo que toca producto o memoria va a `docs/bandeja_firmas.md` | cada 15 min (`OnCalendar=*:0/15:00`, ±60 s), `Persistent=true` — es la `ventana_s=900` que el propio bucle declara en `loops.db` | Escribe `loops.db`, `plan_ventanas.json` y el cerrojo `flock` en el directorio de datos, y una fila en la bandeja de firmas. `ProtectSystem=strict` + `ReadWritePaths` con **los dos nombres** del directorio de datos (`~/.aurelius` es symlink a `~/.preceptoros`) para que no se caiga el día que el symlink se retire | 2026-09-12 · firmada por el Soberano (Frente A, Opción A). **Probada a mano** antes de cronificar: dejó latido y su primera pasada en 20 días se declaró muerta a sí misma, que es justo su trabajo. 🟡 **INSTALADA Y NO ACTIVA** — el arranque bajo systemd y el `enable` quedaron pendientes de la mano del Soberano | `systemctl --user disable --now director.timer` |

| `ojo-soberano.service` | **El Ojo del Soberano**: nexo de arranque de toda sesión de IA en este nodo (`/api/arranque`) y panel del laboratorio. `ojo.py --check` da «SIRVE · 12 piezas presentes» | `Type=simple` + `Restart=on-failure`, permanente | Escucha **solo en 127.0.0.1:8790** --lo fija el propio `ojo.py`--, así que no se expone a la tailnet. `ProtectSystem=strict` + `ReadWritePaths` al árbol del Ojo y al directorio de datos | 2026-09-12 · firmada por el Soberano. **Probada a mano** antes de instalar: `/`, `/vivo` y `/api/arranque` devolvieron 200. 🟡 **INSTALADA Y NO ACTIVA** -- el `enable` queda para la mano del Soberano | `systemctl --user disable --now ojo-soberano.service` |

### 🔴 El renombrado del 2026-09-04 desconectó el motor Vulkan

El Soberano renombró `aurelius.service` → `preceptoros-pwa.service`. La unidad quedó
perfecta: `active running`, `NRestarts=0`, cara en HTTP 200. **Y el drop-in se quedó
atrás**, en `~/.config/systemd/user/aurelius.service.d/` — un directorio que systemd ya no
mira, porque la unidad a la que pertenecía no existe.

Medido el mismo día:

    systemctl --user show preceptoros-pwa.service -p DropInPaths --value   # vacío
    tr '\0' '\n' < /proc/<MainPID>/environ | grep MOTOR                    # nada

Sin `PRECEPTOROS_MOTOR`, el turno cae al binario CPU del PATH. Lo que cuesta está medido en
la cabecera del propio drop-in: **19,23 tok/s y 6,2 s de pared por turno, frente a 27,25 y
3,9 s**. Un ×1,42 y un 37 % más de espera en cada turno de la app.

Y es invisible por donde se mira: el servicio está verde, el puerto responde 200 y nada
falla. Es la misma familia que el bucle de 7970 reinicios de esa misma mañana — **se vigila
el puerto, no la configuración**. Un drop-in huérfano no da error: deja de aplicarse.

**REMEDIO — exige firma, es una unidad. No aplicado:**

    mkdir -p ~/.config/systemd/user/preceptoros-pwa.service.d
    mv ~/.config/systemd/user/aurelius.service.d/10-motor-vulkan.conf \
       ~/.config/systemd/user/preceptoros-pwa.service.d/
    rmdir ~/.config/systemd/user/aurelius.service.d
    systemctl --user daemon-reload
    systemctl --user restart preceptoros-pwa.service

Y se comprueba que volvió, que es la mitad que suele saltarse:

    systemctl --user show preceptoros-pwa.service -p DropInPaths --value   # ya no vacío
    curl -s -o /dev/null -w '%{http_code}\n' http://127.0.0.1:8740/api/estado

Queda además `aurelius-interfaz.service` (`inactive`, `disabled`), último resto del nombre
viejo. No hace nada; retirarlo es otra firma, y de las baratas.

### Sobre `aurelius.service` — encontrada sin firma, firmada al día siguiente

La encontró el `systemctl --user list-units` de cierre del 2026-08-24: llevaba corriendo
desde el 23 a las 02:21, `active` pero `disabled`, y sirviendo desde `aurelius-mvp` —el
árbol cuya `main` estuvo sesenta commits divergida—. Firmada el 2026-08-25 y reapuntada a
`~/p0x/aurelius`, ahora sí `enabled`: sobrevive a un reinicio y es reproducible.

**Desviación declarada sobre la orden.** La orden decía
`ExecStart=/usr/bin/python3 .../aurelius.py`. No se hizo así, y el motivo es medible:

- `aurelius.py` es el producto **interactivo**, no un servidor. Bajo `Type=simple` con
  `Restart=always` sería un bucle de arranques.
- `bin/aurelius-servicio` existe por una cicatriz escrita dentro de él: con `Type=simple`,
  systemd vigila al proceso que lanza; si ese proceso se va a segundo plano y devuelve 0,
  systemd cree que murió limpiamente y lo reinicia. **Medido en este Beelink: 23 reinicios
  en bucle, cada diez segundos, con `status=0`** — el peor síntoma, porque «salió bien» y
  «se cayó» se leen igual. El envoltorio detecta `INVOCATION_ID`, corre en primer plano y
  entrega el proceso con `exec`.

Se cumple la intención de la orden —apuntarla al árbol bueno— sin reintroducir el bug que
ese envoltorio existe para evitar. Verificado tras arrancar: `NRestarts` no se movió en
25 s, y `/api/estado` responde HTTP 200 desde `~/p0x/aurelius`.

## Lo que NO está activado, y por qué

- `director` (L4) — construido y probado, **sin cronificar**. Es el meta-bucle: planifica
  ventanas y escribe a la bandeja de firmas. Se activa cuando haya más de un bucle que
  dirigir.
- `s0` — construido y probado, **sin cronificar**. Semanal. Se activa cuando haya varios
  filtros de los que sospechar; con uno solo no tiene de qué.
- `centinela`, `peregrino`, `medico`, `escriba`, `cronista`, `vigia` — **no existen
  todavía**. Son L1/L2/L3 y están sin escribir. No se cronifica lo que no está construido y
  probado.

### El reparto horario, y por qué

| hora | bucle | por qué ahí |
|---|---|---|
| 03:00 | Afinador | corre la tanda entera (138 s) y crea y borra árboles temporales |
| 04:00 | Guardián | lee el árbol; si solapara con el Afinador leería un estado a medias |
| dom 05:00 | Curador | **carga 16 GB de modelo**. Va el último y solo un día por semana |

El Curador es el único que carga el 27B. Con el cuelgue del 2026-08-24 fresco —causado por
varias cargas simultáneas de ese modelo— que no comparta hora con nadie no es cortesía: es la
lección.

### Por qué el Afinador va a las 03:00 y el Guardián a las 04:00

Una hora entre los dos, a propósito. El Afinador corre la tanda entera —138 s medidos, y
crea y borra árboles temporales— y el Guardián lee el árbol para ver qué importa cada
fichero. Solapados, el Guardián podría estar leyendo mientras el otro tiene el árbol a
medias, y el hallazgo resultante sería sobre un estado que no existe fuera de esos dos
minutos. Separados, cada uno mide algo real.

### Sobre el drop-in del motor Vulkan — por qué es un fichero y no un parche al producto

`conversacion.motor_llama` construye su orden **sin `-ngl`**, y hace bien: el producto es
portátil y no puede suponer que hay GPU. Pero en este nodo la hay, y el binario del PATH
(`~/.local/bin/llama-completion` → b10488) **no tiene backend Vulkan** — apuntar el producto
ahí sin `-ngl` dejaría la Radeon delante y sin usar.

Por eso el arreglo es un envoltorio de nodo (`deploy/soberano/preceptoros-motor-vulkan.sh`,
desplegado en `~/.local/bin/`) y **ni una línea del producto**: pone `LD_LIBRARY_PATH`,
`-ngl 99` y `--reasoning off`, y **para** si no encuentra el binario Vulkan en vez de caer a
CPU en silencio.

Medido el 2026-08-25, mismo prompt, `-n 80`, el 4B de la cara:

| motor | generación | pared por turno |
|---|---|---|
| CPU (lo que había) | 19,23 tok/s | 6,2 s |
| **Vulkan** | **27,25 tok/s** | **3,9 s** |

Y el 27B (`Qwen3.8-27B-Uncensored`) por la misma vía: **4,32 tok/s · 25 s por turno**. Seis
veces más lento, y el producto **carga el modelo entero en cada turno** porque no hay servidor
que lo mantenga caliente (D68). Es cerebro de bucle nocturno, no de conversación — y por eso
la cara se queda con el 4B.

**Corrección al canon, medida.** `deploy/soberano/CLAUDE.md` afirma que «`llama-completion` de
este build NO tiene `--reasoning off`». Es falso en los **dos** binarios de este nodo: b10068
(Vulkan) y b10488 (PATH) exponen `-rea, --reasoning [on|off|auto]`. Comprobable con
`llama-completion --help | grep reasoning`.

## Lo que corre y NO tiene fila (deriva encontrada el 2026-08-25)

- `open-webui.service` — `active/running`, sin fila. O se le abre una o se apaga.
- `aurelius-interfaz.service` — `loaded`, sin fila, y su copia del repo tiene **otro tamaño**
  que la instalada (1.947 B frente a 549 B).
- `ollama.service` (nivel sistema) — dice `active` y **el puerto 11434 rechaza conexiones**.
  Servicio que se declara vivo y no atiende: el mismo modo de fallo que S0 vigila.
  · **CORREGIDO 2026-09-07:** ya no es cierto. El 11434 atiende — se le pidieron
  turnos a seis modelos distintos esta madrugada, con sus tok/s medidos. Se deja
  la línea vieja tachada en vez de borrarla: saber que estuvo caído y cuándo
  volvió es parte del dato.

## `buzon-medidas.service` — **PROPUESTA, no instalada** (2026-09-07)

**Qué hace.** Recibe `POST /api/v1/medidas-temp` y guarda la medida en
`~/.preceptoros/medidas_temp.db`. Append-only: solo INSERT, y `processed` la
mueve únicamente `scripts/sync_medidas_to_fragua.py`.

**Qué toca.** Ese único fichero SQLite y el puerto **8791 en 127.0.0.1**. Nada
más. Sin dependencias: `http.server` de la biblioteca estándar, porque en este
nodo no hay FastAPI ni sudo para instalarlo — desviación declarada respecto al
encargo, que pedía FastAPI.

**Cómo se apaga.** `systemctl --user disable --now buzon-medidas`. Y mientras no
se instale, se prueba a mano con
`python3 deploy/soberano/medidas_temp_api.py` y `Ctrl-C`.

**Por qué NO está instalada.** El canon pide firma explícita por unidad y que el
bucle se construya y se pruebe primero. Está construido y probado; la firma de
la unidad es un paso aparte.

**Y algo que hay que saber antes de firmarla:** hoy **no la alcanza un navegador
de fuera**. `api.preceptoros.org` sale por el túnel de la-fragua, y
`downloads.preceptoros.org` sí apunta a la IP pública de este nodo
(95.92.164.201) pero no responde — el puerto no está abierto. La alcanzan el
navegador del propio Soberano y la tailnet. El trabajo que falta es de red, no
de código.

### 🟡 `director.timer` queda instalada y apagada (2026-09-12)

El bucle estaba **huérfano**: `ventana_s=900` en `loops.db` y ninguna unidad que lo
disparase. No corría desde hacía 20,5 días, y nadie lo marcaba muerto porque **quien
detecta a los muertos es él mismo**. Un vigilante ausente no puede declarar su propia
ausencia.

Probado a mano el 2026-09-12, y funciona: `pasada()` devolvió
`{"accion": "marcar_muerto", "porque": "sin latido desde hace 1772189 s, más de 2 ventanas
de 900 s"}`, dejó su par `entra`/`sale` en `latidos` y escribió una fila de severidad alta
en la bandeja. La tabla `bucles` pasó de mentir por omisión a decir `director · muerto`.

**Lo que falta, y no se hizo por decisión de no hacerlo a medias:** los ficheros están en
`~/.config/systemd/user/` y `daemon-reload` está hecho, pero `director.timer` sigue
`disabled`. Faltan dos órdenes, en este orden — la primera es la prueba bajo systemd que
las tres unidades hermanas también pasaron antes de cronificarse:

    systemctl --user start director.service      # prueba: debe dejar latido
    systemctl --user enable --now director.timer # y entonces se cronifica

**Aviso sobre `--informe`:** la unidad invoca `director.py` **desnudo**, sin ese flag.
`main()` con `--informe` hace `print(informe(db)); return 0` — imprime y sale. Un timer con
`--informe` habría corrido cada 15 minutos sin marcar a nadie: el vigilante puesto y
apagado a la vez.

**Deriva detectada de paso, y es otra firma:** las unidades de `~/.config/systemd/user/`
son **copias** de las de `deploy/soberano/`, no symlinks, y ya han divergido
(`diff afinador.service` da distinto). El repo no refleja lo que corre.

### 🪦 `aurelius-interfaz.service`, enterrado (2026-09-12)

Estaba `inactive` + `disabled` desde hacía semanas y se retiró por firma del Soberano.
**No era una unidad parada: era un puntero a un árbol que ya no existe.** Su
`ExecStart` apuntaba a `~/aurelius/scripts/servir_interfaz.py`, y ese repo entero
**no está en el disco**. Comprobado antes de borrar, no después.

La orden pedía no perder «los widgets decentes: mapas de aviones, barcos, batería de
la Orange Pi». No había nada que rescatar: el repo no existe, y esos mismos conceptos
**ya viven en el Ojo** (`ojo-shelter.html`, `vector.py`, `enrutador.py`, `grafo.json`).
Se enterró el contenedor, no las piezas, porque las piezas estaban en otro sitio.

Retirada de `~/.config/systemd/user/` y de `deploy/soberano/`. La copia versionada
sigue en la historia de git para quien quiera leerla.
