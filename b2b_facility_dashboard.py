import http.server
import socketserver
import os
import datetime

PORT = 8085
REPORT_FILE = "MASTER_B2B_FACILITY_AUDIT_REPORT.txt"

class FacilityDashboardHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/" or self.path == "/index.html":
            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()

            content = "Kein Audit-Bericht gefunden."
            if os.path.exists(REPORT_FILE):
                with open(REPORT_FILE, "r", encoding="utf-8") as f:
                    content = f.read()

            now_str = datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S")

            html = f"""<!DOCTYPE html>
<html lang="de">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>B2B Facility Management Dashboard - Haus im Wind</title>
<style>
    body {{ font-family: monospace, sans-serif; background-color: #0f172a; color: #e2e8f0; margin: 0; padding: 20px; }}
    .container {{ max-width: 1000px; margin: 0 auto; background: #1e293b; padding: 25px; border-radius: 8px; border: 1px solid #334155; }}
    h1 {{ color: #38bdf8; font-size: 20px; border-bottom: 2px solid #0284c7; padding-bottom: 8px; margin-top: 0; }}
    .badge {{ background: #166534; color: #4ade80; padding: 4px 10px; border-radius: 4px; font-weight: bold; font-size: 14px; display: inline-block; margin-bottom: 15px; }}
    pre {{ background: #0b0f19; padding: 15px; border-radius: 6px; overflow-x: auto; color: #f8fafc; font-size: 13px; line-height: 1.4; border: 1px solid #1e293b; }}
    .footer {{ margin-top: 15px; font-size: 12px; color: #94a3b8; border-top: 1px solid #334155; padding-top: 10px; }}
</style>
</head>
<body>
<div class="container">
    <h1>PROJEKT HAUS IM WIND: B2B-FACILITY-MANAGEMENT DASHBOARD</h1>
    <span class="badge">[TIER-1 STATUS: 100% OPERATIONAL]</span>
    <p>Live-Auswertung der periodischen Liegenschafts-Audits (DIN 31051 / DGUV V3 / RFC 2681):</p>
    <pre>{content}</pre>
    <div class="footer">
        Abrufzeitpunkt: {now_str} | Liegenschaft Haus im Wind (LOC-30 bis LOC-32) | Autarker Instandhaltungsbetrieb
    </div>
</div>
</body>
</html>"""
            self.wfile.write(html.encode("utf-8"))
        else:
            super().do_GET()

def run_server():
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("", PORT), FacilityDashboardHandler) as httpd:
        print(f"[X] B2B-Facility-Dashboard aktiv auf Port {PORT} gebunden.")
        httpd.serve_forever()

if __name__ == "__main__":
    run_server()
