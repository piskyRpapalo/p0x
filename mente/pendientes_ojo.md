# Pendientes del Ojo · anotado 2026-09-07

## 1 · El panel no se levanta solo, y eso hace que parezca que no existe

El canon manda arrancar toda sesión por el Ojo. Hay **dos formas de llamarlo y
no son la misma**:

- `python3 ~/p0x/Alejandria/ojo/ojo.py --arranque` → funciona siempre.
- `http://127.0.0.1:8790/api/arranque` → **000**. No hay unidad systemd que lo
  levante (`systemctl --user list-units --state=running` no lista ninguna).

Una sesión que pruebe primero por `curl` concluye que el Ojo no está y sigue sin
él. Anotado en `recursos.json` para que la próxima use el CLI.

**No se ha creado ninguna unidad systemd**: el canon exige firma explícita para
cada una, una por una, y esta no la tiene. Queda propuesto, no hecho.

## 2 · El Ojo-Vivo no se ha podido verificar

`/vivo` cuelga del mismo servidor que no corre, así que **no hay medida** de si
sus widgets están frescos o estancados. Decir que están bien sería inventar; y
decir que están mal, también. `NO_DATA` hasta que alguien lo arranque.

## 3 · Los modelos nuevos no están en el glosario

`--arranque` no menciona `preceptor-charla-base:v1` ni
`preceptor-charla-multi:v1`, entrenados esta madrugada. No se ha tocado el
glosario **a propósito**: la Prueba de Fuego salió NO-GO, y meter en el save
game unos modelos que no sirven todavía sería exactamente el ruido que el Ojo
existe para evitar. Se añaden cuando pasen, con su medida al lado.

## 4 · Lo que este inventario ya sabía y yo no leí

Esta sesión pisó **cinco** trampas que `recursos.json` ya tenía escritas:

- «El pie de banco de `pkill -f`: la sesión se mata sola» — me mató mi propio
  comando (código 144).
- «Una regla CSS puede estar escrita y no mandar nunca» — el `margin-left:auto`
  sin hueco que repartir.
- «Una hoja nueva no la carga quien tú crees» — la partición de `esquina.css`.
- «Al partir por el tope, la prueba que nombra un fichero se rompe» — el arnés
  del worker, que fijaba 98 rutas a mano.
- «La trampa del service worker» — perdí medidas creyendo que un arreglo no
  funcionaba, con el CSS viejo en caché.

**El fallo es de método, no del inventario:** no corrí el Ojo al arrancar. La
regla existe justamente porque cada sesión empieza en frío, y esta lo demostró
pagando cinco veces por escrito lo que ya estaba pagado.
