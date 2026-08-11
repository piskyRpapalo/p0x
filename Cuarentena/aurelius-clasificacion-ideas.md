# CLASIFICACIÓN COGNITIVA Y EVALUACIÓN ESTRATÉGICA DE IDEAS (aurelius-clasificacion-ideas.md)

Este documento estructura, evalúa y clasifica de manera determinista todas las habilidades, ideas y funcionalidades del sistema Aurelius y p0x documentadas en la base de conocimientos. La clasificación divide el espectro técnico en cuatro categorías discretas atendiendo a la viabilidad física del silicio, madurez del software local, dependencias de red de terceros y coherencia doctrinal.

---

## 1. TABLA RESUMEN DE CLASIFICACIÓN ESTRATÉGICA

| Nombre de Idea / Skill / Funcionalidad | Categoría | Justificación Técnica (1 línea) |
| :--- | :--- | :--- |
| **B.01: Perfiles de Configuración** | `[IMPLEMENTABLE AHORA]` | Parámetro de línea de comandos (CLI) que asigna límites de escucha y recursos sin código dinámico. |
| **B.02: Declaración Honesta del Motor** | `[IMPLEMENTABLE AHORA]` | Consulta determinista a /api/tags de Ollama con mapeo de red mediante parseo de URL local. |
| **B.03: Capabilities API** | `[IMPLEMENTABLE AHORA]` | Endpoint REST estructurado con psutil para declarar las habilidades disponibles en la UI. |
| **B.04: Honest Math (Evaluación AST)** | `[IMPLEMENTABLE AHORA]` | Evaluador matemático basado en Abstract Syntax Tree en Python puro con whitelist estricta de nodos. |
| **B.05: Portapapeles Soberano** | `[IMPLEMENTABLE AHORA]` | Fricción física nativa en CSS/HTML que anula la copia automática y fuerza selección manual. |
| **B.06: Command Guard** | `[IMPLEMENTABLE AHORA]` | Parser determinista sin LLM (regex + blacklist fija) que envuelve bloques de código bash peligrosos. |
| **B.07: Centinela de Hardware** | `[IMPLEMENTABLE AHORA]` | Monitoreo ligero cada 5s de /sys/class/thermal con propuesta de comandos y descarga VRAM. |
| **B.08: Caché de Embeddings** | `[IMPLEMENTABLE AHORA]` | Almacén plano JSONL append-only indexado por hash SHA-256 para evitar duplicar cálculos. |
| **B.09: Ingesta Pasiva (Snippets)** | `[IMPLEMENTABLE AHORA]` | Guardado granular en texto plano de fragmentos pegados sin llamadas a APIs ni procesamiento visual. |
| **B.10: Scaffolding Fading (Frontera de Prompt)** | `[IMPLEMENTABLE AHORA]` | Ajuste de variable contextual de prompt según nivel de misiones (M0-M7) superadas en Gold. |
| **B.11: Espejo de Sócrates** | `[IMPLEMENTABLE AHORA]` | Máquina socrática de chat limitada a 5 preguntas de control con parser O(N) de diversidad léxica. |
| **B.12: Contrato de Silencio (Focus Pact)** | `[IMPLEMENTABLE AHORA]` | Registro pasivo en log Bronze de modificaciones de archivos mediante os.listdir recurrente. |
| **B.13: Senda de los Muertos** | `[IMPLEMENTABLE AHORA]` | Archivo de logs append-only (dead_path.jsonl) que contabiliza y reporta patrones de rechazo. |
| **B.14: Diccionario del Soberano** | `[IMPLEMENTABLE AHORA]` | Extractor regex de preguntas definitorias en chat que exporta Markdown con hashes de origen. |
| **B.15: Simulación de Catástrofe** | `[IMPLEMENTABLE AHORA]` | Árbol de decisiones determinista en Python puro contra acertijos de infraestructura de red local. |
| **B.16: Juez de Arquitectura AST** | `[IMPLEMENTABLE AHORA]` | Análisis estático de importaciones circulares en Python utilizando el módulo nativo ast. |
| **B.17: Espejo de Paneles (tmxu RAM)** | `[IMPLEMENTABLE AHORA]` | Calculadora fija que mide consumo de hilos Python antes de multiplexar terminales con tmux. |
| **B.18: Detector de Code Smell AST** | `[IMPLEMENTABLE AHORA]` | Contador de métricas estáticas de longitud, anidamiento y parámetros sobre parseo AST en C/Python. |
| **B.19: Tesoro de Sesiones tmux** | `[IMPLEMENTABLE AHORA]` | Validador determinista de secuencias de comandos de restauración de terminal contra rúbrica fija. |
| **B.20: Balance de Carga Mental** | `[IMPLEMENTABLE AHORA]` | Tokenizador básico O(N) que mide el solapamiento de palabras clave en perfiles de agentes. |
| **B.21: Forja de Scripting tmux** | `[IMPLEMENTABLE AHORA]` | Validador regex estructurado que evalúa sintaxis de scripts de inicialización tmux sin ejecutarlos. |
| **B.22: Templo del Embudo** | `[IMPLEMENTABLE AHORA]` | Calculadora estática de throughput basada en el conteo de operaciones IO de código analizado. |
| **B.23: Constitución en Capas** | `[IMPLEMENTABLE AHORA]` | Ensamblador de prompts que unifica archivos .prompt en constitution/ sin lógica ejecutable. |
| **B.24: Sesión Persistente (tmux)** | `[IMPLEMENTABLE AHORA]` | Serialización JSON del estado de terminal y layouts de paneles activos en el archivo session_state.jsonl. |
| **B.25: Multiplexor de Misiones** | `[IMPLEMENTABLE AHORA]` | Interfaz CSS Grid de paneles independientes sincronizada localmente por eventos de directorio. |
| **B.26: Modo Templo** | `[IMPLEMENTABLE AHORA]` | Desactivación de escrituras Gold y aislamiento de inferencia al detectar endpoints HTTP de terceros. |
| **B.27: Aislamiento de Prompt Injection** | `[IMPLEMENTABLE AHORA]` | Restricción total de copiado e hiper-fricción manual al operar con motores externos (Huésped). |
| **Remediación Térmica Ryzen** | `[IMPLEMENTABLE AHORA]` | Desvío dinámico del sensor thermal_zone0 inactivo hacia el bus k10temp real en hwmon3. |
| **Remediación Sínodo de Agentes** | `[IMPLEMENTABLE AHORA]` | Ajuste de denominador de agentes n/5 o despliegue de servicio minimalista de enlace en local. |
| **Remediación Heartbeat Redis** | `[IMPLEMENTABLE AHORA]` | Configuración de TTL de 60s en redis.set para evitar la retención indefinida de estados stale. |
| **Remediación Cola FIFO SQLite** | `[IMPLEMENTABLE AHORA]` | Fallback determinista de cola de trabajos por lotes ante la ausencia física de task-spooler. |
| **P.01: Centinela como Laboratorio** | `[HORIZONTE TECNOLÓGICO]` | Requiere interactuar con controladores de frecuencia de la CPU del SO para medir thermal throttling. |
| **P.02: Escriba de Documentación** | `[HORIZONTE TECNOLÓGICO]` | Requiere un generador asíncronamente integrado con Jinja2 que analice logs secuenciales de Bronze. |
| **P.03: Biblioteca Soberana** | `[HORIZONTE TECNOLÓGICO]` | Exige compilación local de la biblioteca faiss-cpu y modelado local de chunks con nomic-embed-text. |
| **P.04: Modo Meditaciones** | `[HORIZONTE TECNOLÓGICO]` | Editor de texto con comparador semántico vectorial contra propósitos maestros en la base Gold. |
| **P.05: Brújula Estoica** | `[HORIZONTE TECNOLÓGICO]` | Análisis periódico de divergencia temática entre logs de Bronze y declaraciones inmutables de Gold. |
| **P.06: Dynamic System Prompt** | `[HORIZONTE TECNOLÓGICO]` | Motor de compilación que lee el historial de Gold para ajustar dinámicamente el discurso del Preceptor. |
| **P.07: Reconciliación en Arranque** | `[HORIZONTE TECNOLÓGICO]` | Comparador de hashes de base de datos relacional contra el índice FAISS para auto-curación. |
| **P.08: La Forja (Evaluación Dual)** | `[HORIZONTE TECNOLÓGICO]` | Validación asíncrona de ritos basada en cosine similarity local, validaciones Ed25519 y entropía O(N). |
| **P.09: Semillero / Invernadero** | `[HORIZONTE TECNOLÓGICO]` | Sistema de herencia que desbloquea misiones avanzadas tras descifrar e importar PoK locales. |
| **P.12: Laboratorio de Entropía Humana** | `[HORIZONTE TECNOLÓGICO]` | Mapeo de fatiga cognitiva mediante series temporales del ratio de entropía en logs de Bronze. |
| **P.13: Sintonía Externa** | `[HORIZONTE TECNOLÓGICO]` | Generador de acertijos y rúbricas locales a partir de la ingesta de temarios en texto plano. |
| **P.14: Arquitecto de Rutas** | `[HORIZONTE TECNOLÓGICO]` | Contrato de carrera que confronta semanalmente syllabus sellados contra logs analizados. |
| **P.15: Auditor de Proyectos** | `[HORIZONTE TECNOLÓGICO]` | Clonado asíncrono local de repositorios de software GitHub y escaneo estático contra B.16 y B.18. |
| **P.16: El Enjambre Soberano** | `[HORIZONTE TECNOLÓGICO]` | Coordinación asíncrona secuencial de agentes locales con firmas físicas y handoffs explícitos. |
| **P.17: Worktrees del Pensamiento** | `[HORIZONTE TECNOLÓGICO]` | Aislamiento de contextos por carpetas físicas de Bronze/Gold con lógica nativa de clonado y fusión. |
| **P.18: El Camino Platzi** | `[HORIZONTE TECNOLÓGICO]` | Generador determinista de secuencias de misiones estructuradas basadas en parsers de Markdown. |
| **O.03: Aurelius Thin Client** | `[HORIZONTE TECNOLÓGICO]` | Redirección de inferencia hacia nodos autorizados del usuario sobre mTLS 1.3 de Tailscale. |
| **O.04: Hot-Start de Contexto** | `[HORIZONTE TECNOLÓGICO]` | Serialización y envío de contextos de conversación mediante llamadas de red privadas cifradas. |
| **O.05: Portabilidad Soberana Cifrada** | `[HORIZONTE TECNOLÓGICO]` | Compilación de scripts de cifrado AES-256-GCM con PBKDF2 y fragmentación en códigos QR. |
| **O.06: Sello Diferido (Prueba de Tiempo)**| `[HORIZONTE TECNOLÓGICO]` | Cifrado AES-256-GCM usando hashes futuros de la cadena Gold como claves criptográficas físicas. |
| **O.01: PoK Verificable como Notaría** | `[DEPIN]` | Emisión y validación criptográfica P2P asíncrona de reclamos asimétricos entre nodos sin red central. |
| **O.02: Verificación de Math de la Mesh** | `[DEPIN]` | Arbitraje y auditoría matemática determinista cruzada de telemetría de recursos de red. |
| **O.07: Honest Math como Notario de SLAs**| `[DEPIN]` | Prevención distribuida de ataques Sybil y verificación de recursos mediante auditoría matemática. |
| **O.08: Templo como Municipio** | `[DEPIN]` | Cerco estricto e hiper-fricción en red de enjambres federados con restricciones deterministas. |
| **O.09: Calibración Federada** | `[DEPIN]` | Agregación anónima distribuida de perfiles numéricos de temperatura y CPU de la red. |
| **O.10: Portfolio Exportable Verificable** | `[DEPIN]` | Notaría distribuida y generación de estáticos HTML verificables mediante hashes públicos. |
| **Marco Neón Cian de Celdas** | `[ARQUEOLOGÍA]` | Descartado en Blueprint v1.3 por competir visualmente con el contraste de los datos. |
| **Fondo Negro Plano de Le Jardin** | `[ARQUEOLOGÍA]` | Descartado en Blueprint v1.3 por ser estéticamente opaco; reemplazado por madera y pergamino. |
| **Sopa de Etiquetas del Second Brain** | `[ARQUEOLOGÍA]` | Descartado en Blueprint v1.3 por provocar sobreposición ilegible; reemplazado por Ley LOD. |
| **Barras de Progreso del Sínodo** | `[ARQUEOLOGÍA]` | Descartadas en Blueprint v1.3 por su ambigüedad; reemplazadas por chips con métricas reales. |
| **Miniatura de Cámara en el Header** | `[ARQUEOLOGÍA]` | Descartada en Blueprint v1.3 para mantener header libre de media; realojada en celda OBSERVE. |
| **localStorage como Única Memoria** | `[ARQUEOLOGÍA]` | Descartado en Blueprint v1.3 para evitar alojar datos del diario en el cliente; migrado a rack local. |
| **Grilla Multicolumna de L'Herbier** | `[ARQUEOLOGÍA]` | Descartada en Blueprint v1.3 para evitar re-maquetaciones; reemplazada por tira horizontal. |
| **Misiones No Lineales M0-M48** | `[ARQUEOLOGÍA]` | Descartadas en Catalogo/Manifest para simplificar; reemplazadas por secuencia M0-M7. |
| **Uso de Daemon immudb** | `[ARQUEOLOGÍA]` | Descartado en Necrópolis v2 por picos térmicos en ARM; reemplazado por trigger local SQLite. |
| **Servidor Flask Monohilo** | `[ARQUEOLOGÍA]` | Descartado en Necrópolis v2 por falta de mTLS y bloqueos; reemplazado por FastAPI + WebSockets. |
| **Puertos TCP Crudos de dump1090** | `[ARQUEOLOGÍA]` | Descartados en Necrópolis v2 por falta de cifrado e inyecciones; aislados a loopback local. |
| **thermal_zone0 en Beelink Ryzen** | `[ARQUEOLOGÍA]` | Descartado en Silver-v2 por ser inactivo (20°C fijos); mapeado a k10temp en hwmon3. |

---

## 2. ANÁLISIS DETALLADO Y JUSTIFICACIÓN EXPANDIDA

### 2.1. Categoria: `[IMPLEMENTABLE AHORA]`
Esta categoría comprende funcionalidades que no requieren dependencias externas de red, APIs propietarias ni librerías de infraestructura pesada. Pueden desarrollarse en Python estricto, SQLite local y HTML/JS plano en un plazo inferior a 2 semanas:

*   **B.01: Perfiles de Configuración (Pro/Lite)**: Estructuración simple de arranque mediante parser nativo de argumentos de CLI. La distinción del puerto de escucha y recursos asignados se asienta de manera síncrona en archivos JSON que no se versionan, permitiendo la portabilidad inmediata del nodo LITE.
*   **B.02: Declaración Honesta del Motor**: Petición de bajo nivel `GET` al socket `/api/tags` de Ollama. No asume estados; si el socket no responde, declara deterministamente `NO DATA` en la interfaz. El parser determina si el motor es Soberano, Delegado o Huésped analizando el host de la URL configurada.
*   **B.04: Honest Math (Evaluación AST)**: El sistema anula de raíz la ejecución de código generado por IA. En su lugar, el intérprete Python procesa las operaciones matemáticas críticas a través de un analizador del árbol de sintaxis abstracta (`ast.parse`), comparando cada nodo contra una estricta lista blanca que veta funciones, llamadas, atributos e indexación para bloquear cualquier inyección de código.
*   **B.06: Command Guard (Firewall Cognitivo)**: Implementación de expresiones regulares optimizadas y arrays estáticos de patrones en el backend. Los comandos propuestos por el modelo se interceptan y evalúan antes del renderizado de la UI; si se detectan cadenas de riesgo (rm -rf, sudo), se inyecta un envoltorio visual rojo de peligro, delegando en el humano la decisión física de copiado.
*   **B.07: Centinela de Hardware (Telemetry Guard)**: Demonio ligero que interroga periódicamente la API de `psutil` y lee directamente el fichero del sensor real k10temp en el Soberano. Proyecta advertencias lógicas e instrucciones de mitigación térmica (como señales de parada de hilos) sin ejecutarlas autónomamente, preservando el principio doctrinal de *IronClaw*.
*   **B.08: Caché de Embeddings**: Almacén JSONL plano append-only. El backend calcula el hash SHA-256 de los bloques de texto normalizados y busca su existencia antes de convocar al modelo local, previniendo el overhead y calentamiento innecesario del procesador local en lecturas repetidas de engramas.
*   **Remediación Térmica Ryzen (Filtro H2)**: Corrección crítica del censo. El Beelink SER9 Soberano desecha la lectura de `thermal_zone0` (la cual devolvía de forma deshonesta 20°C constantes debido al driver ACPI genérico) y mapea dinámicamente el bus físico del AMD Ryzen leyendo el driver honesto `k10temp` expuesto en `/sys/class/hwmon/hwmon3/temp1_input`.
*   **Remediación Cola FIFO SQLite (Filtro H6)**: Ante la ausencia de la utilidad `task-spooler` (tsp) en el Soberano medido, se implementa un fallback determinista que conmuta las tareas pesadas por lotes a una cola local basada en transacciones relacionales SQLite, garantizando la persistencia ordenada sin dependencias de sistema.

---

### 2.2. Categoria: `[HORIZONTE TECNOLÓGICO]`
Funcionalidades que se encuentran en el roadmap del sistema pero cuya implementación inmediata está bloqueada por la necesidad de maduración del backend, requerimientos avanzados de hardware (VRAM/RAM) o el desarrollo previo de módulos de persistencia criptográfica en Gold que exceden un sprint de 2 semanas:

*   **P.03: Biblioteca Soberana (RAG Local)**: Requiere la compilación nativa en el nodo Soberano de la extensión `faiss-cpu` y la inyección síncrona del modelo de embeddings `nomic-embed-text` a través de Ollama. Exige la estructuración previa del troceado (chunking) y la interfaz de aprobación en el Modo Cosecha.
*   **P.05: Brújula Estoica (Goal Tracking)**: Requiere que la base de datos Gold cuente con el histórico consolidado de propósitos firmados del usuario (Misión M0). Requiere un algoritmo periódico de análisis semántico (similitud del coseno local de series temporales) para evaluar los logs de la capa Bronze contra las directivas Gold sin fugar datos a red.
*   **P.08: La Forja (Evaluación Dual)**: Es el rito de paso asíncrono para el ascenso de nivel (M0-M7). Su desarrollo exige integrar tres subsistemas concurrentes: la validación semántica local mediante similitud de coseno, la heurística O(N) de diversidad léxica para textos blandos (entropía de Shannon en arrays de tokens), y la firma digital asimétrica detached del nodo utilizando curvas elípticas Ed25519 de la librería Python `cryptography`.
*   **P.16: Camino 33 · El Enjambre Soberano**: Modela la colaboración multi-agente en local de forma secuencial para no saturar la memoria RAM. Exige una arquitectura robusta de buffers e hilos de handoff en FastAPI donde el operador humano firme digitalmente cada transición de datos de un rol al siguiente antes de su paso por consola.
*   **P.17: Camino 35 · Los Worktrees del Pensamiento**: Requiere un sistema jerárquico de control de directorios en disco que clone, aísle y fusione ficheros JSONL e índices FAISS según la sesión activa, manteniendo la identidad común de la clave pública maestra derivada del Totem.
*   **O.05: Portabilidad Soberana con Transferencia Cifrada**: Script para empaquetar de forma segura la base de datos Gold en caliente. Requiere el uso de cifrado AES-256-GCM y derivación de clave mediante PBKDF2 basada en frases de recuperación humanas, con capacidad opcional de fragmentarse en flujos de datos QR de alta densidad para transferencia física air-gapped.
*   **O.06: Camino 28 · La Prueba del Tiempo (Sello Diferido)**: Requiere cifrado con candado de tiempo criptográfico. En lugar de confiar en el reloj del sistema (el cual es vulnerable a manipulaciones del operador local), la clave de descifrado se deriva del hash futuro del ledger Gold. El contenido es ilegible hasta que la base de datos Gold ha crecido la cantidad de bloques equivalentes a la duración del sello.

---

### 2.3. Categoria: `[DEPIN]`
Esta categoría agrupa las especificaciones de la Mesh Soberana y los mecanismos de enjambre federado cuya viabilidad técnica depende de la implementación completa de la red privada virtual cifrada (Tailscale/Yggdrasil), protocolos de descubrimiento P2P descentralizados de par a par y la reputación compartida sin autoridades centrales de certificación:

*   **O.01: PoK Verificable como Notaría de Conocimiento**: El sistema emite credenciales portables firmadas con Ed25519 que certifican el nivel del usuario. Exige la distribución y asimilación asíncrona de las firmas por parte de otros nodos de la Mesh mediante endpoints de validación cruzada (/api/pok/verify), confirmando la veracidad de la prueba sin fugar el contenido del diario del soberano.
*   **O.02: Honest Math como Protocolo de Verificación Cruzada de la Mesh**: Los nodos de la subred privada auditan deterministicamente los reportes de recursos de sus pares. Exige levantar canales de consulta asíncronos que ejecutan expresiones matemáticas de throughput y consumo a través del evaluador AST de Honest Math, aislando y marcando de inmediato a los nodos que alucinan o falsifican telemetría de hardware.
*   **O.07: Honest Math como Notario de SLAs**: Validación de "Contratos de Acuerdo" entre nodos que comparten cómputo en la red Mesh. El nodo receptor entrega el resultado de la inferencia y un PoK detallado del consumo de VRAM y tiempos de CPU. El nodo emisor evalúa la validez de los números empleando su calculadora Honest Math local, acumulando reputación por par y previniendo ataques Sybil de recursos en la topología P2P.
*   **O.09: Calibración Federada de Hardware (Mesh Telemetry 2.0)**: Agregación estadística y anónima de las predicciones de thermal throttling de los centinelas locales de la red. Requiere un protocolo de descubrimiento y agregación por lotes libre de red central que compile los pares numéricos (temperatura de APU vs. segundos hasta throttling) y retorne advertencias calibradas basadas en la experiencia agregada de la red.

---

### 2.4. Categoria: `[ARQUEOLOGÍA]`
Representa el catálogo de ideas de visualización, andamiajes pedagógicos y tecnologías que han sido descartadas sistemáticamente durante el desarrollo y censo de p0x por atentar contra la doctrina, presentar vulnerabilidades de red, saturar el silicio, o ser andamios pedagógicos retirados tras las auditorías visuales:

*   **Marco Neón Cian de las Celdas (Blueprint v1.3)**: Descartado por el David por competir visualmente con el contraste de las telemetrías reales y consumir ciclos de pantalla innecesarios. Reemplazado por borde de 1px perimetral de contraste con glow reservado exclusivamente a cifras vivas.
*   **Fondo Negro Plano de la Mesa en Le Jardin (Blueprint v1.3)**: Vetado por el soberano por considerarlo "poco agraciado" y frío. Reemplazado por madera clara y pergamino generados mediante CSS vanilla de gradientes lineales, eliminando el coste de cargar imágenes de textura pesadas en la RAM.
*   **Sopa de Etiquetas en el Second Brain (Blueprint v1.3)**: La acumulación de títulos de engramas convertía el grafo en un elemento de ruido ilegible. Reemplazado por la Ley de Detalle por Zoom (LOD), donde los nombres de los nodos solo se renderizan según el grado de conectividad y el nivel de zoom físico de la pantalla.
*   **Barras de Progreso Lineales de Agentes (Blueprint v1.3)**: Descartadas por ser imprecisas e inducir a error conceptual. Reemplazadas por chips de bus con métrica única y real que reportan frescura del feed.
*   **localStorage como Persistencia Única (Blueprint v1.3)**: El preceptor vetó de forma absoluta el uso del navegador del cliente como almacén persistente de las notas de Le Jardin. Reemplazado por llamadas asíncronas HTTP POST al disco del nodo de red, reduciendo `localStorage` a un buffer temporal offline de contingencia con reconciliación automática al arranque.
*   **Grilla Multicolumna Estática o 4x4/6x6 de L'Herbier (Blueprint v1.3)**: Descartada para evitar re-maquetaciones de interfaz cada vez que se escala el grimorio botánico. Reemplazada por una tira horizontal scrollable con snaps de vista adaptativa.
*   **Uso del Daemon immudb (Necrópolis v2)**: Vetado por atentar contra la integridad térmica. Su colector de basura en Go y el cálculo continuo de hashes Merkle sobrecargaban de forma extrema los procesadores ARM de bajo consumo. Reemplazado por la inyección matemática de los árboles de Merkle dentro de la SQLite local utilizando triggers nativos en C.
*   **Servidores Flask Monohilo y Puertos TCP Abiertos 30002/30003 de dump1090 (Necrópolis v2)**: Eliminados por carecer de autenticación mutua, cifrado y firmas criptográficas, exponiendo los dongles SDR a inyecciones remotas de aeronaves y barcos falsos. Reemplazados por el aislamiento estricto de dump1090 de la red LAN y canalizando la telemetría aérea asíncronamente en loopback por FastAPI local.
*   **Uso de `thermal_zone0` como sensor de CPU para el Ryzen (Silver-v2)**: El uso de `thermal_zone0` en el Beelink Ryzen del Soberano devolvía de forma deshonesta 20°C fijos constantes correspondientes al driver ACPI genérico del SO. Reemplazado por la lectura real del bus `k10temp` expuesto en `hwmon3/temp1_input`.

---

## 3. NOTAS DE AUDITORÍA MEDALLION

La taxonomía y el catálogo de habilidades consolidado en este documento mapean de forma honesta el estado tecnológico del nodo. La clasificación de las skills de TMUX (B.17, B.19, B.21, B.24, B.25) y los parsers de código basados en AST (B.16, B.18, B.22) se consideran implementables ahora por operar sobre la stdlib de Python y el motor nativo de SQLite WAL del sistema original. El desarrollo del sistema paralelo en ~/p0x-soberano/ preservará el aislamiento total de estas capas.

--------------------------------------------------------------------------------

METADATOS MEDALLION:
*  Tipo: CONSOLIDACION
*  Archivo que sustituye: NINGUNO
*  Versión: 1.0-Medallion
*  Fuentes base: CATÁLOGO COMPLETO DE SKILLS AURELIUS, FASE 2 REVISADA: APROBADA ✅, inventario-necropolis-v2.md, aurelius_pendiente_silver-v2.txt, p0x-master-manifest-merge-v3.txt, blueprint-de-diseno-soberano-v1.4.md, medallon-dashboards-v2.md, alternativas-filosofia.md, aurelius_estado_bronze.txt, aurelius_nuevas_skills_gold.txt
*  Conflictos resueltos: Consolidación y desduplicación de todo el catálogo de habilidades de Aurelius (Rondas 1 a 4) bajo cuatro taxonomías unívocas y libres de metáforas. Se resuelve el direccionamiento térmico honesto del sensor del Soberano integrando los hallazgos del censo F0 de Beato.
*  Ambigüedades pendientes: NINGUNA
*  Descartes principales: Se descarta cualquier automatización del portapapeles y se desecha de forma irrevocable el uso del sensor thermal_zone0 para telemetría de APU Ryzen en Beato, catalogándolo formalmente en la Necrópolis/Arqueología de silicio.
*  Notas de auditoría: NINGUNA

--------------------------------------------------------------------------------

<<< FIN DOCUMENTO: aurelius-clasificacion-ideas.md >>>