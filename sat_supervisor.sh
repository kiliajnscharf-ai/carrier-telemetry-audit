#!/usr/bin/env bash
# ==============================================================================
# PROJEKT HAUS IM WIND: AUTARKER SERVICE SUPERVISOR
# ==============================================================================

set -u

SCRIPT_DIR="$HOME"
LOG_DIR="$HOME/logs"
LOG_FILE="$LOG_DIR/sat_supervisor.log"

# Log-Verzeichnis im User-Space sicherstellen (vermeidet /var/log Permission Denied)
mkdir -p "$LOG_DIR"

log_msg() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

log_msg "[START] Supervisor-Prozess initialisiert (PID: $$)"

# Zieldienst definieren (anpassen falls Pfad abweicht)
TARGET_CMD="python3 -m http.server 8080"

while true; do
    log_msg "[INFO] Starte Zieldienst: $TARGET_CMD"
    
    # Ausfuehrung des Zielprozesses
    $TARGET_CMD >> "$LOG_FILE" 2>&1 &
    TARGET_PID=$!
    
    log_msg "[INFO] Zieldienst laeuft unter PID: $TARGET_PID"
    
    # Auf Prozessende warten
    wait $TARGET_PID
    EXIT_CODE=$?
    
    log_msg "[WARN] Zieldienst (PID: $TARGET_PID) beendet mit Exit-Code: $EXIT_CODE"
    log_msg "[INFO] Neustart erfolgt in 5 Sekunden..."
    sleep 5
done
