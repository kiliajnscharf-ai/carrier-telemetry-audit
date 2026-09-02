from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

pdf_path = "Mobilfunk_Standort_Dossier.pdf"
doc = SimpleDocTemplate(pdf_path, pagesize=A4, rightMargin=30, leftMargin=30, topMargin=30, bottomMargin=30)
styles = getSampleStyleSheet()
story = []

title_style = ParagraphStyle(
    "TitleStyle",
    parent=styles["Heading1"],
    fontSize=16,
    leading=20,
    textColor=colors.HexColor("#1A237E")
)

story.append(Paragraph("STANDORT-DOSSIER FUER MOBILFUNK-INFRASTRUKTUR", title_style))
story.append(Paragraph("<b>Klassifikation: Prioritaet P1 (Score: 9.13 / 10)</b>", styles["Normal"]))
story.append(Spacer(1, 15))

data = [
    ["Parameter", "Wert / Status"],
    ["Standortbezeichnung", "Mobilfunkstandort 51.9850_9.2550"],
    ["Geokoordinaten", "51.985000 N, 9.255000 E (WGS84)"],
    ["Gelaendehoehe", "250 m ue. NN (Exponierte Lage)"],
    ["Stromanschluss", "Hausanschluss / Trasse in 30 m Distanz"],
    ["Zuwegung", "Befestigter Wirtschaftsweg vorhanden"],
    ["Vodafone", "RSRP < -115 dBm (Funkloch)"],
    ["O2 Telefonica", "RSRP < -115 dBm (Funkloch)"],
    ["1&1 Mobilfunk", "Keine Netzabdeckung (No Service)"],
    ["Deutsche Telekom", "RSRP -105 bis -115 dBm (Randversorgung)"],
    ["Empfohlene Baender", "Band 28 (700 MHz), Band 20 (800 MHz), Band 8 (900 MHz)"],
    ["Empfohlene Bauart", "30 - 40 m Schleuderbeton- / Gittermast"]
]

t = Table(data, colWidths=[180, 340])
t.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#1A237E")),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('FONTSIZE', (0, 0), (-1, -1), 9),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
    ('TOPPADDING', (0, 0), (-1, -1), 5),
    ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
    ('BACKGROUND', (0, 6), (-1, 8), colors.HexColor("#FFCDD2")),
    ('BACKGROUND', (0, 9), (-1, 9), colors.HexColor("#FFF9C4"))
]))

story.append(t)
doc.build(story)
print("PDF erfolgreich generiert: Mobilfunk_Standort_Dossier.pdf")
