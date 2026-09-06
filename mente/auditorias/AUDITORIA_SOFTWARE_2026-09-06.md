# Auditoría de software del nodo `soberano` · 2026-09-06

**Alcance honesto.** Todo lo de aquí está **medido en `soberano`** el 2026-09-06. Los otros nodos no
se auditan desde esta consola: `soberano` es propose-only hacia fragua/torre/vigía, y además el
gateway de La Fragua no contestaba durante la medición. Para ellos: **NO_DATA**, y la auditoría sale
como propuesta cuando alguien tenga esa consola delante.

**Disco al empezar:** 915 G totales · **513 G usados (59 %)** · 357 G libres · 282 procesos de usuario.

---

## 1 · Lo que no coopera con la política del nodo

Ordenado por gravedad, no por tamaño. «Consecuencia» es lo que pasa *hoy*, no lo que podría pasar.

### 🔴 A1 · Sesenta servidores web huérfanos, treinta y ocho de ellos abiertos a toda la red

**Medido:** 60 procesos `python3 -m http.server`, **1.353 MiB de RSS**, ocupando los puertos
8126–8395. **38 escuchan en `0.0.0.0`** — no en loopback. El más viejo arrancó el 2026-09-05 a las
12:08 y sigue en pie.

**De dónde salen:** del truco que el propio Ojo documenta en `recursos.json` — *«servir la web en
OTRO puerto para verla de verdad»*, porque un origen nuevo no tiene service worker registrado. El
truco es correcto. Lo que falta es el final: nadie los apaga.

**Consecuencias, y son tres distintas:**
1. **Exposición.** 38 sockets sirven `preceptoros-web/public` a la LAN entera y al tailnet. Nadie lo
   decidió: `--bind 0.0.0.0` se escribió una vez y se copió cuarenta.
2. **1,3 GB de RAM** retenidos por servidores que nadie va a visitar, en la máquina que decide si
   cabe una forja de LoRA. El vector de estado los estaba contando como RAM ocupada legítima.
3. **Deriva de puertos.** Cada sesión coge el siguiente libre: la numeración ya va por 8395.

**Servicios enlazados:** ninguno depende de ellos. Son hojas.

**Detalle que importa:** a partir del 8161 los servidores **sí** escuchan en `127.0.0.1`. Alguna
sesión posterior corrigió la práctica sin limpiar lo anterior. El arreglo está descubierto; lo que
falta es aplicarlo hacia atrás.

> ⚠️ **Trampa al limpiar, ya documentada en `recursos.json`:** `pkill -f <patrón>` encuentra
> **también al shell que lo invoca**. Hay que filtrar por el patrón exacto y excluir el propio PID, o
> la sesión se mata sola a mitad de limpieza.

### 🔴 A2 · Telemetría de Canonical, activa y subiendo

**Medido:** `ubuntu-insights-collect.timer` y `ubuntu-insights-upload.timer` **vivos**, con última
subida el 2026-09-05 y la siguiente programada. `ubuntu-report.path` habilitado en las unidades de
usuario. `apport` activo.

**Consecuencia:** un nodo cuya doctrina es *«nada sale del nodo»* tiene tres canales que envían datos
de uso y volcados de fallo a un tercero, en el arranque, sin que nadie los haya firmado. No es una
brecha: es una **contradicción declarada entre lo que el nodo dice y lo que hace**.

**Servicios enlazados:** ninguno del rack. Se pueden parar sin tocar nada nuestro.

### 🟠 A3 · `preceptor-cazanido-v2:latest` sigue instalado, y está roto por escrito

**Medido:** 2,0 GB en Ollama. El glosario del Ojo lo dice literal: *«es un adapter de Qwen colgado de
una base Llama y muere al arrancar»*.

**Consecuencia:** un modelo que no arranca ocupando sitio y, peor, **apareciendo en `ollama list`**
como si fuera una opción. El enrutador del Ojo lo listaría como instalado. Un catálogo con una
entrada muerta es un catálogo en el que hay que saber cosas para no equivocarse.

### 🟠 A4 · Cuatro tags pelados, contra el canon

**Medido:** `preceptor-cazanido-v2:latest`, `preceptor-cazanido:latest`, `preceptor-v7:latest`,
`oficial-inventario:latest` (este último, **16 GB**).

**Consecuencia:** el canon los prohíbe porque apuntan a variantes Thinking con razonamiento no
desactivable. En un bucle eso es tiempo de pared invisible — la misma avería que el canon ya midió:
45 tokens de pensamiento para responder una palabra.

### 🟡 A5 · Docker levantado para una sola cosa, con 7,3 GB de sobra

**Medido:** `docker` + `containerd` activos al arranque. **Un** contenedor: `open-webui` en
`0.0.0.0:3000`, 31 h en pie. 3 imágenes, 8,07 GB, de los cuales **7,3 GB (90 %) reclamables**.

**Consecuencia:** dos demonios de sistema y un puerto abierto a la red para una interfaz web de
Ollama que duplica lo que ya hacen el Ojo y la app. Y `open-webui.service` está **habilitado al
arranque** en las unidades de usuario, o sea que vuelve solo.

### 🟡 A6 · El escritorio entero corriendo en un nodo de cómputo

**Medido y activos:** `cups` (impresión), `avahi-daemon` (descubrimiento mDNS), `ModemManager`,
`bluetooth`, `snapd` (3,2 GB de almacen propio, 11 snaps incluidos **Firefox, Brave y
Thunderbird**), `unattended-upgrades`, y la pila de Evolution (calendario y libreta) viva en la
sesión de usuario.

**Consecuencia:** no es urgente y no rompe nada, pero es superficie: `avahi` anuncia el nodo en la
red local, `unattended-upgrades` cambia paquetes sin firma del Soberano —incluido, algún día, un
runtime del que depende una medida—, y tres navegadores mantienen tres perfiles.

---

## 2 · Espacio: dónde está y qué se puede recuperar

| Qué | Tamaño | Estado | Recuperable |
|---|---:|---|---:|
| `p0x/ComfyUI/models` | **157 G** | CineK **archivado hoy** en GitHub · sin tocar desde 2026-08-07 | 157 G |
| `.cache/huggingface` | **41 G** | caché re-descargable | 41 G |
| `.ollama` | 38 G | 8 modelos; 2 rotos o superados | ~20 G |
| `p0x/soberano-bench/models` | 20 G | el modelo del nodo vive aquí | parcial |
| `.config/Claude` | 13 G | estado de la app de escritorio | — |
| `.cache/uv` | 10 G | caché re-descargable | 10 G |
| Docker (imágenes) | 8,1 G | 90 % sin usar | 7,3 G |
| Chrome (config + caché) | 6,4 G | | 1,5 G |
| almacen de `snapd` | 3,2 G | revisiones viejas incluidas | ~1 G |
| `~/Downloads` | 4,4 G | | a criterio |

**Recuperable sin tocar nada vivo: ≈ 240 GB.** El disco pasaría de **59 % a ~33 % usado**, de 357 G
libres a **~597 G**.

**La decisión que no es mía:** los 157 G de ComfyUI son 75 G de *text encoders* y 68 G de
*diffusion models*. Son re-descargables, pero re-descargarlos cuesta ancho de banda y tiempo. CineK
está congelado y archivado; si el Soberano lo da por cerrado, se van. Si no, **se mueven a frío**, no
se borran.

---

## 3 · Lo que sí está limpio, y conviene no tocarlo

- **El enjambre**, con sus tres timers dedicados y firmados: `afinador.timer` (L1),
  `guardian.timer` (L1), `curador.timer` (L3). Corren, tienen dueño y su unidad está documentada.
- **`preceptoros-pwa.service`** — la app en `127.0.0.1:8740`, en loopback, como debe.
- **Ollama** en `*:11434`, consultado por loopback desde el Ojo.
- **El Ojo** y su vector: 5 sondas declaradas, ~100 ms, sin SSH.

---

## 4 · Plan de limpieza, por orden de retorno

**EJECUTADO el 2026-09-06** tras la firma del Soberano, salvo lo que exige `sudo`
o una decision suya. Lo que se hizo y lo que devolvio:

| # | Estado | Resultado real |
|---|---|---|
| L1 | ✅ hecho | **59 servidores apagados**, 0 sockets en `0.0.0.0:81xx`, RAM disponible de 32,7 a 37,7 GB |
| L2 | ✅ parcial | `ubuntu-insights-collect/upload.timer` y `ubuntu-report.path` **enmascarados**. `apport` sigue: es de sistema y aqui no hay sudo |
| L3 | ✅ hecho | retirados `preceptor-cazanido-v2:latest` (roto) y `preceptor-cazanido:latest` (superado) |
| L4 | ✅ hecho | `docker image prune -af` devolvio **228 MB**, no los 7,3 GB estimados: el resto lo sostiene el contenedor vivo |
| L5 | ✅ **afinada** | 27 GB de modelos de video de CineK + 9,8 GB de cache de `uv`. **NO se borro la cache entera**: guardaba `unsloth/Llama-3.2-3B` (6,1 GB) y `Qwen3-4B` (7,6 GB), que son las bases de forja de LoRA. Borrarlas habria obligado a redescargarlas para el primer Mistral |
| L6 | ⏸️ espera | los 157 GB de ComfyUI siguen ahi: frio o fuera es decision del Soberano |
| L7 | ⏸️ propone | snaps y demonios de escritorio exigen sudo |
| L8 | ✅ parcial | creados los tags explicitos `preceptor-v7:llama3.2-1.0` y `oficial-inventario:q4-1.0`. **Los pelados NO se retiran**: `preceptor-v7:latest` es el modelo que sirve el rack por el tunel, y quitarlo romperia a quien lo llame asi. La migracion de los que llaman es tarea aparte |

Lo que sigue sin ejecutarse queda como estaba:

| # | Qué | Coste | Devuelve |
|---|---|---|---|
| L1 | Matar los 60 `http.server` huérfanos, con el filtro que no se suicida | S | 1,3 GB RAM · 38 puertos cerrados |
| L2 | Parar y enmascarar los timers de `ubuntu-insights` + `ubuntu-report.path` + `apport` | S | coherencia con la doctrina |
| L3 | `ollama rm preceptor-cazanido-v2:latest` (roto) y `preceptor-cazanido:latest` (superado por v3) | S | ~4,5 GB |
| L4 | `docker image prune` · decidir si `open-webui` se queda | S | 7,3 GB |
| L5 | Vaciar `.cache/huggingface` y `.cache/uv` | S | 51 GB |
| L6 | Decidir el destino de los 157 G de ComfyUI: frío o fuera | M | 157 GB |
| L7 | Retirar snaps de navegador que no se usan; revisar `cups`/`avahi`/`bluetooth`/`ModemManager` | M | ~2 GB + superficie |
| L8 | Poner tag explícito a `preceptor-v7` y `oficial-inventario` | S | cumple canon |

**Lo que NO propongo:** tocar unidades de systemd nuevas ni cronificar la limpieza. Crear una unidad
es dejar algo corriendo con tus permisos cuando no miras, y eso se pide firmado, una por una — el
canon del nodo ya lo dice.

---

## 5 · Cómo se sostiene esto en el tiempo

El hallazgo A1 no es un descuido de nadie: es un **proceso sin final**. El truco de servir en otro
puerto está documentado como recurso; lo que no estaba escrito es que **hay que apagarlo**. Dos
propuestas para que no vuelva:

1. Que el recurso «servir la web en otro puerto» de `recursos.json` lleve su cierre en la misma
   ficha: `--bind 127.0.0.1` y cómo se apaga.
2. Que el vector del Ojo cuente los servidores huérfanos como una lectura más. Lo que no se mide,
   vuelve.
