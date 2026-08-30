#!/usr/bin/env python3
"""Genera el onboarding en los tres idiomas desde UNA estructura.

POR QUE SE GENERA
-----------------
La paridad i18n se pide «real, no copia». Tres ficheros escritos a mano
empiezan iguales y divergen a la tercera edicion: alguien arregla un boton en
`es` y `fr` se queda con el viejo, y eso no lo ve nadie hasta que un francofono
se topa con el hueco. Aqui la ESTRUCTURA es una y el COPY es un diccionario por
idioma: si falta una clave, este guion para y lo dice; no puede haber deriva.

UNA PAGINA, CUATRO SECCIONES
----------------------------
El encargo pedia «4 pantallas» y la reorientacion pedia «1 pantalla con 2
caminos y secciones scrolleables». Se cumplen las dos con un solo fichero de
cuatro secciones: son cuatro pantallas para quien las recorre, y una sola
pagina para el tope del Agora -- que esta en 6 de 7, y cuatro ficheros lo
habrian reventado en el primer commit.

Dry-run por defecto; `--si` escribe.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

WEB = Path.home() / "preceptoros-web" / "public"
RELEASES = "https://github.com/piskyRpapalo/PreceptorOS/releases/latest/download"

# Los tres assets del encargo. Todavia NO existen: la Fase 2 los construye.
# El boton apunta ya a su URL definitiva -- lo pide el gate -- pero la pagina
# DICE que aun no estan. Un boton que promete una descarga que da 404 es
# exactamente el sensor deshonesto que esta casa no admite.
# Android HOY es Termux, y el APK queda declarado futuro: lo fija plan_v5 en
# su seccion TERMINOLOGIA, y el Soberano lo firmo al resolver el PARO 1. No se
# construye un APK sin cadena de herramientas ni sudo; y un boton que ofrece un
# APK que no existe es peor que no tener boton. El camino de Android ya
# funciona y esta escrito: la guia de Termux de esta misma web.
DESCARGAS = [("android", "./instalar.html#android"),
             ("pc", f"{RELEASES}/install.sh"),
             ("win", f"{RELEASES}/install.ps1")]

COPY = {
 "es": {
  "lang": "es", "titulo": "Empieza aquí · PreceptorOS",
  "desc": "El Instalador te acompaña: instala la app y elige el compañero que encaja con lo que quieres hacer.",
  "marca": "Empieza aquí", "volver": "Portada",
  "obSaluda": "Soy el Instalador. Te acompaño hasta que tengas la app funcionando y hayas elegido a tu compañero. Dime por dónde quieres ir.",
  "obAtajo": "Directo, entonces. Baja: ahí están las tres descargas.",
  "obLargo": "Bien. Te enseño primero qué se queda en tu máquina y qué no.",
  "obQue": "PreceptorOS es la aduana entre tus datos y las IAs de la nube.",
  "obPriv": "Esto no es una promesa: es un filtro que puedes probar ahora mismo.",
  "obDesc": "Elige tu sistema. La app es el taller; yo sigo contigo dentro.",
  "obConec": "Este código de vinculación enlaza tu identidad de la web con la app. Es tuyo y solo tuyo.",
  "obVinculado": "Ahí lo tienes. Ábrelo en la app y seguimos: te presento a tus compañeros.",
  "obSinIdentidad": "Antes necesitas una identidad. Púlsala arriba: se genera en tu navegador y no sale de ahí.",
  "obFalloCodigo": "NO_DATA — no se pudo derivar el código:",
  "s1t": "¿Qué es PreceptorOS?",
  "s1p": "Tu IA en tu máquina, sin nube obligatoria. Memoria persistente que es tuya, y un Privacy Gateway que sanea el contexto antes de que salga hacia cualquier IA externa. Sin cuentas, sin telemetría.",
  "s1b": "Empezar",
  "s2t": "Tu privacidad, tu control",
  "s2p": "El filtro es el que tacha lo privado. Pega tu contexto y mira qué sale antes de dárselo a nadie: ocurre en tu navegador, sin instalar nada, y te dice también dónde NO llega.",
  "s2b": "Probar el filtro ahora",
  "s3t": "Descarga la app",
  "s3p": "La web es el escaparate. La app es el taller: es donde el compañero que elijas trabaja con tus ficheros de verdad, sin que salgan de tu máquina.",
  "s3and": "Android · por Termux", "s3pc": "Linux o macOS · install.sh", "s3win": "Windows · install.ps1",
  "s3aviso": "NO_DATA — Android va hoy por Termux, con la guía de esta web; el APK está declarado como futuro y no existe todavía. Los instaladores de escritorio apuntan a su dirección definitiva en GitHub Releases y darán 404 hasta que se publique la primera versión. Windows y macOS NO están probados en este rack: no hay ninguna máquina de esos sistemas aquí.",
  "s4t": "Tu código de vinculación",
  "s4p": "Tu identidad se genera en el navegador y la clave privada no sale de él. Este código de vinculación se deriva de tu clave pública: es siempre el mismo para ti, y no lleva ningún secreto dentro.",
  "s4b": "Generar mi código de vinculación",
  "s4aviso": "Este código te IDENTIFICA, no te autentica: cualquiera que conozca tu clave pública puede calcularlo. Vincular de verdad exigirá además una firma, y eso llega con el backend.",
  "pieVolver": "← Volver a la portada", "piePlay": "Probador", "pieInst": "Guía de instalación",
 },
 "en": {
  "lang": "en", "titulo": "Start here · PreceptorOS",
  "desc": "The Installer walks you through it: get the app running and pick the companion that fits what you want to do.",
  "marca": "Start here", "volver": "Home",
  "obSaluda": "I'm the Installer. I'll stay with you until the app is running and you've chosen your companion. Tell me which way you'd like to go.",
  "obAtajo": "Straight to it, then. Scroll down: the three downloads are there.",
  "obLargo": "Good. Let me show you first what stays on your machine and what doesn't.",
  "obQue": "PreceptorOS is the customs house between your data and cloud AIs.",
  "obPriv": "This isn't a promise: it's a filter you can try right now.",
  "obDesc": "Pick your system. The app is the workshop; I come with you inside.",
  "obConec": "This pairing code links your web identity to the app. It's yours and only yours.",
  "obVinculado": "There it is. Open it in the app and we carry on: I'll introduce your companions.",
  "obSinIdentidad": "You need an identity first. Tap it above: it's generated in your browser and never leaves it.",
  "obFalloCodigo": "NO_DATA — the code could not be derived:",
  "s1t": "What is PreceptorOS?",
  "s1p": "Your AI on your machine, no cloud required. Persistent memory that belongs to you, and a Privacy Gateway that sanitises context before it reaches any external AI. No accounts, no telemetry.",
  "s1b": "Get started",
  "s2t": "Your privacy, your control",
  "s2p": "The filter is the one that crosses out what is private. Paste your context and see what comes out before you hand it to anyone: it happens in your browser, nothing to install, and it also tells you where it does NOT reach.",
  "s2b": "Try the filter now",
  "s3t": "Download the app",
  "s3p": "The web is the shop window. The app is the workshop: that's where the companion you choose works on your real files, without them leaving your machine.",
  "s3and": "Android · via Termux", "s3pc": "Linux or macOS · install.sh", "s3win": "Windows · install.ps1",
  "s3aviso": "NO_DATA — Android runs through Termux today, following this site's guide; the APK is declared future work and does not exist yet. The desktop installers point at their final address on GitHub Releases and will return 404 until the first version ships. Windows and macOS are NOT tested on this rack: there is no machine of either system here.",
  "s4t": "Your pairing code",
  "s4p": "Your identity is generated in the browser and the private key never leaves it. This pairing code is derived from your public key: always the same for you, and it carries no secret inside.",
  "s4b": "Generate my pairing code",
  "s4aviso": "This code IDENTIFIES you, it does not authenticate you: anyone who knows your public key can compute it. Real linking will also require a signature, and that arrives with the backend.",
  "pieVolver": "← Back to home", "piePlay": "Playground", "pieInst": "Install guide",
 },
 "fr": {
  "lang": "fr", "titulo": "Commence ici · PreceptorOS",
  "desc": "L'Installateur t'accompagne : installe l'app et choisis le compagnon qui correspond à ce que tu veux faire.",
  "marca": "Commence ici", "volver": "Accueil",
  "obSaluda": "Je suis l'Installateur. Je reste avec toi jusqu'à ce que l'app tourne et que tu aies choisi ton compagnon. Dis-moi par où tu veux aller.",
  "obAtajo": "Droit au but, alors. Descends : les trois téléchargements sont là.",
  "obLargo": "Bien. Je te montre d'abord ce qui reste sur ta machine et ce qui n'y reste pas.",
  "obQue": "PreceptorOS est la douane entre tes données et les IA du nuage.",
  "obPriv": "Ce n'est pas une promesse : c'est un filtre que tu peux essayer tout de suite.",
  "obDesc": "Choisis ton système. L'app est l'atelier ; je viens avec toi à l'intérieur.",
  "obConec": "Ce code de liaison relie ton identité web à l'app. Il est à toi et à toi seul.",
  "obVinculado": "Le voilà. Ouvre-le dans l'app et on continue : je te présente tes compagnons.",
  "obSinIdentidad": "Il te faut d'abord une identité. Appuie ci-dessus : elle est générée dans ton navigateur et n'en sort jamais.",
  "obFalloCodigo": "NO_DATA — le code n'a pas pu être dérivé :",
  "s1t": "Qu'est-ce que PreceptorOS ?",
  "s1p": "Ton IA sur ta machine, sans nuage obligatoire. Une mémoire persistante qui t'appartient, et un Privacy Gateway qui assainit le contexte avant qu'il ne parte vers une IA externe. Sans comptes, sans télémétrie.",
  "s1b": "Commencer",
  "s2t": "Ta vie privée, ton contrôle",
  "s2p": "Le filtre est celui qui raye ce qui est privé. Colle ton contexte et vois ce qui sort avant de le donner à qui que ce soit : tout se passe dans ton navigateur, rien à installer, et il te dit aussi où il N'ARRIVE PAS.",
  "s2b": "Essayer le filtre",
  "s3t": "Télécharge l'app",
  "s3p": "Le web est la vitrine. L'app est l'atelier : c'est là que le compagnon que tu choisis travaille sur tes vrais fichiers, sans qu'ils quittent ta machine.",
  "s3and": "Android · via Termux", "s3pc": "Linux ou macOS · install.sh", "s3win": "Windows · install.ps1",
  "s3aviso": "NO_DATA — Android passe aujourd'hui par Termux, avec le guide de ce site ; l'APK est déclaré comme travail futur et n'existe pas encore. Les installateurs de bureau pointent vers leur adresse définitive sur GitHub Releases et renverront 404 jusqu'à la première version. Windows et macOS NE sont PAS testés sur ce rack : aucune machine de ces systèmes n'est ici.",
  "s4t": "Ton code de liaison",
  "s4p": "Ton identité est générée dans le navigateur et la clé privée n'en sort jamais. Ce code de liaison dérive de ta clé publique : toujours le même pour toi, et il ne contient aucun secret.",
  "s4b": "Générer mon code de liaison",
  "s4aviso": "Ce code t'IDENTIFIE, il ne t'authentifie pas : quiconque connaît ta clé publique peut le calculer. Un vrai lien exigera aussi une signature, et cela arrive avec le backend.",
  "pieVolver": "← Retour à l'accueil", "piePlay": "Testeur", "pieInst": "Guide d'installation",
 },
}

# Las claves que el JS necesita. Si falta una en cualquier idioma, se para: una
# clave ausente deja una cadena vacia en la interfaz de ese idioma y solo lo ve
# quien hable ese idioma -- es decir, nadie de los que revisan.
CLAVES_JS = ("obSaluda obAtajo obLargo obQue obPriv obDesc obConec obVinculado "
             "obSinIdentidad obFalloCodigo idEntrar idHola idClave idPublica "
             "idFallo idAviso").split()

# Las de identidad las aporta auth.js y son iguales en las tres portadas: se
# reutilizan de ahi en vez de reescribirlas, para que no haya dos verdades.
IDENT = {
 "es": {"idEntrar": "Crear identidad", "idHola": "Hola,", "idClave": "Ver mi huella",
        "idPublica": "Clave pública:", "idFallo": "NO_DATA — no se pudo crear la identidad:",
        "idAviso": "Se genera una clave en tu navegador. No se puede exportar ni copiar a otro aparato: si borras los datos del sitio, esta identidad se pierde."},
 "en": {"idEntrar": "Create identity", "idHola": "Hello,", "idClave": "Show my fingerprint",
        "idPublica": "Public key:", "idFallo": "NO_DATA — the identity could not be created:",
        "idAviso": "A key is generated in your browser. It cannot be exported or copied to another device: if you clear site data, this identity is lost."},
 "fr": {"idEntrar": "Créer une identité", "idHola": "Bonjour,", "idClave": "Voir mon empreinte",
        "idPublica": "Clé publique :", "idFallo": "NO_DATA — l'identité n'a pas pu être créée :",
        "idAviso": "Une clé est générée dans ton navigateur. Elle ne peut être ni exportée ni copiée : si tu effaces les données du site, cette identité est perdue."},
}


def pagina(idi):
    t = dict(COPY[idi]); t.update(IDENT[idi])
    faltan = [k for k in CLAVES_JS if not t.get(k)]
    if faltan:
        raise SystemExit(f"🔴 {idi}: faltan claves {faltan}. No se genera nada.")
    i18n = json.dumps(t, ensure_ascii=False, indent=1, sort_keys=True)
    d = {k: v for k, v in DESCARGAS}
    return f"""<!doctype html>
<html lang="{t['lang']}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{t['titulo']}</title>
<link rel="icon" type="image/svg+xml" href="/assets/favicon.svg">
<meta name="description" content="{t['desc']}">
<link rel="stylesheet" href="/assets/base.css">
<link rel="stylesheet" href="/assets/movil.css">
<link rel="stylesheet" href="/assets/canon.css">
<link rel="stylesheet" href="/assets/onboarding.css">
</head>
<body>
<main>

<header>
  <div class="seal" role="img" aria-label="PreceptorOS"></div>
  <div class="marca">
    <h1>{t['marca']}</h1>
    <p><a href="./">{t['volver']}</a></p>
  </div>
  <div id="identity" class="fila identity"></div>
</header>

<p class="ob-voz" id="ob-voz" role="status" aria-live="polite">…</p>

<div class="ob-caminos">
  <button type="button" id="ob-atajo">{t['s3t']} →</button>
  <button type="button" id="ob-largo" class="ob-secundario">{t['s1b']}</button>
</div>

<section class="ob-paso" id="ob-que" data-dice="obQue">
  <h2><span class="ob-num">1</span>{t['s1t']}</h2>
  <p>{t['s1p']}</p>
  <button type="button" data-ir="privacidad">{t['s1b']}</button>
</section>

<section class="ob-paso" id="ob-privacidad" data-dice="obPriv">
  <h2><span class="ob-num">2</span>{t['s2t']}</h2>
  <p>{t['s2p']}</p>
  <p><a class="boton" href="./playground.html">{t['s2b']}</a></p>
</section>

<section class="ob-paso" id="ob-descarga" data-dice="obDesc">
  <h2><span class="ob-num">3</span>{t['s3t']}</h2>
  <p>{t['s3p']}</p>
  <div class="ob-descargas">
    <a class="boton" href="{d['android']}">{t['s3and']}</a>
    <a class="boton" href="{d['pc']}">{t['s3pc']}</a>
    <a class="boton" href="{d['win']}">{t['s3win']}</a>
  </div>
  <p class="ob-aviso nodata">{t['s3aviso']}</p>
  <p class="tenue"><a href="./instalar.html">{t['pieInst']} →</a></p>
</section>

<section class="ob-paso" id="ob-conecta" data-dice="obConec">
  <h2><span class="ob-num">4</span>{t['s4t']}</h2>
  <p>{t['s4p']}</p>
  <button type="button" id="ob-vincular">{t['s4b']}</button>
  <p class="ob-codigo" id="ob-codigo">—</p>
  <p class="ob-aviso nodata">{t['s4aviso']}</p>
</section>

<footer class="honest-footer">
  <p><a href="./">{t['pieVolver']}</a> · <a href="./playground.html">{t['piePlay']}</a>
     · <a href="./instalar.html">{t['pieInst']}</a></p>
</footer>

<script type="application/json" id="i18n">{i18n}</script>
<script src="/assets/auth.js"></script>
<script src="/assets/onboarding.js"></script>

</main>
</body>
</html>
"""


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--si", action="store_true", help="escribe (por defecto: dry-run)")
    a = ap.parse_args(argv)
    TOPE, malos = 10 * 1024, []
    for idi in COPY:
        destino = WEB / idi / "onboarding.html"
        html = pagina(idi)
        n = len(html.encode("utf-8"))
        if n >= TOPE:
            malos.append(f"{idi}: {n} B")
        print(f"  {'✓' if a.si else '·'} {destino.relative_to(WEB)} · {n} B")
        if a.si:
            destino.parent.mkdir(parents=True, exist_ok=True)
            destino.write_text(html, encoding="utf-8")
    if malos:
        print("🔴 pasan de 10 KB: " + ", ".join(malos), file=sys.stderr)
        return 1
    if not a.si:
        print("  (dry-run · --si para escribir)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
