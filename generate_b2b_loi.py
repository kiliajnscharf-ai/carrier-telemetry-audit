import datetime

def generate_loi(location_id, location_name, area_sqm, base_rent):
    loi_text = f"""================================================================================
LETTER OF INTENT (LOI) & GESTATTUNGS-VORVERTRAG
ZUR ERRICHTUNG EINER MOBILFUNK-SENDESTELLE (CLUSTER 2026)
================================================================================
Standort-ID:       {location_id}
Bezeichnung:       {location_name}
Datum:             {datetime.datetime.now().strftime('%d.%m.%Y')}
Rechtsrahmen:      Bürgerliches Gesetzbuch (BGB) §§ 535 ff., 1090

ZWISCHEN:
1. Liegenschaftseigentümer / Verfügungsberechtigter (nachfolgend "Eigentümer")
   und
2. Kilian Scharf (Liegenschafts- und Infrastrukturmanagement, nachfolgend "Akquisiteur")

PRÄAMBEL:
Der Akquisiteur projektiert auf dem Grundstück des Eigentümers eine Mobilfunk-Infrastruktur-
anlage zur Schließung regionaler Versorgungslücken und zur Bereitstellung von 5G-/6G-Diensten
im Auftrag bzw. zur Übergabe an lizenzierte Betreiber (Vantage Towers AG, Deutsche Funkturm GmbH,
Telekom, Vodafone, Telefónica, 1&1).

 1 VERTRAGSGEGENSTAND & FLÄCHENNUTZUNG
1. Der Eigentümer gestattet dem Akquisiteur sowie den beauftragten Betreibern die Nutzung einer
   Teilfläche von ca. {area_sqm} m² (gemäß Lageplan) zur Errichtung eines Schleuderbeton-/Gitter-
   mastes, Aufstellung von Systemtechnik-Schränken sowie einer BSI-KRITIS-konformen 72h-USV-Anlage.
2. Der Eigentümer gewährt ein jederzeitiges, ungehindertes Zugangs- und Zufahrtsrecht (24/7/365)
   für Wartungs- und Notfalleinsätze über die bestehenden Wege.

 2 EXKLUSIVITÄT & PRÜFZEITRAUM
1. Der Eigentümer räumt dem Akquisiteur ein ausschließliches, unwiderrufliches Nutzungs- und
   Prüfrecht für die Dauer von 24 Monaten ab Unterzeichnung dieses LOI ein.
2. Während dieser Frist wird der Eigentümer keine Verhandlungen mit Dritten über Mobilfunk-
   anlagen auf dem genannten Grundstück führen.

 3 KONDITIONEN DES HAUPTMIETVERTRAGES
1. Nach erfolgreicher Genehmigungs- und Netzprüfung wird ein Hauptmietvertrag über eine
   Festlaufzeit von 20 Jahren (mit 4 x 5 Jahren automatischer Verlängerungsoption) geschlossen.
2. Die Grundpacht beträgt {base_rent:.2f} EUR / Monat (wertgesichert gemäß Verbraucherpreisindex).
3. Für jeden weiteren aufgeschalteten Betreiber (Multi-Tenancy / Co-Location) wird ein
   Zusatzzuschlag von 375,00 EUR / Monat gewährt.

 4 DINGLICHE ABSICHERUNG
Der Eigentümer verpflichtet sich, zur Sicherung der Anlage im Grundbuch an nächstbereiter Stelle
eine beschränkte persönliche Dienstbarkeit (§ 1090 BGB) zugunsten des Betreibers eintragen zu lassen.

 5 BEMFV & REGULATORISCHE BESTIMMUNGEN
Die Anlage wird unter strikter Einhaltung der 26. BImSchV sowie der DIN EN 50383 projektiert.
Eine gültige Standortbescheinigung (STOB) der Bundesnetzagentur ist zwingende Voraussetzung
für die Inbetriebnahme.

================================================================================
Ort, Datum: _______________________      Ort, Datum: Bad Pyrmont, {datetime.datetime.now().strftime('%d.%m.%Y')}


___________________________________      ___________________________________
Unterschrift Eigentümer                  Unterschrift Kilian Scharf
================================================================================
"""
    filename = f"B2B_LOI_{location_id}.txt"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(loi_text)
    print(f"Gestattungs-LoI erfolgreich generiert: {filename}")

def main():
    print("================================================================================")
    print("B2B GESTATTUNGS- UND LOI-GENERATOR: CLUSTER 2026")
    print("================================================================================")
    locations = [
        {"id": "LOC-30", "name": "Westflanke Forsthaus", "area": 120, "rent": 1250.00},
        {"id": "LOC-31", "name": "Talstation Süd",       "area": 150, "rent": 1350.00},
        {"id": "LOC-32", "name": "Bergkuppe Nordost",    "area": 100, "rent": 1400.00}
    ]
    for loc in locations:
        generate_loi(loc["id"], loc["name"], loc["area"], loc["rent"])
    print("================================================================================")
    print("STATUS: ALLE 3 STANDORT-VERTRAEGE SCHLUESSELFERTIG ERSTELLT.")
    print("================================================================================")

if __name__ == '__main__':
    main()
