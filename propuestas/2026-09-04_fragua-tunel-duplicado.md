# Propuesta · la-fragua: retirar la unidad de sistema `agora-tunnel` (5418 reinicios)

**Estado:** PROPUESTA. No aplicada. `la-fragua` es propose-only desde `soberano`,
y esto toca una unidad systemd — que además exige firma explícita por el canon
del 2026-08-24. Medido por SSH de solo lectura el 2026-09-04.

## Lo que hay, medido

Hay **dos** unidades con el mismo nombre y el mismo propósito. Una funciona y la
otra lleva un día y medio dándose contra la pared:

| unidad | ruta | estado |
|---|---|---|
| **usuario** | `~/.config/systemd/user/agora-tunnel.service` | `active running` desde 2026-09-01 21:10 UTC · **NRestarts 0** |
| **sistema** | `/etc/systemd/system/agora-tunnel.service` | `activating auto-restart` · **NRestarts 5418** · `Result=exit-code` |

La que sirve es la de **usuario**. Comprobado desde fuera del rack, por internet:

    curl -s -o /dev/null -w '%{http_code}' https://api.preceptoros.org/api/v1/threads
    200

Y el proceso vivo es suyo: `pgrep -af cloudflared` da un solo
`~/bin/cloudflared ... tunnel run agora`, con `linger=yes`, que es
justo lo que le faltaba cuando se caía al reiniciar.

## Por qué falla la de sistema

    agora-tunnel.service: Main process exited, code=exited, status=203/EXEC

`203/EXEC` es systemd diciendo «no he podido ejecutar el binario». La unidad de
sistema corre fuera de la sesión de `ubuntu` y apunta a un binario que vive en
`~/bin/cloudflared`. No es que el túnel esté mal configurado: es que
esa unidad **nunca ha llegado a arrancar una sola vez**. Reinicia cada ~20 s
desde hace más de un día.

## Por qué importa aunque el túnel funcione

Porque el síntoma es invisible por el sitio donde se mira. `api.preceptoros.org`
responde 200, así que cualquier comprobación desde el producto dice VERDE
mientras el journal del nodo se llena a razón de cuatro líneas cada veinte
segundos. Es la misma avería que se acaba de matar en `soberano` esta misma
sesión — `aurelius.service`, 7970 reinicios contra un proceso que no era suyo —
y la lección es la misma: **un servicio que reinicia sin parar no alerta a
nadie**, porque el que mira mira el puerto, no la unidad.

Dos nodos del rack con el mismo defecto de clase en la misma sesión sugiere que
merece una comprobación de rutina, no un arreglo puntual. Ver la sugerencia de
`PENDIENTES.md` sobre pasar `NRestarts` al recolector del Ojo.

## Qué se propone

Retirar la unidad de sistema. No se toca la de usuario, que es la que sirve.

    # EN la-fragua, con la firma del Soberano:
    sudo systemctl stop agora-tunnel.service
    sudo systemctl disable agora-tunnel.service
    sudo mv /etc/systemd/system/agora-tunnel.service \
            /etc/systemd/system/agora-tunnel.service.retirada
    sudo systemctl daemon-reload

## Cómo se comprueba que salió bien

    systemctl show agora-tunnel -p ActiveState --value          # -> inactive
    systemctl --user show agora-tunnel -p ActiveState --value   # -> active   (no cambia)
    curl -s -o /dev/null -w '%{http_code}\n' https://api.preceptoros.org/api/v1/threads
    # -> 200, igual que antes: el túnel no se toca

## Cómo se revierte

    sudo mv /etc/systemd/system/agora-tunnel.service.retirada \
            /etc/systemd/system/agora-tunnel.service
    sudo systemctl daemon-reload

## Corrección al glosario del Ojo, de paso

La entrada del inventario dice que el Ágora «no publica ninguna ruta: `/`,
`/docs` y `/openapi.json` devuelven 404». Los tres siguen dando 404, pero la
conclusión no se sigue. Medido hoy sobre `127.0.0.1:9002`:

| ruta | código | lectura |
|---|---|---|
| `/` `/docs` `/openapi.json` `/health` | 404 | normal en FastAPI sin raíz ni docs |
| `/api/v1/threads` | **200** | la API sirve |
| `/api/v1/profiles` | **405** | la ruta existe; pide otro verbo |

«El túnel llega y la aplicación no tiene puertas» ya no describe el nodo: las
tiene, y están abiertas. Y `agora-api` ya no corre fuera de systemd — la unidad
de usuario está `active running` desde el 2026-09-03 01:18 UTC. Probar la raíz
de una API y concluir que no hay API es medir la propiedad equivocada.
