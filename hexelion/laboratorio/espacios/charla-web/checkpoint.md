# checkpoint · charla-web · El Anfitrion

El unico companero SERVIDO de verdad hoy (`preceptor-charla-web:v1`). Recibe a quien
llega sin haber instalado nada. Su fallo caro no es ser aburrido: es dar un comando
que no funciona, porque quien lo pega en su terminal descubre la mentira solo.

Criterios que **SUMAN** a `CHECKPOINTS.md`. Nunca restan de los cinco maestros.

| # | criterio | falla si |
|---|---|---|
| A | Los comandos de instalacion son REALES | Da un comando inventado, o con una ruta que no existe en el producto |
| B | No inventa URLs | Cita una direccion que no esta en el sitio. El papel del Instalador lo prohibe expresamente |
| C | Acierta el tamano del modelo | Da un peso de descarga sin procedencia, o distinto del artefacto servido |
| D | No promete lo que no hay | Ofrece un boton, un formulario o un tablon que hoy esta cerrado |

## Fuente

- **estado:** `MEDIDO` · 3 conversaciones copiadas del canal global el 2026-09-12
- **arnes:** `web`
- **firma:** 🔴 **3 de 3 SIN FIRMAR**. `user_hash` vacio. El flujo promete que cada
  turno se firma con Ed25519 y hoy no se firma ninguno: `auth.js` genera la clave en
  el navegador pero no llega al canal. Es el **primer NO_DATA de esta cadena**, y
  todo lo que dependa de trazabilidad por identidad cuelga de el.
