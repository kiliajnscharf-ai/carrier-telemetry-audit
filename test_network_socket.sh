#!/bin/bash
# NETWORK TESTER - TITANSTREAM APP - PROJEKT HAUS IM WIND
echo "=== INITIALISIERE NETZWERK-SOCKET-PRÜFUNG ==="

TEST_PORT=8080

# 1. Prüfung, ob Port 8080 bereits belegt ist
if command -v ss &> /dev/null; then
    PORT_CHECK=$(ss -tulpn | grep ":$TEST_PORT ")
elif command -v netstat &> /dev/null; then
    PORT_CHECK=$(netstat -an | grep ":$TEST_PORT ")
else
    PORT_CHECK=""
fi

if [ -n "$PORT_CHECK" ]; then
    echo "[WARNUNG] Port $TEST_PORT wird bereits verwendet. Ein Ausweichport muss definiert werden."
else
    echo "[OK] Ziel-Port $TEST_PORT ist frei und für den User-Space verfügbar."
fi

# 2. Simulation eines Socket-Lauschvorgangs mit Netcat (nc)
if command -v nc &> /dev/null; then
    echo "[INFO] Starte transienten Socket-Test auf Port $TEST_PORT für 5 Sekunden..."
    ( nc -lk -p $TEST_PORT & )
    NC_PID=$!
    sleep 2
    if ps -p $NC_PID > /dev/null; then
        echo "[OK] Netzwerk-Socket erfolgreich im User-Space geöffnet."
        kill $NC_PID &> /dev/null
    else
        echo "[FEHLER] Socket-Öffnung fehlgeschlagen."
    fi
else
    echo "[WARNUNG] 'netcat' (nc) ist nicht installiert. Installation empfohlen zur Socket-Diagnose:"
    echo "          -> sudo apt-get install -y netcat-openbsd"
fi

echo "============================================="
