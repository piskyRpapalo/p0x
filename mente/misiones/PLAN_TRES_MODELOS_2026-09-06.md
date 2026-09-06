# Los tres modelos, la Comunidad y el LoRAtelier · plan adaptado

**Qué es esto.** La visión la firmó el Soberano el 2026-09-06 (pirámide de tres modelos, fusión
MySpace+Tablón, perfil de tres clicks, LoRAtelier como taller). Este documento **no la sustituye**: le
pega al lado lo que el rack dice hoy, medido, y reordena lo que la verificación obliga a reordenar.

**Nada de esto está implementado.** Silicio propone, carbono firma.

---

## 1 · Lo asumido contra lo medido

Seis supuestos del documento, comprobados el 2026-09-06 contra el rack real. Tres se sostienen, dos
se caen y uno cambia de forma.

| Supuesto | Veredicto | Lo que dice el terreno |
|---|---|---|
| «El mini-modelo necesita **apartado propio en la web**» | ❌ **no cabe** | El presupuesto de páginas está **lleno: 9 de 9**. `test_maximo_ocho_paginas` cuenta benchmark, community, index, instalar, onboarding, playground, profile, hitos y manifiesto. |
| «El cuentacuentos **se sirve desde el rack**» | ❌ **hoy imposible** | `rack.js` lo dice en su cabecera: *«TODO: túnel cloudflare pendiente»*. Lo único que funciona es `localai.js`, que habla con **el Ollama del propio visitante** en `127.0.0.1:11434`. Sin túnel, un visitante nuevo y sin Ollama no tiene con quién hablar. |
| «Contribución inmutable con firma, nick mutable» | ⚠️ **con grieta** | La firma Ed25519 **ya existe** (`auth.js`: firma de 64 bytes, `ed25519:<128 hex>`). Pero el apodo **se deriva del hash de la clave pública**. Cambiar de nick sin cambiar de clave no está soportado hoy; cambiar de clave rompe el vínculo con lo firmado antes. |
| «El mini-modelo cabe en un teléfono de 4 GB» | ⏳ **NO_DATA** | Plausible pero **sin medir**: el modelo más pequeño instalado son 2,0 GB (`llama3.2:3b` Q4). En 4 GB dejaría ~2 GB para el sistema. El instrumento para medirlo existe — el Doogee S110 por cable. |
| «El Soberano ya ha entrenado LoRAs» | ✅ **cierto** | `preceptor-lora/` con `forja/`, `datos/` y 803 MB en `salida/`. El nodo afina por CPU en 553 s y 445 s (medido, dos líneas). |
| «Comunidad y Perfil son dos cosas hoy» | ✅ **cierto** | `community.html` (5,5 KB) y `profile.html` (6,9 KB) existen por separado. |

**El tope por fichero ya no es 10 KB, son 16 KB** (`TOPE_FICHERO`), más 50 KB para sprites y 30 KB
para láminas. Cualquier plan escrito contra los 10 KB viejos está calculando mal el espacio.

---

## 2 · La fusión no es cosmética: es la que abre el hueco

El documento pide dos cosas que parecen independientes — fusionar MySpace con el Tablón, y dar
página propia al mini-modelo — y el presupuesto de páginas las convierte en **una sola jugada**:

> `community.html` + `profile.html` fusionadas = **una página liberada**, que es exactamente la que
> el mini-modelo necesita. 9/9 sigue siendo 9/9.

Esto invierte el orden del documento. La fusión deja de ser trabajo de la sección de Comunidad y
pasa a ser **el desbloqueo del Modelo Dos**. Si no se fusiona, el mini-modelo entra dentro de una
página existente o hay que pedir amnistía firmada — que es legítimo, pero es una decisión, no un
trámite.

*Defecto encontrado de paso:* el test se llama `test_maximo_ocho_paginas` y afirma `<= 9`. El nombre
y la aserción dicen cosas distintas; una de las dos miente sobre el presupuesto vigente. No lo toco:
el presupuesto lo firma el Soberano.

---

## 3 · El orden real, y por qué no es el del documento

El documento ordena base → mini → cuentacuentos por dependencia conceptual. El terreno impone otro
orden, por **dependencia de infraestructura**:

```
   túnel al rack ─────────────┐
   (no existe)                ▼
                       CUENTACUENTOS ── bloqueado hasta el túnel
   fusión Comunidad+Perfil ──▶ hueco de página ──▶ MINI-MODELO
   catálogo plural ─────────▶ MODELO BASE ── se puede empezar hoy
```

- **Modelo Base: empezable hoy.** No depende de nada que falte.
- **Mini-modelo: depende de la fusión**, no del entrenamiento. Entrenarlo se puede hacer en
  paralelo; publicarlo necesita el hueco.
- **Cuentacuentos: bloqueado.** Y el bloqueo no es de modelo, es de red.

---

## 4 · Modelo Uno · las bases plurales

**Se sostiene entero.** El catálogo plural ya tiene dónde vivir: `modelos.json` alimenta la página
Instalar, que *deriva* el catálogo en vez de escribirlo a mano.

Lo que el documento pide y todavía no existe: **la pregunta en vez de la lista**. «Qué hardware
tienes, qué quieres hacer, aquí están los dos o tres que caben.» Eso es un filtro sobre el catálogo
existente, no un catálogo nuevo.

**Reutilizar, no reinventar:** el Vector de Estado Soberano ya sabe medir el hardware local
(RAM disponible, temperatura, backend, modelos cargados) y ya declara `NO_DATA` con causa cuando no
puede. La recomendación por hardware debe salir de ahí, no de un segundo medidor.

**Y hay una honestidad que el documento pide y el rack ya tiene escrita:** la recomendación se apoya
en lo medido; lo que no se pueda garantizar, se dice. El dictamen determinista del enrutador es el
patrón — aritmética sobre lo medido, y el modelo solo redacta.

## 5 · Modelo Dos · el mini-modelo

**El nicho es real y está desatendido.** La dignidad que el documento le reclama —«no es un modelo
menor, es un modelo para un hardware que la industria ignora»— es la tesis del producto y no se
negocia.

**Lo que hay que medir antes de prometer nada**, y en este orden:

1. **Cuánto cabe de verdad en el Doogee.** No «4 GB» en abstracto: el teléfono concreto, por cable,
   con el modelo cargado, midiendo tok/s y si el sistema lo mata. Sin ese dato, la promesa de la web
   es humo.
2. **Qué base.** El documento dice bien que da igual el nombre. Lo que no da igual es que el
   resultado tenga identidad PreceptorOS: doctrina dentro, `NO_DATA` cuando no sabe. Eso ya existe
   como LoRA medido — `preceptor-cazanido-v3:llama3.2` responde `NO_DATA.` en cuatro tokens, en
   castellano y sin razonamiento a la vista.
3. **Firma y hash del artefacto descargable.** El mecanismo ya existe en la web (Ed25519 en
   `auth.js`); lo que falta es aplicarlo a un binario de modelo, no a un texto.

**La deuda conocida que hay que respetar:** `preceptor-cazanido-v2:latest` sigue instalado y roto por
escrito. Un producto que nace en un catálogo con entradas muertas nace confuso.

## 6 · Modelo Tres · el cuentacuentos

**Bloqueado por red, no por modelo.** Y merece decirse claro porque cambia qué se puede empezar:

Hoy `localai.js` habla con el Ollama **del visitante**. Un recién llegado —que es exactamente el
público del cuentacuentos— no tiene Ollama. Así que el cuentacuentos servido desde el rack necesita
el túnel que `rack.js` declara pendiente, con su CORS resuelto en el borde.

**Tres caminos, y la elección es del Soberano:**

| Camino | Qué cuesta | Qué rompe |
|---|---|---|
| Levantar el túnel al rack | infraestructura + CORS + exponer el rack | el rack pasa a atender tráfico anónimo: superficie nueva |
| Cuentacuentos **en el navegador** (WebLLM) | modelo pequeño descargado al cliente | nada de doctrina; cuesta megas al visitante |
| Cuentacuentos **guionizado** sin modelo | barato y determinista | no es un modelo: es una historia bien escrita |

La tercera no es una rendición. El documento pide que el cuentacuentos «no invente» y «declare
honestamente lo que no es su dominio»: un guion determinista cumple las dos por construcción, y
puede ser el paso uno mientras el túnel existe o no.

**Lo que sí se puede hacer hoy sin decidir nada de lo anterior:** escribir el corpus del
cuentacuentos —doctrina, honest sensors, kill switch, Huella Soberana, LoRAtelier— porque ese texto
hace falta en los tres caminos.

## 7 · Comunidad, perfil y LoRAtelier

**La fusión** (ver §2) es el primer movimiento y el que más desbloquea. Las tres zonas que pide el
documento —feed, galería de Guerreros de Laboratorio, investigaciones abiertas— caben en la página
fusionada si el perfil aporta la identidad y el tablón el contenido.

**Los tres clicks.** El criterio de éxito es bueno porque es falsable: registrarse, declarar
hardware, contribuir. Lo que hay que verificar antes de prometerlo es **cuánto tarda de verdad la
medición automática** en la máquina más lenta del público objetivo. Si tarda más de diez minutos, el
documento ya dice qué hacer: declararlo y ofrecer continuar después. Eso es lo correcto y hay que
implementarlo, no evitarlo.

**La grieta del nick.** Hoy el apodo sale del hash de la clave pública. «Nick mutable, contribución
inmutable» exige separar las dos cosas: una identidad estable (la clave) y una etiqueta cambiante
(el nombre), con las firmas antiguas apuntando a la clave y no al nombre. Es un cambio de modelo de
datos, pequeño pero de raíz, y mejor hacerlo **antes** de que haya contribuciones firmadas que migrar.

**El LoRAtelier** es el que menos fricción tiene: la página existe, el benchmark existe, y los LoRAs
del Soberano existen de verdad en `preceptor-lora/`. Lo que falta es la transición de espectador a
creador — enseñar lo que ya se entrenó, con su medida y su fecha, junto a lo que el visitante puede
entrenar con su hardware.

## 8 · Los seis LoRAs, por objetivo

Los objetivos del documento se mantienen tal cual. Lo que se añade es **qué existe ya de cada uno**:

| LoRA | Objetivo (del Soberano) | Qué hay hoy |
|---|---|---|
| Cuentacuentos | doctrina entendida en 5 min; que el usuario quiera registrarse | corpus disperso; el LoRA Caza-Nido es la base más cercana |
| Mini-modelo | conversación útil en 4 GB, sin ciudadanos de segunda | sin medir en el Doogee |
| Adaptador de métricas | mediciones a la web en un click, firmadas | firma Ed25519 lista; falta el envío |
| Memoria | responder desde lo que el usuario dijo, no desde lo inventado | `memory.db` con FTS5 ya existe |
| Frontera | exportar contexto sin filtrar claves ni rutas, y **que se vea qué se redactó** | el guardián de higiene del repo ya hace esto para commits: mismo problema, otro dominio |
| Hardware | medir, puntuar, y celebrar al Guerrero de Laboratorio | el Vector mide el metal local hoy |

---

## 9 · Lo que necesita firma antes de empezar

1. **El presupuesto de páginas.** ¿Se fusiona Comunidad+Perfil para abrir el hueco, o se pide
   amnistía para una décima página? Y de paso: el test dice «ocho» en el nombre y «nueve» en la
   aserción.
2. **El túnel al rack.** Levantarlo es exponer el rack a tráfico anónimo. Sin esa decisión, el
   cuentacuentos no pasa del guion.
3. **Identidad frente a apodo.** Separarlos ahora es barato; después de las primeras firmas, no.
4. **Los tags pelados y el modelo roto**, antes de que el catálogo sea producto público.

## 10 · Lo que se puede empezar sin esperar a nada

- El **corpus del cuentacuentos** — hace falta en los tres caminos.
- La **medición del Doogee** — es el dato que sostiene o tumba al mini-modelo.
- El **filtro por hardware** sobre el catálogo, apoyado en el Vector que ya mide.
