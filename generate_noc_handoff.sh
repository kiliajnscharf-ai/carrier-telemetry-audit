#!/usr/bin/env bash
set -euo pipefail

EVIDENCE_DIR="vodafone_evidence"
JSON_OUT="${EVIDENCE_DIR}/noc_incident_payload.json"
CONFIG_OUT="${EVIDENCE_DIR}/as3209_mitigation_template.txt"
TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

echo "Generiere maschinenlesbares Carrier-Ticket (JSON)..."
cat << JSON_EOF > "$JSON_OUT"
{
  "incident_ticket": {
    "generated_utc": "$TIMESTAMP",
    "target_as": "AS3209",
    "target_operator": "Vodafone GmbH (Core Infrastructure)",
    "fault_domain": "IP Backbone Core / Queue Management",
    "affected_node": "145.254.2.19",
    "sla_metrics": {
      "nominal_rtt_ms": 40.10,
      "max_observed_rtt_ms": 284.00,
      "max_recorded_jitter_ms": 186.80,
      "tcp_connect_latency_s": 0.4134,
      "tls_handshake_latency_s": 0.6183,
      "path_mtu_bytes": 1500,
      "mtu_1500_rtt_ms": 302.73,
      "packet_loss_events": "Tail-drop observed (TIMEOUT at peak congestion)"
    },
    "diagnosis": "Severe active queue bufferbloat during concurrent TCP workloads on hop 145.254.2.19. Inadequate AQM parameter tuning causing high tail latency.",
    "recommended_remediation": [
      "Deploy FQ-CoDel / RED on egress queue of interface hosting 145.254.2.19",
      "Re-evaluate BGP local preference metrics to alleviate peak interface saturation",
      "Verify control-plane policing (CoPP) thresholds for ICMP rate limiting"
    ]
  }
}
JSON_EOF

echo "Generiere Router-Konfigurations-Template für das Core-Engineering..."
cat << CONFIG_EOF > "$CONFIG_OUT"
======================================================================
 VODAFONE AS3209 CORE ENGINEERING - RECOMMENDED REMEDIATION TEMPLATE
 AFFECTED HOP: 145.254.2.19 (Vodafone Core Backbone)
======================================================================

Option A: Cisco IOS-XR / ASR 9000 Series (Queue Mitigation)
----------------------------------------------------------------------
policy-map AS3209-CORE-AQM-REMEDY
 class class-default
  queue-limit 15 ms
  random-detect ecn
  random-detect default 20 ms 50 ms
!
interface TenGigE/HundredGigE [Target-Interface-145.254.2.19]
 service-policy output AS3209-CORE-AQM-REMEDY
commit

Option B: Juniper JunOS (Active Queue Management / RED)
----------------------------------------------------------------------
set class-of-service drop-profiles AS3209-CORE-DROP interpolate fill-level 40 drop-probability 5
set class-of-service drop-profiles AS3209-CORE-DROP interpolate fill-level 80 drop-probability 100
set class-of-service schedulers AS3209-SCHEDULER buffer-size temporal 15k
set class-of-service schedulers AS3209-SCHEDULER drop-profile-map loss-priority any protocol any drop-profile AS3209-CORE-DROP
commit comment "Mitigate AS3209 core queue bufferbloat on 145.254.2.19"
======================================================================
CONFIG_EOF

echo "Übergabe-Artefakte erfolgreich erstellt:"
echo "1. $JSON_OUT"
echo "2. $CONFIG_OUT"
