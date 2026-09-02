import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side

def generate_max_portfolio():
    print("================================================================================")
    print("B2B-MAXIMAL-PORTFOLIO & EXPANSIONS-KALKULATOR (PROJEKT HAUS IM WIND)")
    print("================================================================================")

    wb = openpyxl.Workbook()
    
    # Styles
    navy_fill = PatternFill(start_color="0F243E", end_color="0F243E", fill_type="solid")
    blue_fill = PatternFill(start_color="1F4E78", end_color="1F4E78", fill_type="solid")
    accent_fill = PatternFill(start_color="D9E1F2", end_color="D9E1F2", fill_type="solid")
    white_bold = Font(name="Calibri", size=11, bold=True, color="FFFFFF")
    title_font = Font(name="Calibri", size=14, bold=True, color="0F243E")
    bold_font = Font(name="Calibri", size=10, bold=True)
    reg_font = Font(name="Calibri", size=10)
    
    center = Alignment(horizontal="center", vertical="center")
    right = Alignment(horizontal="right", vertical="center")
    left = Alignment(horizontal="left", vertical="center")
    thin = Border(
        left=Side(style='thin', color='D9D9D9'),
        right=Side(style='thin', color='D9D9D9'),
        top=Side(style='thin', color='D9D9D9'),
        bottom=Side(style='thin', color='D9D9D9')
    )

    # TABELLE 1: MAXIMAL-SZENARIEN
    ws1 = wb.active
    ws1.title = "Gesamt_Expansion"
    ws1.merge_cells("A1:F1")
    ws1["A1"] = "MAXIMAL-PORTFOLIO: EXPANSION & BUNDESWEITE B2B-SKALIERUNG"
    ws1["A1"].font = title_font
    ws1["A1"].alignment = left

    headers_exp = ["Szenario-Level", "Suchkreise (p.a.)", "Akquisitions-Erlöse", "Mietertrag Cluster 2026", "Jahres-Gesamtumsatz", "Mtl. Cashflow"]
    ws1.append([])
    ws1.append(headers_exp)
    for col in range(1, 7):
        c = ws1.cell(row=3, column=col)
        c.fill = navy_fill
        c.font = white_bold
        c.alignment = center

    scenarios = [
        ("Level 0: Nur Pacht (Cluster 2026)", 0, 0.0, 93900.0, 93900.0, 7825.00),
        ("Level 1: Regional (12 SK, 85%)", 12, 77000.0, 93900.0, 170900.0, 14241.67),
        ("Level 2: Gebiets-GU (50 SK, 85%)", 50, 325000.0, 93900.0, 418900.0, 34908.33),
        ("Level 3: Bund-Max (100 SK, 90%)", 100, 655000.0, 93900.0, 748900.0, 62408.33)
    ]

    for row_idx, s in enumerate(scenarios, start=4):
        ws1.cell(row=row_idx, column=1, value=s[0]).alignment = left
        ws1.cell(row=row_idx, column=2, value=s[1]).alignment = center
        for c_idx in range(3, 7):
            cell = ws1.cell(row=row_idx, column=c_idx, value=s[c_idx-1])
            cell.number_format = '#,##0.00 €'
            cell.alignment = right
        
        is_max = (s[1] == 100)
        for col in range(1, 7):
            c = ws1.cell(row=row_idx, column=col)
            c.border = thin
            if is_max:
                c.font = bold_font
                c.fill = accent_fill
            else:
                c.font = reg_font

    for col in ["A", "B", "C", "D", "E", "F"]:
        ws1.column_dimensions[col].width = 26

    # TABELLE 2: 4-SÄULEN REINVESTITION (MAXIMALSTUFE)
    ws2 = wb.create_sheet(title="Reinvestition_Maximal")
    ws2.merge_cells("A1:E1")
    ws2["A1"] = "BUDGET-ALLOKATION BUNDESWEITE MAXIMALSTUFE (748.900,00 € p.a.)"
    ws2["A1"].font = title_font
    
    headers_reinv = ["Säule", "Zweck / Premium-Ausrüstung", "Anteil (%)", "Jahresbudget", "Monatliches Budget"]
    ws2.append([])
    ws2.append(headers_reinv)
    for col in range(1, 6):
        c = ws2.cell(row=3, column=col)
        c.fill = blue_fill
        c.font = white_bold
        c.alignment = center

    reinv_data = [
        ("Säule 1: Werkzeuge", "Knipex, Wera Profi-Sätze, Akku-Pressen, Drehmomenttechnik", 0.25, 187225.0, 15602.08),
        ("Säule 2: Autarkie", "LiFePO4-Zellen, Wechselrichter, Otto-Chemie, Notstrom", 0.30, 224670.0, 18722.50),
        ("Säule 3: IT & Server", "Industrie-Workstations, Messgeräte, FIPS-HSM, Linux-Nodes", 0.15, 112335.0, 9361.25),
        ("Säule 4: Reserve", "Liquidität, Baurechts-Sicherung, Gewerbe-Rücklagen", 0.30, 224670.0, 18722.50),
        ("GESAMT", "Volle Reinvestition & Zukunftssicherung (Platz 1)", 1.00, 748900.0, 62408.33)
    ]

    for row_idx, r in enumerate(reinv_data, start=4):
        ws2.cell(row=row_idx, column=1, value=r[0]).alignment = left
        ws2.cell(row=row_idx, column=2, value=r[1]).alignment = left
        c_pct = ws2.cell(row=row_idx, column=3, value=r[2])
        c_pct.number_format = '0.0 %'
        c_pct.alignment = center
        c_yr = ws2.cell(row=row_idx, column=4, value=r[3])
        c_yr.number_format = '#,##0.00 €'
        c_yr.alignment = right
        c_mo = ws2.cell(row=row_idx, column=5, value=r[4])
        c_mo.number_format = '#,##0.00 €'
        c_mo.alignment = right

        is_tot = (r[0] == "GESAMT")
        for col in range(1, 6):
            c = ws2.cell(row=row_idx, column=col)
            c.border = thin
            if is_tot:
                c.font = bold_font
                c.fill = accent_fill
            else:
                c.font = reg_font

    ws2.column_dimensions["A"].width = 24
    ws2.column_dimensions["B"].width = 50
    ws2.column_dimensions["C"].width = 16
    ws2.column_dimensions["D"].width = 20
    ws2.column_dimensions["E"].width = 22

    excel_file = "B2B_MAX_PORTFOLIO_MASTER.xlsx"
    wb.save(excel_file)
    print(f"Master-Excel erfolgreich generiert: {excel_file}")

    summary_text = """================================================================================
B2B-MAXIMAL-EXPANSION: EXECUTIVE MASTER REPORT
================================================================================
ERTRAGSPOTENZIAL DER MAXIMALSTUFE (100 SUCHKREISE + CLUSTER 2026):
- Jahresumsatz Akquisitions-Dienstleistung:     655.000,00 EUR
- Jahresumsatz Mieterträge (4 Betreiber + USV):   93.900,00 EUR
--------------------------------------------------------------------------------
GESAMT-JAHRESUMSATZ (NETTO):                     748.900,00 EUR
MONATLICHER BRUTTO-CASHFLOW:                      62.408,33 EUR / Monat

STRATEGISCHE ALLOKATION DES MAXIMALBUDGETS:
- 25 % Profi-Ausrüstung (Knipex / Wera):         187.225,00 EUR / Jahr
- 30 % Autarke Energiesysteme (LiFePO4/Otto):    224.670,00 EUR / Jahr
- 15 % IT- & Messinfrastruktur (FIPS/Linux):     112.335,00 EUR / Jahr
- 30 % Kapitalreserve & Projektsicherung:        224.670,00 EUR / Jahr
================================================================================
STATUS: MAXIMAL-PIPELINE ERFOLGREICH KALKULIERT UND DOKUMENTIERT.
================================================================================
"""
    with open("B2B_MAX_PORTFOLIO_REPORT.txt", "w", encoding="utf-8") as f:
        f.write(summary_text)
    print(summary_text)

if __name__ == '__main__':
    generate_max_portfolio()
