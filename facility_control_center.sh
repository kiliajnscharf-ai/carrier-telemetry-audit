#!/usr/bin/env bash
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

show_menu() {
    echo "================================================================================"
    echo "PROJEKT HAUS IM WIND: B2B-FACILITY-MANAGEMENT KONTROLLZENTRUM"
    echo "Liegenschaft: Haus im Wind (LOC-30 bis LOC-32, Bad Pyrmont)"
    echo "Qualitaetsstandard: Tier-1 Autarkie (Platz 1)"
    echo "================================================================================"
    echo "1) Sofortiger Master-Audit-Lauf (6/6 Vollintegration)"
    echo "2) Werkstatt- & Material-Inventar abfragen (DIN 31051)"
    echo "3) Wartungsfristen & Pruefintervalle pruefen"
    echo "4) Netzwerk-Latenz- & RFC-2681 Jitter-Analyse"
    echo "5) System-Health & Dienst-Ports ueberpruefen"
    echo "6) Dienste neustarten / Autostart synchronisieren"
    echo "7) FIPS-180-4 Vault-Integritaets-Audit (Gehaertete 100%-Pruefung)"
    echo "0) Beenden"
    echo "================================================================================"
}

execute_option() {
    case "$1" in
        1)
            ./run_b2b_master_audit.sh
            ;;
        2)
            python3 facility_inventory_manager.py
            ;;
        3)
            python3 maintenance_interval_watchdog.py
            ;;
        4)
            python3 analyze_network_latency.py
            ;;
        5)
            python3 system_health_watchdog.py
            ;;
        6)
            ./autostart_facility_services.sh
            ;;
        7)
            python3 verify_vault_integrity.py
            ;;
        0)
            echo "Kontrollzentrum beendet."
            exit 0
            ;;
        *)
            echo "[!] Ungueltige Eingabe."
            ;;
    esac
}

if [ "$1" != "" ]; then
    show_menu
    echo "[TEST] Fuehre Menue-Option aus: $1"
    execute_option "$1"
    exit 0
fi

while true; do
    show_menu
    read -rp "Bitte Option waehlen [0-7]: " OPTION
    execute_option "$OPTION"
    echo ""
    read -rp "Taste druecken zum Fortfahren..." DUMMY
done
