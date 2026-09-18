#!/usr/bin/env bash
TARGET="145.254.2.19"
CSV_FILE="core_node_latency.csv"

while true; do
    TIMESTAMP=$(date +"%Y-%m-%d %H:%M:%S")
    OUTPUT=$(ping -c 5 -i 0.2 -W 2 "$TARGET" 2>/dev/null)
    if [ $? -eq 0 ] && [ -n "$OUTPUT" ]; then
        STATS=$(echo "$OUTPUT" | awk -F'/' '/rtt/ {print $4","$5","$6","$7}')
        LOSS=$(echo "$OUTPUT" | grep -oP '[0-9.]+(?=% packet loss)' || echo "0")
        if [ -n "$STATS" ]; then
            MIN=$(echo "$STATS" | cut -d',' -f1)
            AVG=$(echo "$STATS" | cut -d',' -f2)
            MAX=$(echo "$STATS" | cut -d',' -f3)
            echo "$TIMESTAMP,$MIN,$AVG,$MAX,$LOSS" >> "$CSV_FILE"
        fi
    else
        echo "$TIMESTAMP,0.0,0.0,0.0,100" >> "$CSV_FILE"
    fi
    sleep 20
done
