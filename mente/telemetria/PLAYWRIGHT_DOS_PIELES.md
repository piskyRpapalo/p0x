# Telemetría de suites Playwright · misión LAS DOS PIELES

Registro append-only por fase. Suite: `hexelion/dashboard/tests/` contra `vite preview`
(build real, base `/ui/`). Viewports de ley (§2.4): 390 · 768 · 1280×800 (ASUS de Krista) · 1440.

| Fecha | Fase | Suite | Resultado | Duración | Navegador | Nota |
|---|---|---|---|---|---|---|
| 2026-07-19 | 1 | `fase1.spec.ts` (Puente §0 + tokens §2) | **32/32 verde** (0 flaky) | 3.7s | chromium (Playwright 1.49) | 4 viewports × 2 mundos × 4 pruebas: geometría 40×40@12,12 · z-index 9999 · href/aria-label · primer tab-order · conmutación de tokens por `data-theme` (`--nx-void` / `--jd-page` computados) |
| 2026-07-19 | 2 | `fase1+fase2.spec.ts` (Nexo re-vestido §3) | **56/56 verde** (0 flaky) | 5.1s | chromium | 11 celdas presentes · NO DATA §3.2 con gateway cortado por intercepción (lección: `vite preview` hereda `server.proxy` → sin abortar rutas la suite dependía de la red del rack) · fixture AIS-idle capturado del vivo · cero solapes de clicables · cero animaciones de entrada · cámara fuera del header |
