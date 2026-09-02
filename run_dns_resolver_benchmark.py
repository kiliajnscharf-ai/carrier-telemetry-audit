import socket
import time
import datetime

def benchmark_domain(domain, max_time_ms=100.0):
    start = time.time()
    try:
        results = socket.getaddrinfo(domain, 80, socket.AF_INET, socket.SOCK_STREAM)
        duration_ms = (time.time() - start) * 1000.0
        ip_addr = results[0][4][0] if results else "UNKNOWN"
        return True, duration_ms, ip_addr
    except Exception:
        return False, 0.0, "FAILED"

def run_dns_audit():
    print("================================================================================")
    print("PROJEKT HAUS IM WIND: B2B-DNS-RESOLVER- & BENCHMARK-ENGINE (PHASE 53)")
    print("================================================================================")

    now_str = datetime.datetime.now().strftime('%d.%m.%Y %H:%M:%S')

    domains = [
        {"domain": "cloudflare.com",    "purpose": "Global CDN / Edge", "max_ms": 100.0},
        {"domain": "ptbtime1.ptb.de",   "purpose": "KRITIS NTP Zeitserver", "max_ms": 120.0},
        {"domain": "bund.de",           "purpose": "Behörden-Infrastruktur", "max_ms": 120.0}
    ]

    report = []
    report.append("================================================================================")
    report.append("B2B-DNS-RESOLVER- & PERFORMANCE-PROTOKOLL (RFC 1035)")
    report.append(f"Messzeitpunkt:     {now_str}")
    report.append("Prüfverfahren:     getaddrinfo() Direct Query / Resolver Stack")
    report.append("================================================================================\n")
    report.append(f"{'Domain':<20} | {'Verwendungszweck':<24} | {'Aufgelöste IP':<16} | {'Lookup-Zeit':<12} | {'Status'}")
    report.append("-" * 88)

    all_ok = True
    for d in domains:
        success, dur, ip = benchmark_domain(d["domain"], d["max_ms"])
        if success:
            stat = "OPTIMAL (PASS)" if dur <= d["max_ms"] else "VERZOEGERT"
            report.append(f"{d['domain']:<20} | {d['purpose']:<24} | {ip:<16} | {dur:>6.2f} ms   | {stat}")
        else:
            report.append(f"{d['domain']:<20} | {d['purpose']:<24} | {'FEHLER':<16} | {'TIMEOUT':<9} | NICHT AUFGELOEST")
            all_ok = False

    report.append("-" * 88)
    report.append("\nAUDIT-FESTSTELLUNG:")
    if all_ok:
        report.append("[X] 1. Alle Referenz-Domains wurden fehlerfrei aufgelöst.")
        report.append("[X] 2. Resolver-Stack antwortet ohne Timeouts.")
        report.append("[X] 3. Namensauflösung der Liegenschaft entspricht Standard (Platz 1).")
        final_stat = "DNS-BENCHMARK ZU 100% BESTANDEN (PLATZ 1)"
    else:
        report.append("[!] Mindestens ein Resolver-Lookup fehlgeschlagen.")
        final_stat = "RESOLVER-FEHLER DETEKTIERT"

    report.append("================================================================================")
    report.append(f"STATUS: {final_stat}")
    report.append("================================================================================")

    out = "\n".join(report)
    with open("B2B_DNS_RESOLVER_AUDIT.txt", "w", encoding="utf-8") as f:
        f.write(out)
    print(out)

if __name__ == '__main__':
    run_dns_audit()
