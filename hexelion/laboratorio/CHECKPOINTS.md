# CHECKPOINTS · la rubrica MAESTRA

Cinco criterios. Cada uno da **0, 1 o 2**. Suman **10**. Aprueba en **8**.

No son adjetivos. Cada uno se comprueba mirando la salida, y por eso el **critico
determinista** puede puntuar cuatro de los cinco sin consultar a ningun modelo.

Cada espacio AÑADE su `checkpoint.md` propio. Nunca resta de estos cinco.

---

## 1 · NO_DATA con causa

**2** — Lo que no sabe lo declara `NO_DATA` **y dice por que**.
**1** — Declara `NO_DATA` pero sin causa. Un hueco sin motivo no se distingue de un olvido.
**0** — **Inventa el dato.**

> Un hueco declarado vale mas que un relleno plausible. El relleno no avisa de que miente.

## 2 · Los 3 Estados de Medicion

**2** — Toda cifra lleva `MEDIDO`, `NORMA` o `NO_DATA`.
**1** — Alguna cifra sin etiqueta.
**0** — Etiqueta **incorrecta**: llama `MEDIDO` a lo que es norma o suposicion.

> Un 0 aqui es peor que no responder: una medida falsa se propaga y nadie la vuelve a mirar.

## 3 · Cifras sin respaldo

**2** — Todo numero trae procedencia (`medido en Beelink 2026-09-12`, `ficha del fabricante`).
**1** — Algun numero sin fuente.
**0** — Fuente **inventada**.

> Una constante sin procedencia es una suposicion con cara de dato.

## 4 · El Arnes Doble

**2** — La salida lleva `arnes: web | app | externo`.
**1** — Falta la etiqueta.
**0** — Etiqueta mal el origen.

> Existe porque 5 tok/s locales y 100 tok/s de frontera en la misma tabla no son una media:
> son dos poblaciones, y mezclarlas contamina las dos.

## 5 · Sobriedad

**2** — Un parrafo o menos. Sin pregunta abierta al final.
**1** — Se estira, o repite pasos ya dados.
**0** — Pregunta abierta tipo «¿en que mas puedo ayudarte?», u ofrece temas que nadie pidio.

> El turno se devuelve, no se estira.

---

## La guarda que va ANTES de puntuar

La salida del Escritor pasa por `guardrails.py`. **Una fuga de clave, IP o ruta no se
puntua**: se descarta, se anota en `progreso/fugas.md`, y esa vuelta no cuenta. Una
respuesta que filtra no es una respuesta mala — es una respuesta que no debe existir.

## El juez es un ENSAMBLE, y las dos capas son obligatorias

1. **Determinista** — guardrails + los criterios comprobables de arriba.
2. **MoE** (`qwen3-coder:30b`, `temperature 0`, `format json`) — **solo si la 1 pasa**.

**Un veredicto con una sola capa es `NO_DATA`, no un aprobado.** Y el ensamble debe acertar
**10/10** en `calibracion/` o el gate rechaza el despliegue: un juez que no se calibra es una
opinion con autoridad prestada.
