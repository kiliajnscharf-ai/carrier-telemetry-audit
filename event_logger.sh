#!/bin/bash

LOG_FILE="/var/log/sat_events.log"

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
