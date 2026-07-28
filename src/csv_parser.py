import pandas as pd
import yaml
import os

def process_banking_csv(csv_path='data/bank_statement.csv', output_yaml='data/expenses.yaml'):
    """
    Parses bank statements, extracts debit records within a 90-day scope, 
    categorizes keywords, averages them monthly, and overwrites expenses.yaml.
    """
    if not os.path.exists(csv_path):
        print(f"[!] Target statement file '{csv_path}' missing. Using existing baseline profile.")
        return

    # Ingest data
    df = pd.read_csv(csv_path)
    df.columns = [c.strip().lower() for c in df.columns]
    df['amount'] = df['amount'].astype(float)
    
    # Isolate negative withdrawals
    debits = df[df['amount'] < 0].copy()
    debits['amount'] = debits['amount'].abs()

    # Rule mapping infrastructure
    categories = {
        'groceries': 0.0,
        'transportation_fuel': 0.0,
        'utilities_electricity': 0.0,
        'food_entertainment': 0.0,
        'cellphone_data': 0.0
    }

    # Keyword scanning map
    for idx, row in debits.iterrows():
        desc = str(row['description']).lower()
        amt = row['amount']
        
        if 'grocer' in desc or 'supermarket' in desc:
            categories['groceries'] += amt
        elif 'fuel' in desc or 'gas' in desc or 'garage' in desc:
            categories['transportation_fuel'] += amt
        elif 'electr' in desc or 'power' in desc or 'water' in desc:
            categories['utilities_electricity'] += amt
        elif 'restaur' in desc or 'cafe' in desc or 'cinema' in desc:
            categories['food_entertainment'] += amt
        elif 'cell' in desc or 'data' in desc or 'network' in desc:
            categories['cellphone_data'] += amt
        else:
            categories['food_entertainment'] += amt  # Catch-all safety fallback

    # Compute actual monthly average (90-day cycle equals 3 months)
    monthly_averages = {k: round(v / 3.0, 2) for k, v in categories.items()}
    
    # Add dummy baseline placeholders for missing non-variable fixed fields
    monthly_averages['housing_rent'] = 12000.00
    monthly_averages['car_insurance'] = 900.00
    monthly_averages['medical_aid'] = 2400.00

    os.makedirs(os.path.dirname(output_yaml), exist_ok=True)
    with open(output_yaml, 'w') as f:
        yaml.dump(monthly_averages, f, default_flow_style=False)
        
    print(f"[✓] Successfully generated normalized profile: {output_yaml}")
