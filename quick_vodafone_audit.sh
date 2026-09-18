#!/usr/bin/env bash
set -euo pipefail

# Bekannte Kernknoten aus der vorherigen Analyse
TARGETS=(
  "192.168.0.1"
  "pools.vodafone-ip.de"
  "145.254.2.19"
  "8.8.8.8"
)

OUTFILE="vodafone_evidence/quick_audit_$(date +%Y%m%d_%H%M).txt"
mkdir -p vodafone_evidence

printf "%-25s %-10s %-10s %-10s %-10s\n" "Host/IP" "Loss%" "Min(ms)" "Avg(ms)" "Max(ms)" | tee "$OUTFILE"
echo "----------------------------------------------------------------------" | tee -a "$OUTFILE"

for target in "${TARGETS[@]}"; do
    echo "Prüfe Ziel: $target ..." >&2
    STATS=$(ping -c 5 -W 2 -q "$target" 2>/dev/null || true)
    
    if [ -n "$STATS" ] && echo "$STATS" | grep -q "rtt"; then
        LOSS=$(echo "$STATS" | awk -F',' '/packet loss/ {print $3}' | awk '{print $1}')
        RTT=$(echo "$STATS" | awk -F'/' '/rtt/ {printf "%.1f %.1f %.1f", $4, $5, $6}')
        MIN=$(echo "$RTT" | awk '{print $1}')
        AVG=$(echo "$RTT" | awk '{print $2}')
        MAX=$(echo "$RTT" | awk '{print $3}')
        printf "%-25s %-10s %-10s %-10s %-10s\n" "$target" "$LOSS" "$MIN" "$AVG" "$MAX" | tee -a "$OUTFILE"
    else
        printf "%-25s %-10s %-10s %-10s %-10s\n" "$target" "100%" "N/A" "N/A" "N/A" | tee -a "$OUTFILE"
    fi
done

echo "Audit erfolgreich abgeschlossen. Daten gesichert in $OUTFILE"
