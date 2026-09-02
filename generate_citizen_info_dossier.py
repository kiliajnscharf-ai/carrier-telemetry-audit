import datetime

def generate_citizen_dossier():
    print("================================================================================")
    print("PROJEKT HAUS IM WIND: KOMMUNALE BUERGER- & TRANSPARENZ-MATRIX (PLATZ 1)")
    print("================================================================================")

    doc = f"""================================================================================
BUERGERINFORMATION: AUTARKE MOBILFUNK- & KRISENINFRASTRUKTUR
LIEGENSCHAFTS-CLUSTER 2026 (HAUS IM WIND)
================================================================================
Datum:             {datetime.datetime.now().strftime('%d.%m.%Y')}
Herausgeber:       Kilian Scharf (Liegenschafts- und Infrastrukturmanagement)
Zielgruppe:        Bürgerinnen, Bürger und Anwohner der Gemeinde

1. WARUM DIESES PROJEKT DEM GEMEINWOHL DIENT
--------------------------------------------------------------------------------
- Schließung bestehender Mobilfunk-Funklöcher und Sicherstellung stabiler 4G/5G-Netze.
- Höchste Notstrom-Ausfallsicherheit: 72h-LiFePO4-Speicher garantieren Netzbetrieb,
  wenn das öffentliche Stromnetz bei Sturm oder Blackout ausfällt (BSI-KRITIS).
- Kostenloses Notfunknetz: Dezentrales 868-MHz-Bürger-Mesh für Notfall-SMS und
  Katastrophenmeldungen bei Mobilfunkausfall.

2. FAKTEN ZUR GESUNDHEIT & STRAHLUNGSSCHUTZ (26. BIMSCHV)
--------------------------------------------------------------------------------
- Gesetzliche Grenzwerte:    Vollumfänglich eingehalten nach DIN EN 50383 / BNetzA STOB.
- Gemessene Ausschöpfung:    Am Boden beträgt die Feldstärke maximal 8.87 % des Grenzwerts.
- Über 91 % Sicherheitsreserve für Mensch, Tier und Umwelt.

3. BAULICHE UND OEKOLOGISCHE VERANTWORTUNG
--------------------------------------------------------------------------------
- Vollständig emissionsfreier Betrieb ohne Dieselaggregate.
- Witterungs- und schadstofffreie Montage (Otto-Chemie / Fischer Verankerung).
- Vollständiger Ausgleich der Bodenversiegelung durch ökologische Begleitmaßnahmen.

================================================================================
STATUS: BUERGERINFORMATION EINSATZBEREIT FUER GEMEINDE UND AUSHANG (PLATZ 1).
================================================================================
"""
    filename = "BUERGERINFORMATION_CLUSTER_2026.txt"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(doc)
    print(f"Bürgerinformationsblatt erfolgreich generiert: {filename}")
    print(doc)

if __name__ == '__main__':
    generate_citizen_dossier()
