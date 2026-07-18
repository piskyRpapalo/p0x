# Bench fundacional CPU vs Vulkan · soberano (Misión G0, 2026-07-18)

## Método

`llama-bench` de `llama.cpp` release **b10068** (binarios prebuilt oficiales, sin compilar —
evita `cmake`/`build-essential`, que no están instalados y no hay sudo interactivo en este nodo):

- `llama-b10068-bin-ubuntu-x64.tar.gz` (CPU, backend `zen4` optimizado para este Ryzen)
- `llama-b10068-bin-ubuntu-vulkan-x64.tar.gz` (Vulkan, detecta `AMD Radeon 780M Graphics (RADV PHOENIX)`)

Modelo: `Qwen3-Coder-30B-A3B-Instruct-Q4_K_M.gguf` (18.5GB, mismo modelo/quant que sirve Ollama
como `qwen3-coder:30b`) — descargado standalone de `unsloth/Qwen3-Coder-30B-A3B-Instruct-GGUF`
porque el home del servicio Ollama (`/usr/share/ollama/.ollama`, `700`) no es legible sin sudo
aunque `pisky` esté en el grupo `ollama` (desviación declarada — bloqueó el plan original de
apuntar `llama-bench` directo al blob).

`pp512` (prompt processing, 512 tokens) y `tg128` (generación, 128 tokens), **3 corridas cada
configuración**, `-ngl 0` (CPU, 16 hilos) vs `-ngl 99` (Vulkan, todas las capas al iGPU). Datos
crudos completos (las 12 corridas, con `stddev` y muestras individuales) en
`mente/telemetria/soberano_bench_g0.json`.

## Resultado (medias de 3 corridas)

| Test | CPU (16 hilos) | Vulkan (Radeon 780M) | Speedup |
|---|---|---|---|
| `pp512` (tok/s) | 99.93 ± 11.24 | 357.70 ± 2.52 | **3.58×** |
| `tg128` (tok/s) | 9.90 ± 0.30 | 32.49 ± 0.03 | **3.28×** |

Vulkan gana con claridad en ambos, y con mucha menor varianza entre corridas (`stddev` de
`tg128` en Vulkan es prácticamente cero: 0.03 vs 0.30 en CPU). **Decisión por dato: el backend de
`soberano-coder` debe ser Vulkan, no CPU.**

## Acción pendiente para aplicar la decisión (necesita sudo — no ejecutada en esta misión)

Ollama ya trae el flag `OLLAMA_VULKAN:true` por defecto y detecta el dispositivo
(`name=Vulkan0 description="AMD Radeon 780M Graphics (RADV PHOENIX)"`, confirmado en
`journalctl -u ollama`), pero **descarta la iGPU explícitamente**:

```
level=INFO source=runner.go:405 msg="dropping integrated GPU; to enable, set OLLAMA_IGPU_ENABLE=1"
```

Por eso el smoke test del Bloque C corrió 100% CPU (24.9 tok/s en `soberano-coder`, consistente
con el número de este bench). Para activarlo (requiere el sudo que este nodo no tiene en esta
sesión):

```
sudo systemctl edit ollama
# añadir bajo [Service]:
#   Environment="OLLAMA_IGPU_ENABLE=1"
sudo systemctl daemon-reload
sudo systemctl restart ollama
ollama ps   # debería dejar de decir "100% CPU"
```

Tras aplicarlo, repetir el smoke test del Bloque C y comparar tok/s — la ganancia esperada por
este bench es ~3.3× en generación.
