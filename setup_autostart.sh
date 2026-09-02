#!/bin/bash
# AUTOSTART INTEGRATOR - TITANSTREAM APP - PROJEKT HAUS IM WIND
echo "=== INITIERE AUTOSTART-INTEGRATION ==="

BASHRC="$HOME/.bashrc"
AUTOSTART_LINE="bash \$HOME/titanstream/web_app/control.sh start > /dev/null 2>&1"

# 1. Prüfung, ob der Autostart-Eintrag bereits existiert
if grep -q "titanstream/web_app/control.sh start" "$BASHRC" 2>/dev/null; then
    echo "[INFO] Autostart-Eintrag ist bereits in $BASHRC vorhanden."
else
    # 2. Eintrag am Ende der .bashrc anfügen
    echo -e "\n# Titanstream App Autostart - Projekt Haus im Wind\n$AUTOSTART_LINE" >> "$BASHRC"
    echo "[OK] Autostart-Eintrag erfolgreich in $BASHRC integriert."
fi

echo "======================================"
