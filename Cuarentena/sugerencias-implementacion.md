# 🏛️ MANUAL DE SUGERENCIAS DE IMPLEMENTACIÓN Y OPTIMIZACIÓN DE WORKFLOWS (CANON P0X)

Este documento consolidado actúa como el **Criterio de Verdad y Guía de Arquitectura de Coste Cero en RAM** para la construcción, scraping, optimización de flujos y persistencia local-first en tus proyectos paralelos (`Aurelius`, `Hexelion`, `CineK`, `El Vigía`). 

Está optimizado para ser consumido por agentes de desarrollo (ej. Claude Code, Cursor) e inteligencias artificiales locales, unificando las lecciones críticas de los **11 repositorios de código clave** de tu base de conocimientos con las reglas físicas del hardware real de tu nodo.

---

## PARTE I: LA LECCIÓN DE LOS 11 REPOSITORIOS (THE "FULL PICTURE")

Para diseñar un scrapedor de código local, optimizador de workflows de IA, o pipeline de agentes eficiente, se deben asimilar los principios de diseño de bajo nivel que permiten a estos proyectos operar con rendimientos óptimos sin fugar un solo byte de memoria o datos privados:

```
                  ┌──────────────────────────────────────────┐
                  │          SOVEREIGN WORKFLOW              │
                  │   (Conductor-Instrument Architecture)    │
                  └────────────────────┬─────────────────────┘
                                       │
                ┌──────────────────────┴──────────────────────┐
                ▼                                             ▼
  ┌───────────────────────────┐                 ┌───────────────────────────┐
  │      INGESTA / AST        │                 │    PERSISTENCIA / SYNC    │
  │   (Zero-Malloc / DMA)     │                 │   (SQLite WAL / Merkle)   │
  ├───────────────────────────┤                 ├───────────────────────────┤
  │ • ggerganov/llama.cpp     │                 │ • anyproto/anytype-ts     │
  │ • antirez/dump1090        │                 │ • syncthing/syncthing     │
  │ • mtlynch/tinypilot       │                 │ • automerge/automerge     │
  │ • karpathy/llama2.c       │                 │ • codenotary/immudb       │
  └───────────────────────────┘                 └───────────────────────────┘
```

### 1. Optimización del Límite del Silicio y Cero Alocación en Caliente
*   **`ggerganov/llama.cpp`**: Enseña la construcción de un **Grafo de Cómputo Estático (`ggml_cgraph`)** y el uso de **`ggml_gallocr`** [596]. Tu optimizador de workflows o scraper debe calcular en frío el tamaño total de la memoria e interacciones necesarias antes de iniciar la ejecución [596]. Queda prohibida la asignación dinámica de memoria en caliente (`malloc`/`free`); se debe reservar un buffer único contiguo al iniciar el daemon para anular la fragmentación del heap y picos de CPU [596, 602].
*   **`karpathy/llama2.c`**: Demuestra la potencia del **mapeo de memoria virtual (`mmap`)** directo sobre estructuras de datos binarias contiguas alineadas en el heap (Config, pesos) [597]. El scraper o motor de prompts debe cargar bases de conocimiento mapeando archivos directamente en el espacio de direcciones de direcciones virtuales del kernel de Linux, logrando un tiempo de carga cero sin deserializaciones redundantes en la RAM [596, 597].
*   **`antirez/dump1090`**: Enseña la ingesta directa mediante buffers circulares estáticos por acceso directo a memoria (DMA) y el uso de **tablas de búsqueda trigonométrica estáticas (`mag_lut`)** precalculadas en frío [602]. Toda evaluación en caliente o matching de prompts/tokens en bucles repetitivos debe usar arrays indexados estáticos $O(1)$ en lugar de llamar a cálculos pesados en tiempo de ejecución, manteniendo la carga en CPUs ARM por debajo del 5% [602].

### 2. Sincronización Delta y Persistencia Anticaídas
*   **`syncthing/syncthing`**: Implementa el protocolo de intercambio de bloques (**Block Exchange Protocol - BEP**) mediante firmas de bloques SHA-256 [599]. Al sincronizar repositorios, datasets o notas del diario de forma offline, los agentes locales deben intercambiar exclusivamente las firmas de los hashes y descargar únicamente los deltas de bloques modificados [599]. Sella la robustez transaccional migrando toda base de datos volátil a **SQLite en modo WAL** (Write-Ahead Logging) para resistir apagones abruptos de batería solar o picos de consumo [599].
*   **`automerge/automerge`**: Provee el algoritmo matemático CRDT en Rust/WASM con **compresión binaria columnar** [600]. Al fusionar diferentes ramas de pensamiento o sesiones de desarrollo (`worktrees`), el sistema paralelo debe aplicar persistencias incrementales diferenciales (`save_incremental()`) para evitar el desgaste físico de las unidades de estado sólido o tarjetas SD (mitigación de *Write Wear*) [600].
*   **`anyproto/anytype-ts`**: Muestra cómo derivar la identidad digital descentralizada (mTLS) de una semilla mnemónica física de 12 palabras y cómo blindar la sincronización local-first organizando los cambios de los documentos en un **árbol de Merkle inmutable** encriptado de forma simétrica mediante AES-CFB, operando asíncronamente con un backend local vía llamadas gRPC locales [598].

### 3. Inmutabilidad, Búsqueda Local y Orquestación CLI
*   **`codenotary/immudb`**: Define la inmutabilidad relacional mediante logs de transacciones append-only vinculados criptográficamente a través de árboles de Merkle [603]. Permite realizar **Consistency e Inclusion Proofs** sin conexión a internet para asegurar que el registro de auditoría visual de los scripts, renders o firmas no ha sido alterado de forma maliciosa por un proceso del host [603].
*   **`simonw/llm`**: Ofrece el patrón de diseño para la orquestación ligera de modelos mediante terminales de comandos de consola, persistiendo transaccionalmente prompts, respuestas, tokens y metadatos del modelo en SQLite local, desacoplándose de los backends de inferencia mediante plugins estructurados en *entry points* [601].
*   **`Gentleman-Programming`**: Define la estructuración del conocimiento cognitivo en registros o fichas atómicas inmutables denominadas **engrams** de cuatro campos (`What`, `Why`, `Where_Ref`, `Learned`) indexados mediante tablas virtuales **SQLite FTS5** para búsquedas offline ultrarrápidas de texto completo [605].
*   **`mtlynch/tinypilot`**: Demuestra el control de rendimiento web transmitiendo MJPEG sobre WebSockets directos interactuando con el kernel de Linux (`v4l2`), operando una interfaz stateless sin frameworks pesados ni dependencias de Node.js [604].

---

## PARTE II: "SCRAPER" DE WORKFLOWS Y OPTIMIZACIONES DE INFRAESTRUCTURA

Para construir un scraper u optimizador local que analice repositorios locales, genere pipelines de prompts y asigne colas de inferencia sin sobrecargar el procesador AMD Ryzen de 64GB de tu nodo Beelink SER9 Max, debes codificar las siguientes reglas lógicas duras:

### 1. El Filtro de Entropía Léxica $O(N)$ (Anti-Degeneración de IA)
Para evitar que un modelo de lenguaje local (Ollama/Qwen3) entre en bucles infinitos de repetición de tokens durante el análisis o scraping de un repositorio grande (consumiendo VRAM y RAM de forma desmedida), se implementa un interceptor matemático de bajo nivel en el stream de texto:

$$\text{Ratio de Entropía} = \frac{\text{Palabras Únicas}}{\text{Palabras Totales}}$$

```python
import collections

def verificar_entropia_stream(texto_actual, window_size=50):
    """
    Heurística instantánea O(N) que analiza la diversidad de vocabulario.
    Si el ratio cae por debajo de 0.4, corta el socket de inferencia local.
    """
    palabras = [p.lower() for p in texto_actual.split() if p.isalnum()]
    if len(palabras) < window_size:
        return True # Esperando tamaño mínimo de ventana
        
    ultima_ventana = palabras[-window_size:]
    frecuencia = collections.Counter(ultima_ventana)
    ratio = len(frecuencia) / len(ultima_ventana)
    
    # Si la diversidad léxica decae catastróficamente, hay loop de inferencia
    if ratio < 0.4:
        return False # Interrupción determinista: "Fatiga cognitiva o bot detected"
    return True
```

### 2. Parser AST de Seguridad en Pipelines (Command Guard CI/CD)
El scraper de workflows no debe usar llamadas a la IA para auditar comandos peligrosos en scripts o repositorios locales. Se utiliza un parser determinista AST en Python puro que valida los comandos contra una lista negra en frío antes de renderizarlos o permitirlos en el **Portapapeles Soberano** [117, 131, 133]:

```python
import ast

class CommandSecurityValidator(ast.NodeVisitor):
    def __init__(self, whitelist_calls=None):
        self.whitelist = whitelist_calls or {'print', 'len', 'int', 'str', 'sorted'}
        self.is_safe = True
        self.violation = None

    def visit_Call(self, node):
        # Captura llamadas a funciones peligrosas de ejecución dinámica
        if isinstance(node.func, ast.Name):
            if node.func.id in {'eval', 'exec', 'subprocess', 'os.system', 'popen'}:
                self.is_safe = False
                self.violation = f"Llamada prohibida a: {node.func.id}"
        self.generic_visit(node)

def validar_script_local(codigo_fuente):
    try:
        tree = ast.parse(codigo_fuente)
        validator = CommandSecurityValidator()
        validator.visit(tree)
        return validator.is_safe, validator.violation
    except SyntaxError:
        return False, "SyntaxError: Código no analizable de forma segura"
```

### 3. Arquitectura "Conductor-Instrumento" (CineK Pattern)
Para el renderizado de vídeo y audio asíncronos o la automatización de workflows complejos locales:
*   **El Conductor**: El daemon principal en Python de tu nodo Beelink actúa como orquestador ligero [451, 454]. No procesa inferencias pesadas en su hilo principal [451, 454].
*   **Los Instrumentos**: Delegación de tareas pesadas a endpoints REST locales e independientes mediante llamadas asíncronas [451, 454]:
    *   `/api/generate` de ComfyUI (vídeo mediante difusión local) [451, 454].
    *   `/api/tags` / `/api/generate` de Ollama (redacción de guiones con Qwen) [451, 454].
    *   Piper TTS (conversión síncrona a audio .wav en cache) [453, 464].
*   **Multiplexado Zero-Disk con FFmpeg**: El multiplexor de audio y vídeo final se realiza canalizando las salidas directas de memoria (pipes), evitando ciclos redundantes de lectura/escritura en tu unidad NVMe física [453, 454].

---

## PARTE III: REGLAS DE CONTROL TÉRMICO Y ENERGÉTICO (CAPA BRONCE/SILVER)

Un scraper, daemon o cola de procesamiento en un nodo soberano debe conocer y someterse a las variables de estado térmico y suministro solar físico:

### 1. Lectura del Sensor Térmico Honesto (`k10temp`)
El daemon centinela debe eludir las lecturas deshonestas del driver ACPI genérico del sistema operativo (`thermal_zone0` que miente 20°C fijos) [530, 609]. Debe buscar dinámicamente el sensor real `k10temp` expuesto por el procesador AMD Ryzen [530, 609]:

```python
import os
import glob
import time

def obtener_temperatura_ryzen():
    """
    Busca de manera dinámica el bus de hwmon que contiene el sensor real 'k10temp'.
    """
    rutas_name = glob.glob("/sys/class/hwmon/hwmon*/name")
    for ruta_name in rutas_name:
        try:
            with open(ruta_name, "r") as f:
                if "k10temp" in f.read():
                    ruta_temp = os.path.join(os.path.dirname(ruta_name), "temp1_input")
                    if os.path.exists(ruta_temp):
                        with open(ruta_temp, "r") as tf:
                            # Devuelve el valor en grados Celsius con precisión decimal
                            return float(tf.read().strip()) / 1000.0
        except IOError:
            continue
    return None # Si no hay sensor real, conmuta a NO_DATA (Honestidad de Sensores)
```

*   **Régimen de Guarda Térmica**:
    *   **$\ge$ 80.0°C**: Detiene inmediatamente las colas asíncronas de renderizado y limita las inferencias locales pausando hilos [512, 517].
    *   **$\le$ 72.0°C (Histéresis)**: Reanuda los workflows pendientes de forma segura [512, 517].
    *   **$\ge$ 90.0°C (Crítico)**: Descarga forzosamente los modelos de la RAM/VRAM matando el daemon de inferencia [512, 517].

### 2. Inferencia Solar Degradada (Presupuesto de Carbono)
*   **Voltaje $\ge$ 12.8V (`SOLAIRE_OK`)**: Funcionamiento normal de CineK y modelos pesados [512, 612].
*   **Voltaje < 12.8V (`EN_ATTENTE`)**: El decorador `@solo_si_hay_sol` de la API de FastAPI bloquea las colas de renderizado y devuelve un código de estado determinista `503 Service Unavailable` [512].
*   **Voltaje < 12.2V (Crítico)**: Inyecta el archivo de configuración degradada de Ollama (`OLLAMA_NUM_THREADS=2`) y reduce a 2 los hilos de CPU en los procesos de backend, bajando el consumo térmico y de vatios en tu batería Anker Solix C1000X [512, 517].

---

## PARTE IV: ARQUITECTURA DE PERSISTENCIA SEGURA (CAPA GOLD)

### 1. Mecanismo Atómico "Temp-and-Rename" contra Caídas de Tensión
Queda terminantemente prohibido abrir descriptores de archivos para escritura directa sobre archivos maestros. Si ocurre un fallo en caliente de alimentación en Beato, el archivo se corrompe. Aplica siempre esta función utilitaria de escritura a disco de coste cero:

```python
import os
import tempfile

def escritura_atomica(directorio_destino, nombre_archivo, contenido_utf8):
    """
    Escribe los datos de manera atómica en un archivo temporal intermedio
    en el mismo sistema de archivos físico, garantizando persistencia libre de corrupción.
    """
    fd, ruta_temp = tempfile.mkstemp(dir=directorio_destino, suffix=".tmp")
    try:
        with os.fdopen(fd, 'w', encoding='utf-8') as tmp_file:
            tmp_file.write(contenido_utf8)
            tmp_file.flush()
            # Fuerza al kernel del SO a vaciar el búfer físico de caché a disco
            os.fsync(tmp_file.fileno())
            
        ruta_destino = os.path.join(directorio_destino, nombre_archivo)
        # Primitiva atómica del sistema operativo (mismo FS): cambia el puntero de inodo
        os.replace(ruta_temp, ruta_destino)
        
        # Sincroniza el directorio padre para asegurar el registro en la tabla FAT/ext4
        dir_fd = os.open(directorio_destino, os.O_RDONLY)
        try:
            os.fsync(dir_fd)
        finally:
            os.close(dir_fd)
            
    except Exception as e:
        if os.path.exists(ruta_temp):
            os.remove(ruta_temp)
        raise e
```

### 2. Estructura de Conflictos: HLC + CRDT (`Worktrees`)
Para sincronizar repositorios locales o engramas del diario en escenarios sin internet (offline-first), desterra los timestamps del sistema operativo (propensos a derivas térmicas y desajustes de zona horaria) [120, 201]. Utiliza un reloj lógico híbrido **Hybrid Logical Clock (HLC)** compuesto por:

$$\text{HLC} = \{\text{physical\_ms}, \text{logical\_counter}\}$$

*   **LWW-Element-Set CRDT (Last-Write-Wins)** [171, 180, 251]:
    *   Al fusionar dos ramas del diario (`Le Cahier`), compara los HLC de las entradas [171, 251].
    *   Gana la entrada que posea el HLC mayor [171, 251].
    *   Si los HLC son idénticos (empate absoluto), desempata calculando el checksum SHA-256 de los contenidos [171, 251].
    *   El proceso es completamente reproducible e idempotente de forma local, sin requerir una base de datos de coordinación central [171, 251].

---

## PARTE V: CHECKLIST DE VERIFICACIÓN CRIPTO-FÍSICA (VERIFY_POW.SH)

Al arrancar el sistema paralelo, el script de arranque `verify_pow.sh` actúa como la cerradura lógica en frío del nodo. Debe validar la integridad total bajo la siguiente secuencia síncrona [83, 122]:

1.  **[ ] Verificación del Manifiesto de Dependencias (ABM)**: Lee el archivo `aurelius.abm` y valida que los hashes SHA-256 de los paquetes instalados en el entorno virtual correspondan exactamente con la lista de firmas autorizadas [122, 281].
2.  **[ ] Auditoría de Firmas de Capa Gold**: Comprueba la firma asimétrica detached `.sig` de la base de datos de configuraciones contra tu clave pública Ed25519 en frío [83, 122]. Si hay discrepancias, aborta inmediatamente (`exit code 1`) [122].
3.  **[ ] Prueba Relacional SQLite**: Ejecuta `PRAGMA integrity_check` sobre la base unificada de SQLite WAL para descartar corrupciones lógicas físicas de la NVMe [122].
4.  **[ ] Bloqueo de Interfaces Físicas**: Verifica que las APIs expuestas están amarradas exclusivamente a la dirección virtual de Tailscale `[IP_TAILNET_REDACTADA]:8050` o interfaces loopback, abortando si detecta escucha activa en interfaces cableadas o inalámbricas abiertas [538, 540].
