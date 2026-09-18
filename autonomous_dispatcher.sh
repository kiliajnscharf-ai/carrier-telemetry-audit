#!/usr/bin/env bash
# Autonomer Dispatcher fuer Vodafone Carrier Telemetrie

INTERVAL=600  # 10 Minuten Takt

echo "[INIT] Starte autonomen Dispatcher (Intervall: ${INTERVAL}s)..."

while true; do
    # 1. Telemetrie-JSON neu berechnen
    ./export_telemetry_json.sh >/dev/null 2>&1

    # 2. Text-Update fuer Tickets/Mails aktualisieren
    TIMESTAMP=$(date -u '+%Y-%m-%d %H:%M:%S UTC')
    CYCLES=$(awk -F, 'NR>1 && $1 !~ /^#/ && $4 ~ /^[0-9.]+$/ {c++} END {print c}' core_node_latency.csv)
    
    cat << TOUT > ticket_live_update.txt
AUTOMATISIERTES TELEMETRIE-UPDATE (STAND: ${TIMESTAMP})
Zielknoten: 145.254.2.19 (Vodafone Core AS3209)
Messbasis: ${CYCLES} Zyklen (Langzeit-Monitoring)

$(python3 - << 'PYEOF'
import json
with open("carrier_telemetry_report.json") as f:
    d = json.load(f)
m = d["metrics"]
r = d["reliability"]
print(f"Aktuelle Core-Latenzen:\n- Baseline: {m['latency_baseline_ms']} ms\n- Median (p50): {m['latency_p50_ms']} ms\n- 90. Perzentil (p90): {m['latency_p90_ms']} ms\n- 95. Perzentil (p95): {m['latency_p95_ms']} ms\n- Maximaler Peak: {m['latency_max_ms']} ms\n- Paketverlust: {round(r['loss_events_ratio']*100, 2)} % der Zyklen (Max: {r['max_packet_loss_percent']} %)")
PYEOF
)

Status: CRITICAL_BUFFERBLOAT
Handlungsempfehlung NOC: Deployment von AQM (FQ-CoDel/CAKE) gemaess RFC 8290.
TOUT

    echo "[$(date '+%Y-%m-%d %H:%M:%S')] Update fuer Zyklus ${CYCLES} autonom bereitgestellt."
    
    # 3. Warteschleife
    sleep "$INTERVAL"
done
