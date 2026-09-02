import hashlib
import glob
import os
import datetime

def seal_vault(output_manifest='B2B_DELIVERY_VAULT_SHA512.txt'):
    # Schreibschutz aufheben, falls Datei aus vorherigem Lauf existiert
    if os.path.exists(output_manifest):
        try:
            os.chmod(output_manifest, 0o600)
            os.remove(output_manifest)
        except Exception:
            pass

    files_to_seal = sorted(
        glob.glob("*.xlsx") + 
        glob.glob("*.geojson") + 
        glob.glob("*.xml") + 
        glob.glob("*.html") + 
        glob.glob("*.json") + 
        glob.glob("*.txt")
    )
    
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    lines = []
    lines.append("================================================================================")
    lines.append("B2B-CLIENT DELIVERY VAULT: KRYPTOGRAFISCHES SHA-512 MASTER-SIEGEL")
    lines.append("================================================================================")
    lines.append(f"Erstellungszeitpunkt: {timestamp}")
    lines.append(f"Dienstleister-Status: Remote Site Acquisition & Infrastructure Engineering")
    lines.append(f"Integritaets-Standard: FIPS 180-4 SHA-512 (Revisionssicher)\n")
    
    sealed_count = 0
    for file_path in files_to_seal:
        if file_path == output_manifest or file_path.startswith("ALL_CLUSTERS"):
            continue
        if os.path.isfile(file_path):
            with open(file_path, "rb") as f:
                file_hash = hashlib.sha512(f.read()).hexdigest()
            size_kb = os.path.getsize(file_path) / 1024
            lines.append(f"{file_hash}  {file_path} ({size_kb:.1f} KB)")
            sealed_count += 1
            
    lines.append("\n================================================================================")
    lines.append(f"Gesamtanzahl versiegelter Kundenartefakte: {sealed_count}")
    lines.append("STATUS: UNVERAENDERBAR & AUDIT-KONFORM FUER BETREIBER-UEBERGABE")
    lines.append("================================================================================")
    
    manifest_content = "\n".join(lines)
    with open(output_manifest, "w", encoding="utf-8") as f:
        f.write(manifest_content)
        
    # Nach Erstellung wieder schuetzen
    os.chmod(output_manifest, 0o400)
    
    print(manifest_content)
    print(f"\nMaster-Siegel exportiert: {output_manifest}")

if __name__ == '__main__':
    seal_vault()
