# Telemetría de suites Playwright · misión LAS DOS PIELES

Registro append-only por fase. Suite: `hexelion/dashboard/tests/` contra `vite preview`
(build real, base `/ui/`). Viewports de ley (§2.4): 390 · 768 · 1280×800 (ASUS de Krista) · 1440.

| Fecha | Fase | Suite | Resultado | Duración | Navegador | Nota |
|---|---|---|---|---|---|---|
| 2026-07-19 | 1 | `fase1.spec.ts` (Puente §0 + tokens §2) | **32/32 verde** (0 flaky) | 3.7s | chromium (Playwright 1.49) | 4 viewports × 2 mundos × 4 pruebas: geometría 40×40@12,12 · z-index 9999 · href/aria-label · primer tab-order · conmutación de tokens por `data-theme` (`--nx-void` / `--jd-page` computados) |
