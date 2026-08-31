
### M10-EM-2 Smart Plug (Simatop/Tuya)
- **Fecha de entierro:** 2026-08-31 · **CASO CERRADO POR EL SOBERANO**
- **Causa de muerte:** doble barrera, y la segunda es la que mata.
  1. *Técnica:* firmware Tuya parcheado post-feb-2022 sin perfil público en
     tuya-cloudcutter. No explotable por OTA; chip BK7231N confirmado por
     gemelo F1s202-EU (Antela). BL0937 presente (medición de energía).
  2. *Administrativa:* **Tuya bloquea la API del wizard tras una vinculación
     fallida.** No es un fallo que se reintente: es una puerta que se cierra
     con llave desde el otro lado. Ninguna vía de extracción sobrevive a eso,
     porque el obstáculo ya no está en el aparato sino en la cuenta.
- **Intentos:** CloudCutter → lista vacía de plugs EM. OpenBeken DB → 0
  resultados para "m10". Gemelo F1s202-Antela identificado pero sin perfil CC
  propio. Vinculación por wizard → fallida, y el fallo cerró la API.
- **Alternativas:** **ninguna, y no se buscan más.** El UART, que esta ficha
  declaraba «pendiente», queda **cerrado por decisión del carbono**: seguir
  abriendo el aparato es gastar horas contra una barrera administrativa que no
  cede por hardware. No se toca, no se flashea, no se reintenta.
- **Reemplazo soberano:** **Shelly Plug S** (API local HTTP/MQTT, sin nube
  obligatoria, sin abrir el aparato). Para el camino crítico batería→pared:
  Shelly siempre. **Pendiente de compra.**
- **Corrección de alcance (2026-08-31, dato del Soberano):** la **Anker Solix
  está en WiFi y se gobierna desde el Doogee**, así que el lado de la *batería*
  del camino crítico **ya reporta** por su propia vía. Lo que el M10 iba a medir
  y hoy nadie mide es el lado de la *pared* — la toma. Eso reduce el Shelly de
  «pieza que desbloquea el camino» a «pieza que cierra el tramo que falta»:
  sigue haciendo falta, pero **no es un bloqueante**, y conviene no comprarlo
  con prisa de urgencia que no tiene.
- **Destino físico:** caja «NECRÓPOLIS».
- **Lección:** los plugs mini EU con BL0937 recientes están mayoritariamente
  parcheados, y la liberación OTA es cada vez más rara. Pero la lección cara no
  es esa: es que **una barrera administrativa derrota a una vía técnica que
  funciona**. El fabricante no tuvo que hacer el chip inexpugnable — le bastó
  con cerrar la cuenta. Cuando el obstáculo se mueve del silicio al contrato,
  el tiempo de ingeniería deja de comprar nada, y la respuesta correcta es
  cambiar de proveedor, no insistir.
