import datetime

def generate_followup_engine():
    print("================================================================================")
    print("PROJEKT HAUS IM WIND: B2B-ESKALATIONS- & NACHFASS-ENGINE (PLATZ 1)")
    print("================================================================================")

    now = datetime.datetime.now().strftime('%d.%m.%Y %H:%M:%S')

    vantage_notice = f"""================================================================================
B2B-STATUSNACHFASSUNG & FRISTWAHRUNG (VANTAGE TOWERS AG)
STANDORT-CLUSTER 2026 | TICKETS: LLSM0135511 & LLSM0135540
================================================================================
Datum:             {now}
An:                Vantage Towers AG (Standortakquisition & Partnermanagement)
Referenz-Tickets:  LLSM0135511 (Standortdossier LOC-30 bis 32)
                   LLSM0135540 (B2B-Lieferanten- & Partnerakkreditierung)
Projektleitung:    Kilian Scharf (Liegenschafts- und Infrastrukturmanagement Haus im Wind)

Sehr geehrte Damen und Herren,

in Bezug auf die am 01.09.2026 übermittelten Standort- und Qualifikationsunterlagen
sowie die vereinbarte 14-tägige Regelprüffrist bis zum 15.09.2026 fassen wir
den aktuellen Bearbeitungsstand förmlich nach.

STATUS DER STANDORTE:
1. Bauantragsreife (NBauO / § 35 BauGB) für LOC-30, LOC-31 und LOC-32 liegt vor.
2. EMF-Immissionskataster nach 26. BImSchV weist eine Grenzwertausschöpfung von < 9 % nach.
3. Vor-Ort-Begehungsprotokolle (TSS) und Letter of Intent (LOI) liegen unterschriftsreif bereit.

Wir bitten um Bestätigung der technischen Eignungsprüfung sowie um Abstimmung
des Termins zur gemeinsamen Standortbegehung (TSS) vor Ort.

Mit freundlichen Grüßen
Kilian Scharf
Liegenschafts- und Infrastrukturmanagement Haus im Wind
================================================================================
"""

    dfmg_notice = f"""================================================================================
B2B-STATUSNACHFASSUNG & FRISTWAHRUNG (DEUTSCHE FUNKTURM GMBH - DFMG)
STANDORT-CLUSTER 2026 | VORGANG: DFMG-INCOMING-2026
================================================================================
Datum:             {now}
An:                Deutsche Funkturm GmbH (Standortakquise / Konzerneinkauf)
Referenz:          DFMG-INCOMING-2026 (Standorte LOC-30, LOC-31, LOC-32)
Projektleitung:    Kilian Scharf (Liegenschafts- und Infrastrukturmanagement Haus im Wind)

Sehr geehrte Damen und Herren,

zur Wahrung der Projektfristen für das Liegenschafts-Cluster 2026 fragen wir den
Stand der technischen Vorprüfung an.

Die Liegenschaften bieten sofortige Baureife im Außenbereich (§ 35 BauGB), eine
gesicherte Schwerlastzufahrt, 288-kWh-LiFePO4-USV-Pufferung (BSI-KRITIS) sowie
vorbereitete Multi-Tenancy-Kapazitäten.

Bitte teilen Sie uns zeitnah das Ergebnis der Suchkreis-Plausibilisierung mit,
damit die B2B-Gestattungsverträge finalisiert werden können.

Mit freundlichen Grüßen
Kilian Scharf
Liegenschafts- und Infrastrukturmanagement Haus im Wind
================================================================================
"""

    with open("ESCALATION_NOTICE_VANTAGE.txt", "w", encoding="utf-8") as f:
        f.write(vantage_notice)
    with open("ESCALATION_NOTICE_DFMG.txt", "w", encoding="utf-8") as f:
        f.write(dfmg_notice)

    print("Nachfass-Dossier Vantage Towers generiert: ESCALATION_NOTICE_VANTAGE.txt")
    print("Nachfass-Dossier DFMG generiert:           ESCALATION_NOTICE_DFMG.txt")
    print("================================================================================")
    print("STATUS: ESKALATIONS-ENGINE VOLLSTAENDIG EINSATZBEREIT (PLATZ 1).")
    print("================================================================================")

if __name__ == '__main__':
    generate_followup_engine()
