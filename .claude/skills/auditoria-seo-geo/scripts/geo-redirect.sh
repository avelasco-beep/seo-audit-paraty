#!/usr/bin/env bash
# Detecta redirección automática por idioma del navegador (Accept-Language).
# No puede cambiar la IP, así que la parte de geolocalización por país se
# comprueba a mano; esto cubre el vector más común: redirección por idioma.
#
# Uso:  bash geo-redirect.sh https://www.ejemplo.com/
#
# Qué mira:
#  1) La home con distintos Accept-Language: ¿responde 200 igual, o 3xx a /es/, /en/, /de/…?
#  2) Un bot (Googlebot es-US) frente a un navegador es-ES: ¿reciben distinta URL final?
#  Si la URL final cambia según el idioma pedido, hay redirección automática.

URL="${1:?uso: bash geo-redirect.sh <url>}"
UA_BROWSER="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4 Safari/605.1.15"
UA_GBOT="Mozilla/5.0 (Linux; Android 6.0.1; Nexus 5X) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126 Mobile Safari/537.36 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)"

probe () { # $1=etiqueta  $2=accept-language  $3=user-agent
  local code loc
  read -r code loc < <(curl -sk -m 20 -o /dev/null \
    -A "$3" -H "Accept-Language: $2" \
    -w "%{http_code} %{redirect_url}" "$URL")
  printf "  %-22s -> %s%s\n" "$1" "$code" "${loc:+  → $loc}"
}

echo "URL: $URL"
echo "== ¿la home redirige según el idioma pedido? =="
probe "sin idioma"        ""              "$UA_BROWSER"
probe "en-US"             "en-US,en;q=0.9" "$UA_BROWSER"
probe "es-ES"             "es-ES,es;q=0.9" "$UA_BROWSER"
probe "de-DE"             "de-DE,de;q=0.9" "$UA_BROWSER"
probe "fr-FR"             "fr-FR,fr;q=0.9" "$UA_BROWSER"
probe "ja-JP (no soportado)" "ja-JP,ja;q=0.9" "$UA_BROWSER"
echo "== bot vs navegador (mismo idioma es) =="
probe "Googlebot es"      "es-ES,es;q=0.9" "$UA_GBOT"
probe "navegador es"      "es-ES,es;q=0.9" "$UA_BROWSER"
echo
echo "Lectura: si la 'URL final' cambia entre idiomas, hay redirección automática por idioma"
echo "(mala para rastreo: Googlebot llega en su mayoría como en-US y no verá los otros idiomas)."
echo "La geolocalización por país (IP) hay que confirmarla a mano desde una VPN o con la ficha de Google."
