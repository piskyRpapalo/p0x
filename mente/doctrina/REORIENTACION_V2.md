# REORIENTACIÓN ESTRATÉGICA DEL ECOSISTEMA SOBERANO (v2.0)

**Fecha de firma:** 2026-09-01
**Versión:** 2.0 (Canon activo)
**Firmado por:** El Soberano

Este documento establece la nueva dirección del proyecto, fusionando la realidad física del hardware, las lecciones de la Necrópolis y la nueva doctrina comercial y técnica "Caza-Nido". No contiene código; es el mapa mental y operativo que guiará todas las decisiones futuras.

## 1. EL NUEVO PARADIGMA: DOCTRINA CAZA-NIDO (EDGE AI CONSULTING)

El ecosistema deja de intentar competir con los modelos gigantes de la nube. En su lugar, los esclaviza. El valor ya no está en generar texto desde cero, sino en la soberanía del dato, la privacidad y la estructura.

El modelo operativo es el **"Agente Pequeño Guía"**. Dado que el hardware local no puede entrenar ni ejecutar eficientemente modelos masivos, el LoRA local (4B parámetros) actúa como un portero y un arquitecto. Su función es:

- Intercepta la petición del usuario.
- Si requiere conocimiento externo o generación masiva, declara `NO_DATA` y ordena al usuario "cazar" esa información en una IA externa (Gemini, ChatGPT).
- Cuando el usuario trae el texto crudo, el Agente Local aplica el filtro de privacidad (`guardrails.py`), tacha datos sensibles, estructura la información y la anida en el Second Brain local (SQLite).
- El usuario obtiene una IA personalizada, offline, que conoce su contexto, sin que sus datos privados hayan alimentado a un modelo externo.

## 2. LA VERDAD DEL SILICIO (HARDWARE ACTIVO Y SUS LÍMITES)

La arquitectura se adapta estrictamente a lo que el metal puede hacer sin alucinar capacidades:

- **Soberano Principal (Beelink SER9 Max):** 64 GB RAM, CPU pura. Es el cerebro de orquestación, el gateway FastAPI y el motor de inferencia CPU (Ollama). Aquí se entrena y sirve el LoRA guía en ~9 minutos.
- **La Torre (Jetson Orin Nano Super 8GB):** 67 TOPS, pero con un techo real de ~2 GB de modelo por limitación de VRAM. Se usa exclusivamente para inferencia CUDA de modelos pequeños y específicos, no para entrenamiento de modelos grandes.
- **La Fragua (Orange Pi 5 Plus) y El Vigía (Raspberry Pi):** Nodos de adquisición de radiofrecuencia (ADS-B y AIS) y telemetría. Operan bajo la regla "propose-only": el Soberano no ejecuta cambios en ellos por SSH sin una firma explícita.
- **Energía:** El rack opera con una declaración verificada de 99% solar (Aiko Neostar3 + Anker Solix + UPS onda senoidal), medido en vatios por el Nous A1T.

## 3. ARQUITECTURA DE SOFTWARE (LÍMITES INQUEBRANTABLES)

- **Cero dependencias pesadas en el MVP:** Python stdlib únicamente. Nada de Electron, Go o frameworks que consuman cientos de megabytes de RAM en reposo.
- **Base de datos:** SQLite con `journal_mode=WAL` e índice FTS5. Es la única fuente de verdad de la memoria.
- **Red:** Comunicación estricta por loopback (127.0.0.1) o mTLS sobre Tailscale/Yggdrasil. La web pública nunca hace fetch directo a IPs locales; el MVP sanea antes de cualquier exportación.
- **Identidad:** Ed25519. Pseudónima, no extraíble, cero PII.
- **El Ojo del Soberano:** Solo pinta, no mide. Recibe el estado de `recolector.py` y lo visualiza. Si un dato falta, muestra `NO_DATA` con causa, nunca un cero decorativo.

## 4. EL FLUJO DE VALOR (CÓMO FUNCIONA AHORA)

1. **Captura:** El usuario interactúa con la App MVP. El sistema registra la intención.
2. **Delegación Soberana:** Si la tarea excede las capacidades locales, el sistema instruye al usuario sobre qué pedir a la nube y cómo traerlo de vuelta.
3. **La Aduana:** El texto importado pasa por `guardrails.py`. IPs, correos y datos personales son tachados automáticamente antes de tocar el disco.
4. **Anidamiento:** El Agente Local (Archivero/Estratega) toma el texto saneado, lo vincula con el contexto existente y lo guarda en la memoria local.
5. **Banco de Pruebas:** El usuario puede verificar en tiempo real el rendimiento (tokens/s, RAM, latencia) de su modelo local, convirtiendo la métrica técnica en una herramienta de confianza y venta.

## 5. LA NECRÓPOLIS (LO QUE YA NO EXISTE Y POR QUÉ)

El cementerio de tecnologías define tanto el proyecto como el código activo. Se recuerda para no repetir errores:

- **Electron y Go:** Vetados por consumo de RAM e ineficiencia en ARM.
- **Google Coral:** Devuelto por limitaciones de hardware; reemplazado por la Jetson Orin Nano.
- **immudb:** Descartado por los picos térmicos de su garbage collector en ARM; reemplazado por triggers nativos de Merkle Hash en SQLite.
- **Flask monohilo:** Reemplazado por FastAPI asíncrono para evitar bloqueos en la pila TCP.
- **localStorage como única persistencia:** Vetado. La verdad vive en el rack; el navegador es solo un buffer offline de reconciliación.

## 6. HOJA DE RUTA INMEDIATA (PRÓXIMOS PASOS)

- **Mapeo de Agentes:** Consolidar en la interfaz web la traducción de los 8 IDs del túnel (instalador, privacidad, etc.) a los 6 roles de la doctrina Caza-Nido (guía, filtro, analista, archivero, cronista, estratega), usando SVG sprites para ahorrar peso.
- **UI del Banco de Pruebas:** Finalizar el panel en el MVP que muestre las métricas de rendimiento en vivo, validando la promesa de "funciona en tu máquina".
- **Blindaje del Túnel:** Asegurar que la API de la Fragua (`agora_api`) tenga CORS estricto y que el servicio `cloudflared` esté correctamente enrutado y monitorizado.
- **Automatización del Entrenamiento:** Dejar el script de entrenamiento LoRA en CPU (`entrenar_lora.py`) listo para ser ejecutado con un solo comando, generando el adaptador `.gguf` que se inyectará en el Ollama del cliente.

## 7. MANIFIESTO FINAL

Esta reorientación convierte una limitación técnica (no poder correr modelos gigantes) en la mayor ventaja competitiva: privacidad absoluta, costos operativos nulos y un control total del conocimiento por parte del usuario final.

**La máquina gana siempre, pero ahora, la máquina trabaja para el usuario, no para la nube.**
