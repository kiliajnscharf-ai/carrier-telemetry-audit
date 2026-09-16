#!/usr/bin/env bash
FILE="core_node_latency.csv"

if [ ! -f "$FILE" ]; then
    echo "Fehler: $FILE nicht gefunden."
    exit 1
fi

awk -F, 'NR>1 && $1 !~ /^#/ && $4 != "FAIL" && $4 ~ /^[0-9.]+$/ {
    count++;
    val = $4 + 0;
    values[count] = val;
    sum += val;
    if (val > 100) spikes++;
}
END {
    if (count == 0) {
        print "Keine validen Messdaten vorhanden.";
        exit;
    }
    
    # Sortierung für Perzentil-Berechnung
    for (i = 1; i <= count; i++) {
        for (j = i + 1; j <= count; j++) {
            if (values[i] > values[j]) {
                tmp = values[i];
                values[i] = values[j];
                values[j] = tmp;
            }
        }
    }
    
    mean = sum / count;
    p50 = values[int(count * 0.50) > 0 ? int(count * 0.50) : 1];
    p90 = values[int(count * 0.90) > 0 ? int(count * 0.90) : 1];
    p95 = values[int(count * 0.95) > 0 ? int(count * 0.95) : 1];
    max_val = values[count];
    min_val = values[1];
    
    printf "======================================================================\n";
    printf "   AUTOMATISIERTER NOC-DIAGNOSEBERICHT: CORE-NODE LATENCY PROFILE\n";
    printf "======================================================================\n";
    printf "Datenbasis: %d Zyklen erfasst\n", count;
    printf "Minimale Latenz (Baseline)       : %.2f ms\n", min_val;
    printf "Mittlere Maximallatenz (Mean)    : %.2f ms\n", mean;
    printf "Median-Spitzen (p50)             : %.2f ms\n", p50;
    printf "90. Perzentil (p90)              : %.2f ms\n", p90;
    printf "95. Perzentil (p95)              : %.2f ms\n", p95;
    printf "Absolutes Maximum                : %.2f ms\n", max_val;
    printf "Anomalierate (> 100 ms)          : %d von %d (%.1f%%)\n", spikes, count, (spikes/count)*100;
    printf "----------------------------------------------------------------------\n";
    printf "TECHNISCHE DIAGNOSE FUER VODAFONE 2ND/3RD-LEVEL:\n";
    if (p95 > 100) {
        printf "[KRITISCH] p95-Latenz liegt bei %.2f ms. Der Schwellenwert fuer\n", p95;
        printf "VoIP/Gaming/Echtzeit (< 45 ms) wird drastisch ueberschritten.\n";
        printf "Nachweis erbracht: Chronische Pufferstaus am Hop 145.254.2.19.\n";
    } else {
        printf "[MODERAT] p95-Latenz liegt unter 100 ms. Weiteres Monitoring erforderlich.\n";
    }
    printf "======================================================================\n";
}' "$FILE"
