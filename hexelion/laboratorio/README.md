# Laboratorio Hexelion

El banco donde una respuesta de un agente se juzga contra la doctrina **antes** de que
sus datos lleguen a un LoRA. No entrena: juzga y propone. Quien aprueba es el carbono.

## Por que vive en `hexelion/laboratorio/` y no en `hexelion/`

`~/p0x/hexelion/` ya tiene dueño --`CONTEXTO_FUTURO.md`, `HARDWARE_MAP.md`,
`ROADMAP_LORA.md`-- y el canon del nodo define Hexelion como **la capa fisica**: el rack,
los sensores, la impresora, el Nexo. Esto es el laboratorio DE Hexelion, no una
redefinicion de Hexelion.

## Lo que NO construye, porque ya vive

| pieza | donde |
|---|---|
| El RAG (recuperacion con presupuesto de tokens) | `preceptor/memory.py:1013 recuperar()` |
| Indice FTS5 autosincronizado | `memory.db` · `engrams_fts` + 3 disparadores |
| Canal local de conversaciones | `~/.preceptoros/conversaciones.db` |
| Filtro de fugas | `preceptor/guardrails.py` |
| Cadena de integridad | `preceptor/linea.py` |
| Bandeja de firmas (human in the loop) | `preceptor-internal/docs/bandeja_firmas.md` |
| Hooks de gate | `deploy/soberano/hooks/` |

Se conectan. No se reescriben. Es la Regla de Oro: *no reinventes lo que ya vive*.

## Las tres reglas duras

1. **Propose-only.** Sin `--ejecutar` no escribe ni marca nada.
2. **Anti-telefono-descompuesto.** Se escribe fichero y se devuelve la RUTA, nunca el
   contenido por el chat.
3. **Un veredicto sin las dos capas del juez es `NO_DATA`.** Determinista primero, MoE
   despues, y solo si la primera pasa.

## Uso

    ./init.sh                                    # el gate: verde o no hay entregable
    python3 reflexion.py --espacio <id> --seco   # ensena que haria y para

## La barrera de 16 KiB NO rige aqui

Firmado por el Soberano el 2026-09-12. Ese tope protege **la app open source y la
comunidad**, donde el peso es una promesa a quien descarga, y su unico dueno es
`preceptoros-web/test_web.py`. **Hexelion por dentro puede tener las herramientas que
necesite**: una regla pensada para cuidar una descarga no puede frenar el desarrollo
interno.

Lo que queda del ratchet es **visibilidad, no freno**: `init.sh` dice cuanto crecio
cada fichero desde la ultima linea base, y crecer no rompe nada. Crecer sin que nadie
lo vea, si.

## Donde esta el primer NO_DATA

El principio que ordena esta arquitectura: si se sabe **cual es el primer hueco de la
cadena**, la reparacion empieza por ahi y lo de aguas abajo se arregla solo. Por eso
cada `checkpoint.md` nombra el suyo y dice de quien lo hereda.

Hoy hay dos, y ninguno se arregla desde este laboratorio:

| cadena | primer NO_DATA | quien lo repara |
|---|---|---|
| identidad | `user_hash` vacio en las 4 conversaciones: la firma Ed25519 que `auth.js` genera no llega al canal | la web (Paso 2) |
| fisica | ningun sensor en `hexelion-nexo/sensores/`: telemetria y jardin nacen secos | el enchufe, no el modelo |
