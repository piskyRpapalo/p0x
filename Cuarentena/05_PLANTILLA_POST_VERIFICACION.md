---
id: plantilla-post-verificacion
titulo: Plantilla del entregable POST_VERIFICACION
tipo: operativo
clase: operativo
version: 1.0.0
dominio: cuarentena-documental
presupuesto_kb: 10
actualizado: 2026-08-10
---

# PLANTILLA · POST_VERIFICACION

Se escribe en `LA CARPETA/POST_VERIFICACION_R<id>.md`.

**Núcleo fijo (siempre, las 9 secciones).** **Anexo (solo el que corresponda a la ronda).** Una ronda que rellena tres anexos es una ronda que hizo mal tres cosas en vez de bien una.

---

## NÚCLEO FIJO

```markdown
# POST_VERIFICACION · R<id>
Misión:
Fecha:
Dominio:
Estado: PROPUESTA / PENDIENTE_DE_FIRMA / FIRMADO / RECHAZADO
Firmante: Soberano

## 1 · RESUMEN
3-6 líneas. Qué se hizo · qué se propone · qué falta · qué decisión necesita el Soberano.

## 2 · HECHO
Qué se analizó. Qué NO se ejecutó (explícito).

## 3 · MEDIDO
Solo cifras y hechos verificables de ESTA sesión.
Cada línea con el comando de solo lectura o la ruta que la produjo.
Sin medición → NO_DATA. Sin adjetivos.

## 4 · CRÍTICO
Hallazgo grave, o "ninguno". Coherente con el resto del documento.

## 5 · BLOQUEADO
<item> ← <dependencia exacta>

## 6 · NO_DATA
Todo lo que no se pudo determinar. Nunca vacío sin declararlo.
"Ninguno" y vacío no son lo mismo.

## 7 · PARA CLAUDE CODE
Solo tareas acotadas, verificables y con dependencia clara. No una lista de deseos.
Por ítem: tarea · prioridad · riesgo · dependencia · prompt sugerido (autónomo y acotado).
Ningún prompt puede abrir un frente aparcado.

## 8 · DECISIÓN PARA EL SOBERANO
UNA pregunta. Si hay varias, o son una sola decisión compuesta, o sobran.

## 9 · CIERRE
- Destino propuesto del documento dentro de la documentación del proyecto.
  (Si la ruta no existe, se propone crearla como decisión — no se ejecuta.)
- Documentos útiles que no deben perderse, y su destino.
  Si su contenido esencial ya quedó dentro de este POST_VERIFICACION, se declara.
- Archivado o borrado de la carpeta temporal: por defecto **archivar**.
  El borrado exige la secuencia completa de `01_LEEME_PRIMERO.md §6`.
```

---

## ANEXOS (uno por ronda, el que toque)

### ANEXO A · Documental (R00)
Por cada fichero: ruta · tipo · tamaño o líneas · clasificación · motivo · acción propuesta.
Después: qué se conserva de los útiles (reglas, estructuras, criterios) y por qué se rebaja el resto.

### ANEXO B · Software residual (R01)
Matriz. Por ítem: componente · acción (`ELIMINAR`/`ARCHIVAR`/`REFACTORIZAR`/`CONSERVAR`) · justificación técnica · coste/beneficio · plan de reversión · evidencia. Sin evidencia suficiente → `NO_DATA`, y el ítem no se propone.

### ANEXO C · Fuentes de dato (R02)
Por fuente declarada: `existe` · `visible por la Aduana` · `esquema definido` · `última medición real` · `estado`.
Solo evidencia en disco. Si una fuente declarada no se resuelve, la ronda es **BLOQUEADA** y se dice.

### ANEXO D · Estructura Medallón (R03)
Árbol propuesto · esquemas mínimos por fuente · puntos de validación · reglas de paso entre capas. Rutas relativas a la raíz del proyecto.

### ANEXO E · Conexión y reparación (R04-R05)
Qué dato ya funciona y puede anclarse hoy · qué está roto y cuál es la causa verbatim · qué está `NO_DATA`. Un fallo se documenta con su error literal, nunca parafraseado.
