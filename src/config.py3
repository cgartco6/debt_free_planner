import yaml
import os

def load_yaml(filepath):
    """Safely loads and parses YAML configuration files."""
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"The file {filepath} was not found. Please create it.")
    with open(filepath, 'r') as file:
        return yaml.safe_load(file)

def load_financial_data():
    """Combines expenses and complex variable debt configurations."""
    expenses_data = load_yaml('data/expenses.yaml')
    debts_data = load_yaml('data/debts.yaml')
    
    total_expenses = sum(expenses_data.values())
    total_min_payments = sum(debt['minimum_payment'] for debt in debts_data['debts'])
    
    # Base monthly disposable income after fixed expenses
    base_disposable_income = debts_data['current_net_income'] - total_expenses
    
    # Process seasonal inputs securely into normalized integer mapping
    raw_seasonal = debts_data.get('seasonal_income', {})
    seasonal_schedule = {}
    if raw_seasonal:
        for key, value in raw_seasonal.items():
            month_num = int(''.join(filter(str.isdigit, str(key))))
            seasonal_schedule[month_num] = float(value)

    return {
        'net_income': debts_data['current_net_income'],
        'total_expenses': total_expenses,
        'base_disposable_income': base_disposable_income,
        'total_min_payments': total_min_payments,
        'debts': debts_data['debts'],
        'strategy': debts_data['strategy'],
        'seasonal_schedule': seasonal_schedule
    }
