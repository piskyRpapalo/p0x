# Lo que cuesta un ciclo del Laboratorio de Turnos

**REQUISITO 10.** Medido el 2026-09-13 en `soberano` (Beelink Ryzen 7 255 +
Radeon 780M, Vulkan, `ollama ps` a 100% GPU), con `medir_modelo.py` contra el
esquema del juez: mismo prompt, mismo `num_ctx 8192`, misma `temperature 0`.

## El reparto, y lo que tarda cada turno

| turno | papel | modelo | tok/s | segundos |
|---|---|---|---|---|
| 0 | Portero | Python | — | ~0 |
| 1 | Bibliotecario | `qwen2.5-coder:3b` | **35,9** | **5,4** |
| 2 | Analista | `qwen2.5:7b` | 16,72 | 13,8 |
| 3 | Guardián | `granite3-dense:8b` | 15,46 | 11,3 |
| 4 | Forjador | Python | — | ~0 |
| 5 | Evaluador | `qwen3-coder:30b` | **35,8** | ~5 |

**Por fila: ~36 segundos de pared.** Un ciclo de 20 filas ronda los **12
minutos**, y el tope de ritmo (5 vueltas/minuto) no llega a morder: una fila
tarda más de 12 segundos por sí sola.

## Por qué el Evaluador es el 30B y no el 27B

Los dos devuelven el esquema completo. Lo que los separa es el reloj:

| | tok/s | segundos | |
|---|---|---|---|
| `qwen3-coder:30b` | **35,8** | ~5 | MoE A3B: pesa 30B, **activa ~3B** |
| `swift-qwen:27b` | 4,44 | 52,8 | 27,3B **denso**, y además `thinking` |

Ocho veces más rápido para el mismo trabajo. En un ciclo de 20 filas eso son
**1 minuto contra 17**. La inversión del sentido común —el modelo grande es el
rápido— es la arquitectura, no la suerte.

## La energía: NORMA, no MEDIDO

Los 58 W de los benchmarks **no están medidos en este nodo**, y por dos razones
distintas que se suman:

1. **El enchufe A1T mide la regleta entera** — impresora, TV y rack juntos,
   186,90 W de lectura total. Una regleta mide la suma; no sabe atribuirle
   vatios al Beelink.
2. **«CPU puro» contradice el backend medido.** `ollama ps` da **100% GPU** con
   Vulkan activo. Un vatiaje calculado sobre CPU no describe lo que corrió.

Así que toda cifra en mWh de este laboratorio es **NORMA · derivada de una
constante no atribuida**, y se etiqueta así donde aparezca. Lo MEDIDO son los
tok/s y los segundos de la tabla de arriba, que se tomaron en esta máquina.

**Qué haría falta para subirla a MEDIDO:** un medidor en la toma del Beelink, o
apagar todo lo demás de la regleta y restar. Mientras tanto, `tok_s_vatio` sigue
siendo `NO_DATA` para todos los nodos, y la matriz de `colocacion.json` lo dice
en tres de sus cuatro filas en vez de rellenarlas.

## El coste que no se mide en vatios

El tope de **5 vueltas por minuto** no existe para ahorrar energía: existe
porque la iGPU es una sola y la comparten los bucles del rack. Medido esta misma
sesión — mis propias tandas de 27B en segundo plano provocaron **19
aplazamientos** del bucle director por «carga 3.07 > 2.0». El observador altera
lo observado, y el tope es la correa.
