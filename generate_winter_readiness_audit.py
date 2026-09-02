import datetime

def generate_winter_audit():
    print("================================================================================")
    print("PROJEKT HAUS IM WIND: B2B-WINTERFESTIGKEITS- & WITTERUNGSAUDIT (PHASE 30)")
    print("================================================================================")

    now_str = datetime.datetime.now().strftime('%d.%m.%Y')

    audit_text = f"""================================================================================
B2B-WINTERFESTIGKEITS- & FROSTSCHUTZPRUEFPLAN (DIN EN 50308 / VDE 0100)
LIEGENSCHAFTS-CLUSTER 2026 (LOC-30 / LOC-31 / LOC-32)
================================================================================
Stand:             {now_str}
Verantwortlich:    Kilian Scharf (Liegenschafts- und Infrastrukturmanagement)
Prüfperiode:       Herbst/Winter 2026/2027 | Schutzklasse: Tier-1 KRITIS

1. THERMALMANAGEMENT LIFEPO4-BATTERIESPEICHER (288 KWH)
--------------------------------------------------------------------------------
[ ] 1.1 Frostschutz-Heizung:     Funktion der PTC-Heizregister im Container verifiziert
[ ] 1.2 Ladesperre BMS:          BMS-Notabschaltung bei Zelltemperatur < 0 °C aktiv
[ ] 1.3 Isolationsüberwachung:   Wand- und Bodendämmung (Mineralwolle A1) intakt
[ ] 1.4 Lüftungsklappen:         Thermostatgesteuerte Zuluftklappen schließen dicht

2. MECHANISCHE WITTERUNGS- & EISSCHLAGPRUEFUNG
--------------------------------------------------------------------------------
[ ] 2.1 Eisschutzhauben:         Abweiser über GPS- und Richtfunkantennen fest montiert
[ ] 2.2 Fugen & Durchführungen:  Alle Wandanschlüsse mit OTTOSEAL S 110 nachversiegelt
[ ] 2.3 Steigschutzschiene:      Eisfreihaltung und Leichtgängigkeit der Auffangstrecke
[ ] 2.4 Fundamententwässerung:   Kiesbett und Drainagerohre laub- und schlammfrei

3. ZUWEGUNG & NOTFALL-LOGISTIK IM WINTER
--------------------------------------------------------------------------------
[ ] 3.1 Räum- und Streuplan:     Zugang zum Technikraum bei Schneefall < 4h geräumt
[ ] 3.2 Streugutvorrat:          200 kg salzfreies Granulat im Lager vorrätig
[ ] 3.3 Notbeleuchtung:          Akku-Arbeitsscheinwerfer geladen und winterfest

================================================================================
STATUS: WINTERFESTIGKEITSPLAN EINSATZBEREIT FUER DEN VOR-ORT-CHECK (PLATZ 1).
================================================================================
"""
    filename = "B2B_WINTERFESTIGKEIT_PLAN.txt"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(audit_text)
    print(f"Winterfestigkeitsplan erfolgreich generiert: {filename}")
    print(audit_text)

if __name__ == '__main__':
    generate_winter_audit()
