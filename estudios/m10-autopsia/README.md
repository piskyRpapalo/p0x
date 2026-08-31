# Autopsia del M10-EM-2 · bucle de estudio

**Estado: el paso determinista esta HECHO y en verde; el bucle del modelo espera al Orin.**

## Que hay aqui

| Fichero | Que es | Estado |
|---|---|---|
| `autopsia.py` | el guion **determinista**: inventario fisico + consulta a OpenBeken → JSON | **corrido, gate VERDE** |
| `m10-inventario.json` | su salida, 3318 B, `estado: MEDIDO` | **producido** |
| `correr-en-orin.sh` | los pasos que exigen el Orin: modelo, consumo, ficha, firma | **sin correr** |

## Por que no viaja por `git clone` a `~/hexelion-nexo`

`la-torre` ya aloja `jetson:p0x.git`. Este estudio vive dentro de `p0x`, asi que
al Orin llega con `git pull`, sin un repositorio nuevo que mantener. Si aun asi
se quiere en `~/hexelion-nexo/estudios/`, un symlink basta.

## El hallazgo que ya dio el paso determinista

**El gemelo F1s202-EU no prueba el chip.** Aparece DOS veces en la base de
OpenBeken con chips distintos: `ANTELA / BK7231N` y `Antela / BK7231T`. La ficha
de la necropolis lo daba como confirmacion del BK7231N. El mismo numero de
modelo se fabrica con silicio distinto — que es exactamente por lo que un perfil
de cloudcutter no es transferible entre gemelos.

Medido sobre 889 dispositivos (esquema 0.1): 427 con BK7231N, 113 con BL0937,
52 con ambos. **El perfil del M10 es comun y aun asi el M10 no esta.**

## Lo que se midio en el Orin, y el techo que salio

El bucle corrio entero. Resultados, todos medidos:

| Modelo | Resultado |
|---|---|
| `qwen3:8b-instruct` | **no existe** · 404 en el registro; el tag real es `qwen3:8b` |
| `qwen3:8b` (5,2 GB) | **no carga** · `unable to allocate CUDA0 buffer`, repetido con 4,1 GB libres |
| `qwen3:4b-instruct-2507-q4_K_M` (2,5 GB) | **no carga** · mismo error con 4,2 GB libres |
| `qwen2.5:1.5b` (1,9 GB) | **carga** · 100 % GPU, contexto 4096 |

**El techo real de este nodo esta entre 1,9 y 2,5 GB de modelo**, muy por debajo
de lo que sugieren sus 8 GB. El demonio de inferencia lleva mas de cuatro dias
en pie y ha encajado varios OOM; reiniciarlo exige privilegios y es firma del
carbono, no tarea del silicio.

Consumo por INA3221 (riel VDD_IN) muestreado a 5 Hz **durante** la inferencia,
no antes ni despues: **16,28 W de media**, 16,84 de pico, 5,11 en reposo, 121
muestras. 607 tokens a 25,93 tok/s → **1,53 tokens/W**, 0,11 Wh el estudio.

## El auditor bloqueo la ficha, y hacia falta

El 1.5b leyo un JSON que dice que el gemelo NO es concluyente y escribio que si
lo era; afirmo que el aparato fue liberado (falso) y propuso flashear, que es la
prohibicion numero dos del mismo JSON. `auditor.py` lo caza con cuatro reglas,
sin modelo: para una contradiccion literal contra el documento de entrada no
hace falta un segundo modelo, y un `in` no alucina.

**La firma quedo en NO_DATA** por dos causas, y cualquiera basta: el gate esta
rojo, y no hay clave Ed25519 de atestacion designada para este nodo.

## Prohibiciones vigentes (2026-08-31)

No tocar el M10 fisicamente · no flashear nada mas · no buscar mas vias de
extraccion. El UART quedo **cerrado por decision del carbono**: la barrera es
administrativa (Tuya bloquea la API del wizard tras vinculacion fallida) y no
cede por hardware.
