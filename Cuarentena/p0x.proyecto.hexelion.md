# 🏛️ SPECIFICATION MASTER FILE: p0x.proyecto.hexelion
> **SYSTEM_METADATA:**
> *   **Namespace:** `p0x.proyecto.hexelion`
> *   **Version:** `2.0-Hexelion-Jardin`
> *   **Status:** Fully Implemented and Validated in Lisboa/Beato
> *   **Date:** 2026-08-08
> *   **Editor:** AI Redactora Experta en Lenguaje AI (G.R.I.D. Protocol)
> *   **Classification:** Frontend, UI/UX, CSS, Themes & Interactive Dashboards

---

## 🥉 CAPA BRONCE (DOM ESTÁTICO, PLACAS DE FONDO & SWITCHER)

### 1. El Switcher de Tres Caras: El Puente [136, 137]
Navegación global anclada en la interfaz (`fixed; top: 12px; left: 12px; z-index: 9999`) con tamaño táctil mínimo de 44×44 px [137]:
*   **Cara 1: El Nexo (Jardín)**: SVG hexagonal con stroke fino en color phosphor (#43F5A0). Opacidad reposo: 0.45; activo/hover: opacidad 1 con transición lineal de 120ms [138].
*   **Cara 2: Le Jardin (El Nexo)**: SVG de hoja o vegetal. Botón circular con fondo pergamino (`--jd-parchemin`), borde amatista y border-radius 50%. Opacidad reposo: 0.55; activo/hover: escala scale(1.06) en 240ms cubic-bezier(.34,1.56,.64,1) y halo box-shadow [139].
*   **Cara 3: El Chat (Sínodo)**: SVG de burbuja de diálogo monocromo. Opacidad reposo: 0.45; activo/hover: opacidad 1. Redirecciona estrictamente a `http://soberano.[HOST_TAILNET_REDACTADO]:8080` [140].

### 2. Estilo Atmosférico y Regla Muro-Papel (`escena.css`) [104]
El archivo unificado `escena.css` importa `muro.css` (Nexo) y `laboratorio.css` (Jardin) [104]:
*   **Aislamiento del Fondo**: Placas de fondo (`placaa.webp` y `placab.webp`) cargadas en un contenedor `.scene-canvas` configurado con `position: fixed; pointer-events: none; z-index: 0` [104]. Esto evita que el fondo estático intercepte los clics del ratón destinados a los widgets interactivos de primer plano.
*   **Overlays**: Pantalla completa traslúcida en `#root` de color `rgba(5,7,6,.78)` para El Nexo y Le Jardin [104].

---

## 🥈 CAPA PLATA (ADAPTABILIDAD, LEY L.O.D. & ESTABILIDAD DEL DOM)

### 1. El Grid Soberano y la Tira de Herbier [104, 149]
*   **Layout del Nexo**: Contenedor de mapa y grafo distribuidos paralelamente mediante CSS Grid (`grid-template-columns: 1fr 1fr`) usando el selector `:has()` para no alterar el TSX original de React [104].
*   **Grid de Le Jardin**: Ancho centrado estricto a 1180px (`.jd-grid-soberana`) [104].
*   **Tira Deslizable de L'Herbier**: Reemplaza las grillas estáticas pesadas por un slider horizontal con snaps adaptativos (`scroll-snap-type: x mandatory; gap: 16px`) y máscaras laterales de transparencia para difuminar los bordes (`mask-image: linear-gradient(...)`) [149].
*   **Ficha de Icono Botánico**: Tamaño fijo de 96×112px, con una traslación hover de `translateY(-4px)` en 180ms [149].

### 2. Salvaguardas en Código (Sutura React & ErrorBoundary) [68, 85]
*   **ErrorBoundary `Limite`**: Envoltura nativa React implementada alrededor del componente `Cahier` en `src/jardin/main.tsx` [68]. Impide que un crash del diario deje la pantalla entera en blanco, mostrando el error en texto rojo sobre pergamino [68].
*   **Hook `useRevelado` Persistente**: Corrige el bug del StrictMode de React (que desmonta y remonta effects, vaciando colas de observación e hiriendo la opacidad a 0 constante) mediante el uso de un Set de referencia persistente (`useRef<Set<HTMLElement>>(new Set())`) [85].

### 3. Ley LOD (Level of Detail) del Second Brain [152]
*   **Zoom < 0.8**: Renderiza únicamente los nodos y etiquetas de texto fijadas [152].
*   **Zoom 0.8 - 1.4**: Muestra etiquetas de texto solo si el nodo posee una conectividad $\ge 4$ [152].
*   **Zoom > 1.4**: Renderiza todas las etiquetas del grafo [152].

---

## 🥇 CAPA GOLD (EL DIARIO ÍNTIMO DE NOTAS & REFLEJO DE BATERÍA SOLAR)

### 1. Le Cahier: El Ritual de Apertura y Cierre 3D [105, 148]
*   **Apertura del Libro (3D)**: Duración de 480ms mediante `perspective: 1200px` y una rotación espacial de `rotateY(-18deg) -> 0` [152]. Lanza automáticamente el foco en el editor al completarse [152].
*   **Cierre del Libro**: Duración de 360ms, ejecutando el movimiento inverso mediante un cierre en dos fases (`cerrando -> cerrado`) acoplado al evento `onAnimationEnd` para evitar cortes visuales abruptos [152].
*   **Lomo y Sello Físico**: Incorpora un lomo de cuero generado por gradientes en `::before` y una muesca de páginas en `::after` [86]. El botón de apertura incluye el sello del escudo de Aurelius [94].
*   **Tinteros de Control de Fricción**: Dos tinteros circulares de 48px: "Garder" (guarda de forma síncrona enviando HTTP POST a la ruta local `/api/jardin/notes`) y "Mémoire" (consolidación semántica en la base Gold relacional de engramas) [148].
*   **Honestidad del Diario**: Si la página está en blanco, el tintero Garder avisa "La page est blanche" sin cerrar el libro ni crear entradas falsas [100]. El pegado de texto sanea los strings forzando formato `text/plain` [105].

### 2. Modo de Ahorro de Carbono en Interfaces [103, 155]
Al reportar voltaje < 12.8V o alimentación por baterías UPS, el sistema inyecta la clase `.mode-ahorro` en el `<body>` [155]:
*   **El Nexo**: Muestra el banner superior "ON BATTERY · batch queue paused", reduce el brillo al 92%, suspende el refresco de los tiles de Leaflet y apaga los brillos de telemetría [155].
*   **Le Jardin**: Muestra la cinta "La lanterne baisse — le jardin économise sa lumière" con oscilación de 3s [155]. El motor de CSS **pausa los hilos ambientales y desvanece las animaciones** aplicando `animation-play-state: paused` y `opacity: 0` sobre los contenedores hijo del fondo en una transición lineal de **400ms** (sin filtros de desenfoque costosos en GPU) [1].

### 3. Duraciones Detalladas de la Luz de Ambiente (Loops) [156, 157]
*   **El Muro (Nexo)**: Neones variables de **7s / 11s / 13s** [156]. God-rays diagonales en periodos de **107s / 79s** [156]. Balanceo de hiedras en ciclos coprimas de **13s / 17s / 19s** [156]. Hojas temblando (13 instancias) de **2.7s a 3.9s** [156]. Barrido de mármol de **37s** [156]. Polen dorado flotando durante **11s** [156].
*   **El Laboratorio (Jardin)**: Cielo crepuscular respirando en ciclos de **23s** [157]. Luna oculta en `display: none` [157]. Luz violeta naciente angular de **29s** [157]. Halos de velas parpadeando de forma asíncrona en periodos primos de **1.7s / 2.9s / 4.3s / 5.3s** [157]. Chispas ascendentes en elevación lineal de **4.7s a 7.1s** [157]. Pociones vivas en ciclos independientes de **7.9s / 9.7s / 11.3s** [157].
