#!/bin/bash

CONFIG_FILE="config.json"
CHANNELS_CONF="channels.conf"
LOG_FILE="/var/log/sat_monitor.log"
SIMULATION_MODE=1
POLL_INTERVAL=10

generate_channels_conf() {
    > "$CHANNELS_CONF"
    tp_count=$(jq '.transponders | length' "$CONFIG_FILE")
    for ((i=0; i<tp_count; i++)); do
        freq=$(jq -r ".transponders[$i].frequency_mhz" "$CONFIG_FILE")
        pol=$(jq -r ".transponders[$i].polarization" "$CONFIG_FILE")
        echo "TP$i $freq $pol" >> "$CHANNELS_CONF"
    done
}

log_event() {
    printf "%s TP=%s FREQ=%s POL=%s LOCK=%s SNR_dB=%s SIG=%s HEALTH=%s ACTION=%s\n" \
        "$(date +'%Y-%m-%dT%H:%M:%S')" "$1" "$2" "$3" "$4" "$5" "$6" "$7" "$8" \
        >> "$LOG_FILE"
}

safe() { [ -z "$1" ] && echo 0 || echo "$1"; }

simulate_metrics() {
    lock="FE_HAS_LOCK"
    snr_db=$(echo "scale=2; 5 + ($RANDOM % 40)/10" | bc -l)
    sig_pct=$((50 + RANDOM % 50))
    echo "$lock;$snr_db;$sig_pct"
}

compute_health() {
    lock="$1"
    snr="$2"
    target="$3"

    if [ "$lock" != "FE_HAS_LOCK" ]; then
        echo "CRITICAL"
        return
    fi

    delta=$(echo "scale=2; $snr - $target" | bc -l)

    if (( $(echo "$delta >= 0" | bc -l) )); then
        echo "NOMINAL"
    elif (( $(echo "$delta >= -2" | bc -l) )); then
        echo "DEGRADED"
    else
        echo "CRITICAL"
    fi
}

classify_recovery_state() {
    lock="$1"
    snr="$2"
    target="$3"
    delta=$(echo "scale=2; $snr - $target" | bc -l)

    if [ "$lock" != "FE_HAS_LOCK" ]; then
        echo "CRITICAL_NO_LOCK"
        return
    fi

    if (( $(echo "$delta >= 0" | bc -l) )); then
        echo "SNR_OK"
    elif (( $(echo "$delta >= -2" | bc -l) )); then
        echo "SNR_WARN"
    else
        echo "SNR_FAIL"
    fi
}

declare -A LOCK_FAIL

monitor_tp() {
    i="$1"

    tp_id=$(jq -r ".transponders[$i].tp_id" "$CONFIG_FILE")
    freq=$(jq -r ".transponders[$i].frequency_mhz" "$CONFIG_FILE")
    pol=$(jq -r ".transponders[$i].polarization" "$CONFIG_FILE")
    band=$(jq -r ".transponders[$i].band" "$CONFIG_FILE")
    std=$(jq -r ".transponders[$i].standard" "$CONFIG_FILE")
    sr=$(jq -r ".transponders[$i].symbolrate_ksps" "$CONFIG_FILE")
    fec=$(jq -r ".transponders[$i].fec" "$CONFIG_FILE")
    net=$(jq -r ".transponders[$i].net_ts_bitrate_mbps" "$CONFIG_FILE")
    target=$(jq -r ".transponders[$i].target_snr_db" "$CONFIG_FILE")

    if [ "$SIMULATION_MODE" -eq 1 ]; then
        metrics=$(simulate_metrics)
        lock=$(echo "$metrics" | cut -d';' -f1)
        snr_db=$(echo "$metrics" | cut -d';' -f2)
        sig_pct=$(echo "$metrics" | cut -d';' -f3)
    else
        dvbv5-zap -c "$CHANNELS_CONF" -f "$freq" -p "$pol" >/dev/null 2>&1 &
        zap_pid=$!
        sleep 1
        femon_output=$(femon -H 2>/dev/null)
        kill "$zap_pid"

        lock=$(echo "$femon_output" | grep -m1 "status" | awk '{print $2}')
        snr_pct=$(echo "$femon_output" | grep -m1 "SNR" | awk '{print $3}' | sed 's/%//')
        sig_pct=$(echo "$femon_output" | grep -m1 "signal" | awk '{print $3}' | sed 's/%//')
        snr_db=$(echo "scale=2; 20*l($snr_pct/100)/l(10)" | bc -l)
    fi

    lock=$(safe "$lock")
    snr_db=$(safe "$snr_db")
    sig_pct=$(safe "$sig_pct")

    health=$(compute_health "$lock" "$snr_db" "$target")
    recovery=$(classify_recovery_state "$lock" "$snr_db" "$target")

    if [ "$lock" != "FE_HAS_LOCK" ]; then
        LOCK_FAIL[$tp_id]=$((LOCK_FAIL[$tp_id] + 1))
    else
        LOCK_FAIL[$tp_id]=0
    fi

    if [ "${LOCK_FAIL[$tp_id]}" -ge 3 ]; then
        log_event "$tp_id" "$freq" "$pol" "$lock" "$snr_db" "$sig_pct" "$recovery" "RETUNE"
        LOCK_FAIL[$tp_id]=0
    fi

    log_event "$tp_id" "$freq" "$pol" "$lock" "$snr_db" "$sig_pct" "$recovery" "MONITOR"

    printf "%-6s %-10s %-4s %-5s %-7s %-10s %-6s %-12s %-10s %-10s %-10s %-10s %-15s\n" \
        "$tp_id" "$freq" "$pol" "$band" "$std" "$sr" "$fec" "$net" "$target" "$lock" "$snr_db" "$sig_pct" "$recovery"
}

main() {
    generate_channels_conf
    tp_count=$(jq '.transponders | length' "$CONFIG_FILE")

    while true; do
        printf "%-6s %-10s %-4s %-5s %-7s %-10s %-6s %-12s %-10s %-10s %-10s %-10s %-15s\n" \
            "TP" "FREQ" "POL" "BAND" "STD" "SR" "FEC" "NET_Mbps" "TGT_SNR" "LOCK" "SNR_dB" "SIG_%" "RECOVERY"
        printf "%0.s-" {1..120}
        echo ""

        for ((i=0; i<tp_count; i++)); do
            monitor_tp "$i"
        done

        sleep "$POLL_INTERVAL"
        echo ""
    done
}

main
