#!/usr/bin/env bash
set -euo pipefail

VENDOR="${1:-Unbekannter_Hersteller}"
COMPONENT="${2:-System}"
LOG_TARGET="${3:-https://api.github.com}"

REPORT_MD="reports/ISSUE_${VENDOR^^}_$(date +%Y%m%d_%H%M%S).md"

cat << EOREPORT > "${REPORT_MD}"
# Fehler- und Diagnosebericht: ${VENDOR} - ${COMPONENT}

- **Datum:** $(date -u +"%Y-%m-%d %H:%M:%S UTC")
- **Zielsystem:** ${LOG_TARGET}
- **Status:** Reproduziert via Bash-Framework

## Diagnosedaten
\`\`\`
$(curl -s -w "HTTP_STATUS: %{http_code}\nDNS_TIME: %{time_namelookup}s\nCONNECT_TIME: %{time_connect}s\nTOTAL_TIME: %{time_total}s\n" -o /dev/null "${LOG_TARGET}")
\`\`\`

## Empfohlene Optimierung
- Automatisiert generiert durch das Projekt-Pruefframework.
EOREPORT

echo "[ERFOLG] Bericht erstellt: ${REPORT_MD}"
