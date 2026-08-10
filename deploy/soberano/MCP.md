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

---

## Fragilidad declarada · pin `mcp<2` — 2026-08-10

**Los tres servidores de PyPI mueren en silencio con el SDK `mcp` 2.x.** No dan
error de instalación ni aviso: arrancan, revientan al importar o al registrar
sus manejadores, y el arnés solo ve una conexión cerrada. En `claude mcp list`
aparecen como `✘ Failed to connect — Connection closed`, sin causa a la vista.

Trazas exactas medidas el 2026-08-10 con `mcp` 2.0.0:

```
mcp-server-git     AttributeError: 'Server' object has no attribute 'list_tools'
mcp-server-sqlite  AttributeError: 'Server' object has no attribute 'list_resources'
mcp-server-fetch   ImportError: cannot import name 'McpError' from 'mcp.shared.exceptions'
```

Causa: los tres declaran la dependencia `mcp` **sin techo de versión**, y `uv`
resuelve a la última. El SDK 2.0.0 renombró esa superficie.

**Regla operativa, no sugerencia:** toda instalación o reinstalación de estos
tres lleva el pin, siempre.

```bash
uv tool install --force --with "mcp<2" mcp-server-git
uv tool install --force --with "mcp<2" mcp-server-sqlite
uv tool install --force --with "mcp<2" mcp-server-fetch
```

Resuelto y verificado con `mcp 1.29.0` en los tres.

**Un `uv tool upgrade` sin el pin los rompe.** También los rompería `uv tool
install` de un solo paquete sin `--with`, porque el pin no queda grabado en el
entorno de la herramienta: vive en el comando, no en disco. Esa es exactamente
la clase de límite que la doctrina llama débil — el que hay que acordarse de
escribir cada vez.

Comprobación rápida de que el pin sigue en pie:

```bash
for t in mcp-server-git mcp-server-sqlite mcp-server-fetch; do
  printf "%-20s mcp=" "$t"
  "$HOME/.local/share/uv/tools/$t/bin/python" \
    -c "import importlib.metadata as m; print(m.version('mcp'))"
done
```

Cualquier salida que no empiece por `1.` significa que los tres servidores están
caídos aunque el registro diga que existen.
