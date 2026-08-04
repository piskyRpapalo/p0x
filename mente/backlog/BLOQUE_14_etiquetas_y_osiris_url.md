---
id: bloque-14-etiquetas-osiris-url
titulo: BLOQUE 14 · Etiquetas de nodo obsoletas y URL de OSIRIS apuntando a un nodo muerto
tipo: operativo
clase: backlog
actualizado: 2026-08-04
---

# BLOQUE 14 · Etiquetas de nodo y `OSIRIS_GDELT_URL`

**Estado:** ⬜ pendiente · abierto 2026-08-04 por decisión del Soberano (ronda SOBERANO-DECISIONES)
**Coste:** S el 14.1 · M el 14.2 · **Apalancamiento:** medio — es honestidad del dashboard, no estética

**Regla de esta ronda, innegociable:** *no se toca el código vivo del dashboard todavía.* Aquí solo
vive el plan. El BLOQUE 9 se desplegó hace unas horas y el gateway lleva minutos estable; meterle
otro cambio sin prueba sería exactamente el error que el BLOQUE 9 existe para no repetir.

## Por qué existe

Dos cosas del dashboard **afirman algo que ya no es cierto**. Ninguna es un fallo estético: las dos
hacen que un panel diga saber cosas que no sabe.

1. `legion_sol` y `legion_luna` están etiquetados **«DePIN Worker»**. `legion_sol` es
   `musculo-hp-01`, hoy **inhabilitado** (offline en la tailnet, retirado del canon). `legion_luna`
   es `musculo-hp-02`, al que **se le retiraron hoy todos los servicios de *earning*** — ya no hace
   DePIN de ninguna clase; pasa a ser nodo de rack.
2. `OSIRIS_GDELT_URL` apunta al `:3000` de `musculo-hp-01`, un nodo **muerto desde hace 10 días**.

## 14.1 · Reetiquetar los dos nodos

Sitios exactos, verificados el 2026-08-04 (repo `hexelion`):

| Fichero | Línea(s) | Qué dice hoy |
|---|---|---|
| `hexelion_pollers.py` | 37-38 | `kind: "depin_worker"` para `legion_sol` y `legion_luna` |
| `hexelion_pollers.py` | 216, 239, 324-325 | colectores `collect_legion_sol` / `collect_legion_luna` |
| `disk_poller.py` | 47-48 | nombres «Legión Sol · HP1» / «Legión Luna · HP2» |
| `hexelion_gateway.py` | 334 | `"legion_sol": {..., "role": "DePIN Worker"}` |
| `hexelion_gateway.py` | 738 | `_NODE_IDS_V6` incluye ambos |
| `hexelion_gateway.py` | 2489 | peso/orden `"legion_sol": 12` |

**Propuesta de destino:**

- `legion_sol` → rol `INHABILITADO`. **No se borra del mapa**: un nodo que desaparece de la vista
  se confunde con un nodo sano. Debe verse, y debe verse *caído*, con la fecha del último contacto.
- `legion_luna` → rol `Nodo de rack`. Sin métricas de *earning*, que ya no existen.

**Trampa a evitar:** si el colector de `legion_sol` deja de ejecutarse y el panel simplemente se
queda en blanco, habremos sustituido un dato honesto («caído desde tal fecha») por un hueco mudo.
El estado `INHABILITADO` tiene que ser **explícito y con antigüedad declarada**.

## 14.2 · `OSIRIS_GDELT_URL`

Hoy: `hexelion_gateway.py:1999` apunta al `:3000` de `musculo-hp-01`. El gateway hace *pull*, falla,
y el panel OSINT queda vacío — que es **honesto por accidente**, no por diseño.

**Propuesta:** mientras OSIRIS no exista en ningún sitio, la URL no debe apuntar a una máquina
muerta: el estado correcto es **`NO DATA` declarado**, con el motivo («OSIRIS inhabilitado con
`musculo-hp-01`, sin origen del código») y la fecha. Cuando OSIRIS se instale en `musculo-hp-02`,
se repunta ahí.

**Bloqueo previo, y es real:** el código de OSIRIS **vive en `musculo-hp-01` y no hay de dónde
copiarlo** — sin repo remoto conocido, sin imagen publicada, sin backup localizado. Hasta resolver
eso, 14.2 solo puede llegar hasta el `NO DATA` explícito.

## Criterio de cierre

- Ningún panel afirma que un nodo hace DePIN cuando no lo hace.
- `legion_sol` aparece **visible y declarado inhabilitado**, con antigüedad del dato — no ausente.
- El panel OSINT dice `NO DATA` **por decisión declarada**, no porque una petición falle en silencio.
- `tsc`/tests y arranque del gateway verdes; el gateway sigue bajo systemd, no bajo un proceso manual.
