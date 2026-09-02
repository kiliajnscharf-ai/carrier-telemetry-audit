import pandas as pd
import folium

# 1. Daten aus Excel laden
df = pd.read_excel("Batch_P1_Auswertung.xlsx")

# 2. Kartenzentrum berechnen (Mittelwert der Koordinaten)
center_lat = df["Breitengrad"].mean()
center_lon = df["Laengengrad"].mean()

m = folium.Map(location=[center_lat, center_lon], zoom_start=12, tiles="OpenStreetMap")

# 3. Standorte und 5-km-Funkradien einzeichnen
for _, row in df.iterrows():
    lat = row["Breitengrad"]
    lon = row["Laengengrad"]
    site_id = row["ID"]
    name = row["Name"]
    score = row["Score"]
    alt = row["Hoehe_m"]

    popup_text = f"""
    <b>{site_id} - {name}</b><br>
    Prioritaet: <b>P1</b> (Score: {score})<br>
    Hoehe: {alt} m ue. NN<br>
    Versorgungsradius: 800 MHz Low-Band
    """

    # Marker
    folium.Marker(
        [lat, lon],
        popup=popup_text,
        tooltip=f"{site_id}: {name} (P1)",
        icon=folium.Icon(color="green", icon="signal", prefix="fa")
    ).add_to(m)

    # 5 km Funkzelle (Low-Band Band 20/28)
    folium.Circle(
        location=[lat, lon],
        radius=5000,
        color="#1E7E34",
        weight=2,
        fill=True,
        fill_opacity=0.15,
        popup=f"Versorgungszone 5 km ({site_id})"
    ).add_to(m)

# 4. Karte speichern
output_map = "P1_Standorte_Cluster_Karte.html"
m.save(output_map)
print(f"Interaktive Cluster-Karte erfolgreich generiert: {output_map}")
