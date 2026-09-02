import hashlib
import os

files_to_hash = [
    "Mobilfunk_Cluster_Uebergabepaket.zip",
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

print('=' * 80)
print('INTEGRITAETS-PRUEFUNG: SHA-256 HASH-GENERIERUNG')
print('=' * 80)

checksum_lines = []
for filename in files_to_hash:
    if os.path.exists(filename):
        sha256 = hashlib.sha256()
        with open(filename, 'rb') as f:
            while chunk := f.read(8192):
                sha256.update(chunk)
        digest = sha256.hexdigest()
        checksum_lines.append(f'{digest}  {filename}')
        print(f'{digest}  {filename}')
    else:
        print(f'Warnung: Datei {filename} nicht gefunden.')

with open('SHA256SUMS.txt', 'w', encoding='utf-8') as f:
    for line in checksum_lines:
        f.write(line + chr(10))

print('=' * 80)
print('Pruefsummendatei erfolgreich exportiert: SHA256SUMS.txt')
print('=' * 80)
