#!/bin/bash
while true; do
  STATUS=$(curl -s http://127.0.0.1:6673/v4/mission_control/status | grep -o 'ACTIVE')
  if [ "$STATUS" == "ACTIVE" ]; then
    echo "STATUS ACTIVE - HARDWARE ON"
    # HIER KOMMT DER BEFEHL ZUR GPIO-SCHALTUNG (Z.B. GPIOD)
    # gpio set 1 1
  else
    echo "STATUS INACTIVE - HARDWARE OFF"
    # gpio set 1 0
  fi
  sleep 5
done
