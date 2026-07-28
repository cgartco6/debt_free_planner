import os
import csv
from src.config import load_financial_data
from src.calculator import calculate_payoff_schedule
from src.visualizer import generate_financial_chart

def main():
    print("=== Launching Secure Nest-Egg & Debt Paydown Engine ===")
    
    try:
        fin_data = load_financial_data()
    except FileNotFoundError as e:
        print(e)
        return

    # Process Simulation Engine Matrix
    schedule, raw_months = calculate_payoff_schedule(fin_data)
    
    # Isolate cross-over debt elimination index
    debt_free_entry = next((item for item in schedule if item["remaining_balance"] <= 0), None)
    debt_free_month = debt_free_entry["month"] if debt_free_entry else raw_months

    # Identify when emergency fund first hits target metrics
    target_ef_val = fin_data['base_expenses'] * fin_data['ef_months_target']
    ef_ready_entry = next((item for item in schedule if item["emergency_fund"] >= target_ef_val), None)
    ef_ready_month = ef_ready_entry["month"] if ef_ready_entry else "N/A"

    print(f"\n Strategy Metrics Summary:")
    print(f" --------------------------------------------------")
    print(f" Paydown Strategy Mode       : {fin_data['strategy'].upper()}")
    print(f" Target Nest Egg Shield      : {fin_data['ef_months_target']} Months of Expenses (~R {target_ef_val:,.2f})")
    print(f" Nest Egg Fully Stacked Month: Month {ef_ready_month}")
    print(f" Debt Free Horizon Target    : Month {debt_free_month} (~{debt_free_month/12:.1f} Years)")
    
    final_wealth = schedule[-1]["cumulative_savings"]
    print(f" Final Portfolio Value       : R {final_wealth:,.2f}")

    # Generate CSV Output
    os.makedirs('output', exist_ok=True)
    csv_file = 'output/payoff_schedule.csv'
    
    with open(csv_file, mode='w', newline='') as file:
        writer = csv.writer(file)
        headers = [
            'Month'
        ] + [d['name'] for d in fin_data['debts']] + [
            'Remaining Balance Total', 
            'Liquid Emergency Fund', 
            'Monthly Wealth Input', 
            'Compounding Portfolio Value'
        ]
        writer.writerow(headers)

        for entry in schedule:
            row = [entry['month']]
            for debt in fin_data['debts']:
                row.append(f"{entry['payments'].get(debt['name'], 0.0):.2f}")
            row.extend([
                f"{entry['remaining_balance']:.2f}", 
                f"{entry['emergency_fund']:.2f}",
                f"{entry['monthly_savings']:.2f}", 
                f"{entry['cumulative_savings']:.2f}"
            ])
            writer.writerow(row)

    print(f"\n Detailed path projection table exported to: {csv_file}")

    print(" Mapping advanced asset variables onto custom chart space...")
    generate_financial_chart(schedule)
    print(" Complete graphic trajectory map rendered: output/debt_vs_savings.png")

if __name__ == "__main__":
    main()
