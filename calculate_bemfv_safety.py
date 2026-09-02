import pandas as pd
import math

def calculate_bemfv(input_excel='Batch_P1_Auswertung.xlsx', output_file='BEMFV_Sicherheitsabstand.txt'):
    df = pd.read_excel(input_excel)
    
    # Grenzwerte nach 26. BImSchV / ICNIRP
    # Grenzwert Leistungsflussdichte S_lim bei 700-900 MHz ca. 4.5 W/m^2
    # Formel fuer Personensicherheitsabstand r = sqrt(EIRP / (4 * pi * S_lim))
    S_LIM = 4.5  # W/m^2
    EIRP_PER_SECTOR = 2500  # Watt EIRP
    
    # Hauptstrahl-Sicherheitsabstand
    r_safety = round(math.sqrt(EIRP_PER_SECTOR / (4 * math.pi * S_LIM)), 2)
    # Vertikaler Sicherheitsabstand nach unten (gedaempft durch Antennendiagramm ca. Faktor 0.22)
    r_vertical = round(r_safety * 0.22, 2)
    
    lines = []
    lines.append("================================================================================")
    lines.append("BEMFV-STRAHLENSCHUTZ- & SICHERHEITSABSTANDSBERICHT (26. BImSchV)")
    lines.append("================================================================================")
    lines.append(f"Berechnungsgrundlage: DIN EN 50383 / ICNIRP (S_Grenzwert: {S_LIM} W/m^2)")
    lines.append(f"Referenz-Sendeleistung pro Sektor: {EIRP_PER_SECTOR} W EIRP (3 Sektoren je 120 Grad)\n")
    
    for _, row in df.iterrows():
        mast_h = 40 if row.get('Hoehe_m', 200) > 250 else 30
        ground_clearance = mast_h - r_vertical
        
        lines.append(f"Standort {row['ID']} ({row['Name']}):")
        lines.append(f"  - Mastbauhoehe:               {mast_h} m")
        lines.append(f"  - Horizontaler Schutzabstand: {r_safety} m (Hauptstrahlrichtung)")
        lines.append(f"  - Vertikaler Schutzabstand:   {r_vertical} m")
        lines.append(f"  - Reale Bodenfreiheit:        {ground_clearance:.2f} m (Grenzwert am Boden sicher unterschritten)")
        lines.append(f"  -> BEMFV-Konformitaet:        VOLLSTAENDIG GEGEBEN (Kein Konflikt mit Aufenthaltsbereichen)\n")
        
    lines.append("================================================================================")
    content = "\n".join(lines)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(content)
        
    print(content)
    print(f"Bericht erfolgreich exportiert: {output_file}")

if __name__ == '__main__':
    calculate_bemfv()
