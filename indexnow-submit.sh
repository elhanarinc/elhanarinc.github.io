#!/usr/bin/env bash
# Submit URLs to IndexNow (Bing, Yandex, Naver, etc.)
# Usage: ./indexnow-submit.sh https://elhanarinc.github.io/hexora/oracle.html https://elhanarinc.github.io/hexora/tr/fal.html
set -euo pipefail

KEY="867d24559d40c4325caab092169a98e0"
HOST="elhanarinc.github.io"
KEY_LOCATION="https://${HOST}/${KEY}.txt"

if [ "$#" -eq 0 ]; then
  echo "Usage: $0 <url1> [url2 ...]" >&2
  exit 1
fi

URL_LIST=$(printf '"%s",' "$@" | sed 's/,$//')

PAYLOAD=$(cat <<EOF
{"host":"${HOST}","key":"${KEY}","keyLocation":"${KEY_LOCATION}","urlList":[${URL_LIST}]}
EOF
)

echo "Submitting $# URLs to IndexNow..."
curl -fsSL -X POST "https://api.indexnow.org/indexnow" \
  -H "Content-Type: application/json; charset=utf-8" \
  -d "$PAYLOAD" -o /dev/null -w "HTTP %{http_code}\n"
