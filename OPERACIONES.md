# OPERACIONES P0X — lecciones y herramientas para el silicio que venga
> Cuaderno de ingeniería del rack (fuera de `mente/`: esto es método operativo,
> no conocimiento del Soberano). Append-only por sesión de misión. Quien herede
> este sistema (Sonnet/Opus/Fable/otro) empieza leyendo esto + `MANUAL_DEL_SOBERANO`
> (`mente/manual/`) + la última auditoría (`mente/auditorias/`).

## Lecciones aprendidas (con cicatriz)

### 2026-07-06 · PATH de systemd ≠ PATH interactivo (misión VENTANA VIVA)
- **Síntoma**: Observar moría con `FileNotFoundError: 'yt-dlp'` solo cuando el job
  nacía del gateway; el E2E manual pasaba (transcript en cache saltaba yt-dlp).
- **Causa**: los servicios systemd NO cargan `~/.bashrc` → su PATH no trae
  `~/.local/bin`. El server tsp hereda el env de QUIEN LO PARIÓ (el primer
  `p0x-enqueue`), así que todos los jobs de la cola arrastran el PATH deficiente.
- **Regla**: todo binario invocado desde pipeline se resuelve con
  `shutil.which() + fallback absoluto` (patrón `YTDLP_BIN`/`WHISPER_BIN` en
  `pipeline/ingest_youtube.py`). `bin/p0x-enqueue` exporta `~/.local/bin` al PATH.
- **Al cambiar env de la cola**: `tsp -K` con cola vacía para que el server
  renazca limpio; verificar antes con `tsp -l`.

### 2026-07-06 · Solapes de UI: audita cajas, no ojos
- `hexelion/tools/audit_overlaps.py` (repo hexelion) — Playwright, 4 páginas ×
  1440/768/390/Pixel7, bounding boxes de clicables con clipping por ancestros
  `overflow` (lo scrolleado fuera de un panel NO colisiona) y exclusión de
  `.leaflet-marker-icon` (clustering geográfico = datos, no layout).
  Criterio de la casa: **0 colisiones**; exit code 2 si hay alguna.
- La colisión clásica: elementos `position:fixed` sobre headers (logo pisando
  CLEAR ALL). Cura: meter el elemento al flujo flex del header, no z-index wars.

### 2026-07-06 · Voz local (Piper) — números medidos en la fragua
- Cadena en `hexelion/voz_api.py`: cache sha256(voz|texto) → residente
  127.0.0.1:8021 → subprocess frío niced. Medido: frío 3705ms / residente
  681ms / cache 29ms. RSS residente ~272MB (davefx).
- La síntesis NO usa la cola tsp (un ▶ del chat no puede esperar detrás de un
  job de 40 min); serializa con semáforo propio + nice/ionice.
- Voz por defecto davefx (Gate 0: modelo 17% menor, RSS -44MB, misma velocidad).
  Clips de comparación: `hexelion/assets/voz-gate0/` y `voz/gate0/metricas.txt`.
- Residente = unit `deploy/fragua/p0x-voz.service` PROPUESTA (veto clasificador
  al silicio; paste patrón #4 en el commit a269912).

## Los lazos vivos (loops) y cómo probarlos
- **Observar**: `POST :8001/api/observar/ingest {url, comentario}` → tsp →
  `pipeline/observar_runner.py` (guard térmico 80°C + pacing 78→74°C) →
  `pending_review` → ACCEPT/DISCARD UI → `ingest_mente.py` → `gen_niveles.py`
  → segunda ingesta (los niveles del nodo nuevo entran al grafo). Estado por
  job en `pipeline/observar/<job>/{state.json,runner.log}`.
- **Ingesta mente**: `p0x-enqueue python3 mente/pipeline/ingest_mente.py` —
  manifest sha256, solo lo cambiado; SIEMPRE regenera grafo → copia a
  `hexelion/assets/second_brain.json`. SCOPE_DIRS vive en DOS sitios
  (ingest_mente.py y skills/auditar-p0x/scripts/audit_lib.py): tocar ambos.
- **Voz**: `curl -X POST :8001/api/voz/sintetizar -d '{"texto":"..."}'` → wav;
  telemetría en `mente/telemetria/voz.jsonl`.
- **Auditoría**: `bash skills/auditar-p0x/run_audit.sh` (mantenimiento).
- **Cola**: `tsp -l` (estado), `tsp -K` (matar server, solo con cola vacía).

## Invariantes que NO se negocian (resumen operativo)
IronClaw propose-only en `mente/` (diffs `.patch` en `mente/auditorias/`, firma
del carbono aplica) · voz/texto jamás salen del rack · fragua encolada + pacing
térmico · torre intocable (receta certificada, tags instruct explícitos) ·
backup `.bak-YYYYMMDD` + screenshot antes/después en todo lo visible ·
commit por bloque, push soberano (p0x→jetson, hexelion→torre).

## Release v1.3 en BORRADOR · esperando firma (2026-08-31)

Existe un release **draft** en `piskyRpapalo/PreceptorOS` con tres assets.
**No está publicado, y publicarlo es firma del carbono.**

- Ver: `gh release view v1.3 --repo piskyRpapalo/PreceptorOS`
- Publicar: `gh release edit v1.3 --draft=false --repo piskyRpapalo/PreceptorOS`

**El tag `v1.3` NO existe todavía en el remoto** — comprobado, 0 refs. GitHub
lo crea al publicar, no al guardar el borrador. Por eso un draft no viola la
regla de «sin push»: no hay ni un objeto nuevo en la historia del repo.

Estado de pruebas de los assets, medido y no supuesto:

| Asset | Estado |
|---|---|
| `install.sh` · Linux | **PROBADO** el 2026-08-31 de punta a punta, con `HOME` aislado y clonando del árbol local: requisitos → clon → entrada de escritorio → instrucciones. El `HOME` real quedó intacto |
| `install.sh` · macOS | NO PROBADO · no hay máquina macOS en el rack |
| `install.ps1` · Windows | NO PROBADO · no hay `pwsh` ni máquina Windows en el rack |
| `INSTALACION_ANDROID.md` | Termux funciona; el APK no existe y la guía lo dice en su §3 |

**Lo que la web sigue diciendo es correcto y no hay que tocarlo**: un borrador
no es público, así que `releases/latest/download/install.sh` sigue dando 404 y
los dos NO_DATA de `instalar.html` siguen siendo ciertos. El día que se firme
la publicación, ESE es el momento de revisarlos — no antes.

## Panel de herramientas del Ágora · para qué es (2026-08-31)

Bajo el chat hay un `#herramientas` que crea `chat-router.js` (no está en el
marcado: las tres portadas van justas de bytes). Hoy aloja lo que se sacó del
chat por no ser conversación — descargar modelo, motor, IA local, dictado.

**Lo que va a alojar, firmado por el Soberano:** los datos del modelo activo
junto a sus «available tools», una caja de descripción, y debajo **cajas de
palabras clave que son DISPARADORES del LoRA**. No son metadatos: son el
interfaz por el que el usuario arma qué activa a su compañero.

Eso lo ata a `mente/doctrina/LORATELIER_P0X.md` por el extremo contrario al
botón «corregir esta respuesta»: uno recoge correcciones, el otro define
disparos. Con D1-D4 abiertas, **el panel puede existir vacío; los disparadores
no se activan sin firma**.

## El tope por fichero de la web · 16 KiB, medido (2026-09-05)

El tope llevaba en 10 KB desde que el Soberano lo puso a mano. Sube a **16 KiB
(16.384 B)**, y esta vez sale de una cuenta que se deja aquí para que la
próxima revisión discuta con datos y no con gusto.

**Lo que se descubrió al medir: el tope de 10 KB nunca fue un límite de red.**
Los 77 ficheros que la regla vigila comprimen **2,43x** de media —458.360 B en
disco contra 188.656 B con `gzip -9`—, así que uno de 10.240 B viajaba como
~4.214. La ventana inicial de congestión son ~14 KB (diez paquetes de ~1.460),
o sea que el tope viejo gastaba **menos de un tercio** del primer viaje de ida
y vuelta. Sobraba red por todas partes.

**Lo que sí acotaba era el razonamiento.** El **43 %** de un fichero de este
árbol es prosa, porque aquí los comentarios son la documentación. A 10.240 B
eso deja ~5.850 B de código útil; en cuanto una pieza pedía 6,5 KB, lo que se
recortaba era el porqué. Pasó de verdad en la sesión del 2026-09-05: se limaron
comentarios propios **seis veces seguidas** para volver bajo el tope, que es
exactamente lo que «se parte, no se recorta» viene a impedir.

**La aritmética del número nuevo.** Se reparte la ventana inicial y se le da a
un fichero la mitad —varios se piden en paralelo y comparten ese vuelo—: 7 KB
en el cable. A 2,43x son 17,4 KB en disco, redondeado a la baja al binario
limpio: **16 KiB**. Comprobado al revés: 16.384 B viajan como ~6.743, el 48 %
de un viaje.

**No se queda en una suposición.** El tope de disco es un proxy, así que entró
con `test_ningun_fichero_gasta_medio_viaje_de_red`, que comprime cada fichero y
lo mide contra ese medio viaje. Un ratio medio deja de valer en cuanto entra
algo que comprime mal —base64, rutas SVG largas—, y una regla que se cumple por
casualidad se rompe el día que alguien cambia lo casual.

**Lo que desbloquea, y por qué importa para refactorizar.** `sw.js` gana 6,1 KB,
que a ~22 B por línea de precache son sitio para ~270 ficheros más. La razón por
la que un `capas.css` se escribió y se deshizo el mismo día —su etiqueta dejaba
`sw.js` en 10.244 B— deja de existir. A partir de aquí **partir por asunto ya no
cuesta una ranura**: se puede separar sin negociar con el tope.

La cifra es pública: se anuncia en las tres portadas y en el README, así que se
cambia en los cinco sitios a la vez. Enmienda propuesta para `METRICAS_NORMA.md`
en `propuestas/2026-09-05_tope-fichero-web.md` — ese documento es
`editor_autorizado: carbono` y solo el Soberano lo canoniza.
