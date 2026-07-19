# Reporte de misión · LAS DOS PIELES — construcción del duplex Nexo/Jardin

- **Nodo:** soberano · **Fecha:** 2026-07-19 · **Estado:** COMPLETA (fases 0–5); el deploy en
  fragua queda como sesión aparte con la mano del carbono (paquete listo, ver §4).
- **Doctrina madre:** `mente/doctrina/BLUEPRINT_DISENO_SOBERANO.md` v1.2 (canon pendiente del
  commit del Soberano — carta #119). Protocolo Dry-Run + `[ACCEPT]` cumplido en las 6 fases.

## §1 · Qué se construyó (hexelion.git, rama `nexo-carbono-dashboard-20260623`)

| Fase | Commit(s) | Entregable |
|---|---|---|
| 0 · Rescate | `0a5c6ca` | As-built 2026-07-19 de lo servido en vivo (HTTP read-only contra fragua:8001) — el fuente completo espera el rescate #121 (mano-david) |
| 1 · Cimientos | `cba0b8f` | `tokens.css` duplex (§2, cero hex fuera), el Puente §0 (40×40, z-9999), bus 10Hz, interfaces núcleo |
| 2 · Nexo | `dee5c5b` | Celda universal §3.1, NO DATA §3.2, Sínodo §3.4, LOD, mapa, header sin cámara |
| 3 · Bandeja | `ae51d14` | Bandeja Ejecutiva §3.3: carril interno + carril comunidad-cuarentena, cartas con COMMANDS+VERIFY, higiene anti-secretos |
| 4a · Cahier | `cff1d88` | Le Cahier §4.2: Garder→rack (veto §7.7), buffer offline declarado, búsqueda con `<mark>`, Mémoire V1, Libro Abierto |
| 4b · Portada Jardin | `cfae84b` | L'Herbier + ficha §4.5, La Sentinelle honesta, L'École con sieste, mascota, navegación |
| 5 · Puertas y paquete | `2791c7f` `abec9e0` `1fa2ea1` `60d2023` | Gateway dos-pieles opt-in + `/api/jardin/notes` + dist versionado + 2 puertas finales |

**Puertas:** 172/172 verde, 0 flaky, 4 viewports (390/768/1280×800/1440) — registro por fase en
`mente/telemetria/PLAYWRIGHT_DOS_PIELES.md`. **Capturas:** `hexelion/dashboard/capturas/`
(fase2 Nexo ×2 vivo, fase3 bandeja ×2, fase4a Cahier ×2, fase4b portada ×2 vivo).

## §2 · El gateway (Fase 5)

- **Item 01** (`2791c7f`+`60d2023`): mount único `/ui` → `dashboard/dist` del repo (deploy = git
  pull + restart). Swap **opt-in** por `UI_CARA=dos-pieles`: aliases FileResponse para
  `/dashboard`, `/tareas` y `/jardin`. Sin la env, cero cambio de conducta.
- **Item 04** (`abec9e0`): `/api/jardin/notes` GET/POST — upsert por id sobre
  `verde/cahier_notes.json` (escritura atómica tmp+replace con lock, vacío honesto, más-nueva
  primero). Contrato exacto de `datos/notas.ts` (Fase 4a).
- **Bug cazado en esta fase (mío):** el comentario del mount prometía un alias `/jardin` que no
  existía — con el swap activo, el marcador de Krista y el 308 de `/indoor` caían en 404.
  Corregido (`60d2023`) antes de empaquetar; la ruta es inalcanzable sin el swap.

## §3 · Verificación en frío de los patches (cicatriz PROPUESTA_29)

`01-serve-from-git.patch` + `04-jardin-notes.patch` aplicados en orden sobre el gateway base
`cfae84b` en un directorio limpio producen **byte a byte** el `hexelion_gateway.py` de `60d2023`
(`diff` vacío). `python3 -m py_compile` OK. Los EXPECT del deploy viven en el paquete.

## §4 · El paquete único (`deploy/fragua/paquete-dos-pieles/`)

`README.md` (tabla de 5 ítems con verificación) · `01-serve-from-git.patch` ·
`04-jardin-notes.patch` · `05-SHA256SUMS` (17 archivos del dist `1fa2ea1`) · `05-swap.md`
(secuencia completa: backup obligatorio → código → restart sin swap con EXPECT → swap por env →
humo del Cahier → rollback de un gesto). Ítems 02 (PROPUESTA_28) y 03 (#98) siguen vivos y
documentados en la tabla. **Propose-only: nada se aplicó por SSH desde soberano.**

## §5 · Desviaciones declaradas (acumuladas de la misión)

1. **`dist/` versionado en git** (Fase 5, anunciada en Fase 0): deploy sin builds ni scp en
   fragua; 620KB/17 archivos; `.gitignore` documenta la razón.
2. **Quiz de L'École reconstruido desde las fichas** — los juegos del V1 viajan en el rescate
   #121; no se copió código no versionado que no se pudo leer.
3. **Fichas démo del Herbier declaradas** (chip «fiches de démonstration») mientras
  `verde/herbier/` siga vacío (#77); se retiran solas con datos reales (probado con mock).
4. **Stream MJPEG sin primer frame en captura headless** — la ventana viva de la Sentinelle
   queda para verificación de ojo humano en el deploy.
5. **Nombre del unit systemd del gateway en fragua: sin dato** desde soberano (SSH denegado,
   #121) — `05-swap.md` lo deja como `<unit-del-gateway>` a resolver in situ.
6. **Numeración**: los hallazgos #122–#133 pertenecen a la serie del brief de la misión (p.ej.
   #133 broker MQTT inexistente); las sugerencias nuevas saltan a #134 para no colisionar.

## §6 · Lo que necesita la mano de David

1. **La sesión de deploy en fragua** siguiendo `05-swap.md` (backup → verificar → swap) — #138.
2. **Las cartas de la Bandeja #116–#121** (canon producto, blueprint #119, PROPUESTA_29 #120,
   rescate as-built #121) — siguen pendientes de firma; la Bandeja Ejecutiva nueva las muestra.
3. **Sembrar `verde/herbier/*.md`** para que la démo se retire sola (#136, con Krista).

## §7 · SUGERENCIAS

Anexadas a `mente/feedback/PENDIENTES.md` como #134–#138 (S/M/L): endpoint real del carril
comunidad (M) · Mémoire→mini-cerebro con el grafo real (M) · sembrar herbier con Krista (S) ·
ESP32+broker MQTT del Vigía (L) · deploy del paquete, mano-david (S).
