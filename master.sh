#!/bin/bash
echo "=== Status am $(date) ===" >> $HOME/logs/system_status.log
free -h >> $HOME/logs/system_status.log
df -h | grep -E "Filesystem|/dev/block/dm" >> $HOME/logs/system_status.log
