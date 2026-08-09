# Reconciliación de `hexelion` — medición, 2026-08-09

Ronda CARAS-PUBLICAS-1 · Bloque 2. **Solo se mide.** No se fusionó, no se
rebasó, no se publicó. La resolución la decide el Soberano.

## Lo que se midió

Dos relaciones distintas, que la ronda planteaba como una sola:

1. El repo de trabajo `hexelion` frente a **su** remoto (el host git del rack).
2. El repositorio **público** de GitHub frente a lo que hoy sirve de verdad.

La segunda resultó no ser lo que se creía. Va en su propio apartado.

---

## 1 · `hexelion` frente a su remoto — NO han divergido

Traído sin fusionar:

```
$ git fetch --all --prune --verbose
 = [up to date]      nexo-carbono-dashboard-20260623 -> origin/nexo-carbono-dashboard-20260623
 = [up to date]      dashboard-honestidad-20260622 -> origin/dashboard-honestidad-20260622
 = [up to date]      main          -> origin/main
 = [up to date]      theme-violeta -> origin/theme-violeta
```

Rama activa `nexo-carbono-dashboard-20260623`:

```
$ git rev-list --left-right --count origin/nexo-carbono-dashboard-20260623...HEAD
0	4
```

Cuatro commits solo en local, **cero** solo en el remoto.

```
$ git merge-base origin/nexo-carbono-dashboard-20260623 HEAD
1fbaf94810b21a356d8f95d11cd1eb64c4a6d997

$ git merge-base --is-ancestor origin/nexo-carbono-dashboard-20260623 HEAD ; echo $?
0
```

La base común **es** la punta del remoto: el remoto es antecesor directo del
local. No hay divergencia, solo desacompasamiento.

```
$ git log --oneline HEAD ^origin/nexo-carbono-dashboard-20260623
5e957c2 🏛️ OLEADA VISUAL v3.0 — Sello de Oro post-recuperación
7a2481b sec(informe): redacta las credenciales Titan que quedaban en INFORME_PASADA_MATINAL
8d464cd sec(nodos): retira DEPIN_INVENTORY.md y lo sustituye por un sucesor sanitizado
49517d3 docs(nodos): HP1 INHABILITADO, HP2 limpio y reconvertido a nodo de rack

$ git log --oneline origin/nexo-carbono-dashboard-20260623 ^HEAD
(vacío)
```

`main`:

```
$ git rev-list --left-right --count origin/main...main
0	0
```

**Escenario: avance rápido posible.** Subir esta rama sería un fast-forward
limpio, sin merge ni rebase. Queda sin hacer: no se publica en esta ronda.

Nota: el árbol de trabajo de `hexelion` tiene cambios sin confirmar (borrados
y modificaciones en `dashboard/`), ajenos a esta medición y no tocados.

---

## 2 · El repositorio público — no contiene `hexelion`, contiene `p0x`

Esto no estaba previsto en la ronda y es el hallazgo que la reordena.

El repo de trabajo `hexelion` **no tiene ningún remoto en GitHub**: su único
remoto es el host git del rack. El repositorio público
`piskyRpapalo/-hexelion-public` está enganchado al repo **privado** `p0x`, como
`origin` **y** como `github`, ambos a la misma URL:

```
$ git -C p0x remote -v
github  https://github.com/piskyRpapalo/-hexelion-public.git (fetch)
github  https://github.com/piskyRpapalo/-hexelion-public.git (push)
origin  https://github.com/piskyRpapalo/-hexelion-public.git (fetch)
origin  https://github.com/piskyRpapalo/-hexelion-public.git (push)
```

Estado vivo del remoto:

```
$ git ls-remote origin
f4a7ad7fbc78a0d86ca7dc69856b16d48b0d2410	HEAD
f4a7ad7fbc78a0d86ca7dc69856b16d48b0d2410	refs/heads/master
3d4a4b93195f82c2a1b1298340926606832fbccc	refs/tags/v2026.08.08-sensor-dinamico
fcbf8f8387d02bdb105e5fd262053c6b39624d09	refs/tags/v2026.08.08-sensor-dinamico^{}
```

`f4a7ad7` es la punta de `master` de **p0x**, el repo privado con `mente/`.

```
$ gh repo view piskyRpapalo/-hexelion-public --json visibility,isPrivate
{"isPrivate":false,"visibility":"PUBLIC"}
```

### La cara pública anterior fue sobrescrita

La referencia local `github/master` conserva la cara pública sanitizada que
había antes — diez commits, otro árbol, sin `mente/`:

```
$ git log --oneline -5 github/master
4ffd475 docs(public): 3 nuevos ADR + Measured Performance + mermaid flow + Non-Goals
3ad3a85 docs(readme): System Architecture + explicit Tech Stack + achievement framing
d42dc3e docs(public): El Jardin + Teaching Kernel; higiene — sin motores internos expuestos
9cf98f2 ADRs: the constitution's load-bearing decisions, exported (sanitized)
d36a5be CI as doctrine: GitHub Actions gates + badges + rack-gates evidence

$ git ls-tree --name-only github/master
.github
.gitignore
README.md
docs
screenshots
tools

$ git ls-tree github/master mente/
(vacío)
```

Relación entre las dos historias:

```
$ git rev-list --left-right --count github/master...origin/master
10	256

$ git merge-base github/master origin/master
(vacío — no hay antepasado común)

$ git merge-base --is-ancestor github/master origin/master ; echo $?
1
```

**Historias sin parentesco.** No es un avance ni una divergencia: son dos
árboles distintos. Los 256 commits de `p0x` sustituyeron por completo a los 10
de la cara pública, y `refs/heads/master` en el remoto ya no apunta a
`4ffd475`. Solo un empuje forzado produce eso.

`4ffd475` sigue existiendo en local; en GitHub puede quedar como objeto
inalcanzable, pero ya no como rama.

**Escenario: sustitución, no reconciliación.** No hay merge ni rebase que
arregle esto — y ninguno se ha intentado. La decisión es del Soberano.

---

## Cifras

| Medición | Comando | Resultado |
|---|---|---|
| hexelion local ↔ su remoto | `git rev-list --left-right --count origin/<rama>...HEAD` | `0  4` |
| ¿divergen? | `git merge-base --is-ancestor origin/<rama> HEAD` | `0` → no |
| hexelion `main` | `git rev-list --left-right --count origin/main...main` | `0  0` |
| público: cara vieja ↔ actual | `git rev-list --left-right --count github/master...origin/master` | `10  256` |
| ¿parentesco? | `git merge-base github/master origin/master` | vacío |
| visibilidad del repo | `gh repo view … --json visibility` | `PUBLIC` |
