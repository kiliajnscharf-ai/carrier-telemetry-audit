#!/bin/bash
LOGFILE="$HOME/system_tests.log"
echo "=== Sauberer Standard-Testlauf: $(date) ===" >> "$LOGFILE"
ip addr >> "$LOGFILE" 2>/dev/null
free -h >> "$LOGFILE" 2>/dev/null
echo "Test beendet." >> "$LOGFILE"
