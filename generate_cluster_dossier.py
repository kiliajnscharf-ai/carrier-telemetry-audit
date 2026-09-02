cluster_doc = """================================================================================
STANDORT-CLUSTER-DOSSIER FUER MOBILFUNK-INFRASTRUKTUR (P1)
================================================================================

PROJEKTBEZEICHNUNG: Ausbau-Cluster Nord-Ost (2 Neubaustandorte P1)
REGION:             Bad Pyrmont Umland
GESAMTBEWERTUNG:    Prioritaet P1 (Sofortiger koordinierter Ausbaubedarf)

1. UEBERSICHT DER CLUSTER-STANDORTE:
--------------------------------------------------------------------------------
Standort-ID:        LOC-10 (Nordhang Funkfeld)
- Koordinaten:      51.992000 N, 9.261000 E (WGS84)
- Hoehe:            260 m ue. NN (Exponierte Nordhanglage)
- Stromdistanz:     25 m zur Niederspannungstrasse
- Zuwegung:         Befestigter Wirtschaftsweg
- Score:            9.38 / 10 (P1)

Standort-ID:        LOC-12 (Osthoehe Forst)
- Koordinaten:      51.988000 N, 9.275000 E (WGS84)
- Hoehe:            245 m ue. NN (Exponierte Ostkante)
- Stromdistanz:     45 m zur Niederspannungstrasse
- Zuwegung:         Befestigter Wirtschaftsweg
- Score:            8.97 / 10 (P1)
--------------------------------------------------------------------------------

2. INFRASTRUKTURELLE VORTEILE DES GESAMTCLUSTERS:
- Minimale Tiefbaukosten: In Summe lediglich 70 m Kabeltrasse fuer beide Standorte erforderlich.
- Vollstaendige Wegebefestigung fuer Montage- und Wartungsfahrzeuge vorhanden.
- Standorte ergaenzen sich optimal ohne destruktive Funkfeld-Ueberlappungen.
- Maximale Eignung fuer Multi-Tenancy (Telekom, Vodafone, O2, 1&1).

3. EMPFOHLENE TECHNISCHE REALISIERUNG:
- Bauart: 2x 30-40 m standardisierte Schleuderbeton- oder Gittermasten.
- Frequenzen: Band 28 (700 MHz), Band 20 (800 MHz), Band 8 (900 MHz).
- Gesamter Versorgungsradius: ca. 12 km zusammenhaengende Flaechendurchdringung.

4. BEIGEFUEGTE SYSTEMARTEFAKTE:
- Tabellarischer Datenbericht: Batch_P1_Auswertung.xlsx
- Interaktive GIS-Clusterkarte: P1_Standorte_Cluster_Karte.html
- GIS-Vektordatensatz:         p1_standorte.geojson
================================================================================
"""

with open("Cluster_Einreichung_P1.txt", "w", encoding="utf-8") as f:
    f.write(cluster_doc)

print("Cluster-Dossier erfolgreich exportiert: Cluster_Einreichung_P1.txt")
