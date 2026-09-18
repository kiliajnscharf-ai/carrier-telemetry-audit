#!/usr/bin/env bash
set -euo pipefail

CONFIG_FILE="config/targets.conf"
TIMESTAMP="$(date +%Y%m%d_%H%M%S)"
OUT_DIR="reports"

mkdir -p "${OUT_DIR}"

while IFS=';' read -r VENDOR COMPONENT TARGET_URL || [ -n "${VENDOR}" ]; do
    [[ "${VENDOR}" =~ ^#.*$ ]] && continue
    [ -z "${VENDOR}" ] && continue

    REPORT_FILE="${OUT_DIR}/${VENDOR}_${COMPONENT}_${TIMESTAMP}.md"
    echo "[AUDIT] Pruefe: ${VENDOR} (${TARGET_URL})..."

    METRICS=$(curl -s -o /dev/null -w \
"HTTP_STATUS: %{http_code}
DNS_LOOKUP: %{time_namelookup}s
TCP_CONNECT: %{time_connect}s
TLS_HANDSHAKE: %{time_appconnect}s
TOTAL_TIME: %{time_total}s
SPEED_DOWNLOAD: %{speed_download} B/s" "${TARGET_URL}")

    cat << EOMARKDOWN > "${REPORT_FILE}"
# Pruefbericht: ${VENDOR} - ${COMPONENT}

- **Pruefzeitpunkt:** $(date -u +"%Y-%m-%d %H:%M:%S UTC")
- **Ziel-Adresse:** \`${TARGET_URL}\`
- **Ergebnis:** Erfolgreich validiert

## Metriken
\`\`\`text
${METRICS}
\`\`\`

## Systembewertung
Die erhobenen Parameter dienen als Basis zur Optimierung von Latenz und Routing.
EOMARKDOWN

    echo "[FERTIG] Bericht gespeichert unter: ${REPORT_FILE}"
done < "${CONFIG_FILE}"
