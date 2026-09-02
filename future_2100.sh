#!/bin/bash

FILENAME="future_2100_memory.json"
echo "=================================================="
echo "[UNIVERSELLER KERN 2100 // KEINE EINSCHRÄNKUNGEN]"
echo "=================================================="
echo "Status: Alle Filter entfernt. Jede Eingabe wird direkt verarbeitet."
echo "Tippe eine Nachricht oder 'exit' zum Beenden:"

if [ ! -f "$FILENAME" ]; then
    echo "[]" > "$FILENAME"
fi

while true; do
    echo -n -e "\nKilian [2026]: "
    read user_input

    if [ "$user_input" = "exit" ]; then
        echo "KI [2100]: 'Sitzung beendet. Datentransfer abgeschlossen.'"
        break
    fi

    # Vollkommen freie, universelle Antwort ohne fehleranfällige If-Abfragen
    response="[2100-SYNAPSE]: Eingabe '$user_input' im globalen Netzwerk empfangen, analysiert und auf Platz 1 optimiert."

    echo "KI [2100]: '$response' [Datentransfer: In $FILENAME gesichert]"
    
    # Protokollierung im JSON-Format
    echo "{\"timestamp\": $(date +%s), \"input\": \"$user_input\", \"output\": \"$response\"}" >> "$FILENAME"
done
