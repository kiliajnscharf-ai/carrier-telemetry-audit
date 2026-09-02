import datetime

def generate_submission_package():
    now_str = datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S")
    submission_file = "B2B_MOBILFUNK_VERSAND_TEMPLATE.txt"
    
    lines = []
    lines.append("================================================================================")
    lines.append("PROJEKT HAUS IM WIND: VERSAND- & PORTAL-VORBEREITUNG (PHASE 97)")
    lines.append(f"Erstellungszeitpunkt: {now_str}")
    lines.append("Objekt:             Grundstücksangebot Mobilfunk-Neubau (SITE-BAD-01 bis 03)")
    lines.append("================================================================================")
    lines.append("E-MAIL-VORLAGE FÜR DEN DIREKTVERSAND AN NETZBETREIBER / FUNKTURMGESELLSCHAFTEN:\n")
    
    lines.append("BETREFF: Grundstücksangebot für Mobilfunk-Neubau / Siting-Potentiale Region Bad Pyrmont (SITE-BAD-01 bis SITE-BAD-03)\n")
    lines.append("Sehr geehrte Damen und Herren,\n")
    lines.append("bezugnehmend auf unser anliegendes Vermieterdossier bieten wir Ihnen hiermit drei bautechnisch")
    lines.append("vorbereitete Liegenschaften zur Schließung von Funkabdeckungslücken in Bad Pyrmont und Umgebung an:\n")
    lines.append("- SITE-BAD-01: Bad Pyrmont Süd (Hanglage / Kurpark-Rand, Monopole h=30m)")
    lines.append("- SITE-BAD-02: Gewerbegebiet Holzhausen (Lügder Str., Freiflächen-Gittermast h=40m)")
    lines.append("- SITE-BAD-03: Emmertal-Grenze (Kahlberg-Ausläufer, Richtfunk-Gittermast h=35m)\n")
    lines.append("Sämtliche Standorte verfügen über gesicherte Erschließung (Starkstrom, Glasfaser, Zufahrt)")
    lines.append("und erfüllen alle bautechnischen Normen (DIN EN 1991/1993, BNetzA).\n")
    lines.append("Die detaillierten Bautechnik-Dossiers und Flurstücksübersichten finden Sie im Anhang.")
    lines.append("Wir bitten um Prüfung und Aufnahme in Ihre aktuelle Ausbauplanung 2026/2027.\n")
    lines.append("Mit freundlichen Grüßen")
    lines.append("Facility Management 'Haus im Wind'")
    lines.append("Standort: Bad Pyrmont (LOC-30 bis LOC-32)")
    lines.append("Tier-1 Autarkie (Platz 1)\n")
    lines.append("================================================================================")
    lines.append("ERFORDERLICHE DATEIANHÄNGE FÜR DEN VERSAND:")
    lines.append("1. B2B_MOBILFUNK_VERMIETER_ANGEBOT.txt")
    lines.append("2. B2B_MOBILFUNK_BAUTECHNIK_DOSSIER.txt")
    lines.append("3. Flurstückskarte / Liegenschaftskataster (Flur 1:1000)")
    lines.append("================================================================================")
    lines.append("STATUS: VERSANDPAKET VOLLSTÄNDIG VORBEREITET (PLATZ 1).")
    lines.append("================================================================================")
    
    out_text = "\n".join(lines)
    with open(submission_file, "w", encoding="utf-8") as f:
        f.write(out_text)
        
    print(out_text)

if __name__ == "__main__":
    generate_submission_package()
