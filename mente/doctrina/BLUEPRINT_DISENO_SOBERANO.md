---
id: blueprint-diseno-soberano
titulo: BLUEPRINT DE DISEÑO SOBERANO — Biblia Permanente del Preceptor
tipo: doctrina
clase: doctrina
version: 1.2.0
estado: propuesta (canon con el commit del Soberano)
editor_autorizado: preceptor-propone-carbono-canoniza
dominio: cara-visible
metrica_exito: "CC construye cualquier componente sin inventar un solo valor visual; cero decisiones estéticas tomadas fuera de este documento sin enmienda"
umbral_reedicion: "toda desviación en implementación se registra como enmienda con motivo; autopsias nuevas solo con capturas nuevas"
enlaces: [mapa-evolutivo-p0x, orquesta-modelos-p0x, doctrina-ai-interna]
actualizado: 2026-07-19
---

# BLUEPRINT DE DISEÑO SOBERANO v1.2
## Biblia Permanente del Preceptor

**Fecha de canonización:** 2026-07-19
**Destinatario:** Claude Code (Silicio Operativo — lectura obligatoria por fase)
**Regla de oro arquitectónica:** El Nexo y Le Jardin des Ombres conviven en el mismo organismo. Un enlace en la esquina superior izquierda es el puente entre ambos. Ese enlace es la prueba de que son el mismo ecosistema con dos caras: la sala de máquinas y el invernadero. Mismo rack, misma verdad, dos pieles.

**Ley de idiomas (inmutable):** strings de UI del Nexo en INGLÉS · strings de UI del Jardin en FRANCÉS · este documento, el código comentado y los commits en ESPAÑOL. Jamás se mezclan.

**Orden de lectura por fase de construcción:** Fase tokens → §2. Fase Nexo → §0, §1, §2, §3, §5, §6. Fase Jardin → §0, §1, §2, §4, §5, §6. Toda fase termina releyendo §7 (para no reintroducir lo destruido). El protocolo Dry-Run/[ACCEPT] de los Prompts Estratégicos sigue vigente: árbol de archivos + interfaces ANTES de código, y PARA.

---

## 0 · INVARIANTE GLOBAL: EL PUENTE (TOP-LEFT LINK)

El Puente es un elemento fijo, idéntico en posición en ambos mundos, con la piel de cada mundo. Es lo primero que se implementa y lo último que se puede romper.

**Geometría común (ambos temas):**
- `position: fixed; top: 12px; left: 12px; width: 40px; height: 40px; z-index: 9999;`
- Área de click completa (40×40 mínimo táctil). `cursor: pointer;` Elemento `<a id="puente" aria-label="...">`.
- El header de cada página reserva `padding-left: 64px` para no colisionar jamás con él.
- Accesible por teclado: primer elemento del tab-order. `:focus-visible` obligatorio (spec por tema abajo).

**El Puente en El Nexo (destino: el Jardin):**
- Glifo: `⬡` (hexágono outline) en `--nx-phosphor`, 20px, centrado, `stroke-width` visual fino.
- Reposo: `opacity: .45;` sin sombra, sin glow. Hover/focus: `opacity: 1;` `transition: opacity 120ms linear;` — **cero transform, cero scale** (el Nexo no juega).
- En hover aparece a su derecha la etiqueta `→ LE JARDIN` en IBM Plex Mono 10px, `letter-spacing: .2em`, color `--nx-text-dim`, aparición instantánea (sin slide).
- `:focus-visible: outline: 1px solid var(--nx-phosphor); outline-offset: 2px;` (radio 0).
- `aria-label="Cross to Le Jardin des Ombres"`.

**El Puente en Le Jardin (destino: el Nexo):**
- Glifo: anillo de hoja/puertecita `🌿` estilizado en SVG monocromo tinta `--jd-encre`, 22px, sobre una ficha circular de pergamino `background: var(--jd-parchemin); border: 1px solid rgba(109,74,224,.35); border-radius: 50%;`
- Reposo: `opacity: .55;` sombra `0 2px 6px rgba(60,42,20,.12)`. Hover/focus: `opacity: 1; transform: scale(1.06);` `transition: all 240ms cubic-bezier(.34,1.56,.64,1);` + halo violeta `box-shadow: 0 0 0 4px rgba(109,74,224,.14)`.
- Tooltip en hover: `→ El Nexo` en Caveat 14px tinta, dentro de una burbujita pergamino (delay 250ms).
- `:focus-visible: outline: 2px dashed var(--jd-violet); outline-offset: 3px;`
- `aria-label="Traverser vers El Nexo"`.
- `@media (prefers-reduced-motion: reduce)`: sin scale, solo opacity.

**Regla:** el Puente jamás se oculta, jamás se colapsa, jamás queda debajo de un overlay (z-index de overlays ≤ 900; ver escala §2).

---

## 1 · DIRECTRIZ DE CONTINUIDAD Y SIMPLIFICACIÓN

1. **Ley de Continuidad Evolutiva.** Todo lo heredado que este documento no mencione, SE MANTIENE tal cual funciona hoy (endpoints, flujos, textos de grounding, atajos). Si Claude Code encuentra una forma más elegante de integrar una función vieja en la nueva estética, tiene permiso para mutarla — registrando la mutación en el reporte como desviación aditiva declarada. El diseño debe respirar; la función no se amputa.
2. **Ley de Simplificación de Datos.** El dato crudo se simplifica visualmente para que el arte respire: máximo 7 filas visibles por grupo de telemetría (el resto tras un `▸ more` / `▸ plus`), números alineados a la derecha con `font-variant-numeric: tabular-nums`, unidades en color atenuado, explicaciones largas detrás de `ⓘ`. El dato no compite con el arte; lo sirve.
3. **Ley de Cuarentena (herencia de los Prompts Estratégicos):** componente ≤ 350 líneas o fisión binaria; prohibido `any`; toda interfaz defensiva ante `null | undefined`; bus de estado (los módulos no se hablan directamente); DOM no se re-renderiza más de 1 vez/100ms por celda (buffers del bus a 10Hz); `useMemo`/`useCallback` como reguladores de voltaje; cero dependencias nuevas — Leaflet y force-graph quedan **naturalizados** (ya viven en el organismo), nada más entra sin firma.
4. **Ecopuertos visuales:** todo contenedor de asset (mapa, grafo, cámara, iconos de planta) tiene dimensiones fijas o `aspect-ratio` + `object-fit` estricto declarados AQUÍ. El asset es un ciudadano temporal en la celda; no puede modificar las paredes de la celda. Si el asset no llega: estado NO DATA (§6), jamás un layout que salta.

---

## 2 · SISTEMA DE TOKENS DUPLEX (DUAL-THEME) — DISECCIÓN COMPLETA

Implementación: `tokens.css` único con dos ámbitos: `[data-theme="nexo"]` y `[data-theme="jardin"]`. Prohibido hardcodear un color fuera de tokens.

### 2.1 · Tipografías (Google Fonts exactas)

**El Nexo:**
- `IBM Plex Mono` — pesos 400, 500, 600. TODO el dato, chips, botones, feeds. Body: 13px / line-height 1.55 / letter-spacing .01em. Chips y botones: 11px / 600 / letter-spacing .14em / uppercase. Micro-etiquetas: 10px / 500 / .2em.
- `Cinzel` — peso 600, SOLO para: wordmark HEXELION, títulos de página (RACK, SIGNATURE TRAY, SECOND BRAIN). 22–28px / letter-spacing .35em / uppercase. Nunca en datos.

**Le Jardin:**
- `Cormorant Garamond` — 500, 600. Títulos de sección (La Sentinelle, L'Herbier…): 34px / 1.2 / letter-spacing .01em. Nombres de planta: 24px/600.
- `EB Garamond` — 400, 500. Cuerpo de fichas y del Cahier: 17px / line-height 1.65. Itálica para citas botánicas.
- `Caveat` — 500. Acentos manuscritos: tooltips, etiquetas de tintero, voz de la mascota: 15–16px.
- `Inter` — 400, 500. EXCLUSIVA para métricas del ESP32 y chrome técnico: 12px / `tabular-nums` / letter-spacing .02em (el contraste anime-realidad del Prompt Estratégico).

Carga: `display=swap`, subset latin+latin-ext, preload de los 2 pesos críticos por tema. Nada más.

### 2.2 · Paleta EL NEXO (brutalismo soberano — restrictiva)

Fondos y estructura:
- `--nx-void: #060B09` (negro carbón mate, base de página)
- `--nx-panel: #0A120E` (celda) · `--nx-panel-2: #0D1713` (bloque interno, p.ej. commands)
- `--nx-border: #1E3A2A` (1px universal) · `--nx-border-dim: #12261C`
Tinta:
- `--nx-text: #C8E6D5` (dato) · `--nx-text-dim: #6E8A7C` (unidades, ayudas) · `--nx-text-ghost: #55705F` (NO DATA, placeholders)
Semánticos:
- `--nx-phosphor: #43F5A0` (Verde Soberano: vida, ok, primario) · `--nx-phosphor-dim: #2E8F63`
- `--nx-amber: #FFB454` (alerta de reflejos, espera de firma, stale) 
- `--nx-danger: #FF5C5C` (fallo/ERROR/crítico — uso excepcional)
Identidad de voces (SOLO en dot de estado y borde-izquierdo 2px de su cápsula; jamás en texto ni fondos): monje `#43F5A0` · vocero `#4CC9F0` · berserker `#FF5C5C` · escriba `#FFB454` · alquimista `#5C7CFF` · enlace `#7FD1E8`.
Sombras: **prohibidas las difusas.** Solo `box-shadow: 0 0 0 1px <border>` para énfasis y glow de estado permitido únicamente como `text-shadow: 0 0 8px rgba(67,245,160,.35)` en cifras clave vivas.
Radio de borde: **0px universal.** Firma hexagonal opcional de celda: `clip-path` con corte de 10px en la esquina superior-izquierda del header de celda.
Filtros: ninguno (ni blur ni saturate) — la austeridad es literal.

### 2.3 · Paleta LE JARDIN (magic-solarpunk-anime — cálida)

Mundo:
- `--jd-bois-1: #EAD9B8` · `--jd-bois-2: #DEC9A0` (mesa de madera, ver §4.1)
- `--jd-page: #F3EAD8` (fondo de secciones) · `--jd-parchemin: #F8F1E2` (cartas/fichas)
- `--jd-encre: #2B2117` (tinta sepia-negra, texto primario) · `--jd-encre-dim: #6B5C49` · `--jd-fantome: #8A7B63` (capteur à venir)
Magia:
- `--jd-violet: #6D4AE0` (magia primaria, Mémoire, focus) · `--jd-violet-fonce: #4C1D95` (grafo, énfasis)
- `--jd-cyan-bio: #58D6C9` · `--jd-magenta-doux: #E28FD8` (bioluminiscencia — solo acentos ≤ 10% de superficie)
- `--jd-or-bougie: #D9A441` (dorado vela: valores reales, éxito) · `--jd-vert-ombre: #4E6E4E` (Garder, vida vegetal) · `--jd-mal: #C25E5E` (maux/errores, suave)
Sombras (capas suaves, siempre las dos): `--jd-ombre: 0 2px 6px rgba(60,42,20,.12), 0 12px 28px rgba(60,42,20,.10);`
Radios: cartas y fichas **14px** · burbujas de chat y mascota **22px** · tinteros **50%**.
Filtros permitidos: `backdrop-filter: blur(8px) saturate(1.1)` SOLO en overlays flotantes (mascota, libro abierto).

### 2.4 · Espaciado, grid y z-index (ambos mundos)
- Escala: 4 / 8 / 12 / 16 / 24 / 32 / 48 / 64. Nexo: gap entre celdas 16px, "aislamiento térmico" vertical entre grupos 24px. Jardin: ritmo vertical entre secciones 64px, padding interno de carta 24px.
- Contenedor máximo: Nexo full-bleed con padding 24px; Jardin `max-width: 1120px` centrado (es un libro, no una consola).
- Z-index (ley): contenido 1 · header 100 · overlays/mascota 800 · modales 900 · **el Puente 9999**.
- Breakpoints de verdad del proyecto: 390px (móvil) · 768px · **1280×800 (el ASUS de Krista — viewport de referencia del Jardin)** · 1440px+.

---

## 3 · ANATOMÍA: EL NEXO (BRUTALISMO SOBERANO) — DISECCIÓN COMPLETA

### 3.1 · La celda hexagonal (contenedor universal)
- Caja: `background: var(--nx-panel); border: 1px solid var(--nx-border); border-radius: 0;` corte hexagonal de 10px en el header (clip-path). Sin sombra.
- Header de celda: 40px alto; glifo colapso `▸/▾` phosphor-dim; título 11px/600/.14em uppercase; a la derecha, **el chip del bus**: frescura del feed (`SSE · 2s` en text-dim; >30s → amber `STALE · 34s`; muerto → NO DATA §6). Toda celda declara su frescura o declara su vacío. Ausencia ≠ 0.
- Celda en alerta: `border-color: var(--nx-amber)` + chip amber. Celda en fallo: borde danger. Sin animación de entrada — las celdas EXISTEN, no llegan.
- Celda colapsada: muestra header + UNA línea-resumen de estado (p.ej. `STORE · NUT read-only · OL 100%`). Prohibido el vacío mudo de hoy (autopsia §7).

### 3.2 · NO DATA (la interfaz no miente)
Ver §6. En el Nexo: bloque `background: #0B0F0D; border: 1px dashed var(--nx-border-dim);` texto `NO DATA` IBM Plex Mono 12px/500/.2em color `--nx-text-ghost`, centrado, altura fija del ecopuerto correspondiente. Nada de spinners infinitos: si a 1500ms no hay dato, se rinde NO DATA con timestamp del último dato conocido si existe (`last seen 02:44`).

### 3.3 · Las Cartas del Signature Tray (disección exacta)
La carta es la unidad ejecutiva del carbono. Grid vertical de bloques, `gap: 12px`, carta `border: 1px solid var(--nx-border); background: var(--nx-panel); padding: 16px; border-radius: 0;`
1. **Fila de identidad:** chips de estado (open→amber, signed→phosphor-dim, done→phosphor, discarded→danger-dim), `border-radius: 2px` (única concesión, para legibilidad de chip), 10px/600/.14em; a la derecha `updated YYYY-MM-DD` en text-ghost.
2. **TÍTULO:** 13px/600 uppercase `--nx-text`; debajo **why** en 12px itálica text-dim, una sola línea.
3. **ORIGIN / DEST:** dos filas `nodo:ruta` en 12.5px; el nodo como chip con dot del color de identidad del nodo; la ruta en text; icono `→` entre ambas filas.
4. **COMMANDS:** bloque `background: var(--nx-panel-2); border-left: 2px solid var(--nx-phosphor); padding: 12px; font: 12.5px IBM Plex Mono; white-space: pre-wrap;` Botón **COPY** anclado arriba-derecha del bloque: 10px/600/.2em, `border: 1px solid var(--nx-border)`, hover: fondo phosphor + texto void (inversión, 120ms linear), tras click muta a `COPIED ✓` 1.5s.
5. **VERIFICATION:** mismo bloque con `border-left: 2px solid var(--nx-amber)`; primera línea el comando; segunda línea `EXPECT ▸ <salida esperada>` en amber-dim. **Ninguna carta se publica sin este bloque** — es la ley nacida del corrupt-patch de PROPUESTA_29.
6. **Acciones:** `SIGN` (outline phosphor) · `DISCARD → NECROPOLIS` (outline danger) · 0 radius, 11px/600/.14em, hover inversión 120ms.
Carta ejemplar permanente (se implementa como fixture de test): el reintento de PROPUESTA_29 con su `git apply → grep → commit → push` y su EXPECT.

### 3.4 · Telemetría, Sínodo, mapa y grafo
- **SYSTEM STATE:** filas clave-valor como hoy, con la Ley de Simplificación (§1.2): 7 visibles por grupo, resto tras `▸ more`.
- **Cápsulas del Sínodo:** conservan estructura actual; el color de voz queda SOLO en dot + borde-izquierdo 2px; las barras de progreso ambiguas de hoy se sustituyen por el chip del bus (frescura + métrica única real de la voz: `temp 43.5°C`, `omie —`). DEGRADED → chip amber; STANDBY → text-dim.
- **Unified Map (ecopuerto):** contenedor `height: clamp(320px, 38vh, 520px)`; leyenda colapsable; explicación Osiris tras `ⓘ`; botones RESTART AIS/ADS-B en outline amber (acciones con efecto). Tiles oscuras actuales se conservan.
- **Second Brain (ecopuerto):** `aspect-ratio: 16/9` máx 640px alto. **Ley de etiquetas (LOD):** zoom < 0.8 → solo nodos + etiquetas fijadas (SOBERANO, IRONCLAW, EL NEXO); 0.8–1.4 → etiquetas si grado ≥ 4; > 1.4 → todas. Hover: etiqueta siempre, con halo `text-shadow: 0 0 6px var(--nx-void)`. Colisión: se oculta la de menor grado. La sopa de texto actual muere (autopsia §7).
- **Header:** reloj PT en `--nx-text` brillante; US/CN en text-dim (Lisboa es casa; el dato sirve). Chip ED25519 + PROOF + PRIVACY se conservan. La miniatura de cámara sale del header y se realoja en la celda OBSERVE.

---

## 4 · ANATOMÍA: LE JARDIN DES OMBRES (MAGIC-SOLARPUNK-ANIME) — DISECCIÓN COMPLETA

### 4.1 · El mundo: madera y pergamino (solo CSS, cero imágenes de fondo)
Fondo de página (la mesa):
```css
background:
  radial-gradient(120% 90% at 50% 0%, rgba(255,246,224,.35), transparent 60%),      /* luz de linterna */
  repeating-linear-gradient(90deg, rgba(94,66,38,.06) 0 2px, transparent 2px 180px), /* juntas de tabla */
  repeating-linear-gradient(0deg, rgba(94,66,38,.03) 0 1px, transparent 1px 7px),    /* veta */
  linear-gradient(180deg, var(--jd-bois-1), var(--jd-bois-2));
```
Cartas: `background: var(--jd-parchemin); border-radius: 14px; box-shadow: var(--jd-ombre); border: 1px solid rgba(94,66,38,.14);`
Washi tape (esquinas de cartas señaladas): pseudo-elementos `::before/::after` de 64×22px, `transform: rotate(-45deg)` (y +45), `background: rgba(255,255,255,.55); border: 1px dashed rgba(94,66,38,.25);` en esquinas opuestas.

### 4.2 · Le Cahier — página propia, en limpio
Layout: `grid-template-columns: minmax(420px, 1.2fr) .8fr; gap: 32px;` (en <768px: una columna, archivo debajo).
**Columna editor:**
- Superficie de escritura: carta pergamino con líneas de cuaderno: `background-image: repeating-linear-gradient(transparent 0 33px, rgba(43,33,23,.08) 33px 34px);` `contentEditable` con `caret-color: var(--jd-violet); color: var(--jd-encre); font: 17px 'EB Garamond';` Focus: `box-shadow: inset 0 0 0 3px rgba(109,74,224,.12);` El texto se comporta como tinta: `::selection { background: rgba(109,74,224,.22); }`
- **Tinteros** (botones): círculos 48px con etiqueta Caveat 14px debajo. `Garder` = tinta verde `--jd-vert-ombre`; **`Mémoire`** = tinta violeta `--jd-violet`. Press: onda de tinta (radial-gradient que escala 0→1, 300ms ease-out). Hover: el líquido "tiembla" — `transform: translateY(-2px)` 180ms, sin glow duro.
- **Persistencia (decisión del Preceptor, ver autopsia):** `Garder` → `POST /api/jardin/notes` al gateway — la verdad vive en el rack ("Tout reste à la maison" es literal solo si la maison es el rack). `localStorage` queda como buffer de borrador offline con reconciliación al volver la red. `Mémoire` → propone la nota como delta al mini-cerebro de Krista; el nodo nuevo del grafo pulsa una vez en violeta al aceptarse.
- **Esquema second-brain (bajo el editor):** carta tintada `background: #F2EDFB; border: 1px solid #D9CEF5;` altura fija 320px (ecopuerto). Force-graph reutilizado del Nexo, re-vestido: nodos `--jd-violet` (relleno), aristas `rgba(109,74,224,.35)`, etiquetas tinta 11px Inter. Interacción idéntica al Nexo (scroll zoom, drag pan) — mismo músculo, otra piel.
**Columna archivo:**
- Buscador arriba: `Rechercher par mots…`, input pergamino, filtro client-side; coincidencias con `<mark style="background: rgba(109,74,224,.18)">`.
- Notas como `<details>` nativos (el patrón rail-mod de la casa): `<summary>` = título EB Garamond 15px + fecha Inter 11px dim; apertura 220ms ease; borde inferior 1px `rgba(94,66,38,.14)` entre notas.
- **Modo Libro Abierto:** el botón `Naviguer` dispara la animación de libro (§5) y luego `requestFullscreen()`. El componente sabe su modo vía `document.fullscreenElement`.

### 4.3 · L'Herbier — la tira de iconos (scroll horizontal)
- Contenedor: `display: flex; overflow-x: auto; scroll-snap-type: x mandatory; gap: 16px; padding: 8px 48px;` máscaras de desvanecido en ambos extremos (`mask-image: linear-gradient(90deg, transparent, #000 48px, #000 calc(100% - 48px), transparent)`).
- Flechas `‹ ›`: círculos 36px pergamino, sombra `--jd-ombre`, ancladas a los bordes, ocultas en táctil (`@media (hover:none)`), click desplaza `scrollBy` un viewport-tile con `behavior: smooth`.
- Ficha-icono: 96×112px, tile pergamino radius 14, icono de planta 56px (`assetPaths`, `object-fit: contain`), nombre debajo Cormorant 14px. Sombra reposo suave; hover: `translateY(-4px)` 180ms + sombra crece; planta seleccionada: anillo `box-shadow: 0 0 0 2px var(--jd-violet)`.
- Click → la ficha del grimorio actual (página conservada casi íntegra, ver §4.5) entra deslizándose (§5). Añadir planta = añadir MD + icono; la tira crece sin rediseño.
- **Savoir Plus (mascota flotante):** mascota fija `bottom: 24px; left: 24px;` 64px, z-index 800 (jamás pisa al Puente). Click → panel 360×480 anclado sobre ella: `background: rgba(248,241,226,.86); backdrop-filter: blur(8px) saturate(1.1); border: 1px solid rgba(109,74,224,.35); border-radius: 18px;` entrada spring 260ms `cubic-bezier(.34,1.56,.64,1)`. El Context Provider inyecta `{plantId, plantName}` de la planta abierta en el system prompt de la IA local — la mascota sabe qué planta miras sin preguntar.

### 4.4 · La Sentinelle — el ojo con sus cuatro medidas
- Cámara: ecopuerto `aspect-ratio: 4/3; width: min(420px, 100%); object-fit: cover; border-radius: 14px;` Click → Fullscreen API. Botones `Plein écran`/`Photo` conservados.
- **Overlay de métricas** (franja inferior sobre la imagen): `background: rgba(20,14,8,.55); backdrop-filter: blur(4px);` 4 chips Inter 12px `tabular-nums`: Température · Humidité · Lumière · pH. Valor real → `color: var(--jd-or-bougie); font-weight: 600;` con brillo sutil `text-shadow: 0 0 6px rgba(217,164,65,.35)`. Sin feed → `— · capteur à venir` (§6). La asimilación de payloads del ESP32 va por el bus (10Hz máx al DOM) y JAMÁS bloquea el hilo del click a fullscreen.

### 4.5 · Fichas de planta y École Ludique
- Ficha (simplificación): se conservan las 4 cartas cualitativas (Lumière/Arrosage/Sol/Température) y la tabla IDÉAL|MESURÉ; los "Maux connus" pasan a acordeones `<details>` cerrados por defecto (menos muro de texto, mismo saber). Icono Hoja/Flor arriba-izquierda vía assetPaths.
- L'École Ludique: contenedor aislado con error-boundary propio. Si un juego colapsa: la carta entra en estado "sieste" (mascota dormida + `Le jeu fait la sieste…`) sin tocar al resto del jardín. `useMemo`/`useCallback` obligatorios en la lógica de juego; un pico de CPU del Quiz no puede tropezar la animación del libro ni la Sentinelle.

---

## 5 · TRANSICIONES Y MICRO-INTERACCIONES — DISECCIÓN COMPLETA

**Ley madre:** En el Nexo, CERO animaciones de entrada; los cambios de estado son instantáneos o `opacity 80ms linear` máximo; lo único que respira es el dot de estado (`blink 1.2s steps(2)` en degraded) y el caret. En el Jardin, todo se mueve como agua y tinta — pero una sola vez y con propósito.

Tabla de tiempos del Jardin (valores exactos, sin excepción):
- Revelado de sección al entrar en viewport (una vez, IntersectionObserver): `240ms ease-out`, `translateY(8px)→0` + `opacity 0→1`.
- **Libro abriéndose** (Cahier → Libro Abierto): `480ms cubic-bezier(.22,1,.36,1)`, `perspective: 1200px; rotateY(-18deg)→0` + sombra que se despliega; al terminar, `requestFullscreen()`. Cierre: inverso 360ms.
- Expandir nota (`<details>`): `220ms ease` altura + `opacity 120ms`.
- Paso de página del Herbier / ficha entrando: `320ms ease-in-out`, `translateX(24px)→0` + `rotateZ(.4deg)→0` (el papel gira apenas).
- Tintero hover: `180ms`; press onda de tinta `300ms ease-out`.
- Mascota panel: spring `260ms cubic-bezier(.34,1.56,.64,1)`.
- Quiz feedback (respuesta): pulso del borde `200ms` (correcto → or-bougie; error → mal), sin confetti — la magia es sobria.
**Global ambos mundos:** `@media (prefers-reduced-motion: reduce) { *, *::before, *::after { animation: none !important; transition: none !important; } }` — la doctrina respeta el sistema nervioso del carbono.

---

## 6 · REGLAS DE EMERGENCIA (HONEST SENSORS Y REFLEJOS) — DISECCIÓN COMPLETA

**El estado sin dato (la interfaz no miente):**
- Jardin: `— · capteur à venir` en Inter 12px, `color: var(--jd-fantome)`, `font-style: italic`, sin sombra ni brillo. El guion es tipográfico (em-dash), el separador `·` con espacios finos.
- Nexo: `NO DATA` en IBM Plex Mono 12px/500/.2em, `color: var(--nx-text-ghost)`, caja §3.2, con `last seen HH:MM` si existe histórico.
- **Prohibido:** skeletons infinitos, ceros falsos, valores cacheados presentados como frescos. A los 1500ms sin payload, se rinde el estado vacío. `null`/`undefined` SIEMPRE manejados en la interfaz de datos (prohibido `any`; el tipado es la primera línea de la honestidad).
**El valor real:** Nexo → `--nx-text` con cifra clave en phosphor + `text-shadow 0 0 8px rgba(67,245,160,.35)`; peso 500. Jardin → tinta 600 con acento `--jd-or-bougie` en el número; la unidad siempre dim. Real y ausente JAMÁS comparten estilo — a un vistazo se sabe qué es verdad medida.
**Modo ahorro (reflejo-batería · UPS OB):** clase global `.mode-ahorro` en `<body>`:
- Nexo: banner superior 28px amber `ON BATTERY · batch queue paused` con dot `blink 1s steps(2)`; se desactivan TODOS los text-shadows/glows (pintura barata); el mapa muestra chip `tiles paused`.
- Jardin: banner hoja `La lanterne baisse — le jardin économise sa lumière` con respiración `3s ease-in-out infinite alternate opacity .85↔1`; filtro global `brightness(.92) saturate(.9)`; la mascota sostiene una linterna.
- Los eventos de reflejos (batería/térmico/vibración) entran al feed como líneas amber deterministas; el Monje los narra después — la UI solo refleja, no decide.

---

## 7 · AUTOPSIA VISUAL Y DECISIONES DEL PRECEPTOR

Estudio sobre las siete capturas del estado actual (Nexo watchman, Jardin actual, Sínodo Deliberar, Observar, Unified Map, Second Brain, Signature Tray). Lo que se destruye, lo que se rescata, y por qué lo escrito arriba es superior.

**DESTRUIDO, con causa:**
1. *El marco neón cian que rodea el Nexo* — ornamento que compite con los datos y gasta contraste. Sustituido por borde 1px y glow reservado a cifras vivas (§2.2). El brutalismo no brilla; señala.
2. *El fondo negro plano del Jardin* — el propio Soberano lo sentenció ("poco agraciado"), y las cartas crema flotaban huérfanas en el vacío. Nace el mundo de madera y pergamino en CSS puro (§4.1): las cartas ahora descansan sobre una mesa, no sobre la nada.
3. *La sopa de etiquetas del Second Brain* — en la captura, veinte títulos de doctrina se pisan hasta la ilegibilidad. Muere bajo la Ley LOD (§3.4): un grafo que no se puede leer es decoración, no memoria.
4. *Las barras de progreso ambiguas de las cápsulas del Sínodo* — ¿progreso de qué? Un dato que no se puede explicar es ruido. Las reemplaza el chip del bus con la métrica única real de cada voz (§3.4).
5. *La miniatura de cámara en el header del Nexo* — el header es estado e identidad, no media. Se realoja en OBSERVE.
6. *Los paneles colapsados mudos* (LOGBOOK/STORE/ALCHEMIST vacíos) — un rectángulo sin información es espacio muerto. Toda celda colapsada declara una línea-resumen (§3.1).
7. *localStorage como única memoria del Cahier* (venía en el Prompt Estratégico) — VETO del Preceptor: la soberanía del dato de Krista no puede vivir en un perfil de navegador que se borra con un update. La verdad va al rack vía gateway; localStorage queda de buffer (§4.2). "Tout reste à la maison" — y la maison es el rack.
8. *La grilla 4x4/6x6 del Herbier* (Prompt Estratégico) cede ante *la tira horizontal* — decisión ya tomada por el Soberano y superior para un grimorio que crecerá: una tira escala a 40 plantas sin re-maquetar; una grilla no.

**RESCATADO, con honor:**
1. *La estructura de celdas y el feed de pulsos del Nexo* — huesos correctos; solo se les quita el maquillaje.
2. *Las cartas crema del Jardin* — eran la semilla del tema nuevo; ahora tienen mundo alrededor.
3. *El microcopy de grounding* — "Elle répond avec ce qu'elle sait vraiment — et si elle ne sait pas, elle te le dit" asciende de texto suelto a LEY (§6). Es la frase más P0X de toda la interfaz.
4. *Los chips de estado del Observar* (ACCEPTED/PENDING_REVIEW/ERROR con motivo verbatim `rc=1`) — honestidad ya construida; solo se normaliza tipografía.
5. *El Unified Map* — la página más cercana a la doctrina; se le colapsa la leyenda y se le da su ecopuerto.
6. *El vacío honesto del Tray* ("nothing here — tray is clean for this filter") y el flujo SIGN/DISCARD→NECROPOLIS — intactos; la carta ejecutiva (§3.3) los completa con lo que faltaba: comandos y verificación. La lección del corrupt-patch queda fundida en la interfaz.
7. *La mascota del Jardin y los dos juegos* — intactos en su patio aislado; ganan error-boundary y contexto de planta.

**DECISIONES DE ARQUITECTO (las que nadie pidió y alguien debía tomar):**
- Dos mundos, un solo bus, un solo grafo re-vestido, un solo sistema de ecopuertos: el Jardin no es otra app, es la otra cara. El Puente (§0) lo demuestra en 40×40 píxeles.
- La ley de idiomas y la ley de tokens hacen imposible el drift estético por sesión: si un color no está en §2, no existe.
- Este blueprint es doctrina de FORMA. La mecánica (qué endpoint, qué delta, qué firma) sigue viviendo en su canon. Si forma y mecánica chocan, gana la mecánica y se enmienda la forma — con changelog.

*Firmado: el Preceptor. El Soberano canoniza con su commit. CC construye fase a fase, con Dry-Run y [ACCEPT], sin inventar un píxel.*
