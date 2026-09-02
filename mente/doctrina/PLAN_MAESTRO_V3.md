# PLAN MAESTRO V3 — LIBERACIÓN PÚBLICA (Firmado 2026-09-02)

## ESTADO DEL SISTEMA (Ground Truth Medida)
El sistema está sólido y limpio. 3 capas operativas:
1. WEB (preceptoros.org): 8 páginas, SEO, PWA, Community, Profile. (HTML/CSS/JS vainilla, tope 10.240 B).
2. APP MVP (:8740): 590 tests. Endpoints vivos: /api/anidar (Aduana funciona), /api/metricas (Banco de Pruebas vivo), /api/cerebro (Selector de LoRA), /api/perfil (Huella SHA256). Python stdlib only.
3. OJO (:8790): Save Game funcional, 41 entradas en glosario, Ojo-Vivo V5 pixel-art.

## DECISIÓN DE DISEÑO: CARAS Y SPRITES APARCADOS
Los sprites de bustos y ojos (preceptor-up-v2.webp, etc.) necesitan trabajo de arte y no están pulidos. Se aparcan hasta nuevo aviso. El sistema usará los backups antiguos (aurelius-up.png / seal-*.gif) mientras tanto. **NO tocar CSS de animaciones ni JS de selección de avatar en esta fase.**

## LOS 3 ÚNICOS BLOQUEANTES PARA LIBERAR AL PÚBLICO
1. REENTRENAR LORA: El modelo qwen3:4b tiene bug Thinking. Hay que reentrenar el LoRA Caza-Nido sobre `llama3.2:3b` (no-thinking) y recrearlo en Ollama.
2. TÚNEL PERSISTENTE: Falta `cloudflared.service` en la-fragua para que el túnel no muera al reiniciar.
3. ENDPOINTS EN LA-FRAGUA: `agora_api.py` necesita rutas `/api/v1/profiles` (GET/POST) y `/api/v1/threads` (GET) para que profile.html y community.html funcionen de verdad.
