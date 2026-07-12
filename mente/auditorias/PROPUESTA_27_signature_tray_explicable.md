<!-- PROPUESTA no ejecutada — diseño para revisión del Soberano.
     Misión PUERTA VERDE 2026-07-12. Sin front-matter §2 a propósito:
     este archivo es un documento de diseño, no un MD evolutivo del grafo
     (build_graph no debe proyectarlo). Nada de lo descrito aquí está
     implementado; adoptarlo es una decisión de firma (→ sugerencia #68). -->

# PROPUESTA 27 — Bandeja de firma explicable
### Que cada fila de PENDIENTES.md pueda decir su nivel, su prioridad, si es reversible y dónde está su doc — sin romper nada de lo que ya funciona

---

## 1 · Problema

La bandeja `/tareas` muestra las filas de `PENDIENTES.md` tal cual: texto técnico,
sin prioridad declarada, sin saber si firmar algo es reversible, y sin enlace al
documento que lo explica. Para el Soberano funciona; para el objetivo
"traductor a analfabeto" (que cualquier persona de la casa entienda qué firma)
falta una capa declarativa.

## 2 · Esquema elegido: marcadores inline retrocompatibles

En la celda **Sugerencia** de las filas NUEVAS (append-only §4.3 intacto: las
filas viejas jamás se reescriben), al final del texto:

```
| 72 | **Regar automático**: bomba 5V con timer [prio:media] [rev:sí] [doc:mente/manual/riego.md] | M | propuesta |
```

Gramática (todos opcionales, orden libre, siempre al final de la celda):

```
marcador   := "[" clave ":" valor "]"
prio       := "[prio:" ("alta"|"media"|"baja") "]"
rev        := "[rev:" ("sí"|"no") "]"          # ¿revocable tras firmar?
doc        := "[doc:" ruta-relativa-p0x ".md]"  # doc que lo explica
```

El **nivel básico** no necesita marcador nuevo: es la convención ya presente
`**negrita**:` al inicio de la celda — la parte en negrita es el titular llano;
lo que sigue a los dos puntos es el detalle técnico. Render básico = solo la
negrita; render experto = celda completa.

## 3 · Extracción (mismo mecanismo probado que `[aud:slug]`)

```python
_TAREA_MARCA_RE = re.compile(r"\[(prio|rev|doc):([^\]]+)\]")

def extraer_marcadores(texto_celda: str) -> tuple[str, dict]:
    marcas = dict(_TAREA_MARCA_RE.findall(texto_celda))
    limpio = _TAREA_MARCA_RE.sub("", texto_celda).rstrip()
    return limpio, marcas   # marcas ausentes → la UI no muestra el dato (honesto)
```

Compatibilidad verificada por construcción con el parser actual de `/tareas`:
- el split de celdas usa `(?<!\\)\|` — los marcadores no contienen `|`;
- `[aud:slug]` ya convive dentro de la celda sin romper nada (probado en vivo);
- una fila sin marcadores se comporta exactamente igual que hoy (todo opcional);
- el estado sigue viviendo SOLO en la celda Estado — los marcadores son
  metadatos de lectura, jamás de máquina de estados.

## 4 · Mock de render en /tareas

```
┌──────────────────────────────────────────────────────────────┐
│ #72 · Regar automático                        [prio: media]  │
│ ▸ bomba 5V con timer                                         │
│ firmar es reversible (rev:sí) · explicación: riego.md ↗      │
│ [ FIRMAR ]  [ APLAZAR ]  [ DESCARTAR ]                       │
└──────────────────────────────────────────────────────────────┘
```

- `prio:alta` → borde ámbar y orden arriba; sin prio → orden actual.
- `rev:no` → el botón FIRMAR pide doble confirmación con texto llano
  ("esto no se puede deshacer con otro clic").
- `doc:` → enlace "explicación ↗"; ruta inexistente → se muestra en gris con
  "(doc aún no escrito)" — honesto, no roto.
- Toggle basico/experto de página: básico muestra solo el titular en negrita
  + los marcadores traducidos a frases llanas.

## 5 · Plan de adopción (si se firma #68)

1. Añadir `extraer_marcadores` al bloque TAREAS del gateway y exponer
   `prio/rev/doc/titular` en `GET /api/tareas` (solo lectura, cero escritura).
2. Render en `/tareas` según el mock (§4), con toggle basico/experto.
3. Empezar a usar marcadores en las filas nuevas de PENDIENTES.md (las
   misiones los añaden al proponer; el Soberano puede añadirlos a mano).
4. Nada retroactivo: las filas #1–#71 quedan como están.

## 6 · Trade-off documentado: ¿y una columna nueva?

Alternativa descartada: añadir columnas `Prio | Rev | Doc` a la tabla.
- En contra: rompe el parser actual (espera 5 celdas exactas), obliga a
  reescribir TODAS las filas históricas (viola append-only §4.3), y los diffs
  de git se vuelven ilegibles al tocar cada línea.
- A favor (reconocido): más legible en el MD crudo y validable por posición.
- Veredicto: los marcadores inline ganan porque extienden sin migrar — el
  mismo razonamiento que ya validó `[aud:slug]` en producción. Si algún día
  PENDIENTES.md se parte en archivos por año (poda), reevaluar columnas ahí.
