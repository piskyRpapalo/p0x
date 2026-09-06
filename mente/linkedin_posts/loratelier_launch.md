# Borrador · LinkedIn · el LoRA de Atención al Público

**Estado: BORRADOR, pendiente de firma.** Y con tres correcciones al encargo que
hay que resolver **antes** de publicar, porque un post es público y este proyecto
se sostiene sobre decir cosas comprobables.

---

## ⚠️ Tres cosas del encargo que no se pueden publicar tal cual

### 1. «Primer LoRA soberano entrenado en hardware local» es falso

Este nodo ya ha entrenado LoRAs **tres veces** antes: `preceptor-cazanido` v1 y
v3, y `preceptor-v7`. Está escrito en el inventario del propio rack —*«este nodo
AFINA LoRAs por CPU en menos de diez minutos, y ya lo ha hecho tres veces»*— y
cualquiera puede verlo en el repositorio público.

Publicar «el primero» sería un error factual sobre nuestro propio trabajo, y el
peor sitio para tenerlo es el post donde presumimos de medir.

**Lo que sí es primero:** el primer LoRA de **utilidad pública** del LoRAtelier
—los anteriores eran de doctrina interna y de métricas— y el primero con **dos
datasets comparativos** para medir el efecto de la lengua.

### 2. «Sin alucinaciones» no se puede afirmar, y menos antes de medir

Es una promesa absoluta y no la sostiene ninguna medición. Además, cuando se
escribe esto el entrenamiento **está corriendo**. Lo que sí se puede decir es
concreto y más fuerte: *qué le prohibimos decir, y cómo se comprueba*.

### 3. El enlace no existe

`github.com/piskyRpapalo/preceptor-lora` da 404: `preceptor-lora` es una carpeta
dentro del repositorio `p0x`, que sí es público. O se enlaza a `p0x`, o se saca
la carpeta a repositorio propio antes de publicar.

---

## Borrador corregido

> **Título:** Un LoRA de atención al cliente entrenado en un mini PC — y la regla
> que le prohibimos romper

Entrenamos un adaptador LoRA para atender reclamaciones de consumidores. No en
la nube: en un mini PC de sobremesa, sobre CPU, con un modelo europeo de licencia
Apache 2.0.

Lo interesante no es que quepa en el hardware. Es lo que le enseñamos a **no**
hacer.

**La regla de los plazos.** El 15 % del corpus son dudas del tipo «¿cuánto tiempo
tengo para reclamar?». El modelo tiene prohibido responder con un número. Los
plazos cambian por país y por sector, y un dato dicho con aplomo puede costarle a
alguien su reclamación. Así que nombra el canal —hoja de reclamaciones, oficina
de consumo, arbitraje— y manda a confirmarlo en la fuente oficial.

Decir «no lo sé, y sé quién sí» es más útil que acertar ocho de cada diez veces.

**Las otras tres conductas**, cada una contra una avería concreta de los bots de
atención que todos hemos sufrido:

- No inventar política. Si la norma no consta, se dice que no consta — en vez de
  citar una «política 4.2» que no existe.
- Escalar de verdad: a una persona, con referencia y plazo. No devolver a la
  misma cola por cuarta vez.
- No pedir datos sensibles por chat. Ni tarjeta, ni documento, ni claves —
  aunque el cliente los ofrezca primero.

**Dos datasets, no uno.** 200 muestras en total, con el mismo reparto: 50 % casos
estándar, 20 % casos límite, 15 % dudas al reclamar, 15 % doctrina. Uno entero en
inglés; el otro repartido en seis lenguas (40 % español, y el resto entre
portugués, francés, italiano, griego e inglés). El tramo inglés del segundo es
idéntico al del primero **a propósito**: así la comparación mide la lengua y no
dos redacciones distintas.

Los repartos no se declaran en un comentario: los comprueba una aserción al
generar. Un reparto escrito y desmentido por el fichero es peor que no tenerlo.

**El coste, medido.** [PENDIENTE — rellenar al terminar: s/paso, minutos totales,
pico de RAM, pico de temperatura y pérdida inicial → final de cada dataset.]

**Lo que falta**, y se dice porque forma parte del método: el artefacto no está
publicado, así que todavía no hay botón de descarga. Sin firma y sin hash
verificable no se ofrece nada.

🔗 [PENDIENTE — enlace: `p0x`, o `preceptor-lora` si se saca a repo propio]

---

## Notas para el Soberano

- El gancho más fuerte es **la regla de los plazos**, no el hardware. «Un modelo
  al que le prohibimos dar una fecha» se lee y se recuerda; «entrenado en local»
  lo dice todo el mundo.
- Los dos huecos `[PENDIENTE]` son deliberados: uno espera a la medición que está
  corriendo, el otro a tu decisión sobre el repositorio.
- Sin «disruptivo» ni «revolucionario», como pediste. Tampoco «democratizar».
- Si el post lleva captura, la del LoRAtelier con los bloques en «en
  entrenamiento» y sin botón de descarga dice más que una de código: enseña que
  no se ofrece lo que aún no se puede comprobar.
