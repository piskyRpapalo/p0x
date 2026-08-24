# UNIDADES ACTIVAS EN `soberano`

Registro de todo lo que corre sin que nadie mire. **Una fila por unidad, y ninguna
unidad sin fila.** Si algo corre y no está aquí, o está aquí y no corre, una de las dos
cosas es mentira y hay que averiguar cuál.

Regla que gobierna este fichero: *«no se crean servicios systemd sin aprobación explícita
del Soberano»* + *«`systemctl --user list-units` al cerrar cada sesión»*. Firmada
2026-08-24, tras dos meses en el archivo sin llegar al repo.

| unidad | qué hace | cuándo | qué toca | firmada | cómo se apaga |
|---|---|---|---|---|---|
| `guardian.timer` | Vigila que no entre en el árbol de Aurelius un `import` fuera de la biblioteca estándar | diario 04:00 (±15 min) | **Solo lee** `~/p0x/aurelius`. Escribe latidos y hallazgos en `~/.aurelius/loops.db` | 2026-08-24 | `systemctl --user disable --now guardian.timer` |

## Lo que NO está activado, y por qué

- `director` (L4) — construido y probado, **sin cronificar**. Es el meta-bucle: planifica
  ventanas y escribe a la bandeja de firmas. Se activa cuando haya más de un bucle que
  dirigir.
- `s0` — construido y probado, **sin cronificar**. Semanal. Se activa cuando haya varios
  filtros de los que sospechar; con uno solo no tiene de qué.
- `afinador`, `centinela`, `peregrino`, `medico`, `escriba`, `cronista`, `vigia` — **no
  existen todavía**. Son L1/L2/L3 y están sin escribir. No se cronifica lo que no está
  construido y probado.
