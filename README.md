# Automatisierte Mobilfunk-Standortplanung (P1-Cluster)

## Projektuebersicht
Automatisiertes Pipeline-System zur Erfassung, geodaetischen Bewertung, Klassifizierung und Dokumentation hochprioritaerer Mobilfunk-Neubaustandorte (P1) fuer Netzbetreiber und TowerCos.

## Kriterienmodell
- Versorgungsdefizit (35%): Ausfall mehrerer Netzbetreiber (RSRP < -115 dBm)
- Topografie & Exposition (30%): Hoehe ue. NN und freie Sichtachsen
- Stromnetzanschluss (20%): Distanz zur naechsten Niederspannungstrasse
- Zuwegung & Erschliessung (15%): Befahrbarkeit fuer Baufahrzeuge

## Ausfuehrung der Pipeline
Der gesamte Workflow wird mit folgendem Befehl in bash ausgefuehrt:
./run_pipeline.sh beispiel_standorte.csv

## Enthaltene Kern-Artefakte
- Mobilfunk_Cluster_Uebergabepaket.zip: Revisionssicheres Gesamtarchiv
- Batch_P1_Auswertung.xlsx: Formatierte Management-Tabelle (OpenXML)
- P1_Standorte_Cluster_Karte.html: Interaktive GIS-Karte (Leaflet)
- Cluster_Einreichung_P1.txt: Formelles Antragsdossier fuer TowerCos
- p1_standorte.geojson: Georeferenzierte Vektordaten (RFC 7946)
- SHA256SUMS.txt: Kryptografische Pruefsummen aller Dateien
