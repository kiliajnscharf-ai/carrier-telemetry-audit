import os
import hashlib
import datetime

def calculate_sha256(filepath):
    h = hashlib.sha256()
    with open(filepath, "rb") as f:
        while chunk := f.read(8192):
            h.update(chunk)
    return h.hexdigest()

def verify_system_integrity():
    print("================================================================================")
    print("PROJEKT HAUS IM WIND: B2B-SYSTEM-INTEGRITAETS-WAECHTER (PHASE 48 - V2)")
    print("================================================================================")

    hash_catalog = "GIT_REPO_MASTER_SHA256.txt"
    if not os.path.exists(hash_catalog):
        print(f"FEHLER: Hashkatalog {hash_catalog} nicht gefunden!")
        return

    now_str = datetime.datetime.now().strftime('%d.%m.%Y %H:%M:%S')
    total_files = 0
    passed_files = 0
    mismatched_files = []
    missing_files = []

    # Ausnahmeliste für selbstreferenzielle Katalogdateien
    excluded_files = {hash_catalog, "RELEASE_ARCHIVE_SHA256.txt", "B2B_INTEGRITY_SENTINEL_LOG.txt"}

    with open(hash_catalog, "r", encoding="utf-8") as f:
        lines = f.readlines()

    for line in lines:
        line = line.strip()
        if not line:
            continue
        parts = line.split(maxsplit=1)
        if len(parts) != 2:
            continue
        expected_hash, rel_path = parts

        if rel_path in excluded_files:
            continue  # Selbstreferenzielle Meta-Dateien überspringen

        total_files += 1

        if not os.path.exists(rel_path):
            missing_files.append(rel_path)
            continue

        actual_hash = calculate_sha256(rel_path)
        if actual_hash == expected_hash:
            passed_files += 1
        else:
            mismatched_files.append((rel_path, expected_hash, actual_hash))

    report = []
    report.append("================================================================================")
    report.append("B2B-DATEISYSTEM-INTEGRITAETS-AUDIT (BEREINIGT & KORRIGIERT)")
    report.append(f"Zeitstempel:       {now_str}")
    report.append(f"Referenzkatalog:   {hash_catalog}")
    report.append("================================================================================\n")
    report.append(f"{'Prüfparameter':<40} | {'Sollwert / Erwartung':<20} | {'Istwert / Status'}")
    report.append("-" * 75)
    report.append(f"{'Geprüfte Master-Dateien':<40} | {'>= 40 Artefakte':<20} | {total_files} Dateien")
    report.append(f"{'Kryptografisch valide':<40} | {'100% Match':<20} | {passed_files} Dateien")
    report.append(f"{'Hash-Mismatches (Korruption)':<40} | {'0 Abweichungen':<20} | {len(mismatched_files)} Abweichungen")
    report.append(f"{'Fehlende Dateien':<40} | {'0 Dateien':<20} | {len(missing_files)} fehlend")
    report.append("-" * 75)

    report.append("\nAUDIT-FESTSTELLUNG:")
    if passed_files == total_files and len(mismatched_files) == 0:
        report.append("[X] 1. Alle geschäftskritischen Master-Dateien sind bitgenau intakt.")
        report.append("[X] 2. Keine Datenkorruption und keine unautorisierten Modifikationen.")
        report.append("[X] 3. Meta-Hashes bereinigt; System zu 100% konform (Platz 1).")
        status_text = "SYSTEMINTEGRITAET ZU 100% BESTAETIGT (PLATZ 1)"
    else:
        report.append("[!] FEHLER: Systemintegrität verletzt!")
        status_text = "INTEGRITAETSFEHLER DETEKTIERT"

    report.append("================================================================================")
    report.append(f"STATUS: {status_text}")
    report.append("================================================================================")

    out = "\n".join(report)
    with open("B2B_INTEGRITY_SENTINEL_LOG.txt", "w", encoding="utf-8") as f:
        f.write(out)
    print(out)

if __name__ == '__main__':
    verify_system_integrity()
