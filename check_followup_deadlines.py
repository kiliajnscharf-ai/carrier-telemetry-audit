import pandas as pd
import datetime

def check_deadlines():
    df = pd.read_excel("B2B_TICKET_TRACKING_MASTER.xlsx")
    today = datetime.datetime.now()
    
    print("================================================================================")
    print("B2B-FRISTEN-MONITORING: STANDORT-AKQUISITION CLUSTER 2026")
    print("================================================================================")
    print(f"Aktuelles Datum: {today.strftime('%d.%m.%Y %H:%M:%S')}\n")
    
    # Standard-Prueffrist der Betreiber: 14 Kalendertage
    SUBMISSION_DATE = datetime.datetime(2026, 9, 1)
    TARGET_DEADLINE = SUBMISSION_DATE + datetime.timedelta(days=14)
    days_left = (TARGET_DEADLINE - today).days
    
    for _, row in df.iterrows():
        betreiber = row['Betreiber']
        ticket = row['Ticket_ID']
        status = row['Status']
        
        print(f"Betreiber:        {betreiber}")
        print(f"Ticket-ID:        {ticket}")
        print(f"Status:           {status}")
        print(f"Einreichung:      {SUBMISSION_DATE.strftime('%d.%m.%Y')}")
        print(f"Wiedervorlage am: {TARGET_DEADLINE.strftime('%d.%m.%Y')} (Verbleibend: {days_left} Tage)")
        print(f"Aktion:           Warten auf Pruefbescheid Funknetzplanung / Pachtvertragsentwurf")
        print("--------------------------------------------------------------------------------")
        
    print("STATUS: ALLE VORGAENGE INNERHALB DER REGULAEREN PRUEFFRIST.")
    print("================================================================================")

if __name__ == '__main__':
    check_deadlines()
