# PRECHECK SOBERANO · medido 2026-08-16 · verdad, no hipótesis
# Cowork razona sobre esto, no lo redescubre.

## §1 · BEELINK (soberano) · MEDIDO
CPU AMD Ryzen 7 255 (8C/16T, 4.9GHz) · iGPU Radeon 780M (Vulkan,
  /dev/dri/renderD128) · RAM 57Gi total (64GB físico), 46Gi libre ·
  NVMe 915G, 541G disp.
MODELOS YA EN DISCO (no descargar):
  · Qwen3-Coder-30B-A3B-Instruct-Q4_K_M.gguf (18G) → cerebro privado
  · Qwen3-4B-Instruct-2507-Q4_K_M.gguf (2.4G) → gerente público actual
  · flux1-schnell-Q4_K_M.gguf (6.5G, en ComfyUI) → imagen
SOFTWARE INSTALADO: ollama (no corriendo), openscad 2021.01, bambu-studio
  2.7.1 (flatpak), python 3.14.4.
FALTAN EN PATH: piper (aunque .onnx existe en ~/.aurelius/voz/), llama-cli,
  whisper-cli.
~/.aurelius (61M): memory.db 32K (0 engrams,1 profile) · WAL 0 · 6 WAV sala ·
  voz es_ES-davefx onnx 61M.
p0x: rama master, 5 commits sin push (19244ef..20f7ed7), gate D8_JAMAS activo.
aurelius-mvp vive EN ~/p0x/aurelius-mvp/, no en ~.
CARPETAS NUEVAS (tamaños): ComfyUI 163G · soberano-bench 21G · CineK_Studio
  36M · cine_soberano_app 1.6M · codice-emancipacion-atomica 736K ·
  propuestas 16K · Cuarentena 5.3M.
AGUJERO SVALBARD: ~/aurelius-copia-2026-08-16.tgz (57M) en MISMO disco.
RECUPERACIÓN NO-DESTRUCTIVA: ejecutada y VERDE 7 criterios (--verify VALID).

## §2 · JETSON (la-torre) · MEDIDO · SSH <USER_AT_NODE>
CPU ARMv8 6-core · GPU Orin (nvgpu) · RAM 7.4Gi (6 libre) · NVMe 172G, 83G disp.
OLLAMA 0.11.4 CORRIENDO con modelos: qwen3:4b-instruct-2507-q4_K_M (2.5G),
  qwen3:4b, hexelion:latest (2.0G), qwen2.5:1.5b, llama3.2:3b.
YA TIENE (no reinstalar): ComfyUI · hexelion.git · hexelion-lab.git ·
  hexelion_sinodo · p0x.git · jardin-des-ombres.git · jetcam · jetson-gpio ·
  cinek_automatico. → Hexelion-3D arranca aquí, no de cero.

## §3 · FRAGUA (OPi5 Plus) · MEDIDO · SSH <USER_AT_NODE>
CPU RK3588 (aarch64) · RAM 15Gi (14 libre) · / 59G (29 disp) ·
  <NVME> 3.7T (3.5T disp, 2%).
SDR ADS-B ACTIVO: dump1090 corriendo (dev 00001090) + RTL2838 conectado.
M5Stack (usb-Hades2001_M5stack_6952B20639-if00-port0) CONECTADO AQUÍ.
→ NODO SVALBARD: 3.5T libres en máquina distinta = destino del .tgz.

## §4 · VIGÍA (RPi 5) · MEDIDO · SSH <USER_AT_NODE>
CPU BCM2712 (kernel 6.12.75+rpt-rpi-2712, aarch64) · RAM 4.0Gi (3.6 libre) ·
  SD 58G, 50G disp (12%). Temp ~49°C post-boot.
Proceso: ais-catcher-wait.sh (wrapper que arranca ais-catcher cuando detecta
  el SDR). SE RECUPERA SOLO tras reboot (servicio activo). SDR AIS NO está
  conectado ahora; el script espera. M5Stack NO está aquí (ver §3).
→ Nodo ligero auto-recuperable. Cuando conectes SDR AIS, arranca solo.

## §5 · RED TAILSCALE · MEDIDO
Activos: soberano (<TAILNET_IP>) · el-vigia (<TAILNET_IP>) · la-fragua
  (<TAILNET_IP>) · la-torre/Jetson (<TAILNET_IP>, active direct).
Offline: desktop-quob12l, fedora, krista, musculo-hp-01, musculo-hp-02, s110.

## §6 · ACCIONES SOLO DEL SOBERANO (firmables)
1. SVALBARD: scp ~/aurelius-copia-2026-08-16.tgz a <NODE>:<NVME>/
   → desbloquea prueba destructiva.
2. PUSH: resolver D8_JAMAS de los 5 commits (origin privado).
3. INSTALAR: piper en PATH · compilar llama-cli · compilar whisper-cli.
4. CRIBA CINE: CineK_Studio vs cine_soberano_app → UNA viva, otra a
   necropolis/. Vacíos (¿para,¿por,No) → archivar.
5. Firmar el manifiesto de variantes (bin/variantes + fitness functions).

## §7 · HIPÓTESIS DEL BRIEF QUE CC DEBE MEDIR (NO_DATA hasta medir)
· Qwen3-Coder-Next 80B Q4_K_M: ¿cabe en 57Gi RAM? ¿tok/s real en iGPU?
· Anomalía MoE en CPU (3-4× más lento que bandwidth predice).
· ik_llama.cpp como FIX potencial (1.9× mejora).
· SQLite WAL checkpoint antes de sign: ¿está ya en manifest.py?
