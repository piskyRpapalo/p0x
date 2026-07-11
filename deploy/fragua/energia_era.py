"""energia_era.py — P0X Pista A · el envoltorio @sleeping rescatado (arqueología #43).

Rescate del patrón HEXELION_BATTERY_FLAG_SPEC (15-may-2026): UNA variable
conmuta la Era energética del sistema; el código de la otra Era queda presente,
versionado y OBSERVABLE, pero dormido. Compatible con honest-sensors: lo
dormido no finge datos, se loguea cada invocación.

LO QUE NO SE RESCATA (enterrado, IronClaw): las tácticas de arbitraje de
mercado que el spec original envolvía (MCT-MAX, carga de red negativa para
generar ingresos, modos de valor). Los reflejos son SOLO protectores.

Uso (patrón formal de la Pista A):
    from energia_era import ENERGY_ERA, sleeping, sun_synchronous

    @sleeping(reason="umbral SOC: no aplicable sin batería solar")
    def rearme_por_soc(): ...

    @sun_synchronous(reason="sin batería, la UPS es la única reserva")
    def rearme_por_ups_ol(): ...

Flag: P0X_BATTERY_PRESENT (env, default false → Era SOL_SINCRONO).
Doctrina: mente/reflejos/patron-era-energetica.md
"""
import functools
import logging
import os

logger = logging.getLogger("p0x.energia_era")

BATTERY_PRESENT: bool = os.environ.get(
    "P0X_BATTERY_PRESENT", "false"
).lower() in ("true", "1", "yes")

ENERGY_ERA: str = "PLENA" if BATTERY_PRESENT else "SOL_SINCRONO"


def sleeping(reason: str = "requiere P0X_BATTERY_PRESENT=true"):
    """La función existe y se versiona, pero NO corre en Era SOL_SINCRONO.
    Cada invocación dormida se loguea (observable, jamás silenciosa)."""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            if not BATTERY_PRESENT:
                logger.info("@sleeping: %s no ejecutada (era=%s). Motivo: %s",
                            func.__name__, ENERGY_ERA, reason)
                return None
            return func(*args, **kwargs)
        wrapper.__sleeping__ = True
        wrapper.__sleeping_reason__ = reason
        return wrapper
    return decorator


def sun_synchronous(reason: str = "solo tiene sentido sin batería"):
    """Simétrico: la función SOLO corre en Era SOL_SINCRONO."""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            if BATTERY_PRESENT:
                logger.info("@sun_synchronous: %s no ejecutada (era=%s). Motivo: %s",
                            func.__name__, ENERGY_ERA, reason)
                return None
            return func(*args, **kwargs)
        wrapper.__sun_synchronous__ = True
        return wrapper
    return decorator
