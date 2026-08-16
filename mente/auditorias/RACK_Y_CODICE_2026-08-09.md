# Recuperación del rack y verificación del Códice — noche del 2026-08-09

Ronda CARAS-PUBLICAS-1 · Bloque 5. Esta auditoría se intentó comprometer aquella
noche y el comando falló porque el fichero nunca llegó a escribirse. Lo que solo
vive en una conversación se pierde: se escribe ahora.

## Advertencia sobre la procedencia de estos datos

**No hay transcripción de aquella sesión.** Se buscó y no existe:

```
$ git -C p0x reflog --date=iso        # ningún intento de commit de la auditoría
$ grep -nE "sha256|codice|shasum" ~/.bash_history
(sin coincidencias)
$ find ~/.claude/projects -name "*.jsonl" -newermt "2026-08-08 12:00" \
       ! -newermt "2026-08-09 12:00"
(sin resultados)
```

Los hashes se ejecutaron dentro de la sesión, no en la consola, y esa sesión no
dejó fichero. Por tanto **las salidas de abajo son de hoy, 2026-08-09, no
transcripciones de aquella noche**. Coinciden con lo que se recordaba —cuatro
hashes iguales— y son verificables ahora mismo. Lo que no se puede reconstruir
va listado al final.

## 1 · Verificación de la copia del Códice — cuatro hashes coincidentes

El Códice tiene cuatro instancias en este nodo: tres ficheros en disco y el
objeto que git tiene rastreado.

```
$ find ~ -name "CODICE_david.md" -not -path "*/.git/*" | sort | xargs sha256sum
dba72c348458be44b2e8a8de43db538fe8388918fa90eaa011be5d7bcc11be77  p0x/codice/CODICE_david.md
dba72c348458be44b2e8a8de43db538fe8388918fa90eaa011be5d7bcc11be77  pre-bee/p0x/MD 3/CODICE_david.md
dba72c348458be44b2e8a8de43db538fe8388918fa90eaa011be5d7bcc11be77  pre-bee/p0x/p0x2/CODICE_david.md

$ git -C p0x ls-files -s codice/CODICE_david.md
100644 36bea22c54cc6b591afd90e31e2054483284bf7f 0	codice/CODICE_david.md

$ git -C p0x cat-file -p 36bea22c | sha256sum
dba72c348458be44b2e8a8de43db538fe8388918fa90eaa011be5d7bcc11be77  -
```

**Cuatro hashes, uno solo distinto de los demás: ninguno.**

```
sha256  dba72c348458be44b2e8a8de43db538fe8388918fa90eaa011be5d7bcc11be77
tamaño  3075 bytes, 66 líneas
```

Las dos copias de `pre-bee/` son del árbol anterior a este nodo y siguen
byte-a-byte idénticas a la viva. La copia rastreada por git no ha derivado del
fichero en disco. El Códice no se ha corrompido en ninguno de los traslados.

### El quinto camino, que no verifica nada

```
$ ls -la p0x/mente/codice/
lrwxrwxrwx  CODICE_david.md -> /mnt/nvme/p0x/codice/CODICE_david.md  # guardia:permitir · transcrito de auditoría anterior a D34 · ruta de disco propio · 2026-08-09

$ sha256sum p0x/mente/codice/CODICE_david.md
sha256sum: … No such file or directory
```

`mente/codice/CODICE_david.md` es un enlace simbólico a una ruta absoluta de un
nodo anterior. Está **roto** en este nodo desde el traslado, y rastreado en git
como enlace (modo `120000`), lo que significa que la ruta absoluta de aquel nodo
viaja publicada dentro del repositorio. Se anota; no se toca en esta ronda.

## 2 · Estado del rack, censo de hoy

Medido con `tailscale status`. Se dan roles y estado; las direcciones se omiten
a propósito — este fichero vive en un repositorio que hoy está publicado.

| Nodo | Estado medido |
|---|---|
| Soberano | en línea (este nodo) |
| la-fragua | activa, enlace directo |
| la-torre | en línea, ociosa |
| el-vigía | en línea |
| musculo-hp-01 | **offline, visto por última vez hace 15 días** |
| musculo-hp-02 | offline, visto hace 1 día |

Concuerda con el canon: `musculo-hp-01` fue declarado INHABILITADO el
2026-08-04 llevando ya diez días fuera; hoy van quince. Sigue sin ser
recuperable por vía remota.

## 3 · Lo que se hizo aquella noche, según el registro de git

Único rastro duro que sobrevive.

```
$ git -C p0x log --since="2026-08-08 20:00" --until="2026-08-09 06:00"
f4a7ad7 2026-08-09 00:14:07  docs(canon): Misiones 7-9 (§5.1 ambiente, --nx-green fix, lápida CMP)
ae6b910 2026-08-08 23:51:27  test: fuga simulada
fcbf8f8 2026-08-08 23:34:02  fix(cinek): sensor dinámico k10temp por nombre con NO_DATA bloqueante

$ git -C p0x reflog --date=iso
f4a7ad7  2026-08-09 00:14:07  commit
ae6b910  2026-08-09 00:12:11  pull origin master --no-edit: Fast-forward
fcbf8f8  2026-08-09 00:12:10  reset: moving to HEAD~1
95ea7b4  2026-08-09 00:10:28  commit (misma canonización, reescrita)
fcbf8f8  2026-08-08 23:51:29  reset: moving to HEAD~1
ae6b910  2026-08-08 23:51:27  commit: test: fuga simulada
```

Dos observaciones que el reflog deja a la vista:

1. `ae6b910 test: fuga simulada` **se confirmó, se deshizo con un reset, y
   volvió a entrar** en el `pull` de las 00:12. Sigue en la historia, y su
   fichero `mente/test_fuga.md` está publicado.
2. El `pull origin master` de las 00:12 fue contra el repositorio **público**:
   es el remoto que `p0x` tiene configurado. Esa es la noche en la que la cara
   pública dejó de ser una exportación sanitizada — ver
   `RECONCILIACION_HEXELION_2026-08-09.md`.

De la «recuperación del rack» propiamente dicha, el único rastro es del día
anterior, en el otro repositorio:

```
$ git -C hexelion log --since="2026-08-07 20:00" --until="2026-08-09 06:00"
5e957c2 2026-08-08 00:22:59  🏛️ OLEADA VISUAL v3.0 — Sello de Oro post-recuperación
```

## Datos que no se pudieron determinar

- **Los comandos y salidas originales de aquella noche.** No hay transcripción,
  ni en el historial de consola ni en las sesiones guardadas. Lo de arriba es
  re-medición de hoy, no copia de entonces.
- **Qué se recuperó exactamente en «la recuperación del rack»**, con qué
  comandos y contra qué nodo. El mensaje de `5e957c2` la da por hecha pero no la
  documenta.
- **El comando de commit que falló** y su mensaje de error.
- **Si aquella noche los cuatro hashes fueron estos cuatro caminos** o incluía
  alguna copia en otro nodo del rack. Se reconstruyen cuatro y coinciden; que
  sean *los mismos* cuatro no es verificable.
