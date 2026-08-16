# p0x · canon privado del Soberano

Repositorio privado del rack P0X. `mente/` es el Segundo Cerebro (doctrina, manual,
telemetría, feedback), `deploy/<nodo>/` los artefactos de despliegue por nodo, y
`OPERACIONES.md` el cuaderno de ingeniería append-only.

**Este repo es privado y no se publica.** El producto público vive en
`aurelius-mvp/` (repo propio, rama `main`) y la app de aprendizaje en `~/aurelius`.
La frontera no se cruza: lo que se escribe aquí no viaja al producto.

## Dashboard local

Ventana de escritorio para hablar con Aurelius en este nodo, sin navegador y sin red.

**Solo local. Sin red. Sin sockets. Sin nube.**

**Frontera: este dashboard es privado. No va al producto público.**

### Qué es

`dashboard.py` abre una ventana PyWebView (GTK3/WebKit2) que carga *la cara ya
existente* — `~/aurelius/interface/aurelius_face.html` — por `file://`, de modo que
sus diez assets relativos (4 CSS + 6 JS) resuelven solos. La cara **no se edita**:
vive en otro repo, es pública, y una segunda copia se quedaría vieja el día que se
corrija la primera.

La cara fue escrita contra el servidor estático `:8050` y contra un endpoint ollama:
llama por `fetch()` a `/api/estado`, `/api/inventario`, `/api/preferencia` y
`<EP>/api/chat`. Como aquí no hay ni servidor ni ollama, `dashboard.py` inyecta un
*user script* de WebKit en `document-start` —antes de que corra un solo script de la
página— que redirige esas rutas al puente `pywebview.api`:

| ruta que llama la cara | va a |
|---|---|
| `/api/chat` (POST) | `enviar_pregunta()` → el gerente como proceso hijo |
| `/api/estado` (GET) | `obtener_estado()` |
| `/api/inventario` (GET) | `leer_memoria()` |
| `/api/preferencia` (GET) | `obtener_preferencia()` |
| `/api/preferencia` (POST) | `guardar_preferencia()` |
| `models.json`, `config.json`, `config.example.json` | `leer_json()` (lista blanca) |

Es **inyección, no edición**: `aurelius_face.html` queda intacto en el disco.

`/api/chat` se traduce a un stream NDJSON sintético de un solo trozo, porque la cara
lo lee con `body.getReader()` como si hablara con ollama y el gerente es de un
disparo. La cara no nota la diferencia.

### Requisitos

`pywebview` y `psutil`. El python del sistema está *externally-managed* (PEP 668), así
que las dependencias viven en un venv con acceso a los paquetes del sistema — hace
falta para ver `gi`/PyGObject, que es de apt y no se instala por pip:

```sh
cd ~/p0x
python3 -m venv --system-site-packages .venv-dashboard
.venv-dashboard/bin/pip install pywebview psutil
```

El venv está en `.gitignore`: se regenera con esos dos comandos.

### Cómo ejecutar

```sh
~/p0x/.venv-dashboard/bin/python ~/p0x/dashboard.py
```

### Acceso directo (menú de GNOME)

Un `.desktop` no expande `~` ni `$HOME`, así que el fichero se genera con las rutas
ya resueltas (heredoc sin comillas):

```sh
cat > ~/.local/share/applications/aurelius.desktop <<EOF
[Desktop Entry]
Name=Aurelius
Comment=El Preceptor, local. Sin red, sin sockets, sin nube.
Exec=$HOME/p0x/.venv-dashboard/bin/python $HOME/p0x/dashboard.py
Icon=utilities-terminal
Type=Application
Terminal=false
Categories=Utility;
StartupWMClass=dashboard.py
EOF
update-desktop-database ~/.local/share/applications/
```

El `Exec` apunta al python del venv, no a `python3`: el del sistema no tiene
pywebview. `Icon` usa un icono de tema porque no hay `icon.png` en el repo.

### Las tres capas, todas procesos hijos (D75)

El dashboard no habla por HTTP con nada. Llama a `~/aurelius-m1/aurelius`, que
ensambla modelo (`llama-cli`), carácter (`ARQUETIPO.md`) y voz (`piper`) por tubería.
La pregunta va por **ARGV**, no por stdin: el gerente es un wrapper de un disparo
(`llama-cli -no-cnv`), no un proceso conversacional.

El gerente resuelve `llama-cli`, el modelo y `ARQUETIPO.md` contra `$HOME`, pero los
tres se mudaron bajo `~/p0x/` y su literal se quedó viejo. `dashboard.py` lanza al
hijo con `HOME` apuntando a este repo **solo para ese proceso**, lo que alinea las
tres rutas sin tocar el gerente (que está fuera de alcance). `AQUI` del wrapper es
`dirname($0)`, así que `voces/` y `venv/piper` siguen resolviendo en `~/aurelius-m1`.
Si algún día el gerente se corrige, esta desviación sobra y no estorba.

La respuesta se pide con voz: `piper` deja el wav y el puente lo suelta en el primer
reproductor que exista (`pw-play`, `paplay`, `aplay`, `ffplay`, resueltos con
`which`), sin esperar a que termine — el texto ya está pintado y el audio no debe
retrasarlo.

### Tres footguns, con cicatriz

- **`about:blank` levanta un servidor HTTP.** `is_local_url()` de pywebview trata
  `about:blank` como url local, y eso arranca su servidor interno en `:42001` —
  medido, un `LISTEN` real, violación directa de D75. `file://` **no** lo dispara
  (está excluido explícitamente). Por eso la ventana nace con `html=` y la cara se
  carga después con `load_url(file://…)`. `dashboard.py` además comprueba en runtime
  que `webview.http.global_server` siga siendo `None` y lo grita si no.
- **`before_show` corre en otro hilo**, en carrera con `load_uri`: no sirve para
  registrar el user script a tiempo. El shim se registra desde `webview.start(func)`,
  esperando a que exista la instancia del backend, y sólo entonces se carga la cara.
- **La Fetch API rechaza el esquema `file://`** por diseño. `ALLOW_FILE_URLS` de
  pywebview mapea a `allow_file_access_from_file_urls`, que cubre XHR, no `fetch()`.
  Por eso los `fetch("models.json")` / `fetch("config.json")` de la cara fallaban en
  silencio: caía al literal de último recurso y pintaba el aviso naranja «point
  Aurelius at your model» con el modelo respondiendo ahí al lado. Los sirve el puente.

### El gerente, invocado a mano

`~/aurelius-m1/aurelius "di hola"` fuera del dashboard sí depende de que sus rutas
existan bajo `$HOME`. Se resolvió con dos enlaces —`~/aurelius-mvp` y
`~/soberano-bench`, ambos a sus destinos dentro de este repo—, aditivos y
reversibles con `rm`. El dashboard no los necesita: lleva su propio `HOME` para el
hijo, así que sigue funcionando aunque los enlaces desaparezcan.

### Verificado (2026-08-16)

Sin sockets (`lsof -a -i -n -P -p <pid>` vacío, en el proceso y en sus hijos WebKit);
RAM del dashboard 205 MB; «¿quién eres?» end-to-end por la UI real, con voz generada
y reproducida, en 4.35 s de media sobre tres muestras; aviso de configuración oculto.

Nota de método: `lsof -i -p <pid>` **sin `-a`** combina los filtros con OR y lista los
sockets de toda la máquina. La `-a` no es opcional.
