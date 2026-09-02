#!/usr/bin/env python3
import math
import sqlite3
import datetime
import argparse
import sys

# --- Debug-Banner ---
print("Astra/SES Bodenstation – Ultra-Stabile Version startet...")

# --- Standort (fest, kein Auto-Location) ---
LAT = 51.98   # Bad Pyrmont
LON = 9.25

# --- Satellitenliste ---
SATELLITES = {
    "Astra_19_2E": 19.2,
    "Astra_23_5E": 23.5,
    "Astra_28_2E": 28.2,
    "SES_5_W": -5.0
}

# --- Geometrie Konstanten ---
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

# --- Signal-Stub (immer stabil, keine externen Tools) ---
def get_signal_quality():
    return {
        "snr": 12.5,
        "ber": 0.00001,
        "lock": True
    }

# --- SQLite Datenbank ---
DB = "astra_ses_ultra.db"

def init_db():
    try:
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
    except Exception as e:
        print("Fehler beim Initialisieren der Datenbank:", e)
        sys.exit(1)

def log_measurement(sat, az, el, skew, sig):
    try:
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
    except Exception as e:
        print("Fehler beim Schreiben in die Datenbank:", e)

# --- CLI-Funktionen ---
def cmd_status(args):
    sat = args.satellite
    if sat not in SATELLITES:
        print("Unbekannter Satellit. Verfügbar:")
        for name in SATELLITES:
            print(" -", name)
        return

    sat_lon = SATELLITES[sat]
    az, el, skew = calc_angles(LAT, LON, sat_lon)
    sig = get_signal_quality()

    print("\n=== STATUS ===")
    print(f"Satellit: {sat}")
    print(f"Standort: {LAT:.3f}°N, {LON:.3f}°E\n")
    print(f"Azimut:    {az:.2f}°")
    print(f"Elevation: {el:.2f}°")
    print(f"LNB-Skew:  {skew:.2f}°\n")
    print(f"SNR: {sig['snr']} dB")
    print(f"BER: {sig['ber']}")
    print(f"Lock: {sig['lock']}\n")
    print("Wartungshinweise:")
    print(" - Schüssel stabil?")
    print(" - Kabel fest?")
    print(" - LNB sauber?")
    print(" - Winkel korrekt eingestellt?")

def cmd_log(args):
    print("\nMessungen werden geloggt...")
    for sat in SATELLITES:
        sat_lon = SATELLITES[sat]
        az, el, skew = calc_angles(LAT, LON, sat_lon)
        sig = get_signal_quality()
        log_measurement(sat, az, el, skew, sig)
    print("Messungen gespeichert in", DB)

def cmd_show_last(args):
    try:
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
    except Exception as e:
        print("Fehler beim Lesen aus der Datenbank:", e)
        return

    if not rows:
        print("Keine Messungen vorhanden.")
        return

    print("\n=== LETZTE MESSUNGEN ===")
    for r in rows:
        ts, sat, snr, ber, lock, az, el, skew = r
        print(f"[{ts}] {sat}: SNR={snr} dB, BER={ber}, Lock={bool(lock)}, "
              f"Az={az:.2f}°, El={el:.2f}°, Skew={skew:.2f}°")

# --- Main ---
def main():
    init_db()

    parser = argparse.ArgumentParser(
        description="Astra/SES Bodenstation – Ultra-Stabile Version (eine Datei, mit SQLite)"
    )
    sub = parser.add_subparsers(dest="cmd")

    p_status = sub.add_parser("status", help="Status für einen Satelliten anzeigen")
    p_status.add_argument("satellite", help="z.B. Astra_19_2E")
    p_status.set_defaults(func=cmd_status)

    p_log = sub.add_parser("log", help="Messungen für alle Satelliten speichern")
    p_log.set_defaults(func=cmd_log)

    p_show = sub.add_parser("show-last", help="letzte Messungen anzeigen")
    p_show.set_defaults(func=cmd_show_last)

    args = parser.parse_args()
    if hasattr(args, "func"):
        args.func(args)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
