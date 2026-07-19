# La voz única de HEXELION · Misión G1-R, Bloque D (2026-07-19)

## Decisión del Soberano (19-jul, relevada por el Preceptor)

Muere el mapa agente→voz de la SUGERENCIA #29 (cada voz del Sínodo con un Piper distinto). **UNA
sola voz para HEXELION.** Los contratos de grounding por dominio de las 6 voces del Sínodo
(Monje, Alquimista, Escriba, Vocero, Berserker, Enlace — Doctrina AI Interna §6) **siguen
intactos**: esto unifica la garganta, no la ley de qué puede decir cada una.

Se conserva la mitad viva de #29: pre-síntesis en background + cache por hash — ya existía
parcialmente (`voz_api.py` ya cacheaba por `sha256(voz|texto)`), lo que faltaba era **disparar**
la síntesis al llegar la respuesta del chat, no solo al pulsar ▶.

## Qué ya existía (verificado, no reinventado)

- `POST /api/voz/sintetizar` — cadena cache→residente→frío, 100% local, ya en producción
  (`hexelion/voz_api.py`, misión VENTANA VIVA B4 / #21).
- El botón ▶ en `dashboard-v9/sinodo.html` (`playVoz()`) — **ya llama al endpoint sin mandar
  `voz`**, es decir, en la práctica ya usaba una sola voz (la default) desde el frontend. No hubo
  que tocar el HTML.
- `davefx` ya era la default, con la razón medida en el propio docstring (Gate 0: 17% más pequeño,
  ~44MB menos RSS pico que `sharvard`).

## Qué se construyó en esta misión

1. **`VOZ_ACTIVA`** (`voz_api.py`): config de despliegue de una línea (`os.environ.get`), no
   elección del llamante. El endpoint `/api/voz/sintetizar` ahora **ignora** cualquier `voz` que
   mande el cliente y usa siempre `VOZ_ACTIVA` — imposible que un cliente futuro reintroduzca el
   mapa agente→voz sin querer. Ambos modelos (`davefx`, `sharvard`) siguen instalados; cambiar de
   voz es una variable de entorno + restart, cero código.
2. **`_obtener_wav()`**: la cadena cache→residente→frío se extrajo a una función compartida, para
   que el endpoint HTTP y la pre-síntesis en background usen exactamente la misma vía — sin
   duplicar lógica que pudiera divergir.
3. **`presintetizar(texto)`**: nueva función fire-and-forget. Se llama con `asyncio.create_task()`
   en **3 puntos** de `hexelion_gateway.py`, justo cuando el chat tiene su respuesta completa:
   - `sinodo_v2_chat_stream` — camino torre (éxito) y camino fragua (fallback), las 6 voces del
     Sínodo.
   - `indoor_chat` (Le Jardin / El Watchman) — camino torre y camino fragua (tuvo que añadirse la
     acumulación de `full_reply`, que antes no existía ahí).
   - Nunca puede tumbar ni ralentizar el chat: cualquier excepción se traga en silencio (es una
     optimización de latencia percibida, no una garantía).

## Verificación hecha (sin poder desplegar)

- `python3 -m py_compile` limpio en ambos archivos modificados.
- Revisión manual de los 3 puntos de inserción: cada uno ocurre solo cuando `done=True` y el
  stream tiene contenido real, antes del `return`/fin del generador.
- **No se pudo probar en vivo** — sin acceso a torre/fragua/Redis/Ollama de producción desde
  `soberano`. Doctrina AI Interna §4.3: el despliegue y su verificación E2E son mano de David o de
  una sesión CC en `la-fragua`.

## Despliegue (mano de David o CC-fragua)

```bash
cd /mnt/nvme/p0x/hexelion  # o donde viva el checkout real en fragua
git pull origin nexo-carbono-dashboard-20260623   # o la rama que fragua tenga desplegada — CONFIRMAR CUÁL ES
sudo systemctl restart hexelion-gateway   # recarga voz_api.py y hexelion_gateway.py
# opcional, para cambiar de voz sin tocar código:
#   añadir Environment="VOZ_ACTIVA=sharvard" al unit o su .env, luego restart
```

**Verificación E2E propuesta tras desplegar**: lanzar una pregunta al Sínodo desde el dashboard,
esperar a que termine de responder, y comprobar (sin pulsar ▶ todavía) que
`mente/telemetria/voz.jsonl` ya tiene una entrada nueva con `cache_hit:false` justo después del
`done` del chat — eso confirma que la pre-síntesis disparó sola. Luego pulsar ▶ y confirmar
latencia baja (debería leer de CACHE, `cache_hit:true` si se repite la telemetría).
