### INVENTARIO SOBERANO Y LA NECRÓPOLIS DE SILICIO v2
#### COMPILACIÓN DE RECURSOS ACTIVOS Y DOCTRINA DE DESCARTE · p0x
*Generado por Gemini Notebook - Actualizado tras Censo F0 de Lisboa (WEST)*

--------------------------------------------------------------------------------

#### 1. INVENTARIO FÍSICO-LÓGICO (ESTADO ACTIVO MEDIDO)
El nodo soberano de **p0x · Le Jardin** (Lisboa, Beato) se estructura sobre hardware de silicio aislado y bajo el principio inquebrantable de "El silicio es la frontera" [1, 108]:

##### 1.1. Computadoras y Nodos de Borde (Edge)
1.  **Soberano Principal (Beelink SER9 Max)** [109]:
    *   **Procesador**: AMD Ryzen R7 H255 (8C/16T, hasta 4.9 GHz) [108, 109].
    *   **Sensor Térmico Honesto**: k10temp expuesto en `/sys/class/hwmon/hwmon3/` (temp1_input = 40875 raw, Tctl = 40.9°C). El uso de `thermal_zone0` (acpitz = 20.0°C constantes) queda formalmente catalogado como **OBSOLETO** y deshonesto para este nodo por ser un sensor inactivo de portabilidad. En `la-fragua` (RK3588) y `el-vigía` (RPi), `thermal_zone0` sigue leyendo el SoC real.
    *   **Memoria**: 64 GB DDR5 [108, 109].
    *   **Almacenamiento**: 1 TB NVMe PCIe 4.0 [108, 109].
    *   **Rol**: Inferencia local del preceptor Qwen mediante Ollama, gateway FastAPI, y panel de orquestación local-first [109, 133].
    *   **Protección**: Desgaste de escritura (Write-Wear) mitigado con logrotate agresivo, noatime y almacenamiento de logs en tmpfs [109].

2.  **La Fragua (Orange Pi 5 Plus)** [109]:
    *   **Procesador**: Rockchip RK3588 (8-core 64-bit ARM) [109].
    *   **Memoria**: 16 GB LPDDR4/4x [109].
    *   **Almacenamiento**: Lexar NM790 4 TB NVMe PCIe 4x4 [108, 109].
    *   **Rol**: Nodo de adquisición de radiofrecuencia (SDR ADS-B), base de datos de observaciones e inyección masiva de logs [42, 109].

3.  **El Vigía (Raspberry Pi - Modelo por confirmar)** [110]:
    *   **Rol**: Nodo de adquisición de radiofrecuencia (AIS marítimo), puente serie estable `/dev/serial/by-id/usb-Hades2001_M5stack_6952B20639-if00-port0` para telemetría ambiental del M5Stack y sensores distribuidos [110, 111, 113, 117].

4.  **Nodo IA Acelerada (Yahboom Jetson Orin Nano Super 8GB)** [110]:
    *   **Rendimiento**: 67 TOPS [108, 110].
    *   **Almacenamiento**: 256 GB SSD [110].
    *   **Rol**: Inferencia acelerada por hardware (CUDA), cubriendo el hueco dejado por el coprocesador Google Coral [110].

5.  **Nodos Ligeros y Efímeros**:
    *  Raspberry Pi Zero 2W (512 MB RAM, 64 GB microSD) [110].
    *  M5Stack Atom Lite ESP32 (×2) [110, 112].
    *  Chromebox (×3) [110].

##### 1.2. Directorios que NO existen (Axioma de Construcción Paralela)
Queda estrictamente prohibida la suposición o uso de las siguientes rutas en el entorno original del sistema, debiendo diferirse su existencia para la fase del sistema paralelo en `~/p0x-soberano/`:
*   ❌ `~/.aurelius-p0x/` (La suposición de que esta estructura ya existe es **OBSOLETA**; no se debe crear en el sistema original).
*   ❌ `~/.open-webui/`
*   ❌ `~/repos/`

##### 1.3. Infraestructura de Energía y Climatización (Le Jardin)
*   **Generación Solar**: 2 × 475 Wp Aiko Neostar3 activos (1 × 475 Wp en standby para un total de 1,425 Wp) [108, 113].
*   **Reserva Energética**: Anker Solix C1000X (1,800 W) + Greenwell UPS 1000VA/700W de onda senoidal pura [108, 113].
*   **Controladores y Medición**: Shelly Plus 1PM (WiFi + monitorización de consumo real en Brennenstuhl de 8 tomas) [113].
*   **Acondicionamiento del Rack**: Armario DIGITUS 12U de 19" (profundidad 600 mm) con ventiladores Noctua NF-P12 redux-1700 controlados por PWM [115].

##### 1.4. Adquisición de Señal y Radiofrecuencia (SDR)
*   **Dongle 1 (EEPROM 00001090)**: RTL2838 (Nooelec v5, TCXO 0.5 PPM) en La Fragua para sintonizar ADS-B de aviación a 1090 MHz [113].
*   **Dongle 2 (EEPROM 00000162)**: RTL2838 (Nooelec v5, TCXO 0.5 PPM) en El Vigía para sintonizar señales marítimas AIS a 162 MHz [113].
*   **Antenas**: Flightaware 1090MHz 5.5dBi e inalámbrica plegable Bingfu VHF/UHF [114].

##### 1.5. Fabricación Local
*   **Impresora 3D**: Bambu Lab A1 Mini Combo (FDM rápida, multicolor, operando bajo modo LAN-only aislado) [115].

--------------------------------------------------------------------------------

#### 2. SOFTWARE Y MAPA DE SERVICIOS ACTIVOS (SSH CONFIRMADO)
El entorno lógico del Soberano está habitado por cuatro ciudades operativas, corriendo bajo servicios systemd `--user` del operador `pisky`:

1.  **Aurelius Interfaz** (`aurelius-interfaz.service`):
    *   **Ruta**: `/home/pisky/aurelius/`
    *   **Script**: `servir_interfaz.py`
    *   **Escucha**: Escucha activa en `0.0.0.0:8050` (⚠️ *Violación de doctrina detectada*: Contradice el Master Manifest §4.4 y la Fuente 1 §3 al no amarrarse exclusivamente a la IP de Tailscale. Se corregirá únicamente dentro del sistema paralelo, no en el actual).
2.  **Hexelion FastAPI Gateway**:
    *   **Ruta**: `/home/pisky/hexelion/`
    *   **Estado**: Existente, puerto en escucha.
3.  **p0x Pipeline & Reflejos**:
    *   **Ruta**: `/home/pisky/p0x/`
    *   **Estado**: Código de reflejos y telemetría del Censo F0.
4.  **Codice**:
    *   **Ruta**: `/home/pisky/codice-emancipacion-atomica/`
    *   **Estado**: Repositorio de scripts de automatización Bash.
5.  **OpenWebUI Chat** (`open-webui.service`):
    *   **Ruta**: `~/.local/bin/open-webui`
    *   **Escucha**: IP de Tailscale `[IP_TAILNET_REDACTADA]:8080`.
    *   **Configuración**: `OLLAMA_BASE_URL=http://127.0.0.1:11434`.
6.  **Ollama Engine**:
    *   **Ruta de Modelos**: `~/.ollama/`
    *   **Reconfiguración de Servicio**: Modificado con override de systemd de usuario en `/etc/systemd/system/ollama.service.d/override.conf` con:
        ```ini
        [Service]
        Environment="OLLAMA_HOST=0.0.0.0"
        Environment="OLLAMA_ORIGINS=*"
        ```
        Servicio reiniciado y operativo de forma local-first.

--------------------------------------------------------------------------------

#### 3. LA NECRÓPOLIS (SISTEMAS Y ANDAMIOS DESCARTADOS)
La Necrópolis representa el cementerio de tecnologías que han violado la doctrina de honestidad, han sido ineficientes con el carbono o la RAM, o corresponden a andamios formativos que han sido retirados para forzar la competencia del operador humano [17, 26, 37]:

##### 3.1. Infraestructura y Software Vetados por la Doctrina
1.  **Electron y Go (Capa anytype heredada)** [17]:
    *   *Causa de Muerte*: Veto absoluto por consumo excesivo de RAM (300 MB de base) e ineficiencia extrema de hilos sobre procesadores ARM de bajo consumo, además de la vulnerabilidad sandbox: false [17].
    *   *Reemplazo*: Scripts ultraligeros de Python que sincronizan SQLite cifradas con AES-CFB a través de enlaces directos [17].
2.  **Google Coral Dev Board**:
    *   *Causa de Muerte*: Devuelto al fabricante por limitaciones de rendimiento y hardware [110].
    *   *Reemplazo*: Yahboom Jetson Orin Nano Super de 8GB aportando 67 TOPS estables [110].
3.  **Daemon de base de datos immudb** [22]:
    *   *Causa de Muerte*: El recolector de basura de Go y la sobrecarga del cálculo continuo de hashes provocaban picos térmicos severos en microcontroladores ARM limitados, acelerando el desgaste de las eMMC de Le Jardin [22].
    *   *Reemplazo*: Inyección matemática de una columna merkle_hash directamente en la base SQLite local mediante triggers nativos en C [22].
4.  **Servidor Flask monohilo (de TinyPilot heredado)** [23]:
    *   *Causa de Muerte*: Falta de cifrado SSL nativo, bloqueo de la pila TCP ante ráfagas de video MJPEG, e inexistencia de firmas en comandos de control [23].
    *   *Reemplazo*: Panel stateless de React/Vite en Catppuccin Mocha que habla con WebSockets cifrados TLS 1.3 mTLS validados en el gateway de FastAPI [23].
5.  **Puertos TCP crudos expuestos de dump1090 (30002/30003)** [21]:
    *   *Causa de Muerte*: Exposición a inyecciones remotas de telemetría aérea falsa desde la red WiFi local sin autenticación [21].
    *   *Reemplazo*: Aislamiento de dump1090 de la red abierta; solo se permite a FastAPI asíncrono local leer el puerto 30003 en loopback [21].

##### 3.2. Refactorizaciones Estéticas y de Interfaz (Autopsia del Blueprint v1.3)
Durante la evolución hacia el diseño soberano, los siguientes elementos visuales y de persistencia fueron desmantelados [37]:
*   **Marco de neón cian del Nexo**: Sentenciado por competir con los datos y desgastar contraste. Reemplazado por borde de 1px + glow reservado a cifras vivas [37].
*   **Fondo negro plano de Le Jardin**: Sentenciado por el soberano por considerarlo "poco agraciado". Reemplazado por un render de madera y pergamino mediante CSS puro, libre de imágenes pesadas de fondo [33, 37].
*   **Sopa de etiquetas del Second Brain**: Sentenciado por su nula legibilidad ante la acumulación de títulos. Reemplazado por la Ley de Detalle por Zoom (LOD), donde los nodos se ocultan o expanden dinámicamente según el nivel de zoom [32, 37].
*   **Barras de progreso ambiguas del Sínodo**: Sentenciadas por ser inexplicables. Reemplazadas por chips de bus con métrica única y real [32, 37].
*   **Miniatura de la cámara en el header del Nexo**: Removida del header para preservar su naturaleza de estado puro e identidad; realojada en la celda de observación activa (OBSERVE) [32, 37].
*   **localStorage como única persistencia del Cahier**: Veto absoluto por almacenar la soberanía en el navegador. Reemplazado por sincronización mediante API POST al rack de Le Jardin, dejando a localStorage únicamente como buffer offline de reconciliación [33, 37].
*   **Grilla 4x4 o 6x6 del Herbier**: Descartada para evitar re-maquetaciones ante el escalado de plantas. Reemplazada por una tira horizontal scrollable con snaps de vista [34, 37].

##### 3.3. El Retiro de Andamios (Scaffolding Faded)
*   **Mecánica**: Todo andamio, plantilla formativa de las misiones (_scaffold/) o código de pruebas es considerado residuo temporal en el disco [11, 26, 126].
*   **Proceso de Eliminación**: Al completarse y verificarse una misión, el script de arranque verify_pow.sh empaqueta automáticamente estas plantillas en un archivo comprimido .tar.gz de solo lectura y las elimina físicamente del espacio de trabajo de producción, forzando la autonomía técnica individual [11, 26, 126].

##### 3.4. La Senda de los Muertos (Archivo de Rechazos - Skill B.13)
*   **Mecánica**: Cuando el operador rechaza una propuesta o declina aprender un tema técnico mediante la interfaz de Aurelius, la propuesta no se desvanece silenciosamente. Se entierra en un log append-only local llamado dead_path.jsonl [60].
*   **Auditoría de Evasión**: El archivo almacena la propuesta completa, el motivo verbatim del rechazo y el timestamp [60]. Al acumular 5 rechazos sobre el mismo tema, el sistema genera una alerta no valorativa para confrontar al operador con sus propios patrones de evasión cognitiva [60].
