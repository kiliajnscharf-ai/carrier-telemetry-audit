import geojson

feature = geojson.Feature(
    geometry=geojson.Point((9.2550, 51.9850)),
    properties={
        "name": "Mobilfunkstandort 51.9850_9.2550",
        "altitude_m": 250,
        "score": 9.13,
        "priority": "P1",
        "status_vodafone": "RSRP < -115 dBm",
        "status_o2": "RSRP < -115 dBm",
        "status_1und1": "No Service",
        "status_telekom": "RSRP -105 to -115 dBm",
        "power_distance_m": 30,
        "access": "Wirtschaftsweg"
    }
)

with open("standort_51_9850_9_2550.geojson", "w") as f:
    geojson.dump(feature, f, indent=2)

print("GeoJSON-Datei erfolgreich erstellt: standort_51_9850_9_2550.geojson")
