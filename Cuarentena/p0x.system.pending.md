# 🏛️ SPECIFICATION MASTER FILE: p0x.system.pending
> **SYSTEM_METADATA:**
> *   **Namespace:** `p0x.system.pending`
> *   **Version:** `2.0-Deudas-Senda`
> *   **Status:** Active Backlog & Historical Artifact Necropolis
> *   **Date:** 2026-08-08
> *   **Editor:** AI Redactora Experta en Lenguaje AI (G.R.I.D. Protocol)
> *   **Classification:** Technical Debt, Necropolis & Roadmap

---

## 🥉 CAPA BRONCE (LA SENDA DE LOS MUERTOS - ARQUEOLOGÍA VISUAL)

Aquí yacen los elementos de diseño, interfaces y andamiajes descartados de forma sistemática para proteger la CPU del nodo y cumplir el canon visual brutalista [200]:

### 1. Elementos Visuales Enterrados [106, 200]
*   **Luna del Cielo en Le Jardin**: Eliminada por desentonar con el propósito rústico e íntimo del huerto [106]. Se aplica `display: none` incondicional [106].
*   **Bolas Violetas Flotantes en El Muro**: Descartadas por toscas e intrusivas en el espacio negativo del arte de fondo [106].
*   **Marco de Neón Cian de las Celdas**: Retirado del Nexo por competir con el contraste de los datos de telemetría numéricos [200].
*   **Barras de Progreso Lineales de los Agentes**: Reemplazadas en el Sínodo por chips compactos con métricas numéricas reales [200].
*   **Sopa de Etiquetas sin L.O.D. en el Second Brain**: La superposición indiscriminada saturaba la pantalla. Sustituido por la Ley de Detalle por Zoom (LOD) [200].
*   **Grilla Multicolumna Estática o 4x4 de L'Herbier**: Provocaba constantes saltos de layout al poblarse. Reemplazada por un slider horizontal con snaps adaptativos [200].

### 2. Decisiones Técnicas Vetadas [200]
*   **`localStorage` como Almacén Único en Le Cahier**: Vetado por el preceptor por razones de privacidad y persistencia débil en el cliente. Sustituido por llamadas HTTP POST al disco del rack (`diary_sealed/`) [200].
*   **Glassmorphism (`Modifier.blur()` / Haze)**: Prohibido de forma absoluta en widgets. Con una CPU Ryzen pura sin dGPU de alta VRAM, repintar convoluciones gaussianas a 60 fps satura el silicio [106, 200].
*   **Daemon de base immudb**: Vetado por sobrecarga térmica extrema en ARM de bajo consumo debido a su colector de basura en Go. Reemplazado por triggers en C nativos dentro de SQLite [200].
*   **Puertos TCP Abiertos de dump1090 (30002/30003)**: Eliminados de la LAN para evitar inyección de aeronaves falsas. Confinados estrictamente a loopback (`127.0.0.1`) mediante nftables [200].

---

## 🥈 CAPA PLATA (DEUDA TÉCNICA ACTIVA & FILTROS DE MEJORA)

### 1. Registro de Incidentes Pendientes en Beato [121, 122, 123]
*   **M5Stack Serie-Redis**: El puente serie del Vigía reporta fallos de lectura aleatorios. Se exige implementar el fallback de sensor ausente ("— · capteur à venir") con timestamp de último avistamiento [121].
*   **Agente Enlace**: El servicio de Enlace no existe físicamente en el disco de producción, rompiendo el ratio de Sínodo $n/6$. Se debe aprovisionar el micro-servicio minimal en Python [122].
*   **Claves de Pulso en Redis**: Las claves de latido de los agentes carecen de tiempo de vida (TTL), impidiendo la detección de estados desconectados (`stale`). Se debe inyectar un TTL estricto de 60 segundos [122].
*   **Ruta de Aislamiento Base**: Varios scripts asumen la ruta `~/.aurelius-p0x/` que no existe en el metal de producción de Beato [123]. El sistema paralelo debe confinarse exclusivamente a `~/p0x-soberano/` [123].

---

## 🥇 CAPA GOLD (HOJA DE RUTA Y OLEADA DE PRODUCCIÓN DE ENERO-AGOSTO 2026)

### 1. Roadmap Inmediato de Despliegue Visual (Fase de Cierre) [113, 222]
*   **Paso 1: Compilación de Vite**: Ejecutar `npm run build` para generar la carpeta estática optimizada `dist/` [222]. Esto anula por completo el consumo continuo de CPU por el hot-reload de Vite dev en el puerto `:5173` [222].
*   **Paso 2: Servidor Nginx**: Configurar el proxy reverso Nginx para escuchar en la IP privada de Tailscale `[IP_TAILNET_REDACTADA]:8090`, sirviendo los estáticos y enrutando de forma segura las pasarelas de CineK Studio (`:9000`) y Ollama (`:11434`) [102, 222].
*   **Paso 3: Sello de Telemetría Solar Real**: Cablear físicamente los feeds del Shelly Plus 1PM y del microcontrolador para escribir en la tabla relacional `bronze_solar`, sustituyendo la simulación actual de CineK.
*   **Paso 4: Animaciones Avanzadas de Le Cahier**: Refinar el shader de iluminación radial violeta al nacer las notas y pulir el rito de cierre del libro 3D al pulsar Mémoire.
