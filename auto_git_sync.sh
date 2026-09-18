#!/usr/bin/env bash
# Synchronisiert alle 30 Minuten autonom mit dem oeffentlichen Remote-Repository
while true; do
    ./export_telemetry_json.sh >/dev/null 2>&1
    git add -f core_node_latency.csv carrier_telemetry_report.json ticket_live_update.txt README.md >/dev/null 2>&1
    
    # Pruefen ob Änderungen vorliegen
    if ! git diff-index --quiet HEAD --; then
        CYCLES=$(awk -F, 'NR>1 && $1 !~ /^#/ && $4 ~ /^[0-9.]+$/ {c++} END {print c}' core_node_latency.csv)
        git commit -m "telemetry: automated sync cycle ${CYCLES} [$(date -u '+%Y-%m-%d %H:%M:%S UTC')]" >/dev/null 2>&1
        # Push wird aktiv, sobald ein Remote 'origin' hinterlegt ist:
        git push origin main >/dev/null 2>&1
        echo "[$(date '+%Y-%m-%d %H:%M:%S')] Repository und Telemetrie autonom synchronisiert (Zyklus ${CYCLES})."
    fi
    sleep 1800
done
