# Propuesta · nginx para las descargas del LoRAtelier

**Propose-only.** Nada de esto se ha ejecutado: la primera parte pide `root` en
`soberano` y la segunda pide consola en `la-fragua`, y hacia allí este nodo es
propose-only por canon.

Fecha: 2026-09-06 · medido, no supuesto.

---

## Parte 1 · Por qué se cierra la página en el teléfono

**Causa, con una línea señalada.** La configuración actual de
`/etc/nginx/sites-available/preceptoros-downloads` lleva:

```nginx
add_header Content-Disposition attachment;
```

Está **dentro del `location /downloads/`**, así que se aplica a *todo* lo que
cuelga de ahí — el README y el propio listado de directorio incluidos. Ese
encabezado significa «no muestres esto, descárgalo». El navegador del teléfono
obedece: manda la respuesta al gestor de descargas y cierra la vista. No es un
fallo de la página; es que le estamos diciendo que no es una página.

Medido ahora mismo desde la malla:

```
/downloads/README.md   →  200 · Content-Type: application/octet-stream
                              Content-Disposition: attachment
/downloads/            →  200 · Content-Type: application/json
```

**Y una trampa que sobrevive al arreglo:** `Cache-Control: public,
max-age=31536000` son 365 días. La respuesta cacheada lleva el `attachment`
dentro, así que **el teléfono seguirá descargando en vez de mostrar hasta que se
borren los datos del sitio**, aunque nginx ya esté corregido. Al aplicar esto,
borrar datos del sitio en el móvil antes de volver a probar.

### La corrección

```nginx
server {
    listen 8081;
    listen [::]:8081;
    server_name _;

    # El listado, como PÁGINA y no como fichero JSON que el navegador se baja.
    location /downloads/ {
        alias /home/pisky/p0x/preceptoros-web/public/downloads/;  # guardia:permitir es una config de nginx, la ruta ES el contenido
        autoindex on;
        autoindex_format html;

        # El .md se lee, no se descarga. Sin esto nginx lo manda como
        # `application/octet-stream`, que para un navegador es «fichero».
        types { text/markdown md; text/plain txt sha256; }
        default_type text/plain;

        charset utf-8;

        # Cache CORTA para lo que se lee. Un año en un README es un README que
        # no se puede corregir.
        add_header Cache-Control "public, max-age=300";
        add_header Access-Control-Allow-Origin *;
    }

    # `attachment` SOLO donde toca: los pesos. Un location anidado, para que el
    # encabezado no alcance a nada más.
    location ~ \.gguf$ {
        alias /home/pisky/p0x/preceptoros-web/public/downloads/;  # guardia:permitir es una config de nginx, la ruta ES el contenido
        add_header Content-Disposition attachment;
        add_header Access-Control-Allow-Origin *;
        add_header Cache-Control "public, max-age=31536000, immutable";
    }

    location / {
        default_type text/plain;
        return 404 "PreceptorOS Downloads · usa /downloads/\n";
    }
}
```

> ⚠️ **Ojo con el `alias` en el `location ~ \.gguf$`**: con una expresión regular,
> `alias` se comporta distinto que con un prefijo. Si al probar da 404, la forma
> segura es anidar dentro del primero:
>
> ```nginx
> location /downloads/ {
>     alias /home/pisky/p0x/preceptoros-web/public/downloads/;  # guardia:permitir config de nginx
>     ...
>     location ~ \.gguf$ {
>         add_header Content-Disposition attachment;
>         add_header Cache-Control "public, max-age=31536000, immutable";
>     }
> }
> ```

**Aplicar y comprobar:**

```bash
sudo nginx -t && sudo systemctl reload nginx
curl -sI http://127.0.0.1:8081/downloads/README.md | grep -i 'content-type\|disposition'
# esperado: text/markdown · SIN Content-Disposition
curl -sI http://127.0.0.1:8081/downloads/preceptor-tribune-en-v1.gguf | grep -i disposition
# esperado: attachment
```

**Y una nota sobre la ruta que sirve.** La ruta que nginx tenía en el `alias` era
un directorio suelto con un solo fichero, distinto del repositorio versionado de
la web. Lo que se publicaba ahí no llegaba nunca a git, y lo que se commiteaba no
llegaba nunca a nginx. Se ha convertido en un
**enlace simbólico** al repositorio de verdad, así que la configuración de arriba
no cambia de ruta y ahora sirve lo versionado. El andamio anterior está guardado
en el scratchpad de la sesión por si hacía falta.

---

## Parte 2 · El proxy en La Fragua, para la vía pública

Esto **no se puede aplicar desde `soberano`**: la-fragua es otro nodo y hacia
allí este es propose-only. Va como texto para copiar y pegar en esa consola.

**Antes de nada, una decisión del Soberano:** `preceptoros.org` lo sirve
Cloudflare. Meter `/downloads/` en ese mismo dominio exige tocar el enrutado en
el panel de Cloudflare, no solo nginx. Es más limpio un subdominio propio,
`downloads.preceptoros.org`, apuntado al túnel — así el sitio estático y las
descargas no se pisan.

`/etc/nginx/sites-available/preceptoros-downloads` **en la-fragua**:

```nginx
server {
    listen 80;
    server_name downloads.preceptoros.org;

    # La direccion de malla del Beelink. NO se escribe aqui a proposito: este
    # repositorio es publico y la guardia de higiene lo impide, con razon.
    # Se obtiene en el propio Beelink con `tailscale ip -4` y se pega al aplicar.
    set $soberano <IP-DE-MALLA-DEL-BEELINK>:8081;

    location /downloads/ {
        proxy_pass http://$soberano;
        proxy_set_header Host $host;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

        # Un GGUF son 52 MB. Sin esto nginx lo bufferiza entero en disco antes
        # de empezar a servir, y con varias descargas a la vez llena /var.
        proxy_max_temp_file_size 0;
        proxy_buffering off;
        proxy_request_buffering off;

        # Una descarga lenta desde un móvil por red móvil tarda. Los tiempos por
        # defecto (60 s) la cortan a la mitad.
        proxy_connect_timeout 30s;
        proxy_send_timeout    600s;
        proxy_read_timeout    600s;

        client_max_body_size 0;
    }

    location / {
        default_type text/plain;
        return 404 "PreceptorOS Downloads · usa /downloads/\n";
    }
}
```

**Habilitar y recargar, en la-fragua:**

```bash
sudo ln -sf /etc/nginx/sites-available/preceptoros-downloads \
            /etc/nginx/sites-enabled/preceptoros-downloads
sudo nginx -t && sudo systemctl reload nginx
```

**Comprobar desde fuera de la malla** (desde datos móviles, no desde wifi de
casa, que si no se resuelve por la malla y no prueba nada):

```bash
curl -sI https://downloads.preceptoros.org/downloads/preceptor-tribune-en-v1.gguf
```

**Y lo que falta después**, que no es nginx: apuntar `downloads.preceptoros.org`
al túnel en Cloudflare. Mientras eso no exista, la ruta relativa
`/downloads/…` que lleva el registro seguirá dando 404 en la vía pública — y por
eso el bloque está en `beta` y no en `disponible`. Un botón que falla para todo
visitante de fuera es peor que no tener botón.

---

## Lo que NO se propone

- **Ningún servicio nuevo ni ningún timer.** Crear una unidad es dejar algo
  corriendo con permisos cuando nadie mira; eso se pide firmado y por separado.
- **Ni un cambio aplicado por SSH desde aquí a la-fragua.** Es la línea que este
  nodo no cruza.
