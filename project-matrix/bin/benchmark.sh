#!/usr/bin/env bash
set -euo pipefail

TARGET_URL="${1:-https://api.github.com}"
REPORT_FILE="reports/diagnostic_$(date +%Y%m%d_%H%M%S).log"

echo "=== START DIAGNOSE: ${TARGET_URL} ===" | tee "${REPORT_FILE}"
curl -s -w "HTTP_CODE: %{http_code}\nTIME_TOTAL: %{time_total}s\n" -o /dev/null "${TARGET_URL}" | tee -a "${REPORT_FILE}"
echo "=== STATUS: ERFOLGREICH ===" | tee -a "${REPORT_FILE}"
