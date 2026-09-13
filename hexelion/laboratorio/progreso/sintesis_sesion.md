# por donde vamos · 2026-09-12 21:55

> Escrito por `oficial-inventario:q4-1.0` desde un dosier de hechos medidos.
> Generacion: 4.58 tok/s · 155.1 s.

**Frente abierto:** La firma de las 4 conversaciones pendientes en charla-base y charla-web, y la estabilización de la carga que se mantiene en 2.32.

## Hecho
- Se ejecutó la recuperación híbrida RAG donde el léxico manda y lo semántico rescata el hueco (commit b96f824).
- Se midió la carga del sistema en 2.32, superando el umbral de 2.0, detectado por los bucles afinador y curador.
- Se identificaron 5 repeticiones del hallazgo en transformers:herramientas/medir_tokens.py.
- Se registraron 4 conversaciones sin firmar: 1 en charla-base y 3 en charla-web.
- Se completaron 20 commits hoy, incluyendo fixes de sintesis, telemetría y el cerebro principal del rack.

## Lo siguiente
- Implementar la firma ED25519 al canal, ya que las 6 conversaciones actuales tienen user_hash vacío y el flujo promete que todo se firma.
- Resolver el bloqueo de la feature 'espacio-impresion3d' esperando la aparición de la impresora en hexelion-nexo/sensores/.
- Decidir la regla de identificadores de terceros para desbloquear 'espacio-osint-pasivo', respetando la regla de una feature a la vez.
- Mantener la carga por debajo de 2.0, ya que actualmente está en 2.32 y los bucles afinador y curador la están monitorizando.

## Lo que NO se sabe
- NO_DATA: la impresora no aparece en hexelion-nexo/sensores/ (bloquea espacio-impresion3d).
- NO_DATA: la cripto se trata aparte, cuando se haga el DASHBOARD DE HEXELION, y queda completamente fuera de web y app (bloquea depin-keyless).
