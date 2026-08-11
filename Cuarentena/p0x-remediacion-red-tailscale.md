# ESPECIFICACIÓN DE REMEDIACIÓN DE SEGURIDAD DE RED Y ENLACE TAILSCALE (Capa Plata)

## 1. POLÍTICA DE AMARRE (BIND) EXCLUSIVO DE INTERFAZ

El servidor del sistema paralelo (`p0x-soberano`) debe implementar de manera obligatoria una política de direccionamiento restringida a nivel de sockets del sistema operativo para neutralizar cualquier exposición accidental en redes públicas o LANs físicas desprotegidas:

### 1.1. Dirección de Escucha (Bind IP)
*   **IP del Túnel**: `[IP_TAILNET_REDACTADA]` (Interfaz virtual de Tailscale).
*   **Puerto de Escucha**: `8050` (Puerto de la interfaz del dashboard paralelo).
*   **Directiva de Inicialización**: El servidor web asíncrono (FastAPI/Uvicorn) se configurará estrictamente con los parámetros de host `[IP_TAILNET_REDACTADA]` y puerto `8050`.

### 1.2. Prohibición de Escucha Abierta (Wildcard Bind)
*   Queda estrictamente prohibido configurar el host como `0.0.0.0` (escucha en todas las interfaces de red del sistema).
*   Se prohíbe realizar el amarre o binding en la dirección `127.0.0.1` (loopback) en aquellos casos donde el dashboard necesite ser accesible desde otros dispositivos autorizados del operador dentro de la subred privada virtual.
*   El servidor debe rechazar la inicialización si el parámetro de arranque de la interfaz no se resuelve a la IP estricta de Tailscale del nodo.

---

## 2. RECHAZO DE TRÁFICO LAN FÍSICO E INTERFACES DEL HOST

Para garantizar que todo el tráfico interactivo o de datos transite exclusivamente a través del túnel cifrado bajo control del operador, se establece el rechazo determinista de cualquier conexión entrante por hardware local:

### 2.1. Aislamiento de Interfaces de Red Físicas
El sistema paralelo no interactuará ni responderá a peticiones HTTP o WebSockets que provengan de interfaces de hardware de red física locales conectadas al host. Estas interfaces incluyen de forma explícita:
*   Interfaces Ethernet cableadas (e.g., `eth0`, `enp2s0`, etc.).
*   Interfaces de red inalámbricas (e.g., `wlan0`, `wlo1`, etc.).
*   Cualquier otra interfaz que no corresponda al adaptador de red virtual de Tailscale (`tailscale0`).

### 2.2. Bloqueo de Peticiones Fuera del Túnel
Las peticiones que se intenten realizar de forma directa a través de la IP física asignada al nodo Beelink Ryzen por el enrutador de la subred local de Beato (ej. `192.168.x.x` o similar) serán ignoradas y descartadas en la pila TCP/IP, bloqueando el establecimiento del canal antes de procesar cabeceras HTTP.

---

## 3. FILTRADO DE SEGURIDAD A NIVEL DE APLICACIÓN (FastAPI/Python)

Además de las restricciones nativas del sistema operativo en el enlace de sockets, la aplicación paralela escrita en Python implementará una segunda capa de seguridad defensiva activa antes de levantar el enrutamiento de la interfaz de dashboards:

### 3.1. Validación de Socket Pre-Arranque
Antes de inicializar el bucle de eventos del servidor web (FastAPI/Uvicorn), un módulo interceptor del bootstrap paralelo ejecutará la siguiente lógica de control determinista:
1.  **Censo de Interfaces**: Interroga las direcciones del sistema a través de las APIs del kernel de Linux (usando la stdlib de Python `socket` y `struct` para interactuar con descriptores de red).
2.  **Aserción de IP**: Verifica la presencia activa de la dirección IP `[IP_TAILNET_REDACTADA]` asociada a una interfaz cuyo nombre de dispositivo sea de tipo `tailscale` o se valide en la tabla de interfaces del tailnet.
3.  **Aborto de Inicialización**: Si la dirección `[IP_TAILNET_REDACTADA]` no está disponible o la interfaz virtual se encuentra inactiva, la aplicación abortará de forma inmediata la secuencia con un código de salida `rc=1` y registrará el incidente en los ficheros locales `~/p0x-soberano/logs/telemetry.jsonl` bajo el estado `ERROR`.

### 3.2. Middleware de Filtrado de Cabeceras IP
Una vez levantado el socket, un middleware de FastAPI interceptará cada petición HTTP entrante y evaluará el host emisor (`client.host`):
*   **Sintaxis EARS de Filtrado**:
    *   *WHEN an HTTP request is received by the parallel API IF the client origin IP address does not match the Tailscale range [IP_TAILNET_REDACTADA]/10 THE system SHALL reject the connection immediately with HTTP 403 Forbidden and close the socket.*

---

## 4. CONFORMIDAD CON LA SEGURIDAD SOBERANA

Esta configuración de remediación de red implementa de manera estricta el blindaje de la infraestructura paralela:
1.  **Mitigación de Inyecciones**: Previene ataques de inyección de comandos o suplantación de identidad procedentes de otros hosts de la red de área local física de Beato.
2.  **Cifrado Nativo**: Delega el transporte de los comandos de administration hacia el túnel de Tailscale, garantizando cifrado TLS 1.3 de extremo a extremo sin exponer interfaces desprotegidas en la LAN de borde.

--------------------------------------------------------------------------------

METADATOS MEDALLION:
*  Tipo: NUEVO_PARALELO
*  Archivo que sustituye: NINGUNO
*  Versión: 1.0-Medallion
*  Fuentes base: FASE 2 REVISADA: APROBADA ✅, p0x-paper-manifest-v2.txt, inventario-necropolis-v2.md, aurelius_pendiente_silver-v2.txt, blueprint-de-diseno-soberano-v1.4.md, medallon-dashboards-v2.md, CATÁLOGO COMPLETO DE SKILLS AURELIUS
*  Conflictos resueltos: NINGUNO
*  Ambigüedades pendientes: NINGUNA
*  Descartes principales: NINGUNO
*  Notas de auditoría: NINGUNA

--------------------------------------------------------------------------------
