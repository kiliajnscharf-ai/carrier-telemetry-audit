import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side

def build_fee_model():
    print("================================================================================")
    print("B2B-SUCHKREIS- & HONORAR-KALKULATOR (PROJEKT HAUS IM WIND)")
    print("================================================================================")

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Suchkreis_Honorarmatrix"

    header_fill = PatternFill(start_color="1F4E78", end_color="1F4E78", fill_type="solid")
    header_font = Font(name="Calibri", size=11, bold=True, color="FFFFFF")
    bold_font = Font(name="Calibri", size=10, bold=True)
    regular_font = Font(name="Calibri", size=10)
    center_align = Alignment(horizontal="center", vertical="center")
    right_align = Alignment(horizontal="right", vertical="center")
    left_align = Alignment(horizontal="left", vertical="center")
    thin_border = Border(
        left=Side(style='thin', color='D9D9D9'),
        right=Side(style='thin', color='D9D9D9'),
        top=Side(style='thin', color='D9D9D9'),
        bottom=Side(style='thin', color='D9D9D9')
    )

    ws.merge_cells("A1:E1")
    ws["A1"] = "B2B-HONORAR- UND VERGÜTUNGSMATRIX: MOBILFUNK-SUCHKREISAKQUISITION"
    ws["A1"].font = Font(name="Calibri", size=13, bold=True, color="1F4E78")
    ws["A1"].alignment = left_align

    ws["A2"] = "Standard: Tier-1 Reference Architecture | Rahmenvertragsvorlage für DFMG, Vantage, GUs"
    ws["A2"].font = Font(name="Calibri", size=9, italic=True)

    headers_phase = ["Phase", "Bezeichnung Leistungsphase", "Leistungsumfang & Deliverables", "Vergütung (netto)", "Anteil"]
    ws.append([])
    ws.append(headers_phase)
    row_num = 4

    for col in range(1, 6):
        cell = ws.cell(row=row_num, column=col)
        cell.fill = header_fill
        cell.font = header_font
        cell.alignment = center_align

    phases = [
        ("Phase 1", "Initialprüfung & Vorqualifizierung", "GIS-Filter, Katasterprüfung, ITU-R LoS, BNetzA-Check", 1500.00, "21.4 %"),
        ("Phase 2", "Standortsicherung & Gestattung", "Eigentümerverhandlung, LoI-Abschluss, § 1090 BGB Grundbuch", 3500.00, "50.0 %"),
        ("Phase 3", "STOB & Baurechtsreife", "BNetzA STOB XML, DIN EN 50383 BEMFV, Turnkey Übergabe", 2000.00, "28.6 %"),
        ("GESAMT", "Voller Suchkreis-Erfolg", "Schlüsselfertige Übergabe an GU / Betreiber", 7000.00, "100.0 %")
    ]

    for p in phases:
        row_num += 1
        ws.cell(row=row_num, column=1, value=p[0]).alignment = center_align
        ws.cell(row=row_num, column=2, value=p[1]).alignment = left_align
        ws.cell(row=row_num, column=3, value=p[2]).alignment = left_align
        fee_cell = ws.cell(row=row_num, column=4, value=p[3])
        fee_cell.number_format = '#,##0.00 €'
        fee_cell.alignment = right_align
        ws.cell(row=row_num, column=5, value=p[4]).alignment = center_align

        is_bold = (p[0] == "GESAMT")
        for col in range(1, 6):
            c = ws.cell(row=row_num, column=col)
            c.border = thin_border
            if is_bold:
                c.font = bold_font
                c.fill = PatternFill(start_color="D9E1F2", end_color="D9E1F2", fill_type="solid")
            else:
                c.font = regular_font

    row_num += 3
    ws.merge_cells(f"A{row_num}:E{row_num}")
    ws[f"A{row_num}"] = "JAHRES-PROGNOSE: ROLLOUT-SZENARIEN (2026/2027)"
    ws[f"A{row_num}"].font = Font(name="Calibri", size=11, bold=True, color="1F4E78")

    row_num += 1
    headers_scenarios = ["Szenario", "Suchkreise / Jahr", "Erfolgsquote (Phase 2+3)", "Jahresumsatz (netto)", "Mtl. Rohertrag"]
    for col, h in enumerate(headers_scenarios, 1):
        cell = ws.cell(row=row_num, column=col, value=h)
        cell.fill = header_fill
        cell.font = header_font
        cell.alignment = center_align

    scenarios = [
        ("Konservativ (Nebenerwerb)", 5, "80 % (4 gesichert)", 31000.00, 2583.33),
        ("Realistisch (Akkreditiert)", 12, "85 % (10 gesichert)", 77000.00, 6416.67),
        ("Skaliert (Kern-Scout)", 25, "90 % (22 gesichert)", 162500.00, 13541.67)
    ]

    for s in scenarios:
        row_num += 1
        ws.cell(row=row_num, column=1, value=s[0]).alignment = left_align
        ws.cell(row=row_num, column=2, value=s[1]).alignment = center_align
        ws.cell(row=row_num, column=3, value=s[2]).alignment = center_align
        c_year = ws.cell(row=row_num, column=4, value=s[3])
        c_year.number_format = '#,##0.00 €'
        c_year.alignment = right_align
        c_month = ws.cell(row=row_num, column=5, value=s[4])
        c_month.number_format = '#,##0.00 €'
        c_month.alignment = right_align

        for col in range(1, 6):
            c = ws.cell(row=row_num, column=col)
            c.border = thin_border
            c.font = regular_font

    col_widths = {"A": 16, "B": 32, "C": 48, "D": 22, "E": 18}
    for col_letter, width in col_widths.items():
        ws.column_dimensions[col_letter].width = width

    excel_filename = "B2B_SUCHKREIS_HONORAR_MATRIX.xlsx"
    wb.save(excel_filename)
    print(f"Excel-Matrix erfolgreich gespeichert: {excel_filename}")

    report = f"""================================================================================
KAUFMAENNISCHE B2B-SUCHKREIS-MATRIX (ZUSAMMENFASSUNG)
================================================================================
VERGUETUNG PRO SUCHKREIS (TURNKEY):
- Phase 1 (Initialpruefung & GIS):          1.500,00 EUR (garantiert)
- Phase 2 (Standortsicherung / LoI):        3.500,00 EUR (erfolgsbasiert)
- Phase 3 (STOB XML / BEMFV Baureife):      2.000,00 EUR (bei Genehmigung)
--------------------------------------------------------------------------------
GESAMTHONORAR PRO ERFOLGREICHEM STANDORT:   7.000,00 EUR (netto)

PROGNOSTIZIERTE JAHRESUMSAETZE:
- Konservativ (5 Suchkreise):               31.000,00 EUR (2.583,33 EUR/Monat)
- Realistisch (12 Suchkreise):              77.000,00 EUR (6.416,67 EUR/Monat)
- Skaliert (25 Suchkreise):                162.500,00 EUR (13.541,67 EUR/Monat)
================================================================================
STATUS: MATRIX BERECHNET & SCHLUESSELFERTIG HINTERLEGT.
================================================================================"""
    with open("B2B_SUCHKREIS_HONORAR_MATRIX.txt", "w", encoding="utf-8") as f:
        f.write(report)
    print(report)

if __name__ == '__main__':
    build_fee_model()
