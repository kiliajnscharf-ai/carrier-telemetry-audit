#!/usr/bin/env bash
set -euo pipefail

REPORT_PATH="${1:-}"
REPO_OWNER="${2:-}"
REPO_NAME="${3:-}"
GH_TOKEN="${GITHUB_TOKEN:-}"

if [ -z "${REPORT_PATH}" ] || [ -z "${REPO_OWNER}" ] || [ -z "${REPO_NAME}" ]; then
    echo "Aufruf: GITHUB_TOKEN=xxx $0 <REPORT_DATEI> <OWNER> <REPO>"
    exit 1
fi

if [ -z "${GH_TOKEN}" ]; then
    echo "Fehler: Umgebungsvariable GITHUB_TOKEN ist nicht gesetzt."
    exit 1
fi

TITLE="$(head -n 1 "${REPORT_PATH}" | sed 's/^# //')"
BODY="$(cat "${REPORT_PATH}")"

# JSON Payload via Bash formatieren
JSON_PAYLOAD=$(jq -n --arg t "${TITLE}" --arg b "${BODY}" '{title: $t, body: $b}')

HTTP_STATUS=$(curl -s -o /dev/null -w "%{http_code}" \
    -X POST \
    -H "Authorization: token ${GH_TOKEN}" \
    -H "Accept: application/vnd.github.v3+json" \
    https://api.github.com/repos/${REPO_OWNER}/${REPO_NAME}/issues \
    -d "${JSON_PAYLOAD}")

if [ "${HTTP_STATUS}" -eq 201 ]; then
    echo "[ERFOLG] Issue erfolgreich auf GitHub erstellt (HTTP 201)."
else
    echo "[FEHLER] API-Aufruf fehlgeschlagen mit HTTP-Status: ${HTTP_STATUS}"
    exit 1
fi
