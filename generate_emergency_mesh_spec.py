import datetime

def generate_emergency_spec():
    print("================================================================================")
    print("PROJEKT HAUS IM WIND: AUTARKES NOTFUNK- & KRISENKOMMUNIKATIONS-SYSTEM (PLATZ 1)")
    print("================================================================================")

    content = f"""================================================================================
AUTARKE NOTFUNK- UND KRISENKOMMUNIKATIONS-SPEZIFIKATION
BSI-KRITIS 72H-RESILIENZ-MESH (PROJEKT HAUS IM WIND)
================================================================================
Erstellungsdatum:  {datetime.datetime.now().strftime('%d.%m.%Y %H:%M:%S')}
Projektleitung:    Kilian Scharf (Autarke Liegenschaftsinstandhaltung Haus im Wind)
Normen & Gesetze:  BSI-KRITIS, AFuG, DIN EN 62305, DIN VDE 0100, CEPT ERC/REC 70-03

1. EBENE 1: DEZENTRALES BÜRGER-NOTFALL-MESH (LORA 868 MHZ)
--------------------------------------------------------------------------------
- Frequenzbereich:           869.400 - 869.650 MHz (SRD g3 Band, Duty Cycle 10 %)
- Sendeleistung:             500 mW ERP (27 dBm)
- Modulation & Parameter:    LoRa Chirp Spread Spectrum (Bandbreite 125 kHz, SF 11/12)
- Routing-Protokoll:         Meshtastic Flooding-Algorithmus (kein zentraler Master)
- Verschlüsselung:           AES-256 GCM End-to-End für Leitstellen, offener Notkanal
- Antennensystem:            Vertikale Rundstrahlantenne (6 dBi Gewinn) auf Mastspitze
- Primäre Funktion:          Textbasierte Notfall-Alarme, GPS-Tracking, Zivilschutzmeldungen

2. EBENE 2: TAKTISCHER SPRACH- & RELAISFUNK (VHF 2M / UHF 70CM)
--------------------------------------------------------------------------------
- Frequenzzuweisung:         VHF: 145.600 - 145.7875 MHz | UHF: 438.650 - 439.400 MHz
- Betriebsarten:             Dual-Mode: FM Analog (1750 Hz Tonruf / CTCSS) & DMR Tier II
- Sendeleistung Relais:      15 Watt ERP (Notstromoptimiert)
- Weichen- & Filtertechnik:  6-Topf-Koaxialkavitäten-Duplexer (Isolation > 80 dB)
- Relais-Standort:           LOC-32 (Bergkuppe Nordost, Höchster Geländepunkt)
- Reichweiten-Radius:        ca. 45 - 80 km optische und beugungsunterstützte Abdeckung

3. EBENE 3: HOCHLEISTUNGS-IP-BACKBONE (HAMNET 5.8 GHZ)
--------------------------------------------------------------------------------
- Frequenzbereich:           5.650 - 5.850 GHz (Amateurfunkdienst / Richtfunk)
- Bandbreite & Modulation:   10 MHz Kanalbandbreite, OFDM (bis zu 64-QAM)
- Antennentyp:               Parabol- und Panelantennen mit Radom (24 dBi Gewinn)
- Durchsatz:                 Netto bis 85 Mbps Vollduplex zwischen LOC-30, 31 und 32
- Redundanz:                 RSTP-vermaschter Ring mit automatischem Failover (< 1 s)
- Dienste im Backbone:       Dezentraler SIP-Telefonieserver (Asterisk), internes Wiki,
                             Wetter- & Pegelstandssensorik, BNetzA-Messdatenerfassung

4. ENERGIEVERSORGUNG, MONTAGE & BLITZSCHUTZ
--------------------------------------------------------------------------------
- Primäre DC-Quelle:         Direktspeisung aus 288 kWh LiFePO4-USV (48V Nennspannung)
- Spannungswandlung:         Galvanisch getrennte DC/DC-Wandler (Mean Well RSD-100-12/24)
- USV-Laufzeit Notfunk:      > 180 Tage autarker Dauerbetrieb (bei Ausfall des Primärnetzes)
- HF-Zuleitungen:            Dämpfungsarmes Ecoflex 10 Plus Koaxialkabel
- Kabeldurchführungen:       Gas- und wasserdicht versiegelt mit OTTOSEAL S 110
- Blitzschutzableiter:       Koaxiale Gasentladungsableiter, geerdet mit 50 mm² Cu
                             (Pressung nach DIN EN 61238-1 mit Knipex Spezialgesenk)

================================================================================
STATUS: SPEZIFIKATION DEFINIERT - SCHLUESSELFERTIGE RESILIENZ-ARCHITEKTUR (PLATZ 1)
================================================================================
"""
    filename = "B2B_EMERGENCY_MESH_SPEC.txt"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Notfunk-Spezifikation erfolgreich generiert: {filename}")
    print(content)

if __name__ == '__main__':
    generate_emergency_spec()
