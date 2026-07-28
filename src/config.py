import yaml
import os

def load_yaml(filepath):
    """Safely loads and parses YAML configuration files."""
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"The file {filepath} was not found. Please create it.")
    with open(filepath, 'r') as file:
        return yaml.safe_load(file)

def load_financial_data():
    """Combines expenses, complex debts, investment rules, and emergency cash goals."""
    expenses_data = load_yaml('data/expenses.yaml')
    debts_data = load_yaml('data/debts.yaml')
    
    total_expenses = sum(expenses_data.values())
    total_min_payments = sum(debt['minimum_payment'] for debt in debts_data['debts'])
    
    raw_seasonal = debts_data.get('seasonal_income', {})
    seasonal_schedule = {}
    if raw_seasonal:
        for key, value in raw_seasonal.items():
            month_num = int(''.join(filter(str.isdigit, str(key))))
            seasonal_schedule[month_num] = float(value)

    return {
        'net_income': debts_data['current_net_income'],
        'base_expenses': total_expenses,
        'total_min_payments': total_min_payments,
        'debts': debts_data['debts'],
        'strategy': debts_data['strategy'],
        'seasonal_schedule': seasonal_schedule,
        'investment_rate': float(debts_data.get('annual_investment_return', 8.0)) / 100.0,
        'inflation_rate': float(debts_data.get('annual_inflation_rate', 5.0)) / 100.0,
        'ef_months_target': float(debts_data.get('emergency_fund_months_target', 3.0)),
        'current_ef_savings': float(debts_data.get('current_emergency_savings', 0.0))
    }
