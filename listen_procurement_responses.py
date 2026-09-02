import imaplib
import email
from email.header import decode_header
import os
import re
import datetime

def clean_header(text):
    if not text:
        return ""
    decoded_parts = decode_header(text)
    header_text = ""
    for part, encoding in decoded_parts:
        if isinstance(part, bytes):
            try:
                header_text += part.decode(encoding if encoding else "utf-8", errors="ignore")
            except Exception:
                header_text += part.decode("latin1", errors="ignore")
        else:
            header_text += str(part)
    return header_text

def check_inbox():
    IMAP_SERVER = "imap.gmail.com"
    IMAP_PORT = 993
    USERNAME = "kiliajnscharf@gmail.com"
    PASSWORD = os.environ.get("GMAIL_APP_PASSWORD")

    if not PASSWORD:
        print("================================================================================")
        print("FEHLER: GMAIL_APP_PASSWORD IST NICHT GESETZT.")
        print("Bitte vorab via export GMAIL_APP_PASSWORD='...' in bash setzen.")
        print("================================================================================")
        return

    TARGET_DOMAINS = [
        "dfmg.de", "vantagetowers.com", "axians.de", 
        "spie.de", "circet.de", "telekom.de", "vodafone.com"
    ]

    TICKET_PATTERNS = [r"LLSM\w+", r"DFMG[-\w]+", r"LOC-\d+"]

    print("================================================================================")
    print("B2B IMAP-RESPONSE-LISTENER: POSTEINGANGS-SCAN")
    print("================================================================================")
    print(f"Server:     {IMAP_SERVER}:{IMAP_PORT}")
    print(f"Konto:      {USERNAME}")
    print(f"Zeitpunkt:  {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("--------------------------------------------------------------------------------")

    try:
        mail = imaplib.IMAP4_SSL(IMAP_SERVER, IMAP_PORT)
        mail.login(USERNAME, PASSWORD)
        mail.select("inbox")

        # Letzte 50 Mails im Posteingang pruefen
        status, messages = mail.search(None, "ALL")
        if status != "OK" or not messages[0]:
            print("Keine Nachrichten im Posteingang gefunden.")
            mail.logout()
            return

        msg_ids = messages[0].split()
        check_ids = msg_ids[-50:] if len(msg_ids) > 50 else msg_ids
        check_ids.reverse()

        matched_responses = []

        for m_id in check_ids:
            res, data = mail.fetch(m_id, "(RFC822.HEADER)")
            if res != "OK":
                continue

            raw_email = data[0][1]
            msg = email.message_from_bytes(raw_email)

            sender = clean_header(msg.get("From"))
            subject = clean_header(msg.get("Subject"))
            date_str = clean_header(msg.get("Date"))

            sender_match = any(domain in sender.lower() for domain in TARGET_DOMAINS)
            ticket_match = any(re.search(pat, subject, re.IGNORECASE) for pat in TICKET_PATTERNS)

            if sender_match or ticket_match:
                matched_responses.append({
                    "id": m_id.decode(),
                    "sender": sender,
                    "subject": subject,
                    "date": date_str
                })

        print(f"Gefundene relevante B2B-Nachrichten: {len(matched_responses)}\n")

        if matched_responses:
            for item in matched_responses:
                entry = f"[{item['date']}] ABSENDER: {item['sender']} | BETREFF: {item['subject']}"
                print(entry)
                with open("B2B_INCOMING_RESPONSES.log", "a", encoding="utf-8") as f:
                    f.write(f"[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {entry}\n")
        else:
            print("Status: Keine neuen Betreiber-Rueckmeldungen erkannt.")
            print("Alle Vorgaenge verbleiben im regulaeren Fristenfenster (Wiedervorlage 15.09.2026).")

        mail.logout()
        print("================================================================================")
        print("SCAN ABGESCHLOSSEN: PROTOKOLL IN B2B_INCOMING_RESPONSES.log AKTUALISIERT.")
        print("================================================================================")

    except Exception as e:
        print(f"FEHLER BEIM IMAP-ABRUF: {str(e)}")

if __name__ == "__main__":
    check_inbox()
