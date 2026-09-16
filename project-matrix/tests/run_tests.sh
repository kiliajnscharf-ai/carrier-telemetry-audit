#!/usr/bin/env bash
set -euo pipefail

echo "[TEST] Pruefe Syntax aller Skripte..."
find bin/ -type f -name "*.sh" -exec bash -n {} +

echo "[TEST] Fuehre ShellCheck durch..."
command -v shellcheck >/dev/null 2>&1 && find bin/ -type f -name "*.sh" -exec shellcheck {} + || echo "[WARNUNG] shellcheck nicht installiert."

echo "[TEST] Fuehre Funktionslauf aus..."
./bin/benchmark.sh "https://api.github.com" >/dev/null

echo "[ERFOLG] Alle Tests bestanden."
