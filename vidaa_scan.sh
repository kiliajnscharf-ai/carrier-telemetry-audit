#!/bin/bash
# ZIEL-IP DEFINIEREN
TV_IP="10.55.127.240"

echo "=== STARTE SPEZIFISCHEN VIDAA OS PORT-SCAN ==="
echo "Analysiere System-Schnittstellen für IP: $TV_IP..."

# PRÜFUNG DER RELEVANTEN VIDAA-PORTS
for port in 80 8008 8080 9080 9999; do
    echo -n "Prüfe Port $port... "
    if nc -z -w 2 "$TV_IP" "$port" 2>/dev/null; then
        echo "[GEÖFFNET] - Schnittstelle reagiert."
    else
        echo "[GESCHLOSSEN]"
    fi
done
echo "============================================="
