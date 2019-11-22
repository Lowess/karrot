#!/usr/bin/env bash

if [ $# -eq 0 ]; then
    echo "[$(date)] - Note You can provide arguments as: ./notify <JSON_FILE> <INTERVAL>"
fi

HOST=${1:-"localhost:5000"}
FILE=${2:-"$(dirname $0)/../samples/event.json"}
INTERVAL=${3:-"5"}

echo "[$(date)] - Sending notifications every ${INTERVAL} seconds with JSON payload from ${FILE}"

LAG_SIMULATE=5

while true; do
  LAG_SIMULATE="$((LAG_SIMULATE+5))"

  cat "${FILE}" | jq ".Event.Result.totallag = ${LAG_SIMULATE}"

  echo "[$(date)] - POST on ${HOST}/burrow"
  curl -XPOST \
       -H "Content-Type: application/json" \
       --data "$(cat ${FILE} | jq ".Event.Result.totallag = ${LAG_SIMULATE}")" \
      ${HOST}/burrow
  sleep "${INTERVAL}"
done
