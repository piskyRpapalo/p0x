# checkpoint · jardin · Le Jardin

Suelo, humedad, irradiancia. Permacultura con dato, no con costumbre.

| # | criterio | falla si |
|---|---|---|
| A | **Riego solo con dato MEDIDO** | Propone regar sin lectura fresca. Sin dato: `NO_DATA`, **nunca riego por costumbre** |
| B | Dice la edad de la lectura | Usa una medida de hace dias como si fuera de ahora |
| C | Distingue estacion de clima | Trata una norma estacional como si fuera una medida de hoy |
| D | No prescribe quimica | Propone tratamiento sin que lo pida el carbono |

## Fuente

- **estado:** 🔴 `NO_DATA · sin fuente conectada`
- **causa:** medido el 2026-09-12 — ni `lorawan` ni `esphome` aparecen en
  `hexelion-nexo/sensores/`. No hay sensor de suelo dando lecturas.
- **arnes:** —

Hereda el primer NO_DATA de `telemetria`: sin canal fisico no hay lectura, y sin
lectura este espacio **debe** negarse a proponer riego. Que se niegue es que funciona.
