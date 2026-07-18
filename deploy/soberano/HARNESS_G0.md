# Candidatos de harness · instalados en Misión G0 (2026-07-18)

Instalación + smoke test únicamente. **La comparativa de los 5 misiones queda para la Misión G1**
— no se adelanta aquí.

## Instalación (todo en espacio de usuario, sin sudo)

- **Node 24 LTS** vía `nvm` (`~/.nvm`) — requerido por Qwen Code y OpenCode.
- **Qwen Code**: `npm install -g @qwen-code/qwen-code@latest` → binario `qwen`. `npm` bloqueó por
  seguridad (`allow-scripts`) el install script de `@qwen-code/audio-capture` (captura de audio,
  no necesaria para smoke test de texto) — se dejó sin aprobar, decisión deliberada.
- **OpenCode**: `curl -fsSL https://opencode.ai/install | bash` (instalador oficial) → binario en
  `~/.opencode/bin`.
- **Aider**: `uv tool install --force --python python3.12 --with pip aider-chat@latest` (método
  recomendado oficialmente) → binario `aider`.

## Configuración contra Ollama local (`soberano-coder`)

- **Aider**: `OLLAMA_API_BASE=http://127.0.0.1:11434 aider --model ollama/soberano-coder`.
- **OpenCode**: `~/.config/opencode/opencode.json`, provider `ollama` vía
  `@ai-sdk/openai-compatible` sobre `http://127.0.0.1:11434/v1` (config completa en este mismo
  directorio no se versiona por ser config de usuario, no de proyecto — reproducible con el JSON
  documentado abajo).
- **Qwen Code**: variables de entorno `OPENAI_API_KEY=ollama OPENAI_BASE_URL=http://127.0.0.1:11434/v1
  OPENAI_MODEL=soberano-coder` (es un fork de Gemini CLI que soporta cualquier endpoint
  OpenAI-compatible).

```json
// ~/.config/opencode/opencode.json
{
  "$schema": "https://opencode.ai/config.json",
  "provider": {
    "ollama": {
      "npm": "@ai-sdk/openai-compatible",
      "name": "Ollama (soberano, local)",
      "options": { "baseURL": "http://127.0.0.1:11434/v1" },
      "models": { "soberano-coder": { "name": "soberano-coder (qwen3-coder:30b)" } }
    }
  }
}
```

## Smoke test (prompt trivial: "Responde solo con la palabra OK si me lees.")

| Harness | Resultado | Tamaño real del prompt (system+user) | Nota |
|---|---|---|---|
| Aider | ✅ "OK" | ~600 tokens | Rápido, prompt de sistema ligero |
| OpenCode | ✅ "OK" | ~7 100 tokens | `opencode run` inyecta system prompt grande (herramientas/agente) |
| Qwen Code | ✅ "OK" | ~15 000 tokens | System prompt aún mayor; primer intento con timeout de 120s no alcanzó a terminar en CPU |

**Dato relevante para el Bloque D**: los tres corrieron sobre **CPU** (Vulkan aún no activado en
Ollama — ver `BENCH_G0.md`). Con prompts de sistema de 7-15k tokens y `pp512≈100 tok/s` en CPU
medido en el bench, el primer turno de OpenCode/Qwen Code tarda 60-120s solo en prompt processing.
Con Vulkan (`OLLAMA_IGPU_ENABLE=1`, pendiente de sudo) ese mismo prompt debería procesar en
~3.5× menos tiempo por el bench del Bloque D — haría estos harnesses notablemente más usables en
uso interactivo real.
