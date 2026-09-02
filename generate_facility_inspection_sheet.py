import datetime

def generate_inspection_sheet():
    print("================================================================================")
    print("PROJEKT HAUS IM WIND: B2B-LIEGENSCHAFTS- & WERKSTATT-AUDIT (PHASE 24)")
    print("================================================================================")

    now = datetime.datetime.now().strftime('%d.%m.%Y')

    doc = f"""================================================================================
B2B-VOR-ORT-INSPEKTIONSPLAN & HAUSMEISTER-AUDIT
OBJEKT: HAUS IM WIND | LIEGENSCHAFTSMANAGEMENT
================================================================================
Datum:             {now}
Verantwortlich:    Kilian Scharf (Liegenschafts- und Infrastrukturmanagement)
Standard:          DIN 31051 (Instandhaltung) / Premium-Werkzeugstandard

1. PHYSISCHE ZUWEGUNG & AUFSTELLFLAECHEN
--------------------------------------------------------------------------------
[ ] 1.1 Zufahrtswege:            Frei von Bewuchs, Ästen und Hindernissen (Breite >= 3.50 m)
[ ] 1.2 Tragfähigkeit Untergrund:Schotter-/Betonflächen sichtgeprüft auf Risse oder Absackungen
[ ] 1.3 Montagekorridor:         Freiraum für Kran- und Hebebühnenaufstellung sichergestellt
[ ] 1.4 Entwässerung:            Bodenabläufe und Rinnen im Außenbereich laub- und schlammfrei

2. ELEKTROTECHNIK & TECHNIKRAUM (VDE / TAB)
--------------------------------------------------------------------------------
[ ] 2.1 Zähler- und Hauptraum:   Freiraum vor Schaltschränken min. 1.20 m geräumt
[ ] 2.2 Feuchtigkeitskontrolle:  Wanddurchführungen trocken, keine Schimmel- oder Wasserbildung
[ ] 2.3 Potentialausgleich:      Haupterdungsschiene (HES) zugänglich, Kontakte korrosionsfrei
[ ] 2.4 Beleuchtung Technikraum: Not- und Arbeitsbeleuchtung funktionsfähig

3. WERKSTATT- & MATERIALINVENTAR (PREMIUM-KLASSE)
--------------------------------------------------------------------------------
[ ] 3.1 Fischer Verankerung:     FIS EM Plus Kartuschen haltbar, Statikmischer vorrätig
[ ] 3.2 Wera Werkzeugsatz:       Drehmomentschlüssel (DIN EN ISO 6789) kalibriert und einsatzbereit
[ ] 3.3 Knipex Installationsset: Crimp- und Abisolierwerkzeuge gereinigt und leichtgängig
[ ] 3.4 Otto-Chemie Dichtstoffe: OTTOSEAL S 110 Kartuschen ungeöffnet, Düsenspitzen sauber

================================================================================
STATUS: INSPEKTIONSBOGEN BEREIT FUER DIE PRAKTISCHE VOR-ORT-BEGEHUNG (PLATZ 1).
================================================================================
"""
    filename = "B2B_LIEGENSCHAFTS_INSPEKTION.txt"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(doc)
    print(f"Inspektionsplan erfolgreich generiert: {filename}")
    print(doc)

if __name__ == '__main__':
    generate_inspection_sheet()
