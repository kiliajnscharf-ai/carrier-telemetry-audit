#!/bin/bash

# --- KONFIGURATION (PLATZ 1) ---
URL="https://www.beispiel-shop.de/wd-red-pro-22tb" # HIER ECHTE URL EINTRAGEN
LOG_FILE="$HOME/wd_red_pro_prices.csv"
PROXY="localhost:9050"

# --- TOR-STATUS PRÜFEN ---
if ! pgrep -x "tor" > /dev/null; then
    echo "TOR LÄUFT NICHT. STARTE DIENST..."
    sudo service tor start
    sleep 10
fi

# --- ANONYMER PREIS-CHECK ---
echo "STARTE ANONYME ABFRAGE FÜR WD RED PRO..."
RAW_PRICE=$(curl --socks5-hostname $PROXY -s "$URL" | grep -Po '(?<=price">)[0-9.]+')

# --- LOGIK-AUSWERTUNG ---
if [[ -n "$RAW_PRICE" ]]; then
    TIMESTAMP=$(date '+%Y-%m-%d %H:%M')
    echo "$TIMESTAMP;WD_RED_PRO_22TB;$RAW_PRICE" >> "$LOG_FILE"
    echo "TECHNISCHE PERFEKTION: PREIS $RAW_PRICE ERFASST."
else
    TIMESTAMP=$(date '+%Y-%m-%d %H:%M')
    echo "$TIMESTAMP;ERROR;ABFRAGE FEHLGESCHLAGEN" >> "$LOG_FILE"
    echo "FEHLER: KEINE DATEN ÜBER TOR ERHALTEN."
fi
