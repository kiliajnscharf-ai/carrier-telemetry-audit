import folium

lat, lon = 51.9850, 9.2550
m = folium.Map(location=[lat, lon], zoom_start=13, tiles="OpenStreetMap")

# Standort-Marker
folium.Marker(
    [lat, lon],
    popup="<b>Mobilfunkstandort P1</b><br>Score: 9.13<br>250 m ü. NN",
    icon=folium.Icon(color="red", icon="signal", prefix="fa")
).add_to(m)

# 5 km Versorgungsradius (Low-Band 700/800 MHz)
folium.Circle(
    radius=5000,
    location=[lat, lon],
    popup="Versorgungsradius 800 MHz (ca. 5 km)",
    color="#FF0000",
    fill=True,
    fill_opacity=0.15
).add_to(m)

m.save("standort_karte.html")
print("Interaktive Karte erfolgreich erstellt: standort_karte.html")
