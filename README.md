# Carrier Telemetry & Bufferbloat Audit

Automatisierte Latenz- und Pufferanalyse fuer deutsche Mobilfunk-Core-Knoten.

## Problemstellung
Chronischer Bufferbloat und Tail-Drop-Ereignisse an Aggregationspunkten ohne Active Queue Management (AQM).

## Referenzmessung (Node 145.254.2.19)
- **Baseline:** 42.28 ms
- **Median (p50):** 147.92 ms
- **95. Perzentil (p95):** 1122.47 ms
- **Peak RTT:** 2795.43 ms
- **Paketverlust max:** 90.0 % (Tail-Drop)

## Industriestandard-Empfehlung fuer Carrier (Telekom, Vodafone, O2, 1&1)
1. **AQM Deployment:** FQ-CoDel (RFC 8290) oder CAKE.
2. **Buffer-Sizing:** Reduktion auf Bandwidth-Delay-Product (BDP).
3. **ECN-Marking:** Vermeidung destruktiver Drops durch Explicit Congestion Notification (RFC 3168).

Messdaten und JSON-Telemetrie liegen im Repository vor.
