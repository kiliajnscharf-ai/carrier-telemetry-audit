import datetime
import os

def create_maintenance_ticket(component, issue, priority, material_used):
    now = datetime.datetime.now()
    ticket_id = f"TICK-HIW-{now.strftime('%Y%m%d%H%M%S')}"
    date_str = now.strftime('%d.%m.%Y %H:%M:%S')

    ticket_entry = f"""================================================================================
INSTANDHALTUNGS- & MAENGELTICKET (DIN 31051)
ID: {ticket_id} | DATUM: {date_str}
================================================================================
Liegenschaft:      Haus im Wind (Lokalbereich / Technikträger)
Erfasser:          Kilian Scharf (Liegenschafts- und Infrastrukturmanagement)
Komponente:        {component}
Priorität:         {priority} (Prio 1: Sofort / Prio 2: 24h / Prio 3: Zyklisch)

FEHLERBESCHREIBUNG / BEFUND:
{issue}

DURCHGEFUEHRTE MASSNAHME & MATERIALEINSATZ:
- Instandsetzung:  Fachgerecht behoben nach Herstellervorgabe
- Verwendetes Mat: {material_used}
- Werkzeugstandard:DIN EN ISO 6789 / VDE konform

STATUS: ERLEDIGT & ABGENOMMEN (PLATZ 1)
================================================================================\n"""

    with open("B2B_MAENGEL_TICKET_LOG.txt", "a", encoding="utf-8") as f:
        f.write(ticket_entry)

    print(f"Ticket erfolgreich angelegt und archiviert: {ticket_id}")
    print(ticket_entry)

if __name__ == '__main__':
    # Initialer Test-Eintrag für eine präventive Wartung
    create_maintenance_ticket(
        component="Kabeldurchführung Hauptverteilung",
        issue="Präventive Nachdichtung gegen Feuchtigkeitseintritt",
        priority="PRIO-3",
        material_used="OTTOSEAL S 110 (Premium-Neutral-Silikon)"
    )
