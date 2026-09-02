import datetime
import hashlib
import pathlib

def generate_dispatch():
    archive_file = "B2B_Mobilfunk_Master_Dossier_2026.zip"
    hash_file = "B2B_Mobilfunk_Master_Dossier_2026.zip.sha256"
    
    if not pathlib.Path(archive_file).exists():
        print(f"Fehler: {archive_file} nicht gefunden.")
        return
        
    sha256_hash = hashlib.sha256(open(archive_file, "rb").read()).hexdigest()
    size_kb = pathlib.Path(archive_file).stat().st_size / 1024
    timestamp = datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S")
    
    lines = []
    lines.append("================================================================================")
    lines.append("OFFIZIELLES B2B-STANDORTUEBERGABEPROTOKOLL & FREIGABEERKLAERUNG")
    lines.append("================================================================================")
    lines.append(f"Datum / Zeitstempel:   {timestamp}")
    lines.append(f"Dienstleistung:        Remote Site Acquisition & Technical Infrastructure Package")
    lines.append(f"Empfaenger-Kreis:      TowerCos / Mobilfunknetzbetreiber / Generalunternehmer\n")
    lines.append("LIEFERGEGENSTAND:")
    lines.append(f"  - Archivdatei:       {archive_file} ({size_kb:.1f} KB)")
    lines.append(f"  - SHA-256 Hash:      {sha256_hash}")
    lines.append(f"  - Pruefsummenfile:   {hash_file}\n")
    lines.append("ENTHALTENE FACHMODULE:")
    lines.append("  [1] BNetzA_Antrag_STOB.xml          (Schemakonformer Antrag gem. BEMFV/26. BImSchV)")
    lines.append("  [2] CAPEX_Standort_Kalkulation.xlsx (Investitionsrechnung Tiefbau & Mastbau)")
    lines.append("  [3] OPEX_ROI_Auswertung.xlsx        (Amortisationsanalyse fuer 2-4 Betreiber)")
    lines.append("  [4] Backhaul_Anbindung.xlsx         (10-Gbps-Richtfunk vs. Glasfasertrasse)")
    lines.append("  [5] KRITIS_Resilienz_Report.txt     (72h Notstromkonzept nach BSI-Standard)")
    lines.append("  [6] BEMFV_Sicherheitsabstand.txt    (DIN EN 50383 Personenschutzabstaende)")
    lines.append("  [7] Umwelt_Vorpruefung.json         (FFH/NSG/Wasserschutz Pufferanalyse)")
    lines.append("  [8] Master_Cluster_Deutschland.geojson (Makro-Geodatenstruktur EPSG:4326)")
    lines.append("  [9] P1_Standorte_Cluster_Karte.html (Interaktive GIS-Funkfeldkarte)")
    lines.append("  [10] Cluster_Einreichung_P1.txt     (Formelle Liegenschafts- & Pachtgrundlage)")
    lines.append("  [11] B2B_DELIVERY_VAULT_SHA512.txt  (Kryptografisches Master-Manifest)\n")
    lines.append("INTEGRITAETSPRUEFUNG BEIM EMPFAENGER:")
    lines.append(f"  Befehl: sha256sum -c {hash_file}")
    lines.append("================================================================================")
    
    notice_text = "\n".join(lines)
    with open("B2B_Uebergabeprotokoll_Release.txt", "w", encoding="utf-8") as f:
        f.write(notice_text)
        
    print(notice_text)
    print(f"\nUebergabeprotokoll erfolgreich exportiert: B2B_Uebergabeprotokoll_Release.txt")

if __name__ == '__main__':
    generate_dispatch()
