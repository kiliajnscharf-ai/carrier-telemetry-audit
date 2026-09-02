import datetime
import subprocess
import os

def run_monthly_routine():
    print("================================================================================")
    print("PROJEKT HAUS IM WIND: ZYKLISCHER MONATS-PRUEFLAUF (PHASE 41)")
    print("================================================================================")

    now = datetime.datetime.now()
    now_str = now.strftime('%d.%m.%Y %H:%M:%S')

    scripts_to_check = [
        "generate_hazardous_materials_cadastre.py",
        "battery_cycle_resilience_monitor.py",
        "generate_cabinet_hvac_audit.py",
        "generate_cable_duct_inspection.py"
    ]

    report = []
    report.append("================================================================================")
    report.append(f"B2B-MONATSWARTUNGS- & PRUEFBERICHT (DGUV V3 / DIN 31051)")
    report.append(f"Liegenschaft:      Haus im Wind (LOC-30 bis LOC-32)")
    report.append(f"Prüfzeitpunkt:     {now_str}")
    report.append(f"Verantwortlich:    Kilian Scharf (Liegenschafts- und Infrastrukturmanagement)")
    report.append("================================================================================\n")
    report.append(f"{'Prüfmodul / Skript':<42} | {'Status':<15} | {'Ergebnis'}")
    report.append("-" * 75)

    all_ok = True
    for s in scripts_to_check:
        if os.path.exists(s):
            res = subprocess.run(["python3", s], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            if res.returncode == 0:
                report.append(f"{s:<42} | {'ERFOLGREICH':<15} | Ausgeführt & verifiziert")
            else:
                report.append(f"{s:<42} | {'FEHLERHAFT':<15} | Returncode {res.returncode}")
                all_ok = False
        else:
            report.append(f"{s:<42} | {'NICHT GEFUNDEN':<15} | Datei fehlt")
            all_ok = False

    report.append("-" * 75)
    report.append("\nGESAMTBEWERTUNG WARTUNGSZYKLUS:")
    if all_ok:
        report.append("[X] 1. Sämtliche Submodule ohne Fehler oder Grenzwertüberschreitung durchlaufen.")
        report.append("[X] 2. Keine akuten Instandhaltungs- oder Reparaturtickets erforderlich.")
        report.append("[X] 3. Liegenschaft befindet sich in voll betriebsbereitem Zustand (Platz 1).")
        final_stat = "ZYKLUS ERFOLGREICH ABGESCHLOSSEN (PLATZ 1)"
    else:
        report.append("[!] Mindestens eine Prüfung schlug fehl. Prüfprotokolle analysieren.")
        final_stat = "WARTUNGSFEHLER DETEKTIERT"

    report.append("================================================================================")
    report.append(f"STATUS: {final_stat}")
    report.append("================================================================================")

    out = "\n".join(report)
    with open("B2B_MONATSBERICHT_SEPTEMBER_2026.txt", "w", encoding="utf-8") as f:
        f.write(out)
    print(out)

if __name__ == '__main__':
    run_monthly_routine()
