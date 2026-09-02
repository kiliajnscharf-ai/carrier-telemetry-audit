import pandas as pd

def evaluate_backhaul(input_excel='Batch_P1_Auswertung.xlsx', output_excel='Backhaul_Anbindung.xlsx'):
    df = pd.read_excel(input_excel)
    
    # Kostenparameter
    COST_RICHTFUNK_BASE = 18000  # Euro Pauschale (2x Link, Antennen, Montage)
    COST_GLASFASER_PER_M = 70    # Euro pro Meter Tiefbau Trasse
    BREAK_EVEN_METER = int(COST_RICHTFUNK_BASE / COST_GLASFASER_PER_M) # ca. 257m
    
    results = []
    lines = []
    lines.append("================================================================================")
    lines.append("BACKHAUL-ANBINDUNG: ENTSCHEIDUNGSMATRIX RICHTFUNK VS. GLASFASER")
    lines.append("================================================================================")
    lines.append(f"Kostenansatz Richtfunk (E-Band/LoS): {COST_RICHTFUNK_BASE:,} EUR pauschal")
    lines.append(f"Kostenansatz Glasfaser (Tiefbau):   {COST_GLASFASER_PER_M} EUR / Meter")
    lines.append(f"Wirtschaftlicher Break-Even-Point:  {BREAK_EVEN_METER} m Glasfasertrasse\n")
    
    for _, row in df.iterrows():
        # Simulierte Distanz zum naechsten Glasfaser-PoP basierend auf Lage
        gf_dist_m = 450 if 'Nordhang' in str(row['Name']) else 600
        gf_total_cost = gf_dist_m * COST_GLASFASER_PER_M
        
        # Entscheidung: Wenn Glasfaser > Break-Even -> Richtfunk bevorzugt
        selected_tech = "Richtfunk (E-Band 10 Gbps)" if gf_total_cost > COST_RICHTFUNK_BASE else "Glasfaser (FTTS)"
        selected_cost = COST_RICHTFUNK_BASE if selected_tech.startswith("Richtfunk") else gf_total_cost
        savings = abs(gf_total_cost - COST_RICHTFUNK_BASE)
        
        results.append({
            'ID': row['ID'],
            'Name': row['Name'],
            'Glasfaser_Distanz_PoP_m': gf_dist_m,
            'Kosten_Glasfaser_EUR': gf_total_cost,
            'Kosten_Richtfunk_EUR': COST_RICHTFUNK_BASE,
            'Empfohlene_Anbindung': selected_tech,
            'Investition_EUR': selected_cost,
            'Kostenvorteil_EUR': savings
        })
        
        lines.append(f"Standort {row['ID']} ({row['Name']}):")
        lines.append(f"  - Distanz zum GF-Hauptverteiler: {gf_dist_m} m (Kosten GF: {gf_total_cost:,} EUR)")
        lines.append(f"  - Kosten Richtfunk-Alternative: {COST_RICHTFUNK_BASE:,} EUR")
        lines.append(f"  -> Empfehlung:                  {selected_tech}")
        lines.append(f"  -> Investitionsersparnis:       {savings:,} EUR gegenueber Glasfaser-Vollausbau\n")
        
    res_df = pd.DataFrame(results)
    res_df.to_excel(output_excel, index=False)
    
    lines.append("================================================================================")
    print("\n".join(lines))
    print(f"Backhaul-Matrix erfolgreich exportiert: {output_excel}")

if __name__ == '__main__':
    evaluate_backhaul()
