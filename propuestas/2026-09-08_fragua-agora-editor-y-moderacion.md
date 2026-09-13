# Propuesta · `agora_api` (la-fragua): la cuenta de editor y el buzón moderado

**Nodo destino:** `la-fragua` (usuario `ubuntu`) · **Origen:** `soberano`
**Fecha:** 2026-09-08 · **Estado:** PROPUESTA — no aplicada.
`la-fragua` es propose-only desde `soberano`: esto se pega allí, no se empuja
desde aquí.

## Por qué existe, y quién lo pidió

Lo pidió el servidor con sus propias palabras. Hoy, medido:

    GET https://api.preceptoros.org/api/v1/threads
    {"estado":"OK","hilos_reales":0,
     "escritura":"cerrada: el Agora todavia no modera","hilos":[]}

La propuesta del 2026-09-02 cerró el `POST` a propósito: *«escribir exige
moderación, límite de ritmo y una decisión sobre qué se hace con lo publicado.
Nada de eso está firmado, y abrir un buzón público sin saber quién lo vacía es
peor que no tenerlo»*. **Esas tres cosas son lo que esta propuesta trae**, y la
decisión que faltaba la firmó el Soberano el 2026-09-08:

- El editor es **moderador del Ágora**, no editor del contenido del sitio.
- **Varias claves públicas = un mismo editor.** El PC y el teléfono se dan de
  alta como dos claves del mismo nombre. No hay recuperación; hay altas.

## Lo medido en la API viva (2026-09-08, desde `soberano`)

No se parte del papel: se parte de lo que responde hoy.

| Ruta | Hoy | Nota |
|---|---|---|
| `GET /api/v1/reto` | **200** | `{reto, vive_s:300, firma_sobre:"pseudonimo\|clave_publica\|reto"}`, aleatorio por llamada |
| `GET /api/v1/threads` | **200** | `hilos_reales:0`, escritura cerrada |
| `POST /api/v1/threads` | **405** | el buzón no existe, no es que esté cerrado con llave |
| `GET /api/v1/profiles/{huella}` | **404** | `{"detail":{"estado":"NO_DATA","causa":"no hay perfil con esa pseudonimo"}}` |
| `POST /api/v1/profiles` | existe | 405 al hacerle GET |
| CORS | correcto | `allow-origin: https://preceptoros.org` |
| `/openapi.json`, `/docs` | 404 | siguen cerrados, como debe ser |

**El camino de firma ya está entero y funcionando.** No hay que inventarlo:
`/api/v1/reto` da el reto, y `POST /api/v1/profiles` ya verifica Ed25519 sobre
`pseudonimo|clave_publica|reto`. Esta propuesta **reusa ese mecanismo** en vez
de traer un segundo dialecto de autenticación.

## 1 · Dónde vive la lista de editores, y por qué NO en la base

**Fichero en disco, leído al arrancar. Nunca una tabla de la misma base que
recibe escrituras públicas.**

    /home/ubuntu/agora/editores.json   # guardia:permitir ruta del nodo destino; en propose-only el canon EXIGE absoluta con su usuario

    {
      "editores": [
        {"nombre": "soberano",
         "claves": ["<64 hex de la publica del PC>",
                    "<64 hex de la publica del telefono>"],
         "alta": "2026-09-08",
         "nota": "dos aparatos, un editor. La clave privada no es extraible."}
      ]
    }

El motivo no es de gusto: si la lista viviera en la misma SQLite donde caen los
mensajes del público, **cualquier fallo de escritura sería una escalada de
privilegios**. Separarla en un fichero que sólo toca quien tiene la consola
hace que dar de alta un editor sea un acto deliberado —editar y reiniciar—, no
una petición HTTP. Es la misma disciplina que el canon exige para las unidades
systemd: *nada con autoridad entra sin firma explícita*.

**Ruta absoluta y con el usuario dentro** porque este artefacto se ejecuta en
`la-fragua`, donde `~` no es el home de aqui. <!-- guardia:permitir la propuesta explica justo por que no se usa ~ hacia otro nodo -->

Si el fichero no existe o no se puede leer: el servicio **no adivina**. Arranca
con cero editores, la moderación queda cerrada y lo dice con causa. Ante la
duda, NO_DATA.

## 2 · El contrato de la moderación

### `GET /api/v1/reto` — sin cambios

Ya sirve. Se reusa tal cual. El campo `firma_sobre` es el que manda, y por eso
las rutas nuevas devuelven **el suyo** (ver abajo): un cliente que lee
`firma_sobre` no tiene que saberse el formato de memoria.

### `POST /api/v1/threads` — el buzón, que nace en cuarentena

    {"titulo": "...", "cuerpo": "...", "clave_publica": "<64 hex>",
     "reto": "<el de /reto>", "firma": "ed25519:<128 hex>"}

`firma_sobre`: **`titulo|cuerpo|clave_publica|reto`**.

Cubre el contenido, no sólo la identidad, por la misma razón que se escribió en
el contrato de perfiles el 2026-09-02: sin el cuerpo dentro de la firma,
cualquiera que intercepte una petición válida puede cambiar el texto por el
camino y la firma sigue cuadrando.

**Todo hilo entra en estado `pendiente`.** No se publica nada por llegar. Un
`201` con `{"estado":"OK","situacion":"pendiente"}` — y la web tiene que
decirlo, porque un mensaje que se envía y no aparece se lee como una avería.

### `GET /api/v1/threads` — sólo lo publicado

Sigue devolviendo `hilos_reales` y `hilos`, y **sólo los `publicado`**. Añade:

    "escritura": "abierta: los hilos nuevos esperan moderacion"

La frase la lee la web, que es quien tiene idioma. Aquí no se traduce nada.

### `POST /api/v1/threads/{id}/moderar` — la ruta que sólo el editor puede

    {"accion": "publicar" | "rechazar", "clave_publica": "<64 hex>",
     "reto": "<el de /reto>", "firma": "ed25519:<128 hex>"}

`firma_sobre`: **`accion|id|clave_publica|reto`**.

El servidor comprueba **dos cosas y en este orden**: que la firma cuadra, y que
esa pública está en `editores.json`. Si la firma es válida pero la clave no
está en la lista: **403 con causa**, nunca 404. Fingir que la ruta no existe
ante alguien que ya ha probado quién es no protege nada y le miente.

### `GET /api/v1/threads/pendientes` — la bandeja

Misma verificación de editor, sobre `firma_sobre`:
**`pendientes|clave_publica|reto`**. Un `GET` con firma es raro y por eso se
dice: la firma viaja en cabeceras (`X-Clave-Publica`, `X-Reto`, `X-Firma`) para
no meter cuerpo en un GET. Si eso incomoda, hágase `POST` — pero decídase una
vez y escríbase aquí.

## 3 · El límite de ritmo, que es parte del trato

Sin él, la cuarentena no protege: la cola sería el nuevo blanco.

- **Por clave pública:** 5 hilos por hora, 20 al día.
- **Por IP:** 20 hilos por hora — porque crear claves es gratis y la clave sola
  no limita nada.
- Al pasarse: **429 con causa y `reintentar_en_s`**. Un 429 mudo hace que el
  cliente reintente en bucle.

Los contadores viven en memoria del proceso y **se pierden al reiniciar**. Se
dice porque es una debilidad real y conocida, no un descuido: un atacante que
provoque reinicios recupera su cuota. Endurecerlo es trabajo aparte y no
bloquea esto.

## 4 · La base: migración aditiva, con la trampa ya conocida

Los hilos necesitan `situacion`, `creado`, `clave_publica` y `moderado_por`.
Sobre una tabla que ya existe, **`CREATE TABLE IF NOT EXISTS` no falla: no hace
nada**, y el primer `SELECT` sale con `no such column`. SQLite no tiene
`ADD COLUMN IF NOT EXISTS`, así que se pregunta a `PRAGMA table_info` y se
añade lo que falte. Es exactamente la trampa que ya se documentó el 2026-09-02
para `bio` y `avatar`; se repite aquí porque se vuelve a pisar.

`situacion` entra con **`DEFAULT 'pendiente'`**. Si hubiera filas previas,
quedan invisibles hasta que un editor las mire — que es el lado seguro del
error.

## 5 · Lo que hay que MEDIR en `la-fragua` antes de aplicar

No se puede comprobar desde `soberano`, y ninguna es opcional:

1. **Que `cryptography` esté instalada** y verifique Ed25519 en ese Python:

       /usr/bin/python3 -c "from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey; print('OK')"

   Si no está, `PyNaCl` sirve igual. **Lo que no vale es escribir la
   verificación a mano.**
2. **Dónde vive hoy `agora_api.py`** y con qué unidad arranca, para saber qué
   se reinicia y con qué usuario corre.
3. **Si `POST /api/v1/profiles` ya tiene verificador de firma** — casi seguro
   que sí, porque funciona. Entonces **se reusa esa función**, no se escribe
   una segunda. Dos verificadores que se separan es cómo se cuela un agujero.

## 6 · Cómo se comprueba que quedó bien

Desde `la-fragua`, contra el puerto local, antes de tocar el túnel:

    R=$(curl -s http://127.0.0.1:9002/api/v1/reto | python3 -c 'import sys,json;print(json.load(sys.stdin)["reto"])')
    curl -s -X POST http://127.0.0.1:9002/api/v1/threads \
      -H 'Content-Type: application/json' \
      -d "{\"titulo\":\"prueba\",\"cuerpo\":\"prueba\",\"clave_publica\":\"<hex>\",\"reto\":\"$R\",\"firma\":\"ed25519:<hex>\"}"

Y las cinco que tienen que dar rojo, porque un verde que no sabe fallar no vale:

1. Firma válida, clave **no** en `editores.json`, sobre `/moderar` → **403 con
   causa**, no 404.
2. Reto **caducado** (>300 s) → rechazo con causa.
3. Reto **reusado** dos veces → el segundo rechazado. Si no, la firma
   interceptada se puede repetir.
4. Cuerpo cambiado tras firmar → firma no cuadra.
5. Sexto hilo en una hora con la misma clave → **429 con `reintentar_en_s`**.

Desde `soberano`, sólo después:

    curl -s https://api.preceptoros.org/api/v1/threads | python3 -m json.tool
    curl -s -o /dev/null -D - -H 'Origin: https://preceptoros.org' \
      https://api.preceptoros.org/api/v1/threads | grep -i access-control

## 7 · Lo que esta propuesta NO hace, y se dice

- **No toca la web.** El cliente que firme y la bandeja de moderación son
  trabajo aparte, en `preceptoros-web`. Hoy `auth.js` firma pero **no llama a
  la API**: medido, ningún guion de `assets/` usa `/api/v1/reto`.
- **No crea ninguna unidad systemd nueva.** Si hiciera falta, es **firma
  aparte, una por una**, con su línea en el cuaderno del nodo destino.
- **Ninguna clave de firma de valor** entra en este camino. La identidad del
  editor es Ed25519 de autenticación, no de atestación. Si algún día firmara
  valor, eso es otra decisión y otro documento.
- **No siembra hilos de ejemplo.** El tablón se verá vacío hasta que alguien
  escriba y el editor publique. Fingir actividad en un foro sin comunidad es la
  mentira más vieja de internet, y ya está escrito en la cabecera de
  `threads.json`.

## 8 · El orden en que conviene hacerlo

1. Medir las tres cosas de §5. Si `cryptography` no está, para y repórtalo.
2. `editores.json` con **una sola clave** —la del PC— y comprobar que el 403
   funciona antes de dar de alta la segunda.
3. La migración de §4 contra una copia de la base, no contra la buena.
4. El buzón en cuarentena (§2) sin la ruta de moderar: hasta aquí no hay nada
   público que pueda salir mal.
5. La moderación y la bandeja.
6. El límite de ritmo (§3), y las cinco pruebas rojas de §6.
7. Sólo entonces, el alta de la segunda clave.
