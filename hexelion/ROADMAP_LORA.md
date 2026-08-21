# HEXELION · Roadmap evolutivo del LoRA · cuatro vectores edge

> **PRIVADO · Nivel 2. No se publica.** El Dominio 1 no sabe que esto existe.
> Documentación y planificación: **nada de esto se ejecuta** hasta cerrar la
> Fase 3 del producto.
>
> **Nota de ubicación.** El canon del nodo dice que `hexelion` es un repositorio
> propio que empuja a `torre`. En esta máquina no existe. Esto vive en
> `p0x/hexelion/`, que es donde lo nombraste. Si el repositorio aparece, esto se
> mueve entero — se declara para que nadie lo dé por canon en el sitio de otro.

Cada vector lleva **lo que verifiqué** y **lo que no**, separados. La regla que
salió del borrador del Preceptor aplica aquí igual: lo que dijo un tercero va
marcado, no ascendido a hecho.

---

## VECTOR 1 · Sínodo multi-LoRA

**La idea:** dejar de simular el Sínodo con texto y hacerlo con pesos —
`lora_monje`, `lora_berserker`, `lora_alquimista` sobre un único Qwen3-4B en RAM
compartida.

**La acción pedida era documentar la viabilidad de Punica sobre el Ryzen del
Beelink. La respuesta es que no la hay, y conviene saberlo antes de gastar una
sesión en ello.** Punica está construido sobre kernels CUDA (SGMV) para servir
muchos LoRA sobre un batch en GPU NVIDIA. Este nodo tiene una Radeon 780M
integrada y ninguna NVIDIA. Es el mismo muro que Unsloth en la Fase 0, por la
misma razón, y no se arregla con paciencia.

**Lo que sí existe en el metal que tienes:** `llama.cpp` — el runtime que ya usa
el producto — admite **varios adaptadores LoRA a la vez** sobre un solo modelo
base cargado, con escala por adaptador. Eso es exactamente el consejo de pesos
que persigue el vector, sin CUDA y sin dependencia nueva: el base se carga una
vez y cada voz es un fichero pequeño encima.

`SIN VERIFICAR`: no he medido cuánto cuesta activar y desactivar adaptadores
entre turnos en esta build, ni si el coste crece con el número de voces.
Medible en una tarde con `llama-cli` y los tres adaptadores.

**Ganancia real esperada:** una voz nueva deja de costar 2,3 GB y pasa a costar
lo que pese su adapter. Con el Sínodo de tres voces, eso es la diferencia entre
7 GB y 2,4 GB.

---

## VECTOR 2 · Alma comprimida para el carbono móvil

**La idea:** comprimir el adapter ~75 % con una proyección de subespacio
post-entrenamiento y bajarlo de peso para el Doogee.

**`SIN VERIFICAR` · «SOLAR».** No he podido confirmar desde este nodo qué es
exactamente la técnica que nombras ni su factor de compresión. Va marcada como
declarada por terceros, sin fecha de verificación, y **no se apoya ninguna
decisión en ella**.

**Y una corrección de arquitectura que importa más que la compresión.** El
tamaño del adapter **no es hoy lo que limita al Doogee**. La cadena de la Fase 4
que ya está desbloqueada es:

```
adapter PEFT → convert_lora_to_gguf.py → llama-export-lora → llama-quantize
```

`llama-export-lora` **fusiona** el adapter dentro del GGUF base. Lo que llega al
teléfono son ~2,3 GB de modelo fusionado, **con adapter de 22 MiB o de 2 MiB,
exactamente igual**. Comprimir el adapter al 25 % ahorra 17 MiB de transferencia
por USB y **cero** en el teléfono.

La compresión solo paga si se cambia la arquitectura de despliegue: **no
fusionar**, y que el teléfono cargue base + adapter por separado en tiempo de
ejecución. Eso es el Vector 1, no el 2 — y entonces sí, tres voces de 2 MiB
sobre un base de 2,3 GB es una idea excelente.

**Orden correcto, por tanto: el 1 antes que el 2.** Comprimir algo que se va a
fundir es trabajo que se tira.

**Lo que sí está medido y limita de verdad al Doogee:** 5,4–6,3 min por turno,
porque el motor recarga los 2,3 GB en cada turno (medido, sprint del 2026-08-20).
Ahí hay un orden de magnitud que ninguna compresión de adapter toca.

---

## VECTOR 3 · Memoria long-context para el Cahier

**La idea:** atención local dispersa para llevar el contexto de 2k a 8k/16k, y
que el Preceptor lea el historial de misiones firmadas en una sola inferencia.

**Dependencia correcta:** marcado como fase futura, después del Vector 1.

**La cifra que hay que poner delante antes de invertir aquí.** El Doogee procesa
prompt a **5,25 ± 0,43 tok/s** (medido). Un contexto de 8k tokens serían **~26
minutos solo de leer el prompt**, antes de generar una sola palabra. En el
teléfono, este vector no es lento: es inviable.

En el Beelink es otra historia — 14,5 tok/s de generación y prompt bastante más
rápido — y ahí sí tiene sentido, **que es además donde vive el Preceptor**. Así
que el vector es bueno y su destino es el nodo grande, no el bolsillo. Conviene
que quede escrito para que nadie lo pruebe en el Doogee y concluya que la técnica
no sirve.

`SIN VERIFICAR`: no he medido prompt processing en el Beelink a 8k, ni el techo
de RAM con ese contexto. Las dos cosas son medibles antes de comprometer nada.

---

## VECTOR 4 · Auto-canonización

**La idea:** las correcciones del Soberano se convierten automáticamente en pares
de entrenamiento; los repos de solarpunk-lab nutren vocabulario técnico.

**Este es el vector que resuelve el problema real, y por eso lo pondría el
primero de los cuatro.** La Fase 2 lo dejó claro dos veces: 5,9 M de parámetros
entrenables contra ~3 000 tokens de texto. Ningún hiperparámetro arregla eso —
`r=16` memorizaba, `r=8` memorizaba más despacio. **Lo único que lo arregla es
que el dataset crezca**, y este vector es la única fuente de crecimiento que no
es relleno sintético, que la Firma 1 prohibió explícitamente.

**Diseño del bucle** (no implementado; y cuando se implemente, sale como módulo
propio del Dominio 1 con su commit, no como dependencia de esto):

1. **Captura.** Cuando la persona corrige una respuesta, se guarda el trío
   `(prompt, lo que dijo el modelo, lo que la persona puso en su lugar)`. Es
   exactamente la forma que ya tiene `clase: preferencia` en el esquema del
   dataset: `prompt` / `rechazado` / `elegido` / `motivo`.
2. **Consentimiento explícito, una vez por corrección.** Esto convierte palabras
   de una persona en datos de entrenamiento. En un producto cuya primera promesa
   es que nada sale de la máquina, capturar en silencio sería la traición
   perfecta: técnicamente local y moralmente idéntica a la telemetría. **Se
   pregunta, y el no es gratis.**
3. **Cuarentena, no ingreso directo.** Lo capturado va a una bandeja, no al
   dataset. El guardián de la Fase 1 lo valida —redacción, vocabulario de la
   casa, equilibrio EN/ES— y el Soberano firma.
4. **El motivo es obligatorio.** Un par sin motivo no se puede auditar seis meses
   después, y ya está escrito así en el esquema.

**Sobre solarpunk-lab:** `SIN VERIFICAR`. No he inspeccionado esos repositorios
ni su licencia. Antes de que una línea suya entre al dataset hacen falta las dos
cosas: que la licencia lo permita, y que pase el guardián. El dataset es el alma
y el alma no admite material de procedencia no declarada.

---

## Orden propuesto, y por qué difiere del tuyo

| | Tu orden | Propuesto | Motivo |
|---|---|---|---|
| 1º | Sínodo multi-LoRA | **Auto-canonización (V4)** | Es lo único que ataca la causa medida del fracaso de v1 y v2. Sin datos, los otros tres afinan el vacío. |
| 2º | SOLAR | **Sínodo multi-LoRA (V1)** | Con `llama.cpp`, no con Punica. Y es prerrequisito del 2. |
| 3º | Long-context | **Compresión (V2)** | Solo tiene sentido si el 1 decidió no fusionar. |
| 4º | Auto-canonización | **Long-context (V3)** | El más caro y el que menos aprieta hoy. |

No lo cambio por mi cuenta: es una propuesta, y el orden lo firmas tú.
