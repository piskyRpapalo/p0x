---
id: tecnica-patron-era-energetica
titulo: "Patrón Era Energética — el envoltorio @sleeping de la Pista A"
tipo: tecnica
clase: operativo
nivel: vivo
enlaces:
  - proyecto-reflejos
  - reflejo-bateria
  - energia-solar
metrica_exito: "todo reflejo energético declara en qué Era vive; 0 código de la Era ausente ejecutándose en silencio; cada invocación dormida queda logueada"
umbral_reedicion: "llegada de la batería solar (P0X_BATTERY_PRESENT=true) o un reflejo nuevo que no encaje en dos Eras"
actualizado: 2026-07-11
descripcion_niveles:
  basico: "El sistema hoy no tiene batería solar. Este patrón deja escrito el código para 'cuando la haya', dormido pero visible, y una sola llave lo despierta — sin reescribir nada."
  medio: "Rescate del spec BATTERY_FLAG (may-2026): una variable de entorno (P0X_BATTERY_PRESENT) conmuta la Era energética (SOL_SINCRONO ↔ PLENA). Los decoradores @sleeping y @sun_synchronous marcan qué funciones viven en cada Era; lo dormido se loguea, jamás corre en silencio. Los reflejos de la Pista A lo usan para declarar sus supuestos energéticos."
  experto: "deploy/fragua/energia_era.py: flag env → ENERGY_ERA + decoradores con logging de invocación dormida (observable, honest-sensors). Lo rescatado es SOLO el envoltorio arquitectónico; las tácticas de valor que el spec original envolvía (MCT-MAX, arbitraje de red negativa, modos de ingreso) están enterradas en la Necrópolis (mito-fundacional-organismo-20260711) por IronClaw: los reflejos son deterministas y solo protectores. reflejo-bateria es @sun_synchronous de facto (protege la UPS porque no hay batería solar); al llegar la batería, sus umbrales se re-derivan con dato, no se improvisan."
---

# Patrón Era Energética (Pista A)

**Qué rescata** (de `HEXELION_BATTERY_FLAG_SPEC.md`, 15-may-2026, vía arqueología #43):
la idea de que la transición energética del rack (sin batería solar → con batería)
sea **un único punto de cambio** — una variable — y que el código de la Era
ausente viva versionado, dormido y **observable** (cada invocación dormida se
loguea), en vez de reescribirse en producción.

**Qué NO rescata** (enterrado, IronClaw): las tácticas de mercado que el spec
original envolvía — MCT-MAX, carga desde red a precio negativo para generar
ingresos, modos de ahorro/arbitraje autónomos. Los reflejos **jamás tocan
valor**. Ver `mente/necropolis/mito-fundacional-organismo-20260711/motivo.txt`.

## El mecanismo
- Flag: `P0X_BATTERY_PRESENT` (env; default `false` → Era `SOL_SINCRONO`).
- Módulo: `deploy/fragua/energia_era.py` → `ENERGY_ERA`, `@sleeping(reason)`,
  `@sun_synchronous(reason)`.
- Regla de la casa: **todo reflejo energético de la Pista A declara su Era**.
  Lo que solo tiene sentido con batería solar nace `@sleeping` (existe, se ve,
  no corre). Lo que solo tiene sentido sin ella, `@sun_synchronous`.

## Aplicación hoy
- `reflejo-bateria` es `@sun_synchronous` de facto: su premisa es que la UPS es
  la única reserva. Loguea su Era al arrancar (`era=SOL_SINCRONO`).
- Cuando llegue la batería (medidor DC soberano, obj. 2026-07-15+): cambiar el
  flag NO basta — los umbrales de los reflejos se **re-derivan midiendo**
  (Protocolo §3), el patrón solo garantiza que el cambio de Era es un
  interruptor y no una reescritura.
