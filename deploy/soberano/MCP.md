# Servidores MCP del nodo Soberano — 2026-08-10

Ronda MCP-1. Registro de lo instalado, con qué propósito y qué restricción.
Lo que no se pudo instalar va abajo con el motivo, no omitido.

Ámbito de registro: `claude mcp add --scope user`, que escribe en el fichero de
estado del usuario. **No** se usó `claude_desktop_config.json` (es de Claude
Desktop, no de Claude Code) ni un `.mcp.json` de proyecto: ese fichero exige
rutas absolutas y habría metido la ruta del usuario en un repositorio que hoy
está publicado.

## Instalados y verificados

| MCP | Origen real | Verificación ejecutada | Restricción |
|---|---|---|---|
| `filesystem` | npm `@modelcontextprotocol/server-filesystem` 2026.7.10 | `list_directory` sobre `mente/` → 6+ entradas | Acotado a los cinco árboles del rack. Nunca `/` |
| `git` | PyPI `mcp-server-git` 2026.7.10 (`uv tool`) | `git_status` del repo del dashboard → rama y estado | Sin `--repository` fijo: el repo se pasa por llamada |
| `sqlite` | PyPI `mcp-server-sqlite` (`uv tool`) | `list_tables` → 8 tablas · `SELECT COUNT(*) FROM bronze_solar` → 2 | Apuntado a la base de telemetría, no a Gold |
| `fetch` | PyPI `mcp-server-fetch` 2026.7.10 (`uv tool`) | `fetch` contra el servicio local del puerto 8080 → contenido devuelto | Solo localhost y red privada |
| `memory` | npm `@modelcontextprotocol/server-memory` 2026.7.4 | alta y recuperación de una entidad de prueba, ida y vuelta | Grafo fuera de todo repositorio. El disco sigue siendo la fuente de verdad |

Salud tras el registro: los cinco en `✔ Connected` (`claude mcp list`).

## Los nombres del prompt no eran los nombres reales

Tres de los siete paquetes pedidos **no existen en npm**. Se comprobó uno a uno
con `npm view <pkg> version`:

| Pedido | Realidad |
|---|---|
| `@modelcontextprotocol/server-git` | no existe en npm · vive en PyPI como `mcp-server-git` |
| `@modelcontextprotocol/server-sqlite` | no existe en npm · PyPI `mcp-server-sqlite` |
| `@modelcontextprotocol/server-fetch` | no existe en npm · PyPI `mcp-server-fetch` |
| `@modelcontextprotocol/server-github` | existe pero **marcado como no soportado** por su autor |
| `@modelcontextprotocol/server-brave-search` | existe pero **marcado como no soportado** |

Había además una entrada previa de `git` en la configuración apuntando al
paquete npm inexistente: fallaba al conectar. Se sustituyó por el de PyPI.

## La incompatibilidad que costó la mitad de la ronda

Los tres servidores de PyPI arrancaban y morían sin responder al `initialize`:

```
AttributeError: 'Server' object has no attribute 'list_tools'      (git)
AttributeError: 'Server' object has no attribute 'list_resources'  (sqlite)
ImportError: cannot import name 'McpError'                         (fetch)
```

Causa: los tres declaran `mcp` sin techo de versión y resolvían al SDK **2.0.0**,
que renombró esa superficie. Se fijó el SDK a la rama 1.x:

```
uv tool install --force --with "mcp<2" mcp-server-git
uv tool install --force --with "mcp<2" mcp-server-sqlite
uv tool install --force --with "mcp<2" mcp-server-fetch
```

Resuelto a `mcp 1.29.0` en los tres, y los tres responden. **Este pin es frágil:**
cualquier reinstalación sin `--with "mcp<2"` los vuelve a romper.

## No instalados, y por qué

- **`github`** — BLOQUEADO, y no solo por falta de credencial. El paquete pedido
  está descontinuado, y su sustituto exigiría escribir un token en `~/.bashrc`.
  Un token en un fichero de arranque de shell es material de credencial en claro:
  no se escribe desde aquí. Y hay un motivo doctrinal más fuerte, abajo.
- **`brave-search`** — BLOQUEADO. Paquete descontinuado y sin `BRAVE_API_KEY` en
  el entorno. Es además el único de la lista que habla con internet: por la
  restricción de Nivel 3 no debería quedar siempre montado, sino levantarse para
  la tarea concreta y retirarse.

## El conflicto que este montaje destapa

§1 de `mente/EQUIPO_AI_LOOP.md` dice que el Ejecutor no puede empujar, y añade
que el límite es mecánico: «no puede empujar porque el sistema no le deja, no
porque se lo pidieran amablemente». Un MCP de GitHub con token de escritura
**le daría exactamente esa capacidad por otra puerta**, saltándose los ganchos
de git, que solo frenan lo que pasa por `git push`.

Lo mismo, en menor grado, con los que ya están montados: la restricción «solo
lectura» de `filesystem` y de `sqlite` **no es mecánica**. Se comprobó en el
código: `readOnly` en el servidor de ficheros es solo una anotación por
herramienta, no un modo; y el de sqlite expone `write_query` y `create_table`.
Hoy esa restricción vive únicamente en este documento. Lo único mecánico es el
acotado de rutas de `filesystem`, que sí se aplica.
