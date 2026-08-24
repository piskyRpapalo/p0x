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

| `aurelius.service` | «Aurelius Brain Service» · `bin/aurelius-servicio` desde `aurelius-mvp` | `Type=simple` + `Restart=always`, corriendo desde 2026-08-23 02:21 | `WorkingDirectory` y `ExecStart` apuntan a **`aurelius-mvp`**, no a `aurelius` | **NO firmada · encontrada por el chequeo de cierre el 2026-08-24** | `systemctl --user stop aurelius.service` |

### Sobre `aurelius.service` — hallazgo del primer día de la regla

Estaba corriendo **antes** de que la regla se firmara, y no lo puso esta sesión. Lo encontró
el `systemctl --user list-units` de cierre, que es exactamente para lo que existe ese
chequeo. Tres cosas que el Soberano tiene que decidir:

1. **`enabled` dice `disabled` pero está `active`.** Se arrancó a mano y lleva vivo desde el
   23 de agosto. Al reiniciar la máquina **no volverá**, así que hoy hay un servicio que
   funciona y que nadie podría reproducir.
2. **Sirve desde `aurelius-mvp`, no desde `aurelius`.** Es el árbol cuya rama `main` estuvo
   sesenta commits divergida. Lo que ese servicio está sirviendo ahora mismo no es
   necesariamente lo que hay en `origin/main`.
3. **`Restart=always` sin firma.** Un servicio que se relanza solo, indefinidamente, es
   justo la figura que la regla nombra: algo con autoridad corriendo cuando nadie mira.

Propuesta, sin ejecutar: decidir si se firma (y entonces `enable`, y apuntarlo al árbol
bueno) o se para. **No se toca hasta que lo digas**: llevaba dos días sirviendo y pararlo
por iniciativa propia sería romper algo que funciona sin saber quién lo usa.

## Lo que NO está activado, y por qué

- `director` (L4) — construido y probado, **sin cronificar**. Es el meta-bucle: planifica
  ventanas y escribe a la bandeja de firmas. Se activa cuando haya más de un bucle que
  dirigir.
- `s0` — construido y probado, **sin cronificar**. Semanal. Se activa cuando haya varios
  filtros de los que sospechar; con uno solo no tiene de qué.
- `afinador`, `centinela`, `peregrino`, `medico`, `escriba`, `cronista`, `vigia` — **no
  existen todavía**. Son L1/L2/L3 y están sin escribir. No se cronifica lo que no está
  construido y probado.
