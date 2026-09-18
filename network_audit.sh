#!/usr/bin/env bash
set -euo pipefail

TARGET="8.8.8.8"
LOGFILE="network_audit_$(date +%Y%m%d_%H%M%S).csv"

echo "Timestamp;Sequence;RTT_ms;Status" > "$LOGFILE"

echo "Starte Messung auf Platz-1-Niveau gegen $TARGET..."

ping -i 1 -O "$TARGET" | while read -r line; do
    TIMESTAMP=$(date +"%Y-%m-%d %H:%M:%S")
    if echo "$line" | grep -q "bytes from"; then
        SEQ=$(echo "$line" | grep -oP 'icmp_seq=\K[0-9]+')
        TIME=$(echo "$line" | grep -oP 'time=\K[0-9.]+')
        echo "$TIMESTAMP;$SEQ;$TIME;SUCCESS" | tee -a "$LOGFILE"
    elif echo "$line" | grep -q "no answer yet"; then
        SEQ=$(echo "$line" | grep -oP 'icmp_seq=\K[0-9]+')
        echo "$TIMESTAMP;$SEQ;TIMEOUT;PACKET_LOSS" | tee -a "$LOGFILE"
    fi
done
