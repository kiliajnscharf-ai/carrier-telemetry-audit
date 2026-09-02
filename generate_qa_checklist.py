import datetime

def build_qa_checklist():
    print("================================================================================")
    print("PROJEKT HAUS IM WIND: B2B-QUALITAETSSICHERUNGS- & MONTAGE-AUDIT (PLATZ 1)")
    print("================================================================================")

    qa_report = f"""================================================================================
TIER-1 QUALITAETSSICHERUNGS- UND WERKSTATT-AUDITPROTOKOLL
HERSTELLERKONFORME MONTAGE- UND VERARBEITUNGSRICHTLINIE
================================================================================
Standort:          Cluster 2026 (LOC-30 / LOC-31 / LOC-32)
Prüfstandard:      DIN EN ISO 6789, ETA-04/0043, DIN EN 61238-1, DIN 18531
Prüfer / Leitung:  Kilian Scharf (Autarke Liegenschaftsinstandhaltung Haus im Wind)
Datum:             {datetime.datetime.now().strftime('%d.%m.%Y %H:%M:%S')}

1. FISCHER SCHWERLAST-VERANKERUNG (ETA OPTION 1 PRÜFUNG)
--------------------------------------------------------------------------------
[ ] 1.1 Bohrlochtiefe & Durchmesser:  Bohrloch exakt 28 mm für M24 (Soll: 240 mm Tiefe)
[ ] 1.2 Reinigungsprozess:            4x Druckluftölfrei -> 4x Stahlbürste -> 4x Druckluft
[ ] 1.3 Mörtelextrakt:                Erste 10 cm Mörtelstrang verworfen (Farbmischung homogen)
[ ] 1.4 Aushärtezeit eingehalten:     Temperaturabhängig (z.B. 120 min bei 20°C Betontemp.)
[ ] 1.5 Setzkontrolle:                Mörtelaustritt am Bohrlochrand ringsum ringförmig sichtbar

2. WERA SCHRAUB- UND DREHMOMENT-PROTOKOLLIERUNG
--------------------------------------------------------------------------------
[ ] 2.1 Werkzeugkalibrierung:         Click-Torque D 6 Zertifikat nach ISO 6789 gültig (< 12 Mo.)
[ ] 2.2 Mastfußverschraubung M24:     Anzug mit 245 Nm (Kein Schlagschrauber-Nachschlag!)
[ ] 2.3 Antennenausleger M16:         Anzug mit 120 Nm kalibriert
[ ] 2.4 Schaltschrank-Klemmen:        Drehmoment-Schraubendreher 3.5 Nm (VDE 1000V)
[ ] 2.5 Visuelle Sicherung:           Schraubensicherungslack (Rot) über Mutter und Gewinde

3. KNIPEX CRIMP- UND ELEKTROINSTALLATIONSPRÜFUNG
--------------------------------------------------------------------------------
[ ] 3.1 Backenprofil:                 Hexagonal-Gesenk exakt passend zum Querschnitt
[ ] 3.2 Pressbild-Prüfung:            Vollständige Formschließung, kein seitlicher Grataustrieb
[ ] 3.3 Zugentlastungs-Test:          Axialer Rucktest nach DIN EN 61238-1 bestanden
[ ] 3.4 Schrumpfschlauch-Isolation:   Innenkleber-Schrumpfschlauch blasenfrei aufgeschrumpft
[ ] 3.5 Potentialausgleich 50 mm²:    Kontaktflächen metallisch blank, mit Polfett geschützt

4. OTTO-CHEMIE VERSIEGELUNGS- UND DICHTSTOFF-AUDIT
--------------------------------------------------------------------------------
[ ] 4.1 Untergrundvorbereitung:       Reinigung mit OTTO Cleaner T, absolut fett- und staubfrei
[ ] 4.2 Primer-Applikation:           OTTO Primer 1216 auf metallischen / mineralischen Flanken
[ ] 4.3 Fugenabmessung:               Dreiecksfase min. 10x10 mm, kein 3-Flanken-Haftungsfehler
[ ] 4.4 Glättmittel-Einsatz:          OTTO Glättmittel neutral, keine Spülmittel-Zusätze
[ ] 4.5 Brandschott-Verschluss:       OTTO Firestop Silikon min. 25 mm Schichtdicke (EI 120)

5. AUTARKE LIFEPO4-USV-SYSTEMINTEGRATION
--------------------------------------------------------------------------------
[ ] 5.1 Innenwiderstands-Messung:     Zell-Innenwiderstände < 0.25 mOhm, symmetrisch
[ ] 5.2 Drehmoment Polbolzen:         M8 Pole exakt mit 9.0 Nm angezogen (Wera A 5)
[ ] 5.3 BMS-Kommunikation:            CAN-Bus Schnittstelle aktiv, Einzelzellenüberwachung OK
[ ] 5.4 72h-Stresstest-Simulation:    Simulierter Netzausfall, Umschaltzeit < 15 ms verifiziert

================================================================================
BEWERTUNG: 100%IGE EINHALTUNG SICHERT 20 JAHRE WARTUNGSFREIEN BETRIEB (PLATZ 1)
================================================================================
"""
    filename = "B2B_MONTAGE_AUDIT_CHECKLISTE.txt"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(qa_report)
    print(f"Checkliste erfolgreich generiert: {filename}")
    print(qa_report)

if __name__ == '__main__':
    build_qa_checklist()
