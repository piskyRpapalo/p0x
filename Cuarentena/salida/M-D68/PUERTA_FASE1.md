---
id: puerta-fase1-m-d68
titulo: M-D68 · Fase 1 en PC · estado de la puerta antes de ejecutar
tipo: operativo
clase: operativo
version: 1.0.0
sistema: COMPARTIDO
estado: BLOQUEADO · tres entregables, tres puertas, ninguna la abre el silicio
actualizado: 2026-08-13
---

# M-D68 · LA PUERTA DE LA FASE 1
### Parar-y-reportar. Nada ejecutado, nada descargado, nada sustituido.

**Qué pedía el REPORTE:** latencia del modelo pequeño, voz elegida por oído,
resultado de la prueba manual.

**Qué se puede entregar hoy:** ninguno de los tres, y el motivo de cada uno es
distinto. Los tres se desbloquean con actos que el mensaje mismo reserva al
carbono. Este documento es la evidencia de en qué estado está cada puerta, para
que abrirlas cueste minutos y no una sesión de investigación.

---

## §1 · LATENCIA DEL MODELO PEQUEÑO · NO_DATA · falta el modelo

**El modelo pequeño no está en el disco.** Búsqueda exhaustiva de `*.gguf` en el
home del nodo y en sus montajes, hasta profundidad 8:

| Fichero en disco | Tamaño |
|---|---|
| `soberano-bench/models/Qwen3-Coder-30B-A3B-Instruct-Q4_K_M.gguf` | 18,6 GB |
| `ComfyUI/models/unet/flux1-schnell-Q4_K_M.gguf` | 6,9 GB |

Ni `Qwen3-4B-Instruct`, ni `Phi-4-mini`, ni ninguna variante. **El paso §3.1 —el
Soberano firma la descarga, licencia y SHA256 antes— no ha ocurrido.** El
silicio no lo suple: descargar sin esa firma sería exactamente la sustitución
silenciosa que la disciplina prohíbe, y además contradice el «cero descargas»
del propio mensaje.

`NO_DATA` aquí significa *nadie lo ha medido todavía*, no *es lento*. La
distinción es la misma que el producto le enseña a la persona.

### La herramienta SÍ está, y conviene corregir un detalle del plan

`llama-cli` existe en este metal, en la compilación Vulkan `b10068`:

```
soberano-bench/bin/llama-b10068-bin-ubuntu-vulkan-x64/llama-b10068/llama-cli
```

Junto a él viajan `llama-completion`, `llama-bench`, `llama-server` y —dato no
recogido en el plan— **`llama-tts`**. Es decir: **la Fase 1 no necesita
compilar ni descargar runtime.** En cuanto el `.gguf` pequeño esté en disco, la
medición de primer token en Vulkan y en CPU es cuestión de minutos.

**Corrección al hallazgo de M-D67 §4:** el binario que habla por entrada y
salida estándar no hay que ir a buscarlo — ya está aquí, en la misma carpeta
desde la que se sacaron los 32,49 tok/s del 30B.

---

## §2 · VOZ ELEGIDA POR OÍDO · IMPOSIBLE HOY · los clips no están en este nodo

`p0x/voz/gate0/` en **soberano** contiene **un solo fichero**: `metricas.txt`.
Cero WAV. El oído no tiene qué escuchar aquí.

Los clips existen, pero **viven en la fragua**. El propio `metricas.txt` lo dice
en cada línea, apuntando a `voz/gate0/` bajo el NVMe de ese nodo:

```
sharvard-medium_monje.wav · sharvard-medium_alquimista.wav · sharvard-medium_sindato.wav
davefx-medium_monje.wav   · davefx-medium_alquimista.wav   · davefx-medium_sindato.wav
```

Seis clips, dos voces, tres textos (`monje`, `alquimista`, `sindato`), medidos
el 2026-07-05 con la zona térmica anotada antes (49,9 °C) y después (57,3 °C).

**Las dos candidatas son `es_ES-sharvard-medium` (74 M) y `es_ES-davefx-medium`
(61 M).** Ambas españolas, que es lo que pide un timbre «grave y sereno de ~70
años». Traerlas a soberano es un movimiento entre nodos: **propuesta, no
ejecución** — no se toca la fragua desde aquí sin misión para ese nodo.

### Tres cosas que el oído debe saber antes de firmar

1. **En soberano no hay Piper.** No hay binario, y la única voz instalada es
   `en_US-kathleen-low`: inglesa, femenina, calidad baja. Nada que ver con lo
   medido en la fragua. Si el oído elige Piper, **instalarlo en el PC es otra
   descarga que necesita firma.**
2. **Los 681 ms son de la fragua, no de este PC.** `OPERACIONES.md`, bajo el
   epígrafe literal *«números medidos en la fragua»*: frío 3 705 ms, residente
   681 ms, caché 29 ms, RSS ~272 MB con `davefx`. La Fase 1 es en PC: ese número
   hay que volver a medirlo aquí, y probablemente mejore.
3. **La residencia medida es un servicio HTTP en localhost** (`voz_api.py`,
   `127.0.0.1:8021`). Es exactamente la forma que D68 declaró indistinguible de
   un túnel y prohibió **para el gerente**. La voz no es el gerente, y puede que
   la excepción sea legítima — pero conviene que se declare a propósito y no por
   inercia, porque es el mismo patrón que M-D67 §4 señaló como violación.

---

## §3 · PRUEBA MANUAL · ¿FILÓSOFO O SOPORTE TÉCNICO? · aguas abajo

Depende de §3.3 (ensamblar las tres capas), que depende de §3.1 (el modelo). No
hay nada que probar todavía. Es del carbono por definición: la pregunta que
decide es si *suena* a filósofo, y eso no lo mide un test.

---

## §4 · LO QUE ESTÁ LISTO PARA EL MINUTO EN QUE SE ABRA LA PUERTA

- **Runtime:** compilación Vulkan `b10068` completa, con `llama-cli` y
  `llama-tts`. Cero descargas.
- **Cifra de referencia del 30B, para contrastar:** CPU 9,90 tok/s ·
  Vulkan 32,49 tok/s (generación). El pequeño debería estar muy por encima, y
  ese contraste es el que importa: no el número absoluto, sino cuánto se gana.
- **Backend de esta sesión, registrado como manda la disciplina:** `ollama ps`
  responde *could not connect* — el servicio no está levantado. Irrelevante para
  `llama-cli`, que no lo usa, pero queda anotado: el backend de la sesión
  anterior no se asume.
- **Tres capas separadas, sin mezclar:** modelo (falta), arquetipo por prompt
  (B1 firmado, texto sin escribir), voz (candidatas en la fragua). Ninguna de
  las tres depende de las otras dos para existir.

## §5 · LO QUE DESBLOQUEA CADA PUERTA, EN UNA LÍNEA CADA UNA

1. **Latencia** → la firma de la descarga del `.gguf` pequeño (licencia +
   SHA256). Medición inmediata después.
2. **Voz** → traer los seis WAV de la fragua a este PC, o escucharlos allí. Es
   una propuesta entre nodos, y sale de aquí como tal.
3. **Prueba manual** → ensamblaje, que es mío, en cuanto exista el modelo.

**Lo único que puede avanzar sin ninguna firma es el texto del arquetipo
público (B1).** No necesita modelo ni voz: es prosa, y es del producto, no del
Preceptor —D63 intacto—. No se ha escrito en esta ronda porque el REPORTE pedía
tres medidas y no un carácter, y porque el arquetipo es la cara que Aurelius le
enseña a cualquiera: merece la firma del Soberano sobre el texto, no solo sobre
la decisión.

---

**Nada de esto vive en el repo del producto.** `aurelius-mvp` tiene un guardián
que exige cero apariciones de vocabulario de modelos y motores en producción, y
lo cumple. Este documento es del rack, y aquí se queda.
