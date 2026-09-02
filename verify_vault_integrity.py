import os
import subprocess
import hashlib
import datetime

MASTER_HASH_FILE = "GIT_REPO_MASTER_SHA256.txt"
ARCHIVE_HASH_FILE = "RELEASE_ARCHIVE_SHA256.txt"
ARCHIVE_FILE = "Projekt_Haus_im_Wind_Master_Release_2026.tar.gz"
REPORT_FILE = "VAULT_INTEGRITY_AUDIT_REPORT.txt"

EXCLUDED_FROM_CATALOG = {
    "GIT_REPO_MASTER_SHA256.txt",
    "RELEASE_ARCHIVE_SHA256.txt",
    "VAULT_INTEGRITY_AUDIT_REPORT.txt"
}

def get_file_sha256(filepath):
    h = hashlib.sha256()
    with open(filepath, "rb") as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return h.hexdigest()

def verify_vault():
    now_str = datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S")
    lines = []
    lines.append("================================================================================")
    lines.append("PROJEKT HAUS IM WIND: FIPS-180-4 VAULT-INTEGRITAETS-AUDIT (GEHAERTET)")
    lines.append(f"Prüfzeitpunkt:     {now_str}")
    lines.append("Liegenschaft:      Haus im Wind (LOC-30 bis LOC-32, Bad Pyrmont)")
    lines.append("Integritaetsnorm:  FIPS 180-4 / Git Tree SHA Integrity (Exklusive Meta-Hashes)")
    lines.append("================================================================================\n")

    # 1. Git Status prüfen
    git_clean = False
    try:
        git_res = subprocess.run(["git", "status", "--porcelain"], capture_output=True, text=True, check=True)
        uncommitted = [l for l in git_res.stdout.splitlines() if not any(l.strip().endswith(ex) for ex in EXCLUDED_FROM_CATALOG) and not l.strip().endswith("verify_vault_integrity.py")]
        if len(uncommitted) == 0:
            git_clean = True
            git_status_str = "BEREINIGT (WORKING TREE CLEAN)"
        else:
            git_status_str = f"UNCOMMITTED CHANGES ({len(uncommitted)} Dateien)"
    except Exception as e:
        git_status_str = f"FEHLER ({str(e)})"

    lines.append("1. REPOSITORY-ZUSTAND:")
    lines.append(f"Git-Status:        {git_status_str}\n")

    # 2. Release-Tarball Hash prüfen
    archive_ok = False
    archive_hash_expected = ""
    archive_hash_actual = ""
    if os.path.exists(ARCHIVE_HASH_FILE) and os.path.exists(ARCHIVE_FILE):
        with open(ARCHIVE_HASH_FILE, "r") as f:
            archive_hash_expected = f.read().split()[0].strip()
        archive_hash_actual = get_file_sha256(ARCHIVE_FILE)
        archive_ok = (archive_hash_expected == archive_hash_actual)

    lines.append("2. MASTER-RELEASE-TARBALL INTEGRITAET:")
    lines.append(f"Archivdatei:       {ARCHIVE_FILE}")
    lines.append(f"Soll-Hash:         {archive_hash_expected}")
    lines.append(f"Ist-Hash:          {archive_hash_actual}")
    lines.append(f"Status:            {'BITIDENTISCH (100% OK)' if archive_ok else 'HASH-ABWEICHUNG'}\n")

    # 3. Master Hashkatalog validieren (ohne zirkuläre Metadaten)
    total_files = 0
    matched_files = 0
    mismatches = []

    if os.path.exists(MASTER_HASH_FILE):
        with open(MASTER_HASH_FILE, "r") as f:
            for line in f:
                parts = line.strip().split(None, 1)
                if len(parts) == 2:
                    expected_hash, filepath = parts[0].strip(), parts[1].strip()
                    if filepath in EXCLUDED_FROM_CATALOG:
                        continue
                    total_files += 1
                    if os.path.exists(filepath):
                        actual_hash = get_file_sha256(filepath)
                        if actual_hash == expected_hash:
                            matched_files += 1
                        else:
                            mismatches.append(f"MODIFIZIERT: {filepath}")
                    else:
                        mismatches.append(f"FEHLT: {filepath}")

    lines.append("3. MASTER-HASHKATALOG DETAILVERIFIKATION:")
    lines.append(f"Katalog-Eintraege: {total_files} Quelldateien geprueft (Meta-Hashes exkludiert)")
    lines.append(f"Uebereinstimmung:  {matched_files} / {total_files} ({round((matched_files/total_files)*100, 1) if total_files else 0}%)")
    if mismatches:
        lines.append("Abweichungen:")
        for m in mismatches:
            lines.append(f"  - {m}")
    else:
        lines.append("Befund:            0 Bitfehler detektiert.")

    lines.append("\n================================================================================")
    lines.append("GESAMT-AUDIT-FESTSTELLUNG:")
    all_ok = git_clean and archive_ok and (total_files > 0) and (matched_files == total_files)
    lines.append(f"[{'X' if all_ok else ' '}] 100% kryptografische Unversehrtheit des Repositories.")
    lines.append(f"[{'X' if all_ok else ' '}] FIPS-180-4 Kette nahtlos geschlossen.")
    lines.append("================================================================================")
    status_text = "VAULT-INTEGRITAET ZU 100% VERIFIZIERT (PLATZ 1)" if all_ok else "INTEGRITAETS-WARNUNG"
    lines.append(f"STATUS: {status_text}.")
    lines.append("================================================================================")

    out_text = "\n".join(lines)
    with open(REPORT_FILE, "w", encoding="utf-8") as f:
        f.write(out_text)

    h = hashlib.sha256(out_text.encode("utf-8")).hexdigest()
    print(out_text)
    print(f"\nFIPS-180-4 SHA-256 ({REPORT_FILE}):\n{h}")

if __name__ == "__main__":
    verify_vault()
