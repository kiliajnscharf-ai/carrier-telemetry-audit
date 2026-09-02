import pandas as pd
import json
import os
import glob

def aggregate_clusters():
    geojson_files = glob.glob("*standorte*.geojson")
    excel_files = glob.glob("*Auswertung*.xlsx") + glob.glob("*Kalkulation*.xlsx")
    
    features = []
    processed_ids = set()
    
    # 1. GeoJSON Zusammenfuehrung
    for g_file in geojson_files:
        if "Master" in g_file:
            continue
        try:
            with open(g_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                for feat in data.get('features', []):
                    f_id = feat.get('properties', {}).get('id', feat.get('properties', {}).get('ID'))
                    if f_id and f_id not in processed_ids:
                        processed_ids.add(f_id)
                        features.append(feat)
        except Exception as e:
            print(f"Hinweis: Konnte {g_file} nicht parsen: {e}")
            
    master_geojson = {
        "type": "FeatureCollection",
        "name": "Master_Cluster_Deutschland_P1",
        "crs": { "type": "name", "properties": { "name": "urn:ogc:def:crs:OGC:1.3:CRS84" } },
        "features": features
    }
    
    with open("Master_Cluster_Deutschland.geojson", "w", encoding="utf-8") as f:
        json.dump(master_geojson, f, indent=2, ensure_ascii=False)
        
    print("================================================================================")
    print("MULTI-CLUSTER-AGGREGATION ERFOLGREICH DURCHGEFUEHRT")
    print("================================================================================")
    print(f"Konsolidierter Makro-Datensatz: Master_Cluster_Deutschland.geojson")
    print(f"Gesamtanzahl konsolidierter Standorte: {len(features)}")
    for feat in features:
        props = feat.get('properties', {})
        p_id = props.get('id', props.get('ID', 'N/A'))
        p_name = props.get('name', props.get('Name', 'N/A'))
        print(f"  -> Standort erfasst: [{p_id}] {p_name}")
    print("================================================================================")

if __name__ == '__main__':
    aggregate_clusters()
