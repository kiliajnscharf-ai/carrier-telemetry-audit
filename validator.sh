#!/bin/bash

# PREISWERTE UND EFFIZIENTE STREAM-VALIDIERUNG
# NUTZUNG: ./stream_validator.sh <URL>

URL=$1

if [ -z "$URL" ]; then
    echo "FEHLER: KEINE URL ANGEGEBEN."
    exit 1
fi

echo "PRÜFE VERFÜGBARKEIT: $URL"

# CURL NUTZEN FÜR HTTP HEAD REQUEST
RESPONSE=$(curl -I -s --max-time 5 "$URL" | grep "HTTP/1.1" | awk '{print $2}')

if [ "$RESPONSE" == "200" ]; then
    echo "STATUS: STREAM ONLINE (200 OK)"
    exit 0
else
    echo "STATUS: FEHLER / OFFLINE (CODE: $RESPONSE)"
    exit 1
fi
