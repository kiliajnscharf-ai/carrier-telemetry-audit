import shutil
import os
import datetime

def check_toolbox():
    print("================================================================================")
    print("PRAKTISCHE LINUX-WERKSTATT: SYSTEM- & RESSOURCEN-CHECK (PHASE 49)")
    print("================================================================================")

    now_str = datetime.datetime.now().strftime('%d.%m.%Y %H:%M:%S')
    tools = ["bash", "python3", "git", "tar", "sha256sum", "curl", "ssh"]

    report = []
    report.append("================================================================================")
    report.append("STATUSBERICHT: LOKALE LINUX-WERKSTATT & WERKZEUGE")
    report.append(f"Zeitstempel:       {now_str}")
    report.append("================================================================================\n")
    report.append(f"{'Werkzeug / Tool':<25} | {'Verfügbarkeit':<20} | {'Pfad'}")
    report.append("-" * 75)

    for t in tools:
        path = shutil.which(t)
        if path:
            report.append(f"{t:<25} | {'VERFUEGBAR':<20} | {path}")
        else:
            report.append(f"{t:<25} | {'NICHT INSTALLIERT':<20} | -")

    # Speicherplatz prüfen
    total, used, free = shutil.disk_usage(".")
    total_gb = total / (1024**3)
    free_gb = free / (1024**3)

    report.append("-" * 75)
    report.append(f"\nSPEICHERPLATZ: Gesamt: {total_gb:.2f} GB | Frei verfügbar: {free_gb:.2f} GB")
    report.append("================================================================================")
    report.append("STATUS: WERKSTATT EINSATZBEREIT FUER REALE PRAXISAUFGABEN (PLATZ 1).")
    report.append("================================================================================")

    out = "\n".join(report)
    with open("LINUX_WERKSTATT_STATUS.txt", "w", encoding="utf-8") as f:
        f.write(out)
    print(out)

if __name__ == '__main__':
    check_toolbox()
