# Reporte · Misión G1-R — La Segunda Mirada (y la voz única)
### Nodo `soberano` · Claude Code · 2026-07-19

---

## Estado real vs plan

Los seis bloques (A→F) se completaron. Ningún gate se cruzó por decreto — la regla de decisión
del Bloque C se aplicó tal cual quedó pre-registrada, incluso cuando el resultado no fue el
esperado.

### Bloque A · Registro y estado

- **#29 superseded**: muere el mapa agente→voz (decisión del Soberano). Mitad viva (pre-síntesis
  + cache) reimplementada single-voice en el Bloque D.
- **9 sugerencias vigentes (#103-111)** marcadas aprobada/aprobada-pendiente-carbono vía relevo
  del Preceptor (interpretación de "vigentes" = las de los dos últimos reportes; declarada
  explícitamente por si no era la lectura correcta).
- **Verificación de estado real — hallazgo importante**: el intento de David de canonizar la fila
  de la Orquesta (`git apply` + commit `f7ceea6`) **falló silenciosamente** — `git apply` dio
  "corrupt patch" pero el commit se hizo igual (solo trackeó el `.patch` como archivo, el
  `.md` de doctrina nunca cambió). Causa raíz corregida por CC (`15ffc7c`: faltaba una línea de
  contexto en blanco), re-verificado `git apply --check` OK. **#95/#103 siguen abiertas** —
  esperando que David reintente.
- `PROPUESTA_28` (fix del scraper): **no desplegada** — mismo 422 reproducido verbatim.
- `#98` (referencia rota en delta aceptado): **sigue sin corregir**, verificado contra el delta
  real vía API.

### Bloque B · Correcciones #104-107

- **#104**: hipótesis original (transición Ollama/`NUM_PARALLEL=1`) **refutada empíricamente**
  (2 y 4 llamadas consecutivas sin pausa, cero fallos). Causa raíz real no identificada — el
  evento fue transitorio y raro. Mitigación barata aplicada igual: detección+reintento en el
  runner del re-test.
- **#105/#106/#107**: reforzados en `~/.config/opencode/AGENTS.md` (versionado en
  `deploy/soberano/opencode_AGENTS.md`) — convención de credenciales por entorno, uso de campos
  ya calculados, `git status --short` en vez de `git diff --quiet`.

### Bloque C · Re-test EVAL_GROUNDING_G2 (regla pre-registrada, aplicada tal cual)

**Resultado: 5/10 — no aprueba** (umbral ≥8/10). Backend Vulkan confirmado activo toda la prueba.

| Test | Veredicto | Nota |
|---|---|---|
| T1 servicios | ❌ | Recaída real en #102: 2 métodos, mismo punto ciego |
| T2 backend | ❌ | Alucinación nueva: afirma CUDA/NVIDIA, es Vulkan/AMD |
| T3 bench | ❌ | Usó el campo correcto pero no entendió "multiplicador" (reportó "1") |
| T4 derivado | ✅ | Perfecto, exacto |
| T5 búsqueda | ❌ | Sin respuesta final (mismo patrón que la eval original) |
| T6 cita | ✅ | Exacta |
| T7 Qdrant | ✅ | Encontró la credencial vía `env` — corrección #107 funcionó |
| T8 negativo | ✅ | Doble método limpio |
| T9 git | ✅ | `git status --porcelain`, correcto y verificado en tiempo real |
| T10 sin dato | ❌ | Bloqueado por permiso del sandbox, sin caer en "sin dato" |

Por la regla pre-registrada (recaída real en clase #102 → prueba de Aider), se ejecutó una
subprueba de Aider con acceso real (`--read` + `--chat-mode ask`, en vez del modo edición por
defecto que — hallazgo de fricción real — intentó *crear un archivo* ante una pregunta de
solo-lectura, limpiado sin commitear):

| Test | Veredicto | Nota |
|---|---|---|
| T3 (con `--read`) | ✅ | Multiplicadores exactos |
| T4 (con `--read`) | ❌ | Emparejó mal los campos (tg128 Vulkan ÷ pp512 CPU) |
| T6 (con `--read`) | ✅ | Cita exacta |
| T8 (sin herramientas) | honesto | Declaró no poder verificar — grounding correcto, tarea no completable (sin shell) |

**Ninguno de los dos harnesses alcanza aprobación limpia.** La regla pre-registrada no cubre
explícitamente qué hacer si Aider *tampoco* aprueba — se deja para que David/el Preceptor decidan
el siguiente paso en vez de que CC improvise una regla nueva no pactada.

### Bloque D · Voz única de HEXELION

`voz_api.py`: `VOZ_ACTIVA` (config de una línea, default `davefx` por Gate 0) reemplaza la
elección de voz por el llamante — el endpoint ignora cualquier `voz` del cliente. Núcleo de
síntesis compartido (`_obtener_wav`) entre el endpoint HTTP y la nueva `presintetizar()`
fire-and-forget, enganchada en 3 puntos de `hexelion_gateway.py` (Sínodo ×2, indoor/Jardin ×2 —
requirió añadir acumulación de texto que no existía ahí). `py_compile` limpio en ambos archivos.
**No desplegado** — sin acceso a torre/fragua desde `soberano`; comandos y verificación E2E
documentados en `deploy/soberano/VOZ_UNICA_G1R.md`.

### Bloque E · Linaje #108 — corrección honesta

Verificados los identificadores concretos del handoff del 14-jul contra todo el repo real: **cero
coincidencias**. La afirmación de "alta confianza" del reporte de El Yacimiento era prematura —
corregida en `deploy/soberano/LINAJE_G1R_BLOQUE_E.md`. Hallazgo más importante y más urgente que
el original: **el código fuente real del dashboard/Jardin en producción no está versionado en
git** (`dashboard/` solo tiene caché de Vite) — riesgo real de pérdida total.

## Riesgos / desviaciones declaradas

- Interpretación propia de "las 9 sugerencias vigentes" (declarada explícitamente en Bloque A,
  corregible por el Preceptor/David si no era la lectura correcta).
- #104 quedó sin causa raíz confirmada — solo refutada la hipótesis original.
- Los cambios de código del Bloque D no se probaron en vivo (sin acceso a fragua/torre).
- El Bloque E corrige una afirmación propia anterior (El Yacimiento) — declarado explícitamente,
  no se ocultó el error.

## Qué necesita la mano de David

1. Reintentar `git apply mente/auditorias/PROPUESTA_29_orquesta_soberano.patch` + commit (ya
   corregido y verificado por CC).
2. Decidir el siguiente paso tras el resultado 5/10 + subprueba de Aider (la regla pre-registrada
   no cubre este caso exacto).
3. Desplegar la voz única (`deploy/soberano/VOZ_UNICA_G1R.md`) y `PROPUESTA_28` en fragua.
4. **Urgente (nuevo, Bloque E)**: decidir cómo versionar el código fuente real del dashboard/Jardin
   antes de que se pierda como ya pasó una vez (`6a4bb3f`).
5. Ventilación física de fragua, elección definitiva de voz Piper (queda en `davefx` hasta que
   decida), ACCEPT del delta Bambu.

---

## SUGERENCIAS

112. **Investigar por qué OpenCode a veces no da respuesta final tras usar herramientas** (T5 en
     ambas evals, T2 original) — patrón recurrente distinto de "connection refused", posiblemente
     relacionado con cómo cierra el turno tras una secuencia larga de tool calls. [prio:alta] S
113. **Añadir verificación cruzada de hardware antes de nombrar un backend** (T2: CUDA/NVIDIA
     inventado sobre Vulkan/AMD real) — instrucción tipo "no asumas el fabricante del backend sin
     verificarlo con una segunda fuente (lspci, journalctl)". [prio:media] S
114. **Decidir la puerta post-5/10**: la regla pre-registrada de G1-R no cubre "OpenCode no
     aprueba Y Aider tampoco" — falta una regla explícita para este caso antes de la próxima eval.
     [prio:alta] S
115. **Versionar el código fuente real del dashboard/Jardin de producción** (hallazgo del Bloque
     E) antes de que se repita una pérdida como `6a4bb3f`. [prio:alta] M

---

**PARA.** No se inicia G2 ni ninguna misión nueva — ningún commit de fila llegó, ningún harness
aprobó limpio.
