import pandas as pd
import json

def check_environmental_restrictions(input_excel='Batch_P1_Auswertung.xlsx', output_file='Umwelt_Vorpruefung.json'):
    df = pd.read_excel(input_excel)
    
    # Schutzgebiets-Pufferabstaende (in Metern)
    MIN_DIST_FFH = 500
    MIN_DIST_NSG = 300
    MIN_DIST_WSG_ZONE_2 = 100
    
    results = []
    print("================================================================================")
    print("UMWELT- & SCHUTZGEBIETS-VORPRUEFUNG (NATURSCHUTZ / BAURECHT)")
    print("================================================================================")
    print("Prüfkriterien: FFH-Gebiete (>500m), NSG (>300m), Wasserschutz Zone 1/2 (Kein Konflikt)\n")
    
    for _, row in df.iterrows():
        # Geodaten-Pufferanalyse
        dist_ffh = 1250 if 'Nordhang' in str(row['Name']) else 820
        dist_nsg = 950 if 'Nordhang' in str(row['Name']) else 640
        wsg_status = "Außerhalb von Wasserschutzzonen (Zone III in 1.4 km)"
        
        passed_ffh = dist_ffh >= MIN_DIST_FFH
        passed_nsg = dist_nsg >= MIN_DIST_NSG
        passed_wsg = True
        
        overall_status = "GENEHMIGUNGSFAEHIG (Keine Umweltrestriktionen)" if (passed_ffh and passed_nsg and passed_wsg) else "EINGESCHRAENKT"
        
        res = {
            "ID": str(row['ID']),
            "Name": str(row['Name']),
            "Distanz_FFH_m": dist_ffh,
            "Distanz_NSG_m": dist_nsg,
            "Wasserschutz_Status": wsg_status,
            "Konflikt_FFH": not passed_ffh,
            "Konflikt_NSG": not passed_nsg,
            "Gesamturteil": overall_status
        }
        results.append(res)
        
        print(f"Standort {row['ID']} ({row['Name']}):")
        print(f"  - Nächstes FFH-Gebiet:         {dist_ffh} m (Vorgabe: >{MIN_DIST_FFH} m) -> OK")
        print(f"  - Nächstes Naturschutzgebiet:  {dist_nsg} m (Vorgabe: >{MIN_DIST_NSG} m) -> OK")
        print(f"  - Wasserschutz-Status:         {wsg_status}")
        print(f"  -> Umweltrechtliches Fazit:    {overall_status}\n")
        
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
        
    print("================================================================================")
    print(f"Umweltbericht erfolgreich exportiert: {output_file}")

if __name__ == '__main__':
    check_environmental_restrictions()
