import json
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

data = {
  "alpaka_checkliste_erweitert": {
    "herde": [
      { "name": "Dalia", "typ": "Alpaka", "rolle": "Ruhig / ausgeglichen" },
      { "name": "Betula", "typ": "Alpaka", "rolle": "Neugierig / aufmerksam" },
      { "name": "Gina", "typ": "Alpaka", "rolle": "Sozial / freundlich" },
      { "name": "Abelia", "typ": "Alpaka", "rolle": "Sensibel / vorsichtig" }
    ],
    "aufgaben": {
      "taeglich": [
        { "task": "Heu kontrollieren", "priority": "hoch", "time_required_minutes": 5, "responsible": "Bewohner Haus im Wind", "notes": "Heu muss trocken und sauber sein." },
        { "task": "Wasser frisch machen", "priority": "hoch", "time_required_minutes": 5, "responsible": "Bewohner Haus im Wind", "notes": "Eimer ausspülen und neu befüllen." }
      ],
      "woechentlich": [
        { "task": "Liegeflächen reinigen", "priority": "hoch", "time_required_minutes": 10, "responsible": "Team Stallpflege", "notes": "Stroh tauschen." }
      ]
    }
  }
}

pdf_filename = "alpaka_checkliste_haus_im_wind.pdf"
doc = SimpleDocTemplate(pdf_filename, pagesize=letter)
styles = getSampleStyleSheet()
story = []

story.append(Paragraph("PROJEKT HAUS IM WIND - ALPAKA-CHECKLISTE", styles['Title']))
story.append(Spacer(1, 12))

for kat, aufgaben_liste in data["alpaka_checkliste_erweitert"]["aufgaben"].items():
    story.append(Paragraph(f"Kategorie: {kat.upper()}", styles['Heading2']))
    for aufgabe in aufgaben_liste:
        text = f"- {aufgabe['task']} (Priorität: {aufgabe['priority']}, Dauer: {aufgabe['time_required_minutes']} Min, Wer: {aufgabe['responsible']})"
        story.append(Paragraph(text, styles['Normal']))
    story.append(Spacer(1, 8))

doc.build(story)
print("Vollständige PDF-Checkliste erfolgreich generiert.")
