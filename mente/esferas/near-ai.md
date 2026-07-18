---
id: near-ai
titulo: Camino NEAR AI — crear un agente externo, aprendiendo
tipo: esfera
clase: operativo
version: 1.0.0
editor_autorizado: silicio-telemetria
metrica_exito: "el Soberano completa cada hito del camino sin bloqueo y sin acción de valor sin su firma; cada afirmación técnica citable a fuente"
umbral_reedicion: "un hito resulta inejecutable tal como está escrito, o NEAR AI cambia API/preciario/modelo de créditos"
presupuesto_kb: 8
n_medicion: 1
dominio: aprendizaje-nearai
nivel: nuevo
enlaces:
  - orquesta-modelos-p0x
  - cripto-atestacion
  - edge-ai
descripcion_niveles:
  basico: "Un camino paso a paso para que el Soberano cree un pequeño agente de IA en la nube de NEAR, sin prisa, aprendiendo cada pieza. Es externo a P0X pero P0X lo guía."
  medio: "Esfera de aprendizaje + doctrina de seguridad para desplegar un agente en NEAR AI Cloud usando la cuenta hexelion.near y créditos de inferencia, coordinado desde el dashboard bajo IronClaw."
  experto: "Ruta de capacitación para un agente perimetral serverless sobre NEAR AI: gestión de créditos vs liquidez on-chain, claves acotadas, activación por webhook, y separación estricta entre inferencia (créditos) y cualquier operación de valor (firma del carbono)."
actualizado: 2026-07-04
---

# ESFERA · CAMINO NEAR AI
### Estructurar, especificar y crear un agente externo — como trayecto de aprendizaje del Soberano
*Autor: el Preceptor (Fable 5) · El agente es EXTERNO a P0X, pero es un recurso que el Soberano puede ofrecer a la evolución de P0X. Se coordina, no se fusiona. Sin prisa pero sin pausa.*

> **Doble naturaleza.** Este documento es dos cosas a la vez: (1) una **esfera del Segundo Cerebro** — el conocimiento del Soberano sobre NEAR/agentes crece aquí y se mide como cualquier otro dominio; (2) una **doctrina de seguridad** — porque toca dinero real ($5 de crédito hoy, en la org ALCHEMIST / hexelion.near), hereda el suelo entero.

## §0 · EL SUELO APLICADO A ESTE CAMINO (leer antes de gastar un céntimo)

- **Créditos de inferencia ≠ liquidez on-chain.** Los $5 de NEAR AI Cloud son crédito de cómputo (Stripe). La cuenta `hexelion.near` es liquidez on-chain. **Jamás se mezclan en un bucle.** Gastar crédito = correr el agente; mover NEAR = firma física del Soberano.
- **Auto top-up: OFF.** Nunca se activa el recargo automático con tarjeta guardada (visto OFF en la captura — así se queda). Cada recarga es un acto consciente del carbono. Un agente que puede recargarse solo es un bucle autónomo tocando valor = prohibido.
- **Claves acotadas.** La API key de NEAR AI vive en el gestor del Soberano / `.env` del rack, jamás en el código del agente ni en un prompt. Si el agente opera on-chain algún día, usa function-call keys con allowance mínima y método restringido — nunca la full-access key.
- **Activación por webhook, no por loop.** Un agente que se despierta solo y consume crédito sin fin desangra los $5 en una noche. La activación es por evento acotado; el gasto se mide.
- **Coordinado con P0X vía la Orquesta.** Este agente entra en `ORQUESTA_MODELOS_P0X.md §1` con su fila (rol, cuándo, límites) ANTES de operar de verdad. Un cerebro sin fila no opera.

## §1 · LA RUTA DE APRENDIZAJE (niveles, se sube cuando el anterior se estabiliza)

**Nivel 0 · Terreno (entender antes de tocar).**
Qué es NEAR AI Cloud (inferencia con créditos) vs NEAR protocol (cuentas, gas, contratos). Qué es un "agente" aquí: un programa que llama modelos + puede tener herramientas. Leer la doc oficial (verificar en `docs.near.ai`; el Preceptor confirma con búsqueda cuando toque, porque cambia rápido). *Entregable: el Soberano explica en 3 frases la diferencia crédito/gas.*

**Nivel 1 · Hola-agente (gastar el primer céntimo con criterio).**
Un agente mínimo que responde una pregunta usando un modelo de NEAR AI, corriendo con la key acotada. Medir cuánto crédito consume una llamada. *Entregable: primera llamada exitosa + coste real anotado. Esto informa cuánto rinden $5.*

**Nivel 2 · Especificar el servicio (aquí entra el Preceptor de lleno).**
¿Qué ofrece el agente? El Soberano y el Preceptor definen un servicio ÚTIL y acotado, nacido de lo que ya sabe/construye (candidatos: un verificador de atestaciones del Faro consultable desde fuera; un consultor read-only del estado público del microestado; un tutor de un dominio que el Soberano domine). *Entregable: una spec de una página — qué hace, qué NO hace, qué datos toca, dónde está el límite de valor.*

**Nivel 3 · Herramientas y límites (el agente hace, sin firmar).**
Dar al agente herramientas read-only (consultar la cadena keyless, leer un endpoint público). Cero herramientas de valor. Probar que rechaza lo que no debe. *Entregable: el agente cita "no puedo firmar valor" ante una petición de transacción, igual que el Sínodo.*

**Nivel 4 · Perimetral (si y solo si el aprendizaje lo pide).**
Despliegue serverless con activación por webhook, gas abstraído por resolutores nativos SI aplica, liquidez operativa separada de créditos de inferencia. Directrices dictadas por la lógica del Soberano, no por hardware local. *Entregable: diseño revisado por el Preceptor bajo IronClaw antes de cualquier despliegue que toque valor.*

## §2 · COORDINACIÓN CON P0X (el dashboard marca el camino)

Igual que el dashboard muestra el estado del rack, mostrará el estado de este camino: qué nivel va, cuánto crédito queda, qué aprendió el Soberano. El agente externo **reporta** (read-only) a P0X; P0X **no** controla su gasto (eso es carbono). El Alquimista es su voz-espejo en el Sínodo: informa del saldo de créditos y del progreso, sin tocar nada.

## §3 · MÉTRICA DE ESTE CAMINO (aprendizaje, no dinero)

Se mide en comprensión, no en retorno: ¿el Soberano puede explicar cada pieza que despliega? ¿puede especificar un servicio sin ayuda? ¿reconoce dónde está la línea de valor? El día que el agente ofrezca algo útil Y el Soberano entienda cada capa, el camino cumplió. El dinero que entre (si entra) es consecuencia, jamás la métrica — IronClaw.

## ZONA EVOLUTIVA
> El Preceptor y el Soberano añaden aquí: coste real por llamada medido, la spec del servicio elegido, enlaces a la doc verificada, y las lecciones de cada nivel. Cada avance se destila también al dataset maestro (la orquesta aprende).

**2026-07-18 (Misión G1, Bloque D, Claude Code en soberano):** lecturas keyless verificadas contra
`hexelion.testnet` (balance 1.155 NEAR, 2 claves — una function-call-only ya en producción para
El Faro, patrón real confirmado). Propuesta de estrategia del dojo de práctica (function-call key
separada, allowance mínima, muro mainnet estructural) en `mente/esferas/ESTRATEGIA_TESTNET.md`,
a la espera de que David cree la key del dojo para la primera transacción de Nivel 1.
