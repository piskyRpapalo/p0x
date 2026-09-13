# ¿El conocimiento local mejora el razonamiento? · 2026-09-12

**Hipotesis del Soberano:** las tareas de razonamiento del rack son siempre las mismas,
asi que servir el metodo desde el RAG deberia mejorar lo que un modelo razona.

**Diseno:** 2x2. Misma lectura del A1T, misma pregunta, misma temperatura. Dos modelos,
con y sin los 4 engramas de metodo que `telemetria` tiene sembrados.

**La tarea tiene una respuesta correcta conocida**, calculada a mano antes de preguntar:
`V x I = 29,04 W` contra `186,90 W` declarados, y `P/I = 218,9 V` — luego **el campo
roto es el voltaje**. Esa segunda cuenta es la que decide: sin ella se sabe que algo
falla pero no QUE, y no se puede reparar nada.

## Resultado

| modelo | sin contexto | con contexto |
|---|---|---|
| **Qwen 3.8** · 27,3B denso | ❌ no diagnostica · 92 s | ✅ **diagnostica** · 123 s |
| **qwen3-coder:30b** · MoE A3B | ❌ no diagnostica · 14 s | ✅ **diagnostica** · 29 s |

**Los dos modelos fallan sin el harness. Los dos aciertan con el.** La variable que
decide es el contexto, no el modelo.

## Lo que hicieron exactamente

**Sin contexto, los dos se quedan en la incoherencia y no pasan de ahi.** Qwen 3.8
encontro el factor x6,4 y se puso a especular con sistemas trifasicos; qwen3-coder
listo los campos y marco **MEDIDO el voltaje roto**, que es peor que no responder.
Ninguno calculo `P/I`. Ninguno dijo que campo mentia.

**Con contexto, los dos hacen la misma cadena:** calculan `P/I`, lo comparan con el
rango plausible de red, y concluyen que el roto es el voltaje. Los dos usan la palabra
**PARCIALMENTE ROTO**, que es literalmente la taxonomia del engrama sembrado.

## Lo que esto cambia en el reparto

**Sirve el metodo y usa el modelo rapido.** Con contexto, qwen3-coder:30b da el mismo
diagnostico correcto en **29 s** contra los **123 s** de Qwen 3.8: cuatro veces mas
rapido por la misma respuesta. Antes de este experimento la eleccion parecia ser entre
un modelo mas listo y uno mas rapido; medido, la eleccion real es entre **preguntar en
frio o servir lo que la casa ya sabe**, y una vez servido el modelo importa poco.

## Lo que NO arregla el harness

Ninguno de los dos vio que `ReactivePower 0.0` + `ApparentPower == Power` + `Factor
1.00` exactos son **relleno**, y Qwen 3.8 con contexto llego a llamarlos «consistentes».
Ese metodo estaba sembrado y aun asi no se aplico. Y Qwen 3.8 sigue devolviendo su
esquema JSON de inventario en vez del formato pedido: **el harness mejora el
razonamiento, no la obediencia al contrato de salida**.

## Repetirlo

    T="Audita esta lectura del A1T: Voltage 34 V, Current 0.854 A, Active Power 186.90 W..."
    python3 delegar.py --espacio telemetria --tarea "$T"                  # con harness
    python3 delegar.py --espacio telemetria --tarea "$T" --sin-contexto   # el control
