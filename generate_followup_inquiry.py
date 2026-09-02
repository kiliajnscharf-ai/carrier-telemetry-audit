import datetime

def create_inquiry_templates():
    timestamp = datetime.datetime.now().strftime("%d.%m.%Y")
    
    # Template Vantage Towers
    vt_text = f"""Sehr geehrte Damen und Herren,

wir beziehen uns auf das unter dem Ticket LLSM0135511 gefuehrte B2B-Standortdossier fuer das Cluster 2026 (LOC-30, LOC-31, LOC-32) vom 01.09.2026.

Die 14-taegige Prueffrist fuer die funktechnische und baurechtliche Vorpruefung ist erreicht. Bitte teilen Sie uns den aktuellen Pruefstatus der Funknetzplanung sowie den Zeitplan fuer die Vorlage des Standortsicherungsvertrags mit.

Mit freundlichen Gruessen
Kilian Scharf (Liegenschafts- und Infrastrukturmanagement)"""

    # Template DFMG
    dfmg_text = f"""Sehr geehrte Damen und Herren,

wir beziehen uns auf unsere Einreichung des vollstaendigen Standortdossiers fuer das Cluster 2026 (LOC-30, LOC-31, LOC-32) vom 01.09.2026.

Da die zweiwoechige Vorpruefungsphase abgeschlossen ist, bitten wir um eine kurze Rueckmeldung zum Ergebnis der technischen Funknetzpruefung fuer die Deutsche Telekom Technik.

Mit freundlichen Gruessen
Kilian Scharf (Liegenschafts- und Infrastrukturmanagement)"""

    with open("NACHFASSUNG_VANTAGE_LLSM0135511.txt", "w", encoding="utf-8") as f:
        f.write(vt_text)
    with open("NACHFASSUNG_DFMG_2026.txt", "w", encoding="utf-8") as f:
        f.write(dfmg_text)
        
    print("================================================================================")
    print("NACHFASS-TEMPLATES FUER DEN 15.09.2026 ERFOLGREICH GENERIERT")
    print("================================================================================")
    print("Erstellt: NACHFASSUNG_VANTAGE_LLSM0135511.txt")
    print("Erstellt: NACHFASSUNG_DFMG_2026.txt")

if __name__ == '__main__':
    create_inquiry_templates()
