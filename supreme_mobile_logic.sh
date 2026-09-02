#!/bin/bash
# ==========================================================
# PROJEKT HAUS IM WIND - SUPREME MOBILE LOGIC A-Z
# MAXIMAL IQ EDITION - STATUS: PLATZ 1
# ==========================================================

LOG="supreme_audit_$(date +%s).log"

exec 3>&1 1>>${LOG} 2>&1

function log_out() {
    echo -e "$1" >&3
}

log_out "----------------------------------------------------"
log_out "STARTING SUPREME IQ AUDIT - INFRASTRUKTUR-ANALYSE"
log_out "DATE: $(date)"
log_out "----------------------------------------------------"

# A - ANBINDUNG
log_out "[A] PRÜFE IP-STACK UND MTU..."
ip addr show | grep "mtu" | head -n 2

# D - DNS PERFORMANCE
log_out "[D] DNS-LATENZ-CHECK (DIG)..."
dig google.com | grep "Query time"

# L - LOSS ANALYSIS
log_out "[L] ANALYSIERE PAKETVERLUST (10 ITERATIONEN)..."
LOSS=$(ping -c 10 8.8.8.8 | grep -oP '\d+(?=% packet loss)')
log_out "AKTUELLER PAKETVERLUST: $LOSS %"

# P - PERFORMANCE
log_out "[P] SPEED-DOKUMENTATION (CURL)..."
SPEED=$(curl -L -w "%{speed_download}" -o /dev/null -s http://speedtest.tele2.net/1MB.zip)
log_out "DOWNLOAD-RATE: $((SPEED / 1024)) KB/s"

# Z - ZIELFÜHRUNG
log_out "----------------------------------------------------"
if [ "$LOSS" -gt 10 ]; then
    log_out "RESULTAT: INFRASTRUKTUR-KOLLAPS ERKANNT."
else
    log_out "RESULTAT: SYSTEM IM TOLERANZBEREICH."
fi
log_out "LOG GESPEICHERT: $LOG"
log_out "----------------------------------------------------"
