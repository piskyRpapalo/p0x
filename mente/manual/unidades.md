---
id: unidades-p0x
titulo: "Unidades del rack, explicadas — el traductor a llano"
tipo: operativo
clase: operativo
version: 1.0.0
editor_autorizado: silicio-telemetria
dominio: manual-soberano
metrica_exito: "cualquier persona de la casa entiende una medida del dashboard sin preguntar; cero unidades en pantalla sin entrada aquí"
umbral_reedicion: "cada vez que una unidad nueva aparezca en una página del dashboard, entra aquí en el mismo pase"
presupuesto_kb: 12
n_medicion: 1
enlaces:
  - manual-del-soberano
descripcion_niveles:
  basico: "Un diccionario de las siglas que salen en las pantallas de casa (°C, %, hPa…), explicadas dos veces: para cualquiera y para quien quiera el detalle."
  medio: "Diccionario operativo de unidades del rack con dos niveles por entrada (basico/experto), formato parseable que /api/unidades sirve a las páginas para la ayuda contextual '¿qué es esto?'."
  experto: "Semilla del traductor-a-analfabeto: fuente única de explicaciones por unidad (sección `## símbolo · nombre` + `- clave:`/`- sensor:` + `### basico`/`### experto`), consumida por regex con cache mtime en el gateway; el mismo patrón descripcion_niveles del Protocolo §2 aplicado a la telemetría."
actualizado: 2026-07-12
---

# UNIDADES DEL RACK, EXPLICADAS
*Cada entrada se lee dos veces: **basico** (para cualquier persona de la casa, sin
tecnicismos) y **experto** (el detalle real). Las páginas del dashboard leen este
archivo vía `/api/unidades` — lo que se edita aquí cambia la ayuda en pantalla.*

---

## °C · grados de temperatura

- clave: temp_c
- sensor: BME680 (M5 Atom, el rincón de las plantas)

### basico
Cuánto calor o frío hace, igual que el parte del tiempo. Alrededor de 20-26 °C
las personas y la menta están a gusto; por encima de 30 °C la planta pasa calor
y pide más agua.

### experto
Temperatura del aire en grados Celsius medida por el BME680 junto a las plantas.
Ojo: el sensor va pegado a la electrónica del M5 y puede leer 1-3 °C por encima
del aire real (autocalentamiento conocido del BME680).

## % · humedad del aire

- clave: humidity
- sensor: BME680 (M5 Atom)

### basico
Cuánta agua flota en el aire, de 0 a 100. Entre 40 y 60 se está bien; muy bajo
el aire se siente seco (labios, plantas mustias) y muy alto, pegajoso.

### experto
Humedad relativa en porcentaje: cuánto vapor de agua contiene el aire respecto
al máximo que admite a esa temperatura. Por eso el mismo aire "se vuelve más
húmedo" al enfriarse sin añadir agua.

## hPa · presión del aire

- clave: pressure_hpa
- sensor: BME680 (M5 Atom)

### basico
El peso del aire sobre nosotros. No se siente, pero avisa del tiempo: si baja
deprisa, suele venir lluvia o viento; si sube, tiempo tranquilo. Lo normal ronda
1013.

### experto
Presión atmosférica en hectopascales (1 hPa = 100 Pa; equivale al milibar).
La tendencia importa más que el valor: caídas ≥3 hPa en pocas horas anticipan
frentes. El valor local baja ~1 hPa por cada 8 m de altitud.

## kΩ · limpieza del aire (sensor de gas)

- clave: gas_ohm
- sensor: BME680 (M5 Atom) — llega en ohmios, se muestra en kΩ

### basico
Un olfato electrónico: huele vapores y gases en el aire. Aquí la regla es fácil
y va al revés de lo que parece: **cuanto más alto el número, más limpio el
aire**. Si baja mucho, toca ventilar.

### experto
Resistencia en kiloohmios de la capa sensible del BME680 calentada: los
compuestos orgánicos volátiles (VOC) la reducen al reaccionar. Es un indicador
relativo sin calibración absoluta — sirve la tendencia contra su propia línea
base, no el número aislado. No confundir con la g de fuerza del acelerómetro:
son sensores distintos del mismo Atom.

## g · fuerza de movimiento (no gramos)

- clave: accel_g
- sensor: ADXL345 (M5 Atom, acelerómetro)

### basico
Mide sacudidas y vibraciones, como el sensor que gira la pantalla del móvil.
**No son gramos de peso**: aquí la g significa fuerza de movimiento. Quieto y en
paz marca alrededor de 1 (la gravedad de siempre); un golpe o temblor lo dispara.

### experto
Aceleración en múltiplos de la gravedad estándar (1 g = 9.81 m/s²) por eje
x/y/z del ADXL345. En reposo el vector suma ~1 g (solo gravedad); sirve para
detectar golpes, vibración del rack o manipulación. Desambiguación doble: no es
el gramo (masa) ni tiene relación con la kΩ del sensor de gas.

## W · vatios de consumo

- clave: consumo_w
- sensor: SAI/UPS vía NUT (lectura, jamás mando)

### basico
Cuánta electricidad está gastando algo ahora mismo, como los vatios de una
bombilla. El rack entero ronda lo que unas pocas bombillas antiguas.

### experto
Potencia instantánea en vatios reportada por el UPS por NUT (upsc read-only).
Energía = potencia × tiempo: 36 W sostenidos ≈ 0.86 kWh/día. MEDIDO viene del
UPS; ESTIMADO (proxy CPU) se marca aparte — jamás se funden.

## kg · kilogramos

- clave: (sin sensor hoy)
- sensor: pendiente — entra aquí cuando exista báscula

### basico
El peso de toda la vida, el de la báscula de la cocina.

### experto
Unidad de masa del SI. Hoy ningún sensor del rack la emite; la entrada existe
para que la ayuda en pantalla esté lista si algún día se pesa cosecha o tierra.

## m/cm/km · metros, centímetros, kilómetros

- clave: (varias: distancias del mapa, alturas)
- sensor: derivadas (AIS/ADS-B en el mapa; medidas a mano en el cuaderno)

### basico
Distancias y tamaños: un centímetro es la uña de un dedo, un metro es un paso
largo, un kilómetro son unos diez minutos andando. La menta crece unos pocos
centímetros por semana cuando está contenta.

### experto
Longitudes del SI (1 m = 100 cm; 1 km = 1000 m). En el dashboard aparecen en
las distancias del mapa marítimo/aéreo (derivadas de posiciones AIS/ADS-B) y
en cualquier medida apuntada a mano; ningún sensor del rack mide longitud hoy.

## Ⓝ · moneda NEAR

- clave: cosecha (mainnet/testnet)
- sensor: Alquimista (lector keyless de NEAR, solo lectura)

### basico
Una moneda de internet que el sistema solo mira, como quien consulta la
hucha: cuánto hay, sin poder tocarlo desde aquí. Su valor en euros cambia
cada día.

### experto
Token nativo del protocolo NEAR. El Alquimista lee balances por RPC keyless
(cero claves privadas en el rack, fail-closed ViolacionKeyless); la cosecha
es dato observado on-chain, no saldo custodiado por el sistema.
