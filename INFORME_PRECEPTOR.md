# Informe del Preceptor · noche del 2026-08-22

Todo lo de abajo está medido en esta máquina esta noche. Donde no pude medir,
lo digo.

**`bin/pruebas`: VERDE 278/278 · 17 suites** (empezó la noche en 264/16).

---

## §1 · Lo hecho

| Tarea | Estado | Commit |
|---|---|---|
| **A1** · XSS en `cara.py` | **no existía** · 3 pruebas nuevas de regresión | `a4f252e` |
| **A2** · Licencia de sprites | hecho · CC BY-SA 4.0, y una incoherencia más corregida | `a4f252e` |
| **A3** · CI con GitHub Actions | hecho · 5 versiones, sin stub | `ffb5877` |
| **B** · README para humanos | hecho · 407 → 167 líneas, bilingüe, con captura real | `3fbca49` |
| **C1** · `pyproject.toml` | hecho · **sin** quitar el `sys.path.insert` (ver §4) | `4cc34db` |
| **C2** · `--import` | **no hecho a propósito** · ver §4 | — |
| **C3** · Tokens de proveedor | hecho · en CORE, no en CUSTOM (ver §4) | `4cc34db` |
| **C4** · Texto del release | hecho · `RELEASE_v1.0.md` | `2dad26e` |
| **D3** · `--restore` | hecho · 8 pruebas | `62c159a` |
| **D1** · `CONTRIBUTING.md` | no llegué | — |
| **D2** · Migraciones de esquema | no llegué | — |

## §2 · Commits sin empujar

| Hash | Mensaje |
|---|---|
| `a4f252e` | seguridad y licencia: el XSS no existía, y los sprites ya tienen dueño |
| `ffb5877` | ci: las 267 pruebas en las cinco versiones que el producto declara |
| `3fbca49` | readme: una cara para humanos, y lo de auditar a su propio fichero |
| `4cc34db` | guardrails y empaquetado: cuatro proveedores más, y un pyproject que no manda |
| `62c159a` | restore: la simetría de --backup, y no era --import |
| `2dad26e` | release: el texto de v1.0.0 |

Seis en `aurelius-mvp`. Nada pendiente en `p0x`.

## §3 · Verificaciones

| Qué | Cómo | Resultado |
|---|---|---|
| Suite completa | `bin/pruebas` | **278/278** |
| Suite sin el motor en el PATH | `env PATH=/usr/bin:/bin bin/pruebas` | 278/278 — **por eso el CI no lleva stub** |
| XSS | recuerdo con `</script>` y con `onerror=` | el dato no sale del bloque; **cero `innerHTML`** en `cara.py` |
| Licencias | `grep -rn "Apache-2.0" --include="*.md"` | solo notas históricas… **y `MANIFIESTO.md`, ver §4** |
| Tokens nuevos | 7 que deben redactarse + 4 textos inocentes | 7 redactados, **0 falsos positivos** |
| `pip install -e .` | entorno limpio con `uv` | el comando `aurelius` responde |
| `git clone` + ejecutar | sin instalar nada | sigue respondiendo |
| `--restore` | 8 pruebas + prueba a mano | resguarda, pregunta, falla cerrado |
| Ejecutable de PC | arrancado y consultado | sirve la cara, el estado y el filtro real |
| README | `wc -l` + enlaces uno a uno | 167 líneas, los 7 enlaces resuelven |
| CI | **no verificado** | no puedo correr GitHub Actions desde aquí |

## §4 · Decisiones que se apartan del plan, con su motivo

**A1 · El XSS no existía.** La revisión externa lo daba por hecho. Medido: los
recuerdos viajan en un JSON dentro de un `<script>` con `</script>` ya escapado,
y el cliente los pinta con `textContent` — cero `innerHTML` en todo `cara.py`.
Escribí las tres pruebas igualmente: la propiedad estaba y no estaba declarada,
y una propiedad que nadie comprueba se pierde en el primer refactor.

**C3 · Los tokens van en CORE, no en CUSTOM.** El plan los ponía en
`CUSTOM_POLICIES`, **que se pueden apagar desde la configuración**. Un token de
Stripe no es menos grave que uno de AWS, y ese ya vivía en CORE. Los tokens de
proveedor se quedan todos en la clase que no se apaga.

**C1 · No quité el `sys.path.insert`.** El plan lo pedía. Quitarlo rompe la
primera instrucción del README —*«git clone, `python3 aurelius.py`, esa es la
instalación entera»*—. El `pyproject.toml` es para quien **quiera**
`pip install -e .`; la puerta documentada no cambia. Comprobadas las dos.

**A3 · El CI no lleva stub del motor.** El plan traía uno. Medido antes de
escribirlo: la tanda entera pasa con el PATH limpio, porque las suites de
conversación traen su propio motor sintético. Un stub sugeriría que hace falta
algo que no hace falta.

**C2 · `--import` no lo hice, y es lo que más conviene que leas.**
`--export` **redacta por contrato** — falla cerrado si no hay filtro. Un
`--import` de ese fichero devolvería `[REDACTED:API_KEY]` donde estaba tu texto.
El roundtrip que proponía el plan contaría cinco recuerdos y **degradaría los
cinco en silencio**, que es peor que no tenerlo.

La simetría sin pérdida de `--backup` es `--restore`, y esa sí está hecha. Si
aun así quieres `--import`, es una decisión de diseño tuya sobre qué significa
importar texto ya redactado — no algo que yo deba resolver callando.

## §5 · Bloqueos y hallazgos abiertos

**1 · `MANIFIESTO.md` declara «License: Apache-2.0».** Es el mismo agujero que
los sprites, una tercera vez, y contradice al README, que licencia todos los
`.md` como CC BY-SA 4.0. **No lo toqué**: relicenciar un documento es firma
tuya. Una línea, cuando la firmes.

**2 · El CI no está verificado.** El fichero está escrito y su matriz sale de
`interprete.py`, no de mi cabeza. Pero no puedo correr GitHub Actions desde
aquí: la primera vez que se sepa si pasa será tras tu push.

**3 · Un fallo mío que encontré sacando la captura.** El service worker cacheaba
`/`, y `/` cambió de `app.html` a `dashboard.html`. Sin subir la versión del
nombre de caché, **el teléfono servía la cara vieja mientras el servidor
devolvía la nueva**. Arreglado (caché v2, `skipWaiting`, `clients.claim`), y
queda escrito en el fichero: al tocar el armazón, se sube el número. **El
teléfono no lo tendrá hasta tu push.**

**4 · `docs/` sigue en el `.gitignore`.** `TECHNICAL.md`, `INSTALACION_*.md` y
`RELEASE_v1.0.md` van en la raíz por eso. Si prefieres `docs/`, hay que sacar
esa regla o hacerle una excepción — pero entonces conviene decidir qué pasa con
los entregables internos que la regla protege.

**5 · Sobre la crítica externa nº2.** Once puntos. Uno era falso (el XSS), uno
era un problema de diseño distinto del descrito (`--import`), y el resto eran
ciertos. Atendidos ocho; quedan `CONTRIBUTING.md` y las migraciones de esquema.

## §6 · Recomendaciones para la siguiente fase

1. **Firma la licencia de `MANIFIESTO.md`.** Es una línea y cierra el último
   agujero legal del árbol.
2. **Empuja y mira el CI.** Es la única forma de saber si las cinco versiones
   pasan de verdad; hasta entonces la matriz es una hipótesis con buena letra.
3. **Decide qué significa `--import`** antes de que alguien lo pida: importar
   texto redactado, o no tenerlo. Las dos son defendibles; la mala es tenerlo
   sin decir que pierde.
4. **Migraciones de esquema (`PRAGMA user_version`)** antes de la siguiente
   tabla. `captura` y `afinado` ya añadieron tablas con migración aditiva a
   mano; a la tercera conviene el mecanismo.
5. **La APK, si de verdad la quieres, empieza por medir** cuánto ocupa un
   intérprete de Python empaquetado junto al producto. Ese número decide si el
   proyecto vale la pena, y hoy nadie lo tiene.

---

*El silicio paró donde debía. El carbono decide lo siguiente.*
