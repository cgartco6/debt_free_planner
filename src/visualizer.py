import matplotlib.pyplot as plt
import os

def generate_comparative_chart(avalanche_sched, snowball_sched, output_path='output/strategy_compare.png'):
    """ Renders side-by-side strategic trajectories mapping debt paydown lines. """
    av_months = [e['month'] for e in avalanche_sched]
    av_debts = [e['remaining_balance'] for e in avalanche_sched]
    
    sb_months = [e['month'] for e in snowball_sched]
    sb_debts = [e['remaining_balance'] for e in snowball_sched]

    plt.figure(figsize=(10, 5))
    plt.plot(av_months, av_debts, color='#d32f2f', linewidth=2.5, label='Avalanche Strategy (Highest Rate First)')
    plt.plot(sb_months, sb_debts, color='#f57c00', linewidth=2.0, linestyle='--', label='Snowball Strategy (Smallest Balance First)')
    
    plt.xlabel('Timeline Horizon (Months)', fontweight='bold')
    plt.ylabel('Remaining Outstanding Balances (R)', fontweight='bold')
    plt.title('Optimization Analysis Matrix: Avalanche Strategy vs. Snowball Strategy Timeline', fontsize=11, fontweight='bold', pad=12)
    plt.grid(True, linestyle=':', alpha=0.6)
    plt.legend(loc='upper right')
    
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
