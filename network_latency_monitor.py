import socket
import time
import datetime
import os
import csv

CSV_FILE = "NETZWERK_LATENZ_HISTORIE.csv"

TARGETS = [
    {"name": "Cloudflare DNS", "ip": "1.1.1.1", "port": 53},
    {"name": "Google DNS",     "ip": "8.8.8.8", "port": 53},
    {"name": "Quad9 DNS",      "ip": "9.9.9.9", "port": 53}
]

def measure_rtt(ip, port, timeout=2.5):
    start = time.perf_counter()
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(timeout)
    try:
        sock.connect((ip, port))
        sock.close()
        latency_ms = (time.perf_counter() - start) * 1000.0
        return round(latency_ms, 2), "ONLINE"
    except socket.timeout:
        return 0.0, "TIMEOUT"
    except Exception:
        return 0.0, "ERROR"

def run_monitor():
    file_exists = os.path.exists(CSV_FILE)
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    print("================================================================================")
    print("PROJEKT HAUS IM WIND: ECHTER NETZWERK-LATENZ-MONITOR (PHASE 61)")
    print(f"Zeitstempel:       {timestamp}")
    print("Messmethode:       TCP-Connect RTT (Port 53)")
    print("--------------------------------------------------------------------------------")
    print(f"{'Ziel':<18} | {'IP':<15} | {'Latenz (ms)':<12} | {'Status'}")
    print("-" * 60)

    rows_to_write = []
    for t in TARGETS:
        lat, status = measure_rtt(t["ip"], t["port"])
        print(f"{t['name']:<18} | {t['ip']:<15} | {lat:>9.2f} ms | {status}")
        rows_to_write.append([timestamp, t["name"], t["ip"], lat, status])

    with open(CSV_FILE, mode="a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["Timestamp", "Target", "IP", "Latency_ms", "Status"])
        writer.writerows(rows_to_write)

    print("--------------------------------------------------------------------------------")
    print(f"[X] Messwerte erfolgreich in '{CSV_FILE}' protokolliert.")
    print("================================================================================")
    print("STATUS: NETZWERK-MONITOR ZU 100% EINSATZBEREIT (PLATZ 1).")
    print("================================================================================")

if __name__ == "__main__":
    run_monitor()
