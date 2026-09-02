import pandas as pd
import numpy as np
import sys
import os

def normalize_csv(input_path, output_excel='Batch_P1_Auswertung.xlsx'):
    if not os.path.exists(input_path):
        print(f"Fehler: Datei {input_path} existiert nicht.")
        sys.exit(1)
        
    df = pd.read_csv(input_path)
    cols = {str(c).lower().strip(): c for c in df.columns}
    
    def get_col(possible_names, default=None):
        for name in possible_names:
            if name in cols:
                return cols[name]
        return default

    id_col = get_col(['id', 'site_id', 'standort_id', 'kennung'], default=df.columns[0])
    name_col = get_col(['name', 'bezeichnung', 'site_name', 'standort'], default=df.columns[1])
    lat_col = get_col(['breitengrad', 'lat', 'latitude', 'y', 'lat_wgs84'])
    lon_col = get_col(['laengengrad', 'lon', 'lng', 'longitude', 'x', 'long'])
    alt_col = get_col(['hoehe_m', 'hoehe', 'altitude_m', 'elevation', 'height', 'alt'], default=None)
    power_col = get_col(['stromdistanz_m', 'stromdistanz', 'power_dist_m', 'dist_power'], default=None)
    road_col = get_col(['zuwegung_m', 'zuwegung', 'access_road_m', 'road_dist'], default=None)
    prio_col = get_col(['funkloch_prio', 'prio', 'priority', 'ranking'], default=None)

    if not lat_col or not lon_col:
        print(f"Fehler: Geokoordinaten (Breitengrad/Längengrad) konnten nicht identifiziert werden.")
        sys.exit(1)

    normalized_data = []
    print("================================================================================")
    print("UNIVERSAL INGESTION ENGINE: SELBSTADAPTIVE NORMALISIERUNG (GLOBAL TIER-1)")
    print("================================================================================")

    for _, row in df.iterrows():
        s_id = str(row[id_col])
        s_name = str(row[name_col])
        lat = float(row[lat_col])
        lon = float(row[lon_col])
        alt = float(row[alt_col]) if alt_col else 250.0
        dist_power = float(row[power_col]) if power_col else 30.0
        dist_road = float(row[road_col]) if road_col else 50.0
        prio = int(row[prio_col]) if prio_col else 1

        # 4-Faktoren-Scoring-Modell (Max 100 Punkte)
        score_alt = min(30, (alt / 350.0) * 30.0)
        score_power = max(0, 30.0 - (dist_power * 0.3))
        score_road = max(0, 20.0 - (dist_road * 0.15))
        score_prio = 20.0 if prio == 1 else 10.0
        total_score = round(score_alt + score_power + score_road + score_prio, 1)
        p1_status = "P1 (Prioritaet 1)" if total_score >= 60.0 else "P2 (Reserve)"

        normalized_data.append({
            'ID': s_id,
            'Name': s_name,
            'Breitengrad': lat,
            'Laengengrad': lon,
            'Hoehe_m': alt,
            'Stromdistanz_m': dist_power,
            'Zuwegung_m': dist_road,
            'Funkloch_Prio': prio,
            'Score': total_score,
            'Status': p1_status
        })
        print(f"Standort {s_id} ({s_name}): Lat={lat}, Lon={lon}, Hoehe={alt}m -> Score: {total_score} [{p1_status}]")

    res_df = pd.DataFrame(normalized_data)
    p1_df = res_df[res_df['Status'].str.startswith('P1')].copy()
    if p1_df.empty:
        p1_df = res_df.copy()

    p1_df.to_excel(output_excel, index=False)
    print("================================================================================")
    print(f"Normalisierung abgeschlossen. {len(p1_df)} von {len(res_df)} Standorten als P1 exportiert: {output_excel}")
    print("================================================================================")

if __name__ == '__main__':
    src = sys.argv[1] if len(sys.argv) > 1 else 'neue_suchkreise.csv'
    normalize_csv(src)
