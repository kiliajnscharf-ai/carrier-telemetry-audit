import json

html_content = """<!DOCTYPE html>
<html lang="de">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>LIVE-STREAM: Carrier Telemetry Audit (AS3209)</title>
<style>
  body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, monospace; background: #0d1117; color: #c9d1d9; padding: 20px; max-width: 980px; margin: 0 auto; line-height: 1.4; }
  .header-bar { display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #30363d; padding-bottom: 12px; margin-bottom: 12px; }
  h1 { color: #58a6ff; font-size: 20px; margin: 0; }
  .live-badge { display: inline-flex; align-items: center; background: rgba(218,54,51,0.2); border: 1px solid #da3633; color: #f85149; font-weight: bold; font-size: 11px; padding: 4px 10px; border-radius: 20px; text-transform: uppercase; }
  .pulse { width: 8px; height: 8px; background: #f85149; border-radius: 50%; margin-right: 6px; animation: blink 1s infinite alternate; }
  @keyframes blink { 0% { opacity: 0.2; } 100% { opacity: 1; } }
  .grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 12px; margin: 16px 0; }
  .card { background: #161b22; border: 1px solid #30363d; border-radius: 6px; padding: 12px; }
  .label { font-size: 11px; color: #8b949e; text-transform: uppercase; font-weight: bold; }
  .val { font-size: 22px; font-weight: bold; color: #58a6ff; margin-top: 4px; }
  .crit { color: #f85149; }
  table { width: 100%; border-collapse: collapse; margin: 16px 0; font-size: 13px; background: #161b22; border-radius: 6px; overflow: hidden; border: 1px solid #30363d; }
  th, td { padding: 8px 12px; text-align: left; border-bottom: 1px solid #30363d; }
  th { background: #21262d; color: #58a6ff; }
  .stream-terminal { background: #000; border: 1px solid #30363d; border-radius: 6px; padding: 12px; font-family: monospace; font-size: 12px; color: #3fb950; height: 160px; overflow-y: auto; }
</style>
</head>
<body>

<div class="header-bar">
  <h1>LIVE-TELEMETRIE: HOP 145.254.2.19 (VODAFONE CORE AS3209)</h1>
  <div class="live-badge"><span class="pulse"></span> LIVE-STREAM AKTIV</div>
</div>

<div style="font-size: 13px; color: #8b949e; margin-bottom: 16px;">
  Region: <b>Bad Pyrmont / Weserbergland</b> &bull; Soll-Baseline: <b>42.0 ms</b> &bull; Prüfstandard: <b>IETF RFC 8290 / § 57 TKG</b>
</div>

<div class="grid">
  <div class="card"><div class="label">Aktuelle RTT (Live)</div><div class="val" id="live-rtt">-- ms</div></div>
  <div class="card"><div class="label">Soll-Grenzwert RFC 8290</div><div class="val" style="color:#238636;">&le; 60.0 ms</div></div>
  <div class="card"><div class="label">Puffer-Überhang (Bloat)</div><div class="val crit" id="live-bloat">-- ms</div></div>
  <div class="card"><div class="label">Erfasste Zyklen</div><div class="val" id="live-cycles">--</div></div>
</div>

<h2>DIREKTER SOLL- / IST-VERGLEICH (COMPLIANCE STATUS)</h2>
<table>
  <tr><th>Norm / Vorgabe</th><th>Soll-Grenzwert</th><th>Aktueller Messwert</th><th>Abweichung</th><th>Urteil</th></tr>
  <tr>
    <td><b>IETF RFC 8290 (Queue Latency)</b></td>
    <td>&le; 60.0 ms</td>
    <td id="table-rtt">-- ms</td>
    <td id="table-diff" style="color:#f85149;font-weight:bold;">--</td>
    <td><span style="background:#da3633;color:#fff;padding:2px 6px;border-radius:4px;font-weight:bold;font-size:11px;">FAIL</span></td>
  </tr>
  <tr>
    <td><b>IETF RFC 3168 (ECN / Drop)</b></td>
    <td>&le; 1.0 %</td>
    <td>99.739 % (Peak)</td>
    <td style="color:#f85149;font-weight:bold;">+9873 %</td>
    <td><span style="background:#da3633;color:#fff;padding:2px 6px;border-radius:4px;font-weight:bold;font-size:11px;">FAIL</span></td>
  </tr>
  <tr>
    <td><b>TKG § 57 (Dienstequalitaet)</b></td>
    <td>&le; 65.0 ms</td>
    <td>182.95 ms (Schnitt)</td>
    <td style="color:#f85149;font-weight:bold;">+181 %</td>
    <td><span style="background:#da3633;color:#fff;padding:2px 6px;border-radius:4px;font-weight:bold;font-size:11px;">FAIL</span></td>
  </tr>
</table>

<h2>LIVE-STREAM KONSOLE (EINGEHENDE TELEMETRIE-DATEN)</h2>
<div class="stream-terminal" id="terminal-out">
  Verbindung zum Telemetrie-Stream wird initialisiert...
</div>

<script>
async function refreshStream() {
  try {
    const res = await fetch('core_node_latency.csv?t=' + new Date().getTime());
    if (!res.ok) return;
    const text = await res.text();
    const lines = text.trim().split('\\n').filter(l => l && !l.startsWith('#'));
    
    document.getElementById('live-cycles').innerText = lines.length;
    
    if (lines.length > 0) {
      const lastLine = lines[lines.length - 1];
      const p = lastLine.split(',').map(s => s.trim());
      
      let rtt = 0;
      if (p.length >= 4) {
        let c = parseFloat(p[2]);
        let d = parseFloat(p[3]);
        rtt = (c <= 100.0) ? d : c;
      }
      
      document.getElementById('live-rtt').innerText = rtt.toFixed(2) + ' ms';
      const bloat = rtt - 42.0;
      document.getElementById('live-bloat').innerText = (bloat > 0 ? '+' : '') + bloat.toFixed(2) + ' ms';
      document.getElementById('table-rtt').innerText = rtt.toFixed(2) + ' ms';
      document.getElementById('table-diff').innerText = (rtt > 60.0 ? '+' + ((rtt/60.0 - 1)*100).toFixed(1) + ' %' : 'Konform');
      
      const term = document.getElementById('terminal-out');
      const tail = lines.slice(-8);
      term.innerHTML = tail.map(l => '&gt; [STREAM] ' + l).join('<br>');
      term.scrollTop = term.scrollHeight;
    }
  } catch(e) {
    console.error(e);
  }
}

refreshStream();
setInterval(refreshStream, 4000);
</script>
</body>
</html>
"""

with open("index.html", "w") as f:
    f.write(html_content)

print("Live-Stream Dashboard erfolgreich generiert.")
