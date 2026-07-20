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

---

# Ciudadanía del Chat (misión Reparación y Ciudadanía del Chat, 2026-07-20)

El carbono firmó dos decisiones: el Chat es la **tercera cara** del organismo (Puente de 3 caras,
ver `hexelion/dashboard`), y viste **piel del Nexo** (brutalismo soberano, EN).

## Piel del Nexo — APLICADA y verificada (Bloque B)

- **Fuente de verdad:** `deploy/soberano/chat-nexo.css` (versionada en el repo).
- **Mecánica (sin tocar el core):** OpenWebUI carga `/static/custom.css` en su `index.html`
  (línea 35, antes de su propio CSS). Es Tailwind v4 y expone su paleta como variables
  `--color-*`/`--font-*`/`--radius-*`; el CSS las remapea a la paleta Nexo con `!important` (gana
  sin depender del orden de carga). Cero clases parcheadas, cero core modificado.
- **Aplicado el 2026-07-20:**
  `cp deploy/soberano/chat-nexo.css <site-packages>/open_webui/static/custom.css`
  (ruta real: `~/.local/share/uv/tools/open-webui/lib/python3.12/site-packages/open_webui/static/`).
  Verificado servido: `curl http://100.81.82.34:8080/static/custom.css` → 4032 bytes, no vacío.
  **No requiere restart** (archivo estático). Cache-bust en el navegador si no se ve al instante.
- **RE-APLICAR TRAS UPGRADE:** `custom.css` vive dentro del paquete pip; un `uv tool upgrade
  open-webui` lo pisa (lo deja vacío). Tras cualquier upgrade, repetir el `cp`. (Sugerencia #146:
  hook post-upgrade o symlink.)
- **Límites de OpenWebUI (declarados, no forzados):**
  1. **IBM Plex Mono no viene bundleada** (solo NotoSans) → se cae a mono del sistema. Para la
     tipografía exacta: meter el woff2 en `static/fonts` + `@font-face` en el custom.css (paso
     opcional, no hecho para no inflar el nodo con assets sin pedir).
  2. **El botón primario de OpenWebUI es `bg-black/bg-white`** (monocromo), no una variable de
     acento tematizable — se recolorea con el fondo pero no toma el fósforo. Aceptado.

## Branding EN — documentado para tu sesión (env del unit, no aplicado)

Añadir al `open-webui.service` (`~/.config/systemd/user/open-webui.service`) y `systemctl --user
daemon-reload && systemctl --user restart open-webui`. NO se aplicó por CC para no reiniciar tu
servicio mientras montas la cuenta admin (hazlo en la misma sesión):

```ini
Environment=WEBUI_NAME=P0X · EL NEXO
Environment=DEFAULT_LOCALE=en
```

`WEBUI_AUTH=true` ya está. **NO** pongas `ENABLE_SIGNUP=false` en el env todavía: bloquearía crear
la primera cuenta. Se desactiva DESPUÉS (ver §FIN).

## §FIN · Pasos que solo cruza el carbono (el silicio no toca esta puerta)

1. **Cuenta admin — PRIMERO Y CRÍTICO.** `onboarding:true` verificado (no hay admin). En OpenWebUI
   **la primera cuenta registrada se vuelve administradora**. Pasos exactos:
   a. Abre `http://soberano.tailb9e0f7.ts.net:8080` desde un dispositivo del tailnet (tu Android).
   b. Regístrate con tu correo + contraseña fuerte → esa cuenta es admin.
   c. **Ajustes de admin → General → desactiva `Enable New Sign Ups`.** Hasta ese clic, cualquiera
      con la URL puede auto-registrarse: **no compartas la URL ni el nodo hasta desactivarlo.**
   d. Verifica que `qwen3-coder:30b` / `soberano-coder` aparecen en el selector de modelos.
2. **Cuentas de hermanos:** las creas tú (Admin → Users → Add) tras (1), con el **contrato de datos
   de 5 líneas** pegado en el primer login (sigue pendiente de redactar — hueco real).
3. La piel Nexo ya se ve al abrir; si quieres el nombre "P0X · EL NEXO" y el idioma EN forzado,
   aplica el env de arriba en esa misma sesión.
