#!/usr/bin/env bash
# run_diagnostics.sh - Netzwerk-Testsuite

set -euo pipefail

LOG_FILE="network_benchmark_suite.csv"
[ ! -f "$LOG_FILE" ] && echo "timestamp,target,type,min_ms,avg_ms,max_ms,dns_ms" > "$LOG_FILE"

run_test() {
    local target="$1"
    local type="$2"
    local ts
    ts=$(date +"%Y-%m-%d %H:%M:%S")

    # ICMP Latenz (3 Pakete)
    local ping_data
    ping_data=$(ping -c 3 -W 2 "$target" 2>/dev/null | awk -F'/' 'END {gsub(/.*= /, "", $4); print $4 "," $5 "," $6}')
    [ -z "$ping_data" ] && ping_data="FAIL,FAIL,FAIL"

    # DNS Query Time (falls zutreffend)
    local dns_data="-"
    if [ "$type" == "DNS" ]; then
        dns_data=$(dig @$target de-cix.net +time=2 +tries=1 2>/dev/null | awk '/Query time:/ {print $4}')
        [ -z "$dns_data" ] && dns_data="FAIL"
    fi

    echo "$ts,$target,$type,$ping_data,$dns_data" >> "$LOG_FILE"
    printf "%-19s | %-15s | %-5s | %-20s | %-6s\n" "$ts" "$target" "$type" "$ping_data" "$dns_data"
}

printf "%-19s | %-15s | %-5s | %-20s | %-6s\n" "ZEIT" "ZIEL" "TYP" "MIN,AVG,MAX (ms)" "DNS(ms)"
echo "----------------------------------------------------------------------------------"

run_test "145.254.2.19" "CORE"
run_test "1.1.1.1" "DNS"
run_test "8.8.8.8" "DNS"
run_test "9.9.9.9" "DNS"
run_test "de-cix.net" "PEER"

echo "----------------------------------------------------------------------------------"
echo "Ergebnisse gespeichert in $LOG_FILE"
