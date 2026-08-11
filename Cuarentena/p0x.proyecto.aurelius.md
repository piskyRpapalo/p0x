# 🏛️ SPECIFICATION MASTER FILE: p0x.proyecto.aurelius
> **SYSTEM_METADATA:**
> *   **Namespace:** `p0x.proyecto.aurelius`
> *   **Version:** `2.0-Aurelius-Skills`
> *   **Status:** Audited and Unified for Cognitive AI Training
> *   **Date:** 2026-08-08
> *   **Editor:** AI Redactora Experta en Lenguaje AI (G.R.I.D. Protocol)
> *   **Classification:** Aurelius Skills, Learning Architecture & Pedagogical Scaffolding

---

## 🥉 CAPA BRONCE (FUNDAMENTOS DEL APRENDIZAJE SOBERANO - ROUND 1)

### 1. B.01: Perfiles de Configuración (PRO / LITE) [167]
El servidor de backend acepta el argumento CLI `--perfil` al arrancar. Carga `config.lite.json` (para hardware de 8 GB RAM, restringiendo puertos a localhost) o `config.pro.json` (para hardware avanzado de 32+ GB, abriendo escucha a la red Tailscale privada) [167].

### 2. B.02 & B.03: Declaración Honesta y Capabilities API [168]
*   **B.02**: Consulta activamente a Ollama (`/api/tags`) para verificar el modelo real cargado y expone su topología: `SOBERANO` (local), `DELEGADO` (red privada) o `HUESPED` (terceros en la nube) [168].
*   **B.03**: El endpoint `/api/capabilities` expone al frontend las capacidades detectadas del silicio en caliente, adaptando la interfaz dinámicamente [168].

### 3. B.04 & B.05: Honest Math y Portapapeles Soberano [169]
*   **B.04**: Prohíbe de forma absoluta ejecutar código generado por el LLM. Todo cálculo matemático se extrae en backend a un parser AST determinista en Python puro (módulo `ast`) [169].
*   **B.05**: Retira los botones de copiado de un solo clic en las cajas de comandos. El Soberano debe seleccionar manualmente el texto y pulsar `Ctrl+C` para forzar la auditoría visual previa de cada instrucción [169].

### 4. B.06: Command Guard (El Firewall Cognitivo) [170]
El LLM no valida la seguridad. El backend corre un parser determinista (regex + lista negra de comandos peligrosos como `rm -rf`, `sudo`, `curl | bash`, etc.). Si hay riesgo, bloquea el renderizado y envuelve el código en una advertencia roja de peligro, delegando la decisión en el operador [170].

### 5. B.07 a B.10: Telemetría, Caché y Scaffolding [170, 171]
*   **B.07**: Monitorea de forma continua la temperatura de la CPU Ryzen (vía `k10temp`) y el uso de RAM, emitiendo alertas pasivas [170].
*   **B.08**: Almacena embeddings generados en un JSONL simple (`cache_embeddings.jsonl`) indexado por hashes SHA-256 para evitar reprocesamientos redundantes en CPU [171].
*   **B.09**: Permite la ingesta granular de snippets personales buscables mediante coincidencia de texto [171].
*   **B.10**: Retira gradualmente los andamios o explicaciones pedagógicas de la UI a medida que el Soberano supera las misiones M0 a M7 [171].

---

## 🥈 CAPA PLATA (VINCULACIÓN COGNITIVA & EVALUACIÓN DUAL - ROUND 2 & 3)

### 1. B.11 a B.13: Diálogos Críticos y Senda de Rechazos [172, 173]
*   **B.11 (Espejo de Sócrates)**: Modo de conversación donde Aurelius prohíbe dar respuestas directas, guiando al Soberano mediante preguntas reflexivas en un límite estricto de 5 intercambios [172].
*   **B.12 (Focus Pact)**: El usuario bloquea una intención con duración temporal. El sistema monitorea los inodos y archivos modificados en caliente y genera un informe de discrepancia temática al finalizar [172].
*   **B.13 (Senda de los Muertos)**: Guarda las propuestas técnicas rechazadas en `dead_path.jsonl`. Al acumular 5 rechazos de un mismo tema, emite una alerta no valorativa para confrontar al operador con sus propios patrones de evasión acumulada [173].

### 2. P.02: Generador de ADRs (Architecture Decision Records) [179]
Identifica patrones y decisiones tomadas en caliente durante las sesiones de chat del mes y compila un borrador de ADR en formato estructurado de Markdown usando plantillas Jinja2 [179].

### 3. P.08: La Forja (Rito de Evaluación Dual) [182]
Evaluación asíncrona obligatoria para subir de nivel de misión (M0-M7). Ejecuta dos validaciones complementarias en local [182]:
*   **Validación Técnica (Dura)**: Exige una similitud de coseno $> 0.75$ comparando embeddings locales (`nomic-embed-text`) contra los criterios objetivos [182].
*   **Validación Conceptual (Blanda)**: Para textos superiores a 500 caracteres, mide la diversidad léxica en $O(N)$ mediante entropía de vocabulario:
    $$	ext{Ratio de Entropía} = rac{	ext{Palabras Únicas}}{	ext{Palabras Totales}} > 0.4$$
*   **Sello**: Si aprueba ambas, genera una prueba de conocimiento firmada con Ed25519 (`PoK`) [182].

---

## 🥇 CAPA GOLD (NOTARÍA CRIPTOGRÁFICA & CONFLICTOS CRDT)

### 1. O.01 a O.03: Credenciales e Identidad Unificada [184, 185]
*   **O.01 (PoK Verificable)**: Permite verificar de forma local y offline la legitimidad de un conocimiento o nivel adquirido comparando firmas Ed25519, sin fugar el texto crudo del diario [184].
*   **O.03 (Thin Client)**: Mantiene la identidad unificada de tus dispositivos de red. Un terminal LITE (portátil) hereda el contexto de inferencia y las credenciales de Gold de tu terminal PRO de Beato vía Tailscale de forma instantánea [185].

### 2. O.05 & O.06: Portabilidad y Sello Diferido [186]
*   **O.05**: Cifra y empaqueta recursivamente la base relacional Gold y logs de Bronze mediante AES-256-GCM y PBKDF2 basándose en tu frase de recuperación física en frío (sin cloud) [186].
*   **O.06 (Sello Diferido)**: Permite cifrar una nota privada con un candado de tiempo criptográfico. La clave de descifrado no depende del reloj de la máquina (manipulable), sino que se deriva del hash futuro del ledger Gold, siendo ilegible hasta que la cadena relacional haya crecido un número exacto de bloques previstos [186].
