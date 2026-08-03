# CONTRATO DEL JURADO · verificación cruzada  (PROPUESTA — pendiente de firma del Soberano)

**Estado:** ⬜ propuesta · 2026-08-03 · BLOQUE 8.2. **El jurado ANTES que el feed.**
Un veredicto es un JUICIO con fecha, no una caché. Ante duda o caducidad → **NO DATA**,
jamás un recuerdo fantasma. El combustible no confiable jamás vota solo, firma ni atesta.

## Tiers de confianza de las fuentes
- **T0 · propia** — sensor del rack (AIS de El Vigía, ADS-B de La Fragua): observación directa.
- **T1 · pública verificable** — API con contrato y terceros que la corroboran (p.ej. aisstream).
- **T2 · no confiable** — OSINT / OSIRIS / GDELT: combustible. NUNCA firma, NUNCA atesta, NUNCA vota solo.

## 1 · Qué cuenta como fuente INDEPENDIENTE
Dos fuentes son independientes **si y solo si** cumplen las tres:
1. **No comparten upstream** (ni servicio, ni nodo, ni pipeline). Dos derivados de GDELT NO son independientes.
2. **Modalidad de recolección distinta** (sensor RF propio / API pública / scrape OSINT / cadena on-chain).
3. **Tier de confianza declarado por separado.**

## 2 · Quórum — cuántas para emitir veredicto
- **CORROBORADO** = ≥2 fuentes independientes de acuerdo, **con al menos una T0 o T1**. (Dos T2 de acuerdo **no** corroboran.)
- **FUENTE-ÚNICA** = 1 sola T0/T1. Se declara "single-source" — honesto, no disfrazado de corroborado.
- **NO-VERIFICADO** = solo una T2 lo afirma. Se muestra etiquetado `[OSINT no confiable]`, jamás como hecho.
- Ninguna fuente → **NO DATA**.

## 3 · Contradicción — ¿el veredicto correcto puede ser EN DISPUTA?
**Sí. `EN-DISPUTA` es un veredicto VÁLIDO y honesto, no un fallo.**
- Dos fuentes **T0/T1 independientes que se contradicen** → `EN-DISPUTA`: se emite con **ambas** afirmaciones y sus fuentes; el jurado **no elige ganador en silencio**. Una contradicción declarada vale más que un consenso fabricado.
- **T2 contra T0/T1** → gana la T0/T1 para el HECHO; la divergencia de la T2 se **registra** y se etiqueta "OSINT discrepante" — el combustible no confiable no tumba una observación directa (no dispara disputa).
- **Nunca** se promedia ni se inventa un punto medio.

## 4 · Caducidad — TTL (un veredicto sin caducidad es un recuerdo falso con retraso)
- Todo veredicto lleva `emitido` + `caduca`. Al caducar **sin re-corroboración** → revierte a **NO DATA**, jamás al veredicto viejo (STALE ≠ MISSING, como la clave del M5).
- TTL por **volatilidad** del dato:
  - posición/evento marítimo o aéreo (volátil): TTL corto, ≤ la ventana de frescura del feed (p.ej. 60–120 s).
  - entidad/sanción (estable): TTL largo (horas) — pero **siempre finito**.
- **El TTL del veredicto ≤ el TTL más corto de sus fuentes** (un veredicto no puede ser más fresco que su fuente más vieja).

## Invariantes del jurado
- Determinista y auditable: mismo conjunto de fuentes → mismo veredicto.
- Jamás firma ni escribe al Faro (los veredictos **no** son atestación).
- Jamás pinta un veredicto sin fuente y sin fecha de caducidad.

---
**PROPUESTA. Requiere firma del Soberano antes de escribir el motor del jurado (8.3).**
Nada desplegado, ninguna red saliente nueva, ningún dato pintado — solo esta especificación.
