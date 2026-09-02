#!/bin/bash
# ROBUSTE CPU-STEUERUNG - PROJEKT HAUS IM WIND
echo "=== KORRIGIERTE GOVERNOR-ANPASSUNG ==="

# Sichere Ausführung ohne komplexe Schachtelung
for g in /sys/devices/system/cpu/cpu*/cpufreq/scaling_governor; do
    if [ -f "$g" ]; then
        echo "performance" | sudo tee "$g" > /dev/null
        echo "[OK] $g -> performance"
    else
        echo "[INFO] Keine direkte CPU-Schnittstelle unter $g gefunden."
    fi
done

echo "======================================="
