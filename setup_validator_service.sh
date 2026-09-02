#!/bin/bash
# SERVICE GENERATOR - TITANSTREAM APP - PROJEKT HAUS IM WIND
echo "=== GENERIERE STREAM-VALIDIERUNGS-DIENST ==="

cat << 'SERVICE' > titanstream/web_app/stream_validator.sh
#!/bin/bash
# TITANSTREAM - RUNTIME VALIDATOR & BUFFER CONTROL

CONFIG_FILE="titanstream/web_app/config/stream_config.json"
LOG_FILE="titanstream/web_app/logs/stream_integrity.log"

# Auslesen der Puffer-Konfiguration (Simulierte JSON-Parsung im Bash-User-Space)
BUFFER_SIZE=$(grep -o '"ring_buffer_size_mb": [0-9]*' "$CONFIG_FILE" | awk '{print $2}')
INITIAL_DELAY=$(grep -o '"initial_delay_ms": [0-9]*' "$CONFIG_FILE" | awk '{print $2}')

echo "[$(date '+%Y-%m-%d %H:%M:%S')] Starte Titanstream Validierung mit ${BUFFER_SIZE}MB Ringpuffer..." >> "$LOG_FILE"
echo "Titanstream-Dienst aktiv (Initialer Puffer-Delay: ${INITIAL_DELAY}ms)"

# Simulierte adaptive Puffer-Regelung
LPT=0 # Letzte Paket-Laufzeit (ms)
while true; do
    # Generierung einer simulierten Netzwerk-Latenz (0 bis 100ms)
    LATENCY=$(( RANDOM % 100 ))
    
    # Adaptive Puffer-Berechnung
    if [ "$LATENCY" -gt 80 ]; then
         echo "[WARNUNG] Erhöhte Netzwerklatenz detektiert: ${LATENCY}ms. Puffer wird vergrößert." >> "$LOG_FILE"
    fi
    
    sleep 2
done
SERVICE

chmod +x titanstream/web_app/stream_validator.sh

if [ -f "titanstream/web_app/stream_validator.sh" ]; then
    echo "[OK] stream_validator.sh erfolgreich generiert und ausführbar gemacht."
else
    echo "[FEHLER] Erstellung des Dienstes fehlgeschlagen."
fi

echo "============================================"
