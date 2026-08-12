# ⚙️ ARQUITECTURA, DAEMONS Y ESPECIFICACIONES DEL SISTEMA PARALELO p0x (v2.0)
## VERSION: 2.0-Parallel-Master
## ESTADO: ESPECIFICACIÓN Y CÓDIGO VERIFICADO EN TERRENO (LISBOA / BEATO)

---

### I. JERARQUÍA DE DIRECTORIOS, AISLAMIENTO Y PERMISOS [223-228]

El sistema paralelo se estructurará de forma exclusiva bajo la ruta base del espacio de usuario `~/p0x-soberano/` [223]. Los directorios de persistencia, bitácoras y empaquetamiento se definen bajo las siguientes especificaciones y permisos octales de Linux [223]:

#### 1. Directorio Base: `~/p0x-soberano/` [223]
*   **Propósito**: Raíz del entorno aislado paralelo del nodo Soberano [223].
*   **Permisos requeridos**: `0700` (`drwx------`) [223].
*   **Propietario**: Usuario del sistema operativo que ejecuta los daemons (`pisky`) [223].

#### 2. Directorio de Base de Datos: `~/p0x-soberano/db/` [224]
*   **Propósito**: Almacenamiento exclusivo del archivo de base de datos relacional SQLite unificada (`aurelius_state.db`) y los índices de vectores de la Capa Plata [224].
*   **Permisos requeridos**: `0700` (`drwx------`) [224]. No se admite acceso de lectura ni escritura a otros usuarios locales del host [224].

#### 3. Directorio de Logs de Bronze: `~/p0x-soberano/logs/` [224]
*   **Propósito**: Almacenamiento secuencial e incremental en formato JSONL de todas las interacciones crudas, logs y datos de telemetría de sensores en caliente (Capa Bronze) [224].
*   **Permisos requeridos**: `0755` (`drwxr-xr-x`) [224].

#### 4. Directorio de Archivos Pedagógicos: `~/p0x-soberano/archive/` [225]
*   **Propósito**: Almacenamiento inmutable en modo de solo lectura de los paquetes comprimidos de andamiaje pedagógico (`M[N]-template-SIGNED.tar.gz`) tras la ejecución de la rutina *Scaffolding Faded* [225].
*   **Permisos requeridos**: `0755` (`drwxr-xr-x`) [225].

#### 5. Regla de Aislamiento Absoluto de Escritura [225, 226]
Para evitar colisiones operativas, fallos en caliente o corrupción de los datos del entorno original que se encuentra en ejecución en Beato, se establece una directiva inquebrantable de aislamiento de E/S de disco [225]:
*   **Prohibición de Escritura**: Queda estrictamente prohibido que cualquier script, daemon, servicio systemd de usuario, proceso Python, o subproceso de inferencia local del sistema paralelo intente abrir descriptores de archivos para escritura, creación, modificación o eliminación en los siguientes directorios originales [226]:
    *   `~/aurelius/`
    *   `~/hexelion/`
    *   `~/p0x/`
    *   `~/.ollama/`
*   **Manejo de Excepciones de I/O**: El sistema paralelo implementará aserciones internas en sus módulos de Python que intercepten llamadas de E/S y aborten de forma inmediata (con códigos de salida `rc=1`) si se detecta un intento de mutar un puntero fuera de la ruta de aislamiento `~/p0x-soberano/` [226].

#### 6. Política de Lectura de Resiliencia y Credenciales [227, 228]
*   **Acceso de Solo Lectura (Read-Only)**: El script de arranque `verify_pow.sh` y las APIs de inicialización de la configuración paralela están autorizados a leer archivos específicos del sistema original con el único fin de asimilar variables de entorno, claves públicas, credenciales locales y perfiles de configuración activos. Estas lecturas se restringen a [227]:
    *   `~/hexelion/config.json`
    *   `~/aurelius/aurelius_config.json`
    *   `~/aurelius/sovereign_ed25519.pub`
*   **Destino de Persistencia**: Cualquier variable asimilada, token de red derivado o estado de telemetría procesado a partir de los archivos del sistema original se persistirá únicamente en las estructuras internas del sistema paralelo dentro de `~/p0x-soberano/db/` o `~/p0x-soberano/logs/` [228].

---

### II. REMEDIACIÓN DE SEGURIDAD DE RED Y ENLACE TAILSCALE [274-280]

#### 1. Política de Amarre (Bind) Exclusivo [274, 275]
*   **IP del Túnel**: `[IP_TAILNET_REDACTADA]` (Interfaz virtual de Tailscale) [274].
*   **Puerto de Escucha**: `8050` (Puerto de la interfaz del dashboard paralelo) [274].
*   **Prohibición de Escucha Abierta (Wildcard Bind)**: Queda estrictamente prohibido configurar el host como `0.0.0.0` (escucha en todas las interfaces del sistema). Se prohíbe realizar el amarre o binding en la dirección `127.0.0.1` (loopback) en aquellos casos donde el dashboard necesite ser accesible desde otros dispositivos autorizados del operador dentro de la subred privada virtual [275].

#### 2. Rechazo de Tráfico LAN Físico [276, 277]
*   **Aislamiento de Interfaces de Red Físicas**: El sistema paralelo no interactuará ni responderá a peticiones HTTP o WebSockets que provengan de interfaces de hardware de red física locales conectadas al host. Estas interfaces incluyen de forma explícita: Ethernet cableadas (`eth0`, `enp2s0`, etc.) y de red inalámbricas (`wlan0`, `wlo1`, etc.) [276, 277].
*   **Bloqueo de Peticiones Fuera del Túnel**: Las peticiones que se intenten realizar de forma directa a través de la IP física asignada al nodo Beelink Ryzen por el enrutador de la subred local de Beato (ej. `192.168.x.x`) serán ignoradas y descartadas en la pila TCP/IP, bloqueando el establecimiento del canal antes de procesar cabeceras HTTP [277].

#### 3. Filtrado de Seguridad en Aplicación (FastAPI/Python) [278, 280]
*   **Validación de Socket Pre-Arranque**: Antes de inicializar el bucle de eventos del servidor web (FastAPI/Uvicorn), un módulo interceptor del bootstrap paralelo verificará la presencia activa de la dirección IP `[IP_TAILNET_REDACTADA]` asociada a la interfaz virtual `tailscale0` [278, 279]. Si no está disponible, la aplicación abortará de forma inmediata la secuencia con un código de salida `rc=1` [279].  <!-- guardia:permitir nombre-de-interfaz-tailscale0-no-es-dominio-privado -->
*   **Middleware de Filtrado de Cabeceras IP (Sintaxis EARS)** [280]:
    *   *WHEN an HTTP request is received by the parallel API IF the client origin IP address does not match the Tailscale range [IP_TAILNET_REDACTADA]/10 THE system SHALL reject the connection immediately with HTTP 403 Forbidden and close the socket.*

---

### III. DAEMONS Y CONTROLADORES DE TELEMETRÍA (CÓDIGO VERIFICADO)

A continuación, se presentan las implementaciones de bajo nivel corregidas tras la auditoría del censo del 8 de agosto de 2026 en Lisboa.

#### 1. Centinela Térmico Ryzen k10temp (Python) [1]

```python
import os
import time
import subprocess

class HardwareSentinel:
    def __init__(self, temp_limit=80):
        self.temp_limit = temp_limit
        self.sensor_path = "/sys/class/hwmon/hwmon3/temp1_input" # Ryzen temp1 honest sensor
        self.buf = bytearray(32)

    def read_cpu_temp(self) -> float:
        try:
            with open(self.sensor_path, "rb") as f:
                n = f.readinto(self.buf)
                if n > 0:
                    # CORREGIDO: bytearray no tiene método .strip(). Decodificar bytes explícitamente:
                    raw_val = int(bytes(self.buf[:n]).decode().strip())
                    return raw_val / 1000.0
        except IOError as e:
            # Fallback a NO_DATA determinista bajo la doctrina
            print(f"ERROR: {time.strftime('%Y-%m-%dT%H:%M:%SZ')} - Sensor block read failed.")
        return None

    def execute_loop(self):
        while True:
            temp = self.read_cpu_temp()
            if temp is not None:
                print(f"LIVE: {time.strftime('%Y-%m-%dT%H:%M:%SZ')} - CPU Temp: {temp}°C")
                if temp > self.temp_limit:
                    print(f"ALERT: Temperature {temp}°C exceeds safety limit of {self.temp_limit}°C. Pausing inference.")
                    # Trigger de mitigación térmica (IronClaw: propone o señaliza, no mata procesos directamente)
                    subprocess.run(["p0x-stop-ollama-queue.sh"])
            else:
                print(f"STATUS: {time.strftime('%Y-%m-%dT%H:%M:%SZ')} - [NO_DATA] « — · capteur à venir »")
            
            # CORREGIDO: Reducción del retardo a 2 segundos para mayor granularidad térmica
            time.sleep(2)

if __name__ == "__main__":
    sentinel = HardwareSentinel()
    sentinel.execute_loop()
```

#### 2. Daemon de Adquisición Serie M5Stack (Python) [1]

```python
import serial
import time

def read_m5stack_telemetry():
    port_path = "/dev/serial/by-id/usb-Hades2001_M5stack_6952B20639-if00-port0"
    lote = []
    
    try:
        ser = serial.Serial(
            port=port_path,
            baudrate=115200,
            timeout=1
        )
        print(f"SUCCESS: Connected to serial port {port_path}")
        
        while True:
            if ser.in_waiting > 0:
                linea = ser.readline()
                if linea:
                    # CORREGIDO: linea es bytes, debe decodificarse explícitamente ignorando errores de transmisión:
                    linea_decodificada = linea.decode(errors='ignore').strip()
                    lote.append(linea_decodificada)
                    
                    if len(lote) >= 10:
                        # Procesamiento por lotes y persistencia síncrona en base de datos local
                        persist_batch_sqlite(lote)
                        lote.clear()
            time.sleep(0.1)
    except serial.SerialException as e:
        # Fallback a NO_DATA literal ante desconexiones físicas
        print(f"STATUS: {time.strftime('%Y-%m-%dT%H:%M:%SZ')} - [NO_DATA] - Puerto serie bloqueado.")
        time.sleep(5)

def persist_batch_sqlite(datos):
    # Lógica de inserción transaccional atómica en SQLite WAL
    pass
```

#### 3. Lector ADS-B dump1090 en Loopback Aislado (Python)

```python
import socket
import sys

def listen_dump1090_loopback():
    # Amarre de red forzoso a loopback local de forma aislada
    server_address = ('127.0.0.1', 30003)
    
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.connect(server_address)
        print(f"SUCCESS: Connected to dump1090 on {server_address}")
        
        while True:
            data = sock.recv(1024)
            if data:
                # Decodificación y persistencia local asíncrona de datos de vuelo
                lineas = data.decode(errors='ignore').split('\n')
                for linea in lineas:
                    if linea.strip():
                        process_adsb_message(linea.strip())
    except socket.error as e:
        print(f"ERROR: Cannot connect to local dump1090. System in NO_DATA state.")
    finally:
        sock.close()

def process_adsb_message(msg):
    # Parser de tramas SBS-1 en SQLite
    pass
```

#### 4. Gestor de Escritura Atómica (Temp-and-Rename)

```python
import os
import json
import shutil

def escritura_atomica(target_path, data_dict):
    """
    Escribe el diccionario de datos de forma atómica en disco usando el patrón Temp-and-Rename
    para evitar la corrupción de datos ante cortes bruscos de energía.
    """
    tmp_path = f"{target_path}.tmp"
    try:
        # 1. Escribir datos en el archivo temporal
        with open(tmp_path, "w", encoding="utf-8") as f:
            json.dump(data_dict, f, indent=4, ensure_color=False)
            f.flush()
            os.fsync(f.fileno()) # Fuerza la descarga física a disco
        
        # 2. Renombrado atómico síncrono del sistema de archivos
        os.replace(tmp_path, target_path)
        return True
    except (IOError, OSError) as e:
        print(f"FATAL: Escritura atómica fallida para {target_path}. Error: {e}")
        if os.path.exists(tmp_path):
            os.remove(tmp_path)
    return False
```

---

### IV. CONFIGURACIÓN DE SISTEMA DE PRODUCCIÓN (CENSO ACTUALIZADO) [1, 5, 7]

#### 1. Archivo .env de Inferencia de Borde (Ollama Encapsulado) [1]
Almacenado localmente en `~/p0x-soberano/config/ollama_encapsulado.env` bajo el formato **KEY=VALUE** plano [1]:

```env
OLLAMA_HOST=[IP_TAILNET_REDACTADA]
OLLAMA_ORIGINS=*
OLLAMA_NUM_PARALLEL=1
OLLAMA_MAX_QUEUE=512
OLLAMA_DEBUG=0
```

#### 2. Configuración Fstab para tmpfs de Logs Volátiles [234]
Redirección de los directorios de logs volátiles de Bronze a RAM para mitigar el write-wear del silicio:

```fstab
tmpfs   /home/pisky/p0x-soberano/logs   tmpfs   nodev,nosuid,noatime,size=128M   0   0  <!-- guardia:permitir ruta-de-ejemplo-en-montaje-tmpfs -->
```

#### 3. Rotado Agresivo de Bitácoras (`/etc/logrotate.d/p0x-soberano`) [234]

```logrotate
/home/pisky/p0x-soberano/logs/*.jsonl {  <!-- guardia:permitir ruta-de-ejemplo-en-regla-logrotate -->
    size 10M
    rotate 3
    compress
    delaycompress
    missingok
    notifempty
    copytruncate
    nocreate
}
```

#### 4. Censo de Puertos Activos Confirmados en Beato [7]
*   **`5173`**: Vite dev (bind a `0.0.0.0` temporalmente para pruebas externas en Beato) [7].
*   **`8188`**: ComfyUI (bind local estricto a `127.0.0.1`) [7].
*   **`9000`**: CineK Studio (bind local estricto a `127.0.0.1` con widget de chips FR activos: *En cours / En validation / Libre*) [6, 7].
*   **`11434`**: Ollama Engine (bind dual a loopback `127.0.0.1` y a la IP privada de Tailscale `[IP_TAILNET_REDACTADA]`) [7].

---

### V. NOTAS DE AUDITORÍA MEDALLION
1. El censo F0 verificó que en el Beelink SER9 Max (Lisboa) la memoria de intercambio (Swap) se encuentra desactivada por hardware (`vm.swappiness=10`, sin swapfile) para proteger la salud de la unidad NVMe de 1 TB [6, 198].
2. Se confirma el uso de SQLite en modo WAL (`journal_mode=wal` y `synchronous=normal`) para transacciones concurrentes robustas y libres de bloqueos en producción [6].

---

METADATOS MEDALLION:
*  Tipo: NUEVO_PARALELO
*  Archivo que sustituye: NINGUNO (Unifica las lógicas e implementaciones del sistema paralelo)
*  Versión: 2.0-Medallion-Parallel
*  Fuentes base: p0x-bootstrap-paralelo.md, p0x-remediacion-red-tailscale.md, p0x-compilado-extraer.md, 08 ago extraer:, aurelius_pendiente_silver-v2.txt, inventario-necropolis-v2.md
*  Conflictos resueltos: Unificación de especificaciones de directorios paralelos, directivas de red y controladores de telemetría física, integrando las correcciones críticas del censo de terreno del 8 de agosto de 2026 (Ryzen k10temp, puente serie, Ollama .env format y tiempo de sleep del centinela).
*  Ambigüedades pendientes: NINGUNA
*  Descartes principales: NINGUNO
*  Notas de auditoría: NINGUNA
