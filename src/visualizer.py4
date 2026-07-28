import matplotlib.pyplot as plt
import os

def generate_financial_chart(schedule, output_path='output/debt_vs_savings.png'):
    """
    Constructs a visual map.
    Left Axis (Red): Traces debt diving to zero.
    Right Axis (Green/Blue): Traces emergency cash and long-term portfolio growth.
    """
    months = [entry['month'] for entry in schedule]
    debts = [entry['remaining_balance'] for entry in schedule]
    ef_buffer = [entry['emergency_fund'] for entry in schedule]
    investments = [entry['cumulative_savings'] for entry in schedule]

    fig, ax1 = plt.subplots(figsize=(10, 6))

    # Debt Axis (Left)
    color = '#d32f2f'
    ax1.set_xlabel('Timeline Horizon (Months)', fontweight='bold', labelpad=10)
    ax1.set_ylabel('Total Debt Outstanding (R)', color=color, fontweight='bold')
    line1 = ax1.plot(months, debts, color=color, linewidth=2.5, label='Remaining Debt Balance')
    ax1.tick_params(axis='y', labelcolor=color)
    ax1.grid(True, linestyle=':', alpha=0.6)

    # Assets Axis (Right)
    ax2 = ax1.twinx()
    line2 = ax2.plot(months, ef_buffer, color='#0288d1', linewidth=2.0, linestyle=':', label='Liquid Emergency Nest Egg')
    line3 = ax2.plot(months, investments, color='#2e7d32', linewidth=2.5, linestyle='--', label='Compounding Wealth Account')
    ax2.set_ylabel('Accumulated Assets (R)', color='#2e7d32', fontweight='bold')
    ax2.tick_params(axis='y', labelcolor='#2e7d32')

    lines = line1 + line2 + line3
    labels = [l.get_label() for l in lines]
    ax1.legend(lines, labels, loc='upper center', bbox_to_anchor=(0.5, -0.15), ncol=3)
    
    plt.title('Secure Strategy Map: Shielding with Nest Egg prior to Debt Extinction', 
              fontsize=12, fontweight='bold', pad=15)
    
    fig.tight_layout()
    
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
