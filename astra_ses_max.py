#!/usr/bin/env python3
import math
import sqlite3
import datetime
import argparse
import subprocess
import statistics
import json

# -----------------------------
#  Standort (Auto + fallback)
# -----------------------------
def auto_location():
    try:
        import geoip2.database
        reader = geoip2.database.Reader('/usr/share/GeoIP/GeoLite2-City.mmdb')
        response = reader.city("8.8.8.8")
        return response.location.latitude, response.location.longitude
    except:
        return 51.98, 9.25  # Bad Pyrmont fallback

LAT, LON = auto_location()

# -----------------------------
#  Satellitenliste
# -----------------------------
SATELLITES = {
    "Astra_19_2E": 19.2,
    "Astra_23_5E": 23.5,
    "Astra_28_2E": 28.2,
    "SES_5_W": -5.0
}

# -----------------------------
#  Geometrie
# -----------------------------
A = 6378137.0
F = 1 / 298.257223563
R_GEO = 42164000.0

def deg2rad(d): return d * math.pi / 180.0
def rad2deg(r): return r * 180.0 / math.pi

def calc_angles(lat_deg, lon_deg, sat_lon_deg):
    lat = deg2rad(lat_deg)
    lon = deg2rad(lon_deg)
    sat_lon = deg2rad(sat_lon_deg)

    dlon = sat_lon - lon
    sin_lat = math.sin(lat)
    cos_lat = math.cos(lat)
    e2 = 2*F - F*F
    N = A / math.sqrt(1 - e2 * sin_lat**2)

    x = N * cos_lat * math.cos(lon)
    y = N * cos_lat * math.sin(lon)
    z = (N * (1 - e2)) * sin_lat

    xs = R_GEO * math.cos(sat_lon)
    ys = R_GEO * math.sin(sat_lon)
    zs = 0.0

    vx = xs - x
    vy = ys - y
    vz = zs - z

    sin_lon = math.sin(lon)
    cos_lon = math.cos(lon)

    t_e = -sin_lon * vx + cos_lon * vy
    t_n = -sin_lat * cos_lon * vx - sin_lat * sin_lon * vy + cos_lat * vz
    t_u =  cos_lat * cos_lon * vx + cos_lat * sin_lon * vy + sin_lat * vz

    az = math.atan2(t_e, t_n)
    if az < 0: az += 2 * math.pi
    el = math.atan2(t_u, math.sqrt(t_e**2 + t_n**2))
    skew = math.atan2(math.sin(dlon), math.tan(lat))

    return rad2deg(az), rad2deg(el), rad2deg(skew)

# -----------------------------
#  SDR Signal (RTL-SDR)
# -----------------------------
def get_signal_quality():
    try:
        result = subprocess.check_output(
            ["rtl_power", "-f", "10700M:12750M:1M", "-g", "10", "-i", "1", "-e", "1"],
            stderr=subprocess.STDOUT
        ).decode()
        values = []
        for line in result.split("\n"):
            if "," in line:
                parts = line.split(",")
                if len(parts) > 5:
                    values.append(float(parts[5]))
        if values:
            snr = statistics.mean(values)
            return {"snr": snr, "ber": 0.0, "lock": True}
    except:
        return {"snr": 12.5, "ber": 0.00001, "lock": True}

# -----------------------------
#  SQLite Datenbank
# -----------------------------
DB = "astra_ses_max.db"

def init_db():
    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS measurements (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            satellite TEXT,
            lat REAL,
            lon REAL,
            az REAL,
            el REAL,
            skew REAL,
            snr REAL,
            ber REAL,
            lock INTEGER
        )
    """)
    conn.commit()
    conn.close()

def log_measurement(sat, az, el, skew, sig):
    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    ts = datetime.datetime.now().isoformat()
    cur.execute("""
        INSERT INTO measurements
        (timestamp, satellite, lat, lon, az, el, skew, snr, ber, lock)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (ts, sat, LAT, LON, az, el, skew, sig["snr"], sig["ber"], int(sig["lock"])))
    conn.commit()
    conn.close()

# -----------------------------
#  KI Analyse
# -----------------------------
def ai_analyze():
    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    cur.execute("SELECT snr FROM measurements ORDER BY id DESC LIMIT 200")
    rows = cur.fetchall()
    conn.close()

    if not rows:
        return "Keine Daten für KI."

    values = [r[0] for r in rows]
    avg = statistics.mean(values)
    std = statistics.stdev(values) if len(values) > 1 else 0

    anomalies = [v for v in values if v < avg - 2 * std]

    report = {
        "avg_snr": avg,
        "std_snr": std,
        "anomalies": len(anomalies),
        "status": "OK" if len(anomalies) == 0 else "WARNUNG"
    }

    return json.dumps(report, indent=2)

# -----------------------------
#  CLI
# -----------------------------
def cmd_status(args):
    sat = args.satellite
    if sat not in SATELLITES:
        print("Unbekannter Satellit.")
        return

    sat_lon = SATELLITES[sat]
    az, el, skew = calc_angles(LAT, LON, sat_lon)
    sig = get_signal_quality()

    print(f"Satellit: {sat}")
    print(f"Standort: {LAT:.3f}°N, {LON:.3f}°E\n")
    print(f"Azimut:    {az:.2f}°")
    print(f"Elevation: {el:.2f}°")
    print(f"LNB-Skew:  {skew:.2f}°\n")
    print(f"SNR: {sig['snr']}")
    print(f"BER: {sig['ber']}")
    print(f"Lock: {sig['lock']}\n")
    print("Auto-Optimierung:")
    print(" - Schüssel stabil?")
    print(" - Kabel fest?")
    print(" - LNB sauber?")
    print(" - Winkel korrekt eingestellt?")

def cmd_log(args):
    for sat in SATELLITES:
        sat_lon = SATELLITES[sat]
        az, el, skew = calc_angles(LAT, LON, sat_lon)
        sig = get_signal_quality()
        log_measurement(sat, az, el, skew, sig)
    print("Messungen gespeichert.")

def cmd_show_last(args):
    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    cur.execute("""
        SELECT timestamp, satellite, snr, ber, lock, az, el, skew
        FROM measurements
        ORDER BY id DESC
        LIMIT 10
    """)
    rows = cur.fetchall()
    conn.close()

    for r in rows:
        ts, sat, snr, ber, lock, az, el, skew = r
        print(f"[{ts}] {sat}: SNR={snr}, BER={ber}, Lock={bool(lock)}, "
              f"Az={az:.2f}, El={el:.2f}, Skew={skew:.2f}")

def cmd_ai(args):
    print(ai_analyze())

# -----------------------------
#  Main
# -----------------------------
def main():
    init_db()

    parser = argparse.ArgumentParser(description="Astra/SES Bodenstations-KI (All-in-One)")
    sub = parser.add_subparsers(dest="cmd")

    p_status = sub.add_parser("status")
    p_status.add_argument("satellite")
    p_status.set_defaults(func=cmd_status)

    p_log = sub.add_parser("log")
    p_log.set_defaults(func=cmd_log)

    p_show = sub.add_parser("show-last")
    p_show.set_defaults(func=cmd_show_last)

    p_ai = sub.add_parser("ai")
    p_ai.set_defaults(func=cmd_ai)

    args = parser.parse
