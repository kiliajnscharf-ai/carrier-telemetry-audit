#!/usr/bin/env bash
set -e

CSV="core_node_latency.csv"
OUT="index.html"

if [ ! -f "$CSV" ]; then
    echo "Fehler: $CSV nicht gefunden."
    exit 1
fi

TOTAL=$(awk -F, 'NR>1 && $1 !~ /^#/ && $4 ~ /^[0-9.]+$/ {c++} END {print c}' "$CSV")
AVG_RTT=$(awk -F, 'NR>1 && $1 !~ /^#/ && $4 ~ /^[0-9.]+$/ {sum+=$4; c++} END {if(c>0) printf "%.2f", sum/c; else print "0"}' "$CSV")
MAX_RTT=$(awk -F, 'NR>1 && $1 !~ /^#/ && $4 ~ /^[0-9.]+$/ {if($4>max) max=$4} END {printf "%.2f", max}' "$CSV")
MAX_DROP=$(awk -F, 'NR>1 && $1 !~ /^#/ && $3 ~ /^[0-9.]+$/ {if($3>max) max=$3} END {printf "%.1f", max}' "$CSV")

cat << HTML > "$OUT"
<!DOCTYPE html>
<html lang="de">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Carrier Telemetry & Network Infrastructure Audit</title>
<style>
  body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, monospace; background: #0d1117; color: #c9d1d9; margin: 0; padding: 24px; line-height: 1.5; }
  .container { max-width: 1100px; margin: 0 auto; }
  h1 { color: #58a6ff; border-bottom: 1px solid #30363d; padding-bottom: 12px; font-size: 26px; }
  h2 { color: #f0f6fc; margin-top: 28px; font-size: 20px; border-bottom: 1px solid #21262d; padding-bottom: 6px; }
  .grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 16px; margin: 20px 0; }
  .card { background: #161b22; border: 1px solid #30363d; border-radius: 8px; padding: 16px; }
  .card .label { font-size: 12px; color: #8b949e; text-transform: uppercase; font-weight: bold; }
  .card .value { font-size: 24px; font-weight: bold; color: #58a6ff; margin-top: 6px; }
  .card .alert { color: #f85149; }
  table { width: 100%; border-collapse: collapse; margin-top: 12px; font-size: 14px; background: #161b22; border-radius: 8px; overflow: hidden; border: 1px solid #30363d; }
  th, td { padding: 12px 16px; text-align: left; border-bottom: 1px solid #30363d; }
  th { background: #21262d; color: #f0f6fc; }
  .badge { display: inline-block; padding: 2px 8px; border-radius: 12px; font-size: 11px; font-weight: bold; }
  .badge-crit { background: #da3633; color: #fff; }
  .badge-warn { background: #d29922; color: #000; }
  .badge-ok { background: #238636; color: #fff; }
  pre { background: #161b22; padding: 14px; border-radius: 6px; border: 1px solid #30363d; overflow-x: auto; font-size: 13px; }
</style>
</head>
<body>
<div class="container">
  <h1>CARRIER TELEMETRY & NETWORK INFRASTRUCTURE AUDIT</h1>
  <p><strong>Ziel-Knoten:</strong> 145.254.2.19 (Vodafone Core Backbone / AS3209) &bull; <strong>Region:</strong> Weserbergland / Bad Pyrmont &bull; <strong>Spezifikation:</strong> IETF RFC 8290 &bull; RFC 3168</p>

  <div class="grid">
    <div class="card">
      <div class="label">Verifizierte Messzyklen</div>
      <div class="value">$TOTAL</div>
    </div>
    <div class="card">
      <div class="label">Mittlere RTT (Baseline)</div>
      <div class="value">${AVG_RTT} ms</div>
    </div>
    <div class="card">
      <div class="label">Latenz-Spitze (Bufferbloat)</div>
      <div class="value alert">${MAX_RTT} ms</div>
    </div>
    <div class="card">
      <div class="label">Maximaler Tail-Drop</div>
      <div class="value alert">${MAX_DROP} %</div>
    </div>
  </div>

  <h2>INGENIEUR-DIAGNOSE & TECHNISCHE FORDERUNG</h2>
  <table>
    <tr><th>Parameter</th><th>Gemessener Ist-Zustand</th><th>IETF-Sollwert</th><th>Konsequenz / Behebung</th></tr>
    <tr><td>Queue Management</td><td>Unreguliertes Legacy-FIFO</td><td>Active Queue Management (RFC 8290)</td><td>Implementierung von FQ-CoDel / CAKE</td></tr>
    <tr><td>Überlast-Signalisierung</td><td>Keine (Tail-Drops bis zu ${MAX_DROP}%)</td><td>Explicit Congestion Notification (RFC 3168)</td><td>ECN-Markierung statt Paketverwerfung</td></tr>
    <tr><td>Latenz unter Last</td><td>Peak > ${MAX_RTT} ms</td><td>Latenz-Stabilitaet &le; 60 ms</td><td>Standort-Kapazitaetsausbau & Core-Upgrade</td></tr>
  </table>

  <h2>INFRASTRUKTUR- & STANDORT-DOSSIER</h2>
  <pre>Standortregion: Bad Pyrmont (Koordinatenkorridor Windmuehle / Hochflaeche)
Topografie: Erhoehte Hanglage mit exzellentem Funkfeldkorridor zur Versorgung von Randlagen.
Infrastruktur-Empfehlung: Errichtung eines zusaetzlichen 5G/LTE-Traegers zur Entlastung des Core-Aggregation-Hops 145.254.2.19.
Anbindung: Glasfaser-Zufuehrung oder E-Band-Richtfunk zur Vermeidung von Pufferstaus.</pre>
</div>
</body>
</html>
HTML

echo "Dashboard index.html erfolgreich generiert."
