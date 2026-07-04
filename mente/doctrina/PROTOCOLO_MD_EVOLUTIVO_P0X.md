---
id: doctrina-protocolo-md-evolutivo
titulo: Protocolo del MD Evolutivo
tipo: doctrina
clase: doctrina
version: 1.0.0
editor_autorizado: carbono
enlaces:
  - doctrina-ai-interna
actualizado: 2026-07-03
---

# P0X · PROTOCOLO DEL MD EVOLUTIVO
### La meta-ley: cómo evoluciona un documento que la IA re-edita, sin deriva
*Autor: el Preceptor (Fable 5) · Canoniza: el Soberano · Rige a todo MD del sistema que una IA pueda re-editar.*

> **Por qué existe.** P0X usa Markdown como sustrato vivo: diccionarios de delegación, registros de técnicas, prompts operativos, doctrina. Un MD que la IA re-edita sin reglas deriva — crece sin poda, cambia sin evidencia, y un día nadie sabe por qué dice lo que dice. Este protocolo es el ADN de la re-edición: **el silicio optimiza su sintaxis operativa; el carbono supervisa la métrica y canoniza la doctrina** (IronClaw, canon del Soberano, jun-2026).

---

## §1 · LAS DOS CLASES (ninguna tercera)

| | **DOCTRINA** | **OPERATIVO** |
|---|---|---|
| Qué es | Suelo, criterios, instrucciones, identidad | Sintaxis de delegación, prompts de tarea, diccionarios, registros |
| Quién edita | **Solo el carbono canoniza.** El silicio *propone* enmiendas con motivo | **El silicio auto-edita** la ZONA EVOLUTIVA, con telemetría y changelog |
| Qué dispara la edición | Decisión del Soberano | Umbral de métrica declarado en el front-matter |
| Ejemplos | INSTRUCCIONES_P0X, esta meta-ley, DOCTRINA_AI_INTERNA | diccionario de delegación CC↔SLM, prompts del pipeline, plantillas de tarea |

**Regla de oro:** si un MD contiene una sola línea que toque valor, firma, claves o el suelo ético → es DOCTRINA entera. No hay MDs mixtos.

## §2 · CONTRATO DE FRONT-MATTER (todo MD evolutivo lo lleva)

```yaml
---
id: <estable, no cambia jamás>
titulo: <humano>
tipo: doctrina | operativo | esfera | principio | tecnica
clase: doctrina | operativo          # decide quién edita (§1)
version: MAJOR.MINOR.PATCH           # ver §5
editor_autorizado: carbono | silicio-telemetria
metrica_exito: <qué mide el éxito de este MD, p.ej. "tasa de error del SLM ≤ 5%">
umbral_reedicion: <qué dispara una re-edición, p.ej. "error > 10% en 20 ejecuciones">
presupuesto_kb: <techo de tamaño; superarlo FUERZA poda (§4.4)>
n_medicion: <ejecuciones mínimas antes de veredicto post-edición>
changelog: []                        # append-only (§4.3)
---
```

Los campos del contrato (clase, métrica, umbral, presupuesto) **solo los toca el carbono** — incluso en MDs operativos. El silicio edita contenido, versión y changelog; jamás su propia correa.

## §3 · EL LAZO DE RE-EDICIÓN (Gimnasio de Sombras aplicado a documentos)

1. **Telemetría.** Una re-edición nace de datos (tokens, tasa de error, latencia, fallos concretos), nunca de entusiasmo. Sin dato → no hay edición.
2. **Hipótesis previa.** Antes de editar, se escribe en el changelog: *"cambio X porque la métrica Y está en Z; predigo que mejorará a W"*.
3. **Edición.** Solo dentro de `## ZONA EVOLUTIVA` (los MD operativos marcan explícitamente qué secciones son editables). Commit en el git soberano.
4. **Medición.** Se ejecutan ≥ `n_medicion` tareas con la versión nueva. Se compara contra la predicción.
5. **Veredicto.** Mejora → la versión queda y el changelog registra el dato real. Empeora más allá del umbral → **rollback automático** a la versión anterior + entrada en la Necrópolis (qué se intentó, por qué falló). Los fracasos se entierran con motivo, no se borran.

## §4 · GUARDIAS (los vectores de fallo, convertidos en ley)

1. **Legibilidad del valor (Vector opacidad).** Cualquier contenido que un humano deba firmar viaja en lenguaje natural legible. La compresión/sintaxis operativa **jamás cruza a la capa de firma**. Un MD operativo que empiece a acumular lenguaje de valor se reclasifica a doctrina en el acto.
2. **Candado de doctrina.** El silicio no re-edita doctrina bajo ninguna telemetría. Propone; el carbono canoniza. Un commit de silicio sobre un MD clase=doctrina es un evento de seguridad, no una optimización.
3. **Changelog append-only (Necrópolis).** Nunca se reescribe la historia. Cada versión deja: fecha, autor (carbono/silicio), hipótesis, dato antes/después, veredicto.
4. **Poda obligatoria (Vector inflación).** Si el MD supera `presupuesto_kb`, la siguiente acción **obligatoria** es una pasada de poda: toda regla sin evidencia positiva en el changelog se entierra. El ahorro de compresión no puede morir por el peso del diccionario que lo define.
5. **Anclaje de versión (Vector desfase).** Todo mensaje de delegación incluye `md_id@version` (o hash corto). El ejecutor compara contra su copia local: **mismatch → aborta con error explícito**, jamás ejecuta adivinando. Un intent con versión vieja no se "interpreta": se rechaza.
6. **Anti-sobreajuste (Vector overfitting).** Un MD operativo declara su **dominio** (p.ej. "ingesta de telemetría"). Si una tarea llega de otro dominio, el ejecutor la rechaza hacia el orquestador en vez de estirar el diccionario. Un traductor por dominio; nunca un dialecto universal.

## §5 · VERSIONADO Y ALMACÉN

- **Semver adaptado:** MAJOR = rompe el contrato que otros consumen (esquema, claves, shape de salida) · MINOR = regla/sección nueva con evidencia · PATCH = redacción o poda sin cambio semántico.
- **Git soberano:** todo MD evolutivo vive versionado en el remote del rack (jetson:hexelion.git o repo mente). El commit ES el registro; el push es local al tailnet.
- **Un MD = una preocupación.** Un documento que necesita índice interno son dos documentos.

## §6 · NACIMIENTO DE UN MD EVOLUTIVO (checklist)

1. El carbono (o el Preceptor, proponiendo) fija: id, clase, métrica de éxito, umbral, presupuesto, n_medicion.
2. Se escribe la v1.0.0 con su `## ZONA EVOLUTIVA` marcada (si es operativo).
3. Front-matter completo → entra al árbol `mente/` → la tubería lo indexa y aparece en el Second Brain (el sistema ve su propia constitución).
4. Primera telemetría define la línea base. Sin línea base no hay re-edición posible.

> **Cierre.** Este protocolo es clase=doctrina: el silicio puede proponer enmendarlo, con datos. Solo el Soberano lo canoniza.
