import datetime

def generate_access_plan():
    print("================================================================================")
    print("PROJEKT HAUS IM WIND: B2B-SCHLUESSEL- & ZUTRITTSKONTROLLPLAN (PHASE 26)")
    print("================================================================================")

    now = datetime.datetime.now().strftime('%d.%m.%Y %H:%M:%S')

    plan = f"""================================================================================
B2B-SCHLUESSEL- & ZUTRITTSKONTROLLPLAN (VDI 3586 / DIN 18252)
LIEGENSCHAFT: HAUS IM WIND | CLUSTER 2026
================================================================================
Stand:             {now}
Verantwortlich:    Kilian Scharf (Liegenschafts- und Infrastrukturmanagement)
Sicherheitsstufe:  KRITIS-konform / Schutzbereich gegen Sabotage

1. SCHLIESSZYLINDER- & BERECHTIGUNGSMATRIX
--------------------------------------------------------------------------------
Zylinder-ID | Bereich / Raum           | Schloss-Typ        | Berechtigte Personen
--------------------------------------------------------------------------------
Z-01        | Zufahrtstor Außenbereich | Profil-Doppelzyl.  | Kilian Scharf, TowerCo, Feuerwehr
Z-02        | Technikraum Hauptverteil.| DIN 18252 PZ       | Kilian Scharf, VNB, Betreiber
Z-03        | 288-kWh-LiFePO4-Container| Hochsicherheit VdS | Kilian Scharf (Exklusiv / KRITIS)
Z-04        | Mastfuß-Sicherheitszaun  | Bügelschloss VdS   | Kilian Scharf, Montage-Teams GU

2. SCHLUESSELAUSGABE- & RUECKGABEPROTOKOLL (VORLAGE)
--------------------------------------------------------------------------------
Ausgabedatum:      ____.____.2026   Uhrzeit: ____:____ Uhr
Empfänger:         ____________________________________________________________
Firma / Funktion:  [ ] Vantage Towers  [ ] DFMG  [ ] GU/Sub  [ ] EVU
Zylinder / Key-ID: [ ] Z-01   [ ] Z-02   [ ] Z-03   [ ] Z-04
Rückgabetermin:    ____.____.2026   geplante Einsatzdauer: ____ Std.

VERPFLICHTUNG:
Der Empfänger verpflichtet sich, Schlüssel nicht zu duplizieren, Türen stets
verschlossen zu halten und den Verlust unverzüglich der Liegenschaftsleitung
zu melden.

Unterschrift Empfänger:                     Unterschrift Kilian Scharf:

________________________________________    ________________________________________

================================================================================
STATUS: ZUTRITTS- & SCHLUESSELPLAN EINSATZBEREIT (PLATZ 1).
================================================================================
"""
    filename = "B2B_SCHLUESSEL_ZUTRITTSPLAN.txt"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(plan)
    print(f"Zutrittsplan erfolgreich generiert: {filename}")
    print(plan)

if __name__ == '__main__':
    generate_access_plan()
