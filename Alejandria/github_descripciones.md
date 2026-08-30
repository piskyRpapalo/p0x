# Descripciones y topics de GitHub · 2026-08-30

Posicionamiento firmado por el Soberano. Lo que sigue es esa firma con la forma
pulida y una decisión de idioma declarada.

## La decisión de idioma, y su motivo

**Repos públicos en inglés; privados en español.** Es el canon aplicado
—«español interno, UI en inglés»—: la descripción de un repo público es
escaparate para quien pasa por delante, y ese alguien no habla español por
defecto. `PreceptorOS` ya la tenía en inglés. Los privados son taller: español.

## Lo que había, y por qué estaba viejo

| Repo | Antes |
|---|---|
| **PreceptorOS** | *«Your syllabus, not a catalogue…»* — el posicionamiento de **temario y aprendizaje**, anterior al Privacy Gateway. Sus topics todavía decían `education`, `learning-compass`, `personal-knowledge`. |
| **preceptoros-web** | Una línea, sin topics. |
| **p0x** | Vacía, sin topics. |
| **preceptor-internal** | Vacía, sin topics. |

---

## PreceptorOS · público · inglés

> Your sovereign AI, on your machine, no cloud. The customs house between your
> data and external AIs: context sanitised by the Privacy Gateway, signed local
> memory, Ed25519 identity. Python stdlib only, offline-first, human-in-the-loop.

**Topics:** `python` `privacy` `local-first` `offline-first` `ed25519` `ollama`
`edge-ai` `human-in-the-loop` `eu-ai-act` `sqlite` `sovereign-ai` `llm` `pwa`
`on-device`

*Se retiran* `education`, `learning-compass` y `personal-knowledge`: describían
el producto anterior. *Se conservan* `pwa` y `on-device`, que siguen siendo
ciertos.

## preceptoros-web · público · inglés

> preceptoros.org · the Agora of PreceptorOS: in-browser privacy playground,
> signed community board and public benchmark. Zero external requests on load.

**Topics:** `privacy` `local-first` `offline-first` `ed25519` `webllm` `edge-ai`
`human-in-the-loop` `eu-ai-act` `zero-dependencies`

Sin `python`: esta web no lleva una línea de Python que se sirva.

## p0x · privado · español

> Monorepo del rack soberano: forja LoRA, bucles del enjambre
> (guardian/curador/afinador), sensores y operaciones. El cerebro detrás de
> PreceptorOS.

**Topics:** `python` `lora` `ollama` `edge-ai` `local-first` `homelab`
`self-hosted`

## preceptor-internal · privado · español

> El taller, no el producto: documentación interna, bucles del enjambre y
> auditorías del ecosistema PreceptorOS.

**Topics:** `python` `local-first` `human-in-the-loop`

---

## Fuera de alcance, propuesto y NO aplicado

El campo `homepage` está vacío en los cuatro. En los dos públicos debería
apuntar a `https://preceptoros.org` — es un enlace visible en la cabecera del
repo y hoy se está desperdiciando. No entraba en la firma, así que queda aquí:

```bash
gh api -X PATCH repos/piskyRpapalo/PreceptorOS -f homepage=https://preceptoros.org
gh api -X PATCH repos/piskyRpapalo/preceptoros-web -f homepage=https://preceptoros.org
```
