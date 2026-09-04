# Encargo para `cc-local` · partir los dos ficheros al límite

**Estado:** ENCARGO PREPARADO. Firmado por el Soberano el 2026-09-04
(*«delegar a cc-local la partición de los ficheros al límite; es un refactor
mecánico verificable por gate y la doctrina §3 exige no gastar token de
frontera en esto»*).

    ~/p0x/bin/cc-local          # exporta P0X_BRAIN=local y lo anuncia en el banner

## El problema, medido el 2026-09-04

Techo: **10.240 B por fichero**, y `test_web.py` lo exige con `assertLess`, o sea
que el máximo real es **10.239**.

| fichero | pesa | libre |
|---|---|---|
| `public/assets/chat-router.js` | 10.226 B | **13 B** |
| `public/sw.js` | 10.223 B | **16 B** |

Trece y dieciséis bytes. El siguiente porqué que alguien escriba en cualquiera
de los dos tumba el gate. La doctrina dice **PARTIR, no recortar el comentario**
que explica el porqué: así salieron `fallback.js`, `localai.js`, `engine.js`,
`hub-cola.js` y `profile-obra.js` de sus padres. Hay precedente y hay patrón.

## Objetivo

Los dos ficheros por debajo de **9.000 B**, y los hijos también. No se busca
rozar el techo otra vez: se busca sitio para los próximos tres comentarios.

## Lo que NO se toca

- **Ni una línea de comentario se borra ni se resume.** Viajan con el código al
  que explican. Si un bloque se muda, su porqué se muda con él.
- **Ningún cambio de comportamiento.** Esto es mover código, no mejorarlo. Si
  ves algo que te parece mal, lo anotas en el reporte y **paras**: emitir
  veredictos de arquitectura no es de este cerebro.
- **`VERSION` de `sw.js` NO se toca** salvo que el punto 2 lo obligue (ver ahí).
- Nada fuera de `~/preceptoros-web/public/`.

## 1 · `chat-router.js` → sacar un hijo

Estructura actual: un IIFE con cabecera larga, la barra `.chat-quien`, el panel
`#herramientas`, el gancho de `visualViewport`, `vestir()`, `alternar()`,
`listo()` y el cableado de la cara.

**Corte propuesto:** el bloque que CONSTRUYE piezas del DOM —la barra
`.chat-quien` (avatar + nombre + aviso) y el panel `#herramientas`— sale a
`public/assets/chat-piezas.js`. Es construcción, no enrutado; el resto del
fichero decide *quién habla*, que es lo que su nombre promete.

- El hijo expone lo que haga falta en `window` (`window.ChatPiezas = {...}`) o
  devuelve los nodos; el estilo del repo es `var` y IIFE, **no** módulos ES.
- Añadir `<script src="/assets/chat-piezas.js"></script>` en las **tres**
  portadas (`es/`, `en/`, `fr/`), **antes** de `chat-router.js`.
- Vigila el peso de las portadas: `fr/index.html` es la más gorda. Si una se
  pasa de 10.239, **para y repórtalo** — no la recortes.

## 2 · `sw.js` → sacar la página de sin conexión

**LA TRAMPA, y es la que hunde este encargo si se ignora:** un service worker
**no se puede partir en dos ficheros que la página cargue por separado**. El
navegador registra UN script. La única forma válida es `importScripts()`, que es
síncrono y sólo existe dentro del worker.

Bloques medidos de `sw.js`:

| bloque | líneas | pesa |
|---|---|---|
| cabecera | 1–31 | 1.732 B |
| listas (VERSION, PAGINAS, CARAS, ESFERAS, HUB…) | 32–106 | 3.804 B |
| **página de sin conexión** (`SIN_RED`, `idiomaDe`, `paginaSinRed`) | **107–158** | **2.659 B** |
| estrategias (`refrescarDetras`, `navegacion`, `redPrimero`, `estatico`, `fetch`) | 159–fin | 2.025 B |

**Corte propuesto:** el bloque de sin conexión (2.659 B) sale a
`public/sw-sinred.js`, y `sw.js` lo trae con:

    importScripts('/sw-sinred.js');   // primera linea ejecutable, antes de usarlo

Deja `sw.js` en ~7.6 KB y el hijo en ~2.7 KB. Los dos con holgura.

Tres cosas que comprobar y que son el 90 % del riesgo:

1. **`importScripts` va en el ámbito global del worker**, no dentro de un
   `addEventListener`. Las funciones del hijo quedan visibles sin `export`.
2. **El hijo NO se mete en la lista de precache.** `importScripts` lo pide el
   propio worker al instalarse; añadirlo a `HUB`/`rutasDelShell()` es
   redundante y, si algún día devuelve 404, tumbaría el `addAll` entero.
3. **Ponerlo en la raíz de `public/`, no en `assets/`.** El fichero de un worker
   se sirve desde donde el worker vive; en la raíz no hay duda de ámbito.

Si al partirlo cambia el contenido efectivo del worker, **sube `VERSION`** una
letra (`preceptoros-2026-09-i` → `-j`): sin eso, los navegadores que ya tengan
el worker instalado seguirán con el viejo y la partición no llegará a nadie. Es
el footgun que el glosario llama *«el service worker te enseña código viejo»*.

## El gate manda, y corre solo

    cd ~/preceptoros-web && python3 -m pytest test_web.py -q
    # exigido: 74 passed, 964 subtests passed

Hay un hook `PostToolUse` que lo corre después de cada escritura y **sale con
código 2 si cae**. No hace falta acordarse: si rompes algo, te enteras en el
mismo turno. Un diff que no pasa el gate **no es un entregable, es ruido**.

Comprobación de pesos, que es el objetivo de todo esto:

    cd ~/preceptoros-web && python3 -c "import pathlib;[print(p.stat().st_size,p) for p in pathlib.Path('public').rglob('*') if p.is_file() and p.suffix in ('.html','.css','.js','.json','.webmanifest') and p.stat().st_size>9000]"
    # exigido: chat-router.js y sw.js YA NO salen en esta lista

## Y algo que el gate no puede ver

El gate no registra un service worker. Que `test_web.py` esté en verde **no
prueba que el PWA siga instalando**. Se comprueba en el Doogee por ADB, y así se
midió el 2026-09-04: primera visita **76 peticiones**, segunda **3**. Si tras la
partición la segunda visita no baja a un puñado, el worker no está instalando.

    adb reverse tcp:8124 tcp:8124
    cd ~/preceptoros-web/public && python3 -m http.server 8124 --bind 127.0.0.1 > /tmp/8124.log 2>&1 &
    adb shell am start -a android.intent.action.VIEW -d 'http://127.0.0.1:8124/es/'
    # contar lineas de /tmp/8124.log antes y despues de recargar

**El navegador del arnés NO sirve para esto:** no registra service workers, ni
siquiera uno de una línea. Está anotado en `recursos.json`.

## Al cerrar

Una línea en `mente/telemetria/cerebro_local.jsonl`:
`{fecha, tarea, cerebro, pasadas, minutos, gate_ok, ctx_pico, nota}`. Sin ese
fichero no hay forma legítima de re-editar el reparto de cerebros más adelante.

---

## CÓMO SE ARRANCA, y por qué no basta con `cc-local` a secas

Medido el 2026-09-04. `cc-local` tal cual **aborta antes del primer turno**:

    API Error: 400 request (26327 tokens) exceeds the available context size (16384 tokens)

Y subir la ventana no lo arregla solo, porque la carga **crece con ella**:

| `num_ctx` | lo que pide el arnés | resultado |
|---|---|---|
| 16.384 (el autorizado) | 26.327 | 400 |
| 32.768 | 43.349 | 400 |
| 65.536 | 68.619 | 400 |

Dos causas, y las dos hay que quitar:

1. **El modelo es «unrecognized»**, así que Claude Code supone una ventana de
   200k y empaqueta contra ella. Se corrige diciéndole la de verdad:
   `CLAUDE_CODE_MAX_CONTEXT_TOKENS=65536`.
2. **La sesión carga los ~20 servidores MCP y las skills del perfil global**, y
   sus esquemas son la mayor parte de esos 68 kB de tokens. Con
   `--strict-mcp-config` y una config vacía, la carga baja del techo y el turno
   arranca.

Receta medida que sí levanta la sesión:

    echo '{"mcpServers":{}}' > /tmp/mcp-vacio.json
    P0X_NUM_CTX=65536 deploy/soberano/cerebro-local-arranca.sh
    CLAUDE_CODE_MAX_CONTEXT_TOKENS=65536 ~/p0x/bin/cc-local \
      --strict-mcp-config --mcp-config /tmp/mcp-vacio.json

`num_ctx=65536` está **medido en este metal** y cabe: con el modelo cargado
quedan ~20 GB de RAM libres. Pero **no está autorizado**: el Bloque SOBERANO-1
fija 16.384. Subirlo de forma permanente exige firma; aquí va como parámetro de
una corrida, con su medida al lado, que es lo que el canon pide antes de tocar
un techo.

El backend sigue siendo Vulkan: comprobado por `/dev/dri` en el proceso (2
descriptores) y por el banner del propio envoltorio, no por el log —que a esta
verbosidad no dice ni una palabra de Vulkan.

Y una tranquilidad: **el cerebro local sabe usar herramientas**. Comprobado
contra `/v1/messages` con un `tools:[...]` a mano: devolvió un bloque `tool_use`
correcto con `stop_reason: "tool_use"`. Lo que fallaba era el tamaño del
paquete, no la capacidad del modelo.
