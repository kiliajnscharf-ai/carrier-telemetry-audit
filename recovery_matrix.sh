#!/bin/bash

# Recovery-Matrix für Astra 19.2E
# Klassifikation basierend auf SNR-Delta, Lock-State und BER-Thresholds

classify_recovery_state() {
    local lock="$1"
    local snr_db="$2"
    local target_snr="$3"
    local ber="$4"

    # Lock-State
    if [ "$lock" != "FE_HAS_LOCK" ]; then
        echo "CRITICAL_NO_LOCK"
        return
    fi

    # SNR-Delta
    local delta
    delta=$(echo "scale=2; $snr_db - $target_snr" | bc -l 2>/dev/null)

    if (( $(echo "$delta >= 0" | bc -l) )); then
        snr_state="SNR_OK"
    elif (( $(echo "$delta >= -2" | bc -l) )); then
        snr_state="SNR_WARN"
    else
        snr_state="SNR_FAIL"
    fi

    # BER-Thresholds (simuliert, da WSL kein DVB-Frontend hat)
    if [ -z "$ber" ] || [ "$ber" = "0" ]; then
        ber_state="BER_OK"
    elif (( $(echo "$ber < 0.001" | bc -l) )); then
        ber_state="BER_WARN"
    else
        ber_state="BER_FAIL"
    fi

    echo "${snr_state}_${ber_state}"
}
