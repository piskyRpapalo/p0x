# ESPECIFICACIÓN TÉCNICA DE INITIALIZACIÓN Y AISLAMIENTO DEL SISTEMA PARALELO (p0x-soberano)

## 1. JERARQUÍA DE DIRECTORIOS Y PERMISOS DE SEGURIDAD

El sistema paralelo se estructurará de forma exclusiva bajo la ruta base del espacio de usuario `~/p0x-soberano/`. Los directorios de persistencia, bitácoras y empaquetamiento se definen bajo las siguientes especificaciones y permisos octales de Linux:

### 1.1. Directorio Base: `~/p0x-soberano/`
*   **Propósito**: Raíz del entorno aislado paralelo del nodo Soberano.
*   **Permisos requeridos**: `0700` (`drwx------`).
*   **Propietario**: Usuario del sistema operativo que ejecuta los daemons (`pisky`).

### 1.2. Directorio de Base de Datos: `~/p0x-soberano/db/`
*   **Propósito**: Almacenamiento exclusivo del archivo de base de datos relacional SQLite unificada (`aurelius_state.db`) y los índices de vectores de la Capa Plata.
*   **Permisos requeridos**: `0700` (`drwx------`). No se admite acceso de lectura ni escritura a otros usuarios locales del host.

### 1.3. Directorio de Logs de Bronze: `~/p0x-soberano/logs/`
*   **Propósito**: Almacenamiento secuencial e incremental en formato JSONL de todas las interacciones crudas, logs y datos de telemetría de sensores en caliente (Capa Bronze).
*   **Permisos requeridos**: `0755` (`drwxr-xr-x`).

### 1.4. Directorio de Archivos Pedagógicos: `~/p0x-soberano/archive/`
*   **Propósito**: Almacenamiento inmutable en modo de solo lectura de los paquetes comprimidos de andamiaje pedagógico (`M[N]-template-SIGNED.tar.gz`) tras la ejecución de la rutina *Scaffolding Faded*.
*   **Permisos requeridos**: `0755` (`drwxr-xr-x`).

---

## 2. REGLA DE AISLAMIENTO ABSOLUTO DE ESCRITURA

Para evitar colisiones operativas, fallos en caliente o corrupción de los datos del entorno original que se encuentra en ejecución en Beato, se establece una directiva inquebrantable de aislamiento de E/S de disco:

### 2.1. Prohibición de Escritura
Queda estrictamente prohibido que cualquier script, daemon, servicio systemd de usuario, proceso Python, o subproceso de inferencia local del sistema paralelo intente abrir descriptores de archivos para escritura, creación, modificación o eliminación en los siguientes directorios originales:
*   `~/aurelius/`
*   `~/hexelion/`
*   `~/p0x/`
*   `~/.ollama/`

### 2.2. Manejo de Excepciones de I/O
El sistema paralelo implementará aserciones internas en sus módulos de Python que intercepten llamadas de E/S y aborten de forma inmediata (con códigos de salida `rc=1`) si se detecta un intento de mutar un puntero fuera de la ruta de aislamiento `~/p0x-soberano/`.

---

## 3. POLÍTICA DE LECTURA DE RESILIENCIA Y CREDENCIALES

Para asegurar la continuidad operativa del nodo y la asimilación del estado inmaculado del sistema original, se definen las siguientes reglas de lectura:

### 3.1. Acceso de Solo Lectura (Read-Only)
El script de arranque `verify_pow.sh` y las APIs de inicialización de la configuración paralela están autorizados a leer archivos específicos del sistema original con el único fin de asimilar variables de entorno, claves públicas, credenciales locales y perfiles de configuración activos. Estas lecturas se restringen a:
*   `~/hexelion/config.json`
*   `~/aurelius/aurelius_config.json`
*   `~/aurelius/sovereign_ed25519.pub`

### 3.2. Destino de Persistencia
Cualquier variable asimilada, token de red derivado o estado de telemetría procesado a partir de los archivos del sistema original se persistirá únicamente en las estructuras internas del sistema paralelo dentro de `~/p0x-soberano/db/` o `~/p0x-soberano/logs/`.

---

## 4. VERIFICACIÓN DETERMINISTA EN EL ARRANQUE

El script de inicialización `verify_pow.sh` del sistema paralelo ejecutará de forma secuencial y determinista en cada arranque del nodo:

1.  **Asimilación de Credenciales**: Lee en modo solo-lectura el perfil e identidad de `~/aurelius/` para cargar `sovereign_ed25519.pub` en memoria volátil.
2.  **Validación de Permisos de Directorios**: Evalúa que los directorios `~/p0x-soberano/db/`, `~/p0x-soberano/logs/` y `~/p0x-soberano/archive/` posean exactamente los permisos octales requeridos (`0700` y `0755`). Si un directorio tiene configurados permisos más laxos, ejecuta un endurecimiento automático de seguridad (`chmod`) antes de abrir sockets.
3.  **Comprobación de Integridad**: Ejecuta la aserción de integridad SQLite (`PRAGMA integrity_check`) sobre `~/p0x-soberano/db/aurelius_state.db` antes de levantar las APIs de red de Hexelion paralelo.

--------------------------------------------------------------------------------

METADATOS MEDALLION:
*  Tipo: NUEVO_PARALELO
*  Archivo que sustituye: NINGUNO
*  Versión: 1.0-Medallion
*  Fuentes base: FASE 2 REVISADA: APROBADA ✅, p0x-paper-manifest-v2.txt, inventario-necropolis-v2.md, aurelius_pendiente_silver-v2.txt, p0x-master-manifest-merge-v3.txt
*  Conflictos resueltos: NINGUNO
*  Ambigüedades pendientes: NINGUNA
*  Descartes principales: NINGUNO
*  Notas de auditoría: NINGUNA

--------------------------------------------------------------------------------
