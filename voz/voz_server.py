#!/usr/bin/env python3
"""voz_server.py — Piper RESIDENTE en la fragua (P0X #21, VENTANA VIVA B4).

Mantiene el modelo ONNX cargado en RAM (~250MB) para que la primera sílaba
del Sínodo llegue en ~1.5s en vez de ~3.7s (frío). 100% LOCAL: escucha SOLO
en 127.0.0.1:8021; el texto jamás sale del rack. El gateway (voz_api.py) lo
usa si vive y cae a subprocess frío si no — este servicio es una mejora de
latencia, no una dependencia.

ARTEFACTO PROPOSE-ONLY: la unit deploy/fragua/p0x-voz.service queda PROPUESTA;
instalarla/habilitarla es paste del Soberano (patrón #4).

Arranque manual (sin systemd, para probar):
  /mnt/nvme/p0x/voz/.venv-piper/bin/python /mnt/nvme/p0x/voz/voz_server.py
"""
import io
import wave
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import Response
from piper import PiperVoice
from pydantic import BaseModel

VOZ_DIR = Path(__file__).resolve().parent
VOCES = {
    "davefx": VOZ_DIR / "modelos" / "es_ES-davefx-medium.onnx",
    "sharvard": VOZ_DIR / "modelos" / "es_ES-sharvard-medium.onnx",
}
DEFAULT_VOZ = "davefx"
MAX_CHARS = 4000

app = FastAPI(title="p0x-voz residente")
_cargadas: dict[str, PiperVoice] = {}


def _voz(nombre: str) -> PiperVoice:
    if nombre not in _cargadas:
        _cargadas[nombre] = PiperVoice.load(VOCES[nombre])
    return _cargadas[nombre]


class SintetizarReq(BaseModel):
    texto: str
    voz: str = DEFAULT_VOZ


@app.get("/salud")
def salud():
    return {"ok": True, "residentes": sorted(_cargadas)}


@app.post("/sintetizar")
def sintetizar(req: SintetizarReq):
    texto = req.texto.strip()
    if not texto or len(texto) > MAX_CHARS:
        raise HTTPException(422, f"texto vacío o > {MAX_CHARS} chars")
    if req.voz not in VOCES:
        raise HTTPException(422, f"voz desconocida (disponibles: {sorted(VOCES)})")
    buf = io.BytesIO()
    with wave.open(buf, "wb") as w:
        _voz(req.voz).synthesize_wav(texto, w)
    return Response(content=buf.getvalue(), media_type="audio/wav")


if __name__ == "__main__":
    import uvicorn
    _voz(DEFAULT_VOZ)  # pre-carga: el primer request ya es caliente
    uvicorn.run(app, host="127.0.0.1", port=8021, log_level="warning")
