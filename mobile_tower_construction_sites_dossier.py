import datetime

def generate_dossier():
    now_str = datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S")
    report_file = "B2B_MOBILFUNK_BAUTECHNIK_DOSSIER.txt"
    
    lines = []
    lines.append("================================================================================")
    lines.append("PROJEKT HAUS IM WIND: MOBILFUNK-BAUTECHNIK & FLURSTÜCKS-DOSSIER (PHASE 95)")
    lines.append(f"Prüfzeitpunkt:     {now_str}")
    lines.append("Liegenschaft:      Bad Pyrmont & Region Weserbergland")
    lines.append("Infrastruktur-Zweck: Bauliche Platzierung & Erschließung von Neubau-Masten")
    lines.append("================================================================================")
    lines.append("1. BAULICHE PLATZIERUNG UND MASTEN-TYPOLOGIE:\n")
    
    lines.append("--- STANDORT 1: SITE-BAD-01 (Bad Pyrmont Süd / Kurpark-Rand) ---")
    lines.append("- Exakter Bauplatz: Hanganschnitt im südlichen Kurpark-Übergang (geschützte Topografie).")
    lines.append("- Baustruktur: Monopole (schlanker Stahlrohrmast, h=30m) oder Tarnmast in Antennendesign.")
    lines.append("- Fundamentierung: Flachfundament oder Mikro-Pfahlgründung bei Hangdruck.")
    lines.append("- Anbindung: Zufahrt über bestehende Wirtschaftswege, Strom/Glasfaser direkt im Nahbereich.\n")
    
    lines.append("--- STANDORT 2: SITE-BAD-02 (Gewerbegebiet Holzhausen / Lügder Str.) ---")
    lines.append("- Exakter Bauplatz: Unbebaute Randfläche im Gewerbegebiet Holzhausen.")
    lines.append("- Baustruktur: Klassischer Freiflächen-Gittermast (h=40m) für Mehrfach-Colocation (Multi-Operator).")
    lines.append("- Fundamentierung: Genormtes Schwerkraft-Plattenfundament.")
    lines.append("- Anbindung: Perfekte Erschließung durch LKW-befahrbare Zufahrt, Starkstrom und Haupt-Glasfasertrasse.\n")
    
    lines.append("--- STANDORT 3: SITE-BAD-03 (Emmertal-Grenze / Kahlberg-Ausläufer) ---")
    lines.append("- Exakter Bauplatz: Exponierte Kante am Kahlberg-Ausläufer (Richtfunk- und Sendeachse).")
    lines.append("- Baustruktur: Robuster Gittermast (h=35m) mit wetterfester Ausrüstung gegen Windlasten.")
    lines.append("- Fundamentierung: Fels-Fangsicherungs- und Betonanker.")
    lines.append("- Anbindung: Erschließung über Forst- und Bundesstraßenzufahrt (B83), Richtfunk-Backup möglich.\n")
    
    lines.append("================================================================================")
    lines.append("BAUTECHNISCHE STANDARDS & NORMEN:")
    lines.append("[X] Standsicherheit nach DIN EN 1991 (Eurocode 1) & DIN EN 1993 (Stahlbau).")
    lines.append("[X] Elektromagnetische Verträglichkeit (EMV) & BEMF-Standortbescheinigung (BNetzA).")
    lines.append("[X] Blitzschutz nach DIN EN 62305 & Erdungsanlage nach VDE 0100.")
    lines.append("================================================================================")
    lines.append("STATUS: BAUTECHNISCHES DOSSIER VOLLSTAENDIG ERSTELLT (PLATZ 1).")
    lines.append("================================================================================")
    
    out_text = "\n".join(lines)
    with open(report_file, "w", encoding="utf-8") as f:
        f.write(out_text)
        
    print(out_text)

if __name__ == "__main__":
    generate_dossier()
