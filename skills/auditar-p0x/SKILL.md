---
name: auditar-p0x
description: Audita la higiene del sistema P0X (front-matter §2, grafo, telemetría §3, git soberano) con scripts deterministas y genera un plan de mejora PROPUESTO en PENDIENTES.md. Usar al inicio de sesiones de mantenimiento o tras cambios grandes en mente/. Audita FORMA, jamás decreta mecánica ni auto-ejecuta cambios.
---

# auditar-p0x — la deuda real, sin gastar razonamiento de frontera

**Invocación en una línea** (cualquier modelo: Haiku/Sonnet/Opus/Fable):

```bash
bash /mnt/nvme/p0x/skills/auditar-p0x/run_audit.sh
```

Eso corre los 4 auditores deterministas + el agregador, escribe
`mente/auditorias/AUDIT_<fecha>.md` y anexa las tareas crítico/importante a
`mente/feedback/PENDIENTES.md` con **estado=propuesta** (dedup por marcador
`[aud:slug]`, tope 8/corrida para no reventar el presupuesto de PENDIENTES).

## El único paso que pide modelo (acotado y reproducible)

Abre el `AUDIT_<fecha>.md` recién generado y ejecuta el
**PROMPT DE SÍNTESIS** embebido al final del informe (verificar anclaje de
evidencia + 6 líneas de síntesis ejecutiva). No requiere intuición: las
instrucciones están en el propio informe. Después, reporta al Soberano.

## Qué audita cada script (deterministas, cero LLM)

| script | contrato que verifica |
|---|---|
| `audit_frontmatter.py` | Protocolo §2: id/titulo/tipo; contrato evolutivo completo si hay `clase`; doctrina→editor carbono; `presupuesto_kb` (PODA §4.4); changelog append-only vs HEAD (§4.3); enlaces resuelven; ids duplicados; `.bak` en mente/ |
| `audit_grafo.py` | second_brain.json ↔ MDs: huérfanos, aristas rotas, tipos fuera de vocabulario, esferas sin `descripcion_niveles`, MD sin nodo / nodo sin MD, fuga de Necrópolis |
| `audit_telemetria.py` | §3: por voz (grounded, tokens, latencia) y por dominio·op (valida). `n < n_medicion` → "sin línea base" honesto; umbral cruzado solo si es parseable y hay n suficiente |
| `audit_git.py` | mente/ sin commit, runtime trackeado contra .gitignore, divergencia con los remotes soberanos (behind = crítico) |
| `audit_report.py` | agrega los JSON de `mente/auditorias/out/`, prioriza por TABLA fija (severidad+coste), ancla cada tarea a su infracción, escribe informe + anexo a PENDIENTES |

## LÍMITE DURO (el suelo de esta skill)

- **Audita FORMA, no decreta MECÁNICA**: puede decir "esta esfera no tiene
  niveles" — no puede decidir qué enseñar ni cómo medir comprensión (eso se
  deriva del corpus, aún vacío; hasta entonces la mecánica es STUB).
- **SIEMPRE propone**: el plan va a PENDIENTES.md con estado=propuesta.
  **JAMÁS auto-ejecuta cambios sobre MDs.** Loop = propose → carbono → ejecuta.
- Un commit de silicio sobre clase=doctrina es un evento de seguridad, no una
  optimización (§4.2) — esta skill lo detectaría, nunca lo cometería.

## Salidas

- `mente/auditorias/out/{frontmatter,grafo,telemetria,git}.json` — evidencia cruda
- `mente/auditorias/AUDIT_<fecha>.md` — informe legible + prompt de síntesis
- Anexo a `mente/feedback/PENDIENTES.md` — tareas propuestas para la firma del carbono

## Mantenimiento de la skill

Vive versionada en `p0x:skills/auditar-p0x/` (symlink en `~/.claude/skills/`).
Si el Protocolo cambia (§ nuevos), actualizar la TABLA de `audit_report.py` y
los checks — con commit que cite el § que lo motiva. python3 del sistema +
PyYAML; sin venv propio.
