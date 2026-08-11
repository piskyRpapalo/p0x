# ESPECIFICACIÓN CMP MULTIDISPOSITIVO · DASHBOARDS COHERENTES
## ARQUITECTURA DE SOFTWARE COMPOSE MULTIPLATFORM Y PAQUETE CLAVE · p0x
*Generado bajo los principios matemáticos y de metal de p0x*

---

### 1. MODELO DE DESPLIEGUE Y TARGET DE RENDIMIENTO
El sistema de dashboards unificados de **p0x (Hexelion y Le Jardin)** opera como una aplicación nativa escrita en **Kotlin** usando **Compose Multiplatform (CMP)** [183].
*   **Target Primario**: Desktop/JVM (x86_64) renderizado a través de la biblioteca **Skia nativa** integrada en Compose Desktop [116, 117]. Corre de forma ininterrumpida en el Soberano Principal (**Beelink SER9 Max**) y se proyecta en el panel táctil físico de pared [116, 198].
*   **Target Secundario (Futuro)**: Android nativo (ARM64). Toda la arquitectura de componentes y la lógica de repositorios de datos se mantiene desacoplada de dependencias específicas de plataforma para garantizar la portabilidad limpia al móvil en fases posteriores [116, 117].

---

### 2. ARQUITECTURA DE PAQUETES (ESTRUCTURA DE CÓDIGO) [108, 109]
El esqueleto del proyecto Compose Multiplatform sigue un diseño relacional estricto y desacoplado, libre de frameworks de terceros:

```plain
src/commonMain/kotlin/p0x/dashboard/
├── App.kt                          # Orquestador del ciclo de vida y WindowSizeClass [108]
├── theme/                          # Tokens visuales inmutables y adaptativos
│   ├── HexelionColor.kt            # Definiciones estáticas de tokens de color [109]
│   └── HexelionDimensions.kt       # Sizing Tokens calculados por tipo de pantalla [109]
├── data/                           # Repositorios de telemetría e interfaces defensivas
│   ├── SolarChargeRepository.kt    # Ingesta de paneles solares y tensión de batería [109]
│   ├── SystemThermalRepository.kt  # Telemetría de APU (La Fragua, Beelink) [109]
│   ├── RfSignalRepository.kt       # Datos de dongles SDR (ADS-B/AIS) [109]
│   └── SensorRepository.kt         # Sensores ambientales e ingestión de red [109]
├── viewmodel/                      # Máquina de estados unificada de la UI
│   └── DashboardViewModel.kt       # Control de transiciones de modos y flujos [109]
├── components/                     # Componentes visuales puros con 0px de radio de borde
│   ├── Header.kt                   # Cabecero fijo, esferas de control y zona vacía [108]
│   ├── HeroWidgets.kt              # Accesos directos: MAP, CAMERAS, SECOND BRAIN [109]
│   ├── CenterHeroOrb.kt            # Orbe de telemetría central e interactivo [109]
│   └── DataWidgets.kt              # Badges de solo-lectura y micro-métricas [109]
└── ambient/                        # Orquestación de efectos atmosféricos locales
    ├── EffectRegistry.kt           # Bus y capas de efectos registrados [109]
    ├── AmbientConfig.kt            # Configuraciones JSON de umbrales [109]
    ├── PerformanceWatchdog.kt      # Medidor de frames perdidos y kill switch [108, 109]
    └── effects/                    # Shaders y barridos de renderizado lineal
        ├── PerlinMossEffect.kt     # Musgo atado a señal RF (desactivable) [109, 116]
        ├── LampThermalEffect.kt    # Calidez térmica atada a temperatura de APU [109, 116]
        └── SpecularSweepEffect.kt  # Barrido de luz atado a amperaje de carga solar [109]
```

---

### 3. IMPLEMENTACIÓN DE TOKENS ADAPTATIVOS (DIMENSION SYSTEM) [188, 189]
Para erradicar los valores estáticos acoplados, se provee la clase `HexelionDimensions` a todo el árbol de Compose mediante un `CompositionLocal` de Kotlin, calculando el tamaño en tiempo de arranque basándose en el análisis de `WindowSizeClass` [188, 189]:

```kotlin
package p0x.dashboard.theme

import androidx.compose.runtime.staticCompositionLocalOf
import androidx.compose.ui.unit.Dp
import androidx.compose.ui.unit.TextUnit
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp

data class HexelionDimensions(
    val sphereSize: Dp,
    val sphereIconSize: Dp,
    val heroWidgetSizeMapa: Dp,
    val heroWidgetSizeSecondBrain: Dp,
    val heroWidgetSizeCamarasWidth: Dp,
    val heroWidgetSizeCamarasHeight: Dp,
    val dataBadgeWidth: Dp,
    val dataBadgeHeight: Dp,
    val headerHeightFraction: Float,
    val centerHeroWidthFraction: Float,
    val borderStroke: Dp,
    val fontSizeBody: TextUnit,
    val fontSizeHeader: TextUnit
)

val CompactDimensions = HexelionDimensions(
    sphereSize = 48.dp,
    sphereIconSize = 24.dp,
    heroWidgetSizeMapa = 90.dp,
    heroWidgetSizeSecondBrain = 80.dp,
    heroWidgetSizeCamarasWidth = 120.dp,
    heroWidgetSizeCamarasHeight = 68.dp,
    dataBadgeWidth = 80.dp,
    dataBadgeHeight = 36.dp,
    headerHeightFraction = 0.12f,
    centerHeroWidthFraction = 0.70f,
    borderStroke = 1.dp,
    fontSizeBody = 12.sp,
    fontSizeHeader = 14.sp
)

val MediumDimensions = HexelionDimensions(
    sphereSize = 56.dp,
    sphereIconSize = 28.dp,
    heroWidgetSizeMapa = 110.dp,
    heroWidgetSizeSecondBrain = 100.dp,
    heroWidgetSizeCamarasWidth = 150.dp,
    heroWidgetSizeCamarasHeight = 85.dp,
    dataBadgeWidth = 96.dp,
    dataBadgeHeight = 42.dp,
    headerHeightFraction = 0.10f,
    centerHeroWidthFraction = 0.60f,
    borderStroke = 1.5.dp,
    fontSizeBody = 14.sp,
    fontSizeHeader = 16.sp
)

val ExpandedDimensions = HexelionDimensions(
    sphereSize = 72.dp,
    sphereIconSize = 36.dp,
    heroWidgetSizeMapa = 140.dp,
    heroWidgetSizeSecondBrain = 128.dp,
    heroWidgetSizeCamarasWidth = 190.dp,
    heroWidgetSizeCamarasHeight = 108.dp,
    dataBadgeWidth = 120.dp,
    dataBadgeHeight = 52.dp,
    headerHeightFraction = 0.08f,
    centerHeroWidthFraction = 0.50f,
    borderStroke = 2.dp,
    fontSizeBody = 16.sp,
    fontSizeHeader = 20.sp
)

val LocalHexelionDimensions = staticCompositionLocalOf { CompactDimensions }
```

---

### 4. IMPLEMENTACIÓN DE LOS SEIS ESTADOS SOBERANOS DEL DATO [108, 116]
Para garantizar la honestidad absoluta en pantalla, el modelo de datos de telemetría de los repositorios no acepta inferencias ni aproximaciones numéricas libres de red. Cada indicador se mapea bajo un `StateFlow` tipado que responde a los 6 estados de visualización rigurosos [108, 116]:

```kotlin
package p0x.dashboard.data

sealed class TelemetryState<out T> {
    data class Live<out T>(val value: T, val timestamp: Long) : TelemetryState<T>()
    data class Stale<out T>(val lastValue: T, val secondsSinceUpdate: Long) : TelemetryState<T>()
    data class Static<out T>(val value: T) : TelemetryState<T>()
    data class Simulated<out T>(val mockValue: T) : TelemetryState<T>()
    data class NoData(val lastSeenTimestamp: Long?) : TelemetryState<Nothing>()
    data class Error(val exceptionMessage: String) : TelemetryState<Nothing>()
}
```

---

### 5. EL JUEZ DE INTERFAZ: COMPUIESTEST & AUTOMATED SCREENSHOT [116, 117]
Para asegurar que ninguna actualización de Claude Code rompa el diseño inmutable o viole las zonas sagradas del silicio, se define el script de aserción estricta de coordenadas en `DesktopTest` [116]. 
*   **Axioma del Test**: El test analiza el renderizado final del árbol y **cancela el merge** (`exit code 1`) si algún elemento clickable invade el **Centro Sagrado** (reservado para el Orbe) o el **30% derecho del cabecero** (reservado para visibilidad de la placa física) [116, 117].

```kotlin
package p0x.dashboard.test

import androidx.compose.ui.test.ComposeUiTest
import androidx.compose.ui.test.onNodeWithTag
import androidx.compose.ui.test.runComposeUiTest
import kotlin.test.Test
import kotlin.test.assertTrue

class InterfaceJudgeTest {

    @Test
    fun verifySovereignZonesInmutable() = runComposeUiTest {
        // Inicializar el Layout completo del Dashboard bajo el perfil de test
        setContent {
            HexelionDashboardApp(isTest = true)
        }

        val screenWidth = 1920
        val screenHeight = 1080

        // 1. Validar frontera del Centro Sagrado (Sacred Center)
        val centerLeftBound = screenWidth * 0.30f
        val centerRightBound = screenWidth * 0.70f
        val centerTopBound = screenHeight * 0.25f
        val centerBottomBound = screenHeight * 0.75f

        // Comprobación programática en el árbol de Compose: ningún nodo con tag interactivo
        // ("widget", "button", "badge") puede tener coordenadas (x, y) dentro del Sacred Center.
        onAllNodesWithTag("interactive_widget").assertNoneMatches { coords ->
            val bounds = coords.boundsInWindow
            bounds.left >= centerLeftBound && bounds.right <= centerRightBound &&
            bounds.top >= centerTopBound && bounds.bottom <= centerBottomBound
        }

        // 2. Validar frontera de la Plaqueta de Cobre (30% Derecho del Header)
        val headerRightBound = screenWidth * 0.70f
        val headerHeightLimit = screenHeight * 0.08f // Expanded layout height fraction

        // Comprobación: ningún nodo con interactivos o leyendas puede cruzar el límite derecho
        onAllNodesWithTag("interactive_widget").assertNoneMatches { coords ->
            val bounds = coords.boundsInWindow
            bounds.right > headerRightBound && bounds.top < headerHeightLimit
        }
        
        onAllNodesWithTag("text_label").assertNoneMatches { coords ->
            val bounds = coords.boundsInWindow
            bounds.right > headerRightBound && bounds.top < headerHeightLimit
        }
    }
}
```
