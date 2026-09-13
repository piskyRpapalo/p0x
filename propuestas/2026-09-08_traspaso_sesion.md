# Traspaso · dónde queda todo al cerrar el 2026-09-08

Para la sesión que venga. Escrito para alguien que **empieza en frío** y no
tiene por qué reconstruir nada de memoria.

---

## 0 · Lo primero, y no es negociable

```
python3 ~/p0x/Alejandria/ojo/ojo.py --arranque
```

El panel del puerto 8790 **no está levantado** (deuda 4): una sesión que lo
pruebe por `curl` recibe 000 y concluye que no existe. Se usa la CLI.

---

## 1 · Estado de los tres repos

| repo | rama | commits sin empujar | gate |
|---|---|---|---|
| `~/p0x` | `master` | **0** — al día con `jetson` | guardia de higiene ok |
| `~/p0x/preceptor` | `main` | **3** · `b9561cb` el último | 757/757, 49 suites, sabotajes verdes |
| `~/p0x/preceptoros-web` | `main` | **0** — empujado a GitHub | 93 pruebas + 21/21 del arnés |

**El repo de la app tiene tres commits locales y NO están empujados**
(`e5fdbd4`, `75b07bd`, `b9561cb`). Fue orden explícita del Soberano («ningún
push a GitHub por el momento»), y luego autorizó **solo** la web. Antes de
empujar `preceptor`, preguntar.

El cuarto —`4ab2477`, la matriz de cumplimiento— **sí está empujado**: salió
antes de esa orden. Se dice porque un `git log` de cuatro commits nuevos
invita a suponer que faltan los cuatro.

---

## 2 · Lo que se construyó, en una frase cada uno

- **`linea.py`** — registro append-only con cadena de huellas. `verificar()`
  caza la manipulación parcial y dice en cuál evento. Sin `update` ni `delete`:
  el estado es el **pliegue** de la línea.
- **`normas.py`** — el ancla legislativa de cada pieza y el **léxico de la
  casa**. Tabla, no renombrado. Anclar ≠ cumplir.
- **`docs/COMPLIANCE.md`** — la matriz para un auditor, con sus **huecos**
  pesando lo mismo. `test_compliance.py` la ata al código.
- **`importar.py`**, **`medidas.py`**, **`cifras.py`** — el puente de vuelta
  desde la web, el medidor hablando el esquema de la web, y la regla del
  `NO_DATA` aplicada a los números.
- **El círculo cerrado** — consentir, revocar, corregir, juzgar e importar
  escriben su evento dentro de la misma transacción que el cambio.

---

## 3 · Lo que hay que decidir · nadie más puede

1. **Deuda 39 · ¿cómo se ven los enlaces caídos?** Es la pregunta que bloquea
   el arreglo. Tres escenarios y el remedio cambia entero según cuál sea:
   `file://`, subruta, o el dominio raíz. Medido: **1.573 referencias
   absolutas en 59 de 59 ficheros**. La mezcla dentro de una misma página ya
   está arreglada y con gate; la elección de fondo, no.
2. **Deuda 13-bis · con qué se firma el Sello.** Ya **no bloquea la
   arquitectura** —eso se resolvió leyendo las normas— pero sigue abierta para
   el certificado. Dos caminos: entra una dependencia de criptografía, o lo
   emite el rack (donde El Faro ya firma) y la app lo enseña. Canon encima:
   `soberano` no puede ser el emisor.
3. **Deuda 36 · cuatro nombres heredados.** «La Bienvenida», «El Medidor», «La
   Memoria de Aprendizaje», «Atención al Público» están en `HEREDADOS`, no en
   `LEXICO`. Decidir que son canon no le toca a una sesión de IA.
4. **Deuda 32 · validación jurídica de las citas.** El cruce cazó un «art. 52»
   heredado del borrador de 2021 (es el **50** en el texto publicado). Un test
   comprueba coherencia interna, **no validez legal**.

---

## 3-bis · El Alquimista, para el plano de la próxima sesión

Acta en `propuestas/2026-09-08_alquimista_recuperado.md`. Lo que hay que saber
antes de abrirla:

- **No es un módulo nuevo.** Es una voz del canon desde el Discurso Fundacional
  —*«lee la cadena sin tocarla; consejo, nunca Intent»*— y está en el alfabeto.
- **Su paso 1 ya está construido y probado:** `linea.py`. El resto es
  **ensamblaje** de piezas que ya existen bajo otros nombres, no obra nueva.
- **No hay ni una medida de NEAR en `mente/telemetria/`.** Hay doctrina escrita
  y cero histórico de pruebas. El Faro no responde.
- **Lo primero no es construir, es medir:** ¿responde algo de la cadena desde
  este nodo? Un enjambre montado sobre un sensor sin nada que leer no se puede
  probar.

---

## 4 · Lo siguiente que yo haría, en este orden

1. **(S) Deuda 34 · anclar la última huella fuera de la máquina.** Es la mitad
   barata del no repudio y **no necesita dependencias**. La cadena hoy detecta
   el retoque puntual y no el reescrito completo — y eso está probado como tal.
2. **(S) Deuda 11 · escuchar el contador de fugas.** `sinFuga` dispara
   `preceptor:fuga` con lo que tacha y no lo escucha nadie. Es lo que dirá si
   la ronda siguiente del LoRA recita menos, en vez de suponerlo.
3. **(S) Deuda 38 · publicar `lexico.json` derivado.** Hoy el cruce de nombres
   solo funciona si el repo de la web está a mano. Con el JSON publicado el
   gate cierra en cualquier máquina, y de paso el vocabulario queda a la vista.
4. **(M) Deuda 16 · dibujar la barra del corte.** El sustrato ya existe y está
   probado (`linea.py::tramo`). Si el tramo no se puede dibujar, es que la
   línea todavía no era lineal.
5. **(M) Deuda 15-bis · migrar `engrams`, `profile` y `turnos`.** Siguen
   admitiendo `update` —diez, contados— y `COMPLIANCE.md` lo declara por
   escrito.

---

## 5 · Trampas de esta casa que me mordieron hoy

Se anotan porque volverán, y ninguna es evidente:

- **Las hojas CSS se sirven cacheadas.** El `?v=` invalida el HTML, **no** las
  hojas. Medí contra CSS viejo y saqué dos conclusiones falsas antes de servir
  en un puerto limpio. Ante una medida que no cuadra: puerto nuevo.
- **`sed` con `|` de delimitador y `\|` de alternancia** no alterna: lee la
  barra como literal. Media sustitución sin aviso.
- **`platform.processor()` devuelve la palabra «desconocido»** traducida por el
  sistema. Es un valor *verdadero* que no dice nada, así que un `x or y` no lo
  caza.
- **Un `update` que no cambia nada** hace pasar una prueba de manipulación por
  el motivo equivocado. Comprobar que el sabotaje sabotea.
- **El gate lee los comentarios como código.** Una palabra en prosa dentro de
  un comentario puede ponerlo rojo.
- **Los ficheros de `interface/` no admiten mayúsculas en los comentarios**:
  los guardrails las leen como nombres de política.

---

## 6 · La regla que gobierna lo que venga

Del molde, con las palabras del Soberano:

> *Las paredes son el negativo; el cristal fundido llena el hueco sin tocarlas.
> Lo que no esté aquí y haga falta se propone como deuda o como entrada firmada,
> nunca como hecho. **Un hueco declarado vale más que una pared movida a
> escondidas.***

En la práctica: si algo necesita nombre y no está en `normas.LEXICO`, hay dos
salidas legítimas — usar el término del texto legal que lo juzga, o dejarlo
apuntado como deuda. Inventarlo no es una de las dos, y hoy lo hice dos veces.
