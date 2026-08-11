# 🏛️ SPECIFICATION MASTER FILE: p0x.infra.hardware
> **SYSTEM_METADATA:**
> *   **Namespace:** `p0x.infra.hardware`
> *   **Version:** `2.0-Sovereign-Hardware`
> *   **Status:** Verified in Beato/Lisboa Field Audit (F0-Censo)
> *   **Date:** 2026-08-08
> *   **Editor:** AI Redactora Experta en Lenguaje AI (G.R.I.D. Protocol)
> *   **Classification:** Hardware, Telemetry & Physical Infrastructure

---

## 🥉 CAPA BRONCE (HARDWARE BÁSICO & CENSO DE PUERTOS)

### 1. Inventario de Nodos Activos en Terreno (Lisboa) [1, 2]
*   **`soberano` ([IP_TAILNET_REDACTADA])**: Beelink SER9 Max. Ryzen R7 H255 (8 cores / 16 threads), 64 GB DDR5 RAM, NVMe PCIe 4.0. Director de orquesta principal del sistema paralelo [1, 2].
*   **`la-torre` ([IP_TAILNET_REDACTADA])**: Jetson Orin Nano Super de 8GB de memoria compartida (VRAM). Worker de aceleración visual y botánica [1, 2].
*   **`el-vigia` ([IP_TAILNET_REDACTADA])**: Raspberry Pi conectada a un M5Stack para telemetría ambiental dura [1, 2].
*   **`musculo-hp-02` ([IP_TAILNET_REDACTADA])**: Nodo candidato para el despliegue del motor de Whisper (Fase Post-MVP) [1, 2].

### 2. Censo de Puertos Activos Confirmado [7, 134]
*   **`5173`**: Vite dev (bind temporal a `0.0.0.0` para pruebas externas de desarrollo en Beato) [7, 134].
*   **`8188`**: Instancia local de ComfyUI (bind estricto a loopback `127.0.0.1`, con `--threads 8` para FLUX/SDXL) [7, 134].
*   **`9000`**: CineK Studio (FastAPI, bind estricto a loopback `127.0.0.1` sirviendo el widget interactivo) [6, 7, 134].
*   **`11434`**: Motor de Ollama (bind dual a `127.0.0.1` y a la IP privada de Tailscale `[IP_TAILNET_REDACTADA]`) [7, 134].

### 3. Buses de Adquisición Física y Radiofrecuencia [102, 121]
*   **Puerto de Telemetría Serie**: Dispositivo M5Stack conectado vía USB en `/dev/serial/by-id/usb-Hades2001_M5stack_6952B20639-if00-port0` [121].
*   **Ingesta de Ondas RF (SDR)**: Receptores RTL-SDR acoplados a puertos USB físicos. Adquieren señales a 1090 MHz (dump1090) para aviación civil y AIS-catcher a 162 MHz para tráfico marítimo [102].

---

## 🥈 CAPA PLATA (SENSORES HONESTOS & COLA DE RENDERIZADO ASÍNCRONA)

### 1. Gate Térmico Ryzen `k10temp` con Histéresis [6, 121]
El driver ACPI genérico del sistema operativo (`thermal_zone0`) miente devolviendo 20.0°C constantes en el Beelink [121]. Se implementa el desvío directo al sensor de hardware honesto del procesador AMD Ryzen:
*   **Fichero de lectura física**: `/sys/class/hwmon/hwmon3/temp1_input` (mapeado dinámicamente) [6, 121].
*   **Comportamiento de Histéresis**:
    *   **$\ge$ 85°C (OVERHEAT)**: Señaliza pausa total inmediata sobre los trabajos encolados de CineK (`cinek_jobs`) con un retardo forzado de `sleep 30s` [6, 217].
    *   **> 80°C (FRENO)**: Aplica sleep proporcional para enfriamiento progresivo: `(temp_actual - 80) * 2` segundos en cada ciclo [6, 217].
    *   **$\le$ 75°C (PROCEED)**: Libera el freno de CPU por completo y reanuda el renderizado de forma estable [6, 217].
    *   **NO_DATA**: Si el sensor k10temp no es accesible o devuelve valores corruptos, lanza una excepción de honestidad de forma inmediata para evitar cómputos falsos [6, 217].

### 2. Suministro Solar & Baterías [102]
*   **Capacidad de Generación**: 2 placas solares Aiko de 475 Wp [102].
*   **Almacenamiento Físico**: Batería Anker Solix C1000X [102].
*   **Monitoreo**: Telemetría real de voltaje canalizada a través del Shelly Plus 1PM y leída por el daemon `gestor_energia.py` [102].

---

## 🥇 CAPA GOLD (PRESUPUESTO DE CARBONO & PROTECCIÓN TÉRMICA EXTRACTIVA)

### 1. Lógica Determinista de Inferencia Solar Degradada [103]
El voltaje de las baterías solar gobierna de forma incondicional el comportamiento de los modelos de inferencia pesados (Ollama):
*   **Fase de Pleno Sol ($\ge$ 12.8V)**: Estado `SOLAIRE_OK`. CineK y los modelos locales operan al máximo rendimiento y se autorizan renderizados pesados [103].
*   **Fase de Espera/Contingencia (< 12.8V)**: Estado `EN_ATTENTE`. El decorador `@solo_si_hay_sol` bloquea la cola y devuelve HTTP 503 "Certification Solaire: En attente", congelando el renderizado de video [103].
*   **Fase Crítica (< 12.2V / UPS en Batería)**: El sistema inyecta en caliente la configuración de hilos degradada de Ollama (`OLLAMA_NUM_THREADS=2`) reiniciando el servicio para no agotar la Solix C1000X, y reduce al mínimo el uso de recursos [103].

### 2. Protección Física contra Desgaste de Escritura (Write-Wear) y Swap [6, 134]
*   **Memoria de Intercambio (Swap)**: Desactivada por hardware (`vm.swappiness=10`, sin swapfile activo) para resguardar la salud de la unidad NVMe de 1 TB ante escrituras de paginación [134].
*   **Límites de Temperatura Críticos**: Si el sensor Ryzen reporta $\ge$ 90°C sostenidos durante la inferencia, el daemon mata el proceso del motor de Ollama para forzar la descarga de los pesos y enfriar el silicio.
