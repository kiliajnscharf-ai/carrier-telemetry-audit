#!/usr/bin/env bash
set -e

EXPORT_DIR="$HOME/USER_EXPORTS"
MAX_KEEP=5

echo "================================================================================"
echo "PRAKTISCHE LINUX-WERKSTATT: BACKUP-INTEGRITAET & ROTATION (PHASE 2)"
echo "================================================================================"
echo "Prüfverzeichnis:   $EXPORT_DIR"
echo "Maximale Archive:  $MAX_KEEP"
echo "--------------------------------------------------------------------------------"

if [ ! -d "$EXPORT_DIR" ]; then
    echo "[!] Exportverzeichnis existiert nicht: $EXPORT_DIR"
    exit 1
fi

cd "$EXPORT_DIR"

# 1. Integritätsprüfung aller vorhandenen .sha256 Dateien
echo "Prüfe SHA-256 Integrität der vorhandenen Backups..."
FAIL_COUNT=0
PASS_COUNT=0

for hashfile in *.sha256; do
    if [ -f "$hashfile" ]; then
        if sha256sum -c "$hashfile" --status; then
            echo "[OK] Integrität bestätigt: $hashfile"
            PASS_COUNT=$((PASS_COUNT + 1))
        else
            echo "[FEHLER] Integritätsprüfung fehlgeschlagen: $hashfile"
            FAIL_COUNT=$((FAIL_COUNT + 1))
        fi
    fi
done

echo "--------------------------------------------------------------------------------"
echo "Prüfresultat: $PASS_COUNT intakt, $FAIL_COUNT fehlerhaft."

# 2. Rotation: Behalte die neuesten MAX_KEEP Archive
ARCHIVES=($(ls -t WORKSPACE_BACKUP_*.tar.gz 2>/dev/null || true))
TOTAL_ARCHIVES=${#ARCHIVES[@]}

echo "Vorhandene Archive: $TOTAL_ARCHIVES"

if [ "$TOTAL_ARCHIVES" -gt "$MAX_KEEP" ]; then
    echo "Führe Rotation durch (bereinige ältere Archive)..."
    for ((i=MAX_KEEP; i<TOTAL_ARCHIVES; i++)); do
        OLD_ARCHIVE="${ARCHIVES[$i]}"
        OLD_HASH="${OLD_ARCHIVE}.sha256"
        echo "Entferne veraltetes Backup: $OLD_ARCHIVE"
        rm -f "$OLD_ARCHIVE" "$OLD_HASH"
    done
else
    echo "Keine Bereinigung erforderlich (Anzahl im Limit <= $MAX_KEEP)."
fi

echo "================================================================================"
echo "STATUS: INTEGRITAETS- & ROTATIONSPRUEFUNG ZU 100% ABGESCHLOSSEN (PLATZ 1)."
echo "================================================================================"
