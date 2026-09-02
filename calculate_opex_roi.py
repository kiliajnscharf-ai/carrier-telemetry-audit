import pandas as pd

def compute_opex_roi(input_excel='CAPEX_Standort_Kalkulation.xlsx', output_excel='OPEX_ROI_Auswertung.xlsx'):
    df = pd.read_excel(input_excel)
    
    # OPEX Parameter pro Jahr
    PACHT_JAHR = 3500       # Euro Grundstueckspacht
    STROM_JAHR = 3800       # Euro Systemtechnik-Energie
    WARTUNG_JAHR = 1200     # Euro DIN 18014 Pruefungen
    OPEX_TOTAL_JAHR = PACHT_JAHR + STROM_JAHR + WARTUNG_JAHR
    
    # Einnahmen pro Betreiber pro Jahr (Co-Location)
    MIETE_PRO_TENANT_JAHR = 15000  # Euro (1.250 EUR/Monat)
    
    results = []
    for _, row in df.iterrows():
        capex = row['Gesamt_CAPEX_EUR']
        
        # Amortisation bei 2, 3 und 4 Betreibern
        rev_2_tenants = 2 * MIETE_PRO_TENANT_JAHR
        rev_3_tenants = 3 * MIETE_PRO_TENANT_JAHR
        rev_4_tenants = 4 * MIETE_PRO_TENANT_JAHR
        
        net_2 = rev_2_tenants - OPEX_TOTAL_JAHR
        net_3 = rev_3_tenants - OPEX_TOTAL_JAHR
        net_4 = rev_4_tenants - OPEX_TOTAL_JAHR
        
        roi_2 = round(capex / net_2, 1) if net_2 > 0 else 99
        roi_3 = round(capex / net_3, 1) if net_3 > 0 else 99
        roi_4 = round(capex / net_4, 1) if net_4 > 0 else 99
        
        results.append({
            'ID': row['ID'],
            'Name': row['Name'],
            'CAPEX_EUR': capex,
            'OPEX_Jahr_EUR': OPEX_TOTAL_JAHR,
            'Nettoertrag_2_Betreiber_EUR': net_2,
            'Amortisation_2_Betreiber_Jahre': roi_2,
            'Nettoertrag_3_Betreiber_EUR': net_3,
            'Amortisation_3_Betreiber_Jahre': roi_3,
            'Nettoertrag_4_Betreiber_EUR': net_4,
            'Amortisation_4_Betreiber_Jahre': roi_4
        })
        
    res_df = pd.DataFrame(results)
    res_df.to_excel(output_excel, index=False)
    print("================================================================================")
    print("OPEX- & ROI-WIRTSCHAFTLICHKEITSRECHNUNG ERFOLGREICH DURCHGEFUEHRT")
    print("================================================================================")
    print(f"Ergebnisbericht gespeichert unter: {output_excel}\n")
    for _, r in res_df.iterrows():
        print(f"Standort {r['ID']} ({r['Name']}):")
        print(f"  - CAPEX: {r['CAPEX_EUR']:,} EUR | OPEX: {r['OPEX_Jahr_EUR']:,} EUR/Jahr")
        print(f"  - Amortisation bei 2 Betreibern (Telekom/Vodafone): {r['Amortisation_2_Betreiber_Jahre']} Jahre (Netto: {r['Nettoertrag_2_Betreiber_EUR']:,} EUR/a)")
        print(f"  - Amortisation bei 3 Betreibern (+ O2):             {r['Amortisation_3_Betreiber_Jahre']} Jahre (Netto: {r['Nettoertrag_3_Betreiber_EUR']:,} EUR/a)")
        print(f"  - Amortisation bei 4 Betreibern (+ 1&1):            {r['Amortisation_4_Betreiber_Jahre']} Jahre (Netto: {r['Nettoertrag_4_Betreiber_EUR']:,} EUR/a)\n")
    print("================================================================================")

if __name__ == '__main__':
    compute_opex_roi()
