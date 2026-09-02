import json
import csv

with open("alle_standorte.geojson", "r") as f:
    geojson_data = json.load(f)

p1_features = []
p1_rows = []

for feature in geojson_data["features"]:
    props = feature["properties"]
    coords = feature["geometry"]["coordinates"]
    
    if props.get("priority") == "P1":
        p1_features.append(feature)
        p1_rows.append({
            "ID": props["id"],
            "Name": props["name"],
            "Breitengrad": coords[1],
            "Laengengrad": coords[0],
            "Hoehe_m": props["altitude_m"],
            "Strom_Distanz_m": props["power_distance_m"],
            "Zuwegung": props["access"],
            "Fehlende_Betreiber": props["missing_operators"],
            "Score": props["score"],
            "Prioritaet": props["priority"]
        })

# 1. P1-GeoJSON speichern
p1_geojson = {
    "type": "FeatureCollection",
    "features": p1_features
}
with open("p1_standorte.geojson", "w") as f:
    json.dump(p1_geojson, f, indent=2)

# 2. P1-CSV für Tabellenkalkulation / Excel speichern
if p1_rows:
    with open("p1_standorte_einreichung.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=p1_rows[0].keys(), delimiter=";")
        writer.writeheader()
        writer.writerows(p1_rows)

print("=" * 70)
print(f"Filterung abgeschlossen: {len(p1_rows)} P1-Standort(e) extrahiert.")
print("- p1_standorte.geojson (GIS-Format)")
print("- p1_standorte_einreichung.csv (Excel-/Office-Format)")
print("=" * 70)
