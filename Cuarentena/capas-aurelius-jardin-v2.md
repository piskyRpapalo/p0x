# ARQUITECTURA DE TRES CAPAS · AURELIUS Y HEXELION/JARDÍN
## DOCUMENTO DE DISEÑO SOBERANO · p0x

---

## 1. INTRODUCCIÓN A LA ARQUITECTURA MEDALLÓN EN p0x
La arquitectura de datos de p0x se asienta sobre un modelo jerárquico inmutable y desacoplado inspirado en la arquitectura Medallón. Su fin es mitigar el desgaste físico de escritura (Write Wear) de las tarjetas SD, eMMC y unidades de almacenamiento de los nodos edge, garantizando a la vez la inmutabilidad de la memoria cognitiva, la telemetría física de radiofrecuencia y los sensores del entorno local.

---

## 2. LAS TRES CAPAS DE AURELIUS CORE (MEMORIA VIVA)
Aurelius Core estructura su base de datos local y su diario soberano en tres capas físicas inalterables en disco:

### Capa Bronze: El Log Incremental Inmutable (data/bronze/)
*   **Mecánica**: Almacena las interacciones crudas del chat, logs de ejecución y la telemetría de sensores en caliente mediante un formato JSONL incremental (.jsonl).
*   **Física del Silicio**: El sistema pausa de manera automática la escritura en disco durante las inferencias complejas de Ollama para no asfixiar el bus de E/S ni provocar el ahogamiento térmico del procesador local.
*   **Seguridad**: Los prompts de aislamiento y los diálogos de la sesión se sellan bajo firmas criptográficas en caliente.

### Capa Silver: El Almacén Mensual Consolidado (proposals_YYYY-MM.jsonl)
*   **Mecánica**: Un archivo consolidado mensual donde se procesan y ordenan las propuestas cursadas por línea.
*   **Optimización ARM**: Diseñado para facilitar búsquedas secuenciales y lecturas eficientes por bloques o cursores de 10-20 registros sin saturar la RAM ni abrir múltiples descriptores de archivos, ideal para hardware ARM de bajo consumo.
*   **Modo Cosecha (Harvest Mode)**: Espacio intermedio donde los datos consolidados aguardan la aprobación explícita del operador soberano antes de ingresar a la cadena final de la verdad.

### Capa Gold: El Ledger de la Verdad Firmada (gold_chain.jsonl)
*   **Mecánica**: El registro inmutable de engramas de conocimiento (What, Why, Where, Learned).
*   **Estructura Merkle**: Cada bloque de conocimiento se concatena matemáticamente usando triggers SQLite en C, indexando su hash SHA-256 con el hash del bloque anterior (gold_chain.jsonl).
*   **SQLite Unificada**: La base de datos relacional del sistema (~/.aurelius-p0x/db/aurelius_state.db) opera como un derivado directo de esta cadena inmutable.

---

## 3. LAS TRES CAPAS DE LAS 11 MEDITACIONES (MERGE LABORATORY)
El Proyecto Merge destila el software externo y lo clasifica mediante esta rúbrica de tres capas conceptuales y operativas:

### 3.1. llamacpp (Inferencia en Silicio)
*   **Bronce**: Ejecución en C puro, uso de grafos de computación estáticos (evitando el overhead del despacho dinámico de hilos), optimización SIMD ARM NEON, y carga de pesos GGUF mediante mapeo de memoria virtual (mmap) en disco bajo demanda.
*   **Plata**: Alertas críticas deterministas ante desbordamiento de enteros (CVE-2026-33298, CVE-2026-27940) en el parser de cabeceras GGUF para evitar ejecuciones remotas en el host. Alerta de tráfico plano no cifrado en RPC.
*   **Oro**: Validación obligatoria del hash SHA-256 del modelo .gguf y su firma detached .sig contra sovereign_ed25519.pub antes de levantar el servidor. Degradación de hilos (-t) y desconexión si decae el voltaje solar.

### 3.2. anytype (Identidad Local y P2P)
*   **Bronce**: Protocolo any-sync de topología peer-to-peer pura. Identidad local basada en mnemónicos de 12 palabras, firmas Ed25519 y cifrado simétrico AES-CFB de bloques. Interfaz React 18 con backend Go.
*   **Plata**: Veto técnico absoluto a Electron por consumo ineficiente de RAM (300MB base) e inexistencia de destrucción de andamios pedagógicos. Auditoría de la vulnerabilidad sandbox: false en el proceso principal de Electron.
*   **Oro**: Aurelius absorbe la semilla mnemónica en la Misión M0 para derivar sovereign_ed25519.pub en frío. En la Misión M5 se reemplaza por completo Go y Electron por scripts Python ultraligeros que sincronizan bases de datos SQLite cifradas con AES-CFB mediante enlaces de radio LoRa o WiFi directo.

### 3.3. syncthing (Consenso de Red y Backpressure)
*   **Bronce**: Sincronización P2P compilada estáticamente en Go. Migración de base de datos local a SQLite en modo WAL (journal_mode=WAL) para escrituras concurrentes eficientes. Limitación estricta de CPU (GOMAXPROCS=1) y dilatación del intervalo de re-escaneo para evitar desgaste físico.
*   **Plata**: Auditoría de la clave pública de actualización hardcodeada en el código y el límite de 500MB en el Block Exchange Protocol (BEP).
*   **Oro**: Hexelion hereda el protocolo de descubrimiento local UDP broadcast en el puerto 21027 para auto-registro de sensores en caliente. Sincronización asíncrona delta-sync sobre mTLS (TLS 1.3). Si la red cae, la telemetría se acumula localmente en SQLite y se dosifica en la reconexión para prevenir picos de calor.

### 3.4. automerge (CRDT Columnar)
*   **Bronce**: Núcleo en Rust compilado a WASM. Compresión columnar binaria de disco (estilo Apache Parquet) que colapsa documentos de 700MB de RAM a solo 1.3MB en microcontroladores ARM.
*   **Plata**: Identificación de la vulnerabilidad de envenenamiento de filtros Bloom (Bloom Filter Poisoning) y la seguridad laxa por oscuridad basada en la posesión de un docId plano.
*   **Oro**: La Misión M2 modela la memoria colaborativa de Aurelius en un JSON inmutable bajo Automerge compilado en Rust en local. El gateway de FastAPI intercepta los cambios entrantes de la red, valida la firma criptográfica Ed25519 detached y rechaza la fusión de cualquier cambio no firmado por el operador.

### 3.5. llm (Orquestación CLI en Python)
*   **Bronce**: CLI ligero desarrollado por Simon Willison. Interacciona localmente con Ollama y registra un log incremental inmutable de cada interacción en bases SQLite locales (templates.db y logs.db).
*   **Plata**: Vulnerabilidad ante la falta de cifrado de logs en disco expuestos en texto plano e inexistencia de firmas en prompts (riesgo de inyección indirecta de prompts que comprometa el sistema).
*   **Oro**: Integración del diseño relacional de logs de llm en la base de datos unificada aurelius_state.db (tabla bronze_logs) bajo cifrado local AES-256. Evaluación de scripts de ejecución matemática en entornos sandbox de Linux sin acceso a red.

### 3.6. dump1090 (Adquisición de Radio ADS-B)
*   **Bronce**: Decodificador Mode S escrito por antirez en C99 puro. Adquisición directa de señales de aviación comercial a 1090 MHz mediante buffers circulares estáticos prealocados y acceso DMA, garantizando un consumo inferior al 5% de un hilo de CPU ARM.
*   **Plata**: Detección de la falta de autenticación y cifrado en los puertos TCP crudos 30002/30003, permitiendo la inyección de telemetría aérea falsa de forma remota.
*   **Oro**: Hexelion aislará por completo dump1090 de la red abierta. FastAPI asíncrono actúa como el único intermediario local autorizado que lee el puerto 30003 en loopback (127.0.0.1). Compilación optimizada del daemon de antirez (-O3 -march=native -ffast-math).

### 3.7. immudb (Árboles de Merkle Relacionales)
*   **Bronce**: Almacenamiento seguro, inmutable clave-valor en Go mediante Árboles de Merkle que concatenan hashes de transacciones, ideal para auditorías de integridad fuera de red.
*   **Plata**: El recolector de basura de Go y el cálculo continuo de hashes de immudb provocan picos térmicos severos en arquitecturas ARM, acelerando el desgaste de las eMMC de los nodos edge.
*   **Oro**: Se prohíbe levantar el daemon pesado de immudb. Su principio matemático se inyecta directamente en SQLite (~/.aurelius-p0x/db/aurelius_state.db) mediante un trigger nativo en C sobre la tabla virtual de observaciones, vinculando cada nuevo registro SHA-256 con el anterior. El script verify_pow.sh audita esta consistencia en frío antes de activar la red.

### 3.8. tinypilot (KVM HDMI de Ultra-Bajo Consumo)
*   **Bronce**: KVM remoto sobre IP escrito en Python para Raspberry Pi. Captura física de video HDMI (v4l2) y transmisión de imágenes MJPEG por WebSockets. Interfaz ultraligera pura sin Node.js.
*   **Plata**: Servidor Flask monohilo sin cifrado nativo que bloquea la pila TCP ante ráfagas de video MJPEG e impide la recepción de señales HID.
*   **Oro**: Adopción de la renderización stateless sin frameworks para el panel en Catppuccin Mocha de Hexelion. La comunicación utiliza WebSockets cifrados localmente bajo TLS 1.3 con mTLS. El gateway de FastAPI valida la firma Ed25519 de cada comando físico antes de inyectar las tramas HID en /dev/hidg0.

### 3.9. bettatech (Agentes en Disco y Sintaxis EARS)
*   **Bronce**: Orquestación de agentes con persistencia de estado directamente en disco en vez de RAM volátil.
*   **Plata**: Ausencia de firmas criptográficas en las herramientas auto-registradas e inexistencia de control de presupuesto energético (bucles infinitos de CPU).
*   **Oro**: Aurelius implementa la validación sistemática de herramientas bajo la sintaxis estricta EARS de betta-tech (*WHEN [condición] IF [precondición] THE [sistema] SHALL [acción]*) para erradicar las alucinaciones de diseño. Los comandos propuestos por el agente exigen la pulsación física de Ctrl+C sobre el Portapapeles Soberano para su ejecución manual.

### 3.10. gentlemanprogramming (Engrams en SQLite FTS5)
*   **Bronce**: Unidades atómicas de aprendizaje ("engrams") estructuradas rígidamente en cuatro campos (*What, Why, Where, Learned*) y persistidas en tablas de búsqueda rápida SQLite FTS5.
*   **Plata**: Dependencia de frameworks monolíticos de TypeScript y JS en el renderizado de engramas, junto con la falta de validación de integridad en caliente.
*   **Oro**: La base relacional de Aurelius hereda este diseño en la tabla virtual fts_observations usando FTS5 local. Cada registro requiere la firma digital Ed25519 del operador soberano en el arranque diario antes de marcarse como VALIDATED en la interfaz.

### 3.11. platzi (Sistemas Fragmentados y Retiro de Andamios)
*   **Bronce**: Descomposición de la ruta de aprendizaje en misiones formativas autocontenidas para garantizar que los fallos locales de un sensor o microcontrolador no comprometan el entorno general.
*   **Plata**: Mantener dependencias de andamiaje pedagógico y plantillas de desarrollo activas indefinidamente en la interfaz, adormeciendo la competencia del usuario.
*   **Oro**: Aurelius ejecuta de forma estricta la rutina **Scaffolding Faded** en su núcleo (Misión M7). Al firmar el éxito de una misión actual, verify_pow.sh comprime los andamios formativos y ejemplos en un archivo ~/.aurelius-p0x/archive/ y los borra físicamente del espacio de desarrollo, consolidando el silicio y forzando la autonomía técnica individual.

---

## Notas de Auditoría Medallion
La carpeta ~/.aurelius-p0x/ no existe en el nodo medido. Es una ruta propuesta en el diseño original, no verificada en el terreno del nodo Beato.

--------------------------------------------------------------------------------

METADATOS MEDALLION:
*  Tipo: REEMPLAZO_ORIGINAL
*  Archivo que sustituye: capas-aurelius-jardin.md
*  Versión: 1.0-Medallion
*  Fuentes base: capas-aurelius-jardin.md, FASE 2 REVISADA: APROBADA ✅, inventario-necropolis-v2.md, medallon-dashboards.md, p0x-master-manifest-merge-v2.txt
*  Conflictos resueltos: Incorporación de la nota de auditoría de inconsistencia de la ruta ~/.aurelius-p0x/ en producción Beato sin alterar la especificación arquitectónica del sistema original.
*  Ambigüedades pendientes: NINGUNA
*  Descartes principales: NINGUNO
*  Notas de auditoría: Se detectó en el censo Beato que la ruta ~/.aurelius-p0x/ no existe en el sistema activo, manteniéndose en esta versión como referencia de diseño histórica documentada.

--------------------------------------------------------------------------------