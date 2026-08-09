# Verificación del guardia — 2026-08-09

Ronda CARAS-PUBLICAS-1 · Bloques 1 y 4. Un freno que no se prueba es una
suposición. Esto es lo que se probó y lo que salió.

## Instalación

Los ganchos de git no se versionan solos. La fuente vive aquí y se copia a cada
repositorio con `bin/p0x-instalar-ganchos`. Antes de esta ronda el gancho
existía **solo en `p0x`** y solo como `pre-commit`.

```
$ bin/p0x-instalar-ganchos ~/hexelion ~/aurelius ~/cinek_automatico
✅ hexelion — pre-commit + pre-push instalados en …/hexelion/.git/hooks
✅ aurelius — pre-commit + pre-push instalados en …/aurelius/.git/hooks
✅ cinek_automatico — pre-commit + pre-push instalados en …/cinek_automatico/.git/hooks

$ bin/p0x-instalar-ganchos --verificar ~/p0x
✅ p0x/pre-commit al día
✅ p0x/pre-push al día
✅ p0x/guardia_higiene.py al día
```

El `pre-commit` anterior de `p0x` se conservó como `pre-commit.previo`.

## Casos de prueba del escáner

`test_guardia.py`: prosa doctrinal que **debe pasar** frente a formas de
dirección, IPs, rutas, dominios y claves que **deben bloquear**.

```
$ python3 deploy/comun/hooks/test_guardia.py
RESULTADO: 63/63 casos correctos, 0 fallo(s)
```

## El falso positivo que motivó la reparación, medido

El gancho anterior buscaba `\b(soberano|fragua|beato|hexelion|pisky)\b` sin
distinguir mayúsculas. Sobre el corpus de doctrina:

```
$ git ls-files mente/doctrina | wc -l
12
$ git ls-files mente/doctrina -z | xargs -0 grep -liE \
    "\b(soberano|fragua|beato|hexelion|pisky)\b" | wc -l
11
$ git ls-files mente/doctrina -z | xargs -0 python3 \
    deploy/comun/hooks/guardia_higiene.py --files | wc -l
0
```

**11 de 12 ficheros bloqueados antes, 0 ahora, y 0 fugas reales en esa
carpeta.** El freno viejo bloqueaba doctrina limpia; el nuevo no.

## Bloqueo provocado a propósito, repo por repo

Fichero de prueba con una línea de prosa doctrinal legítima y tres fugas
reales. Mismo resultado en `hexelion`, `aurelius` y `cinek_automatico`:

```
$ git add _PRUEBA_GUARDIA.md && git commit -m "prueba guardia"
=== GUARDIA DE HIGIENE · pre-commit ===
❌ BLOQUEADO: fuga de infraestructura en lo staged
_PRUEBA_GUARDIA.md:3: [NODO-USER-AT] …
_PRUEBA_GUARDIA.md:4: [IP-TAILNET] …
_PRUEBA_GUARDIA.md:5: [RUTA-HOME] …
rc=1
```

La línea 2 —«La Torre y el Soberano son léxico de doctrina»— **no** disparó
ninguna regla, que es exactamente el punto. Ningún commit nuevo quedó en los
tres repos, y el fichero de prueba se borró después.

## El caso que se escapó: fuga en medio del rango

`pre-push` revisa el rango completo, no el último commit. Probado de extremo a
extremo contra un remoto local desechable: base publicada, luego un commit
limpio, un commit con fuga colado con `--no-verify`, y un commit limpio encima.

```
$ git push origin master
=== GUARDIA DE HIGIENE · pre-push ===
· refs/heads/master: revisando 3 commit(s) del rango
❌ BLOQUEADO: fuga de infraestructura en el rango de refs/heads/master
c.md:1: [IP-TAILNET] …
error: failed to push some refs to '../remoto.git'
rc=1

$ git --git-dir=../remoto.git log --oneline -1 master
1666bac c1 limpio        ← el remoto no se movió
```

La punta estaba limpia y aun así el empuje se bloqueó, por la fuga enterrada en
el commit del medio.

## Lo que el guardia todavía no ve

- **Destinos de enlaces simbólicos.** Lee contenido, no `readlink`. Hay al
  menos un caso publicado (`mente/codice/CODICE_david.md` → ruta absoluta de un
  nodo anterior).
- **Ficheros binarios.** Solo texto.
- **`--no-verify`.** No deja rastro. Es un agujero por diseño de git.
- **Historial ya publicado.** El gancho mira lo que sale, no lo que ya salió.
