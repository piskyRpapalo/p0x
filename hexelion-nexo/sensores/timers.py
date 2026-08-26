"""Los bucles del orquestador: cuando toca, cuando fue la ultima y si salio bien.

Se lee con `systemctl show`, que devuelve `clave=valor`, y no con
`list-timers`, cuya tabla alinea seis columnas de las que dos son fechas con
espacios dentro. Parsear esa tabla es adivinar donde acaba una fecha y empieza
la siguiente; `show` no deja sitio para adivinar.

Un timer que nunca ha corrido tiene `LastTriggerUSec=` vacio, y eso sale como
NO_DATA con su causa -- no como una fecha inventada ni como un cero.
"""

import shutil
import subprocess

import sensores
from sensores import registro

# Los que son del orquestador. Los del sistema operativo se leen igual pero se
# marcan aparte: mezclarlos haria que «tres bucles» y «seis timers» parecieran
# la misma cifra.
AJENOS = ("ubuntu-", "launchpadlib", "systemd-", "fwupd", "snap.")

CAMPOS = ("Description", "ActiveState", "Unit",
          "NextElapseUSecRealtime", "LastTriggerUSec")


def _systemctl(*args):
    ruta = shutil.which("systemctl")
    if ruta is None:
        raise FileNotFoundError("systemctl no esta en el PATH")
    salida = subprocess.run([ruta, "--user", *args], capture_output=True,
                            text=True, timeout=10)
    return salida.stdout


def _mostrar(unidad, campos):
    crudo = _systemctl("show", unidad, *[f"-p{c}" for c in campos])
    datos = {}
    for linea in crudo.splitlines():
        if "=" in linea:
            k, _, v = linea.partition("=")
            datos[k] = v.strip()
    return datos


def _unidades():
    crudo = _systemctl("list-units", "--type=timer", "--all",
                       "--no-legend", "--plain")
    nombres = []
    for linea in crudo.splitlines():
        partes = linea.split()
        if partes and partes[0].endswith(".timer"):
            nombres.append(partes[0])
    return nombres


def leer():
    try:
        nombres = _unidades()
    except Exception as e:                                       # noqa: BLE001
        return sensores.hueco(f"no se pudo consultar systemd · {type(e).__name__}")
    if not nombres:
        return sensores.hueco("systemd no declara ningun timer de usuario")

    propios, ajenos = [], []
    for nombre in nombres:
        d = _mostrar(nombre, CAMPOS)
        servicio = d.get("Unit") or ""
        s = _mostrar(servicio, ("ActiveState", "Result")) if servicio else {}
        ultima = d.get("LastTriggerUSec") or ""
        fila = {
            "unidad": nombre,
            "descripcion": d.get("Description") or sensores.NO_DATA,
            "activo": d.get("ActiveState") == "active",
            "servicio": servicio or sensores.NO_DATA,
            "proxima": d.get("NextElapseUSecRealtime") or sensores.NO_DATA,
            "ultima": ultima or sensores.NO_DATA,
            # La pregunta que `list-timers` no contesta: corrio, vale, ¿y salio
            # bien? Un bucle que se dispara puntual y falla cada vez se ve
            # exactamente igual que uno sano si solo se miran las horas.
            # Y si nunca ha corrido, el resultado tambien es un hueco. systemd
            # contesta `Result=success` para un servicio que jamas se arranco --
            # es su valor por defecto, no una medida-- y pintarlo como verde
            # seria el cero decorativo de manual: un bucle sin estrenar
            # parecerian identico a uno que acaba de salir bien.
            "resultado": (s.get("Result") or sensores.NO_DATA) if ultima
                         else sensores.NO_DATA,
            "causa": "" if ultima else "armado · no se ha disparado nunca",
        }
        (ajenos if nombre.startswith(AJENOS) else propios).append(fila)

    return sensores.dato(propios=propios, ajenos=ajenos,
                         cuantos=len(propios), cuantos_ajenos=len(ajenos))


registro.registrar("timers", leer)
