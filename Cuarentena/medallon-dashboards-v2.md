# ARQUITECTURA MEDALLÓN DE LOS TRES DASHBOARDS · p0x
## MARCO DE PERSISTENCIA Y RENDERIZADO SOBERANO

Este documento define la distribución, persistencia y comportamiento del stack de visualización de datos del nodo p0x a lo largo de las tres capas de la arquitectura Medallón (Bronze, Silver y Gold). El sistema gestiona tres interfaces independientes sincronizadas mediante el bus de red local:
1.  **El Nexo** (Panel de Control Brutalista Web de React/Vite/FastAPI)
2.  **Le Jardin des Ombres** (Diario y base botánica interactiva web)
3.  **Dashboard CMP** (Panel de pared nativo de escritorio en Compose Multiplatform y Skia)

---

## 1. EL NEXO (BRUTALISMO SOBERANO · WEB UI)

### Capa Bronze (Registro de Interacción y Renderizado Crudo)
*   **Mecánica de Entrada**: Captura en crudo de interacciones en las rutas de disco `raw_events/` y `raw_chat/` correspondientes a cada prompt del operador, comandos propuestos por el preceptor y clicks sobre la interfaz en formato JSONL incremental.
*   **Física de la UI**: Renderizado de baja sobrecarga de procesamiento para elementos base: cajas de texto monospace, terminal de logs inmutable, y layouts de CSS Grid con borde universal de 1px y esquinas con radio de 0px.
*   **Flujo de Datos**: Conexión de transferencia de datos unidireccional y continua mediante Server-Sent Events (SSE) con una cadencia de 2 segundos hacia el backend local de FastAPI, enrutando métricas de red y radiofrecuencia. El DOM limita el re-renderizado a un máximo de 1 vez por 100ms por celda para mitigar la sobrecarga de la CPU.

### Capa Silver (Consolidación de Propuestas y Transición de Estados)
*   **Modo Cosecha (Harvest Mode)**: Las transacciones y cambios de configuración propuestos se consolidan mensualmente en bloques de 10 a 20 registros dentro del archivo mensual de propuestas `proposals_YYYY-MM.jsonl`.
*   **Gestor de Transiciones**: Las animaciones de interfaz decorativas y complejas se deshabilitan. Se autorizan exclusivamente transiciones instantáneas o cambios de opacidad con un límite de duración de 80ms lineal en los cambios de estado de las celdas de telemetría.
*   **Manejo de Ausencia de Datos**: Ante la interrupción del flujo de datos del socket durante 1500ms, la interfaz recupera el timestamp del último paquete válido (`last seen HH:MM`) realizando una consulta al índice temporal local de la capa Silver.

### Capa Gold (Sello de Comando y Verdad Firmada)
*   **El Signature Tray**: Las cartas de comandos del Nexo correspondientes a parches y scripts del sistema exigen un bloque perimetral obligatorio de verificación de código y su correspondiente expectativa de salida (`EXPECT`).
*   **Fricción de Copiado (Portapapeles Soberano)**: Se prohíbe la inyección automatizada de código en la terminal o botones de copia automática de un solo clic. El Nexo exige selección manual del texto y la combinación física de teclado `Ctrl+C` para forzar la auditoría visual obligatoria del comando.
*   **Sello Criptográfico**: La acción `SIGN` calcula el hash SHA-256 de la propuesta. El sistema bloquea la ejecución física hasta que el operador ingresa la firma digital Ed25519 detached, permitiendo que el script de inicio `verify_pow.sh` valide y aplique el cambio de manera inmutable en disco.

---

## 2. LE JARDIN DES OMBRES (SOLARPUNK-ANIME · WEB UI)

### Capa Bronze (El Diario Local y Base de Trabajo)
*   **Mesa de Madera y Pergamino**: Interfaz y texturas generadas exclusivamente mediante gradientes y repeticiones lineales de CSS vanilla en el navegador para evitar la carga de archivos de imagen de fondo pesados.
*   **Superficie de Escritura**: El editor de anotaciones del Cahier opera sobre un elemento `contentEditable` con tipografía `EB Garamond` de 17px, transmitiendo la telemetría de las pulsaciones en caliente a los ficheros del buffer `raw_voice/` o `raw_events/` de la capa Bronze.
*   **Buffer de Red**: Los tinteros interactivos de guardado (`Garder` en verde y `Mémoire` en violeta) persisten temporalmente las modificaciones locales en el búfer `localStorage` del cliente.

### Capa Silver (Reconciliación Offline y Segundo Cerebro)
*   **Reconciliación de Arranque**: En la fase de inicialización de la interfaz, un script compara los hashes de los registros locales en `localStorage` con la base de datos relacional del backend, re-encolando y sincronizando de forma automática los deltas de datos ausentes.
*   **Grafo del Second Brain**: Visualización espacial del grafo de engramas mediante un algoritmo de fuerzas físicas interactivo (`force-graph`), restringido estrictamente bajo la Ley de Detalle por Zoom (LOD) para prevenir la sobreposición de etiquetas de texto y sobrecargas de CPU en hilos cliente.
*   **La Sentinelle (Captura de Video)**: Despliega un componente visualizador de video en relación de aspecto 4:3 con controles interactivos de captura y llamada a Fullscreen API. Los flujos de telemetría del ESP32 se limitan a una frecuencia de actualización de 10Hz hacia el DOM para proteger el hilo de renderizado.

### Capa Gold (Sincronización de Agentes e Identidad Criptográfica)
*   **Soberanía de Datos**: Se prohíbe la persistencia definitiva de datos privados en el navegador del cliente. La pulsación de `Garder` despacha una petición HTTP POST autenticada hacia la API cifrada del nodo de red, guardando la anotación en el diario sellado de Gold (`diary_sealed/`).
*   **Integración del Context Provider**: La selección de una ficha botánica inyecta de forma automática las variables identificadoras de la planta (`plantId`) en el prompt del sistema local, asegurando que las respuestas del preceptor se ciñen exclusivamente al RAG de datos autorizados.
*   **Modo Ahorro de Carbono (OB)**: Ante el reporte de caída de tensión solar o suministro de batería baja (clase `.mode-ahorro` activa), la interfaz atenúa su brillo general mediante filtros de brillo al 92% y activa el patrón visual de consumo mínimo en la mascota flotante.

---

## 3. DASHBOARD CMP (ALTAR FÍSICO Y SEÑAL · COMPOSE DESKTOP/JVM)

### Capa Bronze (Renderizado de Alto Rendimiento en Silicio)
*   **Motor Gráfico**: Renderizado nativo acelerado por hardware a través de Skia ejecutándose bajo la JVM de tu procesador AMD Ryzen.
*   **Pilas de Repositorio**: Conexiones directas a las interfaces desacopladas de datos de bajo nivel: `RfSignalRepository`, `SolarChargeRepository` y `SystemThermalRepository`.
*   **Ecopuertos**: Los contenedores de video de cámaras de seguridad y telemetría operan en relaciones de aspecto fijas de 4:3 o 16:9 y propiedades estrictas de escala de contenido `object-fit: cover`, visualizando caracteres nulos si se detecta pérdida de conexión con el sensor.

### Capa Silver (Performance Watchdog y Screenshot Testing)
*   **Filtro de Jank (PerformanceWatchdog)**: El monitor de frames por segundo analiza en caliente el rendimiento del bucle gráfico de Skia. Si se detectan caídas de velocidad por debajo de los umbrales seguros, suspende de forma automática los shaders de fondo (PERLIN_MOSS) y reduce la densidad de partículas.
*   **Screenshot Juez**: Suite de screenshot testing automatizada previa al merge que captura los layouts del dashboard CMP inmaculado en breakpoints definidos de compilación y evalúa su conformidad con el canon visual.
*   **Mapeo de los 6 Estados**: Conversión sistemática de las lecturas físicas en los seis estados oficiales del dato (`LIVE`, `STALE`, `STATIC`, `SIMULATED`, `NO_DATA` y `ERROR`), activando el estado de advertencia `STALE` si el sensor excede los 30 segundos sin refresco de datos en caliente.

### Capa Gold (El Sistema del Orbe, Red Cifrada y Zona Sagrada)
*   **El Altar del Hero Status Orb**: El componente circular central se configura como el indicador permanente de telemetría inmaculada. Compose bloquea físicamente la colocación de cualquier elemento clickable o widget dentro del **Centro Sagrado** (40% central) y el **30% superior derecho** de la cabecera (destinado a la visualización del cobre físico).
*   **Límites de Seguridad (Lamp Thermal)**: Si el sensor térmico honesto Ryzen (`k10temp`) reporta temperaturas del metal superiores a 80°C, el motor gráfico interrumpe la simulación atmosférica y activa de forma forzosa la alerta visual de parpadeo ámbar.
*   **Amarrado de Red Cifrada**: Todos los descriptores de sockets, WebSockets y consumo de APIs de datos del dashboard CMP se amarran de forma exclusiva a las interfaces de red privadas cifradas de **Tailscale o Yggdrasil**. El renderizador bloquea la interfaz si no se establece una conexión mediante túneles HTTPS con TLS 1.3 de autenticación mutua (mTLS) validados en el arranque por el script de la Constitución.

---

## Notas de Auditoría Medallion
La estructura de persistencia propuesta (~/.aurelius-p0x/db/) no existe en el sistema original. Es especificación de diseño, no estado verificado en el terreno del nodo Beato.

--------------------------------------------------------------------------------

METADATOS MEDALLION:
*  Tipo: REEMPLAZO_ORIGINAL
*  Archivo que sustituye: medallon-dashboards.md
*  Versión: 1.0-Medallion
*  Fuentes base: medallon-dashboards.md, capas-aurelius-jardin.md, especificacion-cmp-multidispositivo.md, FASE 2 REVISADA: APROBADA ✅, inventario-necropolis-v2.md, p0x-master-manifest-merge-v2.txt
*  Conflictos resueltos: Incorporación de la nota de auditoría de inconsistencia de la ruta de base de datos relacional unificada en producción Beato sin alterar la especificación arquitectónica del sistema original.
*  Ambigüedades pendientes: NINGUNA
*  Descartes principales: NINGUNO
*  Notas de auditoría: Se detectó en el censo Beato que la ruta ~/.aurelius-p0x/db/ no existe en el sistema activo, manteniéndose en esta versión como referencia de diseño histórica documentada.

--------------------------------------------------------------------------------

<<< FIN DOCUMENTO: medallon-dashboards-v2.md >>>