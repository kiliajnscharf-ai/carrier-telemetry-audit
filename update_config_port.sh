#!/bin/bash
# PORT UPDATER - TITANSTREAM APP - PROJEKT HAUS IM WIND
echo "=== PORT-AKTUALISIERUNG INITIERT ==="

CONFIG_FILE="titanstream/web_app/config/stream_config.json"

if [ -f "$CONFIG_FILE" ]; then
    # Ersetzen des Standard-Konfigurations-Templates durch den verifizierten Port 8089
    # Sowie Anpassung des Sockets für die Container-Umgebung
    cat << 'CONF' > "$CONFIG_FILE"
{
  "system_environment": "virtualized_container",
  "buffering": {
    "initial_delay_ms": 1500,
    "ring_buffer_size_mb": 64,
    "adaptive_puffer_compensation": true,
    "low_latency_mode": false
  },
  "network": {
    "bind_address": "127.0.0.1",
    "port": 8089,
    "socket_receive_buffer_bytes": 1048576,
    "keep_alive_timeout_ms": 5000,
    "max_reconnect_attempts": 10
  },
  "logging": {
    "log_level": "WARNING",
    "destination": "titanstream/web_app/logs/stream_integrity.log"
  }
}
CONF
    echo "[OK] Port 8089 wurde erfolgreich in der stream_config.json festgeschrieben."
else
    echo "[FEHLER] Konfigurationsdatei unter $CONFIG_FILE nicht gefunden!"
fi

echo "===================================="
