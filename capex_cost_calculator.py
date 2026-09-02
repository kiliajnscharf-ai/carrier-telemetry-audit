import pandas as pd
import pathlib

def calculate_capex(input_excel='Batch_P1_Auswertung.xlsx', output_excel='CAPEX_Standort_Kalkulation.xlsx'):
    df = pd.read_excel(input_excel)
    
    COST_MAST_30M = 85000
    COST_MAST_40M = 115000
    GRID_CONNECT_BASE = 12500
    
    capex_list = []
    for _, row in df.iterrows():
        power_m = row.get('Strom_Distanz_m', 50)
        alt_m = row.get('Hoehe_m', 200)
        access = str(row.get('Zuwegung', 'Wirtschaftsweg'))
        
        cost_per_m = 130 if 'Asphalt' in access else (75 if 'Wirtschaftsweg' in access else 45)
        tiefbau = int(power_m * cost_per_m)
        mast_cost = COST_MAST_40M if alt_m > 250 else COST_MAST_30M
        mast_type = '40m Gittermast' if alt_m > 250 else '30m Betonmast'
        total_capex = tiefbau + mast_cost + GRID_CONNECT_BASE
        
        capex_list.append({
            'ID': row['ID'],
            'Name': row['Name'],
            'Score': row['Score'],
            'Hoehe_m': alt_m,
            'Masttyp': mast_type,
            'Trasse_m': power_m,
            'Tiefbau_Strom_EUR': tiefbau,
            'Mastbau_EUR': mast_cost,
            'Netzanschluss_EUR': GRID_CONNECT_BASE,
            'Gesamt_CAPEX_EUR': total_capex
        })
        
    res_df = pd.DataFrame(capex_list)
    res_df.to_excel(output_excel, index=False)
    print('================================================================================')
    print('CAPEX-INVESTITIONSBERECHNUNG ERFOLGREICH DURCHGEFUEHRT')
    print('================================================================================')
    print(f'Ergebnisbericht exportiert nach: {output_excel}')
    print('')
    for _, r in res_df.iterrows():
        print(f"Standort {r['ID']} ({r['Name']}):")
        print(f"  - Masttyp:          {r['Masttyp']} ({r['Mastbau_EUR']:,} EUR)")
        print(f"  - Tiefbau Strom:    {r['Trasse_m']} m a {r['Tiefbau_Strom_EUR']:,} EUR")
        print(f"  - Netzanschluss:    {r['Netzanschluss_EUR']:,} EUR")
        print(f"  -> Gesamt-CAPEX:    {r['Gesamt_CAPEX_EUR']:,} EUR")
        print('')
    print(f"Summe Gesamtinvestition Cluster: {res_df['Gesamt_CAPEX_EUR'].sum():,} EUR")
    print('================================================================================')

if __name__ == '__main__':
    calculate_capex()
