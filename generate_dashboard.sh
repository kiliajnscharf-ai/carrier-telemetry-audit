#!/usr/bin/env bash
set -e

CSV="core_node_latency.csv"
OUT="index.html"

TOTAL=$(awk -F, 'NR>1 && $1 !~ /^#/ && $4 ~ /^[0-9.]+$/ {c++} END {print (c>0?c:0)}' "$CSV" 2>/dev/null || echo 0)
AVG_RTT=$(awk -F, 'NR>1 && $1 !~ /^#/ && $4 ~ /^[0-9.]+$/ {sum+=$4; c++} END {if(c>0) printf "%.2f", sum/c; else print "0"}' "$CSV" 2>/dev/null || echo 0)
MAX_RTT=$(awk -F, 'NR>1 && $1 !~ /^#/ && $4 ~ /^[0-9.]+$/ {if($4>max) max=$4} END {printf "%.2f", (max>0?max:0)}' "$CSV" 2>/dev/null || echo 0)
MAX_DROP=$(awk -F, 'NR>1 && $1 !~ /^#/ && $3 ~ /^[0-9.]+$/ {if($3>max) max=$3} END {printf "%.1f", (max>0?max:0)}' "$CSV" 2>/dev/null || echo 0)

cat << HTML > "$OUT"
<!DOCTYPE html>
<html lang="de">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Carrier Telemetry & Infrastructure Audit</title>
<style>
  body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, monospace; background: #0d1117; color: #c9d1d9; margin: 0; padding: 24px; line-height: 1.5; }
  .container { max-width: 1100px; margin: 0 auto; }
  h1 { color: #58a6ff; border-bottom: 1px solid #30363d; padding-bottom: 12px; font-size: 24px; }
  h2 { color: #f0f6fc; margin-top: 28px; font-size: 18px; border-bottom: 1px solid #21262d; padding-bottom: 6px; }
  .grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 16px; margin: 20px 0; }
  .card { background: #161b22; border: 1px solid #30363d; border-radius: 8px; padding: 16px; }
  .card .label { font-size: 11px; color: #8b949e; text-transform: uppercase; font-weight: bold; }
  .card .value { font-size: 22px; font-weight: bold; color: #58a6ff; margin-top: 6px; }
  .card .alert { color: #f85149; }
  table { width: 100%; border-collapse: collapse; margin-top: 12px; font-size: 13px; background: #161b22; border-radius: 8px; overflow: hidden; border: 1px solid #30363d; }
  th, td { padding: 10px 14px; text-align: left; border-bottom: 1px solid #30363d; }
  th { background: #21262d; color: #f0f6fc; }
  pre { background: #161b22; padding: 14px; border-radius: 6px; border: 1px solid #30363d; overflow-x: auto; font-size: 13px; color: #79c0ff; }
</style>
</head>
<body>
<div class="container">
  <h1>CARRIER TELEMETRY & INFRASTRUCTURE AUDIT</h1>
  <p><strong>Zielknoten:</strong> 145.254.2.19 (Vodafone AS3209) &bull; <strong>Region:</strong> Bad Pyrmont &bull; <strong>Standards:</strong> RFC 8290 / RFC 3168</p>

  <div class="grid">
    <div class="card"><div class="label">Messzyklen</div><div class="value">$TOTAL</div></div>
    <div class="card"><div class="label">Mittlere RTT</div><div class="value">${AVG_RTT} ms</div></div>
    <div class="card"><div class="label">Peak-Latenz</div><div class="value alert">${MAX_RTT} ms</div></div>
    <div class="card"><div class="label">Max. Tail-Drop</div><div class="value alert">${MAX_DROP} %</div></div>
  </div>

  <h2>VANTAGE TOWERS STANDORT- & INFRASTRUKTUR-SPEZIFIKATION</h2>
  <table>
    <tr><th>Parameter</th><th>Vantage Towers Standard</th><th>Projektierung Bad Pyrmont</th></tr>
    <tr><td>Bauwerkstyp</td><td>Standard-Gittermast (SGM 35) / Schleuderbeton</td><td>Freistehend, 30 m bis 35 m ueber Grund</td></tr>
    <tr><td>Fundamentierung</td><td>Flach- oder Tiefgruendung (~25 m²)</td><td>Minimale Versiegelung, Windlastzone 2</td></tr>
    <tr><td>Sektorisierung</td><td>3 Sektoren (120°-Teilung)</td><td>Volle Abdeckung Topografie / Hanglage</td></tr>
    <tr><td>Backhaul / Anbindung</td><td>10 Gbit/s E-Band-Richtfunk / Dark Fiber</td><td>Entlastung des Core-Hops 145.254.2.19</td></tr>
    <tr><td>AQM-Vorgabe</td><td>RFC 8290 (FQ-CoDel / CAKE)</td><td>Beseitigung unregulierter FIFO-Pufferstaus</td></tr>
  </table>

  <h2>STANDORTPROFIL (SITE CANDIDATE DOSSIER)</h2>
  <pre>Region: Bad Pyrmont (Weserbergland)
Eignung: Makrozellen-Standort zur Schliessung von Kapazitaetsluecken
Kandidatentyp: Greenfield / Rooftop Tower
Kollokationsfaehigkeit: Multi-Operator-Ready (Vodafone, Deutsche Telekom, O2 Telefónica, 1&1)</pre>
</div>
</body>
</html>
HTML

chmod +x generate_dashboard.sh
./generate_dashboard.sh

git add index.html generate_dashboard.sh
git commit -m "Add Vantage Towers structural engineering specs to audit dashboard"
git push origin main
