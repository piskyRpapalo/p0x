# PROPUESTA · Enmienda al Blueprint §2.2 — paleta de grupos marítimos

**Estado:** ⬜ PROPUESTA (propose-only) · requiere firma del Soberano · 2026-08-04
**Origen:** BLOQUE 13 · C2 (color por grupo de buque). **Motivo del PARA:** la
invariante del bloque prohíbe elegir un color por cuenta propia; la paleta actual
no cubre 8 grupos marítimos distintos, así que se detiene el color-por-grupo y se
propone esta enmienda en lugar de inventar tonos o colisionar categorías.

## Por qué la paleta actual NO cubre el caso (medido, no opinado)

`tokens.css` / Blueprint §2.2 (paleta EL NEXO, **restrictiva**):
- Colores de VOZ (vocero cian, alquimista índigo, enlace cian-pálido, escriba
  ámbar, monje verde, berserker rojo) están declarados **"SOLO en dot de estado y
  borde-izquierdo 2px de su cápsula; jamás en texto ni fondos"** → no son usables
  como relleno de marcador sin violar §2.2.
- `--nx-danger` (rojo) es de **"uso excepcional"** (fallo/ERROR/crítico).
- Quedan como tonos de marcador sancionados y legibles sobre mapa oscuro:
  `--nx-phosphor` (verde), `--nx-amber` (ámbar), `--nx-text-dim`/`--nx-text-ghost`
  (neutros). **≈3 tonos** para **8 grupos** (pesca, servicio, pasaje, carga,
  tanque, recreo, autoridad, militar) + desconocido.

BLOQUE 13 exige tipo por `shiptype` (ITU-R M.1371) medido en el feed real
(ais-catcher, La Fragua, 2026-08-04): shiptype ∈ {0,40,52,60,65,68,70,71,79,81}.
La forma del marcador (casco vs avión) YA distingue barco de aeronave sin color
(daltonismo). Lo que falta es el color-por-grupo, y ahí está el hueco.

## Qué se pide firmar

Añadir a §2.2 un sub-bloque **"Marcadores del Unified Map (grupos marítimos)"**
con 8 tokens dedicados + el neutro de desconocido. Requisitos que la firma fija:
1. Distinguibles entre sí sobre el fondo `--nx-void` (mapa oscuro CARTO).
2. Emparejados con FORMA (ya implementada) para robustez ante daltonismo.
3. `militar` = tono de atención (la inferencia MIL? debe saltar), sin ser el rojo
   de fallo exclusivo del sistema.
4. `desconocido` = neutro (reutiliza `--nx-text-dim`, ya sancionado).

Tokens propuestos (nombres estables; **hex CANDIDATO, a ajustar/firmar** — no se
pintan hasta la firma):

| grupo | token | hex candidato | nota |
|---|---|---|---|
| pesca | `--nx-mar-pesca` | `#7FC8A9` | verde-mar apagado |
| servicio | `--nx-mar-servicio` | `#9AA7B0` | gris-azulado (trabajo) |
| pasaje | `--nx-mar-pasaje` | `#43F5A0` | = `--nx-phosphor` (vida) |
| carga | `--nx-mar-carga` | `#4CC9F0` | cian (grupo dominante medido) |
| tanque | `--nx-mar-tanque` | `#C08CE0` | violeta (química/peligro) |
| recreo | `--nx-mar-recreo` | `#FFD27F` | arena cálida |
| autoridad | `--nx-mar-autoridad` | `#FFB454` | = `--nx-amber` (autoridad/atención) |
| militar | `--nx-mar-militar` | `#FF7A7A` | rojo-coral (inferencia MIL?, ≠ danger) |
| desconocido | `--nx-text-dim` | `#6E8A7C` | ya existe (neutro) |

## Lo que YA está hecho sin la firma (no bloqueado por el color)

- Tabla de tipos ITU única (`tiposBuque.ts`) + REGLA DURA (desconocido, jamás el
  más cercano). Inferencia militar (AIS type 35 / rango ICAO) etiquetada MIL? con
  método. Forma casco vs avión. Bitácora del día en la vista FULL. Tests verdes.
- El color de todos los barcos es hoy un **único** color base (heredado). Al
  firmar esta paleta, el cambio es aditivo: leer `meta.tokenPropuesto` por grupo
  en `UnifiedMap.tsx` (el `MetaGrupo.tokenPropuesto` ya apunta a estos nombres).

**Al firmar:** se añaden los tokens a `tokens.css` + §2.2, y se conecta el color
por grupo en el mapa (una línea por grupo). Reversible: sin firma, un color base.
