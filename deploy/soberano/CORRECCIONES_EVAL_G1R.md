# Correcciones aplicadas antes del re-test · Misión G1-R, Bloque B (2026-07-19)

## #104 · `connection refused` entre invocaciones

**Hipótesis original** (EVAL_GROUNDING_G2): transición de Ollama con `OLLAMA_NUM_PARALLEL=1` al
recibir una conexión inmediatamente tras la anterior.

**Test empírico**: 2 llamadas consecutivas sin pausa (rc=0 ambas, sin error) + 4 llamadas rápidas
seguidas sin pausa (rc=0 las 4, sin error nuevo en `opencode.log`). **Hipótesis refutada** — no se
reproduce por timing de invocación simple. `OLLAMA_KEEP_ALIVE=5m0s`, `OLLAMA_MAX_QUEUE=512`: con
esos valores, `NUM_PARALLEL=1` debería encolar una segunda petición, no rechazarla a nivel TCP.

**Conclusión honesta**: el evento fue transitorio y raro (1 ocurrencia en ~25 invocaciones totales
entre el duelo de G1, la eval y estas pruebas) — causa raíz no identificada con certeza. Se aplica
de todos modos una mitigación barata sin coste real: el runner del re-test (Bloque C) añade
detección de `connection refused` en el log y, si aparece, **no cuenta contra el harness** (per la
regla del propio brief: "si reaparece connection refused → se PARA y se re-diagnostica
infraestructura").

## #105 · Patrón #102 por tarea, no solo `AGENTS.md` global

Confirmado en G1-R que `AGENTS.md` global SÍ se carga (funcionó en T8), pero se ignora bajo presión
de tarea (T1, T9). Añadida sección específica a `~/.config/opencode/AGENTS.md` con el caso exacto
que falló en T9 (`git status --short`, no solo `git diff --quiet`) como ejemplo concreto — más
efectivo que una regla abstracta.

## #106 · Imprecisión numérica recurrente

Añadida sección a `AGENTS.md`: usar campos ya calculados tal cual, nunca derivar de otros campos
relacionados; exigir auto-consistencia entre respuestas que citen la misma cifra.

## #107 · Credenciales por configuración estándar del harness

**No se tocó el prompt de la eval** (correcto per el veredicto del Soberano: un eval que insinúa
credenciales no mide nada). Se corrigió el **entorno operativo** del harness: `AGENTS.md` ahora
documenta la convención `<SERVICIO>_API_KEY` como variable de entorno y instruye comprobar `env`
antes de reportar "sin acceso" — exactamente como cualquier operario nuevo conocería dónde están
sus credenciales por convención de la casa, no por adivinanza.
