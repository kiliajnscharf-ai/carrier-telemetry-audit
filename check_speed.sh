#!/bin/bash
echo "---------------------------------------"
echo "STARTING PREMIUM SPEED AUDIT - HAUS IM WIND"
echo "DATE: $(date)"
echo "---------------------------------------"
# DOWNLOAD DER TESTDATEI MIT BASH/CURL
curl -w "Connect: %{time_connect}s | TTFB: %{time_starttransfer}s | Total: %{time_total}s | Speed: %{speed_download} B/s\n" \
     -o /dev/null http://speedtest.tele2.net/1MB.zip
echo "---------------------------------------"
echo "AUDIT COMPLETED."
