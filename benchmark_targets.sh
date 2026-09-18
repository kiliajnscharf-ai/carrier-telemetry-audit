#!/usr/bin/env bash
TARGETS=("1.1.1.1" "8.8.8.8" "9.9.9.9" "de-cix.net" "145.254.2.19")
for t in "${TARGETS[@]}"; do ping -c 3 "$t" | tail -1; done
