#!/usr/bin/env bash
set -e

OWNER="kiliajnscharf-ai"
REPO="carrier-telemetry-audit"

echo "=================================================="
echo " GITHUB TRAFFIC & AUDIT INSPECTOR"
echo " Target: $OWNER/$REPO"
echo "=================================================="

# Pruefe, ob ein GitHub Personal Access Token hinterlegt ist
if [ -z "$GITHUB_TOKEN" ]; then
    echo "HINWEIS: GitHub erfordert fuer Traffic-Metriken einen Token mit 'repo'-Rechten."
    read -rsp "Bitte GitHub Personal Access Token (PAT) eingeben: " GITHUB_TOKEN
    echo ""
fi

if [ -z "$GITHUB_TOKEN" ]; then
    echo "Fehler: Kein Token angegeben. Abbruch."
    exit 1
fi

AUTH_HEADER="Authorization: Bearer $GITHUB_TOKEN"
ACCEPT_HEADER="Accept: application/vnd.github+json"
API_BASE="https://api.github.com/repos/$OWNER/$REPO/traffic"

echo "Frage GitHub API ab..."

VIEWS_JSON=$(curl -s -H "$AUTH_HEADER" -H "$ACCEPT_HEADER" "$API_BASE/views")
CLONES_JSON=$(curl -s -H "$AUTH_HEADER" -H "$ACCEPT_HEADER" "$API_BASE/clones")
REFERRERS_JSON=$(curl -s -H "$AUTH_HEADER" -H "$ACCEPT_HEADER" "$API_BASE/popular/referrers")

python3 -c '
import json, sys

views = json.loads("""'"$VIEWS_JSON"'""")
clones = json.loads("""'"$CLONES_JSON"'""")
referrers = json.loads("""'"$REFERRERS_JSON"'""")

if "message" in views and views.get("message") == "Bad credentials":
    print("\n[!] Authentifizierungsfehler: Der angegebene Token ist ungueltig oder abgelaufen.")
    sys.exit(1)

print("\n--- 1. SEITENAUFRUFE (VIEWS DER LETZTEN 14 TAGE) ---")
total_views = views.get("count", 0)
unique_uniques = views.get("uniques", 0)
print(f"Gesamt-Aufrufe: {total_views} | Eindeutige Besucher (Unique Visitors): {unique_uniques}")

print("\n--- 2. REPOSITORY-KLONE (GIT FETCH / CLONE) ---")
total_clones = clones.get("count", 0)
unique_cloners = clones.get("uniques", 0)
print(f"Gesamte Klon-Vorgaenge: {total_clones} | Eindeutige Nutzer: {unique_cloners}")

print("\n--- 3. REFERRER-QUELLEN (HERKUNFTS-DOMAINS) ---")
if isinstance(referrers, list) and len(referrers) > 0:
    for ref in referrers:
        print(f"- Quelle: {ref.get(\"referrer\")} (Aufrufe: {ref.get(\"count\")}, Uniques: {ref.get(\"uniques\")})")
else:
    print("Keine externen Referrer registriert (Zugriffe erfolgten direkt oder via verschluesseltem Link).")

print("\n==================================================")
'
