# Traspaso · sesión del 2026-09-05

**Gates al cerrar:** `preceptor/bin/pruebas` → **VERDE 617/617** ·
`preceptoros-web/test_web.py` → **76/76**. Los tres repos empujados, cero
pendientes.

**Servidor de pruebas de la web.** Se levanta desde `~/preceptoros-web` con
`nohup python3 -m http.server 8118 --bind 0.0.0.0 --directory public &`, y se
abre desde el móvil con la dirección del nodo en la tailnet —`tailscale ip -4`—
o la del wifi —`hostname -I`—, seguida de `:8118/es/`. Las direcciones no se
escriben aquí: la guardia de higiene las bloquea, y con razón.

**No es el sitio desplegado.** `preceptoros.org` va por detrás y ahí no se ve
nada de lo de hoy. Esa confusión ya costó tres capturas.

---

## Lo hecho, en una línea cada cosa

**App** · el harness lee la base (`herramientas.py`, recuperación inyectada) y
los dos gestos de escritura —botón sobre el turno y formulario del cajón—
escriben por `/api/anidar` con `origen: persona`. Comprobado en metal: turno →
guardar → el turno siguiente contesta «Vera.», y la app no guarda historial, así
que la única vía es la recuperación.

**Techo por fichero** · sube de 10 KB a **16 KiB**, medido y canonizado en
`METRICAS_NORMA.md` v1.1.0. Con `test_ningun_fichero_gasta_medio_viaje_de_red`
vigilando el cable de verdad.

**Web** · cinco capas, cabezal nuevo, dos paneles, cara de la app, atajos
fusionados en una fila, telón, capas 2 y 5.

---

## LO QUE FALTA · empezar por aquí

### 1 · Desplegar
Nada de lo de hoy está en `preceptoros.org`. Es lo primero: el Soberano está
mirando el sitio desplegado y ve la versión de antes.

### 2 · Las transparencias, comprobadas en el móvil de verdad
Están escritas (`color-mix` sobre `--glass-solid` al 62 %, y los desplegables al
78 %) y verificadas en el navegador del arnés. **Falta verlas en el Doogee**: el
`backdrop-filter` se comporta distinto ahí y el respaldo opaco tiene que
aguantar. Si no se ve el fondo a través, mirar primero si `@supports` está
cayendo al respaldo.

### 3 · La secuencia de despertar, la que pidió el Soberano
El telón ya está cableado con `cara-secuencia-apertura-256-telon.webp` al 770 %,
`steps(7, jump-none)` en 1,2 s y la cortina cayendo a 1,8 s — las cifras de la
app. **Lo que falta es comprobar que se ve al abrir la web**, y que la
transición del telón a la cara de reposo no da un salto.

Los masters están en `Alejandria/marca/` con su catálogo (`catalogo.json`, 20
piezas: `busto-dormido`, `busto-grieta`, `busto-rompe`, `busto-ojo`,
`busto-despierto`, `busto-corazon` para el despertar; `habla-1..4` para la boca).
Las tiras ya derivadas viven en `preceptor/assets/` y se copiaron a
`preceptoros-web/public/assets/caras/`.

### 4 · Los tres estados, ya funcionando — no volver a tocarlos
reposo 122,5 % · piensa 612,5 % · habla 490 %, con el desplazamiento 27,78 %.
**Ese 27,78 no es un centro mal puesto**: el busto viene dibujado a la izquierda
de su cuadro y al 50 % los ojos quedan descentrados respecto del aro. Firmado en
la app el 2026-09-04.

### 5 · Los idiomas
**Portugués: HECHO** (2026-09-05). Cuarta lengua, entera y en verde. Se armó
fuera de `public/` y se movió de una vez, así que el gate no estuvo rojo por una
lengua a medias ni un momento — que es la lección que `LEEME-pt.md` dejó escrita.

El bloqueo que aquel documento anunciaba como «el hallazgo que vale para las
cuatro lenguas siguientes» **ya no existe**: los «dos bloques de traducción» eran
el fragmento huérfano de i18n que se borró esa misma mañana. Traducir es traducir
un bloque.

**Faltan cuatro: italiano, alemán, ruso y griego.** Medido lo que cuesta cada
una: ~12.000 caracteres de texto visible repartidos en siete páginas, de los
cuales 6.290 son `instalar.html` sola —que no tiene bloque i18n y lleva la mitad
de sus cadenas en comandos que NO se traducen—. La receta que funcionó:

1. Armar la lengua completa en `traducciones/<idioma>/`, nunca en `public/`.
2. Copiar de `es/`, cambiar `lang`, `prompts-<idioma>.js` y las URL canónicas.
3. Traducir el bloque `id="i18n"` entero y las cadenas visibles.
4. Cablear: `prompts-<idioma>.js`, los dos anuncios, los ocho bustos, el
   selector de la raíz, el `hreflang` en TODAS las portadas, la página sin red
   de `sw.js`, y la cuenta de rutas de `arnes_sw.mjs` (sube de siete en siete).
5. Mover a `public/`, regenerar el sitemap y `coherencia-publica.py --si`.

El selector de la rueda ya NO hay que tocarlo: descubre las lenguas de las
etiquetas `hreflang` de la propia página.

**Y una advertencia sobre ruso y griego:** son las dos que no puedo revisar. La
copia de producto mal traducida en un sitio público es peor que no tenerla.

### 6 · El catálogo de compañeros está solo en castellano
`hub.json` lleva UN `name` y UNA `function` por agente, sin variantes por idioma:
«El Instalador» sale igual en la portada inglesa, la francesa y la portuguesa.
**No lo trajo el portugués — ya pasaba.** Arreglarlo son 8 agentes × N idiomas en
un fichero que tiene sus propias pruebas, y es decisión de contenido: puede que
los nombres sean nombres propios y no deban traducirse.

---

## Tres trampas que mordieron hoy

1. **El caché del navegador enseña código viejo.** Pasó cinco veces. Lo que se ve
   no es lo que hay en disco hasta que se sirve desde un puerto nuevo.
2. **Los guardianes leen los comentarios como si fueran código.** Nombrar
   `text-shadow` en una frase que explica por qué NO se usa pone el gate rojo.
   Igual con palabras de cuatro mayúsculas en `interface/` y con `NO_DATA`, que
   no es una política declarada.
3. **Un oyente que revienta firma el crimen con el nombre de quien lo disparó.**
   Un `insertBefore` mal apuntado en un oyente de `hub:listo` salía atribuido a
   la línea del `dispatchEvent`, en otro fichero y doscientas líneas más allá.
