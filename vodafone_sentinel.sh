#!/usr/bin/env bash
set -euo pipefail

EVIDENCE_DIR="vodafone_evidence"
CORE_HOP="145.254.2.19"
REF_TARGET="8.8.8.8"
WEB_TARGET="https://www.cloudflare.com/"
mkdir -p "$EVIDENCE_DIR"

show_header() {
    clear
    echo "======================================================================"
    echo "       VODAFONE SENTINEL - CARRIER-GRADE AUDIT PROGRAMM"
    echo "       AS3209 CORE BACKBONE TELEMETRIE & BUFFERBLOAT-DETEKTION"
    echo "======================================================================"
}

run_audit() {
    local cycles="${1:-20}"
    local timestamp_id
    timestamp_id=$(date +%Y%m%d_%H%M%S)
    local raw_csv="${EVIDENCE_DIR}/carrier_telemetry_${timestamp_id}.csv"
    local report_file="${EVIDENCE_DIR}/NOC_EXECUTIVE_REPORT_${timestamp_id}.txt"

    echo "Starte Audit-Messung mit $cycles Zyklen gegen $CORE_HOP..."
    echo "Timestamp;Hop_Core_RTT_ms;Ref_Transit_RTT_ms;DNS_Lookup_s;TCP_Connect_s;TLS_Handshake_s;TTFB_s;Total_s" > "$raw_csv"

    for i in $(seq 1 "$cycles"); do
        echo -ne "Messzyklus [${i}/${cycles}] läuft...\r"
        local current_time
        current_time=$(date +"%Y-%m-%d %H:%M:%S")

        local ping_core
        ping_core=$(ping -c 1 -W 2 "$CORE_HOP" 2>/dev/null | awk -F'time=' '/time=/ {print $2}' | cut -d' ' -f1 || echo "999")
        local ping_ref
        ping_ref=$(ping -c 1 -W 2 "$REF_TARGET" 2>/dev/null | awk -F'time=' '/time=/ {print $2}' | cut -d' ' -f1 || echo "999")
        local curl_metrics
        curl_metrics=$(curl -o /dev/null -s -w "%{time_namelookup};%{time_connect};%{time_appconnect};%{time_starttransfer};%{time_total}" "$WEB_TARGET" || echo "0;0;0;0;0")

        echo "${current_time};${ping_core};${ping_ref};${curl_metrics}" >> "$raw_csv"
        sleep 1
    done

    echo -e "\nGeneriere Auswertungsbericht..."
    awk -F';' -v report="$report_file" '
    NR > 1 {
        if ($2 != 999) { core_sum += $2; core_count++; if (min_core == "" || $2 < min_core) min_core = $2; if ($2 > max_core) max_core = $2; if ($2 > 100) core_peaks++ }
        if ($3 != 999) { ref_sum += $3; ref_count++; if (min_ref == "" || $3 < min_ref) min_ref = $3; if ($3 > max_ref) max_ref = $3 }
        dns_sum += $4; tcp_sum += $5; tls_sum += $6; ttfb_sum += $7; total_sum += $8; total_count++
    }
    END {
        core_avg = (core_count > 0) ? core_sum / core_count : 0;
        ref_avg = (ref_count > 0) ? ref_sum / ref_count : 0;
        
        out = "======================================================================\n"
        out = out " NOC-AUDIT BERICHT: AS3209 BACKBONE\n"
        out = out " Datum: " strftime("%Y-%m-%d %H:%M:%S") "\n"
        out = out " Core-Hop: 145.254.2.19 | Referenz: 8.8.8.8\n"
        out = out "======================================================================\n"
        out = out sprintf(" Core-RTT Min/Avg/Max : %.2f / %.2f / %.2f ms\n", min_core, core_avg, max_core)
        out = out sprintf(" Transit-RTT Avg      : %.2f ms\n", ref_avg)
        out = out sprintf(" Peaks > 100 ms       : %d / %d Zyklen\n", core_peaks, total_count)
        out = out sprintf(" Jitter-Delta         : %.2f ms\n", (max_core - min_core))
        out = out sprintf(" TTFB / Total Time    : %.4f s / %.4f s\n", (ttfb_sum/total_count), (total_sum/total_count))
        out = out "======================================================================\n"
        printf "%s", out
        print out > report
    }' "$raw_csv"
    
    echo "Rohdaten: $raw_csv"
    echo "Bericht: $report_file"
}

run_mtu_check() {
    echo "Führe 1500-Byte-MTU-Test gegen $CORE_HOP durch..."
    ping -c 5 -M do -s 1472 "$CORE_HOP" | tee "${EVIDENCE_DIR}/mtu_check_$(date +%Y%m%d_%H%M%S).txt"
}

schedule_evening_run() {
    local target_time="20:30"
    local now_s target_s diff_s
    now_s=$(date +%s)
    target_s=$(date -d "$target_time" +%s)

    if [ "$target_s" -le "$now_s" ]; then
        echo "20:30 Uhr ist für heute bereits vergangen."
        return
    fi

    diff_s=$(( target_s - now_s ))
    echo "Scheduler aktiv: Startet in $diff_s Sekunden (um $target_time Uhr)."
    (sleep "$diff_s" && ./vodafone_sentinel.sh --audit 50) &
    echo "Hintergrund-Timer mit PID $! gestartet. UserLAnd nicht beenden!"
}

package_evidence() {
    echo "Berechne SHA256-Prüfsummen..."
    (cd "$EVIDENCE_DIR" && sha256sum *.* > SHA256SUMS.txt 2>/dev/null || true)
    local tar_name="vodafone_beweisakte_$(date +%Y%m%d_%H%M%S).tar.gz"
    tar -czvf "$tar_name" "$EVIDENCE_DIR"/
    echo "Beweisakte erfolgreich geschnürt: $tar_name"
}

show_peaks() {
    echo "Alle Latenzspitzen > 100 ms aus den Messungen:"
    awk -F';' '$2 > 100 && $2 != 999 {print $1, "Core-Latenz:", $2 "ms"}' "$EVIDENCE_DIR"/carrier_telemetry_*.csv 2>/dev/null || echo "Keine Telemetriedaten vorhanden."
}

# CLI-Parameterverarbeitung
if [ "${1:-}" = "--audit" ]; then
    run_audit "${2:-20}"
    exit 0
fi

# Interaktives Terminal-Menü
while true; do
    show_header
    echo "1) Sofort-Audit starten (20 Zyklen)"
    echo "2) Großer Stresstest starten (100 Zyklen)"
    echo "3) 1500-Byte-MTU-Prüfung ausführen"
    echo "4) Prime-Time-Timer für 20:30 Uhr scharfstellen"
    echo "5) Latenz-Peaks (> 100 ms) anzeigen"
    echo "6) Beweisarchiv (.tar.gz mit SHA256) packen"
    echo "0) Beenden"
    echo "======================================================================"
    read -rp "Auswahl eingeben [0-6]: " choice

    case "$choice" in
        1) run_audit 20; read -rp "Weiter mit Enter..." ;;
        2) run_audit 100; read -rp "Weiter mit Enter..." ;;
        3) run_mtu_check; read -rp "Weiter mit Enter..." ;;
        4) schedule_evening_run; read -rp "Weiter mit Enter..." ;;
        5) show_peaks; read -rp "Weiter mit Enter..." ;;
        6) package_evidence; read -rp "Weiter mit Enter..." ;;
        0) exit 0 ;;
        *) echo "Ungültige Eingabe."; sleep 1 ;;
    esac
done
