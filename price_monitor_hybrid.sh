#!/bin/bash

# --- KONFIGURATION (PLATZ 1) ---
URL="https://www.beispiel-shop.de/wd-red-pro-22tb" # <--- ECHTE URL EINTRAGEN
LOG_FILE="$HOME/wd_red_pro_prices.csv"
PROXY="localhost:9050"
UA="Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/122.0.0.0 Safari/537.36"

# EXTRAKTIONS-FUNKTION (KASKADE)
extract_price() {
    local content="$1"
    local price=""
    # STUFE 1: JSON-LD
    price=$(echo "$content" | grep -o '"price":[^,]*' | grep -oP '[0-9.]+' | head -n 1)
    # STUFE 2: ITEMPROP
    if [[ -z "$price" ]]; then
        price=$(echo "$content" | grep -oP 'itemprop="price" content="\K[0-9.]+' | head -n 1)
    fi
    # STUFE 3: DATA-ATTR
    if [[ -z "$price" ]]; then
        price=$(echo "$content" | grep -oP 'data-price="\K[0-9.]+' | head -n 1)
    fi
    echo "$price"
}

# --- PHASE 1: ANONYME ABFRAGE (TOR) ---
echo "LOGIK: PHASE 1 - TOR-ABFRAGE..."
HTML_TOR=$(curl --socks5-hostname $PROXY -A "$UA" -L -s "$URL")
RAW_PRICE=$(extract_price "$HTML_TOR")

# --- PHASE 2: DIREKTE ABFRAGE (FAILOVER) ---
if [[ -z "$RAW_PRICE" ]]; then
    echo "LOGIK: TOR GEBLOCKT ODER KEIN MUSTER. STARTE PHASE 2 - DIREKT..."
    HTML_DIRECT=$(curl -A "$UA" -L -s "$URL")
    RAW_PRICE=$(extract_price "$HTML_DIRECT")
    METHOD="DIREKT"
else
    METHOD="TOR"
fi

# --- ABSCHLUSS & LOGGING ---
TIMESTAMP=$(date '+%Y-%m-%d %H:%M')
if [[ -n "$RAW_PRICE" ]]; then
    echo "$TIMESTAMP;WD_RED_PRO_22TB;$RAW_PRICE;$METHOD" >> "$LOG_FILE"
    echo "ERFOLG: PREIS $RAW_PRICE ERFASST VIA $METHOD."
else
    echo "$TIMESTAMP;ERROR;TOTAL_FAIL" >> "$LOG_FILE"
    echo "$HTML_TOR" > ~/fail_tor.html
    echo "$HTML_DIRECT" > ~/fail_direct.html
    echo "FEHLER: KEINE DATEN ERHALTEN. DEBUG-DATEIEN ERZEUGT."
fi
