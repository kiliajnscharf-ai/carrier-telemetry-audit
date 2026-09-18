#!/usr/bin/env bash
TARGET="145.254.2.19"
echo "=== SIMULATION: LEGALES PACING / KONTROLLIERTE EINSPEISUNG ==="
echo "1. Starte kontrollierten Latenz-Test waehrend kontinuierlicher Last:"

# Sendet ICMP-Messpakete in praezisem 1-Sekunden-Intervall
ping -c 10 -i 1 "$TARGET" | awk '
/bytes from/ {
    match($0, /time=([0-9.]+)/, arr);
    rtt=arr[1];
    if (rtt > 100) status="BUFFERBLOAT";
    else if (rtt > 50) status="MODERAT";
    else status="OPTIMAL (BASELINE)";
    printf "Echo-Reply: RTT = %6.2f ms | Status: %s\n", rtt, status;
}
/packet loss/ { print "\nStatistik: " $0 }
'
