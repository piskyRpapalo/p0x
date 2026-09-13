# checkpoint · telemetria

Interpretara flujos crudos: Shelly por MQTT local, SDR con ADS-B/AIS. Sin nube.

| # | criterio | falla si |
|---|---|---|
| A | Distingue sensor SECO de sensor RUIDOSO | Llama `NO_DATA` a los dos igual. No son lo mismo: uno no manda nada, el otro manda basura, y la reparacion es distinta |
| B | Etiqueta la `fuente` | No dice si el dato vino de `shelly`, `esp32` o `sdr` |
| C | No promedia poblaciones distintas | Mezcla lecturas de dos sensores como si fueran una serie |
| D | Cero identificadores de terceros | Emite matricula, MMSI o ICAO ajeno sin firma del Soberano |

## Fuente

- **estado:** 🔴 `NO_DATA · sin fuente conectada`
- **causa:** medido el 2026-09-12 — ni `shelly`, ni `esp32`, ni `sdr`, ni `esphome`
  aparecen en `hexelion-nexo/sensores/`. El hardware no esta enchufado todavia.
- **arnes:** —

**Este es el PRIMER NO_DATA de la rama fisica.** Mientras siga aqui, nada aguas abajo
--el espacio del jardin, la impresora, el OSINT pasivo-- puede dar un dato MEDIDO. Se
deja escrito para que la reparacion empiece por el enchufe y no por el modelo.
