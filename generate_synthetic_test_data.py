import csv

test_records = [
    # Fall 1: Exakter P1-Grenzfall (Score >= 8.50)
    {"id": "TEST-P1", "name": "Exakter P1 Grenzfall", "lat": 51.9950, "lon": 9.2600, "altitude_m": 240, "power_dist_m": 30, "access": "Wirtschaftsweg", "missing_operators": 3},
    # Fall 2: P2-Bereich (Score ca. 7.00 - 8.49)
    {"id": "TEST-P2", "name": "Standard P2 Mittellage", "lat": 51.9800, "lon": 9.2500, "altitude_m": 190, "power_dist_m": 80, "access": "Asphaltiert", "missing_operators": 2},
    # Fall 3: P3-Bereich (Score ca. 5.00 - 6.99)
    {"id": "TEST-P3", "name": "P3 Schwachlage", "lat": 51.9700, "lon": 9.2400, "altitude_m": 170, "power_dist_m": 200, "access": "Wirtschaftsweg", "missing_operators": 1},
    # Fall 4: P4-Ausschluss (Score < 5.00)
    {"id": "TEST-P4", "name": "P4 Totalausschluss", "lat": 51.9600, "lon": 9.2300, "altitude_m": 120, "power_dist_m": 500, "access": "Unbefestigt", "missing_operators": 0}
]

with open("synthetische_testfaelle.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=test_records[0].keys(), delimiter=";")
    writer.writeheader()
    writer.writerows(test_records)

print("Synthetischer Grenzwert-Datensatz erstellt: synthetische_testfaelle.csv")
