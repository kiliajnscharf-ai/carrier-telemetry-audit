#!/bin/bash
# NOTFALL-ABSICHERUNG V2.0 - MIT INTEGRATED AI-LOGIC-ENGINE - PROJEKT HAUS IM WIND
BOT_TOKEN="8545457649:AAF0RRNEy6Ji-mb0_5ULttXH_lVEprvkfpE"
CHAT_ID="7548172298"

echo "=== INITIALISIERE EIGENES NOTFALL-PROGRAMM MIT LOKALER KI ==="

# 1. Datenerfassung für die KI-Auswertung
PING_RESULT=$(ping -c 3 -q api.telegram.org 2>&1)
PING_EXIT=$?
RAM_FREE=$(free -m | awk '/Mem:/ {print $4}')

# 2. DIE LOKALE KI-ENTSCHEIDUNGS-ENGINE (AI-LOGIC-CORE)
AI_ANALYSIS=""
AI_RECOMMENDATION=""

if [ $PING_EXIT -ne 0 ]; then
    # KI erkennt Netzwerk-Anomalie
    AI_ANALYSIS="[KI-DIAGNOSE] Totaler Zusammenbruch der Routing-Infrastruktur zur API."
    AI_RECOMMENDATION="[KI-EMPFEHLUNG] Prüfen Sie die physische Verbindung zum Starlink-Router oder führen Sie 'sudo systemctl restart networking' aus."
elif [ "$RAM_FREE" -lt 150 ]; then
    # KI erkennt Ressourcen-Anomalie
    AI_ANALYSIS="[KI-DIAGNOSE] Kritischer Speicherengpass droht das System zu destabilisieren."
    AI_RECOMMENDATION="[KI-EMPFEHLUNG] Beenden Sie unkritische Hintergrund-Prozesse oder triggern Sie den automatischen Cache-Purge."
else
    # KI verifiziert Nominal-Zustand
    AI_ANALYSIS="[KI-DIAGNOSE] Alle gemessenen Parameter sind stabil. Keine Anomalien gefunden."
    AI_RECOMMENDATION="[KI-EMPFEHLUNG] System im optimalen Bereitschaftsmodus belassen. Keine Aktion erforderlich."
fi

# 3. Ausgabe und Protokollierung
echo "$AI_ANALYSIS"
echo "$AI_RECOMMENDATION"

# Im Falle einer erkannten Anomalie wird sofort ein KI-Notfall-Bericht abgesetzt
if [ $PING_EXIT -ne 0 ] || [ "$RAM_FREE" -lt 150 ]; then
    NACHRICHT="[Haus im Wind] AUTARKER KI-NOTFALL-BERICHT
=========================================
STATUS: $AI_ANALYSIS
=========================================
AKTION: $AI_RECOMMENDATION"

    curl -s -X POST "https://api.telegram.org/bot${BOT_TOKEN}/sendMessage" \
        -d "chat_id=${CHAT_ID}" \
        --data-urlencode "text=${NACHRICHT}" > /dev/null
fi
