#!/usr/bin/env bash
echo "Pruefung lokaler Netzwerk-Tools fuer Traffic-Kontrolle:"
for tool in tc iptables nft iperf3 ping; do
    if which $tool >/dev/null 2>&1; then
        echo " - $tool: INSTALLIERT"
    else
        echo " - $tool: NICHT VORHANDEN"
    fi
done
