import pandas as pd
import xml.etree.ElementTree as ET
from xml.dom import minidom

def generate_bnetza_xml(input_excel='Batch_P1_Auswertung.xlsx', output_xml='BNetzA_Antrag_STOB.xml'):
    df = pd.read_excel(input_excel)
    
    root = ET.Element("BNetzA_STOB_Antrag", version="2026.1", standard="BEMFV_26_BImSchV")
    
    antragsteller = ET.SubElement(root, "Antragsteller")
    ET.SubElement(antragsteller, "Unternehmen").text = "Infrastrukturgesellschaft / TowerCo"
    ET.SubElement(antragsteller, "Verfahren").text = "Neuerteilung Standortbescheinigung"
    
    standorte_elem = ET.SubElement(root, "Standortliste")
    
    for _, row in df.iterrows():
        site_id = str(row.get('ID', row.get('id', 'LOC-00')))
        site_name = str(row.get('Name', row.get('name', 'Unbenannt')))
        lat = str(row.get('Breitengrad', row.get('Latitude', row.get('lat', '51.9800'))))
        lon = str(row.get('Laengengrad', row.get('Longitude', row.get('lon', '9.2500'))))
        alt = float(row.get('Hoehe_m', row.get('altitude_m', row.get('Hoehe', 250))))
        
        site = ET.SubElement(standorte_elem, "Standort", id=site_id)
        ET.SubElement(site, "Bezeichnung").text = site_name
        ET.SubElement(site, "Breitengrad").text = lat
        ET.SubElement(site, "Laengengrad").text = lon
        ET.SubElement(site, "Gelaendehoehe_m").text = str(int(alt))
        
        mast_h = 40 if alt > 250 else 30
        antennen_h = mast_h - 2.0
        
        bau = ET.SubElement(site, "Bautechnik")
        ET.SubElement(bau, "Masttyp").text = "40m Gittermast" if mast_h > 30 else "30m Schleuderbetonmast"
        ET.SubElement(bau, "Gesamthoehe_m").text = str(mast_h)
        ET.SubElement(bau, "Antennenunterkante_m").text = str(antennen_h)
        
        sektoren = ET.SubElement(site, "Funkfelder")
        for i, azimut in enumerate([0, 120, 240], start=1):
            sektor = ET.SubElement(sektoren, "Sektor", nr=str(i))
            ET.SubElement(sektor, "Hauptstrahlrichtung_Grad").text = str(azimut)
            ET.SubElement(sektor, "EIRP_Watt").text = "2500"
            ET.SubElement(sektor, "Frequenzbaender").text = "700, 800, 900, 1800, 2100, 3500 MHz"
            ET.SubElement(sektor, "Sicherheitsabstand_Horizontal_m").text = "6.65"
            ET.SubElement(sektor, "Sicherheitsabstand_Vertikal_m").text = "1.46"
            
        mitnutzung = ET.SubElement(site, "Standortmitbenutzung")
        for tenant in ["Deutsche Telekom", "Vodafone", "Telefonica O2", "1&1 Mobilfunk"]:
            t_elem = ET.SubElement(mitnutzung, "Betreiber")
            t_elem.text = tenant
            
    xml_str = minidom.parseString(ET.tostring(root, encoding='utf-8')).toprettyxml(indent="  ")
    
    with open(output_xml, "w", encoding="utf-8") as f:
        f.write(xml_str)
        
    print("================================================================================")
    print("BNETZA-STANDORTBESCHEINIGUNGS-EXPORT (BEMFV STOB-XML) ERFOLGREICH")
    print("================================================================================")
    print(f"Exportiertes XML-Dokument: {output_xml}")
    print(f"Anzahl exportierter Standort-Antraege: {len(df)}")
    print("Sektoren pro Standort: 3 (0°, 120°, 240°) inkl. Multi-Tenancy-Erklaerung")
    print("================================================================================")

if __name__ == '__main__':
    generate_bnetza_xml()
