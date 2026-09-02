import os
import zipfile

artifacts = [
    "README.md",
    "Cluster_Einreichung_P1.txt",
    "Mobilfunk_Standort_Dossier.txt",
    "Batch_P1_Auswertung.xlsx",
    "P1_Mobilfunk_Standorte.xlsx",
    "P1_Standorte_Cluster_Karte.html",
    "standort_karte.html",
    "p1_standorte.geojson",
    "alle_standorte.geojson"
]

zip_filename = "Mobilfunk_Cluster_Uebergabepaket.zip"
print('=' * 80)
print('PROJEKT-ARCHIVIERUNG: MOBILFUNK-STANDORTPLANUNG')
print('=' * 80)

missing_files = 0
with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
    for filename in artifacts:
        if os.path.exists(filename):
            size_kb = os.path.getsize(filename) / 1024
            zipf.write(filename)
            print(f'[OK] Hinzugefuegt: {filename:<35} ({size_kb:.1f} KB)')
        else:
            print(f'[FEHLT] Datei nicht gefunden: {filename}')
            missing_files += 1

print('=' * 80)
total_size_kb = os.path.getsize(zip_filename) / 1024
print(f'Archivierung erfolgreich abgeschlossen: {zip_filename} ({total_size_kb:.1f} KB)')
print('=' * 80)
