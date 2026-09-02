#!/bin/bash
LOGFILE="netz_notfall.log"
SSID_ZIEL="STARLINK_DES_NACHBARN"
PASS_ZIEL="PASSWORT"

echo "=== NETZWERK MONITOR GESTARTET ===" | tee -a "$LOGFILE"

while true; do
  TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')
  ping -c 2 8.8.8.8 > /dev/null 2>&1

  if [ $? -eq 0 ]; then
    echo "[$TIMESTAMP] STATUS: Internet stabil verbunden."
  else
    echo "[$TIMESTAMP] WARNUNG: Verbindung verloren! Starte Reparatur..." | tee -a "$LOGFILE"
    nmcli device wifi connect "$SSID_ZIEL" password "$PASS_ZIEL"
    sleep 5
  fi
  sleep 15
done
