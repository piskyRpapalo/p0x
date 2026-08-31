# Ollama en soberano · el almacen que el servicio no ve

**Estado: PROPUESTA. Nada aplicado. Exige firma.**

## Medido el 2026-08-31

| Almacen | Tamano | Manifiestos | Quien lo lee |
|---|---|---|---|
| `/usr/share/ollama/.ollama` | **60K** | ninguno legible sin sudo | el servicio (`HOME=/usr/share/ollama`) |
| `/home/pisky/.ollama` | **33G** | 2 (`oficial-inventario`, `qwen3-coder-30b`) | nadie |  <!-- guardia:permitir ruta literal del almacen medido -->

`ollama --version` = 0.33.2 · `systemctl is-active ollama` = active ·
`ollama list` = vacio.

## El paso que falta y que un override NO arregla solo

    stat -c '%A %U:%G' /home/pisky   ->   drwxr-x--- pisky:pisky  <!-- guardia:permitir ruta literal del almacen medido -->

El usuario `ollama` **no puede atravesar `/home/pisky`**. Con solo el drop-in,  <!-- guardia:permitir ruta literal del almacen medido -->
el demonio arrancaria y seguiria sin ver nada: el fallo seria por permisos, no
por ruta, y desde fuera se parece exactamente al problema actual.

El grupo `pisky` SI tiene `r-x` sobre ese directorio, asi que basta con meter
al servicio en ese grupo. No hace falta abrir `/home/pisky` al resto del  <!-- guardia:permitir ruta literal del almacen medido -->
mundo con `chmod o+x`, que seria la solucion rapida y la que mas cede.

## Los tres comandos, en este orden

    sudo usermod -aG pisky ollama
    sudo systemctl edit ollama      # pegar deploy/soberano/ollama/override.conf
    sudo systemctl restart ollama

## Como se comprueba que funciono

    ollama list        # debe listar oficial-inventario y qwen3-coder-30b

Si sigue vacio, el fallo NO es este drop-in: mirar entonces si los otros 7
modelos que se servian esta manana estan en el almacen del servicio, que
requiere sudo para leerse:

    sudo ls /usr/share/ollama/.ollama/models/manifests/registry.ollama.ai/library/

## Como se deshace

Borrar el drop-in (`sudo systemctl revert ollama`) y `sudo gpasswd -d ollama
pisky`. El demonio vuelve a su almacen de siempre. No se mueve ni un byte de
modelo en ningun momento: esto solo cambia donde MIRA.

## Lo que esta propuesta NO hace

No mueve modelos, no borra `/usr/share/ollama/.ollama`, y no toca los 33 GB.
El rastreo sugeria `rm -rf` sobre ese directorio: no se hace, porque no se ha
podido leer su contenido sin sudo y borrar lo que no se ha mirado es
exactamente lo que salio mal hoy en otra maquina.
