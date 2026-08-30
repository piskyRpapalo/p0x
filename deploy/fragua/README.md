# deploy/fragua · El Ágora `/api/v1`

Artefacto de despliegue para **la-fragua**. Se aplica bajo la misión acotada
firmada por el Soberano; nada más de este nodo se toca sin palabra nueva.

## Qué es

Tres endpoints y su salud:

    GET  /api/v1/salud
    POST /api/v1/profiles        {pseudonimo, clave_publica}
    GET  /api/v1/agents
    POST /api/v1/agents/select   {pseudonimo, agente}

Base SQLite en modo WAL sobre el NVMe de la-fragua (`AGORA_DATOS`, por
defecto `/mnt/nvme/agora_db`). <!-- guardia:permitir ruta del nodo de destino,
parte del contrato de este artefacto de despliegue -->
Escucha en **loopback**.

## Cómo se prueba quién eres

Con un **reto de un solo uso**:

    GET  /api/v1/reto            -> {reto, vive_s, firma_sobre}
    firma = Ed25519( "pseudonimo|clave_publica|reto" )
    POST /api/v1/profiles        {pseudonimo, clave_publica, reto, firma}
    POST /api/v1/agents/select   {pseudonimo, agente, reto, firma}

Los tres campos van dentro del mensaje firmado a propósito: firmar solo el reto
dejaría reusar esa firma para otro pseudónimo, y firmar solo el pseudónimo la
dejaría valer para siempre.

El nonce **caduca a los 300 s y se quema al usarse**, incluso si el intento
falla. Sin esas dos cosas, una firma capturada una vez vale para siempre y el
reto no es un reto: es una contraseña larga viajando en claro.

`select` verifica contra la clave que **ya está guardada**, no contra una que
venga en la petición: si no, elegir compañero por otro sería mandar su
pseudónimo con la clave propia.

**Dependencia declarada:** `pynacl`. La promesa de «stdlib only» rige la Bóveda
—el producto que se instala la gente—, no el Ágora, que corre en el rack del
Soberano. Escribir Ed25519 a mano sería mucho peor que declararla.

## Pruebas

    ~/venvs/agora/bin/python test_agora.py

Siete casos contra la API viva, y firman de verdad: una prueba que simulara la
firma estaría comprobando el simulador. Cubren el camino honrado, el reto
reusado, la firma corrupta, la clave de otro y elegir en nombre ajeno.

## Arrancar y parar

```bash
~/venvs/agora/bin/uvicorn agora_api:app --host 127.0.0.1 --port 9002
```

No hay unidad systemd: crear una exige firma por unidad (canon DUNI) y se pide
aparte.

## El catálogo

`agentes.json` declara 8 compañeros y **cuál existe de verdad**. Hoy: 1
disponible (el Instalador), 7 con `disponible: false` y su causa. Un catálogo
que ofrece ocho cuando hay dos es un escaparate con cajas vacías.

Nota de nombres: el encargo llamaba «Curador» a uno, y eso ya es el nombre de
un bucle del enjambre. Aquí es **El Bibliotecario**, con la colisión anotada en
el propio JSON.

## El túnel

`config.yml` → `~/.cloudflared/config.yml` · unidad de usuario
`agora-tunnel.service` → `~/.config/systemd/user/`.

**Qué hace:** publica `http://127.0.0.1:9002` como `https://api.preceptoros.org`.
El origen sigue en loopback; nada abre un puerto al exterior.

**Qué toca:** el túnel `agora`
(`bbe3c9be-06b9-4fb6-b368-2cebe65f1dbe`), su fichero de credenciales en
`~/.cloudflared/`, y un registro DNS en `preceptoros.org`.

**Cómo se apaga:**

```bash
systemctl --user stop agora-tunnel.service
systemctl --user disable agora-tunnel.service
```

El `--config` va **explícito** en el `ExecStart`: sin él, `cloudflared` busca en
varios sitios por orden, y el día que aparezca otro fichero en uno de ellos el
túnel arrancaría con una configuración que nadie eligió.

La regla `catch-all` (`http_status:404`) del ingress no es relleno: decide qué
pasa con cualquier host que apunte aquí por error. Sin ella, un hostname mal
configurado serviría esta API.

**Verificado desde fuera:** Beelink y Doogee, por internet y sin `adb reverse`,
reciben `1/8 disponibles`.
