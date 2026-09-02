#!/bin/bash

# --- KONFIGURATION ---
URL="https://www.beispiel-shop.de/wd-red-pro-22tb"
PROXY="localhost:9050"
LOG_FILE="$HOME/wd_red_pro_prices.csv"

# --- USER-AGENT ROTATION (ARRAY) ---
AGENTS=(
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4 Mobile/15E148 Safari/604.1"
    "Mozilla/5.0 (Linux; Android 14; Pixel 8 Pro) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.6261.119 Mobile Safari/537.36"
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:123.0) Gecko/20100101 Firefox/123.0"
)
SELECTED_UA=${AGENTS[$RANDOM % ${#AGENTS[@]}]}

# --- TOR-REFRESH (NEUE IP ERZWINGEN) ---
echo "LOGIK: ERZWINGE NEUE TOR-IDENTITÄT..."
(echo 'AUTHENTICATE ""'; echo 'SIGNAL NEWNYM'; echo 'QUIT') | nc localhost 9051 2>/dev/null

# --- DATEN-ABFRAGE ---
echo "LOGIK: NUTZE AGENT: $SELECTED_UA"
HTML_CONTENT=$(curl --socks5-hostname $PROXY -A "$SELECTED_UA" -L -s "$URL")
echo "$HTML_CONTENT" > ~/last_attempt.html

# --- KASKADEN-PARSING ---
RAW_PRICE=$(echo "$HTML_CONTENT" | grep -o '"price":[^,]*' | grep -oP '[0-9.]+' | head -n 1)

if [[ -z "$RAW_PRICE" ]]; then
    RAW_PRICE=$(echo "$HTML_CONTENT" | grep -oP 'itemprop="price" content="\K[0-9.]+' | head -n 1)
fi

# --- FINALE AUSWERTUNG ---
TIMESTAMP=$(date '+%Y-%m-%d %H:%M')
if [[ -n "$RAW_PRICE" ]]; then
    echo "$TIMESTAMP;WD_RED_PRO_22TB;$RAW_PRICE" >> "$LOG_FILE"
    echo "ERFOLG: PREIS $RAW_PRICE ERFASST (PLATZ 1)."
else
    echo "$TIMESTAMP;ERROR;BLOCK_ODER_MUSTER_FEHLT" >> "$LOG_FILE"
    echo "FEHLER: DATEN KONNTEN NICHT EXTRAHIERT WERDEN. PRÜFE ~/last_attempt.html"
fi
