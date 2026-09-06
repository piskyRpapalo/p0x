# Notas térmicas de la forja · nodo `soberano`

Todo lo de aquí está **medido en este Beelink** (Ryzen 7 255, 8 núcleos / 16
hilos, Radeon 780M, sin GPU dedicada), entrenando LoRAs sobre Mistral 7B en
bf16 con `torch 2.13.0+cpu`. Ninguna cifra es de ficha técnica.

---

## Lo que sabemos, y cómo lo sabemos

| Configuración | s/paso | Temp. máxima | Respiros | Reloj |
|---|---|---|---|---|
| 8 hilos, sin termostato (10 pasos) | 9,48 | **84,0 °C** | 0 | 1,6 min |
| 6 hilos, termostato a 75 °C (10 pasos) | 10,4 | **81,6 °C** | 9 de 10 | 5 min |
| 8 hilos, termostato a 80 °C · corpus EN (200 pasos) | 5,55 | **84,4 °C** | 62 | 39 min |
| 8 hilos, termostato a 80 °C · corpus multilingüe (200 pasos) | 6,83 | **85,1 °C** | 72 | 47 min |

Y la curva de enfriamiento en reposo, medida: **de 58 a 48 °C en 20 segundos**.
La máquina disipa bien; el problema no es que acumule calor.

## Los tres hallazgos

### 1. El termostato pausa ENTRE pasos, y el pico ocurre DENTRO del paso

Es lo que la tanda de 200 pasos dejó claro: con el techo puesto en 80 °C y 62
pausas ejecutadas, **la máxima siguió siendo 84,4 °C**. La pausa llega tarde por
construcción — mide antes del paso siguiente, cuando el pico del anterior ya
pasó.

**Consecuencia:** el termostato sirve para que la temperatura media no se
dispare en una sesión larga. No sirve para poner un techo duro.

### 2. Bajar a 6 hilos NO resuelve, y cuesta caro

Dos hilos menos compraron **2,4 °C** (84,0 → 81,6) y **triplicaron el reloj**:
nueve pausas de 20 s sobre un trabajo de 104 s. Y aun así no se sostuvo por
debajo de 75.

Esto **desaconseja la modificación propuesta para el 12B** tal cual: pasar de 8
a 6 hilos no comprará el margen que hace falta, y sí multiplicará las horas. Si
se quiere el techo de verdad, hay que reducir el trabajo por paso —longitud de
secuencia, o acumulación de gradiente con lotes más cortos—, no el número de
hilos.

### 3. El nodo NO declara su límite térmico

`k10temp` aquí expone `temp1_input` y `temp1_label`, y **nada más**: ni
`temp1_max` ni `temp1_crit`. Así que **los 75 y los 80 °C son objetivo declarado
por el Soberano, no límite medido del hardware**. Antes de pagar horas por
respetarlos conviene mirar la hoja de datos del Ryzen 7 255: si su Tjmax está muy
por encima, 84 °C sostenidos pueden ser régimen normal y no una alarma.

---

### 4. El corpus multilingüe cuesta un 40 % más de RAM, y no es el modelo

Los dos entrenamientos usaron **la misma base, los mismos hilos y el mismo
número de pasos**. La única diferencia era el corpus. Y sin embargo:

| | RAM pico | s/paso |
|---|---|---|
| corpus inglés | 19.058 MiB | 5,55 |
| corpus multilingüe | **26.766 MiB** | 6,83 |

**+7,7 GB por cambiar de corpus.** La causa está medida: las cinco muestras
griegas ocupan **655 tokens de mediana frente a 214** de las de alfabeto latino
— el mismo contenido cuesta el triple porque el tokenizador es latino-céntrico.
Secuencias más largas son más activaciones, y las activaciones son la memoria.

Esto reordena la prioridad para el 12B: **el techo que va a morder no es el
térmico, es el de RAM.** Y la aritmética asusta: si un 7B multilingüe hace pico
de 26,8 GB sobre 38 disponibles, un 12B con el mismo corpus no cabe. Antes de
lanzarlo hay que medir su pico con **una sola muestra griega**, que es el peor
caso, y no con el corpus entero a la hora y media.

### 5. `max_len` es un techo de truncado, NO un relleno

Se propuso bajarlo de 1024 a 256 para reducir calor. **No habría reducido nada.**
En este entrenador el lote es 1 y no hay `padding=`, así que una muestra de 214
tokens cuesta 214 tanto con `max_len=1024` como con 256. El coste va por tokens
reales, no por el techo.

Lo que sí habría hecho: **truncar las cinco muestras griegas** —todas pasan de
256— y borrar del experimento justo la lengua que lo hacía interesante, mientras
el log seguía diciendo que entrenaba con ella. Bajar `max_len` solo sirve para
cortar, y aquí cortar era el daño.

## Para el Mistral Nemo 12B

**Lo que hay que medir antes de lanzarlo**, porque el 7B no lo responde:

- **La RAM.** El 7B en bf16 hizo pico de 19,1 GB. El 12B es ~1,7× en pesos, así
  que la estimación es ~30 GB sobre 38 disponibles. Es un margen estrecho, y una
  estimación no es una medida: **hay que cargarlo y mirar el pico real antes de
  entrenar 200 pasos**, no descubrirlo con un OOM a la hora y media.
- **El pico térmico con más trabajo por paso.** Más parámetros por paso es más
  tiempo al 100 % de los ocho núcleos.

**El throttle dinámico de frecuencia que se propuso NO se puede hacer desde
aquí.** Escribir en `/sys/devices/system/cpu/cpu*/cpufreq/scaling_max_freq` pide
root, y en este nodo no hay sudo interactivo. Sale como **propuesta**, no como
cambio:

```
# PROPUESTA · requiere firma y root. No ejecutado.
# Limitar la frecuencia máxima mientras dure una forja larga:
#   cpupower frequency-set -u 3.2GHz      # antes de entrenar
#   cpupower frequency-set -u <máx>       # al terminar
# Alternativa sin root si el gobernador lo permite:
#   powerprofilesctl set power-saver      # y volver a `balanced` después
```

Lo que **sí** se puede hacer sin root: **acortar las muestras**, que no es lo
mismo que bajar `max_len` — ver el hallazgo 5. El techo no cuesta nada; lo que
cuesta son los tokens reales. Para bajar el pico hay que escribir muestras más
cortas o partir las largas, y la que hay que mirar es la griega: 655 tokens de
mediana contra 214 de las latinas.

---

## La regla que sale de todo esto

**Un techo térmico no se declara: se demuestra.** El termostato escribe
`temp_max_c` en `medida.json` de cada forja, y esa cifra es la que manda sobre
lo que se creía. Si una tanda futura vuelve a pasar de 84 con el techo en 80, no
es un fallo del termostato — es que el techo no se puede sostener pausando.
