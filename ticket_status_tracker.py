import pandas as pd
import datetime

def update_tracker():
    timestamp = datetime.datetime.now().strftime("%d.%m.%Y")
    
    data = [
        {
            "Datum": timestamp,
            "Betreiber": "Vantage Towers AG",
            "Ticket_ID": "LLSM0135511",
            "Cluster": "Cluster 2026 (LOC-30, LOC-31, LOC-32)",
            "Status": "Ticket eröffnet / In fachlicher Prüfung",
            "Kontakt": "Landlords.germany@vantagetowers.com",
            "Telefon": "+49 (0) 800/87 88 388"
        },
        {
            "Datum": timestamp,
            "Betreiber": "Deutsche Funkturm GmbH (DFMG)",
            "Ticket_ID": "DFMG-INCOMING-2026",
            "Cluster": "Cluster 2026 (LOC-30, LOC-31, LOC-32)",
            "Status": "Eingang bestätigt / In Bearbeitung",
            "Kontakt": "Vermieterbetreuung@dfmg.de",
            "Telefon": "Liegenschaftsportal"
        }
    ]
    
    df = pd.DataFrame(data)
    df.to_excel("B2B_TICKET_TRACKING_MASTER.xlsx", index=False)
    
    print("================================================================================")
    print("B2B-TICKET-TRACKER: AKTUELLER STATUS DER BETREIBER-EINREICHUNGEN")
    print("================================================================================")
    print(df.to_string(index=False))
    print("================================================================================")
    print("Exportiert nach: B2B_TICKET_TRACKING_MASTER.xlsx")

if __name__ == '__main__':
    update_tracker()
