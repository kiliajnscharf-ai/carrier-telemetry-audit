#!/bin/bash
# ROBUSTER SOCKET-TESTER (NO-NETLINK) - PROJEKT HAUS IM WIND
echo "=== INITIALISIERE ROBUSTE NETZWERK-PRÜFUNG ==="

# Wir nutzen Port 8089 (Ausweichkanal)
TEST_PORT=8089
PORT_HEX=$(printf '%04X' $TEST_PORT)

# 1. Port-Prüfung über /proc/net/tcp (umgeht Netlink-Sperre)
if grep -q "00000000:${PORT_HEX}" /proc/net/tcp 2>/dev/null; then
    echo "[WARNUNG] Port $TEST_PORT ist im Container bereits belegt!"
else
    echo "[OK] Port $TEST_PORT ist frei und im Container verwendbar."
fi

# 2. Robuster Socket-Test mit Netcat
if command -v nc &> /dev/null; then
    echo "[INFO] Starte Socket-Test auf Port $TEST_PORT..."
    
    # Startet Netcat im Hintergrund und leitet Fehler um
    nc -lk -p $TEST_PORT > /dev/null 2>&1 &
    NC_PID=$!
    
    # Kurze Wartezeit für den Socket-Aufbau
    sleep 1
    
    # Verifikation über aktive PID und Prozessnamen
    if ps -p "$NC_PID" > /dev/null 2>&1; then
        echo "[OK] Netzwerk-Socket auf Port $TEST_PORT erfolgreich geöffnet (PID: $NC_PID)."
        kill "$NC_PID" 2>/dev/null
    else
        echo "[FEHLER] Socket-Öffnung fehlgeschlagen. Port blockiert oder fehlende Rechte."
    fi
else
    echo "[WARNUNG] 'netcat' (nc) ist nicht installiert."
fi

echo "============================================="
