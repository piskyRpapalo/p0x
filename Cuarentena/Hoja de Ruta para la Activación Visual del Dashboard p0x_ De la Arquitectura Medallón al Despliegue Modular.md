# Hoja de Ruta para la Activación Visual del Dashboard p0x: De la Arquitectura Medallón al Despliegue Modular

Este informe detalla un plan estratégico y una hoja de ruta para transformar el estado actual del dashboard p0x, pasando de un estado donde los fondos y efectos visuales están definidos pero no integrados a un sistema operativo y visualmente coherente. La metodología se basa en la aplicación de la arquitectura Medallón como marco conceptual para la gestión del conocimiento y la ejecución, y prioriza la construcción modular de componentes para garantizar la mantenibilidad futura. El objetivo es activar los fondos de pantalla, las placas de escena y una serie de efectos visuales decorativos, asegurando un rendimiento óptimo en un entorno de CPU pura y alineándose estrictamente con la Doctrina de las Dos Luces. La estrategia se divide en tres oleadas secuenciales, cada una construyendo sobre la anterior, y culmina en un conjunto de prompts específicos para los agentes de IA (GLM, Qwen, Kimi) encargados de la implementación.

## Arquitectura Conceptual y Metodología de Trabajo: La Arquitectura Medallón Aplicada

La implementación del dashboard p0x se estructura bajo un marco metodológico disciplinado, adaptando la arquitectura Medallón —un patrón de diseño de datos— para gestionar el ciclo de vida del conocimiento y las decisiones del proyecto [[1](https://www.databricks.com/blog/what-is-medallion-architecture), [2](https://learn.microsoft.com/en-us/azure/databricks/lakehouse/medallion)]. Este enfoque metafórico permite organizar el desarrollo en tres niveles jerárquicos, asegurando que cada etapa esté fundamentada en evidencia tangible, decisiones validadas y entregables sellados. La arquitectura Medallón se aplica aquí no a datos, sino a las fases del desarrollo del software, proporcionando una hoja de ruta clara desde la acción atómica hasta la consolidación del producto. Esta metodología es fundamental para mantener la integridad del proyecto, documentar el razonamiento detrás de las decisiones y facilitar la transición entre fases de manera ordenada y sin ambigüedades.

El nivel más bajo, el **Medallón de Bronce**, corresponde a la fase de comandos y código de despliegue atómico. En esta etapa, la acción es directa y verificable. Incluye los scripts de bash para realizar copias de seguridad (`cp -r`), inyectar fragmentos de código (`cat >>`) o verificar la ausencia de propiedades potencialmente costosas como `will-change` en los widgets mediante herramientas como `grep` [[230](https://www.youtube.com/watch?v=_DWww3Bea2w)]. El propósito de este nivel es establecer una base sólida y reproducible, donde cada cambio se registra de forma atómica y puede ser auditado. Por ejemplo, antes de ejecutar una nueva oleada, se genera un respaldo del directorio `src` actual, creando un punto de restauración claro y específico [[230](https://www.youtube.com/watch?v=_DWww3Bea2w)]. Esta capa de registro es crucial para la resiliencia del sistema; si una implementación falla o introduce un problema, el historial de cambios atómicos permite identificar exactamente qué cambió y revertirlo con precisión.

El **Medallón de Plata** representa el núcleo del acuerdo técnico y de diseño. Aquí se consolida el conocimiento validado a través de diálogos técnicos y pruebas. Las decisiones tomadas en esta fase son principios rectores que guían toda la implementación posterior. Entre las decisiones clave del Medallón de Plata para el dashboard p0x se encuentran la adopción estricta de la doctrina de las dos luces, que separa rigurosamente la "Luz de Estado", cuantizada y binaria según el bus SSE, de la "Luz de Ambiente", compuesta por bucles decorativos autónomos que nunca codifican estado [[230](https://www.youtube.com/watch?v=_DWww3Bea2w), [508](https://www.churchofjesuschrist.org/study/manual/doctrinal-mastery-core-document-2023?lang=spa)]. Otra decisión crítica es la restricción a animaciones basadas únicamente en las propiedades `transform` y `opacity`, ya que estas pueden ser aceleradas por hardware sin un coste computacional excesivo en un entorno de CPU pura [[230](https://www.youtube.com/watch?v=_DWww3Bea2w)]. Además, se validan técnicas avanzadas de optimización como el uso de duraciones de animación coprimas (por ejemplo, 17s, 107s, 13s) para evitar la repetición visual o "beat frequency" durante sesiones prolongadas, y el uso de curvas de interpolación Bézier específicas para dar una sensación orgánica a las animaciones [[7](https://www.techment.com/blogs/medallion-architecture-explained/), [230](https://www.youtube.com/watch?v=_DWww3Bea2w)]. También se define la implementación de un `rAF watchdog` para monitorear el rendimiento en tiempo real y gestionar el presupuesto de composición de la GPU, suspendiendo efectos menos críticos cuando los FPS caen [[230](https://www.youtube.com/watch?v=_DWww3Bea2w)]. Este nivel es el cerebro del proyecto, donde la teoría se convierte en principios de diseño aplicables.

Finalmente, el **Medallón de Oro** selloa el entregable de una oleada específica, certificando que todos los componentes han sido implementados y validados según los principios del Medallón de Plata. Representa el hito de completar una fase del proyecto con éxito. Por ejemplo, al finalizar la Oleada 1, el Medallón de Oro se sellaría una vez que los fondos de pantalla (.nx-void y .jd-invernadero) estuvieran correctamente montados en `main.tsx`, `escena.css` importado, y las placas de escena integradas y funcionales [[230](https://www.youtube.com/watch?v=_DWww3Bea2w)]. Este sellado formal actúa como un checkpoint, asegurando que la base visual está estable antes de proceder con la siguiente fase de desarrollo, que sería la integración de los orbes interactivos y la conexión con el bus de estado. La adopción de esta arquitectura permite un flujo de trabajo disciplinado y transparente, donde cada paso está documentado, justificado y validado, minimizando la incertidumbre y maximizando la calidad del resultado final. A continuación se presenta una tabla que resume la aplicación de la arquitectura Medallón al contexto del dashboard p0x.

| Capa Medallón | Nivel Conceptual | Acciones Clave en el Contexto p0x | Tecnologías/Evidencias |
| :--- | :--- | :--- | :--- |
| **Bronce** | Comandos Atómicos | Creación de backups pre-ejecución, inyección de código via `cat >>`, verificación de reglas (ej. `grep -c "will-change"`). | Bash, React, CSS Puro [[230](https://www.youtube.com/watch?v=_DWww3Bea2w)] |
| **Plata** | Decisiones Validadas | Adopción de la Doctrina de las Dos Luces, uso de `transform/opacity` solo, duraciones coprimas, curvas Bézier orgánicas, Watchdog de FPS. | CSS Puro, React, Principios de UX/UI [[230](https://www.youtube.com/watch?v=_DWww3Bea2w)] |
| **Oro** | Sello de Entregable | Confirmación de que una oleada (ej. Oleada 1) ha cumplido todos sus objetivos funcionales y visuales. | Reporte de estado post-ejecución (ej. `[STATUS] OLEADA 3 COMPLETADA`) [[230](https://www.youtube.com/watch?v=_DWww3Bea2w)] |

Esta metodología no es meramente administrativa; refuerza una cultura de diseño deliberado. Al obligar a registrar tanto las acciones atómicas (Bronce) como las decisiones fundamentales (Plata), el equipo evita la reincidencia de errores y la pérdida de contexto. Ideas que fueron descartadas previamente, como la adición de textura de ruido a las tarjetas del Nexo debido a su naturaleza brutalista, deben ser registradas en un archivo de "Senda de los Muertos" (`dead_path.jsonl`) para que no surjan de nuevo en debates futuros [[230](https://www.youtube.com/watch?v=_DWww3Bea2w)]. Esto solidifica la consistencia y la intencionalidad del diseño. La arquitectura Medallón, en este sentido, se convierte en el ancla metodológica que mantiene el proyecto enfocado en sus objetivos, desde la ejecución de un script simple hasta la concepción de una experiencia de usuario compleja y fluida.

## Fase 1: Establecimiento de la Base Visual y Funcional (Oleada 1)

La primera fase del plan de acción, denominada **Oleada 1: Fundaciones**, tiene como objetivo primordial resolver las brechas críticas que impiden que el dashboard visualmente represente la versión V2. El diagnóstico inicial reveló tres problemas fundamentales: los fondos `.nx-void` y `.jd-invernadero` no estaban aplicados en los componentes raíz, el archivo de estilos `escena.css` existía pero no era importado en los archivos de TypeScript, y había un proceso sospechoso (CineK) que requería atención [[230](https://www.youtube.com/watch?v=_DWww3Bea2w)]. La solución propuesta no es simplemente aplicar los fondos al `<body>` o `#root`, ya que esto crearía graves conflictos de interacción y composición. Una recomendación crítica fue aislar el fondo del DOM interactivo utilizando un contenedor semántico aislado, `.scene-canvas`, con `position: fixed` y `pointer-events: none` [[230](https://www.youtube.com/watch?v=_DWww3Bea2w)]. Este contenedor, con `z-index: 0`, garantiza que el fondo permanezca por debajo de todos los demás elementos, como los widgets y los orbes, que tendrán un `z-index: 10`. El uso de `pointer-events: none` es crucial, ya que hace que el fondo sea "invisible" para los eventos del ratón, evitando que intercepte clics y rompa la interactividad de los componentes superpuestos [[230](https://www.youtube.com/watch?v=_DWww3Bea2w)].

Una vez establecido el aislamiento, la siguiente tarea es integrar las placas fotográficas (`placaa.webp` y `placab.webp`) dentro de este contenedor de escena. Para lograr una integración limpia y eficiente, se recomienda usar una etiqueta `<img>` con `object-fit: cover` para que la imagen cubra todo el contenedor sin distorsionarse. Sin embargo, la transición entre el fondo V1 (negro plano) y las nuevas capas de escena podría generar un "flash" visual o problemas de contraste. Para mitigar esto, se propone la aplicación de un viñeteado radial semántico. Para El Nexo (`.nx-void`), se aplicaría un gradiente radial oscuro (`rgba(10, 12, 18, 0.95)`) en los bordes para enmarcar los datos y mejorar el contraste del texto, mientras que para Le Jardin (`.jd-invernadero`), se usaría un tono verde bosque (`rgba(4, 10, 6, 0.95)`) para crear una sensación de inmersión [[230](https://www.youtube.com/watch?v=_DWww3Bea2w)]. Además, para evitar que las imágenes compitan visualmente con los datos críticos, se sugiere aplicar una opacidad baja (alrededor del 20-30%) y un modo de fusión suave como `mix-blend-mode: overlay` o `soft-light` [[230](https://www.youtube.com/watch?v=_DWww3Bea2w)]. Esto integra la imagen con el color de fondo base, manteniéndola como un soporte atmosférico sutil en lugar de una capa dominante.

La implementación técnica de estos cambios se realiza a través de dos acciones principales. Primero, se debe importar el archivo `escena.css` en ambos puntos de entrada de la aplicación, `nexo/main.tsx` y `jardin/main.tsx` [[230](https://www.youtube.com/watch?v=_DWww3Bea2w)]. Segundo, se modifica la estructura JSX de estos archivos para envolver el contenido principal de la aplicación en el contenedor `.scene-canvas`. Dentro de este contenedor, se renderiza la imagen de la placa correspondiente y una capa de viñeteado. El código CSS para esta capa de composición se define en `escena.css` o en un módulo de estilos global. Se añade también un contenedor para el espacio de trabajo principal (`.dashboard-workspace`) que contendrá todos los widgets y tendrá un padding generoso para que el fondo "respire" en los bordes [[230](https://www.youtube.com/watch?v=_DWww3Bea2w)].

Un aspecto crucial de esta fase, especialmente dado el requisito de CPU pura, es la gestión de las capas de composición. Aunque las placas de escena son elementos estáticos, moverlas a su propia capa de composición puede mejorar el rendimiento general al aislarlas del resto del DOM. Esto se puede lograr forzando al navegador a crear una nueva capa de composición para el `.scene-canvas` usando propiedades como `transform: translateZ(0)` o `will-change: transform` [[230](https://www.youtube.com/watch?v=_DWww3Bea2w)]. Esta medida es particularmente beneficiosa para las animaciones de las siguientes oleadas, ya que asegura que los cambios en los widgets no fuerzan un repintado completo del fondo pesado, lo que podría causar *jank* (caída de FPS). Al ejecutar esta fase, el equipo debe validar que el backup se crea correctamente antes de cualquier modificación y que las importaciones y el montaje JSX sean exitosos, asegurando que la base visual y funcional del dashboard esté sólidamente establecida antes de pasar a la integración de componentes interactivos.

## Fase 2: Integración de Componentes Interactivos y Estado (Oleada 2)

La segunda fase, **Oleada 2: Orbital V2**, se centra en la integración de los componentes interactivos clave: los orbes del Launcher y su conexión con el estado del sistema a través del bus SSE. Esta oleada construye directamente sobre la base visual establecida en la Fase 1. El primer paso es la refactorización del componente de los orbes, extrayéndolo desde su ubicación actual en `nexo/header/Header.tsx` a un componente compartido y reutilizable ubicado en `src/shared/launcher/Launcher.tsx` [[230](https://www.youtube.com/watch?v=_DWww3Bea2w)]. Esta acción de "construcción en cajones" es fundamental para la modularidad y la escalabilidad del dashboard. Al crear un componente aislado, se encapsula toda la lógica y el estilo de los orbes, permitiendo que se monte en diferentes partes de la aplicación (como se solicita para Jardin) sin acoplamiento de código [[13](https://docs.sveltycms.com/docs/development/dashboard/architecture), [338](https://github.com/sandeep-stha/modular-widget-dashboard)]. La centralización de variables de diseño, como el tamaño de los orbes (`--orb-size`), en un archivo de tokens como `tokens.css` es una práctica impecable de un sistema de diseño que facilitará la uniformidad y la futura personalización [[230](https://www.youtube.com/watch?v=_DWww3Bea2w)].

Con el componente `Launcher` aislado, la siguiente tarea es actualizar su apariencia para cumplir con los nuevos estándares visuales. Se especifica que los orbes deben tener un tamaño único de 44px, sin borde exterior (`border: none`), con fondo transparente y `overflow: hidden` para contener la imagen del medallón. La imagen del medallón debe usar `object-fit: cover` para llenar el contenedor perfectamente [[230](https://www.youtube.com/watch?v=_DWww3Bea2w)]. La interacción con el mouse también se redefine: al pasar el cursor sobre un orbe, este debe mostrar una sombra de desplazamiento. Para El Nexo, la sombra será de color cian, y para Le Jardin, de color musgo, creando así un feedback visual diferenciado que refuerza la identidad de cada sub-dashboard [[230](https://www.youtube.com/watch?v=_DWww3Bea2w)]. La implementación de estas sombras se debe hacer de manera eficiente, evitando animaciones costosas en `box-shadow`. Una técnica sugerida es usar un pseudo-elemento `::after` con la sombra ya renderizada y una opacidad de 0, animando la opacidad del pseudo-elemento en lugar de la propiedad `box-shadow` directamente, lo cual es matemáticamente trivial para la CPU [[230](https://www.youtube.com/watch?v=_DWww3Bea2w)].

La parte más crítica de esta oleada es conectar los orbes a la fuente de verdad del sistema: el bus SSE. Actualmente, el componente `IconoVivo` mapea un estado `live` de forma fija. La tarea corregida es hacer que lea el estado real del bus SSE [[230](https://www.youtube.com/watch?v=_DWww3Bea2w)]. Esto implica consumir el contexto del Puente y mapear el estado correcto del sensor (ej. `puente?.nexo?.estado`) a la clase CSS que controla la animación del medallón correspondiente. Se debe implementar un mecanismo de fallback robusto: si el estado del bus es desconocido, el orbe debe mostrar un estado `STATIC` [[230](https://www.youtube.com/watch?v=_DWww3Bea2w)]. Una condición específica a manejar es el caso de la térmica superior a 80°C. En este escenario, el orbe no solo debe cambiar de estado, sino que debe alternar entre dos frames (`radiante_a` y `radiante_b`) y añadir un parpadeo ámbar de alta frecuencia (único parpadeo legal) [[230](https://www.youtube.com/watch?v=_DWww3Bea2w)]. Esto requiere una lógica de estado más sofisticada en el componente `IconoVivo`, que puede ser gestionada con hooks de React como `useEffect` para escuchar los cambios del bus SSE y actualizar el estado local del componente en consecuencia.

Finalmente, se debe realizar el montaje de estos nuevos componentes en la aplicación. Para El Nexo, el componente `Header` ya existe, por lo que el `Launcher` debe ser insertado después de él. Para Le Jardin, se requiere una modificación similar, montando el `Launcher` antes de otro componente específico (`<Launcher contexto="jardin" />`). Dado que estos cambios implican modificar el JSX en archivos de producción, se sugiere un script de Python para realizar la sustitución de manera precisa y automatizada, asegurando que el nuevo componente se inserte en el lugar correcto [[230](https://www.youtube.com/watch?v=_DWww3Bea2w)]. Antes de confirmar la ejecución, es imperativo realizar una verificación exhaustiva para asegurar que los componentes de ambiente se hayan montado correctamente en el árbol de componentes. Esto incluye verificar que las importaciones de `MuroAmbiente` y `LaboratorioAmbiente` existan en los respectivos `main.tsx` y que los componentes se rendericen como JSX, no como comentarios o código muerto [[230](https://www.youtube.com/watch?v=_DWww3Bea2w)]. Al completar esta oleada, el dashboard habrá pasado de ser una interfaz estática a una que no solo muestra información, sino que también responde dinámicamente al estado del sistema, sentando las bases para la activación de efectos ambientales más complejos en la siguiente fase.

## Fase 3: Activación de Efectos Visuales y Optimización de Rendimiento (Oleada 3)

La tercera y más compleja fase, **Oleada 3: Escenas Vivas**, se dedica a activar la "Luz de Ambiente" siguiendo la doctrina de que estos efectos son decorativos y autónomos, sin codificar jamás el estado del sistema [[230](https://www.youtube.com/watch?v=_DWww3Bea2w)]. Esta oleada se divide en la implementación de efectos para El Muro (Nexo) y El Laboratorio (Jardin), cada uno con su propio conjunto de animaciones y reglas de interacción. La implementación debe realizarse con un rigor extremo en el rendimiento, dado el entorno de CPU pura. La estrategia central es la optimización de las capas de composición y la selección cuidadosa de las propiedades CSS a animar. Se debe evitar a toda costa el uso de `will-change` en celdas de datos o widgets, ya que cada asignación consume un recurso valioso de la GPU y es innecesario para transiciones simples de `opacity` y `color` [[230](https://www.youtube.com/watch?v=_DWww3Bea2w)]. Los seis slots de `will-change` globales deben reservarse exclusivamente para los elementos que se mueven o se actualizan constantemente: las placas de escena, los orbes y el propio `rAF watchdog`.

Para El Muro, se implementarán varias capas de animación. Las venas SSE (`nx-venas-sse`) se animarán cambiando su color de borde en función del estado del bus (ej. `data-state="live"`), en lugar de usar `background-color`, para mantener el costo computacional bajo [[230](https://www.youtube.com/watch?v=_DWww3Bea2w)]. Las amatistas (`nx-amatista`) deben respirar con una secuencia de `animation-delay` que evite el patrón robótico del unísono. En lugar de delays lineales, se utilizará una secuencia basada en la proporción áurea (ej. 0s, 1.1s, 1.7s, 2.8s, 4.5s, 7.3s) para crear un ritmo más orgánico [[230](https://www.youtube.com/watch?v=_DWww3Bea2w)]. La animación de respiración misma debe usar una curva de Bézier especial (`cubic-bezier(.45, 0.05, 0.55, 0.95)`) para simular la expansión y contracción de un pulmón biológico [[230](https://www.youtube.com/watch?v=_DWww3Bea2w)]. Las god-rays se implementarán con un pseudo-elemento (`::after`) que use `mix-blend-mode: screen` sobre una capa de gradientes, animando su rotación. Para evitar un impacto de rendimiento masivo, esta capa debe estar confinada a una región pequeña del viewport y su duración debe ser un número primo (ej. 107s) para evitar la repetición visual [[7](https://www.techment.com/blogs/medallion-architecture-explained/), [230](https://www.youtube.com/watch?v=_DWww3Bea2w)]. El vaivén del suelo y la ráfaga de hiedra se animarán con `transform: translateY()` y `transform: translateX()`, respectivamente, y sus duraciones también deben ser números primos (ej. 17s y 37s) [[230](https://www.youtube.com/watch?v=_DWww3Bea2w)].

En Le Jardin, la mecánica es similar pero con un vocabulario visual diferente. Las velas (`jd-vela`) proyectarán luz dinámica sobre la placa `placab.webp` a través de un pseudo-elemento `::after` con un `radial-gradient`. La sincronización del parpadeo de la vela con el destello de su luz se logrará animando la `opacidad` del pseudo-elemento, una operación barata en CPU [[230](https://www.youtube.com/watch?v=_DWww3Bea2w)]. Las duraciones de las velas deben ser números primos (1.7s, 2.9s, 4.3s) para que su parpadeo nunca coincida [[230](https://www.youtube.com/watch?v=_DWww3Bea2w)]. El cofre de oro (`jd-cofre-gold`) debe mostrar un destello (`shimmer`) solo cuando el estado del bus indique que el diario está sellado (`diarysealed`) [[230](https://www.youtube.com/watch?v=_DWww3Bea2w)]. Los pétalos del cosmos (`jd-petalo`) caerán con una duración aleatoria entre 10-16 segundos y se reciclarán usando un pool de 12 nodos DOM para evitar fugas de memoria y mantener el rendimiento, detectando el evento `onAnimationEnd` para reiniciarlos [[230](https://www.youtube.com/watch?v=_DWww3Bea2w)]. El cielo del laboratorio (`jd-arco-sentinelle`) cambiará de brillo con el tiempo, animando una propiedad `filter` en lugar de `background-image` para mayor eficiencia [[230](https://www.youtube.com/watch?v=_DWww3Bea2w)].

Una consideración filosófica y de diseño crucial es la respuesta del sistema ante fallos. Si el bus SSE se desconecta, la doctrina dicta que la Luz de Ambiente no puede ignorar por completo la muerte del sistema. Se implementará un efecto de transición suave: al añadir una clase `.bus-offline` al nodo raíz del documento, todas las capas de ambiente se atenuarán mediante un filtro de `saturate(0.3)` y `brightness(0.6)`, indicando visualmente que el sistema está offline sin simplemente desaparecer [[230](https://www.youtube.com/watch?v=_DWww3Bea2w)]. Para el modo ahorro, se debe implementar una jerarquía de sacrificio elegante: primero se desactivan las microinteracciones de hover, luego se pausan las partículas (motas y pétalos), y finalmente se reduce la opacidad de las god-rays. La Luz de Estado, sin embargo, es inviolable y siempre debe mantenerse visible [[230](https://www.youtube.com/watch?v=_DWww3Bea2w)]. La implementación de un `rAF watchdog` será vital en esta fase. Monitoreando el rendimiento del bucle de animación, este vigilante podrá suspender efectos menos críticos para garantizar que las transiciones de estado del SSE (≤80ms) no se vean afectadas, priorizando siempre la legibilidad de los datos sobre la decoración visual [[230](https://www.youtube.com/watch?v=_DWww3Bea2w)].

## Hoja de Ruta Final y Prompts de Implementación

La hoja de ruta consolidada para la implementación del dashboard p0x se articula en tres oleadas secuenciales, cada una construyendo sobre el conocimiento validado del nivel Medallón de Plata y culminando en un entregable sellado en el nivel Medallón de Oro. Este plan, refinado a través de la colaboración entre el Arquitecto Principal, GLM, Qwen y Kimi, proporciona un camino claro y metódico para transformar el dashboard. La ejecución debe seguir estrictamente la secuencia para evitar dependencias circulares y asegurar que la base visual y funcional esté sólidamente establecida antes de introducir la complejidad de las interacciones y las animaciones.

La primera oleada, **Fundaciones (Oleada 1)**, aborda las brechas críticas iniciales. Consiste en el aislamiento del fondo mediante un contenedor `.scene-canvas` con `pointer-events: none`, la importación de `escena.css` y la integración de las placas fotográficas (`placaa.webp`, `placab.webp`) con viñeteado y modos de fusión para garantizar el contraste y la atmósfera [[230](https://www.youtube.com/watch?v=_DWww3Bea2w)]. Esta fase tiene un riesgo bajo y establece la base visual sobre la cual se construirán todos los demás elementos.

La segunda oleada, **Orbital V2 (Oleada 2)**, introduce la interactividad. Implica la creación de un componente `Launcher` aislado y reutilizable, su refactorización visual para cumplir con los estándares de tamaño y efectos de sombra, y, lo más importante, su conexión con el estado real del bus SSE para reflejar dinámicamente el estado del sistema [[230](https://www.youtube.com/watch?v=_DWww3Bea2w)]. Esta fase conecta la interfaz con la fuente de verdad del sistema, transformándola de estática a dinámica.

La tercera y última oleada, **Escenas Vivas (Oleada 3)**, es la más compleja y se enfoca en la "Luz de Ambiente". Aquí se implementan las animaciones autónomas del Muro y el Laboratorio, utilizando técnicas avanzadas como duraciones coprimas y delays basados en la proporción áurea para evitar la repetición visual y crear un efecto orgánico [[230](https://www.youtube.com/watch?v=_DWww3Bea2w)]. Esta fase también incluye la implementación de un `rAF watchdog` para la gestión del rendimiento y una respuesta visual al estado offline del bus, cumpliendo así con la doctrina de las dos luces [[230](https://www.youtube.com/watch?v=_DWww3Bea2w)].

A continuación, se presentan los prompts finales para cada agente, diseñados para que GLM ejecute la Oleada 3, Qwen valide la estética y Kimi supervise el rendimiento.

**Prompt para GLM (Ejecutor): Oleada 3 Corregida y Blindada**
Este prompt contiene los comandos de ejecución atómica para la Oleada 3, integrando las correcciones y validaciones discutidas. Se debe ejecutar en su totalidad.
```markdown
🏛️ ORDEN OLEADA 3 — Escenas Vivas: Muro + Laboratorio (CORREGIDO Y BLINDADO)

PROTOCOLO:
1. BACKUP:
   BACKUP_DIR=~/hexelion/dashboard/.backups/oleada3_$(date +%s)
   mkdir -p "$BACKUP_DIR"
   cp -r ~/hexelion/dashboard/src "$BACKUP_DIR/"
   echo "[BACKUP] $BACKUP_DIR"

2. VERIFICACIÓN PREVIA:
   grep -n "export.*usePuente\\|export.*PuenteContext" ~/hexelion/dashboard/src/shared/puente/Puente.tsx
   grep -c "will-change" ~/hexelion/dashboard/src/shared/escena/escena.css
   echo "---"
   grep -rn "will-change" ~/hexelion/dashboard/src/nexo/ ~/hexelion/dashboard/src/jardin/ 2>/dev/null | grep -v ".backups" | head -10
   echo "Si hay will-change en celdas/widgets, reportar antes de continuar."

3. ESCRITURA ATÓMICA — Bloque A: escena.css (añadir al final):
   cat >> ~/hexelion/dashboard/src/shared/escena/escena.css << 'EOF'
   [CONTENIDO DE CSS CORREGIDO Y BLINDADO]
   EOF

4. ESCRITURA ATÓMICA — Bloque B: MuroAmbiente.tsx (LECTURA CORREGIDA V-01):
   mkdir -p ~/hexelion/dashboard/src/shared/escena
   cat > ~/hexelion/dashboard/src/shared/escena/MuroAmbiente.tsx << 'EOF'
   [CONTENIDO DE MuroAmbiente.tsx CORREGIDO]
   EOF

5. ESCRITURA ATÓMICA — Bloque C: LaboratorioAmbiente.tsx (LECTURA CORREGIDA V-01):
   cat > ~/hexelion/dashboard/src/shared/escena/LaboratorioAmbiente.tsx << 'EOF'
   [CONTENIDO DE LaboratorioAmbiente.tsx CORREGIDO]
   EOF

6. MONTAJE CORREGIDO — Bloque D (V-02 + V-03):
   # NEXO: ancla es <Header />, NO <Launcher />
   python3 << 'PYEOF'
   [SCRIPT DE PYTHON PARA MONTAR EL COMPONENTE EN NEXO]
   PYEOF

   # JARDIN: ancla es <Launcher contexto="jardin" /> (prefijo <Launcher)
   python3 << 'PYEOF'
   [SCRIPT DE PYTHON PARA MONTAR EL COMPONENTE EN JARDIN]
   PYEOF

7. VERIFICACIÓN DURA (V-03 endurecido):
   echo "=== IMPORTS ==="
   grep -n "MuroAmbiente\\|LaboratorioAmbiente" ~/hexelion/dashboard/src/nexo/main.tsx ~/hexelion/dashboard/src/jardin/main.tsx
   echo ""
   echo "=== JSX RENDERIZADO (obligatorio) ==="
   grep -n "<MuroAmbiente />" ~/hexelion/dashboard/src/nexo/main.tsx
   grep -n "<LaboratorioAmbiente />" ~/hexelion/dashboard/src/jardin/main.tsx
   echo ""
   echo "=== will-change COUNT en escena.css ==="
   grep -c "will-change" ~/hexelion/dashboard/src/shared/escena/escena.css
   echo ""
   echo "=== will-change en widgets (debe ser 0) ==="
   grep -rn "will-change" ~/hexelion/dashboard/src/nexo/celdas/ ~/hexelion/dashboard/src/nexo/tray/ ~/hexelion/dashboard/src/jardin/cahier/ ~/hexelion/dashboard/src/jardin/herbier/ 2>/dev/null | wc -l

REPORTA:
[STATUS] OLEADA 3 COMPLETADA
[BACKUP] Ruta exacta
[WILL-CHANGE] Count escena.css + count widgets
[MONTAJE JSX] Confirmar que ambos componentes aparecen como JSX renderizado
```

**Prompt para Qwen (Validador Visual):**
Después de que GLM ejecute el prompt anterior, este es el prompt para Qwen para que revise la salida y valide la implementación visual.
```markdown
🎨 NODO QWEN · RESPUESTA ÓPTICA (Vanguardia 2026 · p0x)

Verifica la implementación de la Oleada 3 contra la siguiente lista de verificación visual:

1.  **Jerarquía y Contraste (Doctrina de las Dos Luces):**
    *   Verificar que el cian (#00FFFF) de las venas SSE no compita visualmente con los datos. ¿El ratio de contraste WCAG AA se mantiene?
    *   En el Brutalismo (Nexo), confirmar que los bordes de 1px y radio 0 no parecen "ventanas de Windows 95", sino "industriales".
    *   Cuando el estado es ERROR (rojo), verificar que las god-rays del Muro se atenúan automáticamente (ej. opacity: 0.15) y no compiten con la alerta.

2.  **Texturas y Vanguardia 2026:**
    *   Inspeccionar las amatistas. ¿La secuencia de delays (0, 1.1, 1.7...) crea un ritmo orgánico o un patrón detectable?
    *   Observar la animación de respiración. ¿La curva Bézier (`cubic-bezier(0.45, 0.05, 0.55, 0.95)`) produce una expansión/succión suave, como un pulmón?
    *   El cofre de oro debe tener un shimmer que parezca metal bruñido, no plástico. ¿El gradiente y la animación logran esto?

3.  **Integración de CineK y Espacialidad:**
    *   El iframe de CineK debe integrarse como un "cuadro mágico". ¿El borde y la sombra son sutiles pero efectivos?
    *   Cuando se activa el feedback cruzado (destello de 400ms), ¿el color dorado (#FFD700) emerger sobre `placab.webp` sin lavarlo?

4.  **Microinteracciones y Edge Cases:**
    *   Pasar el mouse sobre una celda de dato. ¿Hay un feedback físico (ej. `transform: translateX(2px)`) sin usar color ni sombra?
    *   Simular un bus offline. ¿El efecto de `saturate(0.3) brightness(0.6)` se activa suavemente y el estado STATIC de los orbes se vuelve "vigilante"?
    *   En `.mode-ahorro`, ¿la mascota flotante activa un patrón de bajo consumo (ej. ojos cerrados)?

**Dictamen:** Informar si la implementación cumple o viola la doctrina visual, especificando qué elementos necesitan ajuste.
```

**Prompt para Kimi (Validador de Rendimiento y Seguridad):**
Simultáneamente, este es el prompt para Kimi para auditar la implementación de la Oleada 3.
```markdown
🛡️ NODO KIMI · RESPUESTA DE PARANOIA JUSTIFICADA (p0x)

Auditoría de la Oleada 3 en busca de fugas de rendimiento, segundas intenciones y vulnerabilidades ocultas.

1.  **Rendimiento y Composición (CPU-Only):**
    *   Usando DevTools Layers, verificar que solo haya 6 capas de composición promovidas por `will-change` globales. ¿Están en las placas, orbes y watchdog?
    *   ¿Las celdas de datos y otros widgets tienen `will-change`? Si es así, es una violación crítica.
    *   Analizar el uso de CPU. ¿Las animaciones de `mix-blend-mode` (god-rays) o `filter` en bucles infinitos están causando picos de CPU?
    *   ¿El `rAF watchdog` está correctamente implementado para reducir la densidad de partículas o pausar efectos secundarios cuando los FPS caen por debajo de un umbral (ej. 45)?
    *   ¿El reciclaje de pétalos (pool de 12 nodos) funciona correctamente? ¿Se verifica que un nodo ha salido del viewport antes de ser reciclado para evitar memory leaks?

2.  **Seguridad y Aislamiento (Soberanía):**
    *   El iframe de CineK usa `sandbox`? ¿Permite `postMessage` pero bloquea `top-navigation`?
    *   ¿Se valida el origen (`event.origin`) de los mensajes `postMessage` desde el iframe para prevenir ataques XSS?
    *   ¿Los assets de imagen (WebP) han sido escaneados para la vulnerabilidad CVE-2023-4863? ¿Se ha implementado algún mitigador (ej. deshabilitar WebP, usar librerías saneadas)?
    *   ¿La hidratación de `localStorage` en los tinteros es segura y no causa un "flash de contenido no autorizado" (FOUC)?

3.  **Edge Cases y Resiliencia:**
    *   ¿Qué pasa si un asset de imagen (ej. `placaa.webp`) falla con un error 404? ¿El componente tiene un fallback degradado (ej. glifo CSS o fondo sólido)?
    *   ¿El sistema gestiona adecuadamente el `prefers-reduced-motion`? ¿Los loops de ambiente se detienen, pero las transiciones de estado (≤80ms) permanecen instantáneas?
    *   ¿El `rAF watchdog` tiene un "Dead Man's Switch"? Si el hilo principal se congela, ¿hay un elemento CSS puro que parpadee para alertar al usuario?
    *   ¿El botón de pánico de rollback a la Oleada 2 está documentado y probado? ¿Funciona en menos de 5 segundos?

**Dictamen:** Informar si la implementación es segura y resiliente, o si presenta riesgos de rendimiento, seguridad o estabilidad que requieren corrección inmediata.
```