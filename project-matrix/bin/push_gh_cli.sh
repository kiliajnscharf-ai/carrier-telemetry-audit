#!/usr/bin/env bash
set -euo pipefail

REPORT_FILE="${1:-}"
TARGET_REPO="${2:-}" # Format: owner/repo

if [ -z "${REPORT_FILE}" ] || [ -z "${TARGET_REPO}" ]; then
    echo "Aufruf: $0 <REPORT_DATEI> <OWNER/REPO>"
    exit 1
fi

if [ ! -f "${REPORT_FILE}" ]; then
    echo "Fehler: Datei '${REPORT_FILE}' nicht gefunden."
    exit 1
fi

TITLE="$(head -n 1 "${REPORT_FILE}" | sed 's/^# //')"

echo "[INFO] Uebertrage Issue zu ${TARGET_REPO} via gh CLI..."
gh issue create \
    --repo "${TARGET_REPO}" \
    --title "${TITLE}" \
    --body-file "${REPORT_FILE}"

echo "[ERFOLG] Issue erfolgreich via GitHub CLI erstellt."
