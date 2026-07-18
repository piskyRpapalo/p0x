---
id: estrategia-testnet-dojo
titulo: "Estrategia del Dojo NEAR testnet — practicar sin tocar valor"
tipo: operativo
clase: operativo
version: 1.0.0
editor_autorizado: silicio-telemetria
dominio: aprendizaje-nearai
metrica_exito: "0 transacciones fuera de testnet; 0 claves full-access fuera de David; el Soberano puede explicar el muro mainnet en 3 frases"
umbral_reedicion: "cualquier intento (exitoso o no) de una acción de valor real dispara re-edición inmediata del muro"
presupuesto_kb: 12
n_medicion: 1
enlaces:
  - near-ai
  - orquesta-modelos-p0x
actualizado: 2026-07-18
---

# ESTRATEGIA DEL DOJO NEAR TESTNET
### Propuesta para la ZONA EVOLUTIVA de `near-ai` — practicar la mecánica sin tocar valor real
*Autor: Claude Code (soberano) · Misión G1, Bloque D · Propone; el carbono canoniza si aplica.*

---

## §0 · Lo que ya existe en producción (verificado, keyless, 2026-07-18)

```
near account view-account-summary hexelion.testnet network-config testnet now
→ balance: 1.1550053052205509 NEAR · sin contrato propio · 2 claves de acceso

near account list-keys hexelion.testnet network-config testnet now
→ ed25519:4NoWJL...GT  function-call-only, método ["anchor"], allowance 0.999 NEAR,
                        restringida a faro-anchor.hexelion.testnet
→ ed25519:7Vsqf9...7dM  full access
```

Esto **no es un diseño hipotético** — es el patrón real ya en producción para El Faro
(atestación AIS con firma ed25519, visto en `la-fragua` durante G0). El Dojo de este documento
**reutiliza exactamente ese patrón**, con una key nueva y separada para el agente-dojo, nunca la
misma que usa El Faro.

`api/alquimista/asesoria` devolvió `asesoria: null` (sin caché reciente) y `api/economy/summary`
no rastrea saldo de testnet (rastrea EUR de otro protocolo) — **sin dato comparable hoy**, no se
inventa una cifra donde no la hay.

## §1 · Function-call key para el agente-dojo (propuesta, mano de David)

Una key nueva, distinta de la de El Faro, con:
- **UN método restringido**: `log_practica` (o el nombre que David prefiera) sobre un contrato de
  práctica — **no** sobre `faro-anchor.hexelion.testnet` (eso es producción, el dojo no lo toca).
- **Allowance mínima**: sugerido 0.05 NEAR (testnet, sin valor real — pero la disciplina de poner
  un tope bajo es el hábito que se entrena, no el dinero).
- Ruta de credencial separada: `~/.near-credentials/testnet/dojo-hexelion.testnet.json` (o
  subcuenta equivalente), **jamás** en el mismo directorio/nombre que una credencial de mainnet.

### Comandos exactos (mano de David — firma incluso en testnet)

```bash
# 1) crear la subcuenta del dojo (si no existe ya una para practicar)
near account create-account fund-myself dojo.hexelion.testnet '10 NEAR' \
  autogenerate-new-keypair save-to-keychain sign-as hexelion.testnet \
  network-config testnet sign-with-keychain send

# 2) crear la function-call key restringida (allowance baja, UN método)
near account add-key dojo.hexelion.testnet grant-function-call-access \
  --allowance '0.05 NEAR' \
  --contract-account-id dojo.hexelion.testnet \
  --function-names 'log_practica' \
  autogenerate-new-keypair save-to-keychain \
  network-config testnet sign-with-keychain send
```

## §2 · El muro mainnet (guard estructural, no solo convención)

1. **Chain-id explícito en cada llamada.** Todo script del dojo lleva `network-config testnet`
   literal en el comando o `NEAR_ENV=testnet` en el entorno — nunca un default implícito que
   pueda deslizarse a mainnet si el entorno cambia.
2. **Convención `*_TESTNET_ONLY`** en cualquier variable/constante de este dojo que contenga un
   account-id o RPC endpoint (p.ej. `DOJO_CONTRACT_TESTNET_ONLY = "dojo.hexelion.testnet"`).
3. **Rutas de credenciales separadas**: `~/.near-credentials/testnet/` para el dojo, nunca
   compartir directorio ni nombre de fichero con `~/.near-credentials/mainnet/` (que ni siquiera
   debería existir en `soberano` — invariante #2 de esta misión).
4. **Cero herencia de automatismos hacia mainnet.** Ningún script, cron, ni webhook de este dojo
   se copia o generaliza a mainnet sin una PROPUESTA nueva revisada por el Preceptor bajo IronClaw
   (`instrucciones-p0x` §EL SUELO). Graduar del dojo no es un `s/testnet/mainnet/g`.
5. **El guard vive en el código, no solo en la doc**: cualquier script de este dojo que construya
   una transacción valida `network == "testnet"` antes de firmar/enviar, y aborta con error
   explícito si no lo es — el mismo espíritu que "mismatch → aborta" del Protocolo del MD Evolutivo
   §4.5.

## §3 · Criterios de graduación (mapeados a `near-ai.md` §1)

| Nivel del camino NEAR AI | Qué demuestra el dojo aquí | Entregable de graduación |
|---|---|---|
| Nivel 0 · Terreno | El Soberano ejecuta lecturas keyless (`view-account-summary`, `list-keys`) y explica balance vs allowance vs gas | Ya cumplido en este bloque — ver §0 |
| Nivel 1 · Hola-agente | Primera transacción real por el método restringido, coste medido | Pendiente — ver §4 (condicional a que David cree la key) |
| Nivel 3 · Herramientas y límites | El agente-dojo rechaza una petición fuera de `log_practica` (prueba negativa) | Diseño listo; ejecución es misión futura |
| Nivel 4 · Perimetral | Cualquier despliegue webhook/serverless — **fuera de alcance de G1** | No se toca aquí |

## §4 · Si David crea la key durante la misión (condicional, PARA ahí)

Con la key del §1 ya creada, la transacción de prueba sería:

```bash
near contract call-function as-transaction dojo.hexelion.testnet log_practica \
  json-args '{"nota":"primera practica del dojo, Mision G1"}' \
  prepaid-gas '30 TGas' attached-deposit '0 NEAR' \
  sign-as dojo.hexelion.testnet network-config testnet sign-with-keychain send
```

Medir: gas consumido real (`TGas` reportado por el recibo), latencia (submit→finalidad), y
confirmar coste real = 0 (testnet). **Una sola transacción, después PARA** — no se encadenan más
sin nueva misión.

En esta sesión: **no se creó ninguna key nueva** (acto exclusivo de David). Esta sección queda
lista para ejecutar en cuanto exista.

## ZONA EVOLUTIVA (de este documento)
> Editable por el silicio con telemetría: coste real medido cuando exista la primera transacción,
> ajustes al método restringido si David decide otro nombre/contrato.

*(vacía — v1.0.0 es la línea base, escrita antes de la primera transacción real)*
