import datetime

def generate_sla_contract():
    print("================================================================================")
    print("PROJEKT HAUS IM WIND: B2B-WARTUNGS- & SLA-SERVICEMATRIX (PLATZ 1)")
    print("================================================================================")

    sla_text = f"""================================================================================
B2B-SERVICE LEVEL AGREEMENT (SLA) & WARTUNGSVERTRAG
INFRASTRUKTUR- & LIEGENSCHAFTSINSTANDHALTUNG (CLUSTER 2026)
================================================================================
Datum:             {datetime.datetime.now().strftime('%d.%m.%Y %H:%M:%S')}
Auftragnehmer:     Kilian Scharf (Liegenschafts- und Infrastrukturmanagement Haus im Wind)
Auftraggeber:      Vantage Towers AG / Deutsche Funkturm GmbH (DFMG)
Prüfnormen:        DIN 31051, VDI 3586, DIN VDE 0105-100, DGUV Vorschrift 3

 1 VERTRAGSGEGENSTAND & GELTUNGSBEREICH
Der Auftragnehmer übernimmt die präventive Wartung, zyklische Inspektion sowie die
Störungsbeseitigung für die Liegenschaften LOC-30, LOC-31 und LOC-32 zur Gewährleistung
von 99.99 % technischer Verfügbarkeit.

 2 LEISTUNGSKATALOG NACH DIN 31051
1. QUARTALS-WARTUNG (MECHANIK & GEBAEUDEHUELLE):
   - Kontrolle der M24-Mastverschraubungen auf Solldrehmoment (245 Nm mit Wera D 6).
   - Überprüfung der Fischer FIS EM Plus Verankerungsfugen auf Setzungen oder Haarrisse.
   - Sicht- und Tastprüfung aller OTTOSEAL S 110 Abdichtungen an Kabeldurchführungen.

2. HALBJAEHRLICHE KRITIS-USV-INSPEKTION:
   - Zellensymmetrie-Prüfung der 288 kWh LiFePO4-Bänke (Delta U < 10 mV).
   - Kapazitäts- und Lasttest unter Netzausfall-Bedingungen.
   - Wartung der DC-Trennschalter und Bussmann-Hochleistungssicherungen.

3. JAEHRLICHE WIEDERHOLUNGSPRUEFUNG (DGUV V3 / BLITZSCHUTZ):
   - Schleifenimpedanz- und Isolationswiderstandsmessung nach DIN VDE 0105-100.
   - Durchgängigkeitsprüfung des Blitzschutz-Potentialausgleichs (50 mm² Kupfer).
   - Ausfertigung des rechtssicheren Prüfberichts für Gewerbeaufsicht und Sachversicherer.

 3 REAKTIONSZEITEN & ENTGELTSTRUKTUR
1. NOTFALL-ENTSTOERUNG (24/7/365):
   - Vor-Ort-Reaktionszeit bei kritischen Alarmen (Stromausfall, Sabotage): < 120 Minuten.
2. VERGUETUNG (NETTO):
   - Monatliche Grundpauschale:  450,00 EUR pro Standort (Cluster: 1.350,00 EUR / Monat).
   - Jährliches Wartungshonorar: 16.200,00 EUR / Jahr (wertgesichert nach VPI).
   - Materialaufwand nach tatsächlichem Beleg (Fischer, Wera, Knipex, Otto-Chemie).

================================================================================
STATUS: WARTUNGSVERTRAG SCHLUESSELFERTIG ZUR UNTERZEICHNUNG (PLATZ 1).
================================================================================
"""
    filename = "B2B_SLA_WARTUNGSVERTRAG.txt"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(sla_text)
    print(f"SLA-Vertrag erfolgreich generiert: {filename}")
    print(sla_text)

if __name__ == '__main__':
    generate_sla_contract()
