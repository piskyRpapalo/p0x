# M1 · las tres capas en el Beelink

Todo vive aqui. La fragua queda fuera (firma del Soberano): no se instalo nada
en ella y solo presta, si se pide, los seis WAV del gate de voz.

## Lo instalado, con su hash verificado ANTES de usar

| Pieza | Origen | SHA256 publicado = calculado |
|---|---|---|
| `Qwen3-4B-Instruct-2507-Q4_K_M.gguf` (2,32 GiB) | unsloth, apache-2.0 | `3605803b982cb64aead44f6c1b2ae36e3acdb41d8e46c8a94c6533bc4c67e597` |
| `piper_tts-1.6.1` rueda manylinux x86_64 | PyPI, GPL-3.0-or-later | `c586e71e7923360bc530e411a6d10636bc0c31de37caeddb27731671889ece79` |
| `es_ES-sharvard-medium.onnx` (76,7 MB) | rhasspy/piper-voices | `40febfb1679c69a4505ff311dc136e121e3419a13a290ef264fdf43ddedd0fb1` |

La rueda se descargo aparte, se comprobo, y se instalo **desde el fichero local
ya verificado**, no desde la red. Sus seis dependencias transitivas
(onnxruntime, numpy, protobuf, flatbuffers, packaging, pathvalidate) las
resolvio el instalador contra el indice: eso NO es verificacion a mano y se
declara como tal.

El runtime del modelo no se descargo: la compilacion Vulkan `b10068` ya estaba
en el metal.

## Como cumple D75

Ninguna capa abre un socket. `llama-cli` recibe el caracter por argumento y
escribe a su salida; `piper` recibe el texto por entrada estandar y escribe PCM
crudo por salida estandar. Se pasan el trabajo por tuberia, como programas.

Un detalle medido, no leido: la ayuda de piper 1.6.1 dice que la salida por
defecto es stdout, pero **no es cierto** — sin `-f` intenta REPRODUCIR el audio
y, al no haber reproductor, escribe un `output.wav` en el directorio actual. El
contrato limpio se obtiene con `--output-raw`. Quien lo de por bueno leyendo la
ayuda se encontrara ficheros sueltos y ninguna tuberia.

## Numeros en ESTE metal

| | |
|---|---|
| Sintesis de voz, por invocacion | **0,78-0,80 s** (frio y caliente casi iguales) |
| Las tres capas, pregunta -> audio | **4,57 s** |
| Modelo: prefill / generacion (Vulkan) | 482,17 / 28,69 t/s |

Los 681 ms que figuraban en el canon eran de la fragua y con voz residente tras
un servicio HTTP. Aqui, sin residencia y sin servicio, cada invocacion cuesta
0,8 s. Queda re-medido donde corresponde.

## Uso

    ./aurelius "¿por donde empiezo?"      # español, con voz
    ./aurelius --en "where do I start?"   # ingles, sin voz (la voz es es_ES)
    ./aurelius --muda "..."               # solo texto

`AURELIUS_HABLANTE=1` elige el segundo hablante del modelo de voz: sharvard
trae dos, y la firma de oido se hizo sobre la muestra publica.
