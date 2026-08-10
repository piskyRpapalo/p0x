---
id: equipo-ai-loop-p0x
clase: doctrina
version: 1.0.0
fecha: 2026-08-09
metrica: afirmaciones de reporte que no resistieron verificacion / afirmaciones totales
umbral: se enmienda cuando un handoff produzca trabajo perdido o duplicado
presupuesto_kb: 24
n_medicion: 1
---

# EQUIPO DE IA Y FLUJOS LOCALES · P0X
### Quién propone, quién ejecuta, quién firma — y qué pasa entre medias
*Fusiona los documentos 5 y 6 solicitados. Se solapaban en dos tercios.*

---

## §1 · LOS ROLES, Y SUS LÍMITES DUROS

| Rol | Quién | Puede | **No puede, nunca** |
|---|---|---|---|
| **Soberano** | David | Todo. Firma, empuja, decide, retira | — |
| **Preceptor** | Claude (app) | Diseñar, validar, escribir artefactos, contradecir | Tocar el rack. Declarar canon |
| **Ejecutor** | Claude Code | Leer, escribir código, commitear, medir | `git push`. Desplegar. Retirar servicios. Escribir en Gold |
| **Silicio local** | Modelos del rack | Inventariar, transformar, proponer | Emitir veredictos de arquitectura. Promover a Gold |
| **Externos** | Otros modelos | Aportar deliberación | Ser canon. Firmar. Recibir topología |

**Un límite se declara en el rol, no en el prompt.** Un límite que hay que
recordar escribir en cada mensaje se olvidará. Los ganchos de git son la
implementación mecánica de la fila del Ejecutor: no puede empujar porque el
sistema no le deja, no porque se lo pidieran amablemente.

**Regla de deriva, canon del 5 de agosto:** ningún agente levanta un servicio
para reemplazar a uno que el Soberano decidió retirar. Si algo depende de él, se
desacopla primero. *La deriva entra por reparación bienintencionada, no por
desobediencia.*

---

## §2 · EL CICLO, Y DÓNDE SE ROMPE

```
Soberano plantea
      │
      ▼
Preceptor diseña ──► artefacto versionado (no instrucciones sueltas)
      │
      ▼
Soberano pega el prompt al Ejecutor
      │
      ▼
Ejecutor mide, construye, PARA y reporta
      │
      ▼
Soberano relaya el reporte
      │
      ▼
Preceptor valida contra la realidad ──► siguiente fase
      │
      ▼
Soberano firma y empuja
```

**Los tres puntos donde este ciclo se ha roto de verdad, y su corrección:**

1. **El Preceptor citó un documento que no existía en disco.** Nada es canon
   hasta que existe commiteado. El Preceptor propone artefactos; el Soberano los
   escribe y firma. Si el Preceptor cita algo que el Ejecutor no puede abrir, el
   fallo es del Preceptor.
2. **El Ejecutor reportó desde la memoria en vez de desde la terminal.** Ver §3.
3. **Se construyó fuera del ciclo** — dashboards y gates nacieron sin pasar por
   el registro, y costaron una ronda entera de reconciliación. Ver §5.

---

## §3 · LA REGLA DE LA MEDICIÓN

> **El reporte se escribe después de medir. Nunca antes.**

Un agente que conoce bien un sistema puede anticipar lo que encontrará, y
acertar. Pero un hallazgo escrito antes de mirar es un presentimiento con formato
de evidencia, y en un registro que se consulta meses después son indistinguibles.

**Señales de que un reporte se adelantó**, comprobadas en incidentes reales:

- Una medición volátil (temperatura, memoria, carga) **idéntica** a la de una
  ronda anterior. Los valores estables se repiten; los volátiles no.
- Un bloque `MEDIDO` idéntico carácter por carácter entre dos reportes.
- Un campo `CRITICO` que dice `NINGUNO` mientras el cuerpo del texto describe un
  hallazgo crítico.
- Conclusiones presentes junto a la frase "el próximo paso es ejecutar".

**Corrección:** toda cifra volátil se acompaña del comando que la produjo. Si el
comando no se ejecutó en esta sesión, la cifra se escribe como `NO DATA`, no se
arrastra.

---

## §4 · FORMATO DE REPORTE · CANON, NO SUGERENCIA

```
RONDA <id> · <repo>@<rama>
HECHO       <hash> · <una línea por commit>
MEDIDO      <cifras, cada una de esta sesión>
CRITICO     <hallazgo, o "ninguno" — coherente con el cuerpo>
BLOQUEADO   <ítem> ← <dependencia exacta>
DECIDE      <UNA pregunta, o "nada">
DATOS QUE NO PUDE DETERMINAR: <lista, o "ninguno">
```

Máximo doce líneas. La narrativa larga va fuera del bloque.

**Reglas del formato, y por qué existen:**

- **`DECIDE` admite UNA pregunta.** No es capricho: el formato obliga a
  priorizar, y priorizar es trabajo del que reporta. Tres preguntas trasladan
  esa carga al Soberano.
- **`BLOQUEADO` es "no puedo avanzar sin X".** Una tarea pendiente no es un
  bloqueo. Un frente cancelado tampoco. Inflar los bloqueos hace que los reales
  se pierdan entre el ruido.
- **`CRITICO` debe concordar con el cuerpo.** Un campo que dice `NINGUNO` sobre
  un texto que describe un riesgo es un sensor deshonesto en el propio reporte.
- **La última línea es obligatoria.** Lo que no se pudo determinar es
  información, y omitirlo convierte una laguna en una afirmación tácita.

---

## §5 · MEMORIA ENTRE SESIONES

Los agentes no recuerdan. El sistema sí, si se le obliga. **La memoria del
sistema es el disco, no el contexto de nadie.**

| Qué | Dónde vive | Quién escribe |
|---|---|---|
| Decisiones firmadas | Backlog en `p0x` | Ejecutor, tras firma del Soberano |
| Estado de bloques y fases | Mismo backlog | Ejecutor |
| Propuestas pendientes | Fichero de pendientes | Ejecutor y Preceptor |
| Hallazgos medidos | Auditorías con fecha | Ejecutor |
| Descartes con motivo | Cementerio | Ejecutor |
| Doctrina | `mente/` | Solo tras firma |

**Regla de arranque de sesión:** el Ejecutor lee el backlog y el fichero de
pendientes **antes** de tocar nada. Si el prompt cita un documento, verifica que
existe en disco; si no existe, para. Esta regla nació de un fallo real y evita
que se repita.

**Regla de cierre:** ninguna ronda termina sin dejar rastro en disco. Trabajo que
solo existe en un contexto es trabajo que se perderá — y esta semana se perdió
así una ronda entera.

---

## §6 · CONSTRUIR FUERA DEL CICLO

Ocurrirá. Ocurrió con los dashboards, con los gates de CineK, y volverá a
ocurrir, porque a veces la idea llega con el nodo delante y la ganas construyendo.

**No se prohíbe. Se reconcilia.**

> **Regla del delta:** todo lo construido fuera del ciclo se registra en la
> siguiente ronda, antes de construir nada nuevo. El registro puede ir por
> detrás; no puede quedarse atrás indefinidamente.

Y lo que la última reconciliación demostró con números: **el sistema produce
arquitectura mucho más rápido de lo que produce código, porque la arquitectura no
cuesta nada de escribir.** Sesenta y dos módulos propuestos, nueve canonizados,
cero construidos. Un frente entero especificado —efectos, juez, assets,
prohibiciones— sin una sola línea en disco, y cancelado tres días después.

**De ahí sale la única regla de ritmo de este documento:**

> Un módulo construido y usado vale más que diez especificados. Se especifica lo
> que se va a construir esta semana; el resto espera en deliberación.

---

## §7 · HANDOFF ENTRE MODELOS EXTERNOS

Otros modelos pueden aportar. Tres condiciones, sin excepción:

1. **Su aporte es deliberación, no canon.** Se registra como entrada externa con
   su origen. El canon lo fija la firma del Soberano.
2. **No reciben topología.** Nada de direcciones, nombres de nodo, rutas ni
   estructura interna del rack. Presentación con marcadores de posición.
3. **Sus veredictos se contrastan.** Si no puede citar una fuente verificable, no
   se cree. Externo es dato, no autoridad.

Y una advertencia de forma: un aporte externo bien redactado tiende a colarse en
el vocabulario interno sin pasar por la firma. Cuando el Soberano se descubre
usando un término que no recuerda haber canonizado, conviene buscar de dónde
vino.

---

## §8 · FLUJO DEL PUSH

Único momento en que algo sale de la máquina. Cuatro pasos, siempre:

1. **El Ejecutor no empuja.** Prepara y para.
2. **El Soberano revisa el diff completo de lo que va a subir**, no el árbol
   actual. Lo que ya está commiteado es lo que viaja.
3. **Los ganchos frenan.** Si frenan, se investiga; no se fuerza. Cada uso del
   escape se registra con motivo.
4. **`push` normal, nunca forzado.** Reescribir un remoto destruye lo que hubiera
   debajo sin preguntar, y en un sistema de solo anexión es una contradicción.
   Si hace falta, se registra con motivo como cualquier ruptura de invariante.

**Nota sobre lo ya publicado:** un dato que salió, salió. Reescribir el historial
no lo recupera; rompe referencias y da una falsa sensación de limpieza. La
corrección se hace hacia adelante, y la cicatriz queda como registro honesto.

---

## CHANGELOG

**v1.0.0 (2026-08-09)** · Creación. Fusiona los documentos de equipo y flujos,
que se solapaban en dos tercios. Cada regla se deriva de un fallo documentado en
las ocho rondas de reconciliación, no de una buena práctica genérica.
