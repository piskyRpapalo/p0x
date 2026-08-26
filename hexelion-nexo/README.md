<div align="center">

# EL NEXO

**A read-only window over a four-node home rack.**
**Una ventana de solo lectura sobre un rack doméstico de cuatro nodos.**

<sub>🇬🇧 The server sends finished HTML. The browser places it. Nothing else.<br>
🇪🇸 El servidor manda HTML terminado. El navegador lo coloca. Nada más.</sub>

<img src="https://img.shields.io/badge/front--end-14%20KiB-3DF58F?style=flat-square&labelColor=060B09" alt="Front end: 14 KiB">
<img src="https://img.shields.io/badge/dependencies-0-3DF58F?style=flat-square&labelColor=060B09" alt="Dependencies: 0">
<img src="https://img.shields.io/badge/tests-126%2F126-3DF58F?style=flat-square&labelColor=060B09" alt="Tests: 126 of 126">
<img src="https://img.shields.io/badge/python-stdlib%20only-C6A664?style=flat-square&labelColor=060B09" alt="Python: standard library only">
<img src="https://img.shields.io/badge/cloud-none-C6A664?style=flat-square&labelColor=060B09" alt="Cloud: none">

</div>

---

🇬🇧 One Python process, no dependencies, no build step, no cloud. Sensors read
systemd, the disk and the rack; a single thread composes the readings into HTML;
Server-Sent Events push only what changed. The client is 51 lines and decides
nothing.

🇪🇸 Un proceso de Python, sin dependencias, sin paso de compilación, sin nube.
Los sensores leen systemd, el disco y el rack; un solo hilo compone las lecturas
en HTML; un flujo de eventos empuja solo lo que cambió. El cliente son 51 líneas
y no decide nada.

## Run it / Arrancarlo

```
git clone <this-repo> && cd hexelion-nexo
python3 servidor.py
```

🇬🇧 That is the whole installation. `http://127.0.0.1:8765`. No package manager,
no virtualenv, no `npm install`. Python 3.10 or newer.

🇪🇸 Esa es la instalación entera. Sin gestor de paquetes, sin entorno virtual,
sin `npm install`. Python 3.10 o más nuevo.

| Flag | |
|---|---|
| `--puerto N` | 🇬🇧 another port · 🇪🇸 otro puerto |
| `--sin-red` | 🇬🇧 the cut: remote nodes are not asked · 🇪🇸 el corte: los nodos remotos no se preguntan |
| `--ruidoso` | 🇬🇧 one line per request · 🇪🇸 una línea por petición |

🇬🇧 It binds to loopback, and a test pins that. Reaching the network is a
separate, deliberate step.

🇪🇸 Ata a loopback, y hay una prueba que lo fija. Salir a la red es un paso
aparte y deliberado.

## Configure / Configurar

```
cp .env.example .env                    # gateway + which node is this machine
cp rack.conf.example estado/rack.conf   # one line per node
bash pruebas                            # 126/126 · 2 suites
```

🇬🇧 All optional. With nothing configured the panel still starts and the cards
that depend on what is missing say `NO_DATA` with a cause. **Machine names never
enter the source** — they live in files git ignores.

🇪🇸 Todo opcional. Sin nada configurado el panel arranca igual y las tarjetas que
dependan de lo que falte dicen `NO_DATA` con su causa. **Los nombres de máquina
no entran nunca en el código** — viven en ficheros que git ignora.

## The rack it was built for / El rack para el que se hizo

🇬🇧 Named by MagicDNS, never by address. Four nodes, four states, all measured —
including the two that are not green.

🇪🇸 Nombrados por MagicDNS, nunca por dirección. Cuatro nodos, cuatro estados,
todos medidos — incluidos los dos que no están en verde.

| Node | Metal | State | |
|---|---|---|---|
| `soberano` | Mini PC · 8 cores · 64 GB | `ONLINE` | 🇬🇧 core, local inference · 🇪🇸 núcleo, inferencia local |
| `la-fragua` | ARM SBC · 16 GB · NVMe | `CRITICO` | 🇬🇧 gateway, attestation, RF · AIS probe aimed at the wrong host · 🇪🇸 gateway, atestación, RF · la sonda de AIS mira al nodo equivocado |
| `el-vigia` | SBC · camera · ESP32 | `ONLINE` | 🇬🇧 MJPEG camera, sensors · 🇪🇸 cámara MJPEG, sensores |
| `la-torre` | GPU module · CUDA | `ONLINE` | 🇬🇧 inference served · accelerated stack idle · 🇪🇸 inferencia servida · pila acelerada parada |

🇬🇧 That red went through two wrong diagnoses before it was right, and both are
worth the telling. First: "the radio is disconnected" — false, ADS-B is
receiving through it with sub-second message ages. Then: "the AIS service is
down on this node" — precise, and about **the wrong machine**. The chain had
moved, and the gateway's probe was still aimed where it used to live. A precise
diagnosis about the wrong host sends you to repair what is not broken.

🇪🇸 Ese rojo pasó por dos diagnósticos equivocados antes de acertar, y los dos
merecen contarse. Primero: «la radio está desconectada» — falso, ADS-B recibe
por ella con mensajes de hace menos de un segundo. Después: «el servicio de AIS
está caído en este nodo» — preciso, y sobre **la máquina equivocada**. La cadena
se había movido y la sonda seguía apuntando a donde vivía antes. Un diagnóstico
preciso sobre el nodo equivocado te manda a arreglar lo que no está roto.

🇬🇧 The panel now reports **where the probe is looking**, which is the only thing
it actually knows, and warns when that is not the node on the card.

🇪🇸 El panel ahora dice **a dónde mira la sonda**, que es lo único que sabe de
verdad, y avisa cuando eso no es el nodo de la tarjeta.

## Honest Sensors

> 🇬🇧 **With no data you say there is no data, with its cause.** Never a
> decorative zero, never a frozen screen, never a plausible guess.
>
> 🇪🇸 **Sin dato se dice que no hay dato, con su causa.** Nunca un cero
> decorativo, nunca una interfaz congelada, nunca una suposición verosímil.

🇬🇧 Easy to state, easy to violate. `systemd` reports `Result=success` for a
service that never ran — a timer armed for days would have rendered green,
identical to one that just finished cleanly. A missing probe once made a node
read as asleep, turning *we do not know* into a claim about the world. Both are
fixed, both have tests, and [ARCHITECTURE.md](ARCHITECTURE.md) explains why they
happened — with a Mermaid diagram of the whole data path.

🇪🇸 Fácil de enunciar, fácil de violar. `systemd` contesta `Result=success` para
un servicio que jamás arrancó — un timer armado durante días habría salido en
verde, idéntico a uno recién terminado. Una sonda ausente llegó a pintar un nodo
como dormido, convirtiendo *no lo sabemos* en una afirmación sobre el mundo. Las
dos están corregidas, las dos tienen prueba, y
[ARCHITECTURE.md](ARCHITECTURE.md) cuenta por qué ocurrieron.

## What it refuses to do / Lo que se niega a hacer

🇬🇧 The interesting decisions are refusals — they are what makes the numbers
work.

🇪🇸 Las decisiones interesantes son negativas — son las que hacen que los
números salgan.

- 🇬🇧 **No framework.** React, Vue, Angular, htmx, Alpine: none, not even
  vendored. Reactivity is `EventSource`; open/close is `<details>`. A test greps
  for each name. htmx minified alone is ~14 KB; this whole front end is 11.
  🇪🇸 **Sin framework.** Ninguno, ni vendorizado. La reactividad es
  `EventSource`; abrir y cerrar, `<details>`.
- 🇬🇧 **No write verb.** No POST, PUT, DELETE or PATCH — a test asserts all four
  are rejected. A panel that can turn things off is a command surface.
  🇪🇸 **Ni un verbo que escriba.** Un panel que puede apagar cosas es una
  superficie de mando.
- 🇬🇧 **No SSH.** A window that opens sessions into four machines every thirty
  seconds is not a window; it is an agent holding keys.
  🇪🇸 **Sin SSH.** No es una ventana: es un agente con llaves.
- 🇬🇧 **No JSON on the wire.** `data:` carries a finished section, so escaping
  happens once, in Python, on raw data.
  🇪🇸 **Sin JSON por el cable.** El escapado ocurre una vez y en un solo sitio.

## Publishing / Publicar

```
bash bin/sanitize_for_public.sh [target]
```

🇬🇧 Audits a `git archive HEAD` copy against eleven named patterns — addresses,
home paths, keys, tokens — checks the examples are present, and runs the test
suite **inside the copy**. It refuses rather than rewrites: a sanitiser that
substitutes leaves the job half done when it fails half way.

🇪🇸 Audita una copia sacada de `git archive HEAD` contra once patrones con
nombre, comprueba que los ejemplos están, y corre la tanda **dentro de la
copia**. Se niega en vez de reescribir.

## Layout / Estructura

```
servidor.py       http.server · allow-listed routes · GET and HEAD only
test_caos.py      chaos: break each thing, demand the truth · 20 cases
vigia.py          the single refresher thread · Condition, not polling
fragmentos.py     reading → HTML section · escaping in one place
sensores/         one module per source · reading, or a gap with a cause
estatico/         index.html + static/ · served locally, never from a CDN
pruebas           the test run · bash pruebas
```

## Licence

Apache-2.0 for the code. Prose under CC BY-SA 4.0.
