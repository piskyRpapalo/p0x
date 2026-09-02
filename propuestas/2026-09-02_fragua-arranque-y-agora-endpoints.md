# Propuesta · `la-fragua`: que el Ágora sobreviva a un reinicio, y las tres rutas que la web ya llama

**Nodo destino:** `la-fragua` (Orange Pi 5 Plus, usuario `ubuntu`)
**Origen:** `soberano` · **Fecha:** 2026-09-02
**Estado:** PROPUESTA — no aplicada. `la-fragua` es propose-only desde `soberano`.
Lo único que se hizo contra ese nodo fue **leer** (`ssh` en solo lectura y `scp` de
un fichero hacia aquí). No se escribió nada allí.

---

## 1 · El túnel no se cae «porque se lanza a mano». Se cae por `Linger=no`

El encargo daba por supuesto que no había unidad systemd. **La hay, y está
activa.** Medido hoy, en solo lectura:

| comprobación | salida real |
|---|---|
| `ls ~/.config/systemd/user/agora-tunnel.service` | existe, 665 B, 30 ago 16:46 |
| `systemctl --user is-enabled agora-tunnel.service` | `enabled` |
| `systemctl --user is-active agora-tunnel.service` | `active` |
| `ps -C cloudflared` | vivo desde hace `20:00:01` |
| `uptime` | `up 20:13`, **2 users** |
| `loginctl show-user ubuntu -p Linger` | **`Linger=no`** ← |

Un servicio **de usuario** con `Linger=no` solo existe mientras haya una sesión
abierta de ese usuario. El gestor `systemd --user` arranca al primer login y
muere con el último. Hoy el túnel está arriba porque **hay dos sesiones
abiertas**, no porque el sistema lo levante.

Reiniciar la Orange Pi sin que nadie entre por SSH = `systemd --user` no
arranca = `agora-tunnel.service` no arranca = `api.preceptoros.org` cae. Que
haya sobrevivido a este reinicio no lo desmiente: lo explica.

**Y hay un segundo agujero, más grande:** la API que el túnel publica **no
tiene unidad ninguna**. Corre suelta:

    4371  <home de ubuntu>/venvs/agora/bin/python3  ...  uvicorn agora_api:app --host 127.0.0.1 --port 9002

Aunque se arregle el linger, tras un reinicio subiría el túnel y **no la API**:
`api.preceptoros.org` respondería 502 a todo. Un túnel a un pasillo vacío.

### Lo que hay que ejecutar a mano (un solo `sudo`, y va primero)

```bash
sudo loginctl enable-linger ubuntu
```

```bash
loginctl show-user ubuntu -p Linger    # debe decir Linger=yes
```

### La unidad que falta: `agora-api.service`

Nueva unidad → **firma explícita del Soberano, una por una** (canon del nodo,
2026-08-24), y anotarla en `deploy/<nodo>/unidades.md`. El artefacto está en
`deploy/fragua/agora-api.service`. No lleva dentro ni la IP de la Ollama ni la
ruta del NVMe: las dos son datos de infraestructura y la guardia de higiene
marca `[IP-TAILNET]` (regla que **ni `guardia:permitir` exime**) y `[RUTA-HOME]`.
Viven en un fichero del propio nodo:

```bash
install -d -m 700 ~/.config
printf 'OLLAMA_HOST=http://<ip-tailnet-de-soberano>:11434\nAGORA_DATOS=<el NVMe>\n' > ~/.config/agora.env
chmod 600 ~/.config/agora.env
```

```bash
cp agora-api.service agora-tunnel.service ~/.config/systemd/user/
systemctl --user daemon-reload
systemctl --user enable --now agora-api.service
systemctl --user restart agora-tunnel.service
```

`agora-tunnel.service` gana `After=` y `Wants=agora-api.service`: `Wants` y no
`Requires`, para que si la API cae el túnel no se la lleve por delante.

**Cómo se apaga todo:**

```bash
systemctl --user disable --now agora-api.service agora-tunnel.service
```

---

## 2 · El artefacto versionado NO era lo que corría

`md5sum` del mismo fichero en los dos sitios:

    9305e189061864880d4c144f598d2a42   el que corre en el nodo
    a048a790437f96c9a99bef1850fc3673   el que estaba versionado en el repo

El nodo llevaba **31 líneas que el repo no tenía**: el middleware CORS y el
proxy `POST /api/generate` hacia la Ollama del Soberano, añadidos a mano el
2026-09-01 (`# --- PROXY OLLAMA Y CORS (Añadido por Soberano) ---`).

Esto importa más que la anécdota: **un diff calculado sobre la copia del repo
habría borrado el chat de la portada al aplicarse.** Por eso la baseline de
este cambio es el fichero traído del nodo, no el que había aquí.

Se recupera íntegro salvo tres cosas, y las tres se declaran:

1. `OLLAMA_HOST` deja de ser una IP de tailnet literal y pasa a `os.environ`.
   Sin la variable el proxy **no adivina**: contesta `503` con causa
   (`OLLAMA_HOST no esta puesto en el entorno`). **Ante la duda, NO_DATA.**
2. `allow_origins` pierde `http://localhost:*` y `http://127.0.0.1:*`. **CORS
   no admite comodines de puerto**: el navegador nunca casa esas dos entradas.
   Estaban sin hacer nada; arrastrarlas era fingir que cubrían algo.
3. `allow_methods=["*"]` y `allow_headers=["*"]` bajan a lo que la web usa de
   verdad: `GET, POST, OPTIONS` y `Content-Type`.

---

## 3 · Las tres rutas, y el contrato es el que la web YA habla

No se inventó formato: se leyó el cliente desplegado.

### `GET /api/v1/threads`

`board-fuentes.js` solo comprueba `Array.isArray(d.hilos)`. Se devuelve eso, más
`hilos_reales`, porque **una lista vacía y una lista que no llegó se ven igual
en la pantalla** y la frase la escribe la web (aquí no hay idioma).

> **AVISO DE EFECTO REAL, y es una decisión del Soberano, no mía:** hoy esta
> ruta da 404 y `community.html` cae a `threads.json`, sus hilos de EJEMPLO. En
> cuanto responda `200` con cero hilos, **el tablón se verá vacío**. Es lo que
> hay: `hilos_reales: 0`. La cabecera del propio `threads.json` dice que fingir
> actividad en un foro sin comunidad es la mentira más vieja de internet.

**No hay `POST`.** Escribir exige moderación, límite de ritmo y una decisión
sobre qué se hace con lo publicado. Nada de eso está firmado, y abrir un buzón
público sin saber quién lo vacía es peor que no tenerlo.

### `GET /api/v1/profiles/{huella}`

`huella` es **el pseudónimo o la clave pública entera**. Las dos, porque
`auth.js` llama «la huella completa» a la clave pública en hexadecimal y es lo
que `profile.html` enseña en su `<details>`, mientras el pseudónimo es lo que se
ve en la cabecera. Obligar a elegir una obligaría a la web a saber cuál, y tiene
las dos a mano.

**No pide firma:** es una ficha pública y todo lo que devuelve ya es público por
definición. Exigir firma para leer convertiría un perfil público en privado sin
decirlo.

`scores` sale **`null` con `scores_causa`**, nunca `0`. Un cero se lee como
«midió cero veces» cuando lo cierto es que este nodo no tiene el ledger. Son dos
cosas distintas y la diferencia es el proyecto entero.

### `POST /api/v1/profiles` — ahora también guarda ficha

`bio` y `avatar` son opcionales y **`None`, no cadena vacía**: hay que poder
distinguir «no toco la bio» de «borra la bio».

**La firma cubre el contenido cuando hay contenido.** El mensaje pasa de
`pseudonimo|clave_publica|reto` a `pseudonimo|clave_publica|reto|avatar|bio`.
Sin esto la firma probaría quién eres pero no **qué escribes**: cualquiera que
interceptase una petición válida podría cambiarle la biografía por el camino y
la firma seguiría cuadrando.

El formato condicional no abre hueco en ninguna dirección: una firma de tres
campos no vale para una petición con ficha (el servidor verifica la de cinco y
no cuadra), y una de cinco no vale si le quitan la ficha por el camino. Y
`auth.js`, que firma tres campos para crear identidad, **sigue funcionando sin
tocarlo**.

El avatar se valida por **forma** (`^[a-z0-9][a-z0-9-]{0,31}$`), no contra el
catálogo: `bustos.json` lo publica la web, y copiarlo aquí crearía dos listas
que se separan el día que se añada un busto.

La actualización devuelve **200, no 201**. Un 201 en cada guardado de biografía
diría «he creado un perfil» una vez por pulsación del botón.

### La migración de la base que ya tiene filas

`bio` y `avatar` van por `ALTER TABLE`, no en el `CREATE TABLE IF NOT EXISTS`:
sobre una tabla que ya existe, el `CREATE` **no falla — simplemente no hace
nada**, y el primer `SELECT` saldría con `no such column`. SQLite no tiene
`ADD COLUMN IF NOT EXISTS`, así que se pregunta a `PRAGMA table_info`.

Probado contra una base con el esquema viejo y una fila dentro: la fila
sobrevive, las columnas aparecen, el segundo arranque no repite el `ALTER`.

---

## 4 · Cómo se comprueba que quedó bien, en el propio nodo

```bash
curl -s http://127.0.0.1:9002/api/v1/threads | python3 -m json.tool
```

```bash
curl -s http://127.0.0.1:9002/api/v1/profiles/<un-pseudonimo-que-exista> | python3 -m json.tool
```

```bash
~/venvs/agora/bin/python test_agora.py    # debe cerrar con VERDE · 18/18
```

Y desde fuera, que es lo que importa:

```bash
curl -s -H 'Origin: https://preceptoros.org' -D - https://api.preceptoros.org/api/v1/threads
```

Tiene que traer `200`, `access-control-allow-origin: https://preceptoros.org` y
un JSON con `hilos`. Hoy trae `{"detail":"Not Found"}` — medido en el Doogee,
por internet, a las 18:18 de hoy.

---

## 5 · Lo que NO se pide aquí

- **Nada se aplicó en `la-fragua`.** Solo lecturas.
- **Ninguna clave de firma de valor** cruza a este camino.
- **No se abre escritura del tablón** ni se siembran hilos de ejemplo en la base.
- **No se toca `api-guia` (9001)**, que sigue sin unidad y sigue siendo un falso
  verde del Ojo. Va aparte.
