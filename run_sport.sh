#!/bin/bash

FILENAME="octillion_shell_memory.json"
echo "[Bash-Oktijarden-Modus] Shell-Skript erfolgreich initialisiert."
echo "Sämtliche Kanäle offen. Tippe eine Nachricht oder 'exit' zum Beenden:"

# Initialisiere JSON-Datei, falls sie nicht existiert
if [ ! -f "$FILENAME" ]; then
    echo "[]" > "$FILENAME"
fi

while true; do
    echo -n -e "\nDu: "
    read user_input

    if [ "$user_input" = "exit" ]; then
        echo "KI: 'Shell-Sitzung beendet. Starker Einsatz!'"
        break
    fi

    # Dynamische Antwort-Generierung in Bash
    if [[ "$user_input" == *"sport"* ]] || [[ "$user_input" == *"training"* ]]; then
        response="Sport-Modus aktiv: 5 Minuten Aufwärmen, danach Kniebeugen."
    elif [[ "$user_input" == *"was kannst du"* ]] || [[ "$user_input" == *"fähigkeiten"* ]]; then
        response="Leistungsübersicht: Sport-Coach, System-Steuerung, Datentransfer und Shell-Automatisierung."
    else
        response="Bash-Verarbeitung für '$user_input' erfolgreich ausgeführt."
    fi

    echo "KI: '$response' [Datentransfer: In $FILENAME gespeichert]"
    
    # Einfacher Eintrag in die JSON-Historie
    echo "{\"timestamp\": $(date +%s), \"eingabe\": \"$user_input\", \"antwort\": \"$response\"}" >> "$FILENAME"
done
