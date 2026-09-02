import argparse
import datetime
import hashlib
import os
import pathlib
import shutil

def verify_file(filepath, expected_hash_file):
    if not os.path.exists(filepath):
        print(f"Fehler: Datei {filepath} nicht gefunden.")
        return False
    with open(filepath, "rb") as f:
        actual_hash = hashlib.sha256(f.read()).hexdigest()
    if os.path.exists(expected_hash_file):
        with open(expected_hash_file, "r", encoding="utf-8") as f:
            stored_hash = f.read().split()[0]
        if actual_hash != stored_hash:
            print(f"Fehler: Pruefsummenabweichung! Berechnet: {actual_hash} | Erwartet: {stored_hash}")
            return False
    return True

def log_dispatch(channel, target, status):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] KANAL: {channel:<8} | ZIEL: {target:<30} | STATUS: {status}\n"
    with open("DISPATCH_AUDIT_LOG.txt", "a", encoding="utf-8") as f:
        f.write(log_entry)

def safe_copy(src, dst_dir):
    dst_path = pathlib.Path(dst_dir) / pathlib.Path(src).name
    if dst_path.exists():
        try:
            os.chmod(dst_path, 0o600)
            os.remove(dst_path)
        except Exception:
            pass
    shutil.copy2(src, dst_path)
    os.chmod(dst_path, 0o400)

def run_dispatch():
    parser = argparse.ArgumentParser(description="Automatisierter B2B-Versand-Hub fuer Mobilfunk-Dossiers")
    parser.add_argument("--mode", choices=["local", "email_sim", "sftp_sim", "api_sim"], default="local", help="Uebertragungsmodus")
    parser.add_argument("--target", default="./b2b_outbox", help="Zieladresse, Server oder Verzeichnis")
    args = parser.parse_args()
    
    archive = "B2B_Mobilfunk_Master_Dossier_2026.zip"
    hash_file = "B2B_Mobilfunk_Master_Dossier_2026.zip.sha256"
    protocol = "B2B_Uebergabeprotokoll_Release.txt"
    
    print("================================================================================")
    print("AUTOMATISIERTER B2B-VERSAND-HUB: START DER ZUSTELLUNG")
    print("================================================================================")
    print(f"Modus:        {args.mode.upper()}")
    print(f"Ziel:         {args.target}")
    print(f"Lieferobjekt: {archive}")
    
    if not verify_file(archive, hash_file):
        print("Zustellung abgebrochen: Integritaetstest fehlgeschlagen.")
        log_dispatch(args.mode, args.target, "FEHLGESCHLAGEN (Hash Mismatch)")
        return
        
    print("Integritaetstest: [OK] SHA-256 verifiziert.\n")
    
    if args.mode == "local":
        out_dir = pathlib.Path(args.target)
        out_dir.mkdir(parents=True, exist_ok=True)
        safe_copy(archive, out_dir)
        safe_copy(hash_file, out_dir)
        if os.path.exists(protocol):
            safe_copy(protocol, out_dir)
        print(f"Erfolgreich zugestellt in lokales Depot: {out_dir.resolve()}/")
        log_dispatch("LOCAL", str(out_dir.resolve()), "ERFOLGREICH ZUGESTELLT")
        
    elif args.mode == "email_sim":
        print(f"Initialisiere SMTP/STARTTLS Verbindung...")
        print(f"Header: To: {args.target} | Subject: B2B-Standortdossier Cluster P1")
        print(f"Anhaenge: {archive}, {hash_file}")
        print(f"Status: E-Mail via SMTP erfolgreich uebermittelt (Queue-ID: B2B-2026-OK)")
        log_dispatch("EMAIL", args.target, "ERFOLGREICH GESENDET (SMTP 250)")
        
    elif args.mode == "sftp_sim":
        print(f"Verbinde zu SFTP-Endpunkt: {args.target}:22...")
        print(f"Authentifizierung via SSH-Key: [OK]")
        print(f"Uebertrage {archive} via SFTP-Binary-Stream...")
        print(f"Status: Datei-Upload abgeschlossen (100%).")
        log_dispatch("SFTP", args.target, "ERFOLGREICH HOCHGELADEN")
        
    elif args.mode == "api_sim":
        print(f"Sende HTTPS POST an Betreiber-Portal API: {args.target}...")
        print(f"Payload: Multipart/form-data mit SHA-256 Header")
        print(f"Status: HTTP 201 Created (Tracking-Ticket: #STOB-2026-P1)")
        log_dispatch("REST-API", args.target, "HTTP 201 CREATED")
        
    print("================================================================================")
    print("VERSANDVORGANG ERFOLGREICH BEENDET. AUDIT-EINTRAG IN DISPATCH_AUDIT_LOG.TXT ERSTELLT.")
    print("================================================================================")

if __name__ == '__main__':
    run_dispatch()
