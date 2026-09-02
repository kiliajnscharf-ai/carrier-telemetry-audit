#!/bin/bash
# ==========================================================
# PROJEKT HAUS IM WIND - 24H BEWEISSICHERUNG (PLATZ 1)
# SYSTEM: UBUNTU | ZIEL: ANBIETER-REKLAMATION
# ==========================================================

CSV_FILE="mobilfunk_beweis_$(date +%Y%m%d).csv"
echo "Zeitstempel,IP,Ping_Avg,Loss_Prozent,DNS_ms,Speed_KBps" > $CSV_FILE

echo "----------------------------------------------------------"
echo "AUDIT GESTARTET. DATEI: $CSV_FILE"
echo "DRÜCKE [CTRL+C] ZUM BEENDEN."
echo "----------------------------------------------------------"

while true; do
    TIMESTAMP=$(date "+%Y-%m-%d %H:%M:%S")
    
    # PING & LOSS ERFASSUNG
    PING_DATA=$(fping -c 10 -q 8.8.8.8 2>&1)
    LOSS=$(echo "$PING_DATA" | awk -F '/' '{print $3}' | grep -oP '\d+(?=%)')
    AVG_PING=$(echo "$PING_DATA" | awk -F '/' '{print $8}')
    
    # DNS PERFORMANCE PRÜFUNG
    DNS_TIME=$(dig google.com | grep "Query time" | awk '{print $4}')
    
    # DOWNLOAD SPEED MESSUNG (BASH-NATIV VIA CURL)
    SPEED=$(curl -L -w "%{speed_download}" -o /dev/null -s --max-time 15 http://speedtest.tele2.net/1MB.zip)
    SPEED_KB=$(echo "scale=0; $SPEED / 1024" | bc -l 2>/dev/null || echo 0)
    
    # IN CSV-DATEI SCHREIBEN
    echo "$TIMESTAMP,8.8.8.8,$AVG_PING,$LOSS,$DNS_TIME,$SPEED_KB" >> $CSV_FILE
    
    # LOGISCHE STATUS-AUSGABE
    echo "[$TIMESTAMP] LOSS: $LOSS% | SPEED: $SPEED_KB KB/s | STATUS: OK"
    
    # INTERVALL: 60 SEKUNDEN
    sleep 60
done
