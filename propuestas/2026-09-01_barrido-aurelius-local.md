# Encargo para `cc-local` · barrido de `aurelius`

**Estado:** ENCARGO PREPARADO. No ejecutado por la sesión de frontera, y a
propósito: es un renombrado mecánico y verificable por gate, o sea exactamente
lo que la Regla de oro manda delegar. Firmado por el Soberano el 2026-09-01
(*«el barrido local es preferible gastar tokens locales»*).

    ~/p0x/bin/cc-local

## La línea que separa lo que se toca de lo que no

Dictada por el Soberano, y no es negociable por el silicio:

| Ámbito | Qué se hace |
|---|---|
| **El Ojo** (`Alejandria/ojo/`) | **YA ESTÁ LIMPIO.** Cero referencias, medido. No tocar |
| **La web** (`~/preceptoros-web`) | **HECHO** en `a03aa55`. Sólo queda `dist/aurelius` |
| **La app** (`~/p0x/preceptor`) | **NO SE TOCA.** La app se basa en ese nombre |
| **Historial de git** | **NO SE TOCA** |
| **Textos anteriores al 2026-08-25** | **NO SE TOCA** |

Queda por barrer, con esa línea aplicada: `mente/` (12 ficheros) y
`preceptor-internal/` (69), descontando lo que caiga del lado de no tocar.

## Lo que NO se puede borrar aunque parezca texto viejo

Cinco casos medidos hoy. Borrarlos no es limpiar: es romper.

1. **`preceptor/casa.py` → `NOMBRES_ANTERIORES = (".aurelius",)`**
   Existe para ADOPTAR la casa vieja de quien instaló antes del renombrado.
   Quitarlo hace que esa persona pierda su memoria al actualizar. Es la línea
   con más consecuencias de todo el barrido.
2. **`preceptor/bin/aurelius-*`** — cuatro symlinks a los `preceptoros-*`,
   puestos a propósito en `a634c78` «protegiendo la compatibilidad».
3. **`~/.aurelius` → `~/.preceptoros`** — symlink vivo en el disco. `loops.db`
   se ve por las dos rutas porque es el mismo fichero.
4. **`Alejandria/migrar_casa.py`** — `aurelius` es su SUJETO: es el guion que
   migra desde ahí. Sin el nombre no puede hacer su trabajo.
5. **`~/.venvs/aurelius-forja`** — comprobado, **existe**. El texto que lo
   nombra en `sembrar_memoria.py` es un hecho, no una reliquia.

## El gate, que es lo que hace esto delegable

Nada de este barrido se da por hecho sin las tres tandas en verde:

    cd ~/p0x/preceptor          && python3 -m pytest -q      # 446 passed hoy
    cd ~/p0x/preceptor-internal && pytest agentes/ -q        # 88 passed hoy
    cd ~/p0x                    && python3 -m pytest Alejandria/test_alejandria.py -q

Un diff que no pasa el gate no es un entregable. Y `cc-local` **no toca canon,
no propone enmiendas de doctrina y no emite veredictos de arquitectura**: si
encuentra un caso que no encaja en la tabla de arriba, lo anota como hallazgo y
PARA.

## Telemetría obligatoria

Una línea en `mente/telemetria/cerebro_local.jsonl` al cerrar:
`{fecha, tarea, cerebro, pasadas, minutos, gate_ok, ctx_pico, nota}`.
