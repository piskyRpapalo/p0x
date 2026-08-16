---
id: acta-d78-d80
titulo: Acta D78-D80 · de dónde sale cada afirmación del canon, y cómo recomprobarla
tipo: operativo
clase: operativo
version: 1.0.0
sistema: MVP
estado: PROPUESTA · pendiente de firma del Soberano
actualizado: 2026-08-16
---

# ACTA D78 – D80

Respaldo de las entradas `D78` a `D80e` de `Cuarentena/03_ESTADO_FIRMADO.md`.

**Para qué existe.** Las entradas del canon son cortas a propósito: dicen la
decisión y su porqué. Este documento dice **de dónde sale cada una y con qué
orden se vuelve a comprobar**, para que un auditor que llega sin contexto no
tenga que creerse nada. Si una fila de aquí no se puede reproducir, la entrada
de canon que sostiene está mal y se corrige la entrada.

**Repositorios.** Son dos y no se confunden:

| | |
|---|---|
| **Producto** | `~/p0x/aurelius-mvp` → `github.com/piskyRpapalo/aurelius`, rama `main` |
| **Canon** | `~/p0x` → `jetson:p0x.git`, rama `master`. **No empujado a fecha de este acta.** |

---

## §1 · TABLA DE PROCEDENCIA

| D | Qué afirma | Commit(s) | Fichero(s) | Cómo se recomprueba |
|---|---|---|---|---|
| **D78** | El generador de leitmotivs viaja con el repo y es determinista | `6b354c8` (lo trae), `6d3f379` (lo hace determinista) | `generar_leitmotivs.py` | `git log -S "random.Random" -- generar_leitmotivs.py` · `python3 -m unittest test_leitmotivs` (13) |
| **D78b** | Apagado de hardware del producto, tres puertas, por entorno | `6d3f379` (alta de fichero) | `silencio.py` (+63) | `git log --diff-filter=A -- silencio.py` · `python3 -m unittest test_silencio` (9) |
| **D79** | Una sola gramática para elegir, voz y teclado | `6d3f379` | `fuga.py:103` `numero_dicho()` | `git log -S "def numero_dicho" -- fuga.py` · casos 25–28 de `test_fuga.py` |
| **D79b** | Permiso del gerente: fila ausente = `no`, comprobado dentro | `6d3f379` | `fuga.py:157` `:177` | `git log -S "def permiso_concedido" -- fuga.py` · casos 19–24 de `test_fuga.py` |
| **D79c** | Rango de intérpretes medido, declarado, no bloqueante | `1ee1b3f`, `e531b5b` | `bin/pruebas`, `interprete.py`, `test_interprete.py` | `./bin/pruebas` (cabecera) · `python3 -m unittest test_interprete` (6) |
| **D80** | Un solo escritor de `profile`, con `ON CONFLICT` | `5f56b15` | `memory.py`, `fuga.py` | caso 22 de `test_memory.py` · ver §2 |
| **D80b** | `EXCEPCIONES.md` y `LIMITES_DEL_CRITERIO.md` en la raíz | `2c2c163`, `bd52d76` | los dos `.md` | `git ls-files '*.md'` → 7 · `git check-ignore` → 1 |
| **D80c** | `TMPDIR` fijado + enmienda del acta del rojo | `fd518b6` (etiquetado `M-D80b`) | `bin/pruebas`, `LIMITES_DEL_CRITERIO.md` | `./bin/pruebas` (cabecera) · ver §3 |
| **D80d** | Incidente de borrado del clon | — (sin commit; documental) | `Cuarentena/salida/INCIDENTE_BORRADO/` | `DIAGNOSTICO.md`, `PYTHON_314.md` |
| **D80e** | Estado verificado al cierre | `fd518b6` | árbol entero | `./bin/pruebas ; echo $?` |

**Aviso de numeración, repetido aquí porque es donde un auditor tropieza.** Las
etiquetas de los mensajes de commit y los números de canon **no coinciden en
dos sitios**, y la historia no se reescribe para taparlo:

- `6d3f379` dice «M-D79» y contiene D78 (parte), **D78b**, **D79** y **D79b**.
- `fd518b6` dice «M-D80b» y es lo que el canon llama **D80c**.

Manda `03_ESTADO_FIRMADO.md`. La etiqueta del commit es como quedó escrita.

---

## §2 · D80 · LA PRUEBA CONTRA LAS DOS IMPLEMENTACIONES

Es la fila que más fácil sería creerse sin comprobar, así que va entera.

**Con `ON CONFLICT DO UPDATE`** (árbol real):

```
  ok    · 22 · reescribir una clave que YA EXISTE no borra el resto de su fila
RESULTADO: 25/25 correctos, 0 fallo(s)
```

**Con `INSERT OR REPLACE`** (misma prueba, sobre una copia del árbol; original
intacto, sha256 `8486723ebf8e1cc5` antes y después):

```
  FALLO · 22 · reescribir una clave que YA EXISTE no borra el resto de su fila
          -> la columna que la sentencia no nombra volvio a su DEFAULT (x)
RESULTADO: 24/25 correctos, 1 fallo(s)
```

**Y por qué la prueba tiene la forma que tiene** — con clave nueva no
distinguiría nada:

```
── ON CONFLICT ──                    ── INSERT OR REPLACE ──
  clave NUEVA     -> 'x'               clave NUEVA     -> 'x'
  clave EXISTENTE -> 'personalizado'   clave EXISTENTE -> 'x'
```

**Alcance real de la corrección, para que no se cuente al revés.** `profile`
tiene hoy exactamente tres columnas —`key`, `value`, `updated_at`— y la
sentencia vieja **las nombraba las tres**. Medido: no se perdió ningún dato.
La corrección es **preventiva** (un solo escritor, y sentencia correcta el día
que la tabla gane una columna), no reparadora.

---

## §3 · D80c · LA MEDICIÓN QUE OBLIGÓ A ENMENDAR EL ACTA

| Medida | Valor |
|---|---|
| `/tmp` | `tmpfs`, 29 GB — **RAM** |
| `/var/tmp` | `/dev/nvme0n1p2`, ext4, 541 GB libres | <!-- guardia:permitir /var/tmp es prefijo de sistema (FHS), no el home de nadie; es el dato medido de D80c -->
| `TMPDIR` antes del commit | **no puesto** → `tempfile` resolvía a `/tmp` |
| Temporal capturado en vivo tras el commit | `/var/tmp/sab_fuga_awsve7af` (0 en `/tmp`) | <!-- guardia:permitir /var/tmp es prefijo de sistema (FHS), no el home de nadie; es el dato medido de D80c -->
| Guarda con `TMPDIR` inescribible | `salida=2`, mensaje explícito |

**El punto que corrige el acta:** un `tmpfs` lleno devuelve `ENOSPC` **sin
dejar rastro en el journal y sin disparar `oom-kill`**. Por eso «cero líneas en
`journalctl`» es evidencia contra el disco y **no** es evidencia contra la RAM.
El flanco no está descartado; ha dejado de poder ocurrir por accidente.

---

## §4 · ESTADO MEDIDO AL CIERRE

```
── AURELIUS · TODAS LAS PRUEBAS ────────────────────────────────
  Python 3.14.4 · /usr/bin/python3
  [...]           (la linea de TMPDIR va en la tabla de §3, no aqui)
  224 pruebas · 13 suites · 6 corredores
  ok    test_idioma.py --sabotaje       4/4 detectadas
  ok    test_fuga.py --sabotaje         6/6 detectadas
VERDE · 224/224          salida=0
```

| Verificación | Dónde | Árbol | Resultado |
|---|---|---|---|
| `bin/pruebas` | Soberano, 3.14.4 | `fd518b6` | 224/224, salida 0 |
| `bin/pruebas` | Soberano, 3.10.12 (`uv` standalone) | `fd518b6` | 224/224, salida 0 |
| `bin/pruebas` | **Sandbox del Preceptor**, 3.10.12 | `5a86cc6` | 224/224, salida 0 |
| `bin/pruebas` | Sandbox del Preceptor, 3.10.12 | `73f7bc6` | 217/217, salida 0 |

**Acotación que no se debe perder:** la única verificación en **máquina
independiente** es la de `5a86cc6`. El commit `fd518b6` (D80c) está verificado
solo en el Soberano, en dos intérpretes. No se cuenta como reproducido fuera
hasta que lo esté.

---

## §5 · LO QUE ESTE ACTA NO CIERRA

- **El mecanismo del rojo del 2026-08-16.** `NO_DATA`. La correlación con el
  fichero de 18.000 bytes sigue en pie; el disco está descartado; la presión
  de memoria sobre `tmpfs` **no** lo está.
- **La prueba de recuperación hecha a propósito** (borrar, restaurar desde el
  remoto, cronometrar, exigir verde). Es el único test que mediría lo único
  que el producto promete. Sigue sin hacerse.
- **`aurelius.py` sin cobertura por importación.** 21 KB, punto de entrada del
  producto; ninguna suite lo importa. `test_interprete.py` es lo primero que lo
  arranca, y solo como subproceso y solo para `--view`.
- **El push de `p0x` a `jetson`.** Sin hacer. Todo lo de esta ronda vive en un
  solo disco.

---

Pendiente de firma del Soberano.
