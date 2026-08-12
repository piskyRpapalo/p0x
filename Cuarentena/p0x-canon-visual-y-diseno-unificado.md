# 🎨 CANON VISUAL, DISEÑO DE INTERFAZ Y ARQUITECTURA DE DASHBOARDS p0x (v2.0)
## VERSION: 2.0-Visual-Master
## ESTADO: COMPLETADO Y CONSOLIDADO TRAS AUDITORÍA DE TERRENO

---

### I. EL SWITCHER DE TRES CARAS (EL PUENTE) [113]

El Puente es el componente de navegación global anclado permanentemente en la interfaz del sistema. Facilita la conmutación entre las tres vistas principales: El Nexo (Jardín), La Forja (Sínodo) y el Chat [113].

#### 1. Especificación de Contenedor General [113]
*   **Posición**: `fixed; top: 12px; left: 12px; z-index: 9999`
*   **Estructura**: Elemento `<nav id="puente">` con un diseño de tres caras alineadas en una fila (`display: flex; gap: 4px;`).
*   **Tamaño Táctil Mínimo**: 44×44 px por cara.
*   **Reserva de Cabecera**: El contenedor de fondo adyacente debe poseer `padding-left: 160px` para evitar colisiones visuales de renderizado.
*   **Orden de Foco**: Encabeza el flujo secuencial de tabulación en el documento (`tabindex`).
*   **Idiomas de Interfaz**: Las etiquetas de texto descriptivas se configuran en inglés (EN) desde la interfaz del Nexo, en francés (FR) desde Le Jardin, y bajo la tematización del Nexo para el Chat.

#### 2. Cara 1: El Nexo (Jardín) [114]
*   **Glifo**: SVG hexagonal con contorno (*stroke*), tamaño 20px y grosor de línea (*stroke-width*) fino.
*   **Color**: `--nx-phosphor` (#43F5A0).
*   **Estado de Reposo**: `opacity: 0.45`, sin efectos de sombra ni glow.
*   **Estado Activo/Hover/Focus**: `opacity: 1`, transición lineal de 120ms (`transition: 120ms linear`), sin transformaciones de escala.
*   **Etiqueta**: "→ LE JARDIN", tipografía IBM Plex Mono de 10px, espaciado de letras 0.2em, color `--nx-text-dim`.
*   **Foco Accesible**: `outline: 1px solid var(--nx-phosphor); offset: 2px`
*   **Atributo ARIA**: `aria-label="Cross to Le Jardin des Ombres"`

#### 3. Cara 2: Le Jardin (El Nexo) [115]
*   **Glifo**: SVG de hoja o vegetal monocromo, tamaño 22px.
*   **Ficha/Fondo**: Botón circular con fondo pergamino (`background: var(--jd-parchemin)`), borde de `1px solid rgba(109,74,224,.35)` y `border-radius: 50%`.
*   **Estado de Reposo**: `opacity: 0.55`, con sombra estática de `0 2px 6px rgba(60,42,20,.12)`.
*   **Estado Activo/Hover/Focus**: `opacity: 1`, transformación de escala `transform: scale(1.06)`, transición de 240ms mediante `cubic-bezier(.34,1.56,.64,1)`, y halo `box-shadow` circular de `0 0 0 4px rgba(109,74,224,.14)`.
*   **Tooltip/Etiqueta**: "→ El Nexo", tipografía Caveat de 14px, retardo de aparición de 250ms.
*   **Foco Accesible**: `outline: 2px dashed var(--jd-violet); offset: 3px`
*   **Accesibilidad de Movimiento**: En el modo de movimiento reducido (`prefers-reduced-motion: reduce`), se anula la transformación de escala (*scale*), aplicando únicamente la transición de opacidad.
*   **Atributo ARIA**: `aria-label="Traverser vers El Nexo"`

#### 4. Cara 3: El Chat (Tercera Cara - Sínodo) [116]
*   **Glifo**: SVG de burbuja de diálogo monocromo, tamaño 20px, sin emojis.
*   **Estilo Visual**: Tematización brutalista del Nexo para ambos mundos.
*   **Estado de Reposo**: `opacity: 0.45`.
*   **Estado Activo/Hover/Focus**: `opacity: 1`, con la etiqueta "→ CHAT" posicionada en la zona inferior en tipografía IBM Plex Mono de 10px.
*   **Destino Doctrinal**: `http://soberano.[HOST_TAILNET_REDACTADO]:8080` (MagicDNS constante de compilación).  <!-- guardia:permitir destino-doctrinal-con-host-tailnet-ya-redactado -->
*   **Foco Accesible**: `outline: 1px solid var(--nx-phosphor); offset: 2px`
*   **Reciprocidad**: La navegación de retorno se gestiona exclusivamente a través de la tematización integrada de OpenWebUI, sin alterar el núcleo funcional de la aplicación.

---

### II. DIRECTRICES DE CONTINUIDAD, SIMPLIFICACIÓN Y SEPARACIÓN [117, 118]

1.  **Simplificación de Datos (Frecuencias y Visualización)** [117]:
    *   **Límite de Filas**: Los grupos de telemetría muestran un máximo de exactamente 7 filas de datos activos. Las filas adicionales permanecen colapsadas tras un control interactivo etiquetado como `▸ more`.
    *   **Alineación Numérica**: Todas las cifras de métricas y telemetría se alinean a la derecha utilizando la propiedad `font-variant-numeric: tabular-nums` para asegurar la legibilidad del ancho de los caracteres. Las unidades de medida se renderizan con opacidad atenuada.
    *   **Explicaciones**: La información de contexto teórica se despliega únicamente mediante clicks o interacción sobre iconos de ayuda de tipo `ⓘ`.
2.  **Cuarentena de Componentes e Integridad de Código** [118]:
    *   **Límite de Longitud**: Los nuevos componentes lógicos de la interfaz deben poseer un tamaño inferior o igual a 350 líneas de código. Los componentes que excedan esta frontera se fragmentarán mediante fisión binaria.
    *   **Manejo de Valores Nulos**: Queda estrictamente prohibido el uso del tipo genérico `any` en TypeScript o equivalentes tipados. La interfaz debe implementar comprobaciones estrictas de control ante valores null o undefined.
    *   **Límite de Frecuencia de Renderizado**: Se prohíbe el re-renderizado de celdas a una tasa superior a 1 vez por 100ms para mitigar la sobrecarga del hilo principal del navegador. Es obligatorio el uso de directivas de memorización de funciones y datos (`useMemo`, `useCallback`).
    *   **Dependencias Externas**: No se admite la importación de nuevas librerías. El visor de mapas y el grafo se implementan nativamente sobre Leaflet y force-graph.
    *   **Ecopuertos de Assets**: Todo contenedor destinado a la carga de assets gráficos (como fotos de plantas o streams de cámaras) debe poseer propiedades estricta de `aspect-ratio` y `object-fit: cover` o `contain` para evitar saltos de layout durante la carga.

---

### III. SISTEMA DE TOKENS DUPLEX (DUAL-THEME) [119, 120]

La interfaz unifica la paleta mediante un único archivo de configuración `tokens.css` estructurado en dos ámbitos selectores exclusivos: `[data-theme="nexo"]` y `[data-theme="jardin"]`. Queda prohibido declarar colores hexadecimales de forma directa en los componentes fuera de estas variables [119, 120].

#### 1. Tipografías Autorizadas (Fuentes Locales) [119, 120]
*   **Ámbito: El Nexo** [119]:
    *   *Dato, Chips, Botones y Feeds*: `IBM Plex Mono` (Pesos: 400, 500, 600). Cuerpo base de 13px con interlineado de 1.55 y espaciado de letras 0.01em. Los chips y botones se renderizan a 11px, peso 600, espaciado de de 0.14em en mayúsculas (*uppercase*). Texto micro de 10px, peso 500, espaciado de 0.2em.
    *   *Wordmark y Títulos de Página*: `Cinzel` (Peso: 600). Tamaño de 22–28px con espaciado de letras 0.35em en mayúsculas. Queda prohibido su uso para visualización de telemetría o datos tabulares.
*   **Ámbito: Le Jardin** [120]:
    *   *Títulos de Sección*: `Cormorant Garamond` (Pesos: 500, 600), tamaño 34px, interlineado 1.2, espaciado 0.01em.
    *   *Nombres de Especies*: `Cormorant Garamond` (Peso: 600), tamaño 24px.
    *   *Cuerpo de Notas y Cahier*: `EB Garamond` (Pesos: 400, 500), tamaño 17px, interlineado 1.65. Las citas y taxonomías botánicas se configuran obligatoriamente en estilo itálica.
    *   *Acentos Manuales y Tooltips*: `Caveat` (Peso: 500), tamaño 15–16px. Reservado para tinteros de guardado y mensajes del sistema.
    *   *Métricas y Capas Técnicas*: `Inter` (Pesos: 400, 500), tamaño 12px con alineación `tabular-nums` y espaciado de 0.02em.

#### 2. Paleta de Colores: El Nexo (Brutalismo Soberano) [121, 122]
*   `--nx-void`: `#060B09` (Fondo de página base)
*   `--nx-panel`: `#0A120E` (Fondo de celda)
*   `--nx-panel-2`: `#0D1713` (Bloque de comandos)
*   `--nx-border`: `#1E3A2A` (Borde de contraste de 1px)
*   `--nx-border-dim`: `#12261C` (Borde atenuado)
*   `--nx-text`: `#C8E6D5` (Color de texto de datos)
*   `--nx-text-dim`: `#6E8A7C` (Color de unidades y textos de ayuda)
*   `--nx-text-ghost`: `#55705F` (Color para placeholders y estados de NO DATA)
*   `--nx-phosphor`: `#43F5A0` (Verde primario de estado óptimo o activo)
*   `--nx-phosphor-dim`: `#2E8F63` (Verde secundario atenuado)
*   `--nx-amber`: `#FFB454` (Ámbar de advertencia, estado stale o espera de firma)
*   `--nx-danger`: `#FF5C5C` (Rojo de peligro, fallo crítico o desbordamiento térmico)

##### Colores de Identidad del Sínodo (Indicador Circular + Borde de 2px en Tarjetas) [122]:
*   **Monje**: `#43F5A0`
*   **Vocero**: `#4CC9F0`
*   **Berserker**: `#FF5C5C`
*   **Escriba**: `#FFB454`
*   **Alquimista**: `#5C7CFF`
*   **Enlace**: `#7FD1E8`
*   *Regla de Sombras*: Quedan prohibidas las sombras suavizadas o difusas. El único sombreado permitido es el contorno estricto mediante `box-shadow: 0 0 0 1px var(--nx-border)`. El efecto visual de incandescencia o glow se limita exclusivamente a `text-shadow: 0 0 8px rgba(67,245,160,.35)` en cifras numéricas vivas de alta relevancia [122].
*   *Geometría*: Radio de borde de 0px universal para todos los contenedores y marcos del Nexo. Se autoriza un corte diagonal de diseño (*clip-path*) de 10px en la esquina superior izquierda de las cabeceras de celdas [122].
*   *Filtros*: Queda prohibido el uso de filtros gráficos por hardware en el Nexo [122].

#### 3. Paleta de Colores: Le Jardin (Anime Solarpunk) [123]
*   `--jd-bois-1`: `#EAD9B8` (Madera clara)
*   `--jd-bois-2`: `#DEC9A0` (Madera de transición)
*   `--jd-page`: `#F3EAD8` (Fondo de sección)
*   `--jd-parchemin`: `#F8F1E2` (Fondo de fichas, cartas e interfaces de lectura)
*   `--jd-encre`: `#2B2117` (Tinta oscura para texto primario)
*   `--jd-encre-dim`: `#6B5C49` (Tinta atenuada)
*   `--jd-fantome`: `#8A7B63` (Gris tenue de sensor ausente o "capteur à venir")
*   `--jd-violet`: `#6D4AE0` (Violeta primario de control, foco y base de grafo)
*   `--jd-violet-fonce`: `#4C1D95` (Color de aristas y énfasis del grafo)
*   `--jd-cyan-bio`: `#58D6C9` (Acento de bioluminiscencia limitado a un máximo de 10% del layout)
*   `--jd-magenta-doux`: `#E28FD8` (Acento complementario limitado a un máximo de 10% del layout)
*   `--jd-or-bougie`: `#D9A441` (Dorado de telemetría viva y éxitos de ritos)
*   `--jd-vert-ombre`: `#4E6E4E` (Verde para estado botánico e indicador de salud de plantas)
*   `--jd-mal`: `#C25E5E` (Rojo suave para fallos y maux en Le Jardin)
*   *Regla de Sombras*: Se definen de forma estricta dos capas de profundidad mediante sombreado de contraste sepia: `box-shadow: 0 2px 6px rgba(60,42,20,.12), 0 12px 28px rgba(60,42,20,.10)` [123].
*   *Geometría*: Radio de borde de 14px para cartas y fichas de pergamino; radio de 22px para burbujas de diálogo y notas flotantes; radio de 50% para contenedores circulares de tinta o tinteros [123].
*   *Filtros*: Se permite de forma exclusiva el uso de `backdrop-filter: blur(8px) saturate(1.1)` únicamente en paneles flotantes sobrepuestos de la interfaz (tinteros, libro de herbario abierto o el visor de la mascota) [123].

---

### IV. ANATOMÍA FÍSICA DE LAS INTERFACES [125-132]

#### 1. La Celda Hexagonal del Nexo [125]
La celda hexagonal actúa como el módulo de contención de la interfaz de telemetría y estado:
*   **Fondo**: `var(--nx-panel)`
*   **Borde**: `1px solid var(--nx-border)`
*   **Esquinas**: Rectas, con un radio de borde de 0px [125].
*   **Corte Superior Izquierdo**: Efecto de `clip-path` diagonal de exactamente 10px en la cabecera [125].
*   **Cabecera de Celda**: Altura fija de 40px. Muestra un glifo de control de colapso de tipo `▸` o `▾` en color `--nx-phosphor-dim`. El título de la celda se configura en 11px, peso 600, espaciado de letras 0.14em en mayúsculas [125]. A la derecha, muestra un chip que declara la frecuencia de datos del bus de sensores.
*   **Estado Colapsado**: La celda colapsada debe mostrar su cabecera y una única línea de resumen que sintetice el estado actual. Queda prohibido renderizar un panel vacío [125].
*   **Estado de Alerta/Fallo**: El color de borde conmuta de forma automática a `var(--nx-amber)` (alerta) o `var(--nx-danger)` (fallo) [125].

#### 2. Las Cartas del Signature Tray [127]
El Signature Tray organiza el flujo de validación criptográfica de parches, scripts y propuestas lógicas. Cada carta se estructura bajo las siguientes normas [127]:
*   **Fila de Identidad**: Contiene chips de estado con radio de borde de 2px, tamaño de 10px, peso 600, espaciado 0.14em en mayúsculas: *Abierto/Pendiente* (ámbar), *Firmado* (`--nx-phosphor-dim`), *Completado* (`--nx-phosphor`), o *Descartado* (`--nx-danger`).
*   **Título**: Tamaño 13px, peso 600 en mayúsculas. Justo debajo se incluye el campo descriptivo "Why" en 12px, estilo itálica y en color `--nx-text-dim` limitado a una sola línea [127].
*   **Origen/Destino**: Dos filas independientes que especifican la ruta del nodo y el repositorio (`nodo:ruta`) en tamaño 12.5px [127].
*   **Bloque de Comandos (Commands)**: Contenedor con fondo `--nx-panel-2`, borde izquierdo decorativo de `2px solid var(--nx-phosphor)`, relleno interno de 12px, tipografía `IBM Plex Mono` de 12.5px. Se incluye un botón interactivo "COPY" (10px, peso 600, espaciado 0.2em, radio 0px) que realiza inversión de color al hover y muestra el aviso "COPIED ✓" durante 1.5s tras activarse [127].
*   **Bloque de Verificación (Verification)**: Idéntico al bloque de comandos pero con un borde izquierdo de `2px solid var(--nx-amber)`. La primera línea detalla el comando de validación y la segunda muestra de manera estricta el resultado esperado etiquetado como `EXPECT ▸ <salida esperada>` en color ámbar atenuado. Queda prohibida la publicación de cartas de comandos que carezcan de este bloque [127].
*   **Acciones**: Botones inferiores de control con radio de borde de 0px, tamaño 11px, peso 600, espaciado 0.14em en mayúsculas que realizan inversión de color en el hover (`SIGN` y `DISCARD`) [127].

#### 3. Le Cahier (Página de Escritura del Diario) [130]
*   **Distribución de Layout**: Grid de dos columnas `grid-template-columns: minmax(420px, 1.2fr) .8fr` con una separación de 32px [130]. En viewports inferiores a 768px, el diseño se despliega en una única columna.
*   **Columna del Editor**:
    *   *Superficie de Escritura*: Carta de pergamino con un tramado de líneas de cuaderno horizontales mediante gradiente lineal repetitivo `repeating-linear-gradient(transparent 0 33px, rgba(43,33,23,.08) 33px 34px)`. Contenedor editable nativo (`contentEditable`) con color de cursor de texto `var(--jd-violet)`, color de texto de tinta `var(--jd-encre)` y tipografía `EB Garamond` de 17px [130].
    *   *Controles de Tintero*: Botones circulares de 48px con etiquetas inferiores en tipografía `Caveat` de 14px. El tintero "Garder" representa la acción de guardado local en el diario (tinta verde); el tintero "Mémoire" representa la acción de consolidación semántica (tinta violeta) [130].
    *   *Persistencia*: El tintero "Garder" envía de forma síncrona una petición HTTP POST a la ruta `/api/jardin/notes` del gateway local, utilizando el búfer `localStorage` únicamente como almacenamiento temporal offline de contingencia con reconciliación de datos automática al arranque [130].

#### 4. L'Herbier (Grimorio de Plantas) y la Tira Deslizable [131]
*   **Tira Deslizable de Iconos**:
    *   *Contenedor*: `display: flex; overflow-x: auto; scroll-snap-type: x mandatory; gap: 16px; padding: 8px 48px;` [131].
    *   *Máscaras Laterales*: Gradiente de transparencia en los bordes para difuminar el contenido deslizable: `mask-image: linear-gradient(90deg, transparent, #000 48px, #000 calc(100% - 48px), transparent)` [131].
    *   *Ficha de Icono*: Contenedor de 96×112px de pergamino con radio de borde de 14px. El icono de la especie botánica posee dimensiones de 56px (`object-fit: contain`). Al hover, se ejecuta una traslación de `translateY(-4px)` en 180ms y se incrementa el sombreado [131]. La ficha seleccionada se resalta mediante un contorno estricto `box-shadow: 0 0 0 2px var(--jd-violet)`. Al hacer clic, la ficha botánica detallada entra deslizándose desde el lateral derecho [131].
*   **Mascota Flotante (Savoir Plus)**:
    *   *Posición*: Botón de interacción circular fijo de 64px de diámetro posicionado en `fixed; bottom: 24px; left: 24px; z-index: 800;` [131].
    *   *Panel de Diálogo*: Al pulsar sobre la mascota, se abre un panel flotante de 360×480px anclado sobre su posición: fondo pergamino translúcido `rgba(248,241,226,.86)`, filtro de desenfoque de fondo por hardware `backdrop-filter: blur(8px) saturate(1.1)`, borde perimetral de `1px solid rgba(109,74,224,.35)` y radio de borde de 18px [131].
    *   *Inyección de Contexto*: El Context Provider del sistema inyecta automáticamente los identificadores de la planta activa seleccionada (`plantId`) en el sistema del preceptor local, forzando a que las consultas del chat se limiten estrictamente a esa especie vegetal [131].

#### 5. La Sentinelle (Cámaras de Seguridad) [132]
*   **Visor de Video**: Ecopuerto con una relación de aspecto de 4:3, un ancho controlado mediante `width: min(420px, 100%)` y recorte de borde de 14px con propiedad `object-fit: cover`. Al hacer clic sobre el visor, se activa el escalado a pantalla completa mediante la API Fullscreen nativa del navegador. Provee botones minimalistas de control "Plein écran" y "Photo" [132].
*   **Capa de Telemetría Superpuesta**: Franja informativa inferior con fondo semitransparente oscuro `rgba(20,14,8,.55)` y filtro de desenfoque de fondo `backdrop-filter: blur(4px)`. Despliega cuatro chips informativos en tipografía Inter de 12px con alineación `tabular-nums`: Température · Humidité · Lumière · pH [132].
*   **Indicador de Valor Real**: Los datos medidos se visualizan en color `--jd-or-bougie`, peso de texto de 600 y un resplandor luminoso estático `text-shadow: 0 0 6px rgba(217,164,65,.35)` [132].
*   **Ausencia de Señal**: Si la telemetría del ESP32 se interrumpe, el indicador conmuta de forma automática al estado de sensor ausente "— · capteur à venir" [132].
*   **Consumo de Bus**: La ingesta de datos del microcontrolador ESP32 se realiza mediante un canal asíncrono limitado a un máximo de 10Hz hacia el DOM, garantizando que el refresco de las métricas no interfiera en la suavidad de las animaciones del navegador [132].

---

### V. EL REGISTRO DE LOS SEIS ESTADOS OFICIALES DEL DATO [160, 181]

Para evitar el falseamiento de lecturas y garantizar la honestidad absoluta en pantalla, el modelo de datos de telemetría de los repositorios no acepta inferencias ni aproximaciones numéricas libres de red. Cada indicador se mapea bajo un StateFlow tipado que responde a los 6 estados de visualización rigurosos [160, 181]:
1.  **LIVE**: Dato fresco, medido y recibido en los últimos <30s. Se renderiza en verde `--nx-phosphor` [181].
2.  **STALE**: Dato recibido previamente pero sin refresco durante >30s. Se pinta en color ámbar para denotar desfase, manteniendo el último valor conocido y el timestamp del fallo en lugar de vaciar la interfaz [181].
3.  **STATIC**: Dato de naturaleza estable, manual o cacheado (ej. límites teóricos de las baterías o configuración de hardware) [181].
4.  **SIMULATED**: Datos de marcador de posición (*placeholder*) o demostración de desarrollo. Marcados visiblemente en interfaz con un indicador literal de simulación [181].
5.  **NO_DATA**: El sensor nunca ha emitido ninguna lectura desde el inicio del sistema. Se renderiza con un guion tipográfico (—) y la leyenda *capteur à venir* en tipografía itálica Inter de 12sp, en color `--jd-fantome` para el jardín, o una caja vacía de altura fija `--nx-text-ghost` para el Nexo. Se rinde automáticamente a los 1500ms si no hay payload [181].
6.  **ERROR**: Sensor en estado de fallo de hardware o circuito bloqueado [181].

---

### VI. TRANSICIONES, EFECTOS AMBIENTALES Y LEY DE DETALLE (LOD) [128, 134, 183, 184]

1.  **Transiciones del Nexo**: La interfaz del Nexo se rige bajo la premisa de cero animaciones de entrada para optimizar el rendimiento de la CPU ARM de bajo consumo. Los cambios de estado de celdas y widgets se realizan de forma instantánea o mediante transiciones de opacidad limitadas a un máximo de 80ms con curva de aceleración lineal (`transition: 80ms linear`) [133].
2.  **Transiciones de Le Jardin**: Toda transición en Le Jardin se ejecuta imitando el comportamiento de fluidos naturales y tinta, con propósito y sin ciclos repetitivos [134]:
    *   *Revelado de Sección (Viewport)*: Duración 240ms, curva ease-out, traslación vertical de `translateY(8px)` → 0 y opacidad de 0 → 1.
    *   *Apertura del Cahier (Libro de Notas)*: Duración 480ms, curva `cubic-bezier(.22,1,.36,1)`, perspectiva visual de 1200px y rotación espacial `rotateY(-18deg)` → 0 acompañada del escalado de sombreado de fondo. Al finalizar la animación, el sistema lanza de forma automática el foco en el editor.
    *   *Cierre de Libro*: Duración 360ms, ejecuta la animación inversa de la apertura.
    *   *Despliegue de Detalles de Nota (`<details>`)*: Duración de 220ms, interpolación de altura lineal combinada con una transición de opacidad de 120ms.
    *   *Transición de Ficha de Herbario*: Duración 320ms, curva ease-in-out, traslación horizontal de `translateX(24px)` → 0 acompañada de una ligera rotación angular `rotateZ(0.4deg)` → 0.
    *   *Pulsación de Tintero*: Duración 300ms, se genera una onda radial simulada mediante gradiente de tinta que se expande a escala de 0 a 1 con curva ease-out.
    *   *Despliegue de Panel de la Mascota*: Duración 260ms, se ejecuta una transición de resorte físico mediante curva `cubic-bezier(.34,1.56,.64,1)`.
    *   *Validación de Quiz / Rito*: Duración 200ms, se genera un pulso de color sobre el borde del contenedor (color `--jd-or-bougie` para acierto, color `--jd-mal` para error). Queda estrictamente prohibido el uso de confeti o efectos gráficos dinámicos distractores.
3.  **LOD (Ley de Detalle por Zoom) del Second Brain** [128]:
    *   *Nivel de Zoom < 0.8*: Se renderizan únicamente los nodos y las etiquetas de texto de los engramas fijados.
    *   *Nivel de Zoom 0.8 – 1.4*: Se muestran las etiquetas de texto solo si el nodo posee un grado de conectividad superior o igual a 4.
    *   *Nivel de Zoom > 1.4*: Se renderizan todas las etiquetas del grafo.
    *   *Interacción*: El hover sobre un nodo muestra siempre su etiqueta completa con un efecto de resplandor `text-shadow: 0 0 6px var(--nx-void)`. En caso de colisión física de renderizado entre etiquetas, el sistema oculta de manera automática la de menor grado de conectividad.
4.  **Sistema de Efectos Atmosféricos (Ambiente Activo - CMP)** [183, 184]:
    Se implementa una máquina de renderizado atmosférico controlada bajo el contrato `AmbientEffect` + `EffectRegistry` + `PerformanceWatchdog` con un interruptor de apagado global (*kill switch*) configurable en JSON. Los efectos se expresan en colores **no semánticos** (blanco, gris o cobre atenuado) para que nunca entren en colisión con la Ley del Color Semántico [183]. Los efectos son [184]:
    *   `PERLIN_MOSS` (Medium): Simplex noise (nunca funciones seno) generado mediante shaders nativos (AGSL o Skia) en las grietas del mármol. Está atado al repositorio de radiofrecuencia (`RfSignalRepository`). Si no hay señal (estado NO_DATA o STALE), el musgo se apaga o pasa a un color cobre apagado; nunca simula vida verde falsamente [184].
    *   `KEN_BURNS_DRIFT` (Light): Zoom y paneo suave de un 0.5% a 1% sobre las imágenes de fondo en un periodo de 60 a 90 segundos. Emplea dos capas de desplazamiento parallax [184].
    *   `SPECULAR_SWEEP` (Light): Barrido de luz diagonal en dirección arriba-izquierda hacia abajo-derecha, atado en tiempo real al voltaje/amperaje de `SolarChargeRepository` [184].
    *   `PARTICLES_DUST` (Light): Máximo 30 sprites de polvo flotante en pantalla con ciclos de velocidad y opacidad independientes [184].
    *   `VIGNETTE_BREATH` (Light): Gradiente de viñeta en los bordes de la pantalla que expande su escala y opacidad con una respiración constante de 8 a 10 segundos [184].
    *   `LAMP_THERMAL` (Light - Exclusivo de Jardin): Atado a la temperatura de la APU del Beelink (`SystemThermalRepository` leyendo el bus `k10temp` real). Si el procesador está por debajo del límite de seguridad (80°C), proyecta una calidez de cobre atenuado en el fondo. Si supera el umbral del guard, cambia a un régimen de ámbar parpadeante (alerta de calentamiento físico) [184].

---

### VII. REGLAS DE EMERGENCIA Y CONTROLES CRÍTICOS [1, 137]

#### 1. Modo de Ahorro de Carbono (Reflejo de Batería Solar) [137]
Cuando el gateway de FastAPI del rack físico reporta que la tensión de las baterías ha descendido por debajo del umbral óptimo de generación de Le Jardin, o se detecta que el nodo opera bajo el suministro del sistema de alimentación ininterrumpida (UPS en modo On Battery), se activa la directiva global `.mode-ahorro` en la etiqueta `<body>` de los navegadores, forzando las siguientes mutaciones inmediatas en las interfaces [137]:
*   **El Nexo** [137]:
    *   *Banner de Alerta*: Se despliega un banner superior de aviso de 28px de altura en color ámbar con el mensaje "ON BATTERY · batch queue paused", acompañado de un parpadeo de advertencia de 1s de frecuencia.
    *   *Anulación de Brillos*: Se desactivan de forma inmediata todos los efectos de resplandor de texto (`text-shadow`) e iluminación de cifras de telemetría en pantalla.
    *   *Mapa Unificado*: El visor de mapas suspende la recarga de tiles de mapa, mostrando en su lugar el chip de aviso "tiles paused".
    *   *Cola de Procesamiento*: Las peticiones de inferencia pesadas y tareas por lotes del preceptor local se encolan automáticamente en el buffer local, bloqueando su ejecución para enfriar el procesador.
*   **Le Jardin des Ombres** [137]:
    *   *Banner de Alerta*: Se muestra una cinta informativa en el Cahier con el mensaje en francés "La lanterne baisse — le jardin économise sa lumière", con una oscilación lenta de opacidad de 3s de frecuencia.
    *   *Filtro de Atenuación / Comportamiento Decorativo (Corregido)*: El elemento `<body>` **no** recibe el filtro de brillo en la implementación física real. En su lugar, el estado de ahorro de energía **pausa los hilos y desvanece los bucles mediante `animation-play-state: paused` + `opacity: 0`** aplicados estrictamente sobre los contenedores hijo del ambiente, con una transición lineal de **400ms** [1].
    *   *Efecto Visual de la Mascota*: La mascota flotante cambia su sprite visual para mostrar el glifo de la linterna de emergencia [137].

#### 2. Duraciones de Ambiente Detalladas (Mapeo Fiel) [2, 3]

##### El Muro (Nexo · placaa.webp) [2]:
*   **Neones cian hielo (`.neon.n1-.n6`)**: Ciclos variables de **7s / 11s / 13s** superpuestos de forma exacta sobre los bordes físicos de la fotografía [2].
*   **God-rays diagonales (`.godray`, `.godray.r2`)**: Tiempos de **107s / 79s** proyectados desde la esquina superior izquierda [2].
*   **Viento en hiedra (`.hiedra.h1/.h2/.h3`)**: Balanceo lateral de **13s / 17s / 19s** [2].
*   **Hojas temblando (`.hoja` - 13 instancias)**: Vibraciones estocásticas breves de entre **2.7s y 3.9s** [2].
*   **Barrido de luz mármol (`.sweep`)**: Desplazamiento rasante horizontal de **37s** [2].
*   **Polen dorado (`.polvo` - 14 instancias)**: Flotación pasiva de **11s** de duración dentro del espectro del haz de luz [2].

##### El Laboratorio (Jardin · placab.webp) [3]:
*   **Cielo crepuscular (`.cielo`)**: Respiración lumínica de **23s** confinada a la puerta exterior [3].
*   **Luna (`.luna`)**: **DISPLAY: NONE (Enterrada)** [3].
*   **Luz violeta naciente (`.lab-ambiente::after`)**: Barrido angular de ±7° de **29s** originándose desde la esquina inferior derecha [3].
*   **Halos de vela (`.halo.v1-.v4`)**: Parpadeo asíncrono con ciclos primos de **1.7s / 2.9s / 4.3s / 5.3s** sobre las llamas reales [3].
*   **Chispas ascendentes (`.chispa` - 8 instancias)**: Elevación lineal de **4.7s a 7.1s** [3].
*   **Cofre dorado (`.cofre-brillo`)**: Destello concentrado con un periodo de **8s** [3].
*   **Pociones vivas (`.pocion.am/.te/.vi`)**: Ciclos independientes de **7.9s / 9.7s / 11.3s** en las repisas [3].

---

### VIII. ALTAR CENTRAL, SCREENSHOT TESTING Y SEGURIDAD NATIVA [161, 186, 187, 192, 193]

#### 1. El Altar Central y el Hero Status Orb [182, 195]
La interfaz se organiza como un instrumento científico y un altar contemplativo, situando en el centro el **Hero Status Orb** [182]:
*   **Estado Normal (Heartbeat)**: El Orb no se oculta del todo; late de forma sutil en verde `--nx-phosphor` con baja opacidad (10%), mostrando en su centro el timestamp de ejecución del último ciclo de telemetría de PerformanceWatchdog. El sistema vivo se ve vivo [182].
*   **Estado Alerta / Activo**: El Orb escala de forma instantánea al 100% mediante una transición de `spring()` (sin rebotes decorativos), exponiendo el dato crítico del fallo o temperatura en color phosphor #43F5A0 o alerta ámbar, legible a 2 metros de distancia [182].
*   **Estado NO_DATA**: El Orb parpadea en color ámbar con el timestamp del último avistamiento (*last_seen*) [182].
*   **Inner Glow Determinista**: Queda prohibido el uso de `shadow()` difuso para simular el brillo del Orb. El resplandor interno se logra exclusivamente pintando un `Brush.radialGradient` dentro de la máscara circular recortada [182].

#### 2. Las Cuatro Zonas de Seguridad Inmutables [192]
*   **Centro Sagrado (40% ancho × 50% alto)**: **Verdadero Espacio Negativo**. Queda estrictamente prohibida la colocación de widgets permanentes, tarjetas o carousels. Este espacio se reserva para respiración del arte del fondo y la visualización del Orbe central [192].
*   **Zona Superior (15% alto)**: Reservada exclusivamente para el cabecero fijo (Header) y para asegurar la visibilidad de la Plaqueta de Cobre del fondo [192].
*   **Zona Inferior (10% alto)**: Reservada para navegación minimalista o gestos táctiles del sistema [192].
*   **Bordes Laterales (20% en cada extremo)**: Áreas de identidad destinadas al anclaje de widgets de telemetría y datos [192].

#### 3. El Juez de Interfaz (Screenshot Testing) [161, 187]
Para impedir que cualquier cambio en las vistas de Compose rompa el canon visual o introduzca elementos no permitidos, el sistema despliega un validador automatizado en la suite de pruebas [187]:
*   **Mecánica**: Emplea `ComposeUiTest` con captura programática de imágenes de pantalla (*screenshot capture*) en breakpoints específicos de compilación de escritorio [187].
*   **Validaciones del Juez**:
    *   Ningún elemento interactivo o clickable puede invadir el **Centro Sagrado** (el espacio del Altar central reservado para el Orb) [187].
    *   Ningún elemento clickable puede pisar el **30% superior derecho** de la cabecera (zona reservada para la plaqueta física de cobre de la interfaz) [187].
    *   Comparación exacta de píxeles contra la imagen de referencia inmaculada [187].
*   **Ley de Integración**: Si las pruebas de captura de pantalla del Juez de Interfaz fallan o muestran una desviación visual no aprobada, **el script `verify_pow.sh` aborta el merge (exit code 1)**, denegando la subida de los archivos de Compose a la rama activa del repositorio [187].

---

METADATOS MEDALLION:
*  Tipo: CONSOLIDACION
*  Archivo que sustituye: NINGUNO (Unifica 6 fuentes visuales del original)
*  Versión: 2.0-Medallion-Visual
*  Fuentes base: blueprint-de-diseno-soberano-v1.4.md, medallon-dashboards-v2.md, fuente-2-depurada.md, fuente-3-depurada.md, especificacion-cmp-multidispositivo.md, capas-aurelius-jardin-v2.md, 08 ago extraer:
*  Conflictos resueltos: Consolidación y desduplicación de todo el canon de interfaz, tokens de CSS/Compose, duraciones de animación basadas en números primos y el Juez de Interfaz. Se resuelven las colisiones del modo de ahorro y animaciones de Le Jardin incorporando la corrección física del censo del 8 de agosto de 2026.
*  Ambigüedades pendientes: NINGUNA
*  Descartes principales: Se descartan por completo el glassmorphism, el shadow difuso y la luna de Le Jardin (luna display:none).
*  Notas de auditoría: NINGUNA
