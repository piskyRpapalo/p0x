#!/usr/bin/env bash
# Prepara una copia publicable del Nexo, y se NIEGA si encuentra una fuga.
#
# Por que audita en vez de reescribir: un saneador que sustituye deja el trabajo
# hecho a medias cuando falla a medias, y lo peor de un `sed` sobre codigo es
# que casi siempre funciona -- hasta el dia que rompe una linea y nadie mira el
# diff porque "el script lo arreglo". Aqui no se arregla nada: se comprueba, y
# si hay algo se para con el fichero y la linea en la mano.
#
# La copia sale de `git archive HEAD`, no de `cp -r`. Es la unica forma de que
# lo no versionado --`.env`, `estado/`, restos de una prueba, un fichero que
# alguien dejo ahi hace tres semanas-- no pueda colarse: si no esta en el
# commit, no existe para este script.
#
# Uso:  bin/sanitize_for_public.sh [destino]
# Salida 0 solo si la copia esta limpia.

set -uo pipefail
RAIZ="$(cd "$(dirname "$0")/.." && pwd)"
ORIGEN="hexelion-nexo"
DESTINO="${1:-${TMPDIR:-/tmp}/hexelion-nexo-publico}"

rojo=$'\033[31m'; verde=$'\033[32m'; ambar=$'\033[33m'; gris=$'\033[90m'; fin=$'\033[0m'
[ -t 1 ] || { rojo=""; verde=""; ambar=""; gris=""; fin=""; }

echo "── SANEAMIENTO · EL NEXO ───────────────────────────────────────"
cd "$RAIZ" || exit 2

if ! git diff --quiet -- "$ORIGEN" || ! git diff --cached --quiet -- "$ORIGEN"; then
  echo "${ambar}AVISO · hay cambios sin commitear en ${ORIGEN}.${fin}"
  echo "        La copia sale de HEAD, asi que esos cambios NO viajan."
  echo
fi

rm -rf "$DESTINO"
mkdir -p "$DESTINO"
git archive HEAD -- "$ORIGEN" | tar -x -C "$DESTINO" --strip-components=1 || exit 2
echo "  copia en ${DESTINO}"
echo "  ${gris}$(find "$DESTINO" -type f | wc -l) ficheros · solo lo que esta en HEAD${fin}"
echo

# --- lo que no puede viajar --------------------------------------------------
# Cada patron con el nombre de lo que busca, para que un hallazgo se lea sin
# tener que descifrar la expresion.
declare -a NOMBRE PATRON
add(){ NOMBRE+=("$1"); PATRON+=("$2"); }

add "direccion del tailnet"   '\b100\.([0-9]{1,3}\.){2}[0-9]{1,3}\b'
add "direccion privada"       '\b(192\.168|10)\.([0-9]{1,3}\.)?[0-9]{1,3}\.[0-9]{1,3}\b'
add "direccion privada 172"   '\b172\.(1[6-9]|2[0-9]|3[01])\.[0-9]{1,3}\.[0-9]{1,3}\b'
add "ruta de casa"            '/(home|Users)/[a-z0-9_-]+'
add "ruta de montaje"         '/(mnt|srv|opt|media)/[a-z0-9_-]+'
add "dominio del tailnet"     '\btail[0-9a-f]{6,}\.ts\.net\b'
add "clave privada"           'BEGIN [A-Z ]*PRIVATE KEY'
add "clave publica ssh"       '\bssh-(rsa|ed25519|dss) [A-Za-z0-9+/]{20,}'
add "credencial"              '\b(password|passwd|secret|api[_-]?key|bearer)\b[[:space:]]*[:=][[:space:]]*[^[:space:]]'
add "token con prefijo"       '\b(sk|ghp|gho|xox[abp])-[A-Za-z0-9_]{16,}'
add "fichero de entorno"      '^\.env$'

FALLOS=0
for i in "${!NOMBRE[@]}"; do
  nombre="${NOMBRE[$i]}"; patron="${PATRON[$i]}"
  if [ "$nombre" = "fichero de entorno" ]; then
    hallado="$(cd "$DESTINO" && find . -name ".env" -type f 2>/dev/null)"
  else
    hallado="$(grep -rInE --binary-files=without-match "$patron" "$DESTINO" 2>/dev/null \
               | sed "s#^${DESTINO}/##")"
  fi
  if [ -n "$hallado" ]; then
    FALLOS=$((FALLOS + 1))
    echo "  ${rojo}FUGA${fin}  ${nombre}"
    printf '%s\n' "$hallado" | head -8 | sed 's/^/          /'
  else
    echo "  ${verde}ok${fin}    ${nombre}"
  fi
done

# --- lo que tiene que estar --------------------------------------------------
echo
for necesario in ".gitignore" ".env.example" "rack.conf.example" "LEEME.md"; do
  if [ -f "$DESTINO/$necesario" ]; then
    echo "  ${verde}ok${fin}    ${necesario} presente"
  else
    FALLOS=$((FALLOS + 1))
    echo "  ${rojo}FALTA${fin} ${necesario}"
  fi
done
if grep -qx '\.env' "$DESTINO/.gitignore" 2>/dev/null; then
  echo "  ${verde}ok${fin}    .env esta en .gitignore"
else
  FALLOS=$((FALLOS + 1))
  echo "  ${rojo}FALLO${fin} .env NO esta en .gitignore"
fi

# --- la tanda, en la copia ---------------------------------------------------
# Una copia que no pasa sus propias pruebas no esta lista para que la lea nadie.
echo
if (cd "$DESTINO" && bash pruebas >/dev/null 2>&1); then
  echo "  ${verde}ok${fin}    la copia pasa su propia tanda"
else
  FALLOS=$((FALLOS + 1))
  echo "  ${rojo}FALLO${fin} la copia NO pasa su tanda"
  echo "          (cd $DESTINO && bash pruebas)"
fi

echo
if [ "$FALLOS" = "0" ]; then
  echo "${verde}LIMPIO · ${DESTINO}${fin}"
  echo "${gris}El siguiente paso lo da una persona: git init, remoto y push.${fin}"
  exit 0
fi
echo "${rojo}SUCIO · ${FALLOS} motivo(s). No se publica.${fin}"
exit 1
