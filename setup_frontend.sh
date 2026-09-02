#!/bin/bash
# FRONTEND GENERATOR - TITANSTREAM APP - PROJEKT HAUS IM WIND
echo "=== GENERIERE WEB-FRONTEND ==="

cat << 'HTML' > titanstream/web_app/index.html
<!DOCTYPE html>
<html lang="de">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Titanstream - System-Integrität (Platz 1)</title>
    <style>
        body {
            font-family: 'Courier New', Courier, monospace;
            background-color: #0d1117;
            color: #c9d1d9;
            padding: 20px;
        }
        .container {
            max-width: 800px;
            margin: 0 auto;
            border: 1px solid #30363d;
            border-radius: 6px;
            padding: 20px;
            background-color: #161b22;
        }
        h1 {
            color: #58a6ff;
            border-bottom: 1px solid #30363d;
            padding-bottom: 10px;
        }
        .status-box {
            background-color: #21262d;
            border: 1px solid #30363d;
            padding: 15px;
            border-radius: 4px;
            margin-bottom: 20px;
        }
        .status-ok {
            color: #3fb950;
            font-weight: bold;
        }
        .btn {
            background-color: #238636;
            color: white;
            border: 1px solid rgba(240,246,252,0.1);
            padding: 10px 20px;
            border-radius: 6px;
            cursor: pointer;
            font-weight: bold;
        }
        .btn:hover {
            background-color: #2ea043;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>TITANSTREAM CONTROL INTERFACE</h1>
        <div class="status-box">
            <p>System-Status: <span class="status-ok">AKTIV (Port 8089)</span></p>
            <p>Puffer-Kompensation: <strong>Aktiviert (Adaptive Ring-Buffer 64MB)</strong></p>
        </div>
        <button class="btn" onclick="checkStream()">Stream-Integrität prüfen</button>
        <div id="output" style="margin-top: 20px; white-space: pre-wrap;"></div>
    </div>

    <script>
        function checkStream() {
            const output = document.getElementById('output');
            output.innerText = "Sende Anfrage an API (127.0.0.1:8089)...";
            
            fetch('http://127.0.0.1:8089/status')
                .then(response => response.json())
                .then(data => {
                    output.innerText = JSON.stringify(data, null, 2);
                })
                .catch(error => {
                    output.innerText = "Fehler: Verbindung zum lokalen Backend auf Port 8089 fehlgeschlagen.\nStellen Sie sicher, dass 'stream_validator.sh' im Hintergrund läuft.";
                });
        }
    </script>
</body>
</html>
HTML

if [ -f "titanstream/web_app/index.html" ]; then
    echo "[OK] index.html erfolgreich für Spck Editor und lokalen Browser generiert."
else
    echo "[FEHLER] Erstellung des Web-Frontends fehlgeschlagen."
fi

echo "=============================="
