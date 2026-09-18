#!/usr/bin/env bash
echo "Prüfe Paketverlust zu Vodafone Core und Cloudflare DNS..."
ping -c 50 -i 0.2 145.254.2.19 | grep -E "(packets transmitted|rtt)"
ping -c 50 -i 0.2 1.1.1.1 | grep -E "(packets transmitted|rtt)"
