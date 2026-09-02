import os
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import datetime
import time

def dispatch_all():
    SMTP_SERVER = "smtp.gmail.com"
    SMTP_PORT = 587
    SENDER_EMAIL = "kiliajnscharf@gmail.com"
    SENDER_PASSWORD = os.environ.get("GMAIL_APP_PASSWORD")

    if not SENDER_PASSWORD or SENDER_PASSWORD == "DEIN_APP_PASSWORT":
        print("================================================================================")
        print("FEHLER: UMGEBUNGSVARIABLE GMAIL_APP_PASSWORD NICHT GESETZT!")
        print("Bitte setze das Passwort vorab in bash via:")
        print("export GMAIL_APP_PASSWORD='dein-16-stelliges-app-passwort'")
        print("================================================================================")
        return

    targets = [
        {"name": "Deutsche Funkturm GmbH - Konzerneinkauf", "email": "einkauf@dfmg.de"},
        {"name": "Vantage Towers AG - Procurement", "email": "landlords.germany@vantagetowers.com"},
        {"name": "Axians Deutschland - Standortakquise", "email": "info@axians.de"},
        {"name": "SPIE SAG GmbH - Einkauf Infrastruktur", "email": "kontakt@spie.de"},
        {"name": "Circet Deutschland - Partnermanagement", "email": "info@circet.de"}
    ]

    with open("ANSCHREIBEN_EINKAUF_B2B.txt", "r", encoding="utf-8") as f:
        body = f.read()

    print("================================================================================")
    print("LIVE-VERSAND: B2B-LIEFERANTENAKKREDITIERUNG AN 5 KONZERNE")
    print("================================================================================")
    
    context = ssl.create_default_context()
    
    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.ehlo()
        server.starttls(context=context)
        server.ehlo()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        print("SMTP-Authentifizierung erfolgreich hergestellt.\n")

        for t in targets:
            msg = MIMEMultipart()
            msg['From'] = f"Kilian Scharf <{SENDER_EMAIL}>"
            msg['To'] = t['email']
            msg['Subject'] = "B2B-Lieferantenakkreditierung & Standortakquise: Kilian Scharf - Ref. Cluster 2026"
            msg.attach(MIMEText(body, 'plain', 'utf-8'))

            server.sendmail(SENDER_EMAIL, t['email'], msg.as_string())
            ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(f"[{ts}] Zugestellt an: {t['name']} <{t['email']}> -> STATUS: 250 OK")
            
            # Eintrag in Audit Log
            log_entry = f"[{ts}] B2B_DISPATCH_SUCCESS: {t['name']} ({t['email']}) | Betreff: {msg['Subject']}\n"
            with open("DISPATCH_AUDIT_LOG.txt", "a", encoding="utf-8") as log_file:
                log_file.write(log_entry)
                
            time.sleep(1) # Kurze Pause zwischen den Mails

        server.quit()
        print("\n================================================================================")
        print("VERSAND ERFOLGREICH: ALLE 5 EINKAUFSSTELLEN WURDEN INFORMIERT.")
        print("================================================================================")

    except Exception as e:
        print(f"FEHLER BEIM VERSAND: {str(e)}")

if __name__ == '__main__':
    dispatch_all()
