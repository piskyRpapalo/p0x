"""El segundo cerebro: la FORMA de una memoria, jamas su contenido.

Esto lee la base de recuerdos de una persona, asi que la primera decision es que
NO se lee: ni un texto, ni un titulo, ni un fragmento. Solo se cuentan cosas y
se mide como estan conectadas. La misma regla que el manifiesto del nucleo lleva
escrita -- «el manifiesto no contiene texto de la memoria»-- y por el mismo
motivo: un panel puede acabar en una pantalla que mira alguien mas.

Se abre en modo `ro` de sqlite. No es cortesia: un panel que abre en escritura
crea un `-wal` junto a la base de otro proceso y puede bloquearla.

Y una tabla que no existe no es un error: es una version distinta del esquema.
Se cuenta lo que hay y se declara lo que falta.
"""

import os
import sqlite3
from pathlib import Path

import sensores
from sensores import registro

VARIABLE = "NEXO_MEMORIA"

# Donde suele vivir, de mas nueva a mas vieja. El nucleo renombro su carpeta y
# la anterior sigue en el disco de mucha gente con todo dentro: buscar solo la
# nueva haria que una memoria llena pareciera un jardin vacio.
CANDIDATAS = (".preceptoros/memory.db", ".aurelius/memory.db")

# Lo que se cuenta. Ninguna de estas consultas devuelve texto.
CUENTAS = (("engramas", "engrams"), ("enlaces", "links"),
           ("perfil", "profile"), ("hilos", "hilos"),
           ("proyectos", "proyectos"))

# Cuantos puntos tiene la silueta. Cinco: suficientes para leer una proporcion
# de un vistazo, pocos para que ninguno mienta por redondeo.
PUNTOS = 5


def ruta():
    declarada = (os.environ.get(VARIABLE) or "").strip()
    if declarada:
        return Path(declarada).expanduser()
    try:
        hogar = Path.home()
    except RuntimeError:
        return None
    for c in CANDIDATAS:
        if (hogar / c).is_file():
            return hogar / c
    return None


def silueta(cuantos, techo):
    """La proporcion en puntos llenos y huecos. El hueco tambien es el dato.

    Con cero de algo salen cinco huecos, no una fila en blanco: un jardin vacio
    tiene forma, y ensenarla es la diferencia entre «no hay nada» y «no se ha
    mirado».
    """
    if techo <= 0:
        return "○" * PUNTOS
    llenos = min(PUNTOS, round(PUNTOS * min(cuantos, techo) / techo))
    if cuantos > 0 and llenos == 0:
        llenos = 1                      # lo que existe nunca sale como vacio
    return "●" * llenos + "○" * (PUNTOS - llenos)


def leer():
    db = ruta()
    if db is None or not db.is_file():
        return sensores.hueco(
            "no hay ninguna memoria en este disco · declara su ruta en "
            f"${VARIABLE} si vive en otro sitio",
            "memory.db")
    try:
        con = sqlite3.connect(f"file:{db}?mode=ro", uri=True, timeout=2)
    except sqlite3.Error as e:
        return sensores.hueco(
            "la memoria esta en el disco pero no se deja abrir para lectura",
            type(e).__name__)

    cuentas, faltan = {}, []
    try:
        with con:
            for etiqueta, tabla in CUENTAS:
                try:
                    cuentas[etiqueta] = con.execute(
                        f"select count(*) from {tabla}").fetchone()[0]
                except sqlite3.Error:
                    # Tabla ausente = otra version del esquema, no una averia.
                    faltan.append(etiqueta)
    finally:
        con.close()

    if not cuentas:
        return sensores.hueco(
            "el fichero existe pero no tiene ninguna tabla conocida · "
            "puede ser de otra version", db.name)

    engramas = cuentas.get("engramas", 0)
    enlaces = cuentas.get("enlaces", 0)
    # El techo sale del propio dato y no de una constante: una memoria de tres
    # recuerdos y una de tres mil se leen igual de bien, y ninguna necesita que
    # alguien acierte de antemano cual es «mucho».
    techo = max(engramas, 1)
    filas = [{"que": etiqueta, "cuantos": n,
              "silueta": silueta(n, techo if etiqueta != "perfil" else max(n, 1))}
             for etiqueta, n in cuentas.items()]

    # La densidad de enlaces es la pregunta que importa de un jardin: no cuanto
    # hay, sino cuanto esta conectado con lo demas.
    densidad = (enlaces / engramas) if engramas else None
    return sensores.dato(
        filas=filas,
        engramas=engramas,
        enlaces=enlaces,
        densidad=round(densidad, 2) if densidad is not None else sensores.NO_DATA,
        silueta_enlaces=silueta(enlaces, techo),
        faltan=faltan,
        vacio=engramas == 0,
        causa=("el jardin esta plantado y sin enlazar · cada recuerdo vive solo"
               if engramas and not enlaces else
               "" if engramas else "jardin vacio · todavia no hay nada sembrado"),
    )


registro.registrar("cerebro", leer)
