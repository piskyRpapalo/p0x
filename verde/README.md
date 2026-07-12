# Diario Verde — registro visual del crecimiento (fase interior)

Primera ronda: **menta**, en 3 recipientes (`recipiente-1`, `recipiente-2`, `recipiente-3`).

## Invariante

Las fotos son **100% locales al rack**: `verde/fotos/` y `verde/diario.jsonl` están
gitignorados y jamás salen de esta máquina (ni al bare soberano de La Torre).
Solo este README se versiona.

## Estructura

```
verde/
├── README.md        ← este fichero (único trackeado)
├── fotos/           ← <grupo>-<YYYYMMDDTHHMMSS>.jpg (runtime, gitignored)
└── diario.jsonl     ← un objeto por captura (runtime, gitignored)
```

## Esquema de `diario.jsonl` (un objeto JSON por línea)

```json
{
  "id": "recipiente-1-20260712T101500",
  "ts": "2026-07-12T10:15:00+01:00",
  "foto": "fotos/recipiente-1-20260712T101500.jpg",
  "grupo": "recipiente-1",
  "analisis": "pendiente-VLM",
  "modelo_vision": null,
  "sensores": {}
}
```

- `analisis`: texto del modelo de visión LOCAL si existe en el rack; si no hay
  VLM desplegado, queda el valor honesto `"pendiente-VLM"` (honest-sensors:
  jamás se inventa un análisis). `id` es el asidero para un futuro
  re-análisis en lote cuando llegue el modelo.
- `sensores`: hueco reservado para la fase física (humedad / luz / temperatura
  vía RPi+MQTT, roadmap) — el registro por fecha ya tiene sitio para ellos.

## Operación

- `POST /api/verde/captura {"grupo": "recipiente-N"}` en el gateway (:8001)
  dispara la webcam USB del soberano (detección honesta de `/dev/video[0-9]`;
  sin cámara → 503 `no-camera-detected`, no se finge captura).
- Página `/verde` en el dashboard: diario visual descendente.
