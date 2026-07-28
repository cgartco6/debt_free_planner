import yaml
import os

def load_yaml(filepath):
    """Safely loads and parses YAML configuration files."""
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"The file {filepath} was not found. Please create it.")
    with open(filepath, 'r') as file:
        return yaml.safe_load(file)

def load_financial_data():
    """Combines expenses and debts data into a unified dictionary."""
    expenses_data = load_yaml('data/expenses.yaml')
    debts_data = load_yaml('data/debts.yaml')
    
    total_expenses = sum(expenses_data.values())
    total_min_payments = sum(debt['minimum_payment'] for debt in debts_data['debts'])
    
    # Disposable income is what we can use to aggressively pay off debt
    disposable_income = debts_data['current_net_income'] - total_expenses
    
    return {
        'net_income': debts_data['current_net_income'],
        'total_expenses': total_expenses,
        'disposable_income': disposable_income,
        'total_min_payments': total_min_payments,
        'debts': debts_data['debts'],
        'strategy': debts_data['strategy']
    }
