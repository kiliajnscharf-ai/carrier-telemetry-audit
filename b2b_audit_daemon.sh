#!/usr/bin/env bash
set -e

INTERVAL_SEC=3600
LOG_FILE="$HOME/b2b_audit_daemon.log"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "================================================================================"
echo "PROJEKT HAUS IM WIND: B2B-AUDIT-HINTERGRUND-DAEMON (PHASE 72)"
echo "Prüfintervall:     ${INTERVAL_SEC} Sekunden (1 Stunde)"
echo "Logdatei:          $LOG_FILE"
echo "Arbeitsverzeichnis:$SCRIPT_DIR"
echo "================================================================================"

cd "$SCRIPT_DIR"

if [ "$1" == "--once" ]; then
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] Manuell initiierter Einzellauf gestartet." >> "$LOG_FILE"
    ./run_b2b_master_audit.sh >> "$LOG_FILE" 2>&1
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] Einzellauf mit Exit-Code $? beendet." >> "$LOG_FILE"
    echo "[X] Einzellauf erfolgreich protokolliert in $LOG_FILE"
    exit 0
fi

echo "[$(date '+%Y-%m-%d %H:%M:%S')] B2B-Audit-Daemon als Hintergrunddienst gestartet." >> "$LOG_FILE"

while true; do
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] Starte zyklischen B2B-Master-Audit..." >> "$LOG_FILE"
    if ./run_b2b_master_audit.sh >> "$LOG_FILE" 2>&1; then
        echo "[$(date '+%Y-%m-%d %H:%M:%S')] Zyklus erfolgreich abgeschlossen (OK)." >> "$LOG_FILE"
    else
        echo "[$(date '+%Y-%m-%d %H:%M:%S')] FEHLER im Zyklus festgestellt." >> "$LOG_FILE"
    fi
    sleep "$INTERVAL_SEC"
done
