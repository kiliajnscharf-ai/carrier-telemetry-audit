#!/bin/bash
while true; do
  ping -c 1 8.8.8.8 > /dev/null 2>&1
  if [ $? -eq 0 ]; then
    echo "Internet verbunden"
  else
    echo "Kein Internet - Versuche Verbindung zum Starlink-Netzwerk..."
    nmcli device wifi connect "SSID_DES_NACHBARN" password "PASSWORT"
  fi
  sleep 10
done
