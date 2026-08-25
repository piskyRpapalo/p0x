# BASE DE SUGERENCIAS DEL CEREBRO LOCAL · 2026-08-26

**Quién las escribió:** el 27B del nodo (`Qwen3.8-27B-Uncensored`, Vulkan,
`--reasoning off`), por `agentes/bucles/cerebro.py`. Cinco preguntas, 200 s de
pared en total, 4,2–4,3 tok/s de generación medidos.

**Qué son y qué NO son.** Son *propuestas*, no canon. El silicio propone; el
carbono firma. Ninguna se ha aplicado.

**Por qué por aquí y no por `cc-local`.** El arnés de Claude Code manda 67.071
tokens de preámbulo y en esta iGPU eso son ~17 minutos de lectura antes del
primer token, por llamada — medido el 2026-08-26, con una prueba mínima que
agotó 420 s. `cerebro.pensar` manda decenas de tokens y contesta en 40 s.
**La Regla de oro no cambia; la vía sí.**

## El curso y la terminal ficticia (F5)

- Define un whitelist estricto de comandos y argumentos permitidos en el JSON para evitar inyección de lógica no prevista o estados inconsistentes al ampliar los pasos.
- Valida la salida de la terminal ficticia contra un patrón regex o cadena exacta en lugar de comparar texto libre, garantizando que el usuario no pueda "hackear" el paso con entradas ambiguas.
- Sincroniza el estado de la memoria SQLite con el paso actual del curso antes de cada interacción para prevenir desincronizaciones si el usuario recarga la sesión o cambia de paso abruptamente.

## El traductor de la Frontera (F7)

- Validar que la inserción en la tabla de memoria final esté condicionada por un campo de estado explícito (p. ej., `status='approved'`) que solo el usuario puede modificar, impidiendo que el flujo de simplificación escriba directamente en la base de datos de conocimiento.
- Implementar una transacción atómica que mueva el borrador a la memoria solo tras la confirmación, garantizando que si el proceso falla o el usuario cierra la aplicación, el dato permanezca en el estado de borrador y no se pierda ni se promueva accidentalmente.
- Añadir una verificación en la capa de acceso a datos que rechace cualquier consulta de "memoria activa" que no filtre por el estado de consentimiento, asegurando que el modelo local nunca lea datos no aprobados como contexto de aprendizaje.

## El bucle nocturno de QA (F10/F13)

- Define un campo `reproduccion` que contenga la secuencia exacta de comandos ADB y capturas de pantalla para que el auditor pueda re-ejecutar el fallo sin contexto humano.
- Incluye un campo `hipotesis_causal` donde el rol esceptico registre por qué el fallo ocurrió (ej. "timeout de red" vs "bug de UI") para que el novato aprenda la distinción.
- Añade un campo `impacto_doctrinal` que mapee el hallazgo a un principio de diseño específico de PreceptorOS, permitiendo al auditor priorizar correcciones que violen la arquitectura local.

## La puerta de la v1.1 (F14)

- Verificar que el fichero SQLite se cierra y sincroniza correctamente tras cada sesión para garantizar la integridad de la memoria portable ante cortes de energía.
- Documentar explícitamente en el README las métricas de aprendizaje que el sistema no puede cuantificar, cumpliendo la promesa de transparencia sobre sus limitaciones.
- Ejecutar una prueba de migración de datos desde la versión 1.0 a la 1.1 para asegurar que la estructura de la base de datos no pierde información crítica al actualizar.

---

## Lo que se salió del carril, y por qué se anota igual

El bloque de «auditoría de sencillez» pedía un **criterio** y devolvió
**veredictos de arquitectura**, que es exactamente lo que el reparto de
cerebros (`CLAUDE.md`, `P0X_BRAIN=local`) le prohíbe: *«No emites veredictos de
arquitectura»*. Se anota entero porque un fallo de reparto medido vale más que
un fallo escondido — y porque una de las tres es además **imposible** en este
producto:

- ~~Corta el módulo de proyectos si no permite crear y consultar una entrada en menos de tres clics, priorizando la inmediatez del cuaderno.~~
- ~~Pospón la frontera de privacidad avanzada hasta que la captura de turnos demuestre retención de usuarios, ya que la confianza se gana con la utilidad básica.~~
- ~~Elimina la brújula de aprendizaje si no se integra directamente en la sugerencia de la siguiente acción del cuaderno, evitando la fragmentación de la interfaz.~~

La segunda propone *«posponer la frontera de privacidad hasta que la captura
demuestre retención de usuarios»*. Este producto **no tiene telemetría**: no
hay retención que medir, y no la habrá. El modelo razonó sobre un SaaS
genérico porque el prompt no le dijo que no lo era. **La culpa es del prompt,
no del modelo** — y queda escrito para el siguiente que le pregunte.

## Lo que aporta que yo no había planteado

Tres, y las tres son buenas:

1. **Rechazar en la capa de datos toda consulta de «memoria activa» que no
   filtre por consentimiento.** Una guardia estructural, no una convención.
2. **Prueba de migración 1.0 → 1.1** antes de etiquetar. Nadie la había pedido.
3. **Validar la terminal ficticia contra patrón exacto**, no contra texto
   libre, para que el paso no se pueda «aprobar» con una entrada ambigua.

