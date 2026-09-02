#!/bin/bash
# SYSTEM-KORREKTUR-SKRIPT - PROJEKT HAUS IM WIND
echo "=== SYSTEM-KORREKTUR INITIERT ==="

# 1. CPU-Governor auf Performance setzen (erfordert sudo)
echo "Setze CPU-Governor auf 'performance'..."
if [ -f /sys/devices/system/cpu/cpu0/cpufreq/scaling_governor ]; then
    sudo sh -c 'for g in /sys/devices/system/cpu/cpu*/cpufreq/scaling_governor; do echo performance > "$g"; done'
    echo "[OK] Alle CPU-Kerne auf maximale Leistung (performance) konfiguriert."
else
    echo "[INFO] cpufreq-Schnittstelle nicht verfügbar. Bitte prüfen Sie, ob TLP oder cpufrequtils installiert sind."
fi

# 2. Empfehlung/Installation RT-Kernel (Debian/Ubuntu-basiert)
echo "Prüfe Paketquellen für Realtime-Kernel..."
if [ -f /etc/debian_version ]; then
    echo "[INFO] Debian/Ubuntu-System erkannt. Installationsbefehl vorbereitet:"
    echo "       -> sudo apt-get update && sudo apt-get install -y linux-image-rt-amd64"
else
    echo "[INFO] Anderes Linux-Derivat erkannt. Bitte installieren Sie das entsprechende PREEMPT_RT-Paket Ihrer Distribution."
fi

echo "================================="
