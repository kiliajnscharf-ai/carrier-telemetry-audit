#!/usr/bin/env bash
set -euo pipefail

TARGET="8.8.8.8"
OUTFILE="vodafone_evidence/hop_audit_$(date +%Y%m%d_%H%M).txt"

echo "Ermittle Hops zu $TARGET..."
HOPS=$(tracepath -n "$TARGET" | awk '/^[ ]*[0-9]+:/ {print $2}' | grep -v '^[0-9]' | grep -v '^[?]' | sort -u)

echo "Führe Hop-by-Hop Latenz- und Loss-Audit durch..."
printf "%-25s %-10s %-10s %-10s %-10s\n" "Host/IP" "Loss%" "Min(ms)" "Avg(ms)" "Max(ms)" | tee "$OUTFILE"
echo "----------------------------------------------------------------------" | tee -a "$OUTFILE"

for hop in $HOPS; do
    STATS=$(ping -c 10 -q "$hop" 2>/dev/null || true)
    if [ -n "$STATS" ]; then
        LOSS=$(echo "$STATS" | awk -F',' '/packet loss/ {print $3}' | awk '{print $1}')
        RTT=$(echo "$STATS" | awk -F'/' '/rtt/ {printf "%.1f %.1f %.1f", $4, $5, $6}' || echo "N/A N/A N/A")
        MIN=$(echo "$RTT" | awk '{print $1}')
        AVG=$(echo "$RTT" | awk '{print $2}')
        MAX=$(echo "$RTT" | awk '{print $3}')
        printf "%-25s %-10s %-10s %-10s %-10s\n" "$hop" "$LOSS" "$MIN" "$AVG" "$MAX" | tee -a "$OUTFILE"
    else
        printf "%-25s %-10s %-10s %-10s %-10s\n" "$hop" "100%" "N/A" "N/A" "N/A" | tee -a "$OUTFILE"
    fi
done

echo "Audit abgeschlossen. Gespeichert in $OUTFILE"
