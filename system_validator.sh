#!/bin/bash
# AUTARKER MASTER-VALIDIERER - PROJEKT HAUS IM WIND
echo "=== SYSTEM-INTEGRITÄTS-PRÜFUNG (PLATZ 1) ==="

# 1. Prüfung der Kernel-Echtzeitfähigkeit
if uname -v | grep -q "PREEMPT_RT"; then
    echo "[OK] Kernel-Typ: Echtzeit-Härtung (PREEMPT_RT) aktiv."
else
    echo "[WARNUNG] Kernel-Typ: Standard-Kernel. Für absolute Latenzfreiheit wird PREEMPT_RT empfohlen."
fi

# 2. CPU-Governor Überprüfung
if [ -f /sys/devices/system/cpu/cpu0/cpufreq/scaling_governor ]; then
    GOVERNOR=$(cat /sys/devices/system/cpu/cpu0/cpufreq/scaling_governor)
    if [ "$GOVERNOR" = "performance" ]; then
        echo "[OK] CPU-Governor: performance (maximale Taktstabilität)."
    else
        echo "[WARNUNG] CPU-Governor steht auf '$GOVERNOR'. Für Echtzeit-Streaming auf 'performance' setzen."
    fi
else
    echo "[INFO] CPU-Governor-Schnittstelle nicht direkt zugänglich (virtuelle Umgebung?)."
fi

# 3. Speicher-Verfügbarkeit & Swappiness-Prüfung
SWAP_VAL=$(sysctl -n vm.swappiness 2>/dev/null)
if [ -n "$SWAP_VAL" ]; then
    if [ "$SWAP_VAL" -le 10 ]; then
        echo "[OK] Speicher-Einstellung: vm.swappiness ist optimal eingestellt ($SWAP_VAL)."
    else
        echo "[WARNUNG] vm.swappiness steht auf $SWAP_VAL. Empfohlen wird ein Wert <= 10 zur Vermeidung von Page-Fault-Latenzen."
    fi
fi

echo "============================================="
