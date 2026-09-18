#!/usr/bin/env bash
TARGET="145.254.2.19"
LOGFILE="core_node_latency.csv"

[ ! -f "$LOGFILE" ] && echo "timestamp,min_ms,avg_ms,max_ms,loss_pct" > "$LOGFILE"

while true; do
    TS=$(date +"%Y-%m-%d %H:%M:%S")
    PING_OUT=$(ping -c 10 -W 2 "$TARGET" 2>/dev/null)
    LOSS=$(echo "$PING_OUT" | grep -oP '\d+(?=% packet loss)')
    STATS=$(echo "$PING_OUT" | awk -F'/' 'END {gsub(/.*= /, "", $4); print $4 "," $5 "," $6}')
    
    if [ -n "$STATS" ]; then
        echo "$TS,$STATS,$LOSS" >> "$LOGFILE"
    else
        echo "$TS,FAIL,FAIL,FAIL,100" >> "$LOGFILE"
    fi
    sleep 60
done
