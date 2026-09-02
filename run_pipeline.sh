#!/bin/bash
set -e

INPUT_CSV="${1:-neue_suchkreise.csv}"

echo "================================================================================"
echo "START DER MOBILFUNK-STANDORTPLANUNGS-PIPELINE (10-STUFEN TIER-1 MASTER-SYSTEM)"
echo "================================================================================"

if [ ! -f "$INPUT_CSV" ]; then
    echo "Fehler: Eingabedatei $INPUT_CSV nicht gefunden."
    exit 1
fi

echo "[1/10] Universal Ingestion & selbstadaptiver Header-Mapper..."
python3 universal_ingestion_engine.py "$INPUT_CSV"

echo "[2/10] Investitions- und CAPEX-Kalkulation..."
python3 capex_cost_calculator.py

echo "[3/10] OPEX- & ROI-Wirtschaftlichkeitsanalyse..."
python3 calculate_opex_roi.py

echo "[4/10] BEMFV-Strahlenschutz & 26. BImSchV Nachweiserstellung..."
python3 calculate_bemfv_safety.py

echo "[5/10] Backhaul-Entscheidung & KRITIS-Resilienzprüfung..."
python3 backhaul_selector.py
python3 kritis_power_resilience.py

echo "[6/10] ITU-R P.525 / P.526 Funkfeld- & Fresnelzonen-Berechnung..."
python3 itu_pathloss_fresnel.py

echo "[7/10] Umwelt- & Schutzgebietsprüfung (FFH / NSG / Wasserschutz)..."
python3 environmental_buffer_check.py

echo "[8/10] BNetzA-XML-Export & Multi-Cluster-Aggregation..."
python3 export_bnetza_xml.py
python3 aggregate_all_clusters.py

echo "[9/10] Kryptografische SHA-512 Master-Versiegelung & ZIP-Paketierung..."
python3 archive_vault_sealing.py

rm -f B2B_Mobilfunk_Master_Dossier_2026.zip
zip -9 B2B_Mobilfunk_Master_Dossier_2026.zip BNetzA_Antrag_STOB.xml CAPEX_Standort_Kalkulation.xlsx OPEX_ROI_Auswertung.xlsx Backhaul_Anbindung.xlsx ITU_Funkfeld_Fresnel.xlsx KRITIS_Resilienz_Report.txt BEMFV_Sicherheitsabstand.txt Umwelt_Vorpruefung.json Master_Cluster_Deutschland.geojson P1_Standorte_Cluster_Karte.html Cluster_Einreichung_P1.txt B2B_DELIVERY_VAULT_SHA512.txt
chmod 400 B2B_Mobilfunk_Master_Dossier_2026.zip

sha256sum B2B_Mobilfunk_Master_Dossier_2026.zip > B2B_Mobilfunk_Master_Dossier_2026.zip.sha256
python3 generate_dispatch_notice.py

echo "[10/10] Automatisierter B2B-Versand & Audit-Logging..."
python3 automated_dispatch_hub.py --mode local --target ./b2b_outbox

echo "================================================================================"
echo "TIER-1 MASTER-PIPELINE ERFOLGREICH BEENDET: ALLE 10 STUFEN DURCHGELAUFEN (PLATZ 1)."
echo "================================================================================"
