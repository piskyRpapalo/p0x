# Propuesta · `agora_api` (la-fragua): la ruta de turno que la web ya llama

**Nodo destino:** `la-fragua` · **Origen:** `soberano` · **Fecha:** 2026-09-01
**Estado:** PROPUESTA — no aplicada. `la-fragua` es propose-only desde `soberano`.

## Por que existe esto

La portada de `preceptoros.org` ya no ofrece descargar un modelo ni buscar una
Ollama local: **habla con el modelo del rack**. El cliente esta escrito y
desplegado (`public/assets/rack.js`), y hoy termina en `NO_DATA` con su causa
declarada, que es lo correcto mientras el otro extremo no exista.

Lo que falta esta **entero en `la-fragua`**, no en la web.

## Lo medido el 2026-09-01 (desde `soberano`)

| Hecho | Valor |
|---|---|
| DNS `api.preceptoros.org` | resuelve a Cloudflare (`104.21.93.98`, `172.67.208.165`) |
| Tunel | ARRIBA. Enruta a `127.0.0.1:9002` de `la-fragua` |
| Backend | `uvicorn agora_api:app` (FastAPI) |
| `GET /` | `404 {"detail":"Not Found"}` |
| `GET /api/tags` | `404` |
| `GET /openapi.json` | `404` |
| `GET /docs` | `404` |
| CORS | ninguna cabecera `Access-Control-Allow-Origin` |
| Ollama en `soberano` | VIVA, `*:11434`, sirve `preceptor-v7:latest` |

El 404 **no es de red ni de DNS**: es que `agora_api` no publica esas rutas.

## Lo que la web necesita

`rack.js` habla el **contrato de Ollama**, que es el que ya hablan `localai.js`
y el propio rack. No se eligio por gusto: es el unico que hoy tienen los dos
extremos, y anadir un tercer dialecto seria inventar trabajo.

### Ruta

    POST /api/generate

**Peticion** (`application/json`):

    {"model": "preceptor-v7:latest", "prompt": "<papel + turno>", "stream": true}

`model` sale del catalogo publico `hub.json`, campo `agentes[].real.adaptador`.
Hoy solo `instalador` declara uno: `preceptor-v7:latest`. Los demas van con
`disponible:false` y la web ni siquiera llama — lo dice y para.

**Respuesta**: NDJSON en streaming, **una linea por trozo**:

    {"response":"Hola","done":false}
    {"response":" que","done":false}
    {"eval_count":128,"done":true}

- `response` es el trozo de texto. La web lo acumula.
- `eval_count` son los **tokens reales del motor**. Si no viene, la web declara
  `tok/s NO_DATA` en vez de estimarlo: contar trozos y llamarlos tokens seria
  decorar una cifra, y es justo lo que este proyecto no hace.

Un proxy fino de `agora_api` hacia la Ollama que corresponda cumple esto sin
reescribir nada: el formato ya es el suyo.

### CORS — sin esto, el tunel solo no basta

Medido en el navegador:

    Access to fetch at 'https://api.preceptoros.org/api/generate'
    from origin 'http://...' has been blocked by CORS policy:
    No 'Access-Control-Allow-Origin' header is present

Como quien contesta es **FastAPI y no Ollama**, la cabecera la pone la app.
`OLLAMA_ORIGINS` aqui no pinta nada:

    from fastapi.middleware.cors import CORSMiddleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["https://preceptoros.org"],
        allow_methods=["POST"],
        allow_headers=["Content-Type"],
    )

## Como se comprueba que quedo bien

    curl -N -X POST https://api.preceptoros.org/api/generate \
      -H 'Content-Type: application/json' \
      -d '{"model":"preceptor-v7:latest","prompt":"di listo","stream":true}'

Debe emitir lineas NDJSON y cerrar con una que lleve `eval_count`. Y desde la
web, un turno en `preceptoros.org` tiene que dejar el badge del cerebro en
**verde** (`live`), que hoy se queda apagado a proposito hasta que un turno
vuelve de verdad.

## Lo que NO se pide aqui

- **Nada de exponer la Ollama del Soberano a internet.** El tunel sale de
  `la-fragua` y ahi se queda esa decision.
- **Ninguna clave de firma de valor** cruza a este camino. Es un turno de
  texto, no una atestacion.
- **`api-guia` (puerto 9001) es otro asunto.** No tiene unidad systemd creada
  (`Unit api-guia.service could not be found`), y por eso el Ojo lo declara
  `OK` sin que escuche nadie. Es un falso verde del Ojo y va aparte.
