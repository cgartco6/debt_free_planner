import os
import csv
from src.config import load_financial_data
from src.calculator import calculate_payoff_schedule

def main():
    print("=== Initializing Accurate Debt-Free Planner ===")
    
    # Load Data
    try:
        fin_data = load_financial_data()
    except FileNotFoundError as e:
        print(e)
        return

    # Calculate
    schedule, total_months, future_savings_rate = calculate_payoff_schedule(fin_data)

    print(f"\n Strategy Used: {fin_data['strategy'].title()}")
    print(f" Disposable Income Available for Debt: {fin_data['disposable_income']:.2f}")
    print(f" Estimated Time to Debt Freedom: {total_months} months (~{total_months/12:.1f} years)")
    print(f" Amount that will automatically transition to SAVINGS after debt is cleared: {future_savings_rate:.2f} per month")

    # Ensure Output Directory Exists
    os.makedirs('output', exist_ok=True)

    # Write Short to Long-Term Plan to CSV
    csv_file = 'output/payoff_schedule.csv'
    with open(csv_file, mode='w', newline='') as file:
        writer = csv.writer(file)
        
        # Headers
        headers = ['Month'] + [debt['name'] for debt in fin_data['debts']] + ['Total Remaining Debt']
        writer.writerow(headers)

        # Rows
        for entry in schedule:
            row = [entry['month']]
            for debt in fin_data['debts']:
                amount_paid = entry['payments'].get(debt['name'], 0.0)
                row.append(f"{amount_paid:.2f}")
            row.append(f"{entry['remaining_balance']:.2f}")
            writer.writerow(row)

    print(f"\n Full short-to-long term payoff plan has been exported to {csv_file}")
    print(" When a debt is paid off, its payment value is automatically added to the next debt (snowballing your savings potential).")

if __name__ == "__main__":
    main()
