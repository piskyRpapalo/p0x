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
| `aurelius.service` | La cara (PWA) en `127.0.0.1:8740`, vía `bin/aurelius-servicio` | `Type=simple` + `Restart=always`, permanente | Sirve desde **`~/p0x/aurelius`** (el árbol bueno). Escribe `~/.aurelius/pwa.log` | 2026-08-25 · **FIRMADA**, `enabled`, verificada estable 25 s sin reiniciar | `systemctl --user disable --now aurelius.service` |

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
