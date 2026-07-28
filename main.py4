import os
import csv
from src.config import load_financial_data
from src.calculator import calculate_payoff_schedule
from src.visualizer import generate_financial_chart

def main():
    print("=== Launching Compounding Wealth & Inflation Debt-Free Simulator ===")
    
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

    print(f"\n Simulation Metrics Summary:")
    print(f" --------------------------------------------------")
    print(f" Strategy Applied            : {fin_data['strategy'].upper()}")
    print(f" Expected Investment Growth  : {fin_data['investment_rate']*100:.1f}% per annum")
    print(f" Inflation Living Factor     : {fin_data['inflation_rate']*100:.1f}% annual expansion")
    print(f" Debt Free Horizon Target    : {debt_free_month} Months (~{debt_free_month/12:.1f} Years)")
    
    final_savings = schedule[-1]["cumulative_savings"]
    print(f" Long-Term Wealth Account    : R {final_savings:,.2f} tracking post-debt milestones")

    # Generate CSV Output
    os.makedirs('output', exist_ok=True)
    csv_file = 'output/payoff_schedule.csv'
    
    with open(csv_file, mode='w', newline='') as file:
        writer = csv.writer(file)
        headers = ['Month'] + [d['name'] for d in fin_data['debts']] + [
            'Remaining Balance Total', 'Monthly Budgeted Expenses', 'Monthly Wealth Input', 'Compounding Portfolio Value'
        ]
        writer.writerow(headers)

        for entry in schedule:
            row = [entry['month']]
            for debt in fin_data['debts']:
                row.append(f"{entry['payments'].get(debt['name'], 0.0):.2f}")
            row.extend([
                f"{entry['remaining_balance']:.2f}", 
                f"{entry['tracked_expenses']:.2f}",
                f"{entry['monthly_savings']:.2f}", 
                f"{entry['cumulative_savings']:.2f}"
            ])
            writer.writerow(row)

    print(f"\n Detailed path projection table exported to: {csv_file}")

    # Generate Plot Output Vector Graphic
    print(" Mapping variable coordinates into graphic chart layout...")
    generate_financial_chart(schedule)
    print(" Complete vector simulation chart rendered: output/debt_vs_savings.png")

if __name__ == "__main__":
    main()
