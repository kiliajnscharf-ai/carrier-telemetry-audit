letter_content = """Betreff: Qualifizierte Standortmeldung zur Schliessung struktureller Funkloecher (P1-Prioritaet)

Sehr geehrte Damen und Herren der Netz- und Infrastrukturplanung,

anbei uebermittle ich Ihnen das tabellarische Standort-Dossier (P1_Mobilfunk_Standorte.xlsx) fuer einen topografisch exponierten und sofort erschliessbaren Neubaustandort.

Zusammenfassung der technischen Standortdaten:
- Standort-ID:        LOC-01 (Standort A - Bad Pyrmont Huegel)
- WGS84-Koordinaten:  51.985000 N, 9.255000 E
- Gelaendehoehe:      250 m ue. NN (hervorragende Sichtachsen fuer Flaechenabdeckung)
- Infrastruktur:      Niederspannungsanschluss in nur 30 m Distanz; Zufahrt ueber befestigten Wirtschaftsweg
- Versorgungsstatus:  Strukturelles Versorgungsdefizit (RSRP < -115 dBm bei Vodafone, O2 und 1&1; Telekom im Randbereich)
- Kriterien-Score:    9.38 / 10.0 Punkte (Klassifikation: Sofortiger Ausbaubedarf / P1)

Aufgrund der minimalen Tiefbaukosten (kurze Stromanbindung, bestehende Zuwegung) und der maximalen Flaechenwirkung im Low-Band-Bereich (700/800/900 MHz) eignet sich das Areal optimal fuer einen standardisierten Schleuderbeton- oder Gittermasten zur gemeinsamen Nutzung durch mehrere Betreiber.

Die detaillierten Roh- und Bewertungsdaten entnehmen Sie bitte der beigefuegten Datei P1_Mobilfunk_Standorte.xlsx sowie den zugehoerigen GeoJSON-Vektordaten.

Fuer Rueckfragen zur Eigentuemerstruktur und Vor-Ort-Begehung stehe ich Ihnen jederzeit zur Verfuegung.

Mit freundlichen Gruessen
Kilian Scharf
"""

with open("Anschreiben_Standortmeldung_P1.txt", "w", encoding="utf-8") as f:
    f.write(letter_content)

print("Anschreiben erfolgreich exportiert: Anschreiben_Standortmeldung_P1.txt")
