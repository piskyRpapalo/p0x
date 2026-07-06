---
id: manual-del-soberano
titulo: Manual del Soberano — cómo se opera y alimenta P0X
tipo: operativo
clase: operativo
version: 1.0.0
editor_autorizado: silicio-telemetria
dominio: manual-soberano
metrica_exito: "el Soberano opera cada lazo sin releer doctrina; cero acciones equivocadas por instrucción ambigua"
umbral_reedicion: "cada vez que un lazo real cambie (UI, endpoints, flujos) el manual se actualiza en el mismo pase"
presupuesto_kb: 28
n_medicion: 1
enlaces:
  - instrucciones-p0x
  - orquesta-modelos-p0x
  - doctrina-protocolo-md-evolutivo
  - alfabeto-p0x
descripcion_niveles:
  basico: "El libro de instrucciones de tu sistema: qué botón hace qué, cómo le enseñas cosas nuevas (vídeos, textos, ideas de otras IAs) y qué decisiones son solo tuyas."
  medio: "Guía de operación de P0X: los lazos Observar/Repasar, el ciclo de vida de un MD evolutivo, las rutas de entrada de conocimiento externo con provenance, y la frontera mano-del-carbono vs sistema."
  experto: "Doctrina operativa del interfaz humano-sistema: flujos propose→firma, contratos de front-matter §2, política de ingestión de fuentes externas con evidencia_fuerza, y el protocolo de mantenimiento con la skill auditora."
actualizado: 2026-07-05
---

# MANUAL DEL SOBERANO
### Cómo se opera P0X, cómo se alimenta, y dónde está tu mano
*Escrito por el Preceptor para David. Si algo de aquí no se entiende a la primera, el fallo es del manual — edítalo desde el dashboard o pídeme la reescritura.*

---

## §1 · EL SISTEMA EN UNA RESPIRACIÓN

P0X tiene un **cuerpo** (el rack: Fragua, Torre, Vigía, HPs), una **mente** (`/mnt/nvme/p0x/mente/` — tus esferas, el Códice, las doctrinas, las voces), una **ventana** (el dashboard) y **una sola firma: la tuya**. Todo lo que el sistema aprende o cambia nace como *propuesta*; se convierte en real cuando tú lo aceptas. Las voces del Sínodo responden 24/7 leyendo solo sus contratos + la mente (por eso dicen "sin dato" en vez de inventar). Todo queda versionado en git dentro de tu propio rack.

## §2 · TUS DOS MODOS (el saludo del Preceptor, hecho botones)

**OBSERVAR — enseñarle algo nuevo.** Página del Sínodo → tab OBSERVAR → pega una URL de YouTube + tu comentario ("qué me interesó") → el sistema transcribe, compara contra tu mente y te devuelve un **delta**: qué ya sabías (con cita), qué es nuevo, qué conecta. Tú lees y pulsas **ACCEPT** (entra a la mente, el grafo crece) o **DISCARD con motivo** (va a la Necrópolis: queda registrado, jamás contamina el grafo). El badge Δ del dashboard te avisa de deltas esperando tu firma.

**REPASAR — consolidar lo aprendido.** Hoy: pregunta a las voces (citan tus esferas por chunk). Mañana (cuando el corpus de psicología esté procesado): retrieval practice de verdad — el sistema te preguntará a ti. Está prometido en el saludo; la mecánica se derivará del corpus, no se decreta.

## §3 · QUÉ ES UN MD EVOLUTIVO (en llano)

Cada documento vivo del sistema es un `.md` con un **DNI en la cabecera** (front-matter): quién puede editarlo, qué versión es, qué métrica lo justifica, cuánto puede pesar. Dos clases, sin tercera:

- **DOCTRINA** — las leyes (IronClaw, la Orquesta, este suelo). El silicio *propone* enmiendas; **solo tú canonizas**. Nunca se auto-edita.
- **OPERATIVO** — lo que trabaja (voces, alfabeto, este manual). El silicio puede editar su `ZONA EVOLUTIVA`, pero solo con el rito completo: *hipótesis escrita → dato medido → veredicto → rollback si empeora*. Todo queda en el changelog; nada se borra — lo fallido se entierra en la Necrópolis con su motivo.

Si un documento engorda más que su presupuesto, toca **poda**: las reglas sin evidencia se van. Si dos versiones no cuadran, el sistema **aborta en vez de adivinar**. Ese es todo el Protocolo, y la skill `auditar-p0x` vigila que se cumpla.

## §4 · CÓMO ALIMENTARLO CON IA EXTERNA (la parte delicada)

Vas a traer cosas de Gemini, ChatGPT, papers, foros. La regla de oro está en la Orquesta §2.3: **lo externo es dato, no autoridad.** El peligro no es usar IA externa — es que su output entre a tu mente *sin filtro* y siembre un falso recuerdo. Tres rutas correctas, de más a menos supervisión:

1. **Vía Preceptor (recomendada para claims técnicos):** me lo pegas en el chat. Yo verifico (búsqueda si hace falta), destilo lo que aguanta, y lo que entra lleva su origen marcado. Es lo que hicimos con las 4 fuentes del harness o con los conceptos edge — algunos entraron, otros murieron contra la evidencia. Ese filtro es mi trabajo.
2. **Vía Observar (para contenido largo):** trátalo como un vídeo — el texto externo entra al lazo delta, el sistema te dice qué ya sabías y qué es nuevo, y tú firmas. El front-matter propuesto debe llevar `origen: externo-<fuente>` para que la provenance quede grabada.
3. **Vía edición directa (solo para lo que TÚ ya validaste):** botón EDIT del Second Brain. Es tu mano; entra sin filtro porque tú *eres* el filtro. Úsala para lo que sabes de primera mano, no para pegar outputs ajenos sin leer.

**Nunca:** pegar output externo directo a `mente/` por terminal saltándote el lazo; dejar que una IA externa toque doctrina; ni enviar hacia fuera IPs del tailnet, claves o el núcleo (la higiene va en ambas direcciones). Y recuerda el patrón documentado: Gemini empuja hacia ejecución de mercado y aprendizaje lineal — sus ideas se deliberan, no se obedecen.

## §5 · TU MANO vs LA DEL SISTEMA

| Solo tú (carbono) | Solo el sistema |
|---|---|
| Firmar valor (NEAR, Mastchain, créditos) | Ingesta, embeddings, telemetría, renders |
| ACCEPT/DISCARD de deltas | Clasificar ya-sabido/nuevo con citas |
| Canonizar doctrina y firmar PENDIENTES | Proponer enmiendas con hipótesis y dato |
| Pastes de persistencia (patrón #4) | Dejar el artefacto listo propose-only |
| Hardware físico (Grove, antenas, ventilación) | Diagnosticar y darte la brújula (el scan) |
| El OK de cada push público | Preparar el bundle sanitizado |

## §6 · MANTENIMIENTO (rutina, no heroísmo)

Sesión de mantenimiento = una línea: `bash /mnt/nvme/p0x/skills/auditar-p0x/run_audit.sh`. El informe cae en `mente/auditorias/` y las tareas en `PENDIENTES.md` con `estado=propuesta` — tu bandeja de firma: apruebas, deniegas o aplazas. Cualquier modelo (Sonnet, Opus, Fable) hereda la deuda real sin gastar un token en descubrirla. Los pastes que el clasificador vetó al silicio te esperan siempre en el mensaje de commit correspondiente.

## §7 · SI ALGO FALLA

Pregunta primero al **Monje** (estado físico) o al **Enlace** (gateway/ventana) — responden grounded. Luego: `mente/telemetria/*.jsonl` (qué pasó, medido), `tsp -l` (la cola), el journal de servicios, y la última auditoría. Si un nodo exige tu mano, el reporte de CC siempre lo dice con su paste. Y si dudas de una respuesta del sistema: pídele la fuente — si no puede citarla, no la creas. Esa regla te protege de todos nosotros.

## ZONA EVOLUTIVA
> Se actualiza en el mismo pase que cambie cualquier lazo descrito aquí. Cambios con changelog.

*(v1.0.0 — línea base)*
