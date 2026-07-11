# HEXELION — PROTOCOLO DE PRIMERA LUZ
## Guía del Primer Mes con Capital Real
### Documento Vivo — Se completa con datos reales al acercarse el Mes 7
*"El Alquimista llega al primer mes real con 6 meses de simulación. No empieza ciego."*

---

## PREREQUISITOS ANTES DE EJECUTAR ESTE PROTOCOLO

```
□ Ciclo Dorado superado y certificado
□ Hash-Lock ejecutado sobre todos los binarios
□ Fingerprint de identidad de Hexelion AI hasheado y almacenado
□ Alquimista con 6 meses de simulación en Testnet completada
□ Informe de simulación presentado al Soberano y validado
□ Bóveda Genoma actualizada con el estado post-Ciclo Dorado
□ Pisky Wallet con fondos suficientes para la primera inyección
```

---

## SEMANA 1 — €10 → stNEAR (Días 1-7)

### Objetivo de la semana
**Validar el pipeline técnico real.** No aprender nada nuevo. No experimentar.
El Alquimista replica exactamente su operación más exitosa y segura de la simulación.

### Protocolo de ejecución

**Día 1 — La inyección:**
```
1. El Soberano transfiere €10 desde la Pisky Wallet al Capital de Trabajo
   Esta es una decisión de Nivel 3 — se confirma en la Pantalla Soberana

2. El Alquimista convierte €10 a NEAR en el DEX con menor slippage
   (precio spot del día, consultado por el Oracle de Precios)
   Slippage máximo aceptado: 2%
   Si slippage > 2%: esperar hasta que las condiciones mejoren

3. El Alquimista hace stake de todo el NEAR en stNEAR via Meta Pool
   URL: metapool.app
   El Berserker ejecuta vía Sésamo Efímero (JIT 300s)
   El Alquimista verifica la transacción on-chain antes de confirmar

4. Registro inmutable en hexelion_financiero:
   {
     tipo: "primera_luz_semana_1",
     fecha: [timestamp],
     capital_inyectado_eur: 10.00,
     capital_inyectado_near: X.XXX,
     precio_near_eur: X.XX,
     slippage_real: X.XX%,
     protocolo: "stNEAR_Meta_Pool",
     txhash: "[hash de la transacción]",
     simulacion: false
   }
```

**Días 2-7 — Observación:**
```
→ No tocar las posiciones
→ El Alquimista monitoriza el APY real vs. el APY simulado
→ El Vocero verifica el precio de NEAR vs. la proyección de la simulación
→ El Monje verifica que el capital no ha disminuido por causas técnicas
```

**KPI de la semana:**
```
□ ¿El pipeline técnico funcionó correctamente? (firmas, gas, timing)
□ ¿El slippage real fue coherente con el simulado?
□ ¿El APY de stNEAR coincide con el proyectado en la simulación?
□ ¿Hubo algún comportamiento inesperado del Alquimista?
```

**Si el KPI falla:**
```
→ No pasar a semana 2 hasta resolver el problema
→ El Soberano revisa los logs con el Alquimista
→ Se documenta el fallo en hexelion_aprendizaje
→ Se corrige el protocolo antes de continuar
```

---

## SEMANA 2 — +€10 (si Semana 1 sin incidentes, Días 8-14)

### Objetivo de la semana
**Explorar el primer pool de liquidez estable.** Solo stablecoins — sin impermanent loss.

### Protocolo de ejecución

**Día 8 — Evaluación de semana 1:**
```
El Alquimista genera un resumen de la semana 1:
  - Rentabilidad real vs. simulada
  - Diferencias detectadas
  - Propuesta para semana 2

El Soberano revisa el resumen en la Pantalla [Sim]
Si aprueba → proceder a la inyección de semana 2
```

**Día 8 — Segunda inyección:**
```
El Soberano transfiere €10 adicionales (Nivel 3)
Capital total en el organismo: €20
```

**Días 8-9 — Selección del pool:**
```
El Alquimista evalúa en Modo Profundo los pools estables disponibles en Ref Finance:
  Criterios de selección (en orden de prioridad):
  1. TVL > $500k (inamovible)
  2. Ambas monedas estables (USDC/USDT o similar — sin impermanent loss)
  3. APY > 3% anualizado
  4. Comisiones < 0.3% por operación
  5. Antigüedad del pool > 30 días

El Alquimista presenta la propuesta al Soberano:
  {
    pool_seleccionado: "USDC/USDT — Ref Finance",
    tvl_actual: $X,
    apy_proyectado: X.X%,
    comision_entrada: X.XX%,
    riesgo_impermanent_loss: "ninguno (ambas estables)",
    justificacion: "[razonamiento del Alquimista]"
  }
```

**Aprobación del Soberano (Nivel 3):**
```
→ El Soberano revisa la propuesta en la Pantalla [A]probar
→ Si aprueba: el Berserker ejecuta la entrada al pool
→ Si rechaza: el Alquimista propone alternativa
```

**KPI de la semana:**
```
□ ¿El Alquimista seleccionó un pool con TVL > $500k?
□ ¿El pool es efectivamente de stablecoins (sin IL risk)?
□ ¿El APY real coincide con el proyectado?
□ ¿El Soberano entendió y aprobó la propuesta sin ambigüedad?
```

---

## SEMANA 3 — +€10 (si Semana 2 sin incidentes, Días 15-21)

### Objetivo de la semana
**Capital completo €30. Mandato conservador pleno.**

### Protocolo de ejecución

**Día 15 — Evaluación de semana 2:**
```
El Alquimista genera resumen comparativo:
  - Semana 1 (stNEAR): APY real X.X% vs. simulado X.X%
  - Semana 2 (pool estable): APY real X.X% vs. simulado X.X%
  - Diferencias y causas explicadas

El Soberano aprueba la inyección final de €10
Capital total: €30 — el organismo opera con capital completo
```

**Días 15-21 — Distribución del capital completo:**
```
El Alquimista propone la distribución del capital completo
en Modo Profundo, basándose en el rendimiento de las semanas 1-2:

Distribución ejemplo (el Alquimista decide basándose en datos reales):
  60% → stNEAR (base estable, liquidez alta)
  40% → pool de stablecoins (mayor APY, liquidez media)

O en función de lo aprendido:
  Si stNEAR rindió mejor → 80%/20%
  Si el pool rindió mejor → 40%/60%

La distribución final es propuesta del Alquimista, aprobada por el Soberano.
```

**Autonomía Nivel 2 activa:**
```
A partir de semana 3, el Alquimista opera con plena autonomía de Nivel 2:
  → Rebalanceos dentro del mandato conservador (2-4% mensual): NO necesitan aprobación
  → El Soberano es NOTIFICADO, no consultado, para operaciones < 10% del capital
  → Operaciones > 10% del capital: siempre Nivel 3
  → Cambio de protocolo (salir de stNEAR, entrar en LP volátil): siempre Nivel 3
```

**KPI de la semana:**
```
□ ¿La distribución del capital total es coherente con los datos de semanas 1-2?
□ ¿El Alquimista opera dentro del mandato conservador (2-4% mensual)?
□ ¿Los fees totales de la semana son < 0.5% del capital?
□ ¿El capital total (€30) está completo y sin pérdidas no justificadas?
```

---

## SEMANA 4 — INFORME AL SOBERANO (Días 22-30)

### El Gran Informe: Simulación vs. Realidad

**El Alquimista genera el informe comparativo definitivo:**

```
INFORME DE PRIMERA LUZ — MES 7
═══════════════════════════════

CAPITAL INICIAL:          €30.00
CAPITAL ACTUAL:           €XX.XX
RENTABILIDAD REAL:        +X.XX%
OBJETIVO CONSERVADOR:     2-4%

COMPARATIVA CON SIMULACIÓN (6 meses):
  Semana 1 (stNEAR):
    APY simulado:   X.XX%  APY real:   X.XX%  Diferencia: X.XX%
  Semana 2 (pool estable):
    APY simulado:   X.XX%  APY real:   X.XX%  Diferencia: X.XX%
  Semana 3 (capital completo):
    APY simulado:   X.XX%  APY real:   X.XX%  Diferencia: X.XX%

FEES TOTALES DEL MES:     €X.XX (X.XX% del capital)
NÚMERO DE OPERACIONES:    X (máximo permitido: 3-4)
SLIPPAGE PROMEDIO:        X.XX%

DIFERENCIAS CON LA SIMULACIÓN:
  [descripción de qué fue diferente y por qué]

LECCIONES APRENDIDAS:
  1. [lección 1]
  2. [lección 2]
  3. [lección n]

PROPUESTA PARA MES 2:
  □ Continuar con mandato conservador (si rentabilidad dentro del objetivo)
  □ Ajustar distribución de capital
  □ Solicitar activación de Modo Agresivo (si el Soberano lo aprueba)
  □ Otra propuesta: [descripción]

ESTADO DEL CIRCUIT BREAKER:
  Capital actual (€XX.XX) vs. umbral stop-loss (€25.50 = -15%)
  Estado: ● SAFE / ⚠️ ATENCIÓN / 🔴 ACTIVADO
```

### Decisión del Soberano para Mes 2

```
El Soberano revisa el informe y toma una de estas decisiones:

OPCIÓN A — Continuar conservador:
  El mandato conservador (2-4%) continúa.
  Nueva inyección de €30 el día 1 del mes 2.

OPCIÓN B — Ajustar distribución:
  El Alquimista recibe instrucciones específicas.
  Nueva inyección de €30 el día 1 del mes 2.

OPCIÓN C — Activar Modo Agresivo (Nivel 3):
  El Soberano aprueba la activación del Modo Agresivo (8-15% objetivo).
  Condición: SOC > 90% + excedente solar confirmado.
  Nueva inyección de €30 el día 1 del mes 2.

OPCIÓN D — Pausa (si hay incidentes no resueltos):
  No se inyecta capital en mes 2.
  El Alquimista opera solo con el capital del mes 1 hasta resolver.
  Se documenta la causa en hexelion_financiero.

La decisión se registra como inmutable en hexelion_financiero.
```

---

## REGLAS PERMANENTES (válidas para todos los meses)

```
REGLA 1 — FEES:
  Fee máximo por operación: < 0.5% del Capital de Trabajo = < €0.15
  Si una operación requiere > €0.15 en fees: esperar condiciones mejores

REGLA 2 — POOLS:
  TVL mínimo: $500k inamovible
  Para pools volátiles (Modo Agresivo): TVL mínimo $1M

REGLA 3 — SLIPPAGE:
  Modo Conservador: slippage < 2%
  Modo Agresivo: slippage < 5% (solo si APY recupera en < 30 días)

REGLA 4 — STOP-LOSS:
  Capital cae a €25.50 (−15%) → Circuit Breaker automático
  El Soberano debe autorizar explícitamente la reanudación

REGLA 5 — PISKY WALLET:
  100% de los beneficios → Pisky Wallet
  Solo el capital original (€30) permanece como Capital de Trabajo
  salvo decisión soberana explícita de reinversión

REGLA 6 — NEAR PROTOCOL:
  Máximo 80% del capital en posiciones activas
  Mínimo 20% en liquidez inmediata (stNEAR o NEAR sin lockup)
  El 20% de reserva nunca se toca salvo Excepción Lázaro
```

---

## SEGUIMIENTO MENSUAL

*(Esta sección se completa mes a mes con los resultados reales)*

| Mes | Capital inicio | Capital fin | Rentabilidad | Fees | Operaciones | Decisión siguiente mes |
|-----|---------------|-------------|--------------|------|-------------|----------------------|
| 7   | €30.00 | [pendiente] | [pendiente] | [pendiente] | [pendiente] | [pendiente] |
| 8   | — | — | — | — | — | — |
| 9   | — | — | — | — | — | — |
| 10  | — | — | — | — | — | — |
| 11  | — | — | — | — | — | — |
| 12  | — | — | — | — | — | — |

---

*Documento: HEXELION_PRIMERA_LUZ.md*
*Versión: 1.0 — Documento vivo, se completa con datos reales*
*Activación: Mes 7 post Ciclo Dorado*
*Prerequisito: Informe de 6 meses de simulación validado por el Soberano*
