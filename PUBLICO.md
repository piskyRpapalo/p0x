# Esta rama es la idea. La lógica no está aquí, y es a propósito.

`publico` lleva la **doctrina, el diseño y los datos que lo explican** —`.md` y
`.json`— y **no lleva ni un fichero ejecutable**: nada de `.py`, `.sh`, `.js`,
`.service` ni `.timer`. Son 475 ficheros de 655; los 180 que faltan son la
lógica, y viven en el host git soberano del rack, no aquí.

## Por qué

Un bucle con una unidad systemd detrás no es un ejemplo de código: es algo que
corre solo, con permisos, en una máquina concreta. Publicarlo no enseña la idea
—la idea está escrita— y sí reparte el mapa de una casa. Lo que merece leerse es
**por qué** está hecho así, y eso sí está entero en `mente/` y en los `README`.

## Lo que esta rama NO consigue, y conviene decirlo

Hasta el 2026-09-13 esta lógica **sí estuvo publicada**. Retirarla del HEAD no la
despublica: sigue en el historial de este repositorio, y en cualquier fork o
caché que exista. Esto hace que lo VISIBLE sea la idea; no borra el pasado, y
presentarlo como si lo hiciera sería exactamente la clase de cifra cómoda que
este proyecto existe para no publicar.

## Cómo se mantiene

`master` es la rama completa y va al host soberano. `publico` se reconstruye
desde ella quitando los ejecutables por extensión —una regla que se comprueba,
no un criterio que se recuerda— y es la única que se empuja aquí. El push de
`master` a este remoto está bloqueado en la configuración local del nodo.
