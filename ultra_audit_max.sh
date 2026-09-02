#!/bin/bash
CSV_FILE="audit_max_$(date +%Y%m%d).csv"
echo "Timestamp,Target,Avg_Ping,Loss,DNS_ms,Speed_KBps,CPU_Load,RAM_Free_MB" > $CSV_FILE
while true; do
    TS=$(date "+%Y-%m-%d %H:%M:%S")
    NET_DATA=$(fping -c 5 -q 8.8.8.8 2>&1)
    LOSS=$(echo "$NET_DATA" | awk -F '/' '{print $3}' | grep -oP '\d+(?=%)')
    PING=$(echo "$NET_DATA" | awk -F '/' '{print $8}')
    DNS=$(dig google.com | grep "Query time" | awk '{print $4}' || echo 0)
    SPEED_RAW=$(curl -L -w "%{speed_download}" -o /dev/null -s --max-time 10 http://speedtest.tele2.net/1MB.zip)
    SPEED_KB=$(echo "scale=0; $SPEED_RAW / 1024" | bc -l 2>/dev/null || echo 0)
    CPU_LOAD=$(top -bn1 | grep "Cpu(s)" | awk '{print $2}' | cut -d',' -f1)
    RAM_FREE=$(free -m | awk '/Mem:/ {print $4}')
    echo "$TS,8.8.8.8,$PING,$LOSS,$DNS,$SPEED_KB,$CPU_LOAD,$RAM_FREE" >> $CSV_FILE
    echo "[$TS] SPEED: $SPEED_KB KB/s | LOSS: $LOSS% | STATUS: MAXIMUM"
    sleep 60
done
