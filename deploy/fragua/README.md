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

## Lo que NO hace

**No verifica firmas Ed25519.** Guarda la clave pública y la trata como
identificador. Verificar exigiría una dependencia de criptografía que no está
en este venv, y meterla a escondidas sería peor que el hueco.

Consecuencia, y va también en cada respuesta: cualquiera puede crear un perfil
con la clave pública de otro. Sirve para vincular un aparato propio, no para
autenticar frente a terceros.

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
