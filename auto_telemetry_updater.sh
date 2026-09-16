#!/usr/bin/env bash
while true; do
    ./export_telemetry_json.sh >/dev/null 2>&1
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] JSON-Report aktualisiert. Datensätze:" $(grep -c "^202" core_node_latency.csv)
    sleep 600
done
