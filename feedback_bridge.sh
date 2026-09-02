#!/bin/bash
# TITANSTREAM FEEDBACK BRIDGE V1.1 (MIT FEHLERPRÜFUNG)

LOG_FILE="/var/log/titanstream_debug.log"
TARGET_API="https://feedback.google.com/api/v1/submit"

if [ -f "$LOG_FILE" ]; then
    echo "STARTE ÜBERMITTLUNG AN $TARGET_API..."
    
    # PRÜFUNG DES CURL-STATUS
    if curl -X POST -d @$LOG_FILE $TARGET_API; then
        echo "ÜBERMITTLUNG ERFOLGREICH."
    else
        echo "FEHLER: ÜBERMITTLUNG GESCHEITERT. PRÜFEN SIE DIE INTERNETVERBINDUNG."
    fi
else
    echo "FEHLER: LOG-DATEI NICHT GEFUNDEN."
fi
