#!/usr/bin/env python3
import math
import datetime
import geoip2.database

A = 6378137.0
F = 1 / 298.257223563
R_GEO = 42164000.0

SATELLITES = {
    "Astra_19_2E": 19.2,
    "Astra_23_5E": 23.5,
    "Astra_28_2E": 28.2,
    "SES_5_W": -5.0
}

def deg2rad(d): return d * math.pi / 180.0
def rad2deg(r): return r * 180.0 / math.pi

def auto_location():
    try:
        reader = geoip2.database.Reader('/usr/share/GeoIP/GeoLite2-City.mmdb')
        response = reader.city("8.8.8.8")  # Trick: GeoIP nutzt lokale DB
        lat = response.location.latitude
        lon = response.location.longitude
        return lat, lon
    except:
        return None, None

def az_el_skew(lat_deg, lon_deg, sat_lon_deg):
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

def log_result(lat, lon, sat_name, az, el, skew):
    ts = datetime.datetime.now().isoformat()
    line = f"{ts};{lat};{lon};{sat_name};{az:.3f};{el:.3f};{skew:.3f}\n"
    with open("astra_helper.log", "a") as f:
        f.write(line)

def main():
    print("Astra/SES Helfer – Auto-Location aktiviert\n")

    lat, lon = auto_location()
    if lat is None:
        print("Standort konnte nicht automatisch erkannt werden.")
        return

    print(f"Automatisch erkannter Standort:")
    print(f"  Breite: {lat:.4f}°")
    print(f"  Länge:  {lon:.4f}°")

    print("\nVerfügbare Satelliten:")
    for name in SATELLITES:
        print(f"  - {name}")
    sat_name = input("\nSatellit wählen: ").strip()

    if sat_name not in SATELLITES:
        print("Unbekannter Satellit.")
        return

    sat_lon = SATELLITES[sat_name]
    az, el, skew = az_el_skew(lat, lon, sat_lon)

    print("\nErgebnis:")
    print(f"  Azimut:    {az:.3f}°")
    print(f"  Elevation: {el:.3f}°")
    print(f"  LNB-Skew:  {skew:.3f}°")

    print("\nWartungs-Checkliste:")
    print("  [ ] Schüssel stabil?")
    print("  [ ] Kabel fest?")
    print("  [ ] LNB sauber?")
    print("  [ ] Winkel korrekt eingestellt?")
    print("  [ ] Signalqualität geprüft?")

    log_result(lat, lon, sat_name, az, el, skew)
    print("\nMessung gespeichert in 'astra_helper.log'.")

if __name__ == "__main__":
    main()
