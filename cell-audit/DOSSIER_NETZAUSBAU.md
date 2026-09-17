# Technisches Dossier: Antrag auf Infrastrukturausbau / Neubau Mobilfunkmast
**Zielgebiet:** Bad Pyrmont (Standort Haus im Wind)  
**Betreiber:** Vodafone GmbH / Vantage Towers  
**Referenz-Messdaten:** Öffentliches Audit-Repository (GitHub)

---

## 1. Problemstellung und Versorgungsdefizit
Am genannten Standort liegt eine dauerhafte, gravierende Unterversorgung vor. Das Endgerät wird mangels lokaler Funkzelle auf den ca. 10–13 km entfernten Standort Lügde (Dingelstedtpfad, Cell-ID `50515:31`) eingebucht. 

Durch die topografische Lage und die extreme Distanz treten massive Übertragungsfehler auf, die bis zum vollständigen Abreißen der Datenverbindung führen.

## 2. Physikalische Messdaten (Ist-Zustand)
- **Frequenzband:** 5G NSA / LTE Band 28 (700 MHz)
- **RSRP:** -118 dBm (Grenzempfindlichkeit unterschritten)
- **SNR:** -1 dB (Signalpegel unter dem Grundrauschen)
- **Timing Advance:** 124 (Belegt 10–13 km Funkstreckendistanz)
- **Paketverlust:** Wiederkehrend >= 33%
- **Latenz:** Schwankend zwischen 56 ms und 144 ms
- **Ausfallzeiten:** Nachgewiesene HTTP-Verbindungsabbrüche (Status 000)

## 3. Forderungskatalog
1. **Neubau / Errichtung eines Mobilfunkstandorts** im Areal Bad Pyrmont / Haus im Wind zur Schließung der Versorgungslücke.
2. **Prüfung temporärer Maßnahmen** (z. B. mobile Mastlösung oder Sektor-Nachjustierung), bis die Neubauplanung abgeschlossen ist.
3. **Formelle Weiterleitung an die Netzplanung und das Rollout-Management** (Vantage Towers / Vodafone Infrastruktur).
4. **Vorlage bei der Bundesnetzagentur (BNetzA)** als Nachweis der Nichterfüllung der Versorgungsauflagen gemäß TKG.

---
*Erstellt auf Basis automatisierter Messreihen via cell-audit.*

### Ergänzende Durchsatzmessung (17.09.2026, 11:44 Uhr Lokalzeit)
- **Download:** 1,27 Mb/s (95,6% unter Bundesdurchschnitt)
- **Upload:** 0,30 Mb/s (96,9% unter Bundesdurchschnitt)
- **Latenz:** 63 ms
- **Systemhinweis:** SCHWACHES SIGNAL (LTE+ / IP: 109.41.48.108)
- **Beweisführung:** Der minimale Upload bricht interaktive Sitzungen und App-Verbindungen reproduzierbar ab.
