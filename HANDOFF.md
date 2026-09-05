# Traspaso · sesión del 2026-09-05 (noche)

**Gates al cerrar:** web `test_web.py` **76/76** · `arnes_sw.mjs` **21/21** ·
app `bin/pruebas` **617/617**. Los tres repos empujados, cero pendientes sin
commitear.

**Lee primero:** [`INVENTARIO.md`](INVENTARIO.md) — cada parte de la web y de
la app, con sus secciones, sus visuales y dónde vive cada cosa. Y
`~/preceptoros-web/docs/ESTADO.md` para el trabajo de GitHub.

---

## Lo hecho esta noche, en una línea cada cosa

**Un solo marco** de bronce engloba el lugar de trabajo entero. Eran tres
cajas con mármol entre medias.

**El botón de Herramientas ya no existe.** Sus ocho nubes bajaron al cuadro de
especificaciones, donde se ven sin pulsar nada. Retirar el mando no bastaba: el
router seguía plegándolas al arrancar y quedaron invisibles con contenido
dentro.

**El cabecero, por esquinas.** Escritorio: marca izquierda, rueda e identidad
gemelas —doradas y transparentes— en la esquina derecha. Teléfono: dos
renglones, marca con sus iconos y debajo la cuenta con la rueda.

**La esfera dejó de apagarse.** La traslucidez era una línea literal
(`opacity:.55` al escribir). Ahora se enciende en neón al pensar y saca la nube
«Activando modelo».

**La declaración solar es una pila que se carga**, dibujada en un
pseudo-elemento, sin una sola etiqueta nueva.

**Teclado abierto:** `visualViewport` publica el alto real y la página se
reparte en columna. `dvh` no servía — en Android el teclado se dibuja encima
sin encoger la ventana.

**Un despertar por sesión**, y la app instalada deja de preguntar el idioma
cada vez.

**Los dos README**, en inglés, con la voz del Soberano: para quién se escribe
GitHub, la soberanía de la corriente, el rack como laboratorio, las dos formas
de participar, y la base de datos local explicada para quien empieza.

**Arreglado:** tres guiones que no cargaba nadie, el onboarding que prometía un
404, y el nombre del compañero que viajaba sin traducir.

---

## Las siete trampas de esta sesión

Ninguna se dedujo: todas se midieron o se vieron en pantalla.

1. **El guardián lee los comentarios como código.** Seis rojos por nombrar un
   radio o un `backdrop-filter` en la frase que explica por qué NO se usan.
2. **El caché del navegador enseña código viejo.** Media hora leyendo una regla
   que estaba en disco y no en el navegador. Puerto nuevo por tanda.
3. **El telón bloquea las capturas headless.** Se fotografía sirviendo una
   copia de `public/` sin ese bloque.
4. **Retirar un mando es retirar también lo que le obedecía.**
5. **`display:contents` anula el `order` del envoltorio.**
6. **Un `top` no gana a un margen: se suman.** Los dos mandos declaraban la
   misma altura y uno caía 11,2 px más abajo — el `margin-top` de `.fila`.
7. **Con `margin-left:auto` en dos cajas el hueco se reparte**, no se cierra.

Y una que vale por todas: **un guardián puede estar en verde protegiendo el
fallo.** El del onboarding exigía literalmente las dos URL que daban 404.

---

## Lo que queda

1. **Reordenar GitHub** — hay un prompt escrito para eso en
   `prompts/SESION_GITHUB.md`.
2. **Seguir con web y app** — prompt en `prompts/SESION_PRODUCTO.md`.
3. **Revisión nativa de ruso y griego.** Son las dos lenguas que no puedo
   revisar.
4. **Una captura con el teclado abierto en un teléfono real.** Lo de aquí está
   medido forzando `--alto-visible` en el navegador, no en metal.
5. **Los cinco arreglos propuestos** están en `INVENTARIO.md`, parte 3.
