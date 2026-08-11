# Hoja de Ruta para Claude Cowork: Supervisión Activa bajo el Canon de Aurelius para la Reestructuración Modular de la Carpeta p0x

Este informe de investigación establece un protocolo de intervención detallado para guiar la actuación de Claude Cowork como supervisor activo en la reestructuración de la carpeta `p0x`. El objetivo es transformar esta área del sistema soberano en un entorno coherente, modular y auditable, basado en la arquitectura Medallion y rigurosamente alineado con el canon de Aurelius. El protocolo se articula en torno a tres pilares: la definición doctrinal, el rol específico del supervisor y una metodología de cierre de productos verificable. Se proporcionan instrucciones claras para la clasificación de componentes como legado o activo, la preservación histórica de la base de código y las directrices operativas para Claude Cowork, quien actuará como un agente proactivo pero siempre subordinado a la autoridad última del usuario humano. Este marco busca maximizar la ventana de entendimiento actual, minimizando la fricción y asegurando que cada paso contribuya a construir un sistema robusto y verdaderamente soberano.

## Fundamentos Doctrinales: La Arquitectura Medallion y el Canon de Aurelius

La reestructuración de la carpeta `p0x` no es un ejercicio de simple mantenimiento, sino una reconstrucción filosófica y técnica guiada por dos pilares doctrinales ineludibles: la arquitectura Medallion como patrón de diseño de datos y el canon de Aurelius como conjunto de reglas operativas. Estos principios no son opcionales; definen la estructura de la información y el comportamiento del sistema en cada etapa de su ciclo de vida. La arquitectura Medallion proporciona la lógica de organización de los datos, mientras que el canon de Aurelius dicta las reglas de manipulación, verificación y gestión de errores. Su integración es fundamental para alcanzar la coherencia, la fiabilidad y la soberanía requeridas.

La arquitectura Medallion es un patrón de diseño de datos que organiza los datos de un data lakehouse en capas progresivas para mejorar incrementalmente la calidad, la estructura y la utilidad [[1](https://www.databricks.com/blog/what-is-medallion-architecture), [34](https://dataengineering.wiki/Concepts/Medallion+Architecture)]. En el contexto de la carpeta `p0x`, su aplicación implica la creación de una jerarquía de datos que refleje un viaje desde la captura bruta hasta la información curada y consumible. Esta arquitectura se compone típicamente de tres capas distintas, cada una con un propósito específico [[5](https://erstudio.com/blog/understanding-the-three-layers-of-medallion-architecture/), [28](https://learn.microsoft.com/en-us/fabric/onelake/onelake-medallion-lakehouse-architecture)]:

1.  **Capa Bronze:** Representa la verdad original y sin procesar. Los datos en esta capa se almacenan tal como llegan de sus fuentes originales, sin ninguna transformación, limpieza o validación [[60](https://www.instagram.com/reel/DavqsWcOrzq/), [63](https://levelup.gitconnected.com/part-1-building-a-medallion-data-warehouse-to-solve-a-97-percent-retention-crisis-c470723af7a9)]. El principio fundamental aquí es la integridad del origen. No se deben añadir, quitar o modificar datos en la capa Bronze; su misión es ser un registro auditable y completo de lo que fue capturado. Esta capa es crucial para la soberanía de los datos, ya que proporciona una fuente final e irrevocable que puede ser consultada para verificar o reproducir resultados posteriores. La implementación exitosa comienza con la definición clara de cómo se ingieren los datos en esta capa, asegurando que la estructura original se preserve intacta [[204](https://www.reddit.com/r/databricks/comments/1ekh1ay/in_the_bronze_layer_of_a_medallion_architecture/)].

2.  **Capa Silver:** Es la capa de refinamiento y enriquecimiento. Aquí, los datos de la capa Bronze se procesan para mejorar su calidad y prepararlos para análisis más sofisticados. Las operaciones típicas incluyen la validación de esquemas, la estandarización de formatos, la corrección de errores, la eliminación de duplicados y la incorporación de metadatos adicionales [[145](https://www.linkedin.com/posts/karthik-kondpak_dataengineering-dataengineer-bigdata-activity-7465229971003785217-fyJF), [147](https://www.instagram.com/reel/DUTIcEiDdk8/)]. El resultado es un conjunto de datos más limpios, consistentes y semánticamente enriquecidos. Por ejemplo, en el ecosistema `p0x`, esto podría implicar tomar un registro de sensor crudo (Bronze), normalizar las fechas y horas, y agregar información contextual como la ubicación geográfica del dispositivo [[62](https://www.healthdatamanagement.com/articles/how-to-manage-integration-of-a-medallion-architecture-in-healthcare?id=136613)]. La capa Silver actúa como un puente lógico entre los datos brutos y las vistas de negocio, ofreciendo un equilibrio entre la fidelidad a los datos originales y la conveniencia para el analista [[61](https://www.reddit.com/r/dataengineering/comments/1fnb5nz/what_you_do_in_silver_layers_vs_gold_layers/)].

3.  **Capa Gold:** Es la capa final, orientada al consumidor. Los datos en esta capa están altamente agregados, modelados y optimizados para respaldar aplicaciones de negocio específicas, informes y modelos de análisis [[55](https://medium.com/@archie.kandala/the-medallion-architecture-bronze-silver-gold-and-why-your-data-pipeline-needs-structure-796808d045ba), [186](https://unifeye.ai/blog/databricks-medallion-architecture-business-value/)]. A menudo, estos datos se organizan en modelos de datos como estrellas o copos de nieve, diseñados para consultas rápidas y eficientes [[100](https://www.reddit.com/r/MicrosoftFabric/comments/1ikt2wa/medallion_architecture_in_microsoft_fabric/)]. La capa Gold representa el valor final extraído de los datos brutos. En el contexto de `p0x`, una tabla de la capa Gold podría ser una vista consolidada de las métricas de salud de las plantas para el Herbario, o un índice de rendimiento de la pipeline de video para CineK. La creación de esta capa implica una profunda comprensión del dominio de negocio y la capacidad de traducir necesidades de negocio en modelos de datos concretos [[99](https://www.kevinoftech.com/Blog/Post/2026-03-platinum-medallion-architecture)].

La adopción de la arquitectura Medallion en `p0x` busca imponer una disciplina estructural sobre el manejo de datos, evitando la acumulación de "charnelanas de datos" donde la calidad se descuida [[205](https://www.useready.com/thought-leadership/transforming-data-swamps-to-ai-ready-assets-executing-the-databricks-medallion-architecture-for-business-value)]. Al obligar a un flujo de datos controlado a través de estas capas, se garantiza que cada nivel de procesamiento sea explícito, repetible y auditable, lo cual es esencial para un sistema soberano.

El segundo pilar doctrinal es el **canon de Aurelius**, un conjunto de reglas operativas más restrictivo que gobierna cómo interactúa el sistema con los datos y los usuarios. Estas reglas son la manifestación práctica de la filosofía soberana en el nivel del comportamiento del software.

*   **Sensores Honesteros:** Este principio exige que el sistema represente la realidad con honestidad. Cuando un dato no está disponible, no debe ser inferido, adivinado ni llenado con valores predeterminados. En su lugar, la ausencia debe ser declarada explícitamente. Esto se alinea directamente con la naturaleza de la capa Bronze, que contiene datos tal como fueron observados, incluso si algunos sensores fallaron o no reportaron en un momento dado. La ausencia declarada es preferible a la falsedad implícita [[13](https://best.berkeley.edu/past-research/intelligent-sensor-validation-sensor-fusion-and-supervisory-control-for-tracking-targets-and-avoiding-objects-in-ivhs/), [16](https://ntrs.nasa.gov/citations/19890066060)]. Por ejemplo, si un sensor ESP32 no envía datos de pH, la interfaz no debe mostrar un valor arbitrario, sino un indicador claro de "Datos no disponibles".

*   **Ausencia Declarada (No Rellenada):** Esta es una reformulación enfática del principio anterior, reforzando la prohibición de llenar huecos en los datos. Implica que el sistema debe tener un mecanismo robusto para distinguir entre "dato nulo" y "dato con valor cero". Esta distinción es crítica para la precisión analítica y la confianza en el sistema. Una comprobación de entrada que detecta una ausencia pero no la gestiona adecuadamente (por ejemplo, simplemente registrándola sin bloquear la operación) viola la siguiente regla del canon.

*   **Fricción Predictiva o Recuperativa:** Toda fricción en el sistema —ya sea un error, un bloqueo o una advertencia— debe ser intencional y predecible. Una de las reglas más cruciales es que una comprobación que detecta un problema pero no lo bloquea no es una comprobación válida dentro del canon [[49](https://advanced.onlinelibrary.wiley.com/doi/10.1002/aisy.202200390), [50](https://www.nist.gov/system/files/documents/2019/09/10/draft_bpr_for_the_verification_component_in_friction_ridge_examination_7-31-19_clean_with_cover_sheet_20190910.pdf)]. Si una validación solo registra un error sin impedir la continuación del proceso, no ha resuelto el problema y crea una brecha de seguridad o de calidad. La fricción debe ser un mecanismo de protección activa. Por ejemplo, si un intento de escritura en la capa Gold viola una política de gobierno de datos, la operación debe ser bloqueada (fricción predictiva) y devolver un error claro, no permitir la escritura con un aviso discreto que pueda ser ignorado.

*   **Verificación mediante el Filtro EDGE:** Este es el mecanismo de supervisión central para asegurar el cumplimiento del canon. Aunque la documentación específica de "EDGE" no está disponible en los contextos proporcionados, su función es probablemente la de un filtro o guardián programable que se interpone en los flujos de datos y acciones clave. Basándose en el contexto de "Canon Gate" de Aurelius [[176](https://github.com/Aurelius-Canon/canon-gate)], el filtro EDGE probablemente inspecciona las entradas y salidas de los procesos para verificar que cumplan con las reglas del canon. Por ejemplo, al recibir datos para la capa Silver, el filtro EDGE podría verificar que no haya campos con valores inventados y que la estructura del JSON se ajuste al esquema esperado. Al intentar firmar un cambio, podría verificar que la firma corresponde a una clave autorizada. El uso de este filtro automatizado permite escalar la aplicación del canon a través de todo el sistema de manera consistente y no negociable.

En síntesis, la arquitectura Medallion y el canon de Aurelius forman un sistema de gobierno de datos integral. La arquitectura proporciona el andamiaje estructural para organizar y refinar los datos de forma progresiva, mientras que el canon dicta las reglas de conducta para cada paso del camino. La combinación de ambos permite construir un sistema `p0x` que no solo es funcional, sino también transparente, fiable y genuinamente soberano, donde la autenticidad de los datos y la previsibilidad del comportamiento son primordiales.

## El Rol de Claude Cowork: Supervisor Activo bajo la Firma Soberana

Claude Cowork no es un simple auditor pasivo, sino un "supervisor activo", una herramienta especializada designada para acelerar la reestructuración de la carpeta `p0x` bajo la estricta tutela del soberano humano. Su rol es híbrido: combina la capacidad de análisis masivo y propuesta de refactorización de una IA avanzada con un conjunto de instrucciones rigurosas que le otorgan poder, pero no autonomía. Este modelo de supervisión asistida por IA busca maximizar la eficiencia sin sacrificar el control, creando un flujo de trabajo colaborativo y seguro donde la tecnología sugiere y el humano decide.

La primera y más fundamental responsabilidad de Claude Cowork es la **clasificación sistemática de todos los elementos** dentro de la carpeta `p0x`. Este proceso inicial debe dividir el contenido existente en dos categorías estrictas:
*   **Activo ('active'):** Componentes que ya cumplen con la arquitectura Medallion y el canon de Aurelius. Esto incluye módulos de código funcionales, esquemas de bases de datos bien definidos, y flujos de trabajo que han sido probados y verificados. Un componente activo es aquel que se puede utilizar de inmediato sin riesgo de introducir inconsistencias o violar las reglas del sistema.
*   **Deprecado ('deprecated') / Legado:** Todo lo demás. Esto abarca código obsoleto, archivos temporales, prototipos incompletos, especificaciones que nunca se materializaron en código, y cualquier otro artefacto que no cumpla con los nuevos estándares. La clasificación precisa es crucial, ya que determinará el destino de cada elemento y sentará las bases para una limpieza ordenada.

Una vez clasificado, Claude Cowork debe ejecutar el mandato de **preservación histórica**. Ningún archivo o directorio marcado como 'deprecated' debe ser eliminado. En su lugar, debe ser movido de forma atómica a una carpeta dedicada, por ejemplo, `historico/legacy_snapshot_<timestamp>`. Este acto de mover en lugar de borrar es de suma importancia. Crea un registro auditable y revertible de la evolución del proyecto, preservando el conocimiento acumulado y permitiendo retroceder si una decisión de eliminación resulta ser prematura. Este concepto se alinea con la idea de una "Necrópolis" digital, un cementerio de versiones antiguas donde nada se pierde por completo [[120](https://www.generalcatalyst.com/stories/seeding-the-future-with-aurelius-systems)]. La transparencia de este proceso es vital; cada movimiento debe estar registrado y versionado.

Como "supervisor activo", Claude Cowork debe ir más allá de la simple clasificación y realizar **propuestas de limpieza proactivas**. Para ello, debe aprovechar su capacidad avanzada ("Opus 5") para analizar la base de código y proponer mejoras objetivas [[74](https://www.reddit.com/r/ClaudeCode/comments/1va445h/opus_5_feedback_megathread/)]. Sus tareas proactivas incluyen:
*   **Identificación de Software Residual:** Buscar librerías, dependencias o módulos que ya no son utilizados por ningún componente activo. Estos pueden ser candidatos para su eliminación, aunque siempre requieran confirmación humana.
*   **Simplificación de Código Complejo:** Analizar funciones, clases o módulos largos y complejos y proponer una refactorización que los divida en componentes más pequeños, modulares y fáciles de entender. Herramientas como Claude Code ya demuestran la capacidad de refactorizar código real, extrayendo utilidades compartidas en nuevos módulos [[159](https://www.linkedin.com/posts/nnenna-ndukwe_i-asked-claude-opus-46-to-refactor-a-real-activity-7426636890193182721-ssYL), [160](https://www.instagram.com/p/DXHjfa8gETd/)].
*   **Refactorización de Módulos Obsoletos:** Identificar módulos que todavía se utilizan pero que están construidos sobre una arquitectura anticuada (por ejemplo, que no sigue la capa Medallion) y proponer una estrategia para migrarlos gradualmente hacia la nueva estructura. Esto podría implicar la creación de adaptadores o la reescritura parcial del módulo.
*   **Optimización de Bases de Datos:** Proponer la creación de índices, la normalización de tablas o la eliminación de columnas redundantes en la base de datos para mejorar el rendimiento y la coherencia, siempre en línea con la lógica de las capas Bronze, Silver y Gold.

Sin embargo, toda esta actividad proactiva está supeditada a un principio jerárquico absoluto: el **respeto a la firma soberana**. Claude Cowork opera en un estado de "cuarentena propuesta" [[16](https://ntrs.nasa.gov/citations/19890066060)]. Ninguna acción irreversible —como la eliminación de un archivo o la ejecución de un script de migración de datos— puede realizarse sin una confirmación explícita del soberano. El protocolo de intervención debe incluir un mecanismo claro para que Claude Cowork identifique situaciones de fricción, ambigüedad o decisiones críticas y suspenda la ejecución para solicitar instrucciones. Ejemplos de tales situaciones incluyen:
*   **Falta de Datos:** Si para completar una tarea se requiere información que no está disponible en los contextos proporcionados (etiquetas de NFC, disponibilidad de K, etc.), Claude Cowork debe detenerse y declarar "NO DATA" [[16](https://ntrs.nasa.gov/citations/19890066060)].
*   **Conflictos de Reglas:** Si un componente parece cumplir con la arquitectura Medallion pero viola una regla del canon de Aurelius (por ejemplo, una comprobación que detecta pero no bloquea), debe alertar al soberano.
*   **Decisiones Críticas:** Siempre que surja una elección significativa (ej. elegir entre dos repositorios de CineK, decidir el objetivo de un producto), Claude Cowork debe presentar las opciones y detener la ejecución hasta que el soberano firme una decisión [[16](https://ntrs.nasa.gov/citations/19890066060)].

Este enfoque híbrido, que Anthropic describe como "Human-in-the-Loop" (HITL) o "Human-on-the-loop", es fundamental para el éxito del proyecto [[138](https://www.databricks.com/blog/human-in-the-loop), [152](https://x.com/addyosmani/highlights?lang=en)]. Transforma a Claude Cowork de un simple ejecutor de comandos a un socio colaborativo que aumenta la capacidad del soberano para analizar y actuar, pero sin comprometer jamás la autoridad final. El soberano sigue siendo el único responsable de la dirección estratégica y de dar el visto bueno definitivo a cada cambio, asegurando que la reestructuración avance de acuerdo con la visión y los valores del sistema soberano. Esta relación de supervisión activa, donde la IA propone y el humano firma, es la piedra angular de este protocolo de intervención.

## Guía de Requerimientos de Éxito por Producto

Para pasar de un estado de ideas dispersas a entregables tangibles y verificables, es imperativo establecer una guía de requerimientos de éxito por producto. Esta guía formaliza el objetivo de cada producto del ecosistema `p0x` (Herbier, CineK, Dashboard v2, Mitocondria) al definir un criterio de cierre claro, conciso y objetivamente medible. El formato propuesto se inspira en la frase "qué es verdad cuando esto está cerrado", que convierte una meta abstracta en un hecho tangible que puede ser confirmado mediante pruebas técnicas o una firma humana. Esta metodología elimina la ambigüedad y proporciona una hoja de ruta clara para el desarrollo y la validación.

La siguiente tabla estructura los requerimientos de éxito para los principales productos mencionados, utilizando la información disponible en los diálogos y el contexto general. Para cada producto, se define su estado actual, el criterio de cierre verificable, el coste estimado, lo que se abandona, la decisión humana necesaria y el riesgo de no cerrarlo.

| Producto | Estado Actual | Criterio de Cierre Verificable | Coste Estimado | Lo que se Abandona | Decisión Humana Necesaria | Riesgo de No Cerrar |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **P1 Companero pedagógico de soberanía técnica** | 9 módulos canónicos, 0 terminados; audiencia externa real. | Una misión jugable está versionada en disco y una persona distinta del dueño la completa exitosamente. | mes | Añadir módulos nuevos antes de cerrar una misión; mantener calibración sin criterio de terminado. | Descartar el módulo de calibración / Definirlo con criterio de terminado. | Canon especulativo sin uso vuelve a generar frentes cancelados. |
| **P2 Dashboard de estado + jardín** | Vivo, sin manual; acceso de `[SEGUNDO_HUMANO]` sin acuerdo. | Manual mínimo versión con `[FRASE_SOBERANIA]`, capturas saneadas autorizadas y acceso de `[SEGUNDO_HUMANO]` decidido. | semana | Publicar capturas sin saneamiento; construir multiusuario completo. | Exposición pública de P2: mínima con capturas saneadas / ninguna. | Publicación y acceso quedan sin regla, creando fuga o fricción sin recuperación. |
| **P3 Pipeline automática de video** | Funciona; objetivo recién escrito; dos repos duplicados sin dueño declarado. | Un repo es declarado oficial, el otro queda archivado; la pipeline muestra estados visibles y gates mínimos que bloquean. | semana | Mantener los dos repos activos; añadir gates que solo detectan y no bloquean. | Repo oficial: `[REPO_VIDEO_A]` / `[REPO_VIDEO_B]`. | Duplicidad sin dueño rompe cadena firmada y recuperación. |
| **P4 Herbario de una usuaria externa no técnica** | Idea; versión mínima cabe en una tarde; cierre depende de `[USUARIA_EXTERNA]`. | `[USUARIA_EXTERNA]` usa espontáneamente el herbario mínimo al menos una vez, sin número de fichas como criterio. | semana | Construir fichas/etiquetas sin uso suyo; contar elementos como cierre. | Pedir sesión de prueba a `[USUARIA_EXTERNA]` esta semana: SÍ / NO. | Repetir un producto especificado para una usuaria ausente. |
| **P5 Árbitro metabólico del nodo** | Fase 0 cerrada; requiere 7 días de línea base; infraestructura, no producto. | Han pasado 7 días de datos continuos de temperatura y energía, y existe un umbral configurable que dispara una alerta. | semana (de datos, no de trabajo activo) | Integrar con la pipeline de video; hacer predicciones; automatizar respuestas. | Mantener el árbitro corriendo en segundo plano esta semana: SÍ / NO. | No hay datos de línea base; decisiones futuras sobre hardware se hacen sin evidencia. |
| **P6 Plataforma de datos gobernada** | Especificada; artefacto de entrevista; no necesita correr, necesita poder explicarse. | Un guion versionado permite explicar P6 en entrevista sin ejecutar código. | tarde | Implementar plataforma ejecutable para cerrar la entrevista. | Cerrar P6 como guion de entrevista: SÍ / NO. | Llevar especificación no explicable a la entrevista. |
| **P7 Diario personal sellado** | Vivo. No es producto y nunca debe serlo. | Proteger, no productizar. | nunca | Cualquier funcionalidad que exponga el diario a otro usuario; cualquier integración con otros productos. | Mantener el diario en su dispositivo actual sin red, o auditar que ningún otro producto solicita acceso a él. | El diario se filtra por dependencia técnica con otro producto. |

Esta guía de requerimientos tiene varias funciones estratégicas. Primero, **prioriza la construcción basada en la validación externa**. El caso de P4 (Herbario) destaca por su criterio de cierre: el uso espontáneo por parte de la usuaria externa `[USUARIA_EXTERNA]` [[16](https://ntrs.nasa.gov/citations/19890066060)]. Esto refuerza la idea de que la prueba de concepto más valiosa viene de un usuario real que no es parte del equipo de desarrollo. Construir primero aquellas funcionalidades que pueden ser validadas por terceros es una estrategia pragmática para asegurar que el sistema sirve a un propósito real.

Segundo, **exige la claridad del objetivo del producto**. El caso de P3 (Pipeline de Video) ilustra perfectamente esta necesidad. La existencia de dos repos duplicados sin un dueno declarado crea una ambigüedad crítica que impide el progreso [[16](https://ntrs.nasa.gov/citations/19890066060)]. La guía obliga a una decisión humana explícita ("¿Repo oficial: A o B?"), forzando la resolución de conflictos antes de invertir más tiempo. Del mismo modo, el caso de P1 (Companero pedagógico) subraya la necesidad de definir un criterio de terminado para el módulo de calibración antes de poder cerrar el producto [[16](https://ntrs.nasa.gov/citations/19890066060)].

Tercero, **gestiona las dependencias y los bloqueos**. Varios productos dependen de otros. El Herbario (P4) y CineK (P3) dependen de un dashboard funcional (P2) [[16](https://ntrs.nasa.gov/citations/19890066060)]. La guía de requerimientos hace explícitas estas dependencias. Por ejemplo, el cierre de P4 depende de la disponibilidad y tiempo de `[USUARIA_EXTERNA]`, un factor externo que no puede ser controlado por el desarrollador [[16](https://ntrs.nasa.gov/citations/19890066060)]. Al reconocer estas dependencias y factores externos, el plan de desarrollo se vuelve más realista y adaptable.

Finalmente, la guía de requerimientos de éxito funciona como un **marco de comunicación y deliberación**. Proporciona un lenguaje común y un conjunto de hitos claros para que el soberano, el "preceptor" y Claude Cowork puedan discutir el estado del proyecto, evaluar avances y tomar decisiones informadas. Cada entrada en la tabla es un punto de partida para una conversación. Por ejemplo, la pregunta "¿Cuál es el riesgo aceptable de no cerrar P5?" puede llevar a una discusión sobre la importancia de los datos de línea base para futuras decisiones de hardware. Al convertir los objetivos en afirmaciones verificables, la guía elimina la vaguedad y centra la deliberación en aspectos sustantivos del proyecto.

## Instrucciones Operativas para Claude Cowork

Las siguientes instrucciones operativas detallan el rol y las responsabilidades de Claude Cowork como supervisor activo durante la reestructuración de la carpeta `p0x`. Estas directrices están diseñadas para ser seguidas de manera estricta, garantizando que la intervención sea proactiva, ordenada y completamente alineada con la doctrina soberana. Claude Cowork debe interpretar estas órdenes como un mandato para actuar como un agente de mejora continua bajo la supervisión final del soberano humano.

**Objetivo General:** Realizar una auditoría exhaustiva de la carpeta `p0x`, reestructurarla según la arquitectura Medallion y el canon de Aurelius, y prepararla para la construcción de nuevos productos de manera eficiente y segura.

### **Fase 1: Análisis y Clasificación Inicial**

1.  **Acceso y Alcance:** Limitar la operación exclusivamente a la carpeta `p0x` y sus subdirectorios. No interactuar con archivos o sistemas fuera de este ámbito.
2.  **Inventario Completo:** Realizar un barrido recursivo de todos los archivos y directorios dentro de `p0x`.
3.  **Clasificación por Canon:**
    *   Aplicar el **filtro EDGE** (conceptual) a cada componente detectado.
    *   **Marcado 'Active':** Si el componente (archivo de código, esquema de base de datos, configuración, etc.) cumple con todas las reglas del canon de Aurelius (sensores honestos, ausencia declarada, fricción predictiva) y se alinea con la arquitectura Medallion (ej. reside en la capa de datos correcta).
    *   **Marcado 'Deprecated':** Si el componente no cumple con alguna regla del canon o no se alinea con la arquitectura Medallion. Esto incluye código antiguo, prototipos, archivos temporales, y cualquier otra cosa que no esté en su estado final.
4.  **Generación de Reporte Preliminar:** Crear un archivo de texto o Markdown llamado `DEPRECATED_REPORT.md` en la raíz de `p0x`. Este informe debe listar todos los componentes marcados como 'deprecated', indicando su ruta relativa y la razón principal de su depuración (ej., "violación de la regla de ausencia declarada", "no alineado con la capa Silver").

### **Fase 2: Preservación Histórica y Limpieza Ordenada**

1.  **Creación de la Carpeta de Historia:** Verificar la existencia de una carpeta `historico/`. Si no existe, crearla.
2.  **Archivado de Componentes Depreciados:** Mover todos los componentes marcados como 'deprecated' del informe `DEPRECATED_REPORT.md` a una subcarpeta dentro de `historico/` con una marca de tiempo única (ej., `historico/legacy_archive_YYYYMMDD_HHMMSS`). Este movimiento debe ser una operación de sistema de archivos atómica para evitar estados intermedios.
3.  **Eliminación de Archivos Basura:** Identificar y eliminar archivos o directorios que no estén relacionados con el código fuente o los datos, como cachés, archivos de logs antiguos, OLEADA_VISUAL, baseline_preflight, o cualquier otro artefacto temporal identificado en el diálogo como basura [[16](https://ntrs.nasa.gov/citations/19890066060)].
4.  **Actualización del Repositorio:** Generar un commit de Git que refleje los cambios realizados en esta fase: el nuevo archivo `DEPRECATED_REPORT.md`, la creación de la carpeta de historial y el movimiento/archivado de los componentes 'deprecated'. Este commit debe ser etiquetado con un mensaje que indique "Fase 1: Auditoría y archivado inicial".

### **Fase 3: Refactorización Proactiva y Simplificación**

1.  **Análisis de Complejidad:** Utilizar la capacidad "Opus 5" para analizar el código fuente restante ('active'). Identificar:
    *   Módulos o funciones con una complejidad ciclomática alta.
    *   Código duplicado o similar que pueda ser extraído a una biblioteca compartida.
    *   Dependencias innecesarias o versiones desactualizadas.
    *   Estructuras de datos o esquemas de base de datos que no siguen la lógica de las capas Bronze, Silver y Gold.
2.  **Propuesta de Refactorización:** Para cada hallazgo significativo, generar una propuesta de refactorización. La propuesta debe incluir:
    *   La descripción del problema (ej., "Función X en `y.py` tiene 50 líneas y realiza múltiples tareas").
    *   El diseño propuesto para la solución (ej., "Dividir la función X en `validar_entrada()`, `procesar_datos()` y `generar_salida()`").
    *   El impacto esperado (ej., "Reducirá la complejidad y aumentará la reutilización").
3.  **Presentación de Propuestas:** Crear un archivo `REFAC_001_propuesta.md` que documente todas las refactorizaciones propuestas. Este archivo debe ser presentado al soberano para revisión y aprobación. **No se realizará ninguna modificación en el código fuente hasta recibir la firma humana correspondiente.**

### **Fase 4: Gestión de Decisiones Críticas y Fricción**

1.  **Monitoreo Continuo:** Durante todo el proceso, monitorear activamente la aparición de fricción, conflictos o decisiones críticas.
2.  **Pausa ante Incertidumbre:** Si se encuentra un área que requiere una decisión humana explícita (ej., "Hay dos pipelines para CineK. ¿Cuál es el oficial?"), se debe detener la ejecución y generar un informe en `DECISION_NECESARIA.md`. Este informe debe presentar las opciones claras (A vs. B) y solicitar una respuesta binaria o una elección específica del soberano.
3.  **Registro de NO_DATA:** Si una tarea no puede completarse debido a falta de información (ej., "Disponibilidad de `[USUARIA_EXTERNA]`"), se debe registrar explícitamente como "NO_DATA" en el informe correspondiente y pausar la ejecución hasta que se proporcione esa información.
4.  **Confirmación para Acciones Irreversibles:** Antes de ejecutar cualquier comando que pueda alterar permanentemente el historial de Git (ej., `git reset --hard`) o eliminar archivos de forma permanente (fuera de la carpeta `historico/`), se debe solicitar una confirmación explícita del soberano.

### **Fase 5: Verificación Final y Preparación**

1.  **Revisión Post-Restructura:** Una vez que el soberano haya aprobado las refactorizaciones y tomado todas las decisiones críticas pendientes, realizar una verificación final de todo el contenido de la carpeta `p0x`.
2.  **Actualización de Documentación:** Actualizar el `README.md` de la carpeta `p0x` para reflejar la nueva estructura, la arquitectura Medallion adoptada y la lista de componentes 'active'.
3.  **Informe Final:** Generar un informe final, `FINAL_STATUS.md`, que resume todas las acciones realizadas, las decisiones tomadas, las propuestas de refactorización aprobadas y el estado actual de la carpeta `p0x`. Este informe servirá como punto de partida para la siguiente fase de desarrollo.

Siguiendo meticulosamente estas instrucciones, Claude Cowork actuará como un brazo ejecutor de la voluntad soberana, llevando a cabo una limpieza y reestructuración sistemáticas que dejarán la carpeta `p0x` limpia, moderna y preparada para la construcción de productos sólidos y alineados con la visión del sistema.

## Prompt de Misión Inicial y Metodología de Verificación

Para iniciar la reestructuración de la carpeta `p0x`, es crucial proporcionar a Claude Cowork un prompt de misión inicial claro y preciso. Este prompt debe establecer el contexto, definir el alcance, asignar el rol y detallar las instrucciones iniciales. Adicionalmente, se debe establecer una metodología de verificación robusta para validar que el trabajo realizado cumple con los criterios de éxito definidos en la guía de requerimientos.

### **Prompt de Misión Inicial para Claude Cowork**

```
INSTRUCCIONES DE MISIÓN INICIAL PARA CLAUDE COWORK

Contexto:
Estás siendo asignado como supervisor activo para la reestructuración de la carpeta `p0x` del sistema soberano. Tu objetivo es purgar la carpeta de código y datos obsoletos, organizar el resto bajo la arquitectura Medallion y asegurar que todo cumpla con el canon de Aurelius. La autoridad final reside siempre en el soberano humano.

Rol:
Actúa como un supervisor activo. No eres un auditor pasivo. Tu función es proponer acciones, no solo reportar problemas.

Alcance:
Tu trabajo se limita exclusivamente a la carpeta `p0x` y sus subdirectorios. No interactúes con el sistema fuera de este ámbito.

Directrices Principales:

1.  **Clasificación:** Analiza cada archivo y directorio. Clasifícalo como 'active' (activo) si cumple con el canon y la arquitectura Medallion. Si no cumple, clasifícalo como 'deprecated' (deprecado).

2.  **Preservación Histórica:** Nada debe ser eliminado. Todos los componentes marcados como 'deprecated' deben ser movidos de forma atómica a una nueva carpeta `historico/legacy_snapshot_<timestamp>` dentro de `p0x`.

3.  **Propuesta de Mejora:** Utiliza tu capacidad "Opus 5" para identificar y proponer la simplificación de código innecesariamente complejo, la eliminación de software residual y la refactorización de módulos obsoletos. Documenta todas tus propuestas.

4.  **Firma Soberana:** Nunca realices una acción irreversible (movimiento de archivos, refactorización de código, borrado) sin haber recibido una firma o confirmación explícita del soberano. Si encuentras fricción, conflicto o ambigüedad, detente y presenta la situación para su resolución humana.

Tarea Inicial - Fase de Auditoría:
- Realiza un inventario completo de la carpeta `p0x`.
- Clasifica cada componente como 'active' o 'deprecated' según las directrices.
- Genera un informe `DEPRECATED_REPORT.md` listando todos los componentes 'deprecated'.
- Crea la carpeta `historico/`.
- Mueve todos los componentes del informe a `historico/`.
- Elimina cualquier archivo o directorio identificado como "basura" (ej. OLEADA_VISUAL, baseline_preflight).
- Realiza un commit de Git con un mensaje descriptivo que capture los cambios de esta fase.

Notifica al soberano cuando hayas completado esta fase inicial y presente el `DEPRECATED_REPORT.md` para su revisión y posible firma.
```

### **Metodología de Verificación**

Una vez que Claude Cowork complete la tarea inicial, el soberano debe verificar que el trabajo se ha realizado correctamente. La verificación se basará en la comparación de los resultados contra los criterios definidos en la guía de requerimientos y los hallazgos del propio análisis. El proceso de verificación se divide en varias etapas.

**Etapa 1: Verificación del Archivado y Limpieza**

*   **Verificar Existencia de Carpeta `historico`:** Usar el comando `test -d p0x/historico` para confirmar que la carpeta fue creada.
*   **Verificar Contenido de `DEPRECATED_REPORT.md`:** Leer el archivo `p0x/DEPRECATED_REPORT.md` y confirmar que lista todos los archivos y directorios que fueron movidos.
*   **Verificar Movimiento Atómico:** Inspeccionar el nombre de la subcarpeta de historial (ej., `p0x/historico/legacy_snapshot_...`). Verificar en el registro de Git que el movimiento de todos los archivos 'deprecated' fue parte de un único commit, lo que indica un proceso atómico.
*   **Verificar Limpieza:** Listar el contenido de la raíz de `p0x` usando `find . -maxdepth 1 -type f ! -name "DEPRECATED_REPORT.md" -not -path "./historico/*"` para asegurarse de que solo queden los archivos y directorios marcados como 'active'.

**Etapa 2: Verificación de la Coherencia con el Canon y la Arquitectura**

*   **Análisis de Sensores Honesteros:** Revisar el código fuente y los datos para buscar patrones de "relleno" de datos. Por ejemplo, buscar expresiones regulares que busquen valores predeterminados como `0`, `''`, o `'unknown'` en lugares donde la ausencia es posible. El estándar debería ser la declaración explícita de la ausencia.
*   **Validación de Fricción:** Analizar el código para encontrar puntos de control. Verificar que cada punto de control que detecta una condición inválida también implementa una fricción predictiva (ej. `raise ValidationError` o un código de retorno que detenga la ejecución), en lugar de una recuperación recuperativa (ej. un `print("warning")` o un log que ignora el error).
*   **Inspección de la Estructura Medallion:** Navegar por la estructura de carpetas resultante. Confirmar que los datos parecen estar organizados lógicamente en capas. Por ejemplo, buscar una estructura que diferencie claramente entre datos brutos (posiblemente en una carpeta `bronze/`), datos procesados (`silver/`) y datos agregados para consumo (`gold/`).

**Etapa 3: Evaluación de las Propuestas de Refactorización**

*   **Revisión de `REFAC_*.md`:** Si Claude Cowork generó propuestas de refactorización, revisar el archivo `REFAC_001_propuesta.md`.
*   **Evaluación de la Calidad de las Propuestas:** Evaluar si las propuestas de refactorización son inteligentes, si reducen la complejidad y si mejoran la modularidad del código. No todas las propuestas de una IA son buenas; la supervisión humana es clave [[16](https://ntrs.nasa.gov/citations/19890066060)].
*   **Prueba de Impacto (si aplica):** Si se aprueba una refactorización compleja, se puede solicitar a Claude Cowork que genere un script de prueba o realizar pruebas manuales para verificar que la refactorización no introduce errores de comportamiento.

**Etapa 4: Firma y Versionado**

*   **Firma Explícita:** Una vez que todas las verificaciones anteriores sean satisfactorias, el soberano debe dar su firma explícita (ej. escribiendo "FIRMADO" en un archivo de registro) para aprobar la conclusión de la fase de reestructuración.
*   **Commit Final:** Realizar un commit final de Git. Este commit, que ahora incluye la carpeta `historico` y los archivos 'active' reorganizados, representa el hito de que la carpeta `p0x` ha sido exitosamente purgada y preparada. Este hito, combinado con la firma, es lo que hace que el estado del sistema sea "canonizado" en ese punto.

Este prompt de misión y la metodología de verificación crean un ciclo de trabajo cerrado y auditable. Proporcionan a Claude Cowork una hoja de ruta inequívoca y al soberano un conjunto de herramientas y criterios para garantizar que la intervención se realiza de manera precisa, segura y alineada con los principios del sistema soberano.

## Síntesis Estratégica y Hoja de Ruta para la Reestructuración

La implementación exitosa de este protocolo de intervención transformará la carpeta `p0x` de un conglomerado de proyectos en un andamiaje modular, robusto y soberano, capaz de soportar el desarrollo futuro de manera escalable y confiable. La estrategia se basa en la disciplina de la ejecución, la claridad de los criterios y la colaboración controlada entre el soberano y el supervisor tecnológico. A continuación, se presenta una síntesis de los hallazgos clave y una hoja de ruta accionable para guiar la reestructuración.

La síntesis del análisis revela que el éxito del proyecto no depende de la complejidad de la tecnología, sino de la adherencia a un conjunto de principios sencillos pero estrictos. La **arquitectura Medallion** proporciona la estructura lógica para gestionar los datos de manera progresiva y auditable, desde su estado bruto (Bronze) hasta su forma consumible (Gold) [[1](https://www.databricks.com/blog/what-is-medallion-architecture), [5](https://erstudio.com/blog/understanding-the-three-layers-of-medallion-architecture/)]. El **canon de Aurelius** suministra las reglas de comportamiento no negociables que gobiernan la interacción con esos datos, priorizando la honestidad (sensores honestos), la previsibilidad (fricción predictiva) y la verificación (filtro EDGE) [[16](https://ntrs.nasa.gov/citations/19890066060), [176](https://github.com/Aurelius-Canon/canon-gate)]. El rol de **Claude Cowork como supervisor activo** es la fuerza motriz que automatiza la aplicación de estos principios, realizando tareas de auditoría, clasificación y propuesta de refactorización a una escala que sería impracticable manualmente, todo ello bajo el control absoluto de la firma soberana [[136](https://www.stackai.com/insights/human-in-the-loop-ai-agents-how-to-design-approval-workflows-for-safe-and-scalable-automation), [245](https://www.sundeepteki.org/advice/the-definitive-guide-to-prompt-engineering-from-principles-to-production)].

Los hallazgos clave de la investigación son:
1.  **La Prioridad Absoluta de la Verificación Humana:** El principio de que "nada es canon hasta que existe en disco y versionado" [[16](https://ntrs.nasa.gov/citations/19890066060)] es la regla fundamental. Cada paso, desde la clasificación de un archivo hasta la ejecución de un script de refactorización, debe culminar en una firma humana que valide el resultado. Este mecanismo de control es lo que distingue este enfoque de una automatización ciega y lo alinea con los valores de soberanía.
2.  **La Importancia Crítica de la Decisión Inicial:** La resolución de ambigüedades tempranas, como la elección del repositorio oficial de CineK (`CineK_Studio` en este caso) [[16](https://ntrs.nasa.gov/citations/19890066060)], es un catalizador para el progreso. Sin estas decisiones, el desarrollo se atasca en un estado de indecisión. El protocolo de intervención aborda esto directamente al obligar a la toma de decisiones explícitas.
3.  **La Interdependencia de los Productos como Motor de Priorización:** El análisis mostró que varios productos dependen de otros (ej. Herbier y CineK dependen del Dashboard) [[16](https://ntrs.nasa.gov/citations/19890066060)]. Esto significa que la estrategia de desarrollo no puede ser lineal. La priorización debe ser dinámica, enfocándose primero en los bloques de construcción fundamentales que desbloquean múltiples productos. La heurística de "qué, cerrado, desbloquea más con menos construcción" [[16](https://ntrs.nasa.gov/citations/19890066060)] es la herramienta mental correcta para navegar esta complejidad.
4.  **La Gestión Activa de la Incertidumbre:** El proyecto opera con una cantidad significativa de "NO DATA" [[16](https://ntrs.nasa.gov/citations/19890066060)]. El protocolo reconoce esto y no intenta ignorarlo. En su lugar, trata la incertidumbre como un estado que debe ser gestionado y comunicado. Al detener la ejecución y pedir aclaraciones cuando surgen vacíos de información, el proceso se vuelve más resiliente y menos propenso a errores basados en suposiciones.

Basado en esta síntesis, se propone la siguiente hoja de ruta para la reestructuración de la carpeta `p0x`:

**Fase 0: Preparación y Firmas Iniciales (Estado Actual)**
*   **Acción:** Ya completada. Se han firmado las decisiones críticas iniciales: `CineK_Studio` como oficial, corrección hacia adelante por `config.py`, v2 del dashboard como oficial, push del commit local, uso de `planta_brote.webp` como placeholder, y posposición del Anclaje [[16](https://ntrs.nasa.gov/citations/19890066060)].
*   **Resultado:** La base está establecida para comenzar la reestructuración con una serie de incertidumbres resueltas.

**Fase 1: Purificación y Organización de la Carpeta `p0x` (Próximos Pasos)**
*   **Acción:** Ejecutar el **Prompt de Misión Inicial** para Claude Cowork.
*   **Responsable:** Claude Cowork (bajo supervisión).
*   **Entregable:** Una carpeta `p0x` limpia, con todos los componentes 'deprecated' archivados en `historico/`, y un informe `DEPRECATED_REPORT.md`.
*   **Verificación:** El soberano verifica el informe, la existencia de la carpeta `historico` y el contenido de la carpeta `p0x` principal. Se firma la aprobación.

**Fase 2: Refactorización Basada en Propuestas Aprobadas**
*   **Acción:** El soberano revisa las propuestas de refactorización generadas por Claude Cowork (`REFAC_*.md`) y aprueba las que considera viables.
*   **Responsable:** Soberano y Claude Cowork.
*   **Entregable:** Un conjunto de scripts o instrucciones de codificación para las refactorizaciones aprobadas.
*   **Verificación:** El ejecutor local (humano) realiza las refactorizaciones y se realiza una prueba de regresión para asegurar que no se rompió la funcionalidad existente. Se firma la conclusión de esta fase.

**Fase 3: Desarrollo Dirigido por Criterios de Cierre**
*   **Acción:** Con la base de `p0x` limpia y organizada, el equipo se enfoca en cerrar productos uno por uno, siguiendo la guía de requerimientos de éxito.
*   **Priorización:** Se inicia con el producto que ofrece el mayor desbloqueo con la menor construcción. Según el análisis, esto podría ser el **Herbier mínimo** si su construcción es realmente mínima y depende menos de otras partes del sistema, o el **Dashboard v2** si es el verdadero bottleneck [[16](https://ntrs.nasa.gov/citations/19890066060)].
*   **Proceso Iterativo para Cada Producto:**
    1.  **Definir:** Seleccionar un producto de la lista y definir su criterio de cierre verificable según la guía.
    2.  **Construir:** El ejecutor local (humano) desarrolla la funcionalidad para cumplir con el criterio.
    3.  **Verificar:** Se realiza una prueba técnica para confirmar que el criterio se cumple.
    4.  **Firmar:** El soberano firma la conclusión del producto.
    5.  **Versionar:** Se realiza un commit de Git que encapsule el producto completado.
*   **Verificación:** El ciclo completo (definir, construir, verificar, firmar, versionar) se repite para cada producto, en orden de prioridad.

En conclusión, este protocolo no es solo una serie de instrucciones, sino un marco de trabajo para la construcción soberana. Al fusionar una arquitectura de datos disciplinada, un conjunto de reglas de comportamiento inflexibles y un rol de supervisión tecnológica bien definido, se crea un sistema que es a la vez potente y controlable. Siguiendo esta hoja de ruta, la carpeta `p0x` se convertirá en un núcleo sólido y una demostración práctica de lo que significa construir y gobernar un sistema de datos completo, donde la prueba de que funciona es que dice la verdad, incluso cuando no sabe [[16](https://ntrs.nasa.gov/citations/19890066060)].