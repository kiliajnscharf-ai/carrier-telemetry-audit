# System-Architektur: Mobilfunk-Standortplanung P1

## 1. Mathematisches Bewertungsmodell
Score = (Defizit * 0.35) + (Topografie * 0.30) + (Strom * 0.20) + (Zuwegung * 0.15)
- P1 (Sofortiger Ausbau): Score >= 8.50
- P2 (Mittlere Prioritaet): 7.00 <= Score < 8.50
- P3 (Nachrangig): 5.00 <= Score < 7.00
- P4 (Ausschluss): Score < 5.00

## 2. Pipeline-Stufen (run_pipeline.sh)
1. Ingestion & Scoring (import_external_csv.py)
2. GIS-Kartengenerierung (generate_p1_cluster_map.py)
3. Dossier-Export (generate_cluster_dossier.py)
4. ZIP-Paketierung (package_project_artifacts.py)
5. SHA-256 Hash-Berechnung (generate_checksums.py)
6. Integritaetspruefung (sha256sum -c)

## 3. Standards & Schnittstellen
- GeoJSON: RFC 7946 / EPSG:4326 (WGS84)
- Tabellen: Microsoft Excel OpenXML (.xlsx)
- Webkarten: HTML5 / Leaflet Engine
- Pruefsummen: SHA-256 (POSIX sha256sum)
