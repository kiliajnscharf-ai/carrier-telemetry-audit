#!/usr/bin/env bash
dd if=/dev/zero of=upload_payload.bin bs=1M count=10 2>/dev/null
echo "Starte Upload-Hintergrundlast und messe Latenz..."
curl -s -X POST --data-binary @upload_payload.bin https://speed.cloudflare.com/__down?bytes=10000000 >/dev/null &
PID=$!
ping -c 30 -i 0.2 145.254.2.19 | grep -E "(packets transmitted|rtt)"
wait $PID 2>/dev/null || true
rm -f upload_payload.bin
