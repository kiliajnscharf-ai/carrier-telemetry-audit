#!/usr/bin/env bash

DATA_FILE="data/network_pings.csv"

if [ ! -f "$DATA_FILE" ]; then
    echo "Keine Messdatei gefunden."
    exit 1
fi

echo "=== Latenz- & Jitter-Analyse (letzte 20 Messungen) ==="
tail -n 20 "$DATA_FILE" | awk -F',' '
BEGIN { count=0; sum=0; min=999999; max=0 }
NR > 1 {
    val = $3 + 0;
    if (val > 0) {
        sum += val;
        count++;
        if (val < min) min = val;
        if (val > max) max = val;
        vals[count] = val;
    }
}
END {
    if (count > 0) {
        avg = sum / count;
        diff_sum = 0;
        for (i = 2; i <= count; i++) {
            d = vals[i] - vals[i-1];
            if (d < 0) d = -d;
            diff_sum += d;
        }
        jitter = diff_sum / (count - 1);
        printf "Anzahl Messpunkte: %d\n", count;
        printf "Minimale Latenz:   %.2f ms\n", min;
        printf "Maximale Latenz:   %.2f ms\n", max;
        printf "Durchschnitt:      %.2f ms\n", avg;
        printf "Mittlerer Jitter:  %.2f ms\n", jitter;
    } else {
        print "Keine gueltigen Latenzwerte vorhanden.";
    }
}'
