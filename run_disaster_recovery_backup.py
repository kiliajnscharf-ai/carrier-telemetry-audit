import os
import shutil
import hashlib
import datetime

def calculate_sha256(filepath):
    h = hashlib.sha256()
    with open(filepath, "rb") as f:
        while chunk := f.read(8192):
            h.update(chunk)
    return h.hexdigest()

def create_backup():
    print("================================================================================")
    print("PROJEKT HAUS IM WIND: DISASTER RECOVERY & BACKUP-SPIEGELUNG (PHASE 43)")
    print("================================================================================")

    backup_dir = "BACKUP_VAULT_EXPORT"
    os.makedirs(backup_dir, exist_ok=True)

    files_to_backup = [
        "Projekt_Haus_im_Wind_Master_Release_2026.tar.gz",
        "GIT_REPO_MASTER_SHA256.txt",
        "RELEASE_ARCHIVE_SHA256.txt",
        "PROJEKT_HAUS_IM_WIND_MASTER_DOSSIER_2026.txt"
    ]

    now_str = datetime.datetime.now().strftime('%d.%m.%Y %H:%M:%S')
    report = []
    report.append("================================================================================")
    report.append("B2B-DISASTER-RECOVERY & BACKUP-PROTOKOLL (BSI IT-GRUNDSCHUTZ)")
    report.append(f"Zeitstempel:       {now_str}")
    report.append(f"Zielverzeichnis:   {backup_dir}/")
    report.append("================================================================================\n")
    report.append(f"{'Datei':<46} | {'Original SHA-256':<16} | {'Status'}")
    report.append("-" * 75)

    all_verified = True
    for fname in files_to_backup:
        if os.path.exists(fname):
            dest_path = os.path.join(backup_dir, fname)
            shutil.copy2(fname, dest_path)
            
            orig_hash = calculate_sha256(fname)
            dest_hash = calculate_sha256(dest_path)

            if orig_hash == dest_hash:
                report.append(f"{fname:<46} | {orig_hash[:16]}... | VERIFIZIERT (OK)")
            else:
                report.append(f"{fname:<46} | HASH-MISMATCH     | FEHLER")
                all_verified = False
        else:
            report.append(f"{fname:<46} | DATEI FEHLT      | NICHT GEFUNDEN")
            all_verified = False

    report.append("-" * 75)
    report.append("\nERGEBNISBEWERTUNG:")
    if all_verified:
        report.append("[X] 1. Alle Master-Artefakte redundant in den Backup-Vault gespiegelt.")
        report.append("[X] 2. Bitgenaue SHA-256-Integrität zu 100% verifiziert.")
        report.append("[X] 3. Bereit für externen Export oder Offline-Sicherung.")
        status_text = "DISASTER RECOVERY BEREIT (PLATZ 1)"
    else:
        report.append("[!] FEHLER: Backup unvollständig oder Prüfsummen fehlerhaft.")
        status_text = "BACKUP-FEHLER"

    report.append("================================================================================")
    report.append(f"STATUS: {status_text}")
    report.append("================================================================================")

    out = "\n".join(report)
    with open("B2B_BACKUP_STATUS.txt", "w", encoding="utf-8") as f:
        f.write(out)
    print(out)

if __name__ == '__main__':
    create_backup()
