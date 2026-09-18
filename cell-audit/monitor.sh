#!/usr/bin/env bash

TARGET="8.8.8.8"
URL="http://www.google.com"
DATA_FILE="data/network_pings.csv"

mkdir -p data

if [ ! -f "$DATA_FILE" ]; then
    echo "Timestamp,Target,Latency_ms,Packet_Loss_Percent,HTTP_Status" > "$DATA_FILE"
fi

while true; do
    TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
    
    # 3 Pings senden und sauber mit gawk auswerten
    PING_OUTPUT=$(ping -c 3 -W 2 "$TARGET" 2>&1)
    
    LOSS=$(echo "$PING_OUTPUT" | grep -oP '\d+(?=% packet loss)' || echo "100")
    AVG_LATENCY=$(echo "$PING_OUTPUT" | grep -oP '(?<=min/avg/max/mdev = )[0-9.]+' | cut -d'/' -f2)
    
    if [ -z "$AVG_LATENCY" ]; then
        AVG_LATENCY="0.000"
    fi
    
    # HTTP Check (5s Timeout)
    HTTP_STATUS=$(curl -o /dev/null -s -w "%{http_code}" --connect-timeout 5 "$URL")
    if [ -z "$HTTP_STATUS" ]; then
        HTTP_STATUS="000"
    fi
    
    echo "$TIMESTAMP,$TARGET,$AVG_LATENCY,$LOSS%,$HTTP_STATUS" >> "$DATA_FILE"
    
    sleep 60
done
