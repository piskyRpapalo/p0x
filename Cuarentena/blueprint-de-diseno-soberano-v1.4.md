# BLUEPRINT DE DISEÑO SOBERANO v1.4
## EL NEXO Y LE JARDIN — CANON VISUAL Y DIRECTRICES DE INTERFAZ

Este documento establece las especificaciones técnicas obligatorias y el canon de estilo visual para las interfaces de usuario del nodo Soberano (El Nexo, Le Jardin des Ombres y el Dashboard Compose Multiplatform). El objetivo es optimizar el consumo de hardware local, asegurar el control de backpressure y garantizar la honestidad absoluta en la telemetría visual.

---

## 0. EL SWITCHER DE TRES CARAS (EL PUENTE)

El Puente es el componente de navegación global anclado permanentemente en la interfaz del sistema. Facilita la conmutación entre las tres vistas principales: El Nexo (Jardín), La Forja (Sínodo) y el Chat.

### 0.1. Especificación de Contenedor General
*   **Posición**: `fixed; top: 12px; left: 12px; z-index: 9999`
*   **Estructura**: Elemento `<nav id="puente">` con un diseño de tres caras alineadas en una fila (`display: flex; gap: 4px;`).
*   **Tamaño Táctil Mínimo**: `44×44 px` por cara.
*   **Reserva de Cabecera**: El contenedor de fondo adyacente debe poseer `padding-left: 160px` para evitar colisiones visuales de renderizado.
*   **Orden de Foco**: Encabeza el flujo secuencial de tabulación en el documento (`tabindex`).
*   **Idiomas de Interfaz**: Las etiquetas de texto descriptivas se configuran en inglés (EN) desde la interfaz del Nexo, en francés (FR) desde Le Jardin, y bajo la tematización del Nexo para el Chat.

### 0.2. Cara 1: El Nexo (Jardín)
*   **Glifo**: SVG hexagonal con contorno (`stroke`), tamaño `20px` y grosor de línea (`stroke-width`) fino.
*   **Color**: `--nx-phosphor` (#43F5A0).
*   **Estado de Reposo**: `opacity: 0.45`, sin efectos de sombra ni glow.
*   **Estado Activo/Hover/Focus**: `opacity: 1`, transición lineal de `120ms` (`transition: 120ms linear`), sin transformaciones de escala.
*   **Etiqueta**: `"→ LE JARDIN"`, tipografía `IBM Plex Mono` de `10px`, espaciado de letras `0.2em`, color `--nx-text-dim`.
*   **Foco Accesible**: `outline: 1px solid var(--nx-phosphor); offset: 2px`
*   **Atributo ARIA**: `aria-label="Cross to Le Jardin des Ombres"`

### 0.3. Cara 2: Le Jardin (El Nexo)
*   **Glifo**: SVG de hoja o vegetal monocromo, tamaño `22px`.
*   **Ficha/Fondo**: Botón circular con fondo pergamino (`background: var(--jd-parchemin)`), borde de `1px solid rgba(109,74,224,.35)` y `border-radius: 50%`.
*   **Estado de Reposo**: `opacity: 0.55`, con sombra estática de `0 2px 6px rgba(60,42,20,.12)`.
*   **Estado Activo/Hover/Focus**: `opacity: 1`, transformación de escala `transform: scale(1.06)`, transición de `240ms` mediante `cubic-bezier(.34,1.56,.64,1)`, y halo box-shadow circular de `0 0 0 4px rgba(109,74,224,.14)`.
*   **Tooltip/Etiqueta**: `"→ El Nexo"`, tipografía `Caveat` de `14px`, retardo de aparición de `250ms`.
*   **Foco Accesible**: `outline: 2px dashed var(--jd-violet); offset: 3px`
*   **Accesibilidad de Movimiento**: En el modo de movimiento reducido (`prefers-reduced-motion: reduce`), se anula la transformación de escala (`scale`), aplicando únicamente la transición de opacidad.
*   **Atributo ARIA**: `aria-label="Traverser vers El Nexo"`

### 0.4. Cara 3: El Chat (Tercera Cara - Sínodo)
*   **Glifo**: SVG de burbuja de diálogo monocromo, tamaño `20px`, sin emojis.
*   **Estilo Visual**: Tematización brutalista del Nexo para ambos mundos.
*   **Estado de Reposo**: `opacity: 0.45`.
*   **Estado Activo/Hover/Focus**: `opacity: 1`, con la etiqueta `"→ CHAT"` posicionada en la zona inferior en tipografía `IBM Plex Mono` de `10px`.
*   **Destino Doctrinal**: `http://soberano.[HOST_TAILNET_REDACTADO]:8080` (MagicDNS constante de compilación).
*   **Foco Accesible**: `outline: 1px solid var(--nx-phosphor); offset: 2px`
*   **Reciprocidad**: La navegación de retorno se gestiona exclusivamente a través de la tematización integrada de OpenWebUI, sin alterar el núcleo funcional de la aplicación.

---

## 1. DIRECTRICES DE CONTINUIDAD Y SIMPLIFICACIÓN

### 1.1. Continuidad Evolutiva
Toda la lógica de interfaz, diseño y tokens heredada de versiones previas se mantiene activa. Cualquier modificación de componentes debe registrarse como una desviación aditiva en los metadatos de control.

### 1.2. Simplificación de Datos
*   **Límite de Visualización**: Los grupos de telemetría muestran un máximo de exactamente `7 filas` de datos activos. Las filas adicionales permanecen colapsadas tras un control interactivo etiquetado como `▸ more`.
*   **Alineación Numérica**: Todas las cifras de métricas y telemetría se alinean a la derecha utilizando la propiedad `font-variant-numeric: tabular-nums` para asegurar la legibilidad del ancho de los caracteres. Las unidades de medida se renderizan con opacidad atenuada.
*   **Explicaciones**: La información de contexto teórica se despliega únicamente mediante clicks o interacción sobre iconos de ayuda de tipo `ⓘ`.

### 1.3. Cuarentena de Componentes e Integridad de Código
*   **Límite de Longitud**: Los nuevos componentes lógicos de la interfaz deben poseer un tamaño inferior o igual a `350 líneas` de código. Los componentes que excedan esta frontera se fragmentarán mediante fisión binaria.
*   **Manejo de Valores Nulos**: Queda estrictamente prohibido el uso del tipo genérico `any` en TypeScript o equivalentes tipados. La interfaz debe implementar comprobaciones estrictas de control ante valores `null` o `undefined`.
*   **Límite de Frecuencia de Renderizado**: Se prohíbe el re-renderizado de celdas a una tasa superior a `1 vez por 100ms` para mitigar la sobrecarga del hilo principal del navegador. Es obligatorio el uso de directivas de memorización de funciones y datos (`useMemo`, `useCallback`).
*   **Dependencias Externas**: No se admite la importación de nuevas librerías. El visor de mapas y el grafo se implementan nativamente sobre Leaflet y force-graph.
*   **Ecopuertos de Assets**: Todo contenedor destinado a la carga de assets gráficos (como fotos de plantas o streams de cámaras) debe poseer propiedades estricta de `aspect-ratio` y `object-fit: cover` o `contain` para evitar saltos de layout durante la carga.

---

## 2. SISTEMA DE TOKENS DUPLEX (DUAL-THEME)

La interfaz unifica la paleta mediante un único archivo de configuración `tokens.css` estructurado en dos ámbitos selectores exclusivos: `[data-theme="nexo"]` y `[data-theme="jardin"]`. Queda prohibido declarar colores hexadecimales de forma directa en los componentes fuera de estas variables.

### 2.1. Tipografías Autorizadas (Fuentes Locales)

#### Ámbito: El Nexo
*   **Dato, Chips, Botones y Feeds**: `IBM Plex Mono` (Pesos: 400, 500, 600).
    *   *Especificaciones*: Cuerpo base de `13px` con interlineado de `1.55` y espaciado de letras `0.01em`. Los chips y botones se renderizan a `11px`, peso `600`, espaciado de `0.14em` en mayúsculas (`uppercase`). Texto micro de `10px`, peso `500`, espaciado de `0.2em`.
*   **Wordmark y Títulos de Página**: `Cinzel` (Peso: 600).
    *   *Especificaciones*: Tamaño de `22–28px` con espaciado de letras `0.35em` en mayúsculas. Queda prohibido su uso para visualización de telemetría o datos tabulares.

#### Ámbito: Le Jardin
*   **Títulos de Sección**: `Cormorant Garamond` (Pesos: 500, 600), tamaño `34px`, interlineado `1.2`, espaciado `0.01em`.
*   **Nombres de Especies**: `Cormorant Garamond` (Peso: 600), tamaño `24px`.
*   **Cuerpo de Notas y Cahier**: `EB Garamond` (Pesos: 400, 500), tamaño `17px`, interlineado `1.65`. Las citas y taxonomías botánicas se configuran obligatoriamente en estilo itálica.
*   **Acentos Manuales y Tooltips**: `Caveat` (Peso: 500), tamaño `15–16px`. Reservado para tinteros de guardado y mensajes del sistema.
*   **Métricas y Capas Técnicas**: `Inter` (Pesos: 400, 500), tamaño `12px` con alineación `tabular-nums` y espaciado de `0.02em`.

### 2.2. Paleta de Colores: El Nexo (Brutalismo Soberano)
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

#### Colores de Identidad del Sínodo (Indicador Circular + Borde de 2px en Tarjetas):
*   **Monje**: `#43F5A0`
*   **Vocero**: `#4CC9F0`
*   **Berserker**: `#FF5C5C`
*   **Escriba**: `#FFB454`
*   **Alquimista**: `#5C7CFF`
*   **Enlace**: `#7FD1E8`

*   **Regla de Sombras**: Quedan prohibidas las sombras suavizadas o difusas. El único sombreado permitido es el contorno estricto mediante `box-shadow: 0 0 0 1px var(--nx-border)`. El efecto visual de incandescencia o glow se limita exclusivamente a `text-shadow: 0 0 8px rgba(67,245,160,.35)` en cifras numéricas vivas de alta relevancia.
*   **Geometría**: Radio de borde de `0px` universal para todos los contenedores y marcos del Nexo. Se autoriza un corte diagonal de diseño (`clip-path`) de `10px` en la esquina superior izquierda de las cabeceras de celdas.
*   **Filtros**: Queda prohibido el uso de filtros gráficos por hardware.

### 2.3. Paleta de Colores: Le Jardin (Anime Solarpunk)
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

*   **Regla de Sombras**: Se definen de forma estricta dos capas de profundidad mediante sombreado de contraste sepia: `box-shadow: 0 2px 6px rgba(60,42,20,.12), 0 12px 28px rgba(60,42,20,.10)`.
*   **Geometría**: Radio de borde de `14px` para cartas y fichas de pergamino; radio de `22px` para burbujas de diálogo y notas flotantes; radio de `50%` para contenedores circulares de tinta o tinteros.
*   **Filtros**: Se permite de forma exclusiva el uso de `backdrop-filter: blur(8px) saturate(1.1)` únicamente en paneles flotantes sobrepuestos de la interfaz (tinteros, libro de herbario abierto o el visor de la mascota).

### 2.4. Grillas, Espaciados y Capas de Renderizado (Z-Index)
*   **Escala de Espaciado**: `4 / 8 / 12 / 16 / 24 / 32 / 48 / 64 px`
*   **Separación entre Celdas (Nexo)**: `16px` de separación constante.
*   **Aislamiento Térmico (Nexo)**: Separación vertical constante de `24px` para evitar densidades excesivas.
*   **Ritmo Vertical (Le Jardin)**: `64px` de margen vertical entre secciones de lectura.
*   **Separación Interna de Cartas (Le Jardin)**: `24px` de padding.
*   **Ancho Máximo del Contenedor (Nexo)**: Ocupa el ancho completo de pantalla (`full-bleed`) con padding de seguridad lateral de `24px`.
*   **Ancho Máximo del Contenedor (Le Jardin)**: Centrado horizontal fijo con un ancho máximo de `1120px`.
*   **Z-Index - Capa Base (Contenido)**: `1`
*   **Z-Index - Capa Media (Header de Celdas)**: `100`
*   **Z-Index - Capa Alta (Mascota Flotante/Overlays)**: `800`
*   **Z-Index - Capa Máxima (Modales de Confirmación)**: `900`
*   **Z-Index - El Puente (Switcher)**: `9999`
*   **Puntos de Interrupción (Breakpoints)**: `390px` (Móvil) · `768px` (Tablet) · `1280×800` (Pantalla de referencia del jardín) · `1440px` o superior (Expanded).

---

## 3. ANATOMÍA: EL NEXO (BRUTALISMO SOBERANO)

### 3.1. La Celda Hexagonal
La celda hexagonal actúa como el módulo de contención de la interfaz de telemetría y estado:
*   **Fondo**: `var(--nx-panel)`
*   **Borde**: `1px solid var(--nx-border)`
*   **Esquinas**: Rectas, con un radio de borde de `0px`.
*   **Corte Superior Izquierdo**: Efecto de clip-path diagonal de exactamente `10px` en la cabecera.
*   **Cabecera de Celda**: Altura fija de `40px`. Muestra un glifo de control de colapso de tipo `▸` o `▾` en color `--nx-phosphor-dim`. El título de la celda se configura en `11px`, peso `600`, espaciado de letras `0.14em` en mayúsculas. A la derecha, muestra un chip que declara la frecuencia de datos del bus de sensores.
*   **Estado Colapsado**: La celda colapsada debe mostrar su cabecera y una única línea de resumen que sintetice el estado actual. Queda prohibido renderizar un panel vacío.
*   **Estado de Alerta**: El color de borde conmuta de forma automática a `var(--nx-amber)` acompañado de un chip en el mismo tono.
*   **Estado de Fallo**: El color de borde conmuta de forma automática a `var(--nx-danger)`.

### 3.2. Formato de Estados Sin Datos (NO DATA)
Cuando un widget del Nexo se rinde al expirar el límite de tiempo de payload de `1500ms`, se genera un bloque visual de contingencia:
*   **Fondo**: `#0B0F0D`
*   **Borde**: `1px dashed var(--nx-border-dim)`
*   **Texto**: `"NO DATA"`, tipografía `IBM Plex Mono` de `12px`, peso `500`, espaciado de letras `0.2em`, color `--nx-text-ghost`, centrado horizontal y verticalmente en el contenedor. Si existe un registro histórico previo en el buffer local, se añade debajo el texto `"last seen: HH:MM"`.

### 3.3. Las Cartas del Signature Tray
El Signature Tray organiza el flujo de validación criptográfica de parches, scripts y propuestas lógicas. Cada carta se estructura bajo las siguientes normas:
*   **Fila de Identidad**: Contiene chips de estado con radio de borde de `2px`, tamaño de `10px`, peso `600`, espaciado `0.14em` en mayúsculas:
    *   *Abierto/Pendiente de Firma*: Color ámbar.
    *   *Firmado*: Color `--nx-phosphor-dim`.
    *   *Completado/Aplicado*: Color `--nx-phosphor`.
    *   *Descartado*: Color de peligro atenuado (`--nx-danger-dim`).
    *   *Metadata de Fecha*: A la derecha, se renderiza la fecha de actualización `"updated: YYYY-MM-DD"` en color `--nx-text-ghost`.
*   **Título**: Tamaño `13px`, peso `600` en mayúsculas utilizando el color `--nx-text`. Justo debajo, se incluye el campo descriptivo `"Why"` en `12px`, estilo itálica y en color `--nx-text-dim` limitado a una sola línea.
*   **Origen / Destino**: Dos filas independientes que especifican la ruta del nodo y el repositorio (`nodo:ruta`) en tamaño `12.5px`. El nodo emisor se encapsula en un chip de datos acompañado de un indicador circular de color semántico, usando el glifo `→` como separador visual entre filas.
*   **Bloque de Comandos (Commands)**: Contenedor con fondo `--nx-panel-2`, borde izquierdo decorativo de `2px solid var(--nx-phosphor)`, relleno interno de `12px`, tipografía `IBM Plex Mono` de `12.5px` y propiedad CSS `white-space: pre-wrap`. En la zona superior derecha del bloque se incluye un botón interactivo `"COPY"` (`10px`, peso `600`, espaciado `0.2em`, sin radio de borde) que realiza la inversión de colores al foco y muestra el aviso `"COPIED ✓"` durante `1.5s` tras activarse.
*   **Bloque de Verificación (Verification)**: Idéntico al bloque de comandos pero con un borde izquierdo de `2px solid var(--nx-amber)`. La primera línea detalla el comando de validación y la segunda muestra de manera estricta el resultado esperado etiquetado como `"EXPECT ▸ <salida esperada>"` en color ámbar atenuado. Queda prohibida la publicación de cartas de comandos que carezcan de este bloque de verificación.
*   **Acciones**: Botones inferiores de control con radio de borde de `0px`, tamaño `11px`, peso `600`, espaciado `0.14em` en mayúsculas que realizan inversión de color en el hover:
    *   *SIGN*: Botón con contorno (`outline`) de color `--nx-phosphor`.
    *   *DISCARD*: Botón con contorno de color `--nx-danger` que enruta el comando a la Necrópolis de software.

### 3.4. Telemetría, Sínodo y Second Brain
*   **System State**: Despliegue de datos en modo simplificado: un máximo de 7 líneas de datos visibles por grupo, ocultando el resto bajo el control interactivo `▸ more`.
*   **Cápsulas del Sínodo**: Los colores característicos de las voces de los monjes y agentes se aplican exclusivamente al indicador circular (`dot`) y al borde izquierdo de la tarjeta, dejando el cuerpo en color neutro. Las barras de progreso imprecisas se sustituyen por chips de datos con métricas numéricas reales y frescura del bus. Si un agente cae en estado de inactividad, se muestra el estado `"DEGRADED"` en un chip ámbar o `"STANDBY"` en texto atenuado.
*   **Mapa Unificado (Unified Map)**: Contenedor con altura dinámica regulada mediante `height: clamp(320px, 38vh, 520px)`. Leyenda interactiva colapsable. Explicaciones del estado del espectro encapsuladas tras el icono de Osiris `ⓘ`. Los controles de reinicio de la antena se configuran mediante botones de contorno en color ámbar (`RESTART AIS/ADS-B`). Los tiles oscuros de mapas se mantienen.
*   **Second Brain (Grafo de Conocimiento)**: Relación de aspecto de `16:9` con una altura máxima de `640px`. Implementación estricta de la Ley de Detalle por Zoom (LOD):
    *   *Nivel de Zoom < 0.8*: Se renderizan únicamente los nodos y las etiquetas de texto de los engramas fijados.
    *   *Nivel de Zoom 0.8 – 1.4*: Se muestran las etiquetas de texto solo si el nodo posee un grado de conectividad superior o igual a 4.
    *   *Nivel de Zoom > 1.4*: Se renderizan todas las etiquetas del grafo.
    *   *Interacción*: El hover sobre un nodo muestra siempre su etiqueta completa con un efecto de resplandor `text-shadow: 0 0 6px var(--nx-void)`. En caso de colisión física de renderizado entre etiquetas, el sistema oculta de manera automática la de menor grado de conectividad.
*   **Cabecera (Header)**: Reloj del huso horario de Portugal (Lisboa) en color `--nx-text` brillante, husos horarios de referencia alternativos en color `--nx-text-dim`. Muestra chips tipados correspondientes a las firmas del Códice local (`ED25519`, `PROOF`, `PRIVACY`). La miniatura de la cámara de seguridad exterior se realoja formalmente fuera del header de la página, habitando la celda de observación activa `"OBSERVE"`.

---

## 4. ANATOMÍA: LE JARDIN DES OMBRES (MAGIC-SOLARPUNK-ANIME)

### 4.1. El Mundo de Madera y Pergamino
Toda la interfaz del jardín se genera mediante CSS vanilla, quedando prohibido el uso de imágenes pesadas de textura de fondo para no sobrecargar el bus de memoria del hardware:
*   **Fondo de la Mesa (Fondo de Página)**: Generado mediante gradientes y repeticiones lineales:
    ```css
    background: radial-gradient(120% 90% at 50% 0%, rgba(255,246,224,.35), transparent 60%),
                repeating-linear-gradient(90deg, rgba(94,66,38,.06) 0 2px, transparent 2px 180px),
                repeating-linear-gradient(0deg, rgba(94,66,38,.03) 0 1px, transparent 1px 7px),
                linear-gradient(180deg, var(--jd-bois-1), var(--jd-bois-2));
    ```
*   **Cartas de Pergamino**: Fondo plano de color `var(--jd-parchemin)`, radio de borde de `14px`, marco exterior de `1px solid rgba(94,66,38,.14)` y sombra de profundidad sepia `var(--jd-ombre)`.
*   **Efecto de Cinta Adhesiva (Washi Tape)**: Elementos de pseudocódigo CSS `::before` y `::after` de tamaño `64×22px` con una rotación de `-45deg` (y `+45deg` en la esquina opuesta), color `rgba(255,255,255,.55)` y bordes discontinuos de `1px dashed rgba(94,66,38,.25)`.

### 4.2. Le Cahier (Página de Escritura del Diario)
*   **Distribución de Layout**: Grid de dos columnas `grid-template-columns: minmax(420px, 1.2fr) .8fr` con una separación de `32px`. En viewports inferiores a `768px`, el diseño se despliega en una única columna, desplazando el archivo de notas a la zona inferior.
*   **Columna del Editor**:
    *   *Superficie de Escritura*: Carta de pergamino con un tramado de líneas de cuaderno horizontales mediante gradiente lineal repetitivo `repeating-linear-gradient(transparent 0 33px, rgba(43,33,23,.08) 33px 34px)`. Contenedor editable nativo (`contentEditable`) con color de cursor de texto `var(--jd-violet)`, color de texto de tinta `var(--jd-encre)` y tipografía `EB Garamond` de `17px`.
    *   *Foco Activo*: Efecto de sombreado interno `box-shadow: inset 0 0 0 3px rgba(109,74,224,.12)`.
    *   *Selección de Texto*: Color de fondo de selección `rgba(109,74,224,.22)`.
    *   *Controles de Tintero*: Botones circulares de `48px` con etiquetas inferiores en tipografía `Caveat` de `14px`. El tintero `"Garder"` representa la acción de guardado local en el diario (tinta verde); el tintero `"Mémoire"` representa la acción de consolidación semántica (tinta violeta). Al pulsar, se activa una transición de onda radial `radial-gradient` de `0` a `1` en un periodo de `300ms` con curva de aceleración `ease-out`. El hover del cursor ejecuta una traslación suave de `translateY(-2px)` en `180ms`.
    *   *Persistencia*: El tintero `"Garder"` envía de forma síncrona una petición HTTP POST a la ruta `/api/jardin/notes` del gateway local, utilizando el búfer `localStorage` únicamente como almacenamiento temporal offline de contingencia con reconciliación de datos automática al arranque. El tintero `"Mémoire"` propone el fragmento de conocimiento en caliente para su validación por el preceptor local antes de inyectarse en el grafo.
*   **Columna de Archivo**:
    *   *Esquema del Second Brain*: Tarjeta pergamino tintada en color `#F2EDFB`, borde perimetral de `1px solid #D9CEF5` y altura fija de `320px`. Reutiliza el grafo de fuerza interactivo de la interfaz del Nexo, re-vestido con nodos en color `--jd-violet`, aristas en `rgba(109,74,224,.35)` y etiquetas en tipografía `Inter` de `11px` con color de tinta sepia.

### 4.3. L'Herbier (Grimorio de Plantas)
*   **Tira Deslizable de Iconos**:
    *   *Contenedor*: `display: flex; overflow-x: auto; scroll-snap-type: x mandatory; gap: 16px; padding: 8px 48px;`.
    *   *Máscaras Laterales*: Gradiente de transparencia en los bordes para difuminar el contenido deslizable: `mask-image: linear-gradient(90deg, transparent, #000 48px, #000 calc(100% - 48px), transparent)`.
    *   *Controles de Flechas*: Botones circulares de `36px` con fondo pergamino y sombreado estático sepia. Se fijan en los extremos laterales del contenedor y se ocultan de forma automática en dispositivos táctiles. Al hacer clic, se desplaza el carrusel un ancho completo de visor mediante `behavior: smooth`.
    *   *Ficha de Icono*: Contenedor de `96×112px` de pergamino con radio de borde de `14px`. El icono de la especie botánica posee dimensiones de `56px` y se escala mediante `object-fit: contain`. El nombre común de la planta se visualiza en tipografía `Cormorant Garamond` de `14px`. Al hover, se ejecuta una traslación de `translateY(-4px)` en `180ms` y se incrementa el sombreado de profundidad. La ficha seleccionada se resalta mediante un contorno estricto `box-shadow: 0 0 0 2px var(--jd-violet)`. Al hacer clic, la ficha botánica detallada entra deslizándose desde el lateral derecho.
*   **Savoir Plus (Mascota Flotante)**:
    *   *Posición*: Botón de interacción circular fijo de `64px` de diámetro posicionado en `fixed; bottom: 24px; left: 24px; z-index: 800;`.
    *   *Panel de Diálogo*: Al pulsar sobre la mascota, se abre un panel flotante de `360×480px` anclado sobre su posición: fondo pergamino translúcido `rgba(248,241,226,.86)`, filtro de desenfoque de fondo por hardware `backdrop-filter: blur(8px) saturate(1.1)`, borde perimetral de `1px solid rgba(109,74,224,.35)` y radio de borde de `18px`. La animación de entrada se configura mediante una transición física de resorte (`spring`) de `260ms` con curva `cubic-bezier(.34,1.56,.64,1)`.
    *   *Inyección de Contexto*: El Context Provider del sistema inyecta automáticamente los identificadores de la planta activa seleccionada en el sistema del preceptor local, forzando a que las consultas del chat se limiten estrictamente a esa especie vegetal.

### 4.4. La Sentinelle (Cámaras de Seguridad)
*   **Visor de Video**: Ecopuerto con una relación de aspecto de `4:3`, un ancho controlado mediante `width: min(420px, 100%)` y recorte de borde de `14px` con propiedad `object-fit: cover`. Al hacer clic sobre el visor, se activa el escalado a pantalla completa mediante la API Fullscreen nativa del navegador. Provee botones minimalistas de control `"Plein écran"` y `"Photo"`.
*   **Capa de Telemetría Superpuesta**: Franja informativa inferior con fondo semitransparente oscuro `rgba(20,14,8,.55)` y filtro de desenfoque de fondo `backdrop-filter: blur(4px)`. Despliega cuatro chips informativos en tipografía `Inter` de `12px` con alineación tabular-nums: `Température` · `Humidité` · `Lumière` · `pH`.
*   **Indicador de Valor Real**: Los datos medidos se visualizan en color `--jd-or-bougie`, peso de texto de `600` y un resplandor luminoso estático `text-shadow: 0 0 6px rgba(217,164,65,.35)`.
*   **Ausencia de Señal**: Si la telemetría del ESP32 se interrumpe, el indicador conmuta de forma automática al estado de sensor ausente `"— · capteur à venir"`.
*   **Consumo de Bus**: La ingesta de datos del microcontrolador ESP32 se realiza mediante un canal asíncrono limitado a un máximo de `10Hz` hacia el DOM, garantizando que el refresco de las métricas no interfiera en la suavidad de las animaciones del navegador.

---

## 5. TRANSICIONES Y MICRO-INTERACCIONES

### 5.1. Directriz de Animación del Nexo
La interfaz del Nexo se rige bajo la premisa de cero animaciones de entrada para optimizar el rendimiento de la CPU ARM de bajo consumo. Los cambios de estado de celdas y widgets se realizan de forma instantánea o mediante transiciones de opacidad limitadas a un máximo de `80ms` con curva de aceleración lineal (`transition: 80ms linear`). Los únicos elementos dinámicos permitidos son el parpadeo del indicador circular de estado (`blink 1.2s steps(2)` en estado degradado) y la oscilación del cursor de comandos.

### 5.2. Directriz de Animación de Le Jardin
Toda transición en Le Jardin se ejecuta imitando el comportamiento de fluidos naturales y tinta, con propósito y sin ciclos repetitivos innecesarios:

*   **Revelado de Sección (Viewport)**: Duración `240ms`, curva `ease-out`, traslación vertical de `translateY(8px) → 0` y opacidad de `0 → 1`.
*   **Apertura del Cahier (Libro de Notas)**: Duración `480ms`, curva `cubic-bezier(.22,1,.36,1)`, perspectiva visual de `1200px` y rotación espacial `rotateY(-18deg) → 0` acompañada del escalado de sombreado de fondo. Al finalizar la animación, el sistema lanza de forma automática el foco en el editor.
*   **Cierre de Libro**: Duración `360ms`, ejecuta la animación inversa de la apertura.
*   **Despliegue de Detalles de Nota (`<details>`)**: Duración de `220ms`, interpolación de altura lineal combinada con una transición de opacidad de `120ms`.
*   **Transición de Ficha de Herbario**: Duración `320ms`, curva `ease-in-out`, traslación horizontal de `translateX(24px) → 0` acompañada de una ligera rotación angular `rotateZ(0.4deg) → 0`.
*   **Pulsación de Tintero**: Duración `300ms`, se genera una onda radial simulada mediante gradiente de tinta que se expande a escala de `0` a `1` con curva `ease-out`.
*   **Despliegue de Panel de la Mascota**: Duración `260ms`, se ejecuta una transición de resorte físico mediante curva `cubic-bezier(.34,1.56,.64,1)`.
*   **Validación de Quiz / Rito**: Duración `200ms`, se genera un pulso de color sobre el borde del contenedor (color `--jd-or-bougie` para acierto, color `--jd-mal` para error). Queda estrictamente prohibido el uso de confeti o efectos gráficos dinámicos distractores.

### 5.3. Accesibilidad de Animación Global
El sistema implementa de forma obligatoria un cortafuegos de animaciones para usuarios con sensibilidad de movimiento utilizando la directiva CSS de accesibilidad:
```css
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation: none !important;
    transition: none !important;
    transform: none !important;
  }
}
```

---

## 6. REGLAS DE EMERGENCIA (HONEST SENSORS Y REFLEJOS)

### 6.1. Gestión de Estados Sin Datos (NO DATA)
La interfaz del sistema se rige por el principio inquebrantable de la honestidad de los sensores: un valor nulo o en blanco es preferible a una medición estimada o simulada. Ante la ausencia de payload físico de telemetría tras un intervalo continuo de `1500ms`, el sistema se rinde de forma automática y los widgets conmutan a las siguientes representaciones visuales neutrales:

*   **Mundo: Le Jardin**: Se muestra el guion tipográfico de sensor ausente `"— · capteur à venir"`, renderizado en tipografía `Inter` de `12px`, color de sensor ausente `--jd-fantome` en estilo itálica, bloqueando cualquier efecto de sombra o resplandor de datos.
*   **Mundo: El Nexo**: Se despliega la caja neutral de contingencia de `"NO DATA"` definida en la sección 3.2, mostrando la fecha y hora del último avistamiento válido si reside en el buffer local de Silver.

Queda prohibido el uso de cajas de carga intermitentes (skeletons) infinitas, el despliegue de valores por defecto de tipo cero (`0`) que induzcan a error de lectura, o la visualización de datos de telemetría obsoletos como si fuesen mediciones en tiempo real.

### 6.2. Modo de Ahorro de Carbono (Reflejo de Batería Solar)
Cuando el gateway de FastAPI del rack físico reporta que la tensión de las baterías ha descendido por debajo del umbral óptimo de generación de Le Jardin, o se detecta que el nodo opera bajo el suministro del sistema de alimentación ininterrumpida (UPS en modo On Battery), se activa la directiva global `.mode-ahorro` en la etiqueta `<body>` de los navegadores, forzando las siguientes mutaciones inmediatas en las interfaces:

*   **El Nexo**:
    *   *Banner de Alerta*: Se despliega un banner superior de aviso de `28px` de altura en color ámbar con el mensaje `"ON BATTERY · batch queue paused"`, acompañado de un parpadeo de advertencia de `1s` de frecuencia.
    *   *Anulación de Brillos*: Se desactivan de forma inmediata todos los efectos de resplandor de texto (`text-shadow`) e iluminación de cifras de telemetría en pantalla.
    *   *Mapa Unificado*: El visor de mapas suspende la recarga de tiles de mapa, mostrando en su lugar el chip de aviso `"tiles paused"`.
    *   *Cola de Procesamiento*: Las peticiones de inferencia pesadas y tareas por lotes del preceptor local se encolan automáticamente en el buffer local, bloqueando su ejecución para enfriar el procesador.
*   **Le Jardin des Ombres**:
    *   *Banner de Alerta*: Se muestra una cinta informativa en el Cahier con el mensaje en francés `"La lanterne baisse — le jardin économise sa lumière"`, con una oscilación lenta de opacidad de `3s` de frecuencia.
    *   *Filtro de Atenuación*: Se inyecta un filtro de atenuación general sobre el render del navegador mediante `filter: brightness(.92) saturate(.9)`, reduciendo el contraste y el brillo del color pergamino.
    *   *Efecto Visual de la Mascota*: La mascota flotante cambia su sprite visual para mostrar el glifo de la linterna de emergencia.

---

## 7. AUTOPSIA VISUAL Y HISTORIAL DE DESCARTES

Se documentan de forma explícita las decisiones de arquitectura de diseño adoptadas por el Soberano David, detallando el componente descartado, el motivo técnico de su remoción y su reemplazo:

*   **Marco de Neón Cian de Celdas (El Nexo)**: Descartado por competir visualmente con el contraste de los datos de telemetría. Reemplazado por borde sobrio de `1px` en tono `--nx-border`, reservando el glow exclusivamente a cifras numéricas activas vivas.
*   **Fondo Negro Plano de la Mesa (Le Jardin)**: Descartado por el operador humano por considerarlo poco integrador de la atmósfera botánica. Reemplazado por una estructura de madera y pergamino mediante CSS puro de gradientes y repeticiones lineales, con un peso nulo de carga de disco.
*   **Sopa de Etiquetas y Nodos (Second Brain)**: Descartado debido a que la acumulación de más de veinte nombres simultáneos convertía el grafo en un elemento de ruido decorativo ilegible. Reemplazado por la implementación estricta de la Ley de Detalle por Zoom (LOD), donde los nombres comunes solo se renderizan según la tasa de conectividad del nodo y el nivel de zoom físico de la pantalla.
*   **Barras de Progreso Lineales de Agentes (Sínodo)**: Descartadas por ser visualmente ambiguas e imprecisas. Reemplazadas por chips de bus con métrica única real e indicador circular de estado degradado o activo.
*   **Miniatura de la Cámara de Seguridad en el Header (El Nexo)**: Descartada debido a que el header debe ser un espacio reservado para la identidad, estado global y reloj del sistema, no para reproducción multimedia. Reemplazada mediante el realojamiento del visor en la celda de observación activa `"OBSERVE"` del panel.
*   **localStorage como Persistencia Única (Le Cahier)**: Descartada debido a que la soberanía de las anotaciones del diario no puede vivir expuesta en el perfil del navegador del cliente. Reemplazada por persistencia asíncrona robusta en el disco del rack del nodo mediante llamadas HTTP POST, dejando a `localStorage` únicamente la función de buffer de contingencia offline con reconciliación automática.
*   **Grilla Multicolumna Estática (L'Herbier)**: Descartada para evitar constantes re-maquetaciones y saltos de interfaz conforme la biblioteca botánica se escala con nuevas especies de plantas. Reemplazada por una tira horizontal deslizable con snaps de vista adaptable que crece de forma continua sin alterar el layout de la página.

---

## 8. NOTAS DE AUDITORÍA MEDALLION

MagicDNS no está activo en el nodo Beato. El tráfico real medido por SSH circula por http://[IP_TAILNET_REDACTADA]:8080. Ambas URLs coexisten: MagicDNS es la constante de build doctrinal; la IP es el dato de terreno medido.

--------------------------------------------------------------------------------

METADATOS MEDALLION:
*  Tipo: REEMPLAZO_ORIGINAL
*  Archivo que sustituye: BLUEPRINT DE DISEÑO SOBERANO v1.3
*  Versión: 1.4
*  Fuentes base: BLUEPRINT DE DISEÑO SOBERANO v1.3, capas-aurelius-jardin.md, especificacion-cmp-multidispositivo.md, FASE 2 REVISADA: APROBADA ✅, inventario-necropolis-v2.md, medallon-dashboards.md
*  Conflictos resueltos: Saneamiento del endpoint doctrinal MagicDNS frente a la IP real de Tailscale medida en caliente por SSH en Lisboa sin alterar la arquitectura visual de la constante de compilación. Unificación de los estados oficiales del dato y de las safe zones de la pantalla para evitar colisiones lógicas.
*  Ambigüedades pendientes: NINGUNA
*  Descartes principales: Se descarta cualquier automatización del portapapeles o copia automática, forzando la fricción de la selección manual (Ctrl+C) en el portapapeles soberano para auditoría obligatoria.
*  Notas de auditoría: MagicDNS inactivo en producción; la IP medida para open-webui en Beato es [IP_TAILNET_REDACTADA]:8080, coexistiendo con el host doctrinal.

--------------------------------------------------------------------------------

<<< FIN DOCUMENTO: BLUEPRINT DE DISEÑO SOBERANO v1.4.md >>>