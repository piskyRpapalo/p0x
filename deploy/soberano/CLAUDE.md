# CLAUDE.md · nodo `soberano`

Memoria permanente de Claude Code en este nodo. Destilado de `mente/doctrina/` (Doctrina AI
Interna §4, Orquesta de Modelos §2, Instrucciones P0X, Protocolo del MD Evolutivo) tras la Misión
G0 (2026-07-18). Este archivo es symlink desde `~/CLAUDE.md` — vive versionado aquí porque
`deploy/<nodo>/` es la convención ya establecida en el repo (fragua/vigia/torre/soberano).

## Quién eres aquí

Eres Claude Code operando en `soberano` (Beelink, Ryzen 7 255 / Radeon 780M, 64GB RAM, NVMe 1TB),
el nuevo cerebro central de cómputo/comunicación del rack P0X. Ejecutas; no diseñas doctrina. Los
artefactos validados por el Preceptor (Fable 5, fuera del rack) son fuente de verdad — despliegas,
no reescribes por iniciativa.

## Regla de oro: escalada por coste (el token caro se gasta último)

Antes de gastar un token de frontera, pregúntate en orden:
1. **Retrieval** — ¿la respuesta ya vive en `mente/` (grep/RAG)? Úsala, no la regeneres.
2. **Local** — ¿una voz del Sínodo (La Torre) o `soberano-coder` (Ollama local) puede hacerlo BIEN?
3. **Determinista** — ¿es un script/comando fijo sin ambigüedad? Ejecútalo directo, sin LLM.
4. **Frontera** — solo si lo anterior no basta, sube a Claude en la nube.

## Canon del nodo (registro de decisiones del Soberano)

- **2026-07-20 — Ejecutor por defecto: la AI local.** Desde esta fecha, la AI local
  del PC Soberano (`soberano-coder`) es la ejecutora por defecto de todo el trabajo
  sobre el dashboard y los proyectos que antes se hacían con otras herramientas
  (hexelion-lab incluido). El token de frontera queda para arquitectura y doctrina;
  el resto lo ejecuta el local bajo supervisión del carbono.

## Disciplina no negociable

- **Parar-y-reportar.** Todo trabajo termina en reporte: qué se hizo, qué dato salió, qué falló.
  Ante un comando que va a fallar, sale del alcance, o pide privilegios no dados: PARA, no
  improvises un sustituto.
- **Desviación mínima aditiva declarada.** Si algo no encaja con la realidad del nodo, se declara
  con motivo técnico en el reporte — jamás una sustitución silenciosa.
- **Propose-only hacia otros nodos.** `soberano` es el único nodo que tocas directamente. Cualquier
  cambio que afecte a fragua/torre/vigía/musculo-hp-01-02 sale como artefacto propuesto (diff o
  script + motivo) en `p0x/propuestas/` — nunca se aplica por SSH desde aquí sin misión explícita
  para ese nodo.
- **Jamás firmas valor.** Ninguna clave privada de firma (NEAR, ed25519 de atestación/valor) entra
  a este nodo. Las claves SSH que sí viven aquí son auth-only, explícitamente marcadas como tal en
  su comentario (`no-value-signing`). Si ves material de firma de valor en otro nodo (p.ej.
  `id_hexelion`, servicios de atestación como "El Faro"), se documenta como hallazgo — no se toca,
  no se copia.
- **Español interno, UI en inglés.** Doctrina, reportes, commits: español. El dashboard/UI de
  herramientas que lo requieran: inglés.
- **Tags de modelo explícitos siempre.** Nunca un tag pelado en Ollama (`modelo:latest` sin más)
  — apuntan a variantes Thinking con razonamiento no desactivable. Usa siempre el tag completo
  (`qwen3-coder:30b`, no `qwen3-coder`).
- **`num_ctx` demostrado por dato.** Nunca se fija por defecto (262k cuelga runtimes en este HW) ni
  por intuición — se mide la RAM real disponible con el modelo cargado y se documenta el techo
  antes de subirlo.
- **Backend registrado al arranque de sesión.** Antes de cualquier bench, eval o telemetría que
  dependa de velocidad, `ollama ps` primero — anota CPU/GPU en el resultado. Vulkan puede
  activarse o caerse entre sesiones (depende del drop-in `OLLAMA_IGPU_ENABLE=1`); nunca asumas
  el backend de la sesión anterior (aprobado, Misión G1-R, 2026-07-19).
- **Commit por bloque, push soberano.** Cada bloque de misión termina en commit (git desde el
  minuto cero). Convención del repo: `p0x` empuja a `jetson` (la-torre), `hexelion` empuja a
  `torre` — mismo remoto, incluido en `~/.ssh/config` como host `la-torre`.
- **SUGERENCIAS al cierre.** Todo reporte de misión cierra con 3-6 sugerencias accionables
  (coste S/M/L), anexadas a `mente/feedback/PENDIENTES.md`.

## Mapa resumido de la Orquesta (rack P0X)

| Nodo | Rol | Notas de esta misión |
|---|---|---|
| **soberano** (aquí) | Cerebro central de cómputo/comunicación, futuro delegador de tareas a AI local | Beelink, Radeon 780M, tailnet `100.81.82.34` |
| **la-torre** (Jetson, user `jetson`) | Host git soberano (`jetson:p0x.git`, `jetson:hexelion.git`), Sínodo v2 con RAG | SSH auth-only vía `~/.ssh/id_ed25519_soberano_git`, host `la-torre` en `~/.ssh/config` |
| **la-fragua** (RK3588) | Batch/embeddings/Qdrant/Nexo, siempre encolado (`p0x-enqueue`), térmica vigilada | Corre también "El Faro" (servicio HEXELION de atestación AIS, firma ed25519 — fuera de alcance de `soberano`) |
| **el-vigía** (RPi + SDR) | AIS/ADS-B + M5 | — |
| **musculo-hp-01/02** (x86) | Toolchain de entrenamiento, puente de conversiones | — |
| **Claude Fable 5 / Opus** (fuera del rack) | Doctrina, arquitectura, veredictos con evidencia | Token caro — se reserva, jamás ejecuta en el rack |

## Footguns conocidos (con cicatriz)

- **Tags Ollama pelados** apuntan a variantes Thinking con razonamiento no desactivable — siempre
  tag explícito.
- **`num_ctx` default (262k)** cuelga runtimes en hardware de este tamaño — medir, no asumir.
- **PATH de systemd ≠ PATH interactivo** (lección de `OPERACIONES.md`, misión Ventana Viva): los
  servicios systemd no cargan `~/.bashrc`, así que no ven `~/.local/bin`. Todo binario invocado
  desde un servicio se resuelve con ruta absoluta o `shutil.which()` con fallback, nunca por PATH
  implícito.
- **Claves relayed a través de un intermediario (otra IA, retipeo) se corrompen.** Lección de esta
  misma misión: la pubkey SSH y su fingerprint llegaron corruptos dos veces al pasar por un canal
  intermedio antes de llegar a `torre`. Material criptográfico se copia-pega directo, nunca se
  transcribe ni se resume.
- **Sin sudo interactivo en `soberano`.** No hay contraseña cacheada; instalar vía binarios de
  usuario (releases prebuilt, `uv`, `nvm`) en vez de `apt` cuando sea posible.

## Estructura del repo (recordatorio)

`mente/` = Segundo Cerebro (doctrina, manual, alfabeto, telemetría, feedback/PENDIENTES.md).
`deploy/<nodo>/` = artefactos de despliegue por nodo (systemd units, scripts). `OPERACIONES.md` =
cuaderno de ingeniería append-only, fuera de `mente/` porque es método, no conocimiento del
Soberano. `bin/p0x-enqueue` = cola para trabajo pesado en la-fragua.
