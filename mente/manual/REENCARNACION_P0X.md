---
id: operativo-reencarnacion-p0x
titulo: "Reencarnación P0X — reconstruir el sistema desde cero con lo que existe HOY"
tipo: operativo
clase: operativo
nivel: vivo
enlaces:
  - manual-del-soberano
  - proyecto-reflejos
  - edge-ai
metrica_exito: "una fragua muerta vuelve a servir gateway+dashboard+mente en <2h siguiendo SOLO este documento; 0 pasos que dependan de infraestructura que no existe"
umbral_reedicion: "cambio de topología (nodo nuevo/retirado), cambio del stack docker, o un drill real que revele un paso falso"
actualizado: 2026-07-11
descripcion_niveles:
  basico: "Si el ordenador principal muere, este documento explica cómo reconstruirlo todo desde las copias que viven en el segundo ordenador (La Torre). Sin nube, sin magia: git, unos servicios y paciencia."
  medio: "El genoma real del sistema son 3 repos git bare en La Torre (p0x, hexelion, hexelion-lab) que se sincronizan en cada misión, más el conocimiento re-derivable (Qdrant se reconstruye por ingesta). Este runbook lista los pasos reales de reconstrucción de La Fragua y marca honesto lo que NO está cubierto (secretos .env, estado Redis efímero)."
  experto: "Sustituye al HEXELION_REENCARNACION de mayo-2026 (enterrado el mito; el runbook citaba NPU/RKLLM, Bóveda Genoma cifrada de 4 capas, VLAN 10 y 7 namespaces Qdrant que jamás existieron — veredicto arqueología #42). Este documenta la realidad: Ubuntu ARM + tailnet, docker redis/qdrant/minio, ~20 units systemd cuyas copias canónicas viven en deploy/ y en los repos, receta certificada de La Torre (ctx6144+FA+q8+batch256, tag instruct explícito), y los 3 huecos honestos con su mitigación manual."
---

# REENCARNACIÓN P0X — runbook real (2026-07-11)

> Reemplaza al `HEXELION_REENCARNACION.md` de mayo (enterrado en la Necrópolis
> con el mito: describía NPU/RKLLM, "Bóveda Genoma" cifrada, VLAN 10 y
> namespaces que **jamás existieron**; su drill nunca corrió). Esto es lo que
> HAY. Documentación — no probado destructivamente; primer drill pendiente.

## El genoma real (dónde está la verdad)

| Qué | Dónde | Estado |
|---|---|---|
| Código + mente + doctrina + deploy | **bare repos en La Torre** (`~/p0x.git`, `~/hexelion.git`, `~/hexelion-lab.git`, usuario jetson, tailnet) | ✅ push soberano en cada misión |
| Conocimiento vectorial (Qdrant) | RE-DERIVABLE: `ingest_mente.py` lo reconstruye desde `mente/**` | ✅ por diseño |
| Grafo second_brain | RE-DERIVABLE: `build_graph.py` | ✅ por diseño |
| Units systemd (~20) | copias canónicas en `deploy/{fragua,torre,vigia}/` + repo hexelion; las instaladas viven en `/etc/systemd/system/` | ⚠️ ver hueco H2 |
| Modelos LLM | Ollama re-descarga por tag (torre: `qwen3:4b-instruct-2507-q4_K_M` — JAMÁS el tag pelado) | ✅ reproducible |
| Secretos (`hexelion/config/.env`, tailscale, ssh, NUT passwords) | SOLO en la máquina viva | 🔴 hueco H1 |
| Estado Redis (bitácora, telemetría caliente) | efímero (TTLs) | aceptado: se pierde, se regenera |

## Reconstrucción de La Fragua (muerta → sirviendo)

1. **SO**: Ubuntu 24.04 ARM64 (Joshua Riek) en el NVMe del Orange Pi 5 Plus.
   Usuario `ubuntu`. `apt install docker.io task-spooler nut python3-pip`.
2. **Red**: instalar tailscale y re-autenticar el nodo (mano del Soberano —
   la identidad tailnet no es restaurable desde git). Verificar que La Torre
   responde por su IP de tailnet.
3. **Clonar el genoma** (desde La Torre):
   `git clone jetson@<torre>:p0x.git /mnt/nvme/p0x` ·
   `git clone jetson@<torre>:hexelion.git ~/hexelion` ·
   `git clone jetson@<torre>:hexelion-lab.git ~/hexelion-lab`.
4. **Secretos** (hueco H1): restaurar `~/hexelion/config/.env` desde la copia
   física del Soberano (ver Huecos). Sin él, Qdrant rechaza (`QDRANT_API_KEY`).
5. **Docker**: `redis:7-alpine` (publicado SOLO en tailnet + allowlist — usar
   la unit `hexelion-redis-allowlist`), `qdrant/qdrant`, `minio/minio`;
   recrear SIEMPRE con `docker compose up -d` (jamás `docker start` suelto:
   cicatriz 2026-06-17, Redis volvió desatachado de su red).
6. **Units**: copiar desde `deploy/` y el repo → `/etc/systemd/system/`,
   `daemon-reload`, habilitar el núcleo en orden: redis-allowlist →
   gateway (:8001) → pollers → faro (:8100) → vigilia → vocero-omie →
   bridge/aisstream → p0x-voz → timers (bitacora, cosecha, guardian, disk).
7. **NUT**: `ups.conf`/`upsmon.conf` (driver blazer_usb, ups `greencell`);
   verificar `upsc greencell` → `OL`.
8. **Mente**: `bin/p0x-enqueue python3 mente/pipeline/ingest_mente.py` —
   reconstruye Qdrant Y el grafo. Verificar nodo+links con `jq`.
9. **Ollama local** (fragua): `ollama pull qwen2.5:1.5b` (bitácora/fallback) +
   `nomic-embed-text` (embeddings de ingesta).
10. **Verificación**: `curl :8001/api/system/state` (la Ventana de Estado es
    el checklist vivo: 5 secciones con fuente) · dashboard `:8001/dashboard` ·
    `tools/audit_links.py` 0 rotos.

## Los otros nodos

- **La Torre** (Jetson, CUDA): receta certificada en `deploy/torre/`
  (`modelo_residente.sh`: ctx6144+FA+q8+batch256, keep_alive=-1). Los bare
  repos VIVEN aquí — si muere La Torre, el genoma sigue en la fragua viva
  (los repos de trabajo son clones completos): re-crear bares con
  `git clone --bare` y re-apuntar `origin`.
- **El Vigía** (Pi): `deploy/vigia/` (ingest_m5 + firmware platformio en
  `~/p0x-telemetry` del Pi, copia canónica en `deploy/vigia/firmware/`);
  ais-catcher/dump1090 con el gate por serial (`ais-catcher-wait.sh`).
- **El M5**: reflashear desde `deploy/vigia/firmware/` + `set_rtc_m5.py`
  (hora de Lisboa al DS3231).

## Huecos honestos (mitigación = mano del Soberano)

- **H1 · Secretos**: `.env` (QDRANT_API_KEY), passwords NUT, identidad
  tailscale y claves ssh NO están en git (correcto: git es el genoma público
  interno). Mitigación: copia física del Soberano (USB) actualizada al cambiar
  un secreto. **Pendiente de crear — es LA pieza que falta.**
- **H2 · Deriva units**: lo instalado en `/etc/systemd/system/` puede divergir
  de las copias del repo. Mitigación: tras tocar una unit instalada,
  actualizar su copia canónica en el repo (regla de la casa).
- **H3 · Drill**: este runbook NO se ha ejecutado en frío. Primer drill =
  restaurar en un SBC de repuesto y cronometrar (sugerencia en PENDIENTES).

*(v1 — sustituye al mito de mayo con la realidad de julio. El drill lo valida.)*
