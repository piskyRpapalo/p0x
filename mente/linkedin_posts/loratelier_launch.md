# Borrador · LinkedIn · The Tribune

**Estado: BORRADOR, pendiente de firma.** Incorpora los cuatro ajustes firmados
el 2026-09-06 y las cifras ya medidas del primer entrenamiento.

---

## ⚠️ Un aviso técnico que hay que resolver antes de prometer descargas

`preceptoros.org` responde **200 y va por Cloudflare** (`server: cloudflare`).
Si el sitio se sirve con **Cloudflare Pages**, el límite es **25 MiB por
fichero** — y cada adaptador pesa **52 MiB**. El despliegue lo rechazaría, y lo
haría en silencio desde el punto de vista de quien mira la web.

Tres salidas, y la tercera es la que más se parece a lo que este proyecto dice
ser:

1. **R2** (el almacenamiento de objetos de Cloudflare), que existe justo para
   esto y no tiene ese tope.
2. Partir el fichero. Funciona y es feo: obliga a quien descarga a recomponerlo.
3. **Servirlos desde el rack**, por el túnel que ya existe y ya contesta
   (`api.preceptoros.org`). Es la opción soberana de verdad: el artefacto sale
   de tu máquina, no de un CDN ajeno. Y el día que el rack se apague, la
   descarga se apaga con él — que es honesto, no un defecto.

Mientras no se decida, el bloque se queda en `en_entrenamiento` y **no hay
botón**, que es lo que ya hace el registro.

**Lo que no está roto**, comprobado uno a uno: el dominio, la API del Ágora, los
cuatro enlaces de GitHub y los scripts de instalación. LinkedIn devuelve 999,
que es su antibot y no un enlace roto. El único 404 es `/downloads/`, y es
esperado: los ficheros aún no están.

---

## Borrador

> **Título:** El primer LoRA de utilidad pública de LoRAtelier: un tribuno para
> reclamaciones

Hemos entrenado el primer adaptador LoRA de utilidad pública para LoRAtelier. Se
llama **The Tribune**, y el nombre no es decorativo: el tribuno de la plebe
existía para interponerse entre un ciudadano corriente y un magistrado que le
hacía daño. Eso es exactamente lo que hace.

Lo interesante no es que quepa en un mini PC. Es lo que le enseñamos a **no**
hacer.

**La regla de los plazos.** El 15 % del corpus son dudas del tipo «¿cuánto
tiempo tengo para reclamar?». El modelo tiene prohibido responder con un número.
Los plazos cambian por país y por sector, y un dato dicho con aplomo puede
costarle a alguien su reclamación. Así que nombra el canal —hoja de
reclamaciones, oficina de consumo, arbitraje— y manda a confirmarlo en la fuente
oficial.

Decir «no lo sé, y sé quién sí» es más útil que acertar ocho de cada diez veces.

**Está entrenado con la doctrina Honest Sensors**: declara `NO_DATA` cuando no
sabe, y nombra la clave que le falta en vez de rellenarla.

**Las otras tres conductas**, cada una contra una avería concreta de los bots de
atención que todos hemos sufrido:

- No inventar política. Si la norma no consta, se dice que no consta — en vez de
  citar una «política 4.2» que no existe.
- Escalar de verdad: a una persona, con referencia y plazo. No devolver a la
  misma cola por cuarta vez.
- No pedir datos sensibles por chat. Ni tarjeta, ni documento, ni claves —
  aunque el cliente los ofrezca primero.

**Dos datasets, no uno.** 200 muestras con el mismo reparto: 50 % casos
estándar, 20 % casos límite, 15 % dudas al reclamar, 15 % doctrina. Uno entero
en inglés; el otro repartido en seis lenguas (40 % español, y el resto entre
portugués, francés, italiano, griego e inglés). El tramo inglés del segundo es
idéntico al del primero **a propósito**: así la comparación mide la lengua y no
dos redacciones distintas.

Los repartos no se declaran en un comentario: los comprueba una aserción al
generar.

**El coste, medido en un mini PC de sobremesa** (Ryzen 7, 8 hilos, sin GPU
dedicada, base Mistral 7B en bf16 y licencia Apache 2.0):

- 200 pasos · **5,55 s por paso** · 18,5 min de cálculo
- pérdida **3,80 → 0,62**
- RAM pico **19,1 GB**
- temperatura máxima **84,4 °C**, con 62 pausas térmicas automáticas
- **39 minutos de reloj**, pausas incluidas

Sobre esa pérdida conviene una cautela, y la decimos nosotros antes que nadie:
una caída así con 100 muestras puede ser aprendizaje o puede ser sobreajuste. La
curva no lo distingue. Lo dirán los casos que el modelo no ha visto.

**Lo que falta**, y se dice porque forma parte del método: el artefacto todavía
no está publicado. Sin hash verificable no se ofrece descarga.

🔗 Código: github.com/piskyRpapalo/p0x (el LoRAtelier vive en `preceptor-lora/`)
✉️ davidpecero@gmail.com

---

## Notas para el Soberano

- El gancho es **la regla de los plazos**, no el hardware.
- Sin «disruptivo», «revolucionario» ni «democratizar».
- La cautela sobre el sobreajuste es deliberada: decirla nosotros vale más que
  que la diga un comentarista. Y encaja con lo que el producto predica.
- Falta rellenar las cifras del dataset multilingüe: se está entrenando mientras
  se escribe esto.
- El email es el temporal firmado. Cuando el dominio sirva correo, se cambia
  aquí y en `downloads/README.md`, que son los dos sitios donde está escrito.
