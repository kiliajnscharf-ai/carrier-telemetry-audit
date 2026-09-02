import smtplib
import ssl
import getpass
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

def send_dossier():
    zip_path = "/home/userland/b2b_outbox/B2B_Mobilfunk_Master_Dossier_2026.zip"
    hash_path = "/home/userland/b2b_outbox/B2B_Mobilfunk_Master_Dossier_2026.zip.sha256"
    summary_path = "/home/userland/EXECUTIVE_CLUSTER_SUMMARY.txt"
    
    sender_email = "kiliajnscharf@gmail.com"
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    
    if not os.path.exists(zip_path):
        print(f"Fehler: {zip_path} nicht gefunden.")
        return

    print("================================================================================")
    print("B2B-ECHTVERSAND: MOBILFUNK-STANDORTDOSSIER")
    print("================================================================================")
    print(f"Absender:    {sender_email}")
    print(f"SMTP-Server: {smtp_server}:{smtp_port} (STARTTLS)")
    print("--------------------------------------------------------------------------------")
    print("Hinweis: Google erfordert ein 16-stelliges App-Passwort (nicht das normale Passwort).")
    
    sender_password = getpass.getpass("Google App-Passwort eingeben: ")
    recipient_email = input("Empfaenger-E-Mail (z. B. standortangebote@dfmg.de): ").strip()
    
    if not recipient_email:
        print("Fehler: Keine Empfaenger-Adresse angegeben. Abbruch.")
        return

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = "B2B-Standortdossier & Vorqualifizierung Cluster 2026 (LOC-30, LOC-31, LOC-32)"
    
    body = "Sehr geehrte Damen und Herren,\n\n"
    body += "anbei erhalten Sie das vollstaendig vorqualifizierte B2B-Mobilfunk-Standortdossier fuer das Ausbau-Cluster.\n\n"
    if os.path.exists(summary_path):
        with open(summary_path, "r", encoding="utf-8") as f:
            body += f.read()
            
    msg.attach(MIMEText(body, 'plain', 'utf-8'))
    
    # Anhang 1: ZIP-Archiv
    with open(zip_path, "rb") as f:
        part1 = MIMEBase("application", "zip")
        part1.set_payload(f.read())
    encoders.encode_base64(part1)
    part1.add_header("Content-Disposition", f"attachment; filename={os.path.basename(zip_path)}")
    msg.attach(part1)
    
    # Anhang 2: SHA256-Hash
    if os.path.exists(hash_path):
        with open(hash_path, "rb") as f:
            part2 = MIMEBase("text", "plain")
            part2.set_payload(f.read())
        encoders.encode_base64(part2)
        part2.add_header("Content-Disposition", f"attachment; filename={os.path.basename(hash_path)}")
        msg.attach(part2)
        
    context = ssl.create_default_context()
    print(f"\nVerbinde zu {smtp_server}:{smtp_port}...")
    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls(context=context)
            server.login(sender_email, sender_password)
            server.send_message(msg)
        print(f"\nERFOLG: Dossier wurde vollstaendig per E-Mail an {recipient_email} versendet.")
    except Exception as e:
        print(f"\nFehler beim E-Mail-Versand: {e}")

if __name__ == '__main__':
    send_dossier()
