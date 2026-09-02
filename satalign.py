#!/usr/bin/env python3
import math

A = 6378137.0
F = 1 / 298.257223563
B = A * (1 - F)
R_GEO = 42164000.0

def deg2rad(d):
    return d * math.pi / 180.0

def rad2deg(r):
    return r * 180.0 / math.pi

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
    if az < 0:
        az += 2 * math.pi
    el = math.atan2(t_u, math.sqrt(t_e**2 + t_n**2))

    skew = math.atan2(math.sin(dlon), math.tan(lat))

    return rad2deg(az), rad2deg(el), rad2deg(skew)

if __name__ == "__main__":
    lat = 51.98
    lon = 9.25
    sat_lon = 19.2

    az, el, skew = az_el_skew(lat, lon, sat_lon)
    print(f"Azimut: {az:.3f}°")
    print(f"Elevation: {el:.3f}°")
    print(f"LNB-Skew: {skew:.3f}°")
