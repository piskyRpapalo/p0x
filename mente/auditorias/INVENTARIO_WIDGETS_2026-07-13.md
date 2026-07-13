<!-- Documento-snapshot de la misión INVENTARIO TOTAL (2026-07-13).
     Sin front-matter §2 a propósito: es una fotografía verificada del sistema
     para alimentar el rediseño en Claude Design, no un MD evolutivo del grafo.
     Método: sondas read-only en vivo (curl, systemctl, sondas TCP) entre
     17:42 y 17:48 UTC del 2026-07-13. honest-sensors: todo lo listado como
     VIVO respondió en ese momento; lo demás está marcado tal cual. -->

# INVENTARIO DE WIDGETS Y MÉTRICAS · 2026-07-13

Misión INVENTARIO TOTAL · lectura + síntesis, cero cambios en el sistema vivo.
Este es el mapa de **qué apps y datos puede repartir David en el rediseño**.

Leyenda de estado: **VIVO** = respondió a la sonda de hoy · **VIVO-ESTIMADO** =
funciona pero el número es un modelo, no una medida · **VACÍO-HONESTO** =
cableado y funcionando, pero sin datos que mostrar (y lo dice) · **STALE** =
responde pero con datos viejos · **EN OBRA** = código existe, no desplegado.

---

## A · WIDGETS Y PANELES POR PÁGINA

Las 13 páginas del dashboard Hexelion y el Jardin respondieron **200** hoy.

### A.1 · El Nexo — `/dashboard` (portada, Sovereign default)

| Widget | Qué muestra | Fuente | Estado |
|---|---|---|---|
| Chip de atestación (cabecera) | ◇ firma del Faro: kid, método sha256, modo DRY_RUN | `/api/faro` | VIVO |
| Relojes de mercado | Hora PT / US / CN | JS local | VIVO |
| Punto de vida del Vigía | Latido del nodo sensor | pollers Redis | VIVO |
| **Miniatura viva del Jardin** | Feed de la cámara en miniatura (única puerta de David al Jardin); click → `/jardin/` | componente compartido `jardin-camera.js` → `/api/indoor/feed` | VIVO |
| Seed-reactor (hero) | Mapa mental decorativo (SÍNODO/CÓDICE/PRECEPTOR/AURELIUS…), toggle privacy | datos estáticos en el propio JS | VIVO (decorativo, no lee APIs) |
| SYSTEM STATE | Procesos tsp, reflejos (armado/watcher), salud de nodos, contadores de PENDIENTES y esferas | `/api/system/state` | VIVO |
| Energía · CPU | Vatios de la Fragua (etiqueta ESTIMATED) | `/api/energy/consumption` | VIVO-ESTIMADO |
| Energía · UPS | Estado OL/ON BATTERY + % batería | NUT vía gateway | VIVO (medido) |
| Energía · SOLAR | "NO GENERATION" | `/api/solar/latest` | VACÍO-HONESTO (hardware sin cablear) |
| Tesoro NEAR | Balance mainnet + testnet keyless | store del Alquimista | VIVO pero **frescura manual** (ver B) |
| Asesoría del Alquimista | Señal/flujo/consejo económico | `/api/alquimista/asesoria` | **STALE** — muestra congelada desde ~2026-06-23 (timer 15 min sigue PROPUESTO) |
| Drawer chat Sínodo | Chat SSE local + botón ▶ voz por respuesta | `/api/sinodo/chat` + `/api/voz/sintetizar` | VIVO |
| Bitácora Live (strip) | Narrativa de eventos (aeronaves, buques, pulso) | WS `/ws/bitacora` (Redis) | VIVO |
| Alertas OSINT | Feed GDELT vía OSIRIS (La Legión) | `/api/osint/alerts` | **STALE** (0 items, fuente marcada "no confiable") |
| Jurado | Veredicto de estrategias | `/api/jurado/latest` | VACÍO-HONESTO ("sin_veredicto") |
| Freno térmico (Arnés) | Estado brake/normalized de la Fragua | estado del gateway | VIVO |
| Economy summary | Economía DePIN legada (0 protocolos) | `/api/economy/summary` | VACÍO — legado, redundante con Cosecha |

### A.2 · Resto de páginas Hexelion (gateway :8001)

| Página | Paneles/widgets | Estado |
|---|---|---|
| `/tareas` | **Signature Tray**: filas de PENDIENTES + esferas "awaiting review"; acciones firmar/descartar con motivo | VIVO (bandeja vaciada por David el 07-12) |
| `/verde` | **Green Diary**: diario de capturas de la cámara con sensores incrustados en cada foto | VIVO (campo `analisis` = "pendiente-VLM" en todas — análisis aún no corre) |
| `/second-brain` | Grafo de fuerza del `mente/` (35 nodos / 55 enlaces), navegación ‹prev/next›, edición vía `/api/mente/editar` | VIVO (JSON regenerado en cada ingesta; último 07-11) |
| `/sinodo` | SÍNODO · AGENTS CORE: 6 agentes (monje, alquimista, escriba, vocero, berserker, enlace) con summary vivo cada uno + chat v2 por agente + voz + reset de modelo | VIVO (los 6 `active` hoy; bug conocido #67: flush del think_filter) |
| `/cosecha` | PROTOCOLOS ACTIVOS (9: grass, perceptron, honeygain, uprock, mastchain, acurast, dawnode, near, pawns · 6.18 € + 0.000108 BTC), NOTICIAS DePIN (RSS), ALERTAS | VIVO |
| `/maritimo` | Mapa AIS del Tejo (65 buques hoy), últimos eventos, botón reset antena | VIVO |
| `/aereo` | ADS-B (20 aeronaves hoy), distancia al nodo, reset antena | VIVO |
| `/map` | Mapa unificado (marítimo+aéreo) | VIVO |
| `/proof` | Proof Marketplace (vitrina de atestación) | VIVO |
| `/catastro` | EL CATASTRO: discos por nodo (qué ocupa qué) | VIVO |
| `/pregonero` | Alertas operativas (hoy: precio OMIE ≥ 150 €/MWh) | VIVO |
| `/status`, `/health`, `/metrics`, `/price` | Superficies M2M: JSON de estado, Prometheus, precio de atestación | VIVO |
| `/dashboard/lab-processes` | Procesos del lab (página v9 secundaria) | existe (no auditada en detalle hoy) |

Superficies hermanas fuera del gateway: **El Faro** :8100 (M2M atestación),
**TEJO ship map** :8765 (servicio propio), **preview tema violeta** :8009
(worktree servida; la rama NO está promovida — el tema de producción es verde).

### A.3 · Le Jardin des Ombres — `/jardin/` (nodo de Krista, build Vite estático)

| Widget/territorio | Qué es | Estado |
|---|---|---|
| WelcomeOverlay + RuneNav | Umbral de entrada + navegación por runas entre los 3 territorios | VIVO |
| La Sentinelle · Fenêtre (cámara) | Feed vivo + foto con métricas grabadas — mismo componente compartido `jardin-camera.js` del Nexo | VIVO |
| La Sentinelle · La Voix | Chat narrativo de la planta en francés (grounding honesto con medidas reales; inferencia en La Torre) | VIVO (⚠️ francés SIN validar por Krista — #76) |
| La Sentinelle · Le Cahier | Cuaderno de casa (verde/cuaderno.md) | VIVO |
| Le Grimoire · Herbier | Enciclopedia personal de plantas desde `verde/herbier/*.md` | VACÍO-HONESTO (`{"fiches":[],"estado":"vacio"}` — faltan los .md, #77) |
| L'Arcade · Le Docteur | Minijuego didáctico 1 | VIVO |
| L'Arcade · La Devinette | Minijuego didáctico 2 | VIVO |
| L'Arcade · Trivial | Minijuego 3 | **EN OBRA** — código sin commit y NO está en el build servido (dist es anterior al archivo) |
| Le Fantôme (Cortext) | Mascota perro-hueso, estados honestos | VIVO |

---

## B · MÉTRICAS QUE EL SISTEMA PUEDE LEER HOY

Cada fila sondada en vivo el 2026-07-13 (17:42–17:48 UTC). "Medida" = sensor o
fuente primaria real; "estimada" = modelo/proxy y así se etiqueta en la UI.

| Métrica | Fuente real | Unidad | Frescura | Tipo | ¿Viva hoy? |
|---|---|---|---|---|---|
| Temperatura ambiente | BME680 (M5 Atom, el Vigía) → Redis (TTL 30 s) → `/api/telemetry/m5` | °C | tiempo real (~5 s) | medida | ✅ (29.2 °C) |
| Humedad relativa | ídem | % | tiempo real | medida | ✅ (54 %) |
| Presión atmosférica | ídem | hPa | tiempo real | medida | ✅ (1008.6) |
| Gas / calidad de aire | ídem | Ω | tiempo real | medida | ✅ (82 kΩ) |
| Aceleración 3 ejes | ADXL345 (M5) | g | tiempo real | medida | ✅ (⚠️ eje z clavado en −2.048 = tope de rango; escala/orientación por revisar) |
| Hora RTC del M5 | RTC (M5) | ISO | tiempo real | medida | ✅ pero con **deriva ≈ −13 min** medida hoy (→ #51 re-sync) |
| Buques AIS | ais-catcher (el Vigía, SDR) → `/api/ships/live`, `/api/antenna/health` | buques, msg/min | tiempo real (último msg hace 1 s) | medida | ✅ (65 buques) |
| Aeronaves ADS-B | dump1090 (el Vigía, SDR) → `/api/aircraft` | aeronaves | tiempo real | medida | ✅ (20 visibles 9; 17.6 M msgs acumulados) |
| UPS estado + batería | NUT (GreenCell soberano) | OL/OB, % | tiempo real | medida | ✅ (OL, 100 %) |
| Potencia CPU Fragua | modelo lineal sobre uso de CPU | W | 1 min | **estimada** | ✅ (4.22 W) |
| Potencia La Torre | rail INA3221 (tegrastats) | W | periódica | medida | ✅ (4.82 W) |
| Potencia rack total | wattage nominal por nodo | W | 1 min | **estimada** | ✅ (66 W) |
| kWh día/semana | integración del proxy | kWh | continua | **estimada** | ✅ (1.17 kWh día) |
| Precio eléctrico OMIE | vocero-omie → Redis + TimescaleDB | €/MWh | horaria | medida (mercado) | ✅ (146–150 €/MWh) |
| Generación solar | — | W | — | — | ❌ `no_instalado` (hardware Aiko/Anker colocado, bridge sin cablear) |
| Tesoro NEAR (mainnet+testnet) | cosecha keyless del Alquimista → store NVMe | Ⓝ | **manual** (timer 15 min PROPUESTO, sin habilitar) | medida (on-chain) | ✅ dato válido pero la asesoría lleva ~20 días congelada (muestra hasta 2026-06-23) |
| Balances DePIN (9 protocolos) | actualizaciones al store de cosecha | puntos/tokens/€ | manual/periódica | medida (por protocolo) | ✅ |
| Noticias DePIN | RSS (CoinTelegraph et al.) | items | periódica | externa | ✅ |
| Alertas OSINT | GDELT vía OSIRIS (La Legión) | items | — | externa | ⚠️ STALE, fuente marcada no confiable |
| Cámara indoor (feed) | ustreamer en el Vigía → `/api/indoor/feed` (MJPEG) + `/api/indoor/foto` | vídeo/JPEG | tiempo real | medida | ✅ |
| Captura diaria al diario verde | timer de captura → `/api/verde/diario` (foto + sensores incrustados) | registro | diaria (hoy 08:20) | medida | ✅ (análisis VLM pendiente en todos los registros) |
| Reflejos (batería/térmico/vibración) | eventos en `mente/telemetria/reflejos.jsonl` | eventos | por disparo | medida | ✅ 3 ARMADOS · ⚠️ watcher 24/7 INACTIVO (unit sigue propuesta) |
| Salud de nodos | pollers → Redis → `/api/health/nodes` | online/degraded/down | ciclo ~1 min | medida | ✅ (4 online, 2 degraded: legion_sol y vigilante) |
| Sínodo (6 agentes) | La Torre (Ollama) + resúmenes por rol | estado+summary | por ciclo | medida | ✅ los 6 active |
| Faro: ledger + cadena + anchor | Redis del Faro + contrato NEAR testnet | clientes/créditos/seq | tiempo real | medida | ✅ (29/5/43 · chain=0 honesto en DRY_RUN · anchor epoch 25) |
| Voz local | Piper residente (p0x-voz) | 2 voces (davefx, sharvard) | bajo demanda | — | ✅ |
| Discos por nodo | disk_poller → `/api/disk/nodes` | GiB | periódica | medida | ✅ (NVMe 3.75 TiB, 40 GiB usados) |
| Cola de trabajo | task-spooler (`tsp -l`) vía SYSTEM STATE | jobs | tiempo real | medida | ✅ (cola vacía hoy) |
| Grafo del Second Brain | `second_brain.json` regenerado por la ingesta | 35 nodos / 55 links | por ingesta (últ. 07-11) | derivada | ✅ |
| Esferas / PENDIENTES | front-matter `mente/esferas/` + PENDIENTES.md | contadores | tiempo real | derivada | ✅ (15 esferas, 7 stubs · 96 filas) |
| Métricas Prometheus | `/metrics` | gauges | tiempo real | derivada | ✅ |
| Qdrant (vectores del mente/) | :6333 con API key | colecciones | por ingesta | derivada | ✅ (protegido, responde) |

---

## C · PREPARADO PERO NO CONECTADO

Lo que ya tiene sitio esperándole — cada punto es una app/dato futuro del rediseño.

| Pieza | Qué falta | Verificado hoy |
|---|---|---|
| **Solar Anker/Aiko** | Hardware instalado desde 06-15; falta `bridge_config.json` (integración HA, mano de David). `solar_bridge.py` staged inerte. El widget SOLAR del Nexo ya espera el dato. | `/api/solar/latest` = `no_instalado` |
| **ESP32 del jardín** | Colocados físicamente; el broker MQTT del Vigía no existe aún y no están flasheados. La arquitectura del Jardin (Fase 4) los espera. | puertos 1883 y 9001 del Vigía CERRADOS (sonda TCP) |
| **Herbier del Jardin** | Endpoint + UI listos; faltan los .md de herbología en `verde/herbier/` (solo hay README). Bloquea también "la voz cita el herbier" (#78). | `/api/jardin/herbier` = 0 fiches |
| **Residencia del modelo en La Torre** | Unit + timer + script en `deploy/torre/` PROPUESTOS sin instalar (1 paste). Bug pendiente: la Torre no carga CUDA (memoria 07-12). | archivos presentes, unit no instalada |
| **Timer de cosecha/asesoría del Alquimista** | Timer `*:0/15` PROPUESTO sin habilitar → el tesoro NEAR y la asesoría solo se refrescan a mano (hoy: 20 días congelada). | muestra de asesoría termina 2026-06-23 |
| **Watcher de reflejos 24/7** | Los 3 reflejos están ARMADOS pero la unit del watcher sigue propuesta (paste, #47). | `systemctl is-active reflejo-bateria` = inactive |
| **Tema violeta** | Rama + preview servida; sin promover (decisión #37 descartada → producción sigue verde). La preview sigue viva consumiendo un puerto. | :8009 responde 200 |
| **README público (hexelion-public)** | Commit local listo; sin push — espera el OK del Soberano (#62). | repo local presente |
| **Trivial (3er juego de L'Arcade)** | Código escrito, sin commit ni `npm run build` → NO está en el `/jardin/` servido. | dist anterior al componente; 0 refs en el bundle |
| **Cambios sin commitear** | `hexelion_gateway.py` (13 líneas) + 2 audit tools + screenshots nuevos; en el Jardin: roadmap + App + Devinette + copy.fr. Decidir y commitear. | `git status` de ambos repos |
| **Análisis VLM del diario verde** | Todos los registros con `analisis: pendiente-VLM` (#58). | `/api/verde/diario` |

*Última foto del sistema: 2026-07-13 · sondas 17:42–17:48 UTC · misión INVENTARIO TOTAL (read-only).*
