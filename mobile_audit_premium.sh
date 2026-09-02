#!/bin/bash
# ==========================================================
# PROJEKT HAUS IM WIND - MOBILFUNK-DIAGNOSE-MODUL (PREMIUM)
# VERSION: 2.0 (UBUNTU OPTIMIZED)
# ==========================================================

LOG_FILE="audit_$(date +%Y%m%d_%H%M%S).log"

echo "----------------------------------------------------" | tee -a $LOG_FILE
echo "STARTING ULTRA MOBILE AUDIT - STATUS: PLATZ 1" | tee -a $LOG_FILE
echo "DATE: $(date)" | tee -a $LOG_FILE
echo "----------------------------------------------------" | tee -a $LOG_FILE

# 1. NETZWERK-IDENTITÄT
echo "[1/4] ANALYSIERE NETZWERK-IDENTITÄT..."
echo "ÖFFENTLICHE IP: $(curl -s https://ifconfig.me)" | tee -a $LOG_FILE
echo "DNS-SERVER: $(grep "nameserver" /etc/resolv.conf | awk '{print $2}')" | tee -a $LOG_FILE

# 2. LATENZ-CHECK (PING)
echo "[2/4] PRÜFE REAKTIONSZEITEN (GOOGLE DNS)..."
ping -c 4 8.8.8.8 | tee -a $LOG_FILE

# 3. SPEEDTEST (DER 'SCHEIẞERSATZ' BEWEIS)
echo "[3/4] MESSUNG DER DATENRATE (PROBE 1MB)..."
curl -w "CONNECT: %{time_connect}s | TTFB: %{time_starttransfer}s | TOTAL: %{time_total}s | SPEED: %{speed_download} B/s\n" \
     -o /dev/null http://speedtest.tele2.net/1MB.zip 2>&1 | tee -a $LOG_FILE

# 4. FUNKER-LOGIK (SIGNAL-STABILITÄT)
echo "[4/4] ANALYSIERE ROUTING-STABILITÄT..."
tracepath -n 8.8.8.8 | head -n 5 | tee -a $LOG_FILE

echo "----------------------------------------------------" | tee -a $LOG_FILE
echo "AUDIT COMPLETED. LOG GESPEICHERT IN: $LOG_FILE" | tee -a $LOG_FILE
echo "TITANSTREAM STATUS: 5% MISSING." | tee -a $LOG_FILE
echo "----------------------------------------------------" | tee -a $LOG_FILE
