import os
import csv
from src.config import load_financial_data
from src.calculator import calculate_payoff_schedule
from src.visualizer import generate_financial_chart

def main():
    print("=== Launching Variable-Income Debt-to-Savings Planner ===")
    
    try:
        fin_data = load_financial_data()
    except FileNotFoundError as e:
        print(e)
        return

    # Process Simulation
    schedule, raw_months = calculate_payoff_schedule(fin_data)
    
    # Isolate true cross-over pivot points
    debt_free_entry = next((item for item in schedule if item["remaining_balance"] <= 0), None)
    debt_free_month = debt_free_entry["month"] if debt_free_entry else raw_months

    print(f"\n Execution Metrics:")
    print(f" --------------------------------------------------")
    print(f" Strategy Applied          : {fin_data['strategy'].upper()}")
    print(f" Base Disposable Pool      : R {fin_data['base_disposable_income']:.2f}")
    print(f" Debt Free Horizon Target  : {debt_free_month} Months (~{debt_free_month/12:.1f} Years)")
    
    potential_savings = fin_data['base_disposable_income']
    print(f" Post-Debt Monthly Savings : R {potential_savings:.2f}/mo guaranteed base")

    # Generate CSV Output
    os.makedirs('output', exist_ok=True)
    csv_file = 'output/payoff_schedule.csv'
    
    with open(csv_file, mode='w', newline='') as file:
        writer = csv.writer(file)
        headers = ['Month'] + [d['name'] for d in fin_data['debts']] + ['Remaining Balance Total', 'Monthly Savings Capture', 'Cumulative Growth Engine']
        writer.writerow(headers)

        for entry in schedule:
            row = [entry['month']]
            for debt in fin_data['debts']:
                row.append(f"{entry['payments'].get(debt['name'], 0.0):.2f}")
            row.extend([f"{entry['remaining_balance']:.2f}", f"{entry['monthly_savings']:.2f}", f"{entry['cumulative_savings']:.2f}"])
            writer.writerow(row)

    print(f"\n Matrix exported successfully to: {csv_file}")

    # Generate Plot Output
    print(" Compiling data points to construct precision vector maps...")
    generate_financial_chart(schedule)
    print(" Dynamic chart successfully updated: output/debt_vs_savings.png")

if __name__ == "__main__":
    main()
