# Auditoría de lo ya publicado — 2026-08-09

Ronda CARAS-PUBLICAS-1 · Bloque 3. **No se reescribe historial.** Lo publicado,
publicado está: reescribir no recupera nada y rompe las referencias. La
corrección, si el Soberano la ordena, es hacia adelante.

Este informe da `fichero` y `línea` y la regla que saltó, **sin transcribir el
valor**: un informe de fugas que copia las fugas es otra fuga. El valor se lee
en el fichero. Verificado — el guardia sobre este mismo informe da 0 hallazgos.

## Alcance real

La ronda pedía auditar «la carpeta de doctrina publicada». Al medir, el alcance
resultó mayor: el repositorio público `piskyRpapalo/-hexelion-public` no sirve
una exportación sanitizada sino **el repo privado `p0x` entero**, `mente/`
incluida (ver `RECONCILIACION_HEXELION_2026-08-09.md`). Se audita por tanto la
carpeta pedida **y** el resto del árbol publicado, en apartados separados.

Estado auditado: `origin/master` = `f4a7ad7`, extraído con `git archive` y
escaneado con el guardia reparado en esta misma ronda.

```
$ git archive origin/master | tar -x -C <tmp>
$ find mente -type f | wc -l
102
$ find mente -type f -print0 | sort -z | xargs -0 \
    python3 deploy/comun/hooks/guardia_higiene.py --files
```

## Resultado

**Hay hallazgos.** No es «ninguno».

| Ámbito | Hallazgos | Ficheros |
|---|---|---|
| `mente/` (la carpeta de doctrina pedida) | 30 | 12 de 102 |
| resto del árbol publicado | 34 | 17 |
| **total** | **64** | **29** |

Por tipo:

| Regla | mente/ | resto |
|---|---|---|
| IP-TAILNET (IP de la red superpuesta) | 11 | 14 |
| RUTA-HOME (ruta absoluta al directorio del usuario) | 10 | 14 |
| NODO-COMANDO (nodo como argumento de conexión remota) | 4 | 0 |
| NODO-USER-AT (usuario@host) | 3 | 2 |
| DOMINIO-PRIVADO (dominio de red privada) | 1 | 3 |
| NODO-HOST-PATH (host:/ruta) | 1 | 0 |
| IP-RFC1918 (IP de LAN) | 0 | 1 |

Ninguna clave privada ni token de proveedor. La única coincidencia de
`SECRETO-ASIGNADO` en la primera pasada (`mente/pipeline/to_qdrant.py:43`) era
un falso positivo — una llamada a función, no un literal — y la regla se afinó
en esta misma ronda para descartar llamadas y lecturas de entorno.

## Hallazgos en `mente/` — la carpeta de doctrina

| Fichero | Línea | Regla |
|---|---|---|
| `mente/auditorias/reflejos.md` | 29 | NODO-COMANDO |
| `mente/auditorias/reflejos.md` | 30 | NODO-COMANDO |
| `mente/auditorias/reflejos.md` | 141 | NODO-COMANDO |
| `mente/auditorias/reflejos.md` | 142 | NODO-COMANDO |
| `mente/backlog/BACKLOG_UI.md` | 375 | IP-TAILNET |
| `mente/deliberacion/delta_bambu_a1mini.md` | 73 | IP-TAILNET |
| `mente/deliberacion/INDICE_ARCHIVO_HISTORICO.md` | 8 | RUTA-HOME |
| `mente/deliberacion/INDICE_ARCHIVO_HISTORICO.md` | 22 | RUTA-HOME |
| `mente/feedback/PENDIENTES.md` | 116 | NODO-USER-AT |
| `mente/feedback/PENDIENTES.md` | 312 | DOMINIO-PRIVADO |
| `mente/feedback/PENDIENTES.md` | 314 | IP-TAILNET |
| `mente/feedback/PENDIENTES.md` | 380 | IP-TAILNET |
| `mente/feedback/PENDIENTES.md` | 421 | IP-TAILNET |
| `mente/feedback/PENDIENTES.md` | 457 | IP-TAILNET |
| `mente/feedback/PENDIENTES.md` | 458 | RUTA-HOME |
| `mente/pipeline/build_graph.py` | 21 | RUTA-HOME |
| `mente/pipeline/hw.yaml` | 3 | RUTA-HOME |
| `mente/pipeline/hw.yaml` | 6 | IP-TAILNET |
| `mente/pipeline/hw.yaml` | 10 | IP-TAILNET |
| `mente/pipeline/hw.yaml` | 15 | IP-TAILNET |
| `mente/pipeline/render_voces.py` | 3 | RUTA-HOME |
| `mente/pipeline/render_voces.py` | 21 | RUTA-HOME |
| `mente/pipeline/to_qdrant.py` | 7 | RUTA-HOME |
| `mente/pipeline/to_qdrant.py` | 30 | RUTA-HOME |
| `mente/reportes/DOS_PIELES_soberano_2026-07-19.md` | 12 | NODO-HOST-PATH |
| `mente/reportes/G0_soberano_2026-07-18.md` | 13 | NODO-USER-AT |
| `mente/reportes/G0_soberano_2026-07-18.md` | 26 | IP-TAILNET |
| `mente/reportes/G0_soberano_2026-07-18.md` | 84 | NODO-USER-AT |
| `mente/reportes/G0_soberano_2026-07-18.md` | 98 | IP-TAILNET |
| `mente/reportes/YACIMIENTO_2026-07-19.md` | 8 | RUTA-HOME |

## Hallazgos en el resto del árbol publicado

| Fichero | Línea | Regla |
|---|---|---|
| `BLUEPRINT_DISENO_SOBERANO.md` | 60 | DOMINIO-PRIVADO |
| `deploy/fragua/paquete-dos-pieles/01-serve-from-git.patch` | 8 | RUTA-HOME |
| `deploy/fragua/paquete-dos-pieles/01-serve-from-git.patch` | 14 | RUTA-HOME |
| `deploy/fragua/paquete-dos-pieles/01-serve-from-git.patch` | 35 | RUTA-HOME |
| `deploy/fragua/paquete-dos-pieles/01-serve-from-git.patch` | 71 | RUTA-HOME |
| `deploy/fragua/paquete-dos-pieles/05-swap.md` | 15 | RUTA-HOME |
| `deploy/fragua/paquete-dos-pieles/05-swap.md` | 22 | RUTA-HOME |
| `deploy/fragua/paquete-dos-pieles/05-swap.md` | 34 | RUTA-HOME |
| `deploy/fragua/reflejo-bateria.service` | 19 | RUTA-HOME |
| `deploy/fragua/reflejo-m5.service` | 16 | RUTA-HOME |
| `deploy/soberano/AUDITORIA_G1.md` | 61 | NODO-USER-AT |
| `deploy/soberano/aurelius-interfaz.service` | 3 | RUTA-HOME |
| `deploy/soberano/aurelius-interfaz.service` | 9 | RUTA-HOME |
| `deploy/soberano/aurelius-interfaz.service` | 12 | RUTA-HOME |
| `deploy/soberano/CLAUDE.md` | 110 | IP-TAILNET |
| `deploy/soberano/opencode_AGENTS.md` | 24 | IP-TAILNET |
| `deploy/soberano/OPENWEBUI.md` | 17 | IP-TAILNET |
| `deploy/soberano/OPENWEBUI.md` | 23 | IP-TAILNET |
| `deploy/soberano/OPENWEBUI.md` | 25 | IP-RFC1918 |
| `deploy/soberano/OPENWEBUI.md` | 26 | IP-TAILNET |
| `deploy/soberano/OPENWEBUI.md` | 30 | IP-TAILNET |
| `deploy/soberano/OPENWEBUI.md` | 56 | IP-TAILNET |
| `deploy/soberano/OPENWEBUI.md` | 86 | DOMINIO-PRIVADO |
| `deploy/soberano/openwebui/README.md` | 41 | DOMINIO-PRIVADO |
| `deploy/soberano/open-webui.service` | 6 | RUTA-HOME |
| `deploy/soberano/open-webui.service` | 11 | IP-TAILNET |
| `deploy/soberano/SCRAPER_G1.md` | 6 | IP-TAILNET |
| `deploy/torre/modelo_residente.sh` | 12 | NODO-USER-AT |
| `deploy/vigia/ingest_m5.py` | 22 | IP-TAILNET |
| `deploy/vigia/p0x-m5-ingest.service` | 11 | RUTA-HOME |
| `proxy/litellm_config.yaml` | 4 | IP-TAILNET |
| `proxy/litellm_config.yaml` | 10 | IP-TAILNET |
| `proxy/litellm_config.yaml` | 15 | IP-TAILNET |
| `proxy/litellm_config.yaml` | 20 | IP-TAILNET |

## Un caso aparte

`mente/codice/CODICE_david.md` es un enlace simbólico a una ruta absoluta de un
nodo anterior (`/mnt/...`), roto en este nodo y publicado tal cual. No lo
detecta ninguna regla actual — el guardia lee contenido, no destinos de enlace.
Anotado como carencia del propio guardia.

## Qué NO se hizo, y por qué

- **No se reescribió historial.** Invariante de la ronda, y además inútil: el
  contenido lleva publicado desde antes de que existiera ningún freno, y GitHub
  conserva objetos alcanzables por SHA aunque se reescriban las ramas.
- **No se corrigió hacia adelante.** Sustituir los 64 valores por marcadores
  genéricos es un commit que toca 29 ficheros de doctrina viva; excede «esta
  ronda no construye». Va como sugerencia.
- **No se tocó la visibilidad del repositorio.** Es acción del Soberano.
