#!/usr/bin/env python3
"""genesis.py — el semáforo térmico honesto del Monje (misión LAS TRES JOYAS).

El Monje audita el pulso vital del nodo con sensores honestos: lo que el SO
no expone se rinde como ``null``, jamás se inventa. La salida es UN objeto
JSON plano por stdout (nada más toca stdout) con el veredicto
``viabilidad_roh`` — el guard de los 80°C formalizado como semáforo:
``optimo | templado | peligro_termico``. No es una métrica de rentabilidad ni
existe aquí concepto alguno de cripto o alquiler de cómputo.

Desviación mínima aditiva declarada: si el SO no expone sensores térmicos,
el semáforo rinde ``sin_dato_termico`` — un guard ciego no puede declararse
``optimo`` sin mentir (honest sensors > enum cerrado).

Compartido por P0X y Aurelius: un nodo que se conoce, construido una vez.
"""

from __future__ import annotations

import json
import uuid

import psutil
import requests

UMBRAL_PELIGRO_C: float = 80.0   # el guard: a 80°C se para, no se negocia
UMBRAL_TEMPLADO_C: float = 65.0  # por encima, vigilancia; por debajo, óptimo
UMBRAL_AHORRO_PCT: float = 20.0  # batería baja sin corriente = modo ahorro
TIMEOUT_SERVICIO_S: float = 2.0  # los servicios locales responden ya o no


def nodo_id() -> str:
    """Deriva el identificador del nodo de su dirección MAC.

    Returns:
        MAC en hex de 12 dígitos con prefijo ``nodo-``. ``uuid.getnode()``
        puede rendir un valor aleatorio si no hay MAC real accesible; sigue
        siendo estable dentro del proceso y se rinde tal cual.
    """
    return f"nodo-{uuid.getnode():012x}"


def auditar_energia() -> dict[str, bool | float | None]:
    """Audita la energía del nodo con ``psutil.sensors_battery``.

    Un equipo sin batería (corriente fija, p. ej. el Beelink de soberano)
    rinde ``sensors_battery() -> None`` o lanza — se captura y se declara
    corriente conectada con batería ``null``.

    Returns:
        ``corriente_conectada`` (bool), ``porcentaje_bateria`` (float o
        ``None`` honesto) y ``estado_ahorro`` (bool: batería baja Y sin
        corriente).
    """
    try:
        bateria = psutil.sensors_battery()
    except (AttributeError, NotImplementedError, OSError):
        bateria = None
    if bateria is None:
        return {"corriente_conectada": True, "porcentaje_bateria": None,
                "estado_ahorro": False}
    conectada = bool(bateria.power_plugged)
    porcentaje = float(bateria.percent) if bateria.percent is not None else None
    ahorro = (not conectada and porcentaje is not None
              and porcentaje <= UMBRAL_AHORRO_PCT)
    return {"corriente_conectada": conectada, "porcentaje_bateria": porcentaje,
            "estado_ahorro": ahorro}


def temperatura_cpu() -> float | None:
    """Media de los sensores de núcleo que el SO exponga.

    Prefiere los grupos habituales de CPU (``coretemp``/``k10temp``/
    ``zenpower``/``cpu_thermal``); si no existen, promedia todo lo que haya.

    Returns:
        Media en °C redondeada a 1 decimal, o ``None`` honesto si el SO no
        expone ningún sensor térmico — jamás un número inventado.
    """
    try:
        try:
            grupos = psutil.sensors_temperatures()
        except (TypeError, ValueError, Exception):
            return "sin_dato_termico"
    except (AttributeError, NotImplementedError, OSError):
        return None
    if not grupos:
        return None
    preferidos = ("coretemp", "k10temp", "zenpower", "cpu_thermal", "acpitz")
    lecturas: list[float] = []
    for nombre in preferidos:
        for sensor in grupos.get(nombre, []):
            if sensor.current is not None:
                lecturas.append(float(sensor.current))
        if lecturas:
            break
    if not lecturas:
        lecturas = [float(s.current) for sensores in grupos.values()
                    for s in sensores if s.current is not None]
    if not lecturas:
        return None
    return round(sum(lecturas) / len(lecturas), 1)


def auditar_hardware() -> dict[str, float | None]:
    """Audita CPU, térmica y RAM.

    Returns:
        ``cpu_uso_porcentaje`` (muestra de 1 s), ``cpu_temperatura_celsius``
        (o ``None`` honesto) y ``ram_disponible_gb`` (GiB, 2 decimales).
    """
    return {
        "cpu_uso_porcentaje": float(psutil.cpu_percent(interval=1.0)),
        "cpu_temperatura_celsius": temperatura_cpu(),
        "ram_disponible_gb": round(psutil.virtual_memory().available / 2**30, 2),
    }


def ollama_vivo() -> bool:
    """GET a la raíz de Ollama local; 200 = vivo, cualquier otra cosa no."""
    try:
        return requests.get("http://localhost:11434",
                            timeout=TIMEOUT_SERVICIO_S).status_code == 200
    except requests.RequestException:
        return False


def docker_activo() -> bool:
    """Ping vía SDK de Docker; toda excepción (SDK ausente incluido) = inactivo.

    Nota honesta: un ``False`` aquí no distingue «daemon parado» de «SDK sin
    instalar» — ambos significan que el Monje no puede usar Docker ahora.
    """
    try:
        import docker  # import local: el SDK es opcional en este nodo
        return bool(docker.from_env(timeout=TIMEOUT_SERVICIO_S).ping())
    except Exception:  # noqa: BLE001 — el SDK lanza jerarquías propias variadas
        return False


def semaforo(temperatura_c: float | None) -> str:
    """El guard de 80°C como semáforo honesto.

    Args:
        temperatura_c: media de núcleos, o ``None`` si el SO no la expone.

    Returns:
        ``peligro_termico`` (≥80°C), ``templado`` (≥65°C), ``optimo``
        (<65°C) o ``sin_dato_termico`` (guard ciego declarado — desviación
        aditiva sobre el enum, ver docstring del módulo).
    """
    if temperatura_c is None:
        return "sin_dato_termico"
    if not isinstance(temperatura_c, (int, float)):
        return "sin_datos"
    if temperatura_c >= UMBRAL_PELIGRO_C:
        return "peligro_termico"
    if temperatura_c >= UMBRAL_TEMPLADO_C:
        return "templado"
    return "optimo"


def genesis() -> dict[str, object]:
    """Compone la auditoría completa del nodo. Puro dato, cero side effects."""
    hardware = auditar_hardware()
    return {
        "nodo_id": nodo_id(),
        "energia": auditar_energia(),
        "hardware": hardware,
        "servicios_locales": {
            "docker_activo": docker_activo(),
            "ollama_activo": ollama_vivo(),
        },
        "viabilidad_roh": semaforo(hardware["cpu_temperatura_celsius"]),
    }


if __name__ == "__main__":
    print(json.dumps(genesis(), ensure_ascii=False))
