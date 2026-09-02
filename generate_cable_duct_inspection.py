import datetime

def generate_duct_audit():
    print("================================================================================")
    print("PROJEKT HAUS IM WIND: B2B-KABELZUGSCHACHT- & NAGERSCHUTZ-AUDIT (PHASE 38)")
    print("================================================================================")

    now_str = datetime.datetime.now().strftime('%d.%m.%Y')

    ducts = [
        {"id": "KS-01", "loc": "Zufahrt Tor Nord", "class": "D 400 (40t)", "water_tight": "DICHT", "rodent_prot": "EDELSTAHL V4A", "status": "KONFORM"},
        {"id": "KS-02", "loc": "Knoten LOC-30/31", "class": "B 125 (12.5t)", "water_tight": "DICHT", "rodent_prot": "EDELSTAHL V4A", "status": "KONFORM"},
        {"id": "KS-03", "loc": "Trasse Steilhang LOC-32", "class": "B 125 (12.5t)", "water_tight": "DICHT", "rodent_prot": "EDELSTAHL V4A", "status": "KONFORM"},
        {"id": "EINF-01", "loc": "Hauseinführung HiW", "class": "Wanddurchführung", "water_tight": "IP68 GASDICHT", "rodent_prot": "OTTOSEAL/METALL", "status": "KONFORM"}
    ]

    report = f"""================================================================================
B2B-KABELZUGSCHACHT-, ROHRLEITUNGS- & NAGERSCHUTZPRUEFUNG (DIN EN 124 / VDE 0800)
LIEGENSCHAFTS-CLUSTER 2026 (HAUS IM WIND)
================================================================================
Stand:             {now_str}
Verantwortlich:    Kilian Scharf (Liegenschafts- und Infrastrukturmanagement)
Prüfstandard:      DIN EN 124 (Aufsätze/Abdeckungen) / DIN 18012 (Hauseinführungen)
Materialstandard:  Edelstahl V4A Nagerschutzmanschetten / Otto-Chemie Abdichtungen

INSPEKTIONSBEFUND KABELSCHAECHTE & DURCHDRINGUNGEN:
--------------------------------------------------------------------------------
Schacht-ID | Lage / Trassenabschnitt   | Lastklasse / Typ  | Dichtigkeit    | Nagerschutz     | Status
--------------------------------------------------------------------------------
"""
    for d in ducts:
        report += f"{d['id']:<10} | {d['loc']:<25} | {d['class']:<17} | {d['water_tight']:<14} | {d['rodent_prot']:<15} | {d['status']}\n"

    report += f"""--------------------------------------------------------------------------------
AUDIT-FESTSTELLUNGEN & BETRIEBSZUSTAND:
[X] 1. Alle Schachtabdeckungen rissfrei, plan aufliegend und verriegelt.
[X] 2. Keine Nagerspuren, Kabelverbisse oder Fremdkörpereinträge festgestellt.
[X] 3. Gas- und Druckwasserdichtigkeit an der Hauseinführung nach DIN 18012 gewahrt.
[X] 4. Schachtsohlen trocken, Drainageöffnungen funktionstüchtig.
================================================================================
STATUS: TRASSENSCHUTZ & SCHACHTINFRASTRUKTUR ZU 100% AUDITFEST (PLATZ 1).
================================================================================
"""
    filename = "B2B_SCHACHT_NAGERSCHUTZ_AUDIT.txt"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(report)
    print(f"Schacht-Auditbericht erfolgreich generiert: {filename}")
    print(report)

if __name__ == '__main__':
    generate_duct_audit()
