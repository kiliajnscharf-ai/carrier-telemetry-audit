import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
import datetime

def send_application(target_email, target_name):
    SMTP_SERVER = "smtp.gmail.com"
    SMTP_PORT = 587
    SENDER_EMAIL = "kiliajnscharf@gmail.com"
    SENDER_PASSWORD = os.environ.get("GMAIL_APP_PASSWORD", "DEIN_APP_PASSWORT")
    
    with open("ANSCHREIBEN_EINKAUF_B2B.txt", "r", encoding="utf-8") as f:
        body = f.read()
        
    msg = MIMEMultipart()
    msg['From'] = f"Kilian Scharf <{SENDER_EMAIL}>"
    msg['To'] = target_email
    msg['Subject'] = f"B2B-Lieferantenakkreditierung & Standortakquise: Kilian Scharf - Ref. Cluster 2026"
    msg.attach(MIMEText(body, 'plain', 'utf-8'))
    
    print(f"Bereit zum Versand an: {target_name} ({target_email})")
    print(f"Betreff: {msg['Subject']}")
    print("STATUS: VORLAGE BEREIT. ZUR ECHTEN ZUSTELLUNG UMGEBUNGSVARIABLE GMAIL_APP_PASSWORD SETZEN.")

if __name__ == '__main__':
    send_application("einkauf@dfmg.de", "Deutsche Funkturm GmbH - Konzerneinkauf")
