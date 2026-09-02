#!/bin/bash
# ABSOLUTE HARDWARE-KONTROLLE - PROJEKT HAUS IM WIND
echo "=== SYSTEM-GOVERNOR DIREKTSCHREIBEN (ROOT) ==="

# Prüfung auf echte Root-Rechte vor Ausführung
if [ "$EUID" -ne 0 ]; then
  echo "[FEHLER] Dieses Skript MUSS direkt mit sudo oder als root ausgeführt werden!"
  echo "Bitte starten mit: sudo bash fix_governor_root.sh"
  exit 1
fi

for g in /sys/devices/system/cpu/cpu*/cpufreq/scaling_governor; do
    if [ -f "$g" ]; then
        echo "performance" > "$g"
        # Verifikation des geschriebenen Wertes
        AKTUELL=$(cat "$g")
        if [ "$AKTUELL" = "performance" ]; then
            echo "[OK] $g erfolgreich auf: $AKTUELL"
        else
            echo "[FEHLER] Schreiben fehlgeschlagen auf $g (Wert ist: $AKTUELL)"
        fi
    else
        echo "[INFO] Keine Schnittstelle unter $g"
    fi
done
echo "============================================="
