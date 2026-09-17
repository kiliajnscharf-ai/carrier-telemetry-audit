#!/bin/bash

CSV_FILE="data/network_pings.csv"

# Header anlegen, falls Datei nicht existiert
if [ ! -f "$CSV_FILE" ]; then
    echo "Timestamp,Host,Latency_ms,Packet_Loss_Percent,HTTP_Status" > "$CSV_FILE"
fi

echo "Start der Netzwerk-Messung. Beenden mit STRG+C..."

while true; do
    TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
    TARGET="8.8.8.8"
    
    # Ping-Messung (3 Pings)
    PING_OUTPUT=$(ping -c 3 -W 2 "$TARGET" 2>&1)
    
    # Latenz und Packet Loss parsen
    PACKET_LOSS=$(echo "$PING_OUTPUT" | grep -oP '\d+(?=% packet loss)')
    LATENCY=$(echo "$PING_OUTPUT" | tail -1 | awk -F '/' '{print $5}')
    
    if [ -z "$LATENCY" ]; then
        LATENCY="TIMEOUT"
    fi
    
    # HTTP Check via curl
    HTTP_STATUS=$(curl -o /dev/null -s -w "%{http_code}\n" --max-time 5 https://www.google.com)
    if [ -z "$HTTP_STATUS" ]; then
        HTTP_STATUS="FAIL"
    fi
    
    # Zeile in CSV schreiben
    echo "${TIMESTAMP},${TARGET},${LATENCY},${PACKET_LOSS}%,${HTTP_STATUS}" >> "$CSV_FILE"
    echo "[${TIMESTAMP}] Ping: ${LATENCY} ms | Loss: ${PACKET_LOSS}% | HTTP: ${HTTP_STATUS}"
    
    sleep 60
done
