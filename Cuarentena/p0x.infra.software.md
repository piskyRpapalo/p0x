# 🏛️ SPECIFICATION MASTER FILE: p0x.infra.software
> **SYSTEM_METADATA:**
> *   **Namespace:** `p0x.infra.software`
> *   **Version:** `2.0-Sovereign-Software`
> *   **Status:** Fully Implemented and Validated in Isolated Environment
> *   **Date:** 2026-08-08
> *   **Editor:** AI Redactora Experta en Lenguaje AI (G.R.I.D. Protocol)
> *   **Classification:** Operating System, Network, Sockets & Cryptography

---

## 🥉 CAPA BRONCE (ENTORNOS VIRTUALES & AUTO-CURACIÓN)

### 1. Aislamiento del Intérprete de Python [79, 102]
Debido a que el intérprete del sistema operativo está configurado de forma externa bajo PEP 668 (`externally-managed-environment`), el sistema paralelo vive encapsulado en un entorno virtual dedicado:
*   **Virtualenv de Producción**: `~/CineK_Studio/venv/bin/python` [79].
*   **Script de Auto-Curación**: Bucle en frío de arranque que analiza las salidas de log en busca del fallo "No module named X", instalándolo automáticamente mediante `pip --break-system-packages` si detecta el intérprete global o dentro del venv de forma controlada [79].

### 2. Estructuración del Almacenamiento Volátil [133]
*   **Mitigación de Desgaste**: Configuración de `fstab` para montar `/tmp/p0x-logs/` sobre RAM (`tmpfs`), redirigiendo allí los streams e inserciones ruidosas en caliente de la telemetría de Bronze antes de su consolidación por lotes.

---

## 🥈 CAPA PLATA (ISOLACIÓN DE RED & RELACIONES CONCURRENTES SOBERANAS)

### 1. SQLite WAL & Concurrencia Robusta [6, 103]
Para evitar bloqueos e inconsistencias relacionales en el nodo, la base de datos `aurelius_state.db` en `~/p0x-soberano/db/` opera bajo la siguiente especificación estricta [103]:
*   `PRAGMA journal_mode=WAL;` (Lectores y escritores simultáneos no bloqueantes) [103].
*   `PRAGMA synchronous=NORMAL;` (Reduce el impacto de fsync en cada commit físico de Bronze) [103].
*   `PRAGMA busy_timeout=5000;` (Si CineK transcodifica y retiene el disco, los escritores esperan hasta 5 segundos sin perder transacciones ni arrojar excepciones de base bloqueada) [103].

### 2. Amarre de Interfaces (Network Bind) [129, 131]
*   **Bind de Producción**: El backend FastAPI del sistema paralelo escucha estrictamente en `[IP_TAILNET_REDACTADA]:8050` (IP de Tailscale) [129].
*   **Prohibición de LAN Físicas**: Se prohíben de forma absoluta amarres sobre comodines (`0.0.0.0`) o interfaces inalámbricas/cableadas locales (`eth0`, `wlan0`), bloqueando peticiones de la subred física de Beato (ej. `192.168.x.x`) en la pila TCP/IP [130].
*   **Middleware de Filtrado de IPs (EARS)** [131]:
    *   *WHEN an HTTP request is received BY the parallel API IF the client origin IP address does not match the Tailscale range [IP_TAILNET_REDACTADA]/10 THE system SHALL reject the connection immediately with HTTP 403 Forbidden.*

---

## 🥇 CAPA GOLD (CERRADURA CRIPTOGRÁFICA & PERSISTENCIA INMUTE)

### 1. El Script de Arranque de Confianza: `verify_pow.sh` [83, 103]
La inicialización física de la red privada y los sockets del nodo paralelo exige cumplir la secuencia síncrona en frío de `verify_pow.sh` [103]:
1.  **Auditoría de Dependencias (ABM)**: Valida que los hashes SHA-256 de los paquetes instalados correspondan de forma inmaculada con `aurelius.abm`.
2.  **Firma Detached Ed25519**: Verifica la firma `.sig` de la base de datos del manifiesto contra la clave pública maestra en frío (`~/aurelius/sovereign_ed25519.pub`) [103]. Ante cualquier fallo, aborta (`exit code 1`) bloqueando la escucha de puertos [103].
3.  **Chequeo de Integridad SQLite**: Ejecuta `PRAGMA integrity_check` en la base relacional para descartar corrupciones físicas en la NVMe [103].

### 2. Escritura Atómica Segura (Temp-and-Rename + fsync) [103]
Para anular corrupciones lógicas de archivos de configuración o de diario por fallos eléctricos, toda persistencia crítica de Gold se escribe primero en un fichero temporal en la misma partición y se consolida con el método atómico del OS:
```python
import os

def escritura_atomica(ruta_destino, contenido):
    ruta_tmp = ruta_destino + ".tmp"
    with open(ruta_tmp, "w", encoding="utf-8") as f:
        f.write(contenido)
        f.flush()
        os.fsync(f.fileno())  # Forzar sync en el descriptor
    os.rename(ruta_tmp, ruta_destino)  # Operación atómica de renombrado
```
