# Paleta de grupos marítimos (Unified Map) — ✅ RESUELTO por el Soberano

**Estado:** ✅ RESUELTO · 2026-08-04 · BLOQUE 13 · C2.
**Decisión del Soberano:** *"No le des ocho colores. El ojo no distingue ocho
tonos en marcadores pequeños sobre fondo oscuro… Cuatro o cinco familias visuales.
El color agrupa; el texto precisa."*

## Qué se decidió (y por qué NO hizo falta enmendar los tokens)

El PARA original proponía 8 tokens marítimos nuevos. El Soberano lo **rechazó** por
un motivo perceptual correcto: 8 tonos en marcador chico sobre mapa oscuro se
agrupan mal o dan "sensación de saber sin saber". Se colapsa a **5 familias**, y
esas 5 SÍ caben en los tonos más distinguibles de la paleta **existente** — por lo
que **no se añaden tokens nuevos** ni se inventa ningún hex:

| familia visual | agrupa (tipo fino ITU) | token EXISTENTE | tono |
|---|---|---|---|
| comercio | carga (70-79) + tanque (80-89) | `--voz-vocero` | cian |
| pesca | pesca (30) | `--nx-amber` | ámbar |
| pasaje | pasaje (60-69) | `--nx-phosphor` | verde |
| autoridad | pilot/SAR/policía (50/51/55/59) + militar (35) | `--nx-danger` | rojo |
| otros / desconocido | servicio, recreo, HSC, WIG, other, no declarado | `--nx-text-dim` | neutro |

- **MIL?** NO es un color de familia: es una **marca aparte** (anillo ámbar sobre
  el glifo) + método en el tooltip. Así la inferencia se ve sin gastar un color.
- **HSC (40-49)** es una **fila de tabla** (tipo fino `hsc`, decode "high-speed
  craft"), familia = otros. No es un grupo de color (decisión del Soberano).
- El **tipo fino** (carga vs tanque, tug, sail, HSC, pilot…) sigue vivo en el
  **tooltip** y en la **bitácora** — que es donde se lee de verdad. El color agrupa;
  el texto precisa.

## Desviación de §2.2 — declarada

`--voz-vocero` (color de voz) y `--nx-danger` (uso excepcional) se usan aquí como
**relleno de marcador del mapa**, lo que §2.2 no contempla ("voces solo en dots";
"danger excepcional"). Es una **excepción declarada y firmada por el Soberano** para
los marcadores del Unified Map, consistente con el uso previo del mapa (ya pintaba
barcos con `--voz-vocero` y altitud con voces). No se inventó ningún hex: los 5
tonos salen de `tokens.css`. Si el Soberano quiere formalizarlo, basta añadir a
§2.2 una línea: *"marcadores del Unified Map pueden usar {vocero, amber, phosphor,
danger, text-dim} como familias visuales; el tipo fino vive en tooltip/bitácora"*.

**Implementado:** `dashboard/src/nexo/mapa/tiposBuque.ts` (`FAMILIAS_BUQUE`,
`familiaDeGrupo`) + `UnifiedMap.tsx` (color por familia) + leyenda FULL. Sin PARA.
