# 05 · EL SWAP DE LAS DOS PIELES — instrucción de deploy (fragua)

Sesión de deploy con la mano del carbono (o misión con mandato explícito en fragua).
**Propose-only desde soberano: nada de esto se ejecuta por SSH desde aquí.**
Ley de la misión: **backup previo + Playwright verde ANTES del swap**. El swap es opt-in
por env (`UI_CARA=dos-pieles`) — sin la env, todo lo legado sigue intacto.

Commits que viajan (hexelion.git, rama `nexo-carbono-dashboard-20260623`):
`2791c7f` (mounts, item 01) · `60d2023` (alias /jardin, fix item 01) · `abec9e0`
(/api/jardin/notes, item 04) · `1fa2ea1` (dist versionado + puertas 172/172).

## Paso 0 · Backup (obligatorio, antes de tocar nada)

```bash
cd /home/ubuntu/hexelion
cp hexelion_gateway.py hexelion_gateway.py.bak-dos-pieles
sha256sum hexelion_gateway.py.bak-dos-pieles   # anotar en el cuaderno de deploy
```

## Paso 1 · Traer el código

**Si `/home/ubuntu/hexelion` es checkout de `hexelion.git`** (comprobar con `git -C . remote -v`):

```bash
git fetch && git checkout nexo-carbono-dashboard-20260623 && git pull
```

**Si NO es checkout** (copia viva divergente — *sin dato desde soberano de cuál es el caso*):
aplicar los patches del paquete **en orden** y traer el dist de un clone aparte:

```bash
git apply --check 01-serve-from-git.patch && git apply 01-serve-from-git.patch
git apply --check 04-jardin-notes.patch  && git apply 04-jardin-notes.patch
# dist: rsync desde un clone del repo (dashboard/dist -> /home/ubuntu/hexelion/dashboard/dist)
```

```
VERIFICACIÓN ▸ python3 -m py_compile hexelion_gateway.py && echo OK
EXPECT      ▸ OK
VERIFICACIÓN ▸ (cd dashboard/dist && sha256sum -c /ruta/al/paquete/05-SHA256SUMS)
EXPECT      ▸ 17 líneas «OK», cero «FAILED»
```

## Paso 2 · Restart SIN swap — lo legado intacto, las pieles en /ui/

```bash
sudo systemctl restart <unit-del-gateway>   # nombre real del unit en fragua: sin dato desde soberano
```

```
VERIFICACIÓN ▸ curl -so /dev/null -w '%{http_code}\n' http://127.0.0.1:8001/ui/
EXPECT      ▸ 200
VERIFICACIÓN ▸ curl -s http://127.0.0.1:8001/ui/jardin.html | grep -c 'lang="fr"'
EXPECT      ▸ 1
VERIFICACIÓN ▸ curl -so /dev/null -w '%{http_code}\n' http://127.0.0.1:8001/dashboard
EXPECT      ▸ 200 (y sigue siendo el dashboard VIEJO — el swap aún no existe)
VERIFICACIÓN ▸ curl -s http://127.0.0.1:8001/api/jardin/notes
EXPECT      ▸ {"notes": [], "total": 0, ...} (vacío honesto — el endpoint ya vive)
```

**Puerta Playwright:** la suite corre en soberano sobre el MISMO dist que se despliega
(`1fa2ea1`): 172/172, 0 flaky, registrado en `mente/telemetria/PLAYWRIGHT_DOS_PIELES.md`.
Si el dist de fragua pasa el `sha256sum -c` de arriba, es ese mismo build verificado.

## Paso 3 · El swap (solo si el Paso 2 rindió todos sus EXPECT)

```bash
sudo systemctl edit <unit-del-gateway>      # añadir: Environment=UI_CARA=dos-pieles
sudo systemctl restart <unit-del-gateway>
```

```
VERIFICACIÓN ▸ curl -s http://127.0.0.1:8001/dashboard | grep -c '/ui/assets/'
EXPECT      ▸ ≥1 (el Nexo nuevo)
VERIFICACIÓN ▸ curl -s http://127.0.0.1:8001/jardin/ | grep -c 'lang="fr"'
EXPECT      ▸ 1 (el marcador de Krista vive — alias del fix 60d2023)
VERIFICACIÓN ▸ curl -s http://127.0.0.1:8001/tareas | grep -c '/ui/assets/'
EXPECT      ▸ ≥1 (la Bandeja Ejecutiva nueva)
VERIFICACIÓN ▸ curl -so /dev/null -w '%{http_code}\n' http://127.0.0.1:8001/indoor
EXPECT      ▸ 308 (y su Location /jardin/ resuelve 200)
```

Prueba de humo del Cahier (crear y leer una nota real):

```
VERIFICACIÓN ▸ curl -s -X POST http://127.0.0.1:8001/api/jardin/notes \
                 -H 'Content-Type: application/json' \
                 -d '{"id":"deploy-humo","titre":"Essai","corps":"Note du déploiement.","fecha":"2026-07-19T00:00:00Z"}'
EXPECT      ▸ {"ok": true, "total": 1}
VERIFICACIÓN ▸ curl -s http://127.0.0.1:8001/api/jardin/notes | grep -c deploy-humo
EXPECT      ▸ 1  (y el archivo verde/cahier_notes.json existe en el suelo local)
```

## Rollback (un gesto)

```bash
sudo systemctl edit <unit-del-gateway>      # quitar la línea UI_CARA
sudo systemctl restart <unit-del-gateway>   # todo lo legado vuelve tal cual
```

El backup del Paso 0 cubre además el caso patch-corrupto: `cp` de vuelta y restart.
