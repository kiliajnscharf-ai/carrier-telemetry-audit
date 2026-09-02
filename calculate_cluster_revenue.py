import pandas as pd

def calculate_projected_revenue():
    # Annahmen basierend auf B2B Master-Dossier 2026
    standorte = [
        {"ID": "LOC-30", "Name": "Westflanke Forsthaus", "Basis_Pacht_Jahr": 5000, "Betreiber_Anzahl": 4},
        {"ID": "LOC-31", "Name": "Talstation Sued", "Basis_Pacht_Jahr": 4500, "Betreiber_Anzahl": 4},
        {"ID": "LOC-32", "Name": "Bergkuppe Nordost", "Basis_Pacht_Jahr": 5500, "Betreiber_Anzahl": 4}
    ]
    
    OPTIONS_PRAEMIE = 1000.0  # Einmalig bei Standortsicherung pro Standort
    ZUSATZ_PRO_BETREIBER = 1500.0  # Jaehrlicher Aufschlag ab Betreiber 2
    LAUFZEIT_JAHRE = 20
    INDEXIERUNG_PA = 0.02  # 2% jaehrliche Wertsicherung
    
    total_options = len(standorte) * OPTIONS_PRAEMIE
    
    records = []
    print("================================================================================")
    print("ERTRAGS- & CASHFLOW-PROGNOSE: MOBILFUNK-CLUSTER 2026 (20 JAHRE)")
    print("================================================================================")
    print(f"Einmalige Optionspraemien gesamt (Phase 2): {total_options:,.2f} EUR\n")
    
    total_sum_20y = 0.0
    
    for s in standorte:
        base = s["Basis_Pacht_Jahr"]
        extra = (s["Betreiber_Anzahl"] - 1) * ZUSATZ_PRO_BETREIBER
        annual_start = base + extra
        
        # Kumulierter Cashflow ueber 20 Jahre mit 2% Indexierung
        cum_revenue = sum(annual_start * ((1 + INDEXIERUNG_PA) ** year) for year in range(LAUFZEIT_JAHRE))
        total_sum_20y += cum_revenue
        
        records.append({
            "ID": s["ID"],
            "Name": s["Name"],
            "Pacht_Jahr_1": annual_start,
            "Pacht_20_Jahre_Gesamt": round(cum_revenue, 2)
        })
        
        print(f"Standort {s['ID']} ({s['Name']}):")
        print(f"  - Jaehrliche Pacht (Jahr 1, 4 Betreiber): {annual_start:,.2f} EUR/Jahr")
        print(f"  - Kumulierte Pachteinnahmen (20 Jahre):    {cum_revenue:,.2f} EUR\n")
        
    print("================================================================================")
    print(f"KUMULIERTER GESAMT-CASHFLOW CLUSTER (20 JAHRE): {total_sum_20y:,.2f} EUR")
    print("================================================================================")
    
    df = pd.DataFrame(records)
    df.to_excel("Cluster_Ertragsprognose_20Jahre.xlsx", index=False)
    print("Exportiert nach: Cluster_Ertragsprognose_20Jahre.xlsx")

if __name__ == '__main__':
    calculate_projected_revenue()
