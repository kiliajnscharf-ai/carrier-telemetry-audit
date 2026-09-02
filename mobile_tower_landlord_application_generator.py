import datetime

def generate_application():
    now_str = datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S")
    report_file = "B2B_MOBILFUNK_VERMIETER_ANGEBOT.txt"
    
    lines = []
    lines.append("================================================================================")
    lines.append("PROJEKT HAUS IM WIND: VERMIETER- & GRUNDSTÜCKSANGEBOT (PHASE 96)")
    lines.append(f"Erstellungszeitpunkt: {now_str}")
    lines.append("Empfänger:          Vantage Towers / Deutsche Telekom Towers / Telefónica Infra")
    lines.append("Objektstandort:     Region Bad Pyrmont & Weserbergland (LOC-30 bis LOC-32)")
    lines.append("================================================================================")
    lines.append("FORMELLES GRUNDSTÜCKSANGEBOT FÜR MOBILFUNK-NEUBAU-MASTEN:\n")
    
    lines.append("Sehr geehrte Damen und Herren,\n")
    lines.append("hiermit bieten wir Ihnen im Rahmen unseres Liegenschaftsmanagements drei strategisch")
    lines.append("hochwertige und bautechnisch vorbereitete Potentialflächen für den Neubau von Mobilfunkmasten")
    lines.append("zur Schließung von Abdeckungslücken (White Spots) in der Region Bad Pyrmont an:\n")
    
    lines.append("1. ANGEBOT FLÄCHE 1 (ID: SITE-BAD-01 - Bad Pyrmont Süd / Kurpark-Rand):")
    lines.append("   - Eignung: Hanganschnitt, optimal zur Versorgung des Talkessels.")
    lines.append("   - Struktur: Monopole / Tarnmast (h=30m), optisch integriert.")
    lines.append("   - Erschließung: Zufahrt über Wirtschaftswege, Strom/Glasfaser im Nahbereich.\n")
    
    lines.append("2. ANGEBOT FLÄCHE 2 (ID: SITE-BAD-02 - Gewerbegebiet Holzhausen):")
    lines.append("   - Eignung: Unbebaute Randfläche, ideal für Multi-Operator-Gittermast (h=40m).")
    lines.append("   - Erschließung: LKW-Zufahrt, Starkstrom und Haupt-Glasfasertrasse direkt an der Grundstücksgrenze.\n")
    
    lines.append("3. ANGEBOT FLÄCHE 3 (ID: SITE-BAD-03 - Emmertal-Grenze / Kahlberg):")
    lines.append("   - Eignung: Exponierte Richtfunkkante zur Entlastung der B83.")
    lines.append("   - Struktur: Robuster Gittermast (h=35m) für Breitband- und Mobilfunkversorgung.\n")
    
    lines.append("Alle Standorte verfügen über gesicherte Eigentümerstrukturen und uneingeschränkte baurechtliche")
    lines.append("Voraussetzungen gemäß DIN EN 1991/1993 sowie BNetzA-Konformität.\n")
    
    lines.append("Wir freuen uns auf Ihre Rückmeldung zur Aufnahme in die Ausbauplanung 2026/2027.\n")
    lines.append("Mit freundlichen Grüßen")
    lines.append("Facility Management 'Haus im Wind' (Tier-1 Autarkie - Platz 1)\n")
    lines.append("================================================================================")
    lines.append("STATUS: VERMIETER-ANGEBOTSDOSSIER ERFOLGREICH GENERIERT (PLATZ 1).")
    lines.append("================================================================================")
    
    out_text = "\n".join(lines)
    with open(report_file, "w", encoding="utf-8") as f:
        f.write(out_text)
        
    print(out_text)

if __name__ == "__main__":
    generate_application()
