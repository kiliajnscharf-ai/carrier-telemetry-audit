import pandas as pd

def plan_reinvestment():
    monthly_revenue = 2375.00  # Jahr 1 Basis (Cluster gesamt)
    
    # Allokationsmodell fuer nachhaltige Liegenschafts- und Infrastrukturprojekte
    allocation = {
        "Premium-Ausruestung & Profi-Werkzeuge (Knipex, Wera, etc.)": 0.25, # 25%
        "Autarke Energie- & Gebaeudeinstandhaltung":                   0.30, # 30%
        "IT-Infrastruktur & Server-Hardware":                          0.15, # 15%
        "Steuer- & Notfallruecklagen":                                 0.30  # 30%
    }
    
    print("================================================================================")
    print("REINVESTITIONS- & BUDGETPLANUNG: MONATLICHER CASHFLOW (JAHR 1)")
    print("================================================================================")
    print(f"Monatliches Gesamtbudget: {monthly_revenue:,.2f} EUR/Monat\n")
    
    records = []
    for k, v in allocation.items():
        monthly_budget = monthly_revenue * v
        annual_budget = monthly_budget * 12
        records.append({"Kategorie": k, "Anteil": f"{int(v*100)} %", "Monat_EUR": monthly_budget, "Jahr_EUR": annual_budget})
        print(f"{k:<58} | {int(v*100):>2} % | {monthly_budget:>8.2f} EUR/m | {annual_budget:>9.2f} EUR/a")
        
    print("================================================================================")
    df = pd.DataFrame(records)
    df.to_excel("Reinvestitionsplan_Budget.xlsx", index=False)
    print("Budgetplan exportiert nach: Reinvestitionsplan_Budget.xlsx")

if __name__ == '__main__':
    plan_reinvestment()
