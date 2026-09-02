#!/bin/bash
echo "Starte Master-Daemon im Hintergrund (Projekt Haus im Wind)..."
while true; do
    python3 master_autonomous_daemon.py > /dev/null 2>&1
    sleep 300
done
