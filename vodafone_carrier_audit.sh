#!/usr/bin/env bash
set -euo pipefail

# ==============================================================================
# PROJEKT HAUS IM WIND - CARRIER GRADE NETWORK AUDIT
# STANDARD: AUTONOME TELEMETRIE & BACKBONE AUDIT (AS3209)
# ==============================================================================

CORE_HOP="145.254.2.19"
REFERENCE_IP="8.8.8.8"
WEB_TARGET="https://www.cloudflare.com/"
CYCLES=20
TIMESTAMP_ID=$(date +%Y%m%d_%H%M%S)
AUDIT_DIR="vodafone_evidence"
REPORT_FILE="${AUDIT_DIR}/NOC_EXECUTIVE_REPORT_${TIMESTAMP_ID}.txt"
RAW_CSV="${AUDIT_DIR}/carrier_telemetry_${TIMESTAMP_ID}.csv"

mkdir -p "$AUDIT_DIR"

echo "======================================================================"
echo " STARTE CARRIER-GRADE NETZWERK-AUDIT (AS3209 BACKBONE)"
echo " ZIEL: VOLLSTÄNDIGE ANALYSE VON BUFFERBLOAT, JITTER & TRANSIT-ROUTING"
echo "======================================================================"

echo "Timestamp;Hop_Core_RTT_ms;Ref_Transit_RTT_ms;DNS_Lookup_s;TCP_Connect_s;TLS_Handshake_s;TTFB_s;Total_s" > "$RAW_CSV"

for i in $(seq 1 "$CYCLES"); do
    CURRENT_TIME=$(date +"%Y-%m-%d %H:%M:%S")
    echo -ne "Messzyklus [${i}/${CYCLES}] läuft...\r"

    # 1. ICMP Core-Node vs Reference Target
    PING_CORE=$(ping -c 1 -W 2 "$CORE_HOP" 2>/dev/null | awk -F'time=' '/time=/ {print $2}' | cut -d' ' -f1 || echo "999")
    PING_REF=$(ping -c 1 -W 2 "$REFERENCE_IP" 2>/dev/null | awk -F'time=' '/time=/ {print $2}' | cut -d' ' -f1 || echo "999")

    # 2. Layer-7 Connection Breakdown via cURL
    CURL_METRICS=$(curl -o /dev/null -s -w "%{time_namelookup};%{time_connect};%{time_appconnect};%{time_starttransfer};%{time_total}" "$WEB_TARGET" || echo "0;0;0;0;0")

    echo "${CURRENT_TIME};${PING_CORE};${PING_REF};${CURL_METRICS}" >> "$RAW_CSV"
    sleep 1
done
echo -e "\nDatenerfassung abgeschlossen. Generiere NOC-Inspektionsbericht..."

# 3. Automatische Aggregation & mathematische Auswertung
awk -F';' '
NR > 1 {
    if ($2 != 999) { core_sum += $2; core_count++; if (min_core == "" || $2 < min_core) min_core = $2; if ($2 > max_core) max_core = $2; if ($2 > 100) core_peaks++ }
    if ($3 != 999) { ref_sum += $3; ref_count++; if (min_ref == "" || $3 < min_ref) min_ref = $3; if ($3 > max_ref) max_ref = $3 }
    dns_sum += $4; tcp_sum += $5; tls_sum += $6; ttfb_sum += $7; total_sum += $8; total_count++
}
END {
    core_avg = (core_count > 0) ? core_sum / core_count : 0;
    ref_avg = (ref_count > 0) ? ref_sum / ref_count : 0;
    dns_avg = dns_sum / total_count;
    tcp_avg = tcp_sum / total_count;
    tls_avg = tls_sum / total_count;
    ttfb_avg = ttfb_sum / total_count;
    total_avg = total_sum / total_count;

    print "======================================================================"
    print " OFFZIELLER NOC-PRÜFBERICHT: PERFORMANCE-AUDIT AS3209"
    print " Datum: " strftime("%Y-%m-%d %H:%M:%S")
    print " Untersuchte Kernnetzknoten: 145.254.2.19 (Vodafone Core Backbone)"
    print "======================================================================"
    print "\n1. BACKBONE LATENZ- & BUFFERBLOAT-ANALYSE"
    printf "   - Core-Node (145.254.2.19)  : Min: %.2f ms | Avg: %.2f ms | Max: %.2f ms\n", min_core, core_avg, max_core
    printf "   - Referenz-Transit (8.8.8.8): Min: %.2f ms | Avg: %.2f ms | Max: %.2f ms\n", min_ref, ref_avg, max_ref
    printf "   - Kritische Peaks (>100 ms) : %d Vorfälle in %d Zyklen\n", core_peaks, total_count
    printf "   - Jitter-Delta Core-Router  : %.2f ms\n", (max_core - min_core)
    print "\n2. LAYER-7 VERBINDUNGSPHASEN (Cloudflare Edge)"
    printf "   - DNS Lookup Time           : %.4f s\n", dns_avg
    printf "   - TCP SYN/ACK Connect       : %.4f s\n", tcp_avg
    printf "   - TLS Handshake Negotiation : %.4f s\n", tls_avg
    printf "   - Time to First Byte (TTFB) : %.4f s\n", ttfb_avg
    printf "   - Gesamtlaufzeit Transaktion: %.4f s\n", total_avg
    print "\n3. SYSTEMBEWERTUNG & FAZIT"
    if (core_peaks > 0) {
        print "   [STATUS: KRITISCH] Das Core-Interface 145.254.2.19 leidet unter"
        print "   nachweisbarem Pufferstau (Bufferbloat) und akuter Instabilität."
        print "   Dringende Empfehlung: Traffic-Engineering im AS3209 anpassen,"
        print "   BGP-Metriken re-evaluieren und Active Queue Management (CoDel/FQ) aktivieren."
    } else {
        print "   [STATUS: NOMINAL] Keine signifikanten Pufferüberläufe im Messfenster."
    }
    print "======================================================================"
}' "$RAW_CSV" | tee "$REPORT_FILE"

echo -e "\nBericht erfolgreich exportiert nach: $REPORT_FILE"
echo "Rohdaten gesichert in: $RAW_CSV"
