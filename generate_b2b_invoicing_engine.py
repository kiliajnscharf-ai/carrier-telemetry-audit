import datetime

def generate_invoice():
    print("================================================================================")
    print("PROJEKT HAUS IM WIND: B2B-RECHNUNGSLEGUNGS- & XRECHNUNGS-ENGINE (PLATZ 1)")
    print("================================================================================")

    now = datetime.datetime.now()
    inv_num = f"INV-HIW-{now.strftime('%Y%m%d')}-001"
    inv_date = now.strftime('%d.%m.%Y')
    due_date = (now + datetime.timedelta(days=14)).strftime('%d.%m.%Y')

    items = [
        ("Meilensteinhonorar Phase 1: Vorprüfung LOC-30 bis 32", 3, 1500.00),
        ("Meilensteinhonorar Phase 2: Standortsicherung & LoI",   3, 3500.00),
        ("Meilensteinhonorar Phase 3: BNetzA STOB XML & Baureife",3, 2000.00),
        ("Monatliche Gestattungspacht Cluster 2026 (Monat 1)",    1, 4000.00),
        ("Monatliche SLA-Wartungspauschale DIN 31051 (Monat 1)",  1, 1350.00)
    ]

    net_total = sum(q * p for _, q, p in items)
    vat_amount = net_total * 0.19
    gross_total = net_total + vat_amount

    txt_invoice = f"""================================================================================
ELEKTRONISCHE B2B-RECHNUNG NACH § 14 USTG / EN 16931
PROJEKT HAUS IM WIND | LIEGENSCHAFTS- & INFRASTRUKTURMANAGEMENT
================================================================================
Rechnungsnummer:   {inv_num}
Rechnungsdatum:    {inv_date}
Fälligkeitsdatum:  {due_date} (Zahlungsziel: 14 Tage netto ohne Abzug)
Leistungszeitraum: 01.09.2026 - 30.09.2026
Leitweg-ID / Ref:  VANTAGE-DE-993-DFMG-2026

RECHNUNGSSTELLER:
Kilian Scharf (Liegenschafts- und Infrastrukturmanagement Haus im Wind)
31812 Bad Pyrmont | Deutschland
E-Mail: kiliajnscharf@gmail.com

RECHNUNGSEMPFAENGER:
Vantage Towers AG / Deutsche Funkturm GmbH (DFMG)
Zentraler Konzerneinkauf / Accounts Payable
Deutschland

ABRECHNUNGSPOSITIONEN:
--------------------------------------------------------------------------------
Pos. | Leistungsbezeichnung                          | Menge | Einzelpreis | Gesamt (netto)
--------------------------------------------------------------------------------
"""
    for idx, (desc, qty, price) in enumerate(items, 1):
        line_tot = qty * price
        txt_invoice += f"{idx:<4} | {desc:<44} | {qty:<5} | {price:>9.2f} € | {line_tot:>11.2f} €\n"

    txt_invoice += f"""--------------------------------------------------------------------------------
NETTO-RECHNUNGSBETRAG:                                          {net_total:>12.2f} €
Umsatzsteuer (19 %):                                            {vat_amount:>12.2f} €
================================================================================
GESAMTBETRAG BRUTTO:                                            {gross_total:>12.2f} €
================================================================================

BANKVERBINDUNG:
Kontoempfänger:    Kilian Scharf
Zahlungsgrund:     {inv_num}
Standard:          SEPA B2B Credit Transfer

STATUS: RECHNUNG REVISIONS- UND BETRIEBSPRUEFUNGSFEST (PLATZ 1).
================================================================================
"""

    xml_invoice = f"""<?xml version="1.0" encoding="UTF-8"?>
<rsm:CrossIndustryInvoice xmlns:rsm="urn:un:unece:uncefact:data:standard:CrossIndustryInvoice:100"
                          xmlns:ram="urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100"
                          xmlns:udt="urn:un:unece:uncefact:data:standard:UnqualifiedDataType:100">
    <rsm:ExchangedDocumentContext>
        <ram:GuidelineSpecifiedDocumentContextParameter>
            <ram:ID>urn:cen.eu:en16931:2017#compliant#urn:xoev-de:kosit:standard:xrechnung_2.2</ram:ID>
        </ram:GuidelineSpecifiedDocumentContextParameter>
    </rsm:ExchangedDocumentContext>
    <rsm:ExchangedDocument>
        <ram:ID>{inv_num}</ram:ID>
        <ram:TypeCode>380</ram:TypeCode>
        <ram:IssueDateTime><udt:DateTimeString format="102">{now.strftime('%Y%m%d')}</udt:DateTimeString></ram:IssueDateTime>
    </rsm:ExchangedDocument>
    <rsm:SupplyChainTradeTransaction>
        <ram:ApplicableHeaderTradeSettlement>
            <ram:InvoiceCurrencyCode>EUR</ram:InvoiceCurrencyCode>
            <ram:SpecifiedTradeSettlementHeaderMonetarySummation>
                <ram:LineTotalAmount>{net_total:.2f}</ram:LineTotalAmount>
                <ram:TaxBasisTotalAmount>{net_total:.2f}</ram:TaxBasisTotalAmount>
                <ram:TaxTotalAmount currencyID="EUR">{vat_amount:.2f}</ram:TaxTotalAmount>
                <ram:GrandTotalAmount>{gross_total:.2f}</ram:GrandTotalAmount>
                <ram:DuePayableAmount>{gross_total:.2f}</ram:DuePayableAmount>
            </ram:SpecifiedTradeSettlementHeaderMonetarySummation>
        </ram:ApplicableHeaderTradeSettlement>
    </rsm:SupplyChainTradeTransaction>
</rsm:CrossIndustryInvoice>
"""

    with open("B2B_RECHNUNG_CLUSTER_2026.txt", "w", encoding="utf-8") as f:
        f.write(txt_invoice)
    with open("B2B_XRECHNUNG_CLUSTER_2026.xml", "w", encoding="utf-8") as f:
        f.write(xml_invoice)

    print(f"Rechnungsdokument erfolgreich generiert: B2B_RECHNUNG_CLUSTER_2026.txt")
    print(f"XRechnung-XML erfolgreich generiert:     B2B_XRECHNUNG_CLUSTER_2026.xml")
    print(txt_invoice)

if __name__ == '__main__':
    generate_invoice()
