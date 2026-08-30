#!/usr/bin/env python3
"""El delta de la sesion y su resumen. Y la cascada de correo, declarada.

DOS SALIDAS Y POR QUE EN ESE ORDEN
-----------------------------------
`delta.md` va primero y es la pieza que de verdad impide perder la linea. El
snapshot responde «como esta todo», que es mucho texto y poca informacion
cuando no ha cambiado nada. El delta responde **«que ha cambiado desde que te
fuiste»**, que es la pregunta que una sesion nueva necesita contestada en diez
segundos.

`resumen-<sello>.html` es el mismo contenido para leer fuera de la terminal --
y el que viajaria por correo el dia que haya correo.

SOBRE EL CORREO
---------------
Medido el 2026-08-30: no hay NADA. Ni sendmail, ni mail, ni msmtp, ni mutt, ni
`~/.netrc`, ni keyring, ni claves de proveedor en el entorno. Y sin sudo no hay
apt, asi que instalar un MTA no es una opcion en este nodo.

La cascada esta escrita entera y se DETECTA en cada corrida, pero el envio va
apagado por defecto. Enviar correo es una accion hacia fuera: necesita bandera
explicita `--email` y una direccion que el Soberano confirme. Nunca se adivina
el destinatario, y nunca se escribe una credencial en este fichero.
"""
from __future__ import annotations

import argparse
import json
import os
import shutil
import sqlite3
import subprocess
import sys
import time
from datetime import datetime
from html import escape
from pathlib import Path

RAIZ = Path(__file__).resolve().parent
ESTADO = RAIZ / "estado.json"
DELTA = RAIZ / "delta.md"
RESUMENES = RAIZ / "resumenes"
DB = Path.home() / "p0x" / "preceptor-internal" / "continuidad" / "continuidad.db"

MARCA = {"OK": "✅", "RED": "🔴", "NO_DATA": "⬜"}


def leer_estado():
    if not ESTADO.exists():
        return None
    try:
        return json.loads(ESTADO.read_text(encoding="utf-8"))
    except ValueError:
        return None


def deltas_de(sesion, limite=40):
    if not DB.exists():
        return []
    con = sqlite3.connect(f"file:{DB}?mode=ro", uri=True, timeout=5)
    try:
        return con.execute(
            "SELECT fecha, area, cambio, evidencia FROM deltas "
            "WHERE sesion=? ORDER BY id DESC LIMIT ?", (sesion, limite)).fetchall()
    except sqlite3.Error:
        return []
    finally:
        con.close()


def render_delta(d, sesion, filas):
    L, A = [], None
    A = L.append
    A(f"# Δ Sesión `{sesion}`")
    A("")
    A("> **Lee esto antes que el snapshot.** «Qué ha cambiado desde que te fuiste» "
      "es la pregunta útil; «cómo está todo» es mucho texto y poca información "
      "cuando no ha cambiado nada.")
    A("")
    if d:
        rojos = [k for k, v in d["componentes"].items()
                 if isinstance(v, dict) and v.get("estado") == "RED"]
        A(f"**Medido:** `{d['generado']}` · modo `{d['modo']}` · "
          f"**{len(rojos)} en rojo**")
        for k in rojos:
            A(f"- 🔴 **{k}** — {d['componentes'][k].get('causa', '?')}")
    else:
        A("**Medido:** ⬜ NO_DATA — no hay `estado.json`.")
    A("")
    A("## Cambios registrados en esta sesión")
    A("")
    if filas:
        A("| Hora | Área | Cambio | Evidencia |")
        A("|---|---|---|---|")
        for f, area, cambio, evid in filas:
            hora = f.split("T")[-1] if "T" in f else f
            A(f"| {hora} | `{area}` | {cambio} | {(evid or '')[:100]} |")
    else:
        A("*Ningún cambio de estado registrado. El rack está donde lo dejaste.*")
    A("")
    A("---")
    A("")
    A("*Generado por `resumen.py`. Contexto completo: "
      "`preceptor-internal/continuidad/bootstrap_continuidad.md`.*")
    return "\n".join(L) + "\n"


def render_html(d, sesion, filas):
    def fila_comp(k, v):
        est = v.get("estado", "?")
        det = v.get("causa") or ", ".join(
            f"{a}={b}" for a, b in v.items()
            if a in ("modelos", "latencia_ms", "pasa", "engramas", "libre_gb",
                     "expuestos", "adaptadores", "serial", "online"))
        return (f'<tr><td class="e {est}">{MARCA.get(est, "?")} {est}</td>'
                f"<td><code>{escape(k)}</code></td>"
                f"<td>{escape(str(det))}</td></tr>")

    comp = (d or {}).get("componentes", {})
    filas_comp = "".join(fila_comp(k, v) for k, v in sorted(comp.items())
                         if isinstance(v, dict) and "estado" in v)
    filas_delta = "".join(
        f"<tr><td>{escape(f.split('T')[-1] if 'T' in f else f)}</td>"
        f"<td><code>{escape(a)}</code></td><td>{escape(c)}</td>"
        f"<td class='ev'>{escape((e or '')[:140])}</td></tr>"
        for f, a, c, e in filas) or (
        "<tr><td colspan='4'><em>Ningún cambio: el rack está donde lo dejaste.</em>"
        "</td></tr>")

    return f"""<!doctype html>
<html lang="es"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Δ {escape(sesion)} · Alejandría</title>
<style>
 :root{{--violeta:#6d5ae0;--bronce:#78624c;--tinta:#1e1826;--marmol:#e4e8ec;
        --ok:#2f8f5b;--red:#c23b3b;--nodata:#8a6d2f}}
 body{{margin:0;padding:1.5rem;background:var(--marmol);color:var(--tinta);
       font:15px/1.55 ui-sans-serif,system-ui,sans-serif;max-width:70ch}}
 h1{{font-size:1.3rem;border-bottom:3px solid var(--bronce);padding-bottom:.4rem}}
 h2{{font-size:1rem;color:var(--bronce);margin-top:1.6rem}}
 table{{width:100%;border-collapse:collapse;font-size:.87rem;margin:.5rem 0}}
 th,td{{text-align:left;padding:.35rem .5rem;border-bottom:1px solid #cfd4da;
        vertical-align:top}}
 th{{color:var(--bronce)}}
 code{{color:#4b37c4}} .ev{{color:#5d5668;font-size:.82rem}}
 td.e{{font-weight:700;white-space:nowrap}}
 td.OK{{color:var(--ok)}} td.RED{{color:var(--red)}} td.NO_DATA{{color:var(--nodata)}}
 blockquote{{border-left:3px solid var(--violeta);margin:0;padding:.3rem .9rem;
             background:#fff;color:#3b3548}}
 footer{{margin-top:2rem;border-top:1px solid var(--bronce);padding-top:.6rem;
         font-size:.8rem;color:#5d5668}}
</style></head><body>
<h1>Δ Sesión {escape(sesion)}</h1>
<blockquote>Lee el delta antes que el snapshot: «qué ha cambiado desde que te
fuiste» es la pregunta útil.</blockquote>
<p><strong>Medido:</strong> <code>{escape((d or {}).get('generado', 'NO_DATA'))}</code>
 · modo <code>{escape((d or {}).get('modo', '?'))}</code></p>
<h2>Cambios de esta sesión</h2>
<table><thead><tr><th>Hora</th><th>Área</th><th>Cambio</th><th>Evidencia</th></tr>
</thead><tbody>{filas_delta}</tbody></table>
<h2>Estado de cada componente</h2>
<table><thead><tr><th>Estado</th><th>Componente</th><th>Detalle</th></tr></thead>
<tbody>{filas_comp}</tbody></table>
<footer>Generado por <code>resumen.py</code> en el nodo soberano.
 Contexto completo en <code>bootstrap_continuidad.md</code>.</footer>
</body></html>
"""


# --------------------------------------------------------------------------
# Cascada de correo. Se DETECTA siempre; se envia solo si se pide.
# --------------------------------------------------------------------------

def detectar_correo():
    """Los cuatro peldanos, en orden, con lo que se encontro en cada uno."""
    peldanos = []

    binarios = [b for b in ("sendmail", "mail", "mailx", "msmtp", "ssmtp", "s-nail")
                if shutil.which(b)]
    peldanos.append({
        "via": "i · cliente local (sendmail/mail/msmtp)",
        "disponible": bool(binarios),
        "detalle": ", ".join(binarios) if binarios
        else "ninguno instalado · y sin sudo no hay apt en este nodo"})

    netrc = Path.home() / ".netrc"
    hay_netrc = netrc.exists()
    modo_ok = False
    if hay_netrc:
        modo_ok = (netrc.stat().st_mode & 0o077) == 0
    peldanos.append({
        "via": "ii · smtplib + credencial en ~/.netrc",
        "disponible": hay_netrc and modo_ok,
        "detalle": ("~/.netrc presente con permiso correcto" if hay_netrc and modo_ok
                    else "~/.netrc con permisos abiertos: se ignora" if hay_netrc
                    else "no existe ~/.netrc. Remedio: crear una contraseña de "
                         "aplicación de Gmail y guardarla ahí con chmod 600. "
                         "Es la vía viable aquí: smtplib y netrc son stdlib, "
                         "no hacen falta ni sudo ni instalación")})

    claves = [k for k in ("MAILGUN_API_KEY", "SENDGRID_API_KEY", "RESEND_API_KEY",
                          "POSTMARK_TOKEN") if os.environ.get(k)]
    peldanos.append({
        "via": "iii · webhook de proveedor",
        "disponible": bool(claves),
        "detalle": (", ".join(claves) + " presente(s) [valor REDACTADO]") if claves
        else "ninguna clave de proveedor en el entorno"})

    peldanos.append({
        "via": "iv · solo local (siempre disponible)",
        "disponible": True,
        "detalle": f"resumen guardado en {RESUMENES}"})
    return peldanos


def enviar(destino, asunto, cuerpo_html, peldanos):
    """Envia por el primer peldano disponible. Devuelve (ok, via, detalle)."""
    for p in peldanos[:-1]:
        if not p["disponible"]:
            continue
        if p["via"].startswith("i ·"):
            binario = shutil.which("sendmail") or shutil.which("msmtp")
            msg = (f"To: {destino}\nSubject: {asunto}\n"
                   f"Content-Type: text/html; charset=utf-8\n\n{cuerpo_html}")
            try:
                subprocess.run([binario, "-t"], input=msg, text=True,
                               check=True, timeout=60)
                return True, p["via"], f"entregado a {binario}"
            except Exception as e:
                return False, p["via"], f"{type(e).__name__}: {e}"
        if p["via"].startswith("ii ·"):
            # La credencial NUNCA se escribe aqui: sale de ~/.netrc, que es del
            # Soberano y no del repositorio.
            import netrc as _netrc
            import smtplib
            from email.message import EmailMessage
            try:
                maquina = "smtp.gmail.com"
                auth = _netrc.netrc().authenticators(maquina)
                if not auth:
                    return False, p["via"], f"~/.netrc no tiene entrada para {maquina}"
                usuario, _, clave = auth
                m = EmailMessage()
                m["From"], m["To"], m["Subject"] = usuario, destino, asunto
                m.set_content("Resumen en HTML.")
                m.add_alternative(cuerpo_html, subtype="html")
                with smtplib.SMTP_SSL(maquina, 465, timeout=30) as s:
                    s.login(usuario, clave)
                    s.send_message(m)
                return True, p["via"], f"enviado a {destino}"
            except Exception as e:
                return False, p["via"], f"{type(e).__name__}: {e}"
    return False, "iv · solo local", "ningún transporte disponible"


# --------------------------------------------------------------------------

def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--sesion", required=True)
    ap.add_argument("--email", action="store_true",
                    help="intenta enviar el resumen. Apagado por defecto: enviar "
                         "correo es una acción hacia fuera")
    ap.add_argument("--a", metavar="DIRECCION",
                    help="destinatario. Obligatorio con --email: no se adivina")
    a = ap.parse_args(argv)

    d = leer_estado()
    filas = deltas_de(a.sesion)

    DELTA.write_text(render_delta(d, a.sesion, filas), encoding="utf-8")
    RESUMENES.mkdir(parents=True, exist_ok=True)
    sello = datetime.now().strftime("%Y%m%d-%H%M%S")
    destino_html = RESUMENES / f"resumen-{sello}.html"
    html = render_html(d, a.sesion, filas)
    destino_html.write_text(html, encoding="utf-8")

    print(f"  delta   → {DELTA}")
    print(f"  resumen → {destino_html}")

    peldanos = detectar_correo()
    print("  correo · cascada detectada:")
    for p in peldanos:
        print(f"    {'✅' if p['disponible'] else '⬜'} {p['via']} — {p['detalle']}")

    if not a.email:
        vivos = [p for p in peldanos[:-1] if p["disponible"]]
        if not vivos:
            print("  ⬜ NO_DATA · email no configurado — resumen en "
                  f"{RESUMENES}/")
        else:
            print("  (hay transporte, pero el envío requiere --email y --a)")
        return 0

    if not a.a:
        print("  🔴 --email sin --a: no se adivina el destinatario.", file=sys.stderr)
        return 1
    ok, via, detalle = enviar(a.a, f"Δ Alejandría · {a.sesion}", html, peldanos)
    print(f"  {'✅' if ok else '🔴'} envío por {via} — {detalle}")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
