# EL NEXO · ventana de lectura sobre el ecosistema

Un micro-servidor de biblioteca estándar y una página sin dependencias que
enseñan, en una pantalla, en qué nivel corre el núcleo, qué hacen los bucles y
quién está en pie en el rack.

## Arrancar

```
cd ~/p0x/hexelion-nexo
python3 servidor.py
```

Y ya está: `http://127.0.0.1:8765`. Sin paquete, sin entorno virtual, sin
`pip install`. Ctrl-C para parar.

| Opción | Qué hace |
|---|---|
| `--puerto N` | otro puerto |
| `--sin-red` | **el corte**: los nodos remotos no se preguntan y salen `NO_DATA` |
| `--ruidoso` | una línea por petición |
| `--anfitrion` | por defecto `127.0.0.1`, y salir de ahí se firma aparte |

### La única configuración

El panel necesita saber dónde está el gateway de la forja para las sondas
profundas de nodo. **No vive en el repo** — la guardia de higiene bloquea rutas
de nodo en la historia, y con razón. Se declara en la máquina:

```
echo 'http://<nombre-del-gateway>:8001' > estado/gateway.conf
```

O con `NEXO_GATEWAY` en el entorno, que manda sobre el fichero. Sin ninguna de
las dos el panel arranca igual: los nodos se siguen midiendo por el tailnet y la
tarjeta dice qué le falta.

## La tanda de pruebas del núcleo

Correr 526 pruebas tarda minutos, así que no se mide desde una petición HTTP. Se
mide a mano y el panel lee lo medido **con su hora al lado**:

```
python3 -m sensores.preceptor --medir
```

Pasadas 24 h la cifra se marca rancia. Un «526/526» sin fecha no distingue una
tanda de hace un minuto de una de hace tres semanas.

## Verlo desde el teléfono

**Hoy no se puede, y es a propósito.** El servidor ata a `127.0.0.1` y hay una
prueba que lo fija, para que salir al tailnet no ocurra por descuido.

Cuando se firme, hay dos caminos y **ninguno es gratis**:

```
# A · una ruta en el serve que ya existe
tailscale serve --bg --set-path=/nexo 8765

# B · un puerto propio
tailscale serve --bg --https=8766 8765
```

Lo que hay que saber antes de elegir: `https://<este-nodo>/` ya está tomado —
sirve la PWA del núcleo en el 8740. **A** no la mueve pero modifica un mapeo ya
firmado; **B** lo deja intacto y abre una segunda superficie en el tailnet. En
los dos casos el panel queda alcanzable por cualquiera que esté en el tailnet, y
el panel no pide contraseña porque **no tiene nada que proteger**: no hay un solo
verbo que escriba en él.

## La arquitectura, y por qué esta

**Un solo lector, muchos mirones.** Un hilo refresca la instantánea cada 30 s y
la deja compuesta **en HTML**. Los flujos abiertos no leen sensores: esperan a
que suba el número de versión y reciben lo que cambió. Abrir una pestaña más
cuesta un socket, no una ronda de sondas — y cuando el sensor del rack tarda
cuatro segundos contra el tailnet, quien espera es el refrescador, no quien
mira.

**El servidor emite HTML, no JSON.** Por `/api/flujo` viajan Server-Sent Events
cuyo `data:` es una sección terminada. El navegador no parsea ni decide: coloca
la cadena. El escapado ocurre una vez, en Python, sobre el dato crudo.

**Cero dependencias, y medido.** No hay React, Vue, Angular, htmx ni Alpine —
ni remotos ni vendorizados. La reactividad la da `EventSource`, que es del
navegador. Hay una prueba que barre los tres ficheros buscando cada uno de esos
nombres.

| | |
|---|---|
| La cara entera, descargada | **11 KiB** (html + css + js) |
| JS del cliente | **51 líneas** · antes eran 244 con siete pintores |
| Servidor en memoria | **29 MB RSS** · el intérprete vacío ya son 9,7 |
| Dependencias | **0** |

Sobre los 29 MB: el objetivo de 10 no se alcanza y no se va a alcanzar con
CPython — un intérprete vacío en esta máquina son 9,7 MB y los `import` hacen el
resto. Se dice en vez de redondear hacia el número que se pedía.

## Qué hay dentro

```
servidor.py            http.server · lista blanca de rutas · solo GET/HEAD
vigia.py               el hilo único que refresca · Condition, no sondeo
fragmentos.py          lectura -> sección HTML · el escapado, en un solo sitio
sensores/              un módulo por fuente · contrato: dato o hueco con causa
  registro.py          la única lista de sensores
  soberania.py         pregunta al guardián del núcleo · no recalcula nada
  timers.py            systemctl show · nunca list-timers
  preceptor.py         versión en vivo + tanda medida con su edad
  lora.py  cinek.py  jardin.py  nodos.py
estatico/index.html    siete secciones vacías · las llena el flujo
estatico/static/       hexelion.css · nexo.js · servidos de aquí, nunca de una CDN
estado/                gateway.conf y tanda.json · local, sin versionar
pruebas                la tanda · `bash pruebas`
```

## Las tres reglas que gobiernan todo esto

1. **Solo mira.** No hay POST, ni PUT, ni DELETE, ni PATCH, ni una sesión SSH.
   Una ventana que puede apagar cosas es una superficie de mando.
2. **Sin dato se dice que no hay dato**, con su causa. Nunca un cero decorativo,
   nunca una interfaz congelada. Cuando el servidor calla, la página no se vacía
   —lo medido sigue siendo cierto de cuando se midió— pero deja de presentarse
   como viva.
3. **Un sensor caído no tumba a los demás.** Sale su hueco; el resto sigue.

## Lo que este panel no dirá aunque se le pida

La Torre sale **ONLINE**, no «dormida»: Ollama está sirviendo dos modelos, y eso
está medido por sondeo directo y confirmado por el sensor de la forja. Lo que
duerme ahí es ComfyUI.

El vigía sale **CRÍTICO** con la causa medida — `ais-catcher` caído, puerto
10110 cerrado — y no con «dongle desconectado físicamente»: si el dongle
faltara, ADS-B tampoco recibiría, y ADS-B trae aeronaves con mensajes de hace
menos de un segundo. Mismo rojo, distinta reparación.
