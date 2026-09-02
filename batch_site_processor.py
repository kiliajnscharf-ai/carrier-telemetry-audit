import json

# Eingabedatensatz: Liste potenzieller Standorte
sites_input = [
    {
        "id": "LOC-01",
        "name": "Standort A - Bad Pyrmont Huegel",
        "lat": 51.9850,
        "lon": 9.2550,
        "altitude_m": 250,
        "los": "frei",
        "power_dist_m": 30,
        "access": "Wirtschaftsweg",
        "missing_operators": 3,  # Vodafone, O2, 1&1 < -115 dBm
        "telekom_rsrp": "-105 bis -115 dBm"
    },
    {
        "id": "LOC-02",
        "name": "Standort B - Talsohle Waldrand",
        "lat": 51.9720,
        "lon": 9.2310,
        "altitude_m": 140,
        "los": "teilweise",
        "power_dist_m": 250,
        "access": "Unbefestigt",
        "missing_operators": 2,  # Vodafone, 1&1
        "telekom_rsrp": "-95 dBm"
    },
    {
        "id": "LOC-03",
        "name": "Standort C - Gewerbegebiet Ost",
        "lat": 51.9910,
        "lon": 9.2800,
        "altitude_m": 190,
        "los": "frei",
        "power_dist_m": 15,
        "access": "Asphaltiert",
        "missing_operators": 1,  # nur 1&1 fehlt
        "telekom_rsrp": "-85 dBm"
    }
]

def calculate_score(site):
    # 1. Defizit (35%)
    if site["missing_operators"] >= 3:
        deficit_pts = 10.0
    elif site["missing_operators"] == 2:
        deficit_pts = 7.5
    elif site["missing_operators"] == 1:
        deficit_pts = 4.0
    else:
        deficit_pts = 1.0

    # 2. Topografie & Hoehe (30%)
    if site["altitude_m"] >= 240 and site["los"] == "frei":
        topo_pts = 9.5
    elif site["altitude_m"] >= 180:
        topo_pts = 7.5
    else:
        topo_pts = 4.0

    # 3. Stromanbindung (20%)
    if site["power_dist_m"] <= 30:
        power_pts = 9.5
    elif site["power_dist_m"] <= 100:
        power_pts = 7.5
    elif site["power_dist_m"] <= 300:
        power_pts = 5.0
    else:
        power_pts = 2.0

    # 4. Zuwegung (15%)
    if site["access"] == "Asphaltiert":
        access_pts = 10.0
    elif site["access"] == "Wirtschaftsweg":
        access_pts = 7.5
    else:
        access_pts = 3.0

    total_score = round(
        (deficit_pts * 0.35) + (topo_pts * 0.30) + (power_pts * 0.20) + (access_pts * 0.15), 2
    )

    if total_score >= 8.50:
        priority = "P1"
    elif total_score >= 7.00:
        priority = "P2"
    elif total_score >= 5.00:
        priority = "P3"
    else:
        priority = "P4"

    return total_score, priority

# Batch-Verarbeitung und GeoJSON-Erstellung
features = []

print("=" * 80)
print(f"{'ID':<8}{'STANDORTNAME':<32}{'HOEHE':<10}{'STROM':<10}{'SCORE':<10}{'PRIO':<6}")
print("=" * 80)

for s in sites_input:
    score, prio = calculate_score(s)
    s["score"] = score
    s["priority"] = prio

    print(f"{s['id']:<8}{s['name']:<32}{str(s['altitude_m']) + 'm':<10}{str(s['power_dist_m']) + 'm':<10}{score:<10}{prio:<6}")

    feature = {
        "type": "Feature",
        "geometry": {
            "type": "Point",
            "coordinates": [s["lon"], s["lat"]]
        },
        "properties": {
            "id": s["id"],
            "name": s["name"],
            "altitude_m": s["altitude_m"],
            "power_distance_m": s["power_dist_m"],
            "access": s["access"],
            "missing_operators": s["missing_operators"],
            "score": score,
            "priority": prio
        }
    }
    features.append(feature)

geojson_collection = {
    "type": "FeatureCollection",
    "features": features
}

with open("alle_standorte.geojson", "w") as f:
    json.dump(geojson_collection, f, indent=2)

print("=" * 80)
print("Batch-Erfassung abgeschlossen: alle_standorte.geojson gespeichert.")
