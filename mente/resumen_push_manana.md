# Estado para revisar · 2026-09-07

> **Lo primero, y corrige el encargo:** la orden decía «prepara el push pero no
> empujes». **Ya estaba empujado** cuando llegó, porque unas horas antes el
> Soberano escribió *«pusea todo, firmo lo pendiente»* y desde entonces cada
> bloque se cerró con su push. Este fichero no es un plan de empuje: es el
> inventario de lo que ya viajó, para que se revise sabiendo dónde está cada
> cosa. Nada que se lea aquí está pendiente de subir.

## Dónde está cada repositorio

| repo | remoto | cabeza | limpio |
|---|---|---|---|
| `preceptoros-web` | GitHub `origin/main` | `b3b0fcb` | sí, sin ficheros sueltos |
| `p0x` | `jetson:p0x.git` | `d88eb92` | quedan sueltos los de abajo |

Sueltos en `p0x`, y ninguno es urgente:

- `preceptor-lora/adapters/charla_{base,multilang}_v1/` — los adaptadores de hoy.
  Sus **binarios están ignorados a propósito** (regla añadida hoy, la misma que
  ya llevaba firmada el repo web); lo que falta por commitear es su texto:
  `adapter_config.json`, `medida.json` y el README, que es lo que permite saber
  qué se entrenó sin bajarse 55 MB.
- `preceptor-lora/forja/*.log` — salida de ejecución. No se versiona.
- `Alejandria/marca/Pensamiento./` — 5,9 MB de variaciones generadas, en
  carpetas con nombres automáticos. **Y el directorio se llama `Pensamiento.`
  con punto final**, que rompe en Windows y en algunos descompresores. Se dejó
  fuera a propósito: antes de meterlo en la historia hay que renombrarlo.

## Qué cambió hoy

**Los modelos de La Charla.** Corpus de 250 muestras en siete lenguas escrito y
validado (`forja/corpus_charla.py`), y los dos adaptadores entrenados. El
dataset **no se versiona**: se reconstruye del generador con semilla fija, byte
a byte.

**La web, cuatro bloqueos de la auditoría de flujo.** El botón de descarga que
daba 404, el README que anunciaba un modelo inexistente, el enlace a un
*releases* vacío, y `esquina.css` partido por asunto al llegar al tope.

**El cabezal.** El perfil a la esquina junto a la rueda, y el punto verde
corrido a la izquierda para no pisarlo.

**La puerta de salida del aporte.** El taller arma un paquete en el aparato, lo
enseña entero y ofrece copiarlo y abrir el correo. Sin `fetch` ni `sendBeacon`.

**La propuesta del proxy de La Fragua**, con la sintaxis validada por nginx.

## Dos regresiones mías, ya arregladas, y de la misma familia

Al partir `esquina.css` moví **una mitad del asunto y dejé la otra**, dos veces:

1. `max-width:100%` del móvil se borró en vez de moverse → la pastilla de la
   cuenta se estrangulaba a 375 px.
2. `top:calc(40px + 1.5rem)` se fue a la hoja nueva —que carga después— y le
   ganó al `top:8.4rem` del móvil → la esfera subió 70 px y pisaba la frase
   solar y la cuenta. Es el fallo de la captura del teléfono.

Las dos las cazó la medida, no la lectura. **La lección, si se parte otra hoja:
buscar TODAS las declaraciones del mismo selector antes de mover ninguna.**
`.presentacion` tenía tres, no dos.

## Deuda anotada

- **`esquina.css` volvió a tener sitio** (13.279 B de 16.384) al partirse. Pero
  la regla de la casa —*«se parte por el asunto y no se recortan comentarios»*—
  la incumplí primero recortando los míos. Está escrito en `OPERACIONES.md`.
- **El bloque `reclamaciones` del LoRAtelier está en `en_entrenamiento` con
  `artefacto: null`** a propósito, para no pintar un botón hacia un 404. Vuelve
  a `beta` **sólo** cuando el proxy de La Fragua sirva los 55 MB. Servir
  primero, prometer después.
- **El chat no contesta sin red.** El armazón sí abre offline (143 recursos
  cacheados, cero externos, verificado en el sitio real), pero quien responde es
  el rack. Eso es decisión de producto, no arreglo de `sw.js`.

## Qué NO hacer mañana

- **Nada de `--force` ni reescritura de historia.** Los dos repos están
  publicados y sincronizados; un force-push tira lo que ya está en GitHub.
- **Nada de `git commit --no-verify`.** El guardián de higiene bloqueó hoy con
  razón: `IP-TAILNET` está en su suelo duro y no lo exime ninguna firma. La
  salida buena fue el marcador `IP_TAILNET_SOBERANO`, no saltarse la regla.
- **No versionar los binarios** de `adapters/` ni `public/downloads/*.gguf`.
- **No commitear `Pensamiento.`** hasta renombrarlo sin el punto final.
