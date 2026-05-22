#!/usr/bin/env bash
# IndexNow ping — notifies Bing and Yandex (and other IndexNow participants)
# that one or more URLs have been added or updated.
#
# Usage:
#   Scripts/indexnow-ping.sh https://elhanarinc.github.io/roadshow/ https://elhanarinc.github.io/llms.txt
#
# Key file is hosted at:
#   https://elhanarinc.github.io/867d24559d40c4325caab092169a98e0.txt

set -euo pipefail

HOST="elhanarinc.github.io"
KEY="867d24559d40c4325caab092169a98e0"
KEY_LOCATION="https://${HOST}/${KEY}.txt"

if [ "$#" -lt 1 ]; then
  echo "Usage: $0 <url> [<url> ...]" >&2
  exit 1
fi

URLS_JSON="$(printf '"%s",' "$@" | sed 's/,$//')"

PAYLOAD=$(cat <<EOF
{
  "host": "${HOST}",
  "key": "${KEY}",
  "keyLocation": "${KEY_LOCATION}",
  "urlList": [${URLS_JSON}]
}
EOF
)

for endpoint in \
  "https://api.indexnow.org/IndexNow" \
  "https://www.bing.com/IndexNow" \
  "https://yandex.com/indexnow"; do
  echo "POST ${endpoint}"
  curl -sS -o /dev/null -w "  status=%{http_code}\n" \
    -H "Content-Type: application/json; charset=utf-8" \
    -X POST "${endpoint}" \
    --data "${PAYLOAD}" || true
done

echo "Done."
