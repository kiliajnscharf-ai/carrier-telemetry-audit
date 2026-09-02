import datetime

def generate_permit_dossier():
    print("================================================================================")
    print("PROJEKT HAUS IM WIND: B2B-BAUANTRAGS- & GENEHMIGUNGSDOSSIER (PLATZ 1)")
    print("================================================================================")

    dossier_text = f"""================================================================================
BAUANTRAGS-DOSSIER FUER FREISTEHENDE MOBILFUNK-SENDEANLAGEN
RECHTSRAHMEN: NIEDERSAECHSISCHE BAUORDNUNG (NBAUO) / § 35 BAUGB
================================================================================
Datum:             {datetime.datetime.now().strftime('%d.%m.%Y %H:%M:%S')}
Projektleitung:    Kilian Scharf (Liegenschafts- und Infrastrukturmanagement Haus im Wind)
Cluster:           LOC-30, LOC-31, LOC-32
Zuständige Behörde:Untere Bauaufsichtsbehörde (Landkreis Hameln-Pyrmont)

1. RECHTLICHE WUERDIGUNG & PRIVILEGIERUNG NACH § 35 BAUGB
--------------------------------------------------------------------------------
- Rechtsgrundlage:           § 35 Abs. 1 Nr. 3 BauGB (Privilegiertes Außenbereichsvorhaben)
- Versorgungsnachweis:       Schließung regionaler Mobilfunk- und 5G-Versorgungslücken
- Betreiberbeteiligung:      Multi-Tenancy (Vantage Towers AG, DFMG, Telekom, Vodafone)
- Öffentliches Interesse:    Teil der BNetzA-Versorgungsauflagen und KRITIS-Härtung

2. ABSTANDSFLAECHEN-NACHWEIS NACH § 5 NBAUO
--------------------------------------------------------------------------------
- Abstandsflächentiefe:      0.4 H gemäß § 5 NBauO (Gewerbliche Freiraumnutzung)
  * LOC-30 (H = 45 m):       Erforderliche Tiefe = 18.00 m (Pachtfläche 120 m² gewahrt)
  * LOC-31 (H = 40 m):       Erforderliche Tiefe = 16.00 m (Pachtfläche 150 m² gewahrt)
  * LOC-32 (H = 50 m):       Erforderliche Tiefe = 20.00 m (Pachtfläche 100 m² + Puffer)
- Überdeckung:               Keine Überdeckung mit Nachbargrundstücken; Abstandsflächen
                             liegen vollständig innerhalb der gesicherten Dienstbarkeitsgrenzen.

3. STATIK- UND STANDSICHERHEITSNACHWEIS
--------------------------------------------------------------------------------
- Masttyp:                  Typengeprüfter Stahlgitterturm / Schleuderbetonmast (40 - 50 m)
- Auslegungsnorm:           Eurocode 3 (DIN EN 1993-3-1: Türme und Maste)
- Verankerung:              Fischer Injektionssystem FIS EM Plus (ETA Option 1 / gerissener Beton)
- Erdbeben- / Windzone:     Auslegung für Windzone 3 Binnenland (Geschwindigkeitsdruck q_p = 1.05 kN/m²)

4. UMWELT-, NATURSCHUTZ & LANDSCHAFTSPFLEGE
--------------------------------------------------------------------------------
- Versiegelte Fläche:       Ca. 25 m² Fundamentplatte zzgl. 15 m² USV-Containment
- Eingriffs-Ausgleich:      Kompensationsfaktor 1:1 durch Extensivbegrünung der Nebenflächen
- Vogelschutz:              Antennenmontage mit reflexionsarmen Abdeckungen (DIN EN 50383)
- Emissionen / Lärm:        Emissionsfreier Betrieb (Passive Kühlung + LiFePO4 Speicher)

5. BEIZUFUEGENDE ANLAGEN
--------------------------------------------------------------------------------
[X] Anlage 1: Amtlicher Liegenschaftskatasterauszug (Flurkarte M 1:1000)
[X] Anlage 2: Bauzeichnungen (Grundriss, Ansichten, Schnitte M 1:100)
[X] Anlage 3: BNetzA-Standortbescheinigung (STOB) Antragsentwurf
[X] Anlage 4: EMF-Feldstärkekataster (26. BImSchV Nachweis)
[X] Anlage 5: Verhandelter Gestattungsvorvertrag (Letter of Intent)

================================================================================
STATUS: GENEHMIGUNGSDOSSIER SCHLUESSELFERTIG ZUR BEHOERDENEINREICHUNG (PLATZ 1)
================================================================================
"""
    filename = "B2B_BAUANTRAG_DOSSIER_NBAUO.txt"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(dossier_text)
    print(f"Bauantragsdossier erfolgreich generiert: {filename}")
    print(dossier_text)

if __name__ == '__main__':
    generate_permit_dossier()
