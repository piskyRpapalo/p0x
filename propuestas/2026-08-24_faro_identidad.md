# PROPUESTA · corregir la identidad declarada del Faro

**Nodo destino:** `la-fragua` · **Origen:** sesión de frontera en `soberano`
**Fecha:** 2026-08-24 · **Estado:** PROPUESTA, no aplicada · **Aplica:** el Soberano

> Propose-only. `soberano` no toca la-fragua. Esta sesión solo hizo dos `GET` de lectura.

---

## 1 · Qué está mal, medido

```bash
curl -s http://la-fragua:8100/.well-known/hexelion-attestation.json  # guardia:permitir propuesta propose-only cuyo destino es ese nodo
curl -s http://la-fragua:8100/health  # guardia:permitir propuesta propose-only cuyo destino es ese nodo
```

Devuelto el 2026-08-23 a las 22:19 UTC:

| Endpoint | Campo | Valor |
|---|---|---|
| `/.well-known/hexelion-attestation.json` | `node` | **`hexelion.near`** |
| `/health` | `network` | `testnet` |
| `/health` | `node` | **`hexelion-beato-01`** |

## 2 · Son dos incoherencias, no una

`docs/faro/ESTADO_FINAL.md` declara una deuda menor: *«el `.well-known` declara node:
hexelion.near (mainnet) pero opera en testnet»*, con fix propuesto *«sed sobre el campo node
+ restart»*.

**El diagnóstico se queda corto.** El nombre no solo pertenece a la red equivocada:

1. **Red equivocada** — `hexelion.near` es una cuenta de *mainnet*; el servicio corre en
   testnet (agung, chain_id 9990), en DRY_RUN.
2. **Nodo distinto** — el propio servicio se identifica como `hexelion-beato-01` en
   `/health`. `hexelion.near` no es otro nombre del mismo nodo: es otra identidad.

Un `sed` sobre un solo campo dejaría la mitad del error puesto, y peor: dejaría un manifiesto
*internamente coherente* declarando una identidad de mainnet que no es la del servicio. Hoy
al menos la contradicción es visible.

**Por qué importa más que una errata:** el `.well-known` es lo que un verificador externo lee
para decidir con qué clave comprobar una atestación. Declarar una cuenta de mainnet en un
servicio de testnet invita a que alguien confíe en una identidad que este servicio no
controla. Roza «jamás firmas valor» por el lado de la identidad, no por el de la clave.

## 3 · Qué propongo

**Que el manifiesto declare lo que el servicio es**, y que la ambigüedad se elimine en vez de
resolverse a favor de una de las dos:

```json
{
  "kid": "hxl-attest-1",
  "alg": "ed25519",
  "pubkey": "E94vbxCiKvEP56GZdd1Hx4C8AYzVtbkRxV33Y/1LYcw=",
  "node": "hexelion-beato-01",
  "network": "testnet",
  "format": "v1",
  "domain": "hexelion-faro-attestation-v1",
  "note": "attestation of reception; not proof of physical reality"
}
```

Dos cambios: `node` pasa a la identidad real, y **se añade `network`** — hoy el manifiesto no
dice en qué red opera, que es justo el dato que faltaba para que la contradicción fuera
detectable desde fuera.

`pubkey`, `kid`, `domain` y `note` **no se tocan**: cambiar el dominio de firma invalidaría
las atestaciones ya emitidas.

## 4 · Lo que NO sé, y por eso no traigo un `sed` cerrado

**No he entrado en la-fragua.** No sé si `/.well-known/…` se sirve desde un fichero estático
o se genera en el código del servicio. El `sed` de `ESTADO_FINAL.md` supone lo primero; si es
lo segundo, ese `sed` no encuentra nada y el fix parecerá aplicado sin estarlo.

Primer paso, en la-fragua:

```bash
cd ~/hexelion/faro && grep -rn "hexelion.near\|well-known\|hexelion-attestation" --include='*.py' --include='*.json' .
```

Según lo que salga:

- **Fichero estático** → editar el JSON, `systemctl --user restart hexelion-faro` (o el ámbito
  que corresponda).
- **Generado en código** → cambiar la constante y reiniciar. Si el valor viene de una variable
  de entorno o del `.service`, ahí.

## 5 · Verificación después de aplicar

```bash
curl -s http://la-fragua:8100/.well-known/hexelion-attestation.json | grep -o '"node":"[^"]*"'  # guardia:permitir propuesta propose-only cuyo destino es ese nodo
curl -s http://la-fragua:8100/health  # guardia:permitir propuesta propose-only cuyo destino es ese nodo
curl -s http://la-fragua:8100/selftest  # guardia:permitir propuesta propose-only cuyo destino es ese nodo
```

Los tres deben coincidir en `hexelion-beato-01` y `testnet`. Y `/selftest` debe seguir en
verde: si el manifiesto entra en el material firmado, cambiarlo podría romper la
verificación — **si `/selftest` cae, se revierte y se dice**, no se sigue adelante.

## 6 · Coste y riesgo

- **Coste:** S. Un campo cambiado, uno añadido, un reinicio.
- **Riesgo:** bajo, con una salvedad: si el `node` participa en el material firmado, las
  atestaciones nuevas dejan de casar con las viejas. Por eso la verificación incluye
  `/selftest` y por eso no se toca `domain`.
- **Ventana:** el servicio lleva 4+ días sin interrupción y no tiene mantenedor declarado. Un
  reinicio corta ese uptime — decisión del Soberano si compensa.

## 7 · Alternativa honesta si no compensa tocarlo

Dejarlo como está y **anotar la incoherencia en el propio `note`** del manifiesto, para que
quien lo lea no confíe en el campo `node`. Es peor que arreglarlo, pero es mejor que un
manifiesto que miente en silencio — y no exige reiniciar nada.
