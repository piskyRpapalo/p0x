#!/usr/bin/env python3
"""ingest_youtube.py — Ruta de AUDIO del pipeline P0X (Fase 1).
yt-dlp (audio) -> ffmpeg (16kHz mono wav) -> Silero VAD (recorta no-voz) -> whisper.cpp -> transcript JSON.
Ejecutar SIEMPRE encolado para no saturar la-fragua:
    p0x-enqueue python3 ingest_youtube.py <URL>
Salida: /mnt/nvme/p0x/pipeline/out/<id>/{transcript.json, meta.json}
El 'delta' contra el Codice es el paso SIGUIENTE; aqui se produce el transcript crudo.
SUELO: nada de esto firma valor ni sale del rack."""
import argparse, json, os, shutil, subprocess, wave
from pathlib import Path
P0X = Path(os.environ.get("P0X_ROOT", "/mnt/nvme/p0x"))
PIPE = P0X / "pipeline"
# El PATH de los servicios systemd (gateway->tsp) no incluye ~/.local/bin:
# resolver por PATH y caer a la ruta de instalación real, como WHISPER_BIN.
YTDLP_BIN = shutil.which("yt-dlp") or str(Path.home() / ".local" / "bin" / "yt-dlp")
WHISPER_BIN = PIPE / "whisper.cpp" / "build" / "bin" / "whisper-cli"
WHISPER_MODEL = Path(os.environ.get(
    "P0X_WHISPER_MODEL", PIPE / "whisper.cpp" / "models" / "ggml-small.bin"))
VAD_ONNX = PIPE / "models" / "silero_vad.onnx"
OUT = PIPE / "out"

def run(cmd, **kw):
    print("  $", " ".join(map(str, cmd)))
    return subprocess.run(list(map(str, cmd)), check=True, **kw)

def video_id(url):
    try:
        r = subprocess.run([YTDLP_BIN, "--no-playlist", "--skip-download", "--print", "id", url],
                           check=True, capture_output=True, text=True)
        return (r.stdout.strip().splitlines() or ["video"])[0]
    except Exception:
        return "video"

def download_audio(url, workdir):
    run([YTDLP_BIN, "--no-playlist", "-x", "--audio-format", "wav",
         "-o", str(workdir / "audio.%(ext)s"), url])
    wavs = list(workdir.glob("audio.*"))
    if not wavs:
        raise RuntimeError("yt-dlp no produjo audio")
    norm = workdir / "audio16k.wav"
    run(["ffmpeg", "-y", "-i", wavs[0], "-ar", "16000", "-ac", "1",
         "-c:a", "pcm_s16le", norm])
    return norm

def _read_wav_16k_mono(path):
    import numpy as np
    with wave.open(str(path), "rb") as w:
        assert w.getframerate() == 16000 and w.getnchannels() == 1, "se esperaba 16kHz mono"
        raw = w.readframes(w.getnframes())
    return np.frombuffer(raw, dtype=np.int16).astype("float32") / 32768.0

def vad_trim(wav_path, workdir):
    """Recorta no-voz con Silero v5 ONNX (onnxruntime, sin torch).
    Degradacion LIMPIA: ante cualquier fallo devuelve el wav original."""
    try:
        import numpy as np, onnxruntime as ort
        if not VAD_ONNX.exists():
            print("  [vad] modelo silero ausente -> sin recorte"); return wav_path
        audio = _read_wav_16k_mono(wav_path)
        sess = ort.InferenceSession(str(VAD_ONNX), providers=["CPUExecutionProvider"])
        names = {i.name for i in sess.get_inputs()}
        state = np.zeros((2, 1, 128), dtype="float32")
        sr = np.array(16000, dtype="int64")
        win, thr = 512, 0.5
        keep = np.zeros(len(audio), dtype=bool)
        for i in range(0, len(audio) - win, win):
            chunk = audio[i:i + win].reshape(1, -1)
            feed = {"input": chunk, "sr": sr}
            feed["state" if "state" in names else "h"] = state
            out = sess.run(None, feed)
            if float(out[0].reshape(-1)[0]) >= thr:
                keep[i:i + win] = True
            if len(out) > 1 and getattr(out[1], "shape", None) == state.shape:
                state = out[1]
        if not keep.any():
            print("  [vad] sin voz detectada -> sin recorte"); return wav_path
        trimmed = audio[keep]
        out_path = workdir / "speech16k.wav"
        with wave.open(str(out_path), "wb") as w:
            w.setnchannels(1); w.setsampwidth(2); w.setframerate(16000)
            w.writeframes((trimmed * 32768.0).astype("int16").tobytes())
        print(f"  [vad] voz {100.0 * len(trimmed) / max(1, len(audio)):.0f}% -> recortado")
        return out_path
    except Exception as e:
        print(f"  [vad] WARN ({e}) -> transcribo audio completo")
        return wav_path

def transcribe(wav_path, out_dir, lang):
    if not WHISPER_BIN.exists():
        raise RuntimeError(f"whisper-cli ausente en {WHISPER_BIN} (corre build_audio_pipeline.sh)")
    run([WHISPER_BIN, "-m", WHISPER_MODEL, "-f", wav_path, "-l", lang,
         "-oj", "-of", out_dir / "transcript", "-t", str(os.cpu_count() or 4)])
    return out_dir / "transcript.json"

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("url")
    ap.add_argument("--lang", default="es")
    ap.add_argument("--no-vad", action="store_true")
    a = ap.parse_args()
    vid = video_id(a.url)
    out_dir = OUT / vid; out_dir.mkdir(parents=True, exist_ok=True)
    work = out_dir / "work"; work.mkdir(exist_ok=True)
    print(f"== ingest {vid} ==")
    wav = download_audio(a.url, work)
    wav = wav if a.no_vad else vad_trim(wav, work)
    tj = transcribe(wav, out_dir, a.lang)
    (out_dir / "meta.json").write_text(json.dumps(
        {"url": a.url, "video_id": vid, "lang": a.lang,
         "vad": not a.no_vad, "whisper_model": WHISPER_MODEL.name}, indent=2), encoding="utf-8")
    print(f"OK -> {tj}")
    print("Paso SIGUIENTE (no aqui): cruzar el transcript con el Codice -> DELTA.")

if __name__ == "__main__":
    main()
