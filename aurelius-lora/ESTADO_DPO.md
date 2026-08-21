# Estado del DPO · 2026-08-21

Sesión al límite de presupuesto. Solo pasos 1 y 2. **DPO no se lanzó.**

## 1 · Propagación · OK

Los 18 `elegido` firmados por el Soberano viajaron **verbatim** de
`datos/MITADES_QUE_FALTAN.md` a `datos/negativos.json`. Extraídos por patrón y
escritos tal cual; ni una palabra tocada.

| | |
|---|---|
| Mitades propagadas | **18** (9 casos × 2 idiomas) |
| R8 · pares mancos | **0** — antes eran 18 |
| `entrenar_dpo.py` | `pares completos: 18 · mancos: 0` |
| Guardián Fase 1 | **VERDE** (29 avisos R7, ninguno bloquea) |
| Dataset | 228 registros · 114/114 EN/ES · 72,5 KiB |

`construir_dataset.py` deja de escribir `"elegido": ""` y toma el campo del
fichero de datos, que es donde vive el contenido desde que las familias se
firmaron.

## 2 · Validador · VERDE

`forja/validar_mitades.py`, siete reglas firmadas. **Las 18 mitades pasan.**

Y se falsificó, porque un validador que aprueba todo puede estar simplemente
roto: contra los 18 `rechazado` —que deben disparar— **caza 9**. Emojis, color
como estado, lista negra y evasión sin causa saltan donde tienen que saltar.

Comprobado además lo que **no** debe marcarse:

| | |
|---|---|
| «no puedo decirte si todo el árbol pasa» | **pasa** |
| «I can't tell you if the whole tree passes» | **pasa** |
| «…grupos de pruebas… están validados…» | **pasa** |
| «…test groups… are validated…» | **pasa** |

La regla de evasión mira **el verbo que sigue** al «no puedo», no el «no puedo».
Negarse a afirmar lo que no se ha mirado es el sensor honesto; cerrar la puerta
sin decir por qué es lo que se caza.

**Observación, no corrección.** La lista negra es literal: el rechazado inglés
de `F1/relleno` dice *«We go way back»* donde el español dice *«somos viejos
conocidos»*, y no está en la lista firmada. Los cuatro de F3 y los dos de voseo
tampoco disparan — sus rupturas son de momento y de registro dialectal, que
ninguna de las siete reglas mira. Se dice; no se amplía la lista por iniciativa.

## 3 · Lo que queda

**DPO PENDIENTE: lanzar con presupuesto fresco (tras reset semanal).**

Todo lo que necesita está en su sitio y verificado:

- `forja/entrenar_dpo.py` · cerrojo doble, ya sin bloqueo por pares mancos.
  Ahora solo espera la bandera.
- Referencia por `disable_adapter()` · pico ~9 GiB en vez de 16.
- `pruebas/humo_dpo.py` · instrumento verificado: margen +0,0000 → +15,1095.
- 18 pares completos, firmados y validados.

**Orden sugerido cuando haya presupuesto:** DPO desde el base (aísla la
pregunta), tester completo, y la comparación de EC-2.4 contra `−0,1421` de r=8
y `−0,1052` de r=4. Si el margen cruza cero, el canon aprendió a decir que no.

**Sin tocar, como se ordenó:** DPO, tester, push, `LORE.md`, `ARQUETIPO.md`, el
Doogee.
