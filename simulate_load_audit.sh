#!/usr/bin/env bash
set -euo pipefail

TARGET_IP="145.254.2.19"
LOGFILE="simulation_audit_$(date +%Y%m%d_%H%M%S).csv"

echo "Timestamp;Probe_Type;Target;Latency_ms;HTTP_Code" > "$LOGFILE"

echo "Starte Lastsimulation und Latenz-Audit gegen Vodafone Backbone..."

for i in {1..100}; do
    TIMESTAMP=$(date +"%Y-%m-%d %H:%M:%S")
    
    # 1. ICMP-Latenz zum Core-Router messen
    PING_RES=$(ping -c 1 -W 2 "$TARGET_IP" 2>/dev/null | awk -F'time=' '/time=/ {print $2}' | cut -d' ' -f1 || echo "TIMEOUT")
    echo "$TIMESTAMP;ICMP;$TARGET_IP;$PING_RES;N/A" | tee -a "$LOGFILE"

    # 2. Parallel TCP/HTTP-Lastanfrage simulieren
    HTTP_RES=$(curl -o /dev/null -s -w "%{time_total};%{http_code}" https://www.cloudflare.com/ || echo "TIMEOUT;000")
    CURL_TIME=$(echo "$HTTP_RES" | cut -d';' -f1)
    CURL_CODE=$(echo "$HTTP_RES" | cut -d';' -f2)
    echo "$TIMESTAMP;HTTP_SIM;cloudflare.com;$CURL_TIME;$CURL_CODE" | tee -a "$LOGFILE"

    sleep 1
done
