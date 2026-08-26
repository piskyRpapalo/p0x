# MAPA DE HARDWARE · la topología medida

**Medido:** 2026-08-26 21:33 WEST, desde `soberano`.
**Método:** `tailscale status`, apertura de puerto TCP uno a uno, y el sensor de
nodos que ya vive en el gateway de La Fragua (`/api/health/nodes`).
**Estado:** medido, no dictado. Donde una medida contradice al parte escrito, se
anota la contradicción en la §5 y **manda la medida**.


> **Sobre las direcciones.** Este mapa nombra los nodos por su nombre del
> tailnet y **no lleva ni una dirección IP**. No es un descuido ni una
> simplificación: la guardia de higiene de este repo las bloquea, y su motivo es
> el de siempre — lo que entra en la historia no se saca sin reescribirla. Se
> pierde menos de lo que parece: MagicDNS resuelve estos nombres allí donde
> resolvían las direcciones, y un nombre no caduca el día que una dirección
> cambia. Para verlas, en la máquina: `tailscale status`.

---

## 1 · Los nodos que responden

| Nodo | Usuario | Metal | Estado medido |
|---|---|---|---|
| **soberano** | `pisky` | Beelink · Ryzen 7 255 · 64 GB DDR5 · 1 TB NVMe · Radeon 780M | **en pie** · es esta máquina |
| **la-fragua** | `ubuntu` | Orange Pi 5 Plus · RK3588 8 núcleos ARM · 16 GB · 4 TB NVMe | **en pie** · 3 754 GiB montados, 57,6 usados |
| **el-vigia** | `pi` | Raspberry Pi + SDR + ESP32 | **en pie, con un sentido caído** (§3) |
| **la-torre** | `jetson` | Jetson Orin Nano Super 8 GB · CUDA 12.6 | **en pie y sirviendo** (§5.1) |

## 2 · Los nodos que no responden

| Nodo | Visto por última vez |
|---|---|
| `musculo-hp-01` | hace 32 días · inhabilitado por decisión del 2026-08-04 |
| `musculo-hp-02` | hace 18 días |
| `fedora` | hace 10 días |
| `desktop-quob12l` | `(el nodo equivocado)` · offline · **ojo a la §5.3** |

El teléfono de pruebas, `s110-1` (`s110-1`), está **activo** por enlace
directo en `(su direccion en la LAN)`.

## 3 · Puertos, comprobados de uno en uno

Abierto = se pudo abrir el socket desde `soberano`. Cerrado no siempre es
«caído»: un servicio atado a loopback está sano y es invisible desde aquí, y esa
diferencia se dice en vez de resolverse a ojo.

### la-fragua · la-fragua
| Puerto | Qué hay | Estado |
|---|---|---|
| 8001 | `HEXELION AIS Gateway` v0.3.0 · FastAPI, **43 rutas** | abierto · responde |
| 8100 | `El Faro` v0.1.0 · superficie M2M atestada | abierto · responde |
| 8765 | uvicorn | abierto · **colisiona con el Nexo local** (§5.4) |
| 11434 | Ollama | abierto · `qwen3:4b-instruct-2507-q4_K_M`, `qwen3:4b` |
| 6379 | Redis | cerrado desde el tailnet · el gateway lo reporta `redis: true`, así que **está sano y atado a loopback**, que es lo correcto |

### el-vigia · el-vigia
| Puerto | Qué hay | Estado |
|---|---|---|
| 80 · 8080 · 8090 | HTTP | abiertos · 200 los tres |
| 10110 | salida de `ais-catcher` | **cerrado** · es el flanco caído (§4) |
| 1883 | MQTT | cerrado desde el tailnet · el broker vive en la LAN |
| 6379 | Redis | cerrado desde el tailnet |

### la-torre · la-torre
| Puerto | Qué hay | Estado |
|---|---|---|
| 22 | SSH | abierto |
| 11434 | **Ollama** | **abierto y sirviendo dos modelos** |
| 8188 | ComfyUI | cerrado · instalado, no levantado |

### La red de casa
`la maquina del broker:1883` · broker MQTT · **abierto**. No cuelga de ningún nodo del
tailnet: vive en la LAN y se alcanza por ahí.

## 4 · El flanco caído · la RF del vigía

Medido por `/api/antenna/health` del gateway, no por lectura de un registro:

| Cadena | Vivo | Lo que dice el dato |
|---|---|---|
| **ADS-B** · `dump1090.service` · 1090 MHz | **sí** | 6 aeronaves · 1 351 mensajes · última hace 0,0 s |
| **AIS** · `ais-catcher.service` · 162 MHz | **no** | 0 buques · inalcanzable · `ais_port_10110_open: false` |

**El diagnóstico del parte no cuadra con la medida.** El parte dice «el dongle
NO está conectado o falló». Si el dongle estuviera ausente, ADS-B tampoco
recibiría — y ADS-B está recibiendo ahora mismo, con mensajes de hace menos de
un segundo. Lo que está caído es **`ais-catcher` y su puerto 10110**, no la
radio entera. Es otro fallo y pide otra reparación: mirar el servicio antes de
tocar el hardware.

Sigue siendo **crítico** y sigue pintándose en ámbar. Cambia la causa, no la
gravedad.

## 5 · Cuatro contradicciones entre el parte y el disco

**5.1 · La Torre no está dormida.** El parte dice «SIN SERVICIOS CORRIENDO ·
0 servicios». Ollama está escuchando en `:11434` y sirve dos modelos. Confirmado
por dos fuentes independientes: sondeo directo desde aquí, y `ollama_11434:
true` en el sensor de La Fragua. Lo que sí está dormido es **ComfyUI**: instalado
y sin levantar.

**5.2 · Redis no está «activo» de forma comprobable desde fuera.** Aparece en el
parte como servicio de dos nodos. Desde `soberano` no se alcanza en ninguno. En
La Fragua el gateway lo declara sano por su propio canal; en el vigía **no hay
dato** — y no tenerlo se dice, no se rellena.

**5.3 · El registro de nodos de La Fragua apunta a la máquina equivocada.**
Su tabla trae `soberano → (el nodo equivocado) · desktop-quob12l · offline`. El
`soberano` real es `soberano` y está en pie. Cualquier panel que se fíe de
ese registro dará por caído el nodo desde el que se mira. **No es un fallo del
panel: es un dato viejo en el gateway, y se arregla ahí.**

**5.4 · El puerto 8765 está pedido tres veces.** Lo usa el uvicorn de La Fragua,
lo usa el Nexo en esta máquina, y el encargo pedía montar ahí un servidor nuevo.
Dos de los tres son locales a máquinas distintas y no chocan; el tercero sí
habría chocado con el Nexo.

## 6 · Lo que este mapa NO afirma

- **Ningún proceso remoto se ha listado.** No se ha abierto una sola sesión SSH
  para escribir esto: todo sale de puertos y de las API que los nodos ya
  publican. Un inventario de procesos pide entrar en las máquinas, y entrar en
  otro nodo es una misión aparte.
- **Las bases de datos** (`vessel_db.sqlite`, `lab_registry.db`, `ironclaw.db`)
  se nombran en el parte y **no se han verificado**: viven dentro de La Fragua y
  desde aquí no hay forma de mirarlas sin entrar. `NO_DATA`.
- **El ESP32 con cámara** no se ha alcanzado. `NO_DATA`.
