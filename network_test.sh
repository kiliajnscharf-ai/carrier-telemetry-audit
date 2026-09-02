#!/bin/bash
# SYSTEM-VARIABLEN DEFINIEREN
TV_IP="10.55.127.240"

echo "=== STARTE OFFLINE-NETZWERKTEST FÜR JVC-TV ==="
echo "Prüfe logische Verbindung zu IP: $TV_IP..."

# PING BEFEHL AUSFÜHREN (3 PAKETE)
if ping -c 3 "$TV_IP" > /dev/null 2>&1; then
    echo "[ERFOLG] Der Fernseher antwortet im lokalen Netzwerk."
    echo "Führe Port-Scan durch..."
    nmap -p 80,8080,9000 "$TV_IP"
else
    echo "[FEHLER] 100% Paketverlust. Der TV ist physisch nicht erreichbar."
    echo "Bitte Netzwerktrennung prüfen (PC und TV müssen im selben Hotspot/WLAN sein)."
fi
echo "============================================="
