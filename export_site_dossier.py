with open("standort_51_9850_9_2550.geojson", "r") as f:
    import json
    data = json.load(f)

p = data["properties"]
c = data["geometry"]["coordinates"]

dossier_text = f"""================================================================================
STANDORT-DOSSIER FUER MOBILFUNK-INFRASTRUKTUR (P1)
================================================================================

1. STANDORTDATEN:
- Bezeichnung:        {p['name']}
- Geokoordinaten:     {c[1]:.6f} N, {c[0]:.6f} E (WGS84)
- Topografie / Hoehe: {p['altitude_m']} m ue. NN (Exponierte Huegellage)
- Gelaendeart:        Freiflaeche am Wirtschaftsweg
- Erschliessung:      Stromtrasse in {p['power_distance_m']} m Entfernung vorhanden
- Zuwegung:           {p['access']} fuer Montagefahrzeuge geeignet

2. FUNKTECHNISCHE BEWERTUNG:
- Gesamt-Score:       {p['score']} / 10 (Prioritaetsstufe: {p['priority']})
- Empfohlene Baender: Band 28 (700 MHz), Band 20 (800 MHz), Band 8 (900 MHz)
- Versorgungsradius:  ca. 5 - 8 km zur Schliessung lokaler Funkloecher

3. VERSORGUNGSSITUATION VOR ORT:
- Vodafone:           {p['status_vodafone']} (Strukturelles Funkloch)
- O2 Telefonica:      {p['status_o2']} (Strukturelles Funkloch)
- 1&1 Mobilfunk:      {p['status_1und1']} (Keine Netzabdeckung)
- Deutsche Telekom:   {p['status_telekom']} (Kritische Randversorgung)

4. BEWERTUNG FUER TOWERCOS:
Der Standort bietet maximale Flaechenwirkung bei minimalen Erschliessungskosten.
Geeignet fuer standardisierte Schleuderbeton- oder Gittermasten (30-40 m).
================================================================================
"""

with open("Mobilfunk_Standort_Dossier.txt", "w") as f:
    f.write(dossier_text)

print("Dossier erfolgreich exportiert: Mobilfunk_Standort_Dossier.txt")
