#!/bin/bash
# Astra 19.2E – Full Userland Monitoring System (WSL/Docker compatible)

CONFIG_FILE="config.json"
CHANNELS_CONF="channels.conf"
LOG_FILE="/var/log/sat_events.log"
SIMULATION_MODE=1        # 1 = simulate dvbv5/femon (WSL), 0 = real tuner
POLL_INTERVAL=10

# -----------------------------
#  MODULE: channels.conf generator
# -----------------------------
generate_channels_conf() {
    if [ ! -f "$CONFIG_FILE" ]; then
        echo "ERROR: config.json missing" >&2
        exit 1
    fi

    > "$CHANNELS_CONF"

    tp_count=$(jq '.transponders | length' "$CONFIG_FILE")

    for ((i=0; i<tp_count; i++)); do
        freq=$(jq -r ".transponders[$i].frequency_mhz" "$CONFIG_FILE")
        pol=$(jq -r ".transponders[$i].polarization" "$CONFIG_FILE")

        echo "TP$i $freq $pol" >> "$CHANNELS_CONF"
    done
}

# -----------------------------
#  MODULE: event logger
# -----------------------------
log_event() {
    local tp_id="$1"
    local freq="$2"
    local pol="$3"
    local lock="$4"
    local snr_db="$5"
    local sig_pct="$6"
    local health="$7"
    local action="$8"

    printf "%s TP=%s FREQ=%s POL=%s LOCK=%s SNR_dB=%s SIG=%s HEALTH=%s ACTION=%s\n" \
        "$(date +'%Y-%m-%dT%H:%M:%S')" \
        "$tp_id" "$freq" "$pol" "$lock" "$snr_db" "$sig_pct" "$health" "$action" \
        >> "$LOG_FILE"
}

# -----------------------------
#  MODULE: safe-mode helpers
# -----------------------------
safe_value() {
    if [ -z "$1" ] || [ "$1" = "null" ]; then
        echo "0"
    else
        echo "$1"
    fi
}

safe_lock() {
    if [ -z "$1" ]; then
        echo "NO_LOCK"
    else
        echo "$1"
    fi
}

# -----------------------------
#  MODULE: simulation mode
# -----------------------------
simulate_metrics() {
    local snr_db=$(echo "scale=2; 5 + ($RANDOM % 40)/10" | bc -l)
    local sig_pct=$((50 + RANDOM % 50))
    local lock="FE_HAS_LOCK"

    echo "$lock;$snr_db;$sig_pct"
}

# -----------------------------
#  MODULE: health evaluation
# -----------------------------
compute_health_status() {
    local lock="$1"
    local snr_db="$2"
    local target_snr="$3"

    if [ "$lock" != "FE_HAS_LOCK" ]; then
        echo "CRITICAL"
        return
    fi

    delta=$(echo "scale=2; $snr_db - $target_snr" | bc -l 2>/dev/null)

    if [ -z "$delta" ]; then
        echo "DEGRADED"
        return
    fi

    if (( $(echo "$delta >= 0" | bc -l) )); then
        echo "NOMINAL"
    elif (( $(echo "$delta >= -2" | bc -l) )); then
        echo "DEGRADED"
    else
        echo "CRITICAL"
    fi
}

# -----------------------------
#  MODULE: monitor transponder
# -----------------------------
declare -A LOCK_FAIL_COUNT

monitor_transponder() {
    local i="$1"

    tp_id=$(jq -r ".transponders[$i].tp_id" "$CONFIG_FILE")
    freq=$(jq -r ".transponders[$i].frequency_mhz" "$CONFIG_FILE")
    pol=$(jq -r ".transponders[$i].polarization" "$CONFIG_FILE")
    band=$(jq -r ".transponders[$i].band" "$CONFIG_FILE")
    std=$(jq -r ".transponders[$i].standard" "$CONFIG_FILE")
    sr=$(jq -r ".transponders[$i].symbolrate_ksps" "$CONFIG_FILE")
    fec=$(jq -r ".transponders[$i].fec" "$CONFIG_FILE")
    net=$(jq -r ".transponders[$i].net_ts_bitrate_mbps" "$CONFIG_FILE")
    target_snr=$(jq -r ".transponders[$i].target_snr_db" "$CONFIG_FILE")

    # -----------------------------
    #  SIMULATION MODE (WSL)
    # -----------------------------
    if [ "$SIMULATION_MODE" -eq 1 ]; then
        metrics=$(simulate_metrics)
        lock=$(safe_lock "$(echo "$metrics" | cut -d';' -f1)")
        snr_db=$(safe_value "$(echo "$metrics" | cut -d';' -f2)")
        sig_pct=$(safe_value "$(echo "$metrics" | cut -d';' -f3)")
    else
        # REAL MODE (requires DVB tuner)
        dvbv5-zap -c "$CHANNELS_CONF" -f "$freq" -p "$pol" >/dev/null 2>&1 &
        zap_pid=$!
        sleep 1

        femon_output=$(femon -H 2>/dev/null | sed 's/\r//g')
        kill "$zap_pid" >/dev/null 2>&1

        lock=$(safe_lock "$(echo "$femon_output" | grep -m1 'status' | awk '{print $2}')")
        snr_pct=$(safe_value "$(echo "$femon_output" | grep -m1 'SNR' | awk '{print $3}' | sed 's/%//')")
        sig_pct=$(safe_value "$(echo "$femon_output" | grep -m1 'signal' | awk '{print $3}' | sed 's/%//')")

        snr_db=$(echo "scale=2; 20*l($snr_pct/100)/l(10)" | bc -l 2>/dev/null)
    fi

    health=$(compute_health_status "$lock" "$snr_db" "$target_snr")

    # -----------------------------
    #  RECOVERY LOGIC
    # -----------------------------
    if [ -z "${LOCK_FAIL_COUNT[$tp_id]}" ]; then
        LOCK_FAIL_COUNT[$tp_id]=0
    fi

    if [ "$lock" != "FE_HAS_LOCK" ]; then
        LOCK_FAIL_COUNT[$tp_id]=$((LOCK_FAIL_COUNT[$tp_id] + 1))
    else
        LOCK_FAIL_COUNT[$tp_id]=0
    fi

    if [ "${LOCK_FAIL_COUNT[$tp_id]}" -ge 3 ]; then
        log_event "$tp_id" "$freq" "$pol" "$lock" "$snr_db" "$sig_pct" "$health" "RETUNE"
        LOCK_FAIL_COUNT[$tp_id]=0
    fi

    log_event "$tp_id" "$freq" "$pol" "$lock" "$snr_db" "$sig_pct" "$health" "MONITOR"

    printf "%-6s %-10s %-4s %-5s %-7s %-10s %-6s %-12s %-10s %-10s %-10s %-10s\n" \
        "$tp_id" "$freq" "$pol" "$band" "$std" "$sr" "$fec" "$net" "$target_snr" "$lock" "$snr_db" "$sig_pct"
}

# -----------------------------
#  MAIN LOOP
# -----------------------------
main() {
    generate_channels_conf

    tp_count=$(jq '.transponders | length' "$CONFIG_FILE")

    while true; do
        printf "%-6s %-10s %-4s %-5s %-7s %-10s %-6s %-12s %-10s %-10s %-10s %-10s\n" \
            "TP" "FREQ" "POL" "BAND" "STD" "SR" "FEC" "NET_Mbps" "TGT_SNR" "LOCK" "SNR_dB" "SIG_%"
        printf "%0.s-" {1..110}
        echo ""

        for ((i=0; i<tp_count; i++)); do
            monitor_transponder "$i"
        done

        sleep "$POLL_INTERVAL"
        echo ""
    done
}

main
