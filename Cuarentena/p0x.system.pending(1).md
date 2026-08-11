# 🏛️ SPECIFICATION MASTER FILE: p0x.system.pending
**SYSTEM_METADATA:**
*   **Namespace:**  p0x.system.pending
*   **Version:**  2.1-Deudas-Senda-API
*   **Status:**  Active Backlog, Historical Necropolis & CineK Taller Roadmap
*   **Date:**  2026-08-08
*   **Editor:**  AI Redactora Experta en Lenguaje AI (G.R.I.D. Protocol)
*   **Classification:**  Technical Debt, Senda de los Muertos & Active Architectural Roadmap

---

#### 🥉 CAPA BRONCE (LA SENDA DE LOS MUERTOS - ARQUEOLOGÍA VISUAL Y VETOS TÉCNICOS)
Aquí yacen los elementos de diseño, interfaces y decisiones de arquitectura descartados de forma sistemática para proteger la CPU del nodo, resguardar la privacidad local y cumplir el canon visual brutalista soberano:

##### 1. Elementos Visuales Enterrados (Necrópolis Visual)
*   **Luna del Cielo en Le Jardin**: Eliminada por desentonar con el propósito rústico e íntimo del huerto. Se aplica `display: none` incondicional en los contenedores de CSS.
*   **Bolas Violetas Flotantes en El Muro**: Descartadas por toscas e intrusivas en el espacio de aire del arte de fondo.
*   **Marco de Neón Cian de las Celdas**: Retirado del Nexo por competir con el contraste y nitidez de los datos de telemetría numéricos reales.
*   **Barras de Progreso Lineales de los Agentes**: Reemplazadas en el Sínodo por chips compactos con métricas numéricas y textuales reales de estado del bus.
*   **Sopa de Etiquetas sin L.O.D. en el Second Brain**: La superposición indiscriminada saturaba la pantalla del operador. Sustituida por la Ley de Detalle por Zoom (LOD).
*   **Grilla Multicolumna Estática o 4x4 de L'Herbier**: Provocaba saltos de layout al poblarse. Reemplazada por un slider horizontal con snaps adaptativos.

##### 2. Decisiones Técnicas Vetadas (Protección de Silicio y Privacidad)
*   **`localStorage` como Almacén Único en Le Cahier**: Vetado por el preceptor por razones de privacidad y persistencia débil en el cliente. Sustituido por llamadas síncronas HTTP POST al disco del rack (`diary_sealed/`).
*   **Glassmorphism (`Modifier.blur()` / Haze)**: Prohibido de forma absoluta en los widgets y Compose UI. Con una CPU Ryzen pura sin dGPU de alta VRAM en el nodo doméstico, repintar convoluciones gaussianas a 60 fps satura e incrementa la temperatura del silicio.
*   **Daemon de Base immudb**: Vetado por sobrecarga térmica extrema en ARM de bajo consumo debido a su recolector de basura en Go. Reemplazado por triggers nativos en C dentro de SQLite.
*   **Puertos TCP Abiertos de dump1090 (30002/30003)**: Eliminados de la LAN física para evitar inyección de aeronaves falsas en el espacio aéreo del Vigía. Confinados estrictamente a loopback (`127.0.0.1`) mediante nftables.
*   **Polling de Red para Interfaz**: Vetado por ineficiencia de red y sobrecarga de procesamiento en los clientes. Sustituido de manera definitiva por arquitectura orientada a Server-Sent Events (SSE).

---

#### 🥈 CAPA PLATA (DEUDA TÉCNICA ACTIVA & SUTURA DE HARDWARE)
Este ledger registra los incidentes y desconexiones físicas identificados en Beato, junto con el búfer activo de inconsistencias de la base de conocimientos para la IA auditora:

##### 1. Registro de Incidentes Pendientes en Beato
*   **M5Stack Serie-Redis / Vigía**: El puente serie del Vigía reporta fallos aleatorios de lectura física. Se exige implementar el fallback de sensor ausente ("— · capteur à venir") con un timestamp del último avistamiento (`last_seen`).
*   **Agente Enlace**: El microservicio huerfano no existe físicamente en el disco de producción, rompiendo el ratio de Sínodo $n/6$. Se debe aprovisionar un script minimal en Python.
*   **Claves de Pulso en Redis**: Las claves de latido de los agentes en background carecen de tiempo de vida (TTL), impidiendo la detección automatizada de estados caídos (stale). Se exige un TTL estricto de 60 segundos.
*   **Ruta de Aislamiento Base**: Varios scripts históricos asumen de forma incorrecta la ruta `~/.aurelius-p0x/`. El sistema paralelo y sus daemons deben confinarse exclusivamente a la raíz de usuario `~/p0x-soberano/`.

##### 2. Cableado Físico e Integración de Telemetría Real
*   **Sello de Telemetría Solar (Shelly Plus 1PM)**: El decorador `@solo_si_hay_sol` está diseñado pero opera en modo manual/simulado en FastAPI debido a que el cableado lógico para leer el voltaje real de la Solix C1000X no está conectado en producción.
*   **M5Stack (Datos Ambientales)**: Los flujos de temperatura y humedad del Vigía están disponibles por puerto serie, pero permanecen desconectados del pipeline de tareas de CineK.
*   **RTL-SDR (1090 MHz / AIS 162 MHz)**: Operan de fondo de forma estable en sus daemons aislados en loopback, pero están completamente inactivos dentro del pipeline interactivo de El Nexo.

##### 3. Búfer de Refactorizaciones de Especificación (Auditoría IA)
*   **Sincronización de IPs Estáticas**: Referencias a la IP del túnel de Tailscale `[IP_TAILNET_REDACTADA]` y al puerto `8050` deben mantenerse en estricta sincronía entre `p0x.infra.hardware` and `p0x.infra.software`.
*   **Fase 0.5 ComfyUI Workflows**: Las plantillas en `~/cinek_automatico/comfy_workflows/` requieren la edición manual de los checkpoints locales de FLUX/SDXL para evitar que el pipeline se congele en caliente por archivos no encontrados.

---

#### 🥇 CAPA GOLD (HOJA DE RUTA ACTIVA & TRANSICIÓN CINEK TALLER v2.1)
El balance de la Oleada Visual anterior se consolida como completado, abriendo paso a la refactorización síncrona del monolito del pipeline de video hacia una API REST modular:

##### 1. Estado de la Oleada de Producción Visual (Cierre de Fase Anterior)
*   **Compilación Estática de Vite**: **COMPLETADO ✅** (`npm run build` ejecutado, carpeta `dist/` servida para anular el consumo redundante de CPU del hot-reload en el puerto `5173`).
*   **Visual Wave de Dashboards**: **COMPLETADO ✅** (Superposiciones, capas de z-index del Nexo y estabilidad del StrictMode resueltos en el frontend).

##### 2. Plan de Ruta CineK Taller v2.1 (4 Fases de Desarrollo REST)
*   **Fase A: Cimientos y Validación Fail-Fast** *(Backlog Inmediato - Próximo Paso)*:
    1. Implementar `utils/escritura_atomica.py` (patrón Temp-and-Rename con `fsync` y `rename` atómico para evitar corrupciones por cortes solares).
    2. Extender `verify_pow.sh` para que parsee los flujos de ComfyUI (JSON) y valide que el checkpoint de 10GB `svd_xt_1_1.safetensors` está presente antes de abrir los sockets del servidor.
*   **Fase B: API REST, mTLS and Gate Solar** *(Planificado)*:
    1. Refactorizar el script procedural `cinek_pipeline.py` al servidor modular FastAPI `cinek_api.py`.
    2. Implementar los 3 Endpoints del Taller:
        *   `POST /api/cinek/image` → SDXL, devuelve 5 thumbnails.
        *   `POST /api/cinek/video` → SVD img2vid, procesa la imagen seleccionada.
        *   `POST /api/cinek/audio` → Piper TTS + filter_complex de FFmpeg (con adelay y amix) para doblaje manual.
    3. Integrar el middleware de seguridad EARS (bind exclusivo a Tailscale `[IP_TAILNET_REDACTADA]:8050` y filtro CIDR `[IP_TAILNET_REDACTADA]/10` con HTTP 403 de rechazo).
    4. Cablear el decorador `@solo_si_hay_sol` para bloquear las peticiones con HTTP 503 si el voltaje de las baterías solar es inferior a 12.8V.
*   **Fase C: Backpressure y Flujos en Tiempo Real** *(Planificado)*:
    1. Implementar Server-Sent Events (SSE) bajo el endpoint `GET /api/jobs/stream` para propagar los cambios de estado de SQLite en tiempo real hacia la UI React.
    2. Aplicar backpressure sobre ComfyUI: si la cola interna supera los 3 jobs simultáneos, desvía y encola localmente en SQLite, bloqueando el envío al Jetson para no saturar sus 8GB de RAM.
*   **Fase D: Integración de Medios y Multiplexado** *(Planificado)*:
    1. Sincronización del pipeline real con la Fase 6 (Video SVD), Fase 7 (Audio Piper) y Fase 8 (Filtro FFmpeg).

##### 3. Estado de Ejecución de las Fases del Pipeline
*   **Fases 0–5 (MVP de Terminal)**: **COMPLETADO ✅ (Sellado en Oro)**. Primer job de video real completado con un score de calidad de 8.5 (Prompt -> SDXL Jetson -> LLaVA QA).
*   **Fase 6 (Video SVD)**: Codificado, *Sin probar* (requiere checkpoint físico en ComfyUI).
*   **Fase 7 (Audio Piper)**: Codificado, *Sin probar* (requiere `pip install piper-tts` en el venv).
*   **Fase 8 (Mux FFmpeg)**: Codificado, *Sin probar* (filtergraph de audio diseñado pero no ejecutado).
*   **Fase 11 (CinekWidget.tsx)**: Pendiente (Componente React para la galería, reproductor y editor de timestamps manuales).
*   **Fase 12 (Métricas Energéticas)**: Pendiente (Despliegue del voltaje solar y k10temp real en las tarjetas del dashboard).

##### 4. Salvaguardas Criptográficas de la API
*   Trazabilidad de metadatos mediante un **JSON sidecar** atómico por cada job generado (prompt, seed, hash solar y timestamp).
*   Detección en frío de corrupciones mediante la verificación de firmas Ed25519 de la base de datos contra `sovereign_ed25519.pub` en el arranque.
