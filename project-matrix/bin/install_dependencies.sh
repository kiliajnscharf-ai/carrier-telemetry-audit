#!/usr/bin/env bash
set -euo pipefail

echo "=== STARTE DOWNLOAD UND INSTALLATION ALLER PAKETE MIT BASH ==="

# Paketlisten aktualisieren
apt-get update -y

# Kern-Tools und Netzwerk-Diagnostik installieren
apt-get install -y --no-install-recommends \
    curl \
    jq \
    git \
    shellcheck \
    dnsutils \
    iproute2 \
    traceroute \
    ca-certificates

# GitHub CLI (gh) offiziell via Bash herunterladen und einbinden
if ! command -v gh >/dev/null 2>&1; then
    echo "[INFO] Lade GitHub CLI via Bash herunter..."
    mkdir -p -m 755 /etc/apt/keyrings
    curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg | tee /etc/apt/keyrings/githubcli-archive-keyring.gpg > /dev/null
    chmod go+r /etc/apt/keyrings/githubcli-archive-keyring.gpg
    echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" | tee /etc/apt/sources.list.d/github-cli.list > /dev/null
    apt-get update -y
    apt-get install -y gh
fi

echo "=== VALIDIERUNG DER INSTALLIERTEN WERKZEUGE ==="
for cmd in curl jq git shellcheck dig traceroute gh; do
    if command -v "${cmd}" >/dev/null 2>&1; then
        echo "[OK] ${cmd}: $(command -v "${cmd}")"
    else
        echo "[FEHLER] ${cmd} wurde nicht korrekt installiert."
        exit 1
    fi
done

echo "=== ALLE PAKETE ERFOLGREICH MIT BASH HERUNTERGELADEN UND VERIFIZIERT ==="
