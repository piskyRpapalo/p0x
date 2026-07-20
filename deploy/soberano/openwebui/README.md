# Piel del Nexo para el Chat (OpenWebUI) — nodo `soberano`

Misión *Reparación y Ciudadanía del Chat* (2026-07-20). El carbono firmó que el
Chat viste identidad del **Nexo** (brutalismo soberano, inglés). Aquí vive el
CSS y su vía de aplicación. **El core de OpenWebUI no se toca.**

## Límite honesto de OpenWebUI (verificado en la v0.10.2 instalada)

- **No hay campo de "CSS custom" en el panel admin.** La tematización por CSS se
  hace por un fichero: OpenWebUI enlaza `<link href="/static/custom.css">` en su
  `index.html` (hook de extensión, **vacío por defecto**). Esa es la única vía
  soportada sin tocar el core.
- **La reciprocidad Chat → dashboard es parcial.** CSS no puede inyectar un
  enlace funcional; un botón "volver al Nexo" de primera clase exigiría core/JS
  de OpenWebUI, que no se toca. Por ahora el regreso es el botón *atrás* del
  navegador o el marcador del dashboard. (El enlace de ida dashboard → Chat sí
  existe: es la tercera cara del Puente.)
- **Alcance del CSS:** re-colorea la escala de grises (superficies), los acentos
  de marca (emerald/blue → phosphor), el radio (→ 0) y la tipografía. Iconos,
  gradientes internos y estados que no leen las variables de Tailwind **no** se
  tematizan sin tocar el core. Requiere el **modo Dark** de OpenWebUI (su
  defecto).
- **Tipografía:** el `@import` de la Plex Mono necesita salida a Google Fonts; si
  el navegador está en tailnet puro (sin internet) o una CSP lo bloquea, cae a
  la mono del sistema — la piel sobrevive, sin la Plex Mono.

## Aplicación — dos caminos (mano del carbono; ninguno toca el core)

`custom.css` se sirve por `StaticFiles`, así que **basta recargar la página**
tras cambiarlo — sin reinicio del servicio.

### Camino A · rápido (no sobrevive a `uv tool upgrade`)

Copiar la piel al hook vacío que ya existe:

```bash
cp ~/p0x/deploy/soberano/openwebui/nexo-skin.css \
   ~/.local/share/uv/tools/open-webui/lib/python3.12/site-packages/open_webui/static/custom.css
```

`VERIFY:` `curl -s http://soberano.tailb9e0f7.ts.net:8080/static/custom.css | head -1`
→ imprime la primera línea del comentario de cabecera (hoy: vacío).

Se pierde al actualizar OpenWebUI (habría que recopiar). Por eso existe el B.

### Camino B · recomendado, upgrade-safe (`STATIC_DIR` de usuario)

OpenWebUI lee el directorio estático de `STATIC_DIR` (env, defecto
`.../site-packages/open_webui/static`). Se apunta a un directorio propio:

```bash
mkdir -p ~/.config/openwebui-static
cp -r ~/.local/share/uv/tools/open-webui/lib/python3.12/site-packages/open_webui/static/. \
      ~/.config/openwebui-static/                       # base: favicons, logo, fuentes…
cp ~/p0x/deploy/soberano/openwebui/nexo-skin.css \
   ~/.config/openwebui-static/custom.css                # la piel
# En el drop-in del servicio systemd --user de open-webui, añadir:
#   Environment=STATIC_DIR=%h/.config/openwebui-static
systemctl --user daemon-reload && systemctl --user restart open-webui.service
```

`VERIFY:` mismo `curl` de arriba tras recargar. Sobrevive a upgrades del paquete
(el `custom.css` vive fuera de `site-packages`).

## Orden correcto (importa)

1. **PRIMERO** el carbono crea la cuenta admin y desactiva sign-ups (ver
   `mente/reportes/` de esta misión, §FIN.1). Hasta entonces nadie recibe la URL.
2. Luego aplica esta piel (A o B) y confirma en su Android que el login del Chat
   ya se ve al carbón del Nexo.
3. Luego crea las cuentas de los hermanos con el contrato de datos.
