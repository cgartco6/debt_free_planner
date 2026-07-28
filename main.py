import os
import csv
from src.config import load_financial_data
from src.calculator import run_simulation_engine
from src.visualizer import generate_comparative_chart

def write_csv_output(schedule, filename, debts_meta):
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        headers = ['Month'] + [d['name'] for d in debts_meta] + ['Debt Remaining', 'Nest Egg Value', 'Compounded Net Investment Wealth']
        writer.writerow(headers)
        for entry in schedule:
            row = [entry['month']] + [f"{entry['payments'].get(d['name'], 0.0):.2f}" for d in debts_meta] + [
                f"{entry['remaining_balance']:.2f}", f"{entry['emergency_fund']:.2f}", f"{entry['cumulative_savings']:.2f}"
            ]
            writer.writerow(row)

def main():
    print("=== Launching Dual-Strategy Mathematical Optimizer Engine ===")
    
    try:
        fin_data = load_financial_data()
    except FileNotFoundError:
        print("[!] Core configuration error. Run parse_statement.py first.")
        return

    # Execute split path parallel math
    avalanche_schedule = run_simulation_engine(fin_data, 'avalanche')
    snowball_schedule = run_simulation_engine(fin_data, 'snowball')

    av_df_entry = next((i for i in avalanche_schedule if i["remaining_balance"] <= 0), None)
    sb_df_entry = next((i for i in snowball_schedule if i["remaining_balance"] <= 0), None)

    av_months = av_df_entry["month"] if av_df_entry else len(avalanche_schedule)
    sb_months = sb_df_entry["month"] if sb_df_entry else len(snowball_schedule)

    av_interest = avalanche_schedule[-1]["total_interest_paid"]
    sb_interest = snowball_schedule[-1]["total_interest_paid"]

    # Comparative savings metrics
    interest_savings = sb_interest - av_interest
    time_savings = sb_months - av_months

    print(f"\n==================================================")
    print(f" STRATEGIC OPTIMIZATION INSIGHT REPORT            ")
    print(f"==================================================")
    print(f" AVALANCHE PLAN: Clear in {av_months} months. Interest Paid: R {av_interest:,.2f}")
    print(f" SNOWBALL PLAN : Clear in {sb_months} months. Interest Paid: R {sb_interest:,.2f}")
    print(f"--------------------------------------------------")
    
    if interest_savings > 0:
        print(f" [★] Optimization Verdict: Avalanche saves you R {interest_savings:,.2f} in waste and {time_savings} months of labor.")
    else:
        print(f" [★] Optimization Verdict: Snowball provides parallel efficiency tracking here.")

    # Export outputs
    os.makedirs('output', exist_ok=True)
    write_csv_output(avalanche_schedule, 'output/payoff_avalanche.csv', fin_data['debts'])
    write_csv_output(snowball_schedule, 'output/payoff_snowball.csv', fin_data['debts'])
    generate_comparative_chart(avalanche_schedule, snowball_schedule)
    
    print(f"\n[✓] Both simulation matrices mapped inside the 'output/' directory.")

if __name__ == "__main__":
    main()
