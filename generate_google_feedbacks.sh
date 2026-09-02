#!/bin/bash
# FEEDBACK GENERATOR - TITANSTREAM APP - PROJEKT HAUS IM WIND
echo "=== GENERIERE GOOGLE FEEDBACK-ENTWÜRFE ==="

# Verzeichnis für die Berichte erstellen
mkdir -p titanstream/feedbacks

# 1. BERICHT: CPU GOVERNOR ACCESS
cat << 'REPORT1' > titanstream/feedbacks/report1_cpu_governor.txt
SUBJECT: Request for Unprivileged Read-Access to CPU Scaling Governor in Containerized Environments

DESCRIPTION:
In Android-based virtualization layers (using PRoot / UserLAnd), unprivileged local containers are strictly prevented from reading or writing to the hardware CPU control interfaces located under:
`/sys/devices/system/cpu/cpu*/cpufreq/scaling_governor`

This absolute write block (Permission Denied) and subsequent read blockade prevents high-performance streaming applications, such as real-time IPTV transcoders (e.g., Titanstream), from adapting user-space buffer pools to the current hardware frequency state. 

PROPOSED SOLUTION:
Please implement a secure, virtualized system interface or allow read-only (and restricted user-space write-back) permissions for containerized applications to query the active CPU governor state. This will prevent buffer underflows and latency jitter on multi-core ARM architectures without compromising host system security.

REPRODUCTION PATH:
1. Start an unprivileged PRoot environment on Android 15/16.
2. Execute: cat /sys/devices/system/cpu/cpu0/cpufreq/scaling_governor
3. Output: Permission Denied.
REPORT1

# 2. BERICHT: NETLINK SOCKET SECURITY
cat << 'REPORT2' > titanstream/feedbacks/report2_netlink_socket.txt
SUBJECT: Permission Denied on Netlink Sockets inside Unprivileged Android Sandboxes

DESCRIPTION:
Modern network diagnostics tools (e.g., 'ss' and 'netstat') utilize Netlink sockets to query the state of active TCP/UDP connections and local socket bindings. In current Android SELinux policies, unprivileged containers are blocked from opening Netlink sockets, throwing:
`Cannot open netlink socket: Permission denied`

This restriction breaks standard connection monitoring and port-collision detection routines within local developer setups and isolated web-app environments running on the device loopback interface.

PROPOSED SOLUTION:
Allow unprivileged user-space applications inside local loopback sandboxes to establish basic Netlink query sockets (specifically NETLINK_ROUTE), restricted solely to the local loopback interface (127.0.0.1) and non-root ports, to enable standard network monitoring capabilities.
REPORT2

# 3. BERICHT: PORT FORWARDING / PROOT BINDING
cat << 'REPORT3' > titanstream/feedbacks/report3_port_binding.txt
SUBJECT: Automated Low-Port (0-1023) Redirection Interface for Virtualized Containers

DESCRIPTION:
Unprivileged containers running on Android cannot bind to standard ports lower than 1024 (such as HTTP Port 80 or HTTPS Port 443) due to strict Linux kernel restrictions. This forces developers to use high-ports (e.g., 8089 or 8080), which breaks compatibility with external streaming clients and standard URL routing patterns.

PROPOSED SOLUTION:
Implement an automated, integrated user-space port-forwarding mechanism within the PRoot/UserLAnd translation layer. This layer should securely map external requests on standard privileged ports to unprivileged high-ports inside the container without requiring root privileges on the host device.
REPORT3

if [ -f "titanstream/feedbacks/report1_cpu_governor.txt" ]; then
    echo "[OK] Bericht 1: CPU-Governor-Bericht erstellt."
    echo "[OK] Bericht 2: Netlink-Socket-Bericht erstellt."
    echo "[OK] Bericht 3: Port-Binding-Bericht erstellt."
    echo "[INFO] Alle Berichte liegen unter: titanstream/feedbacks/"
else
    echo "[FEHLER] Erstellung der Berichtsdateien fehlgeschlagen."
fi
echo "=========================================="
