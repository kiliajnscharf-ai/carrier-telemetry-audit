from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

def create_alpaka_pdf():
    filename = "alpaka_checkliste_haus_im_wind.pdf"
    c = canvas.Canvas(filename, pagesize=letter)
    c.drawString(50, 750, "PROJEKT HAUS IM WIND - ALPAKA-CHECKLISTE")
    c.drawString(50, 730, "Herde: Dalia, Betula, Gina, Abelia")
    c.drawString(50, 700, "1. Taeglich: Heu, Wasser und Sichtkontrolle pruefen.")
    c.drawString(50, 680, "2. Woechentlich: Liegeflächen und Wasserbehälter reinigen.")
    c.drawString(50, 660, "3. Monatlich: Gewichtskontrolle und Fell-Check.")
    c.drawString(50, 640, "4. Jährlich: Scheren, Zahnkontrolle und Impfungen.")
    c.save()
    print("PDF-Datei erfolgreich erstellt: alpaka_checkliste_haus_im_wind.pdf")

if __name__ == "__main__":
    create_alpaka_pdf()
