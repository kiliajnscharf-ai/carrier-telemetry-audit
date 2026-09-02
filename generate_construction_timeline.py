import pandas as pd
from datetime import datetime, timedelta

def create_timeline():
    start_date = datetime.now()
    phases = [
        ("Phase 1: Vorlage P1-Dossier & Vertragsschluss", 30),
        ("Phase 2: Baugenehmigungsverfahren (NBauO / Bauamt)", 90),
        ("Phase 3: Tiefbau Stromtrasse & Fundamentbau", 30),
        ("Phase 4: Maststockung & Stahlbau", 14),
        ("Phase 5: Systemtechnik, Antennen & Glasfaser/Richtfunk", 21),
        ("Phase 6: BNetzA-Standortbescheinigung & Netzintegration", 25)
    ]
    
    current = start_date
    print("================================================================================")
    print("MOBILFUNK-NEUBAU: REALISIERUNGSZEITPLAN (ACCELERATED P1-PATH)")
    print("================================================================================")
    print(f"Projektstart (Übergabe Dossier): {start_date.strftime('%d.%m.%Y')}\n")
    
    total_days = 0
    for name, days in phases:
        end = current + timedelta(days=days)
        print(f"[{current.strftime('%d.%m.%Y')} - {end.strftime('%d.%m.%Y')}] ({days:2d} Tage) : {name}")
        current = end
        total_days += days
        
    print(f"\nGesamtrealisierungszeit: {total_days} Tage (ca. {total_days/30:.1f} Monate)")
    print(f"Geplante Inbetriebnahme (On-Air): {current.strftime('%d.%m.%Y')}")
    print("================================================================================")

if __name__ == '__main__':
    create_timeline()
