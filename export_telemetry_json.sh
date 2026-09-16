#!/usr/bin/env bash
FILE="core_node_latency.csv"
OUT="carrier_telemetry_report.json"

if [ ! -f "$FILE" ]; then
    echo "Fehler: $FILE nicht gefunden."
    exit 1
fi

python3 - << 'PYEOF'
import csv
import json
import statistics
from datetime import datetime

file_path = "core_node_latency.csv"
latencies = []
losses = []
cycles = 0

with open(file_path, "r") as f:
    reader = csv.reader(f)
    for row in reader:
        if not row or row[0].startswith("#") or len(row) < 5:
            continue
        try:
            max_rtt = float(row[3])
            loss = float(row[4])
            latencies.append(max_rtt)
            losses.append(loss)
            cycles += 1
        except (ValueError, IndexError):
            continue

if cycles == 0:
    print("Keine validen Messdaten vorhanden.")
    exit(1)

latencies.sort()
p50 = statistics.median(latencies)
p90 = latencies[int(len(latencies) * 0.90)]
p95 = latencies[int(len(latencies) * 0.95)]
max_val = max(latencies)
min_val = min(latencies)
mean_val = statistics.mean(latencies)
loss_cycles = sum(1 for l in losses if l > 0)

telemetry = {
    "carrier_audit_standard": "v1.0-carrier-telemetry",
    "target_core_node": "145.254.2.19",
    "timestamp_utc": datetime.utcnow().isoformat() + "Z",
    "sample_size": cycles,
    "metrics": {
        "latency_baseline_ms": round(min_val, 2),
        "latency_mean_ms": round(mean_val, 2),
        "latency_p50_ms": round(p50, 2),
        "latency_p90_ms": round(p90, 2),
        "latency_p95_ms": round(p95, 2),
        "latency_max_ms": round(max_val, 2)
    },
    "reliability": {
        "loss_events_ratio": round(loss_cycles / cycles, 4),
        "max_packet_loss_percent": max(losses)
    },
    "noc_recommendation": {
        "condition": "CRITICAL_BUFFERBLOAT" if p95 > 100 else "NOMINAL",
        "action_required": "Deploy AQM (FQ-CoDel/CAKE) and configure BDP buffer sizing"
    }
}

with open("carrier_telemetry_report.json", "w") as out_f:
    json.dump(telemetry, out_f, indent=2)

print("Carrier-Standard-Report erfolgreich generiert:")
print(json.dumps(telemetry, indent=2))
PYEOF
