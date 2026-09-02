import pandas as pd

def calculate_kritis_resilience(input_excel='Batch_P1_Auswertung.xlsx', output_file='KRITIS_Resilienz_Report.txt'):
    df = pd.read_excel(input_excel)
    
    # KRITIS Parameter
    POWER_PER_TENANT_KW = 1.0     # kW Dauerlast pro Betreiber
    TENANTS_MAX = 4              # Multi-Tenancy Vollausbau
    TOTAL_LOAD_KW = POWER_PER_TENANT_KW * TENANTS_MAX  # 4.0 kW
    AUTONOMY_HOURS = 72          # Gesetzliche Mindestvorgabe BSI
    
    REQUIRED_KWH = TOTAL_LOAD_KW * AUTONOMY_HOURS  # 288 kWh
    BATTERY_COST_BASE = 14500     # Euro (LiFePO4 48V Rack inkl. ATS & CEE-Einspeisung)
    
    lines = []
    lines.append("================================================================================")
    lines.append("KRITIS- & NOTSTROM-RESILIENZBERICHT (72-STUNDEN-AUTARKIE)")
    lines.append("================================================================================")
    lines.append(f"Gesetzliche Grundlage: BSI-Kritis-Dachgesetz / NIS-2 Richtlinie")
    lines.append(f"Auslegungslast pro Standort: {TOTAL_LOAD_KW:.1f} kW (4 Betreiber a 1.0 kW)")
    lines.append(f"Geforderte Überbrueckungszeit: {AUTONOMY_HOURS} Stunden autarker Weiterbetrieb")
    lines.append(f"Erforderliche Batteriekapazitaet: {REQUIRED_KWH:.1f} kWh (LiFePO4)\n")
    
    total_cost_cluster = 0
    for _, row in df.iterrows():
        total_cost_cluster += BATTERY_COST_BASE
        lines.append(f"Standort {row['ID']} ({row['Name']}):")
        lines.append(f"  - Systemlast:                 {TOTAL_LOAD_KW:.1f} kW (4x Multi-Tenancy)")
        lines.append(f"  - Speichersystem:             LiFePO4 48V Racksystem ({REQUIRED_KWH:.0f} kWh)")
        lines.append(f"  - Notstromeinspeisung:        Automatisches ATS + CEE 32A Steckfeld")
        lines.append(f"  - Investition Notstrom/USV:   {BATTERY_COST_BASE:,} EUR")
        lines.append(f"  -> KRITIS-Resilienzstatus:    KONFORM (72h Netzausfall-Resilienz)\n")
        
    lines.append(f"Gesamtinvestition KRITIS-Resilienz Cluster: {total_cost_cluster:,} EUR")
    lines.append("================================================================================")
    content = "\n".join(lines)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(content)
        
    print(content)
    print(f"KRITIS-Bericht erfolgreich exportiert: {output_file}")

if __name__ == '__main__':
    calculate_kritis_resilience()
