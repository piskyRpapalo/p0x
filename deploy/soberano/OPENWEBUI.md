# OpenWebUI · ventana de los hermanos (prep F2-alfa) — Misión G0, 2026-07-18

## Instalación

`uv tool install open-webui --python 3.12` (espacio de usuario, sin sudo). El Python del sistema
(3.14, sin `pip`/`ensurepip`) no sirve — `pyarrow` (dependencia transitiva) no tiene wheel prebuilt
para 3.14 y su build desde fuente necesita `cmake` (no instalado, sin sudo). Con `--python 3.12`
`uv` trae su propio intérprete y todo instala desde wheels, sin compilar nada.

## Servicio

`systemd --user` (`deploy/soberano/open-webui.service`, copia versionada de
`~/.config/systemd/user/open-webui.service`). Requiere `loginctl enable-linger pisky` (no pidió
sudo, funcionó directo) para que sobreviva sin sesión interactiva abierta.

- `OLLAMA_BASE_URL=http://127.0.0.1:11434` — Ollama local.
- `ExecStart=... serve --host 100.81.82.34 --port 8080` — bind **exclusivo** a la IP del tailnet
  (no `0.0.0.0`, no la interfaz LAN `eno1`).
- `WEBUI_AUTH=true` — auth obligatoria (no hay cuentas creadas todavía, ver más abajo).

## Verificación doble (hecha en esta misión)

- `curl http://100.81.82.34:8080/` → `200` desde el propio nodo (mismo resultado esperado desde
  cualquier otra máquina del tailnet).
- `curl http://192.168.50.202:8080/` (IP LAN) → sin respuesta (`000`, conexión rechazada/timeout).
- `ss -tlnp | grep 8080` confirma un único socket en escucha: `100.81.82.34:8080` (no `0.0.0.0`).

## Pendiente — mano de David (no se hace en esta misión)

1. Abrir `http://100.81.82.34:8080` desde un dispositivo del tailnet.
2. Crear la **primera cuenta** (se convierte automáticamente en admin en OpenWebUI — es la firma
   del carbono, no la hace el silicio).
3. Verificar que `qwen3-coder:30b` / `soberano-coder` aparecen en el selector de modelos (conectan
   vía `OLLAMA_BASE_URL`, ya configurado y confirmado por `environ` del proceso).
4. **Contrato de datos pendiente de redactar**: qué pueden ver/hacer los "hermanos" con acceso a
   esta ventana, retención de conversaciones, etc. — no existe todavía, es un hueco real antes de
   dar la primera cuenta a alguien que no sea David.
