#!/usr/bin/env bash
if [ ! -f "carrier_telemetry_report.json" ]; then
    echo "Report-Datei nicht gefunden. Generiere neu..."
    ./export_telemetry_json.sh >/dev/null 2>&1
fi

python3 - << 'PYEOF'
import json

with open("carrier_telemetry_report.json", "r") as f:
    d = json.load(f)

m = d.get("metrics", {})
r = d.get("reliability", {})
rec = d.get("noc_recommendation", {})

print("=" * 60)
print(f" CARRIER TELEMETRY DASHBOARD - NODE: {d.get('target_core_node')}")
print("=" * 60)
print(f"Messzeitpunkt (UTC) : {d.get('timestamp_utc')}")
print(f"Datenbasis          : {d.get('sample_size')} Messzyklen")
print("-" * 60)
print(f"Baseline-Latenz     : {m.get('latency_baseline_ms')} ms")
print(f"Median (p50)        : {m.get('latency_p50_ms')} ms")
print(f"95. Perzentil (p95) : {m.get('latency_p95_ms')} ms")
print(f"Absoluter Peak      : {m.get('latency_max_ms')} ms")
print(f"Verlustrate Zyklen  : {round(r.get('loss_events_ratio', 0) * 100, 1)} %")
print(f"Maximaler Verlust   : {r.get('max_packet_loss_percent')} %")
print("-" * 60)
print(f"Status-Befund       : [{rec.get('condition')}]")
print(f"Empfohlene Aktion   : {rec.get('action_required')}")
print("=" * 60)
PYEOF
