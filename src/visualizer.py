import matplotlib.pyplot as plt
import os

def generate_financial_chart(schedule, output_path='output/debt_vs_savings.png'):
    """
    Constructs a dual-axis mathematical trajectory plot.
    Left Axis (Red): Traces debt diving to zero.
    Right Axis (Green): Traces freed-up savings climbing rapidly.
    """
    months = [entry['month'] for entry in schedule]
    debts = [entry['remaining_balance'] for entry in schedule]
    savings = [entry['cumulative_savings'] for entry in schedule]

    fig, ax1 = plt.subplots(figsize=(10, 6))

    # Primary Curve - Debt Paydown Line
    color = '#d32f2f'
    ax1.set_xlabel('Timeline Horizon (Months)', fontweight='bold', labelpad=10)
    ax1.set_ylabel('Total Debt Outstanding (R)', color=color, fontweight='bold')
    line1 = ax1.plot(months, debts, color=color, linewidth=2.5, label='Remaining Debt Balance')
    ax1.tick_params(axis='y', labelcolor=color)
    ax1.grid(True, linestyle=':', alpha=0.6)

    # Secondary Axis - Compounding Savings Velocity
    ax2 = ax1.twinx()
    color = '#2e7d32'
    ax2.set_ylabel('Accumulated Savings Pool (R)', color=color, fontweight='bold')
    line2 = ax2.plot(months, savings, color=color, linewidth=2.5, linestyle='--', label='Accumulated Post-Debt Savings')
    ax2.tick_params(axis='y', labelcolor=color)

    # Contextual Layout
    lines = line1 + line2
    labels = [l.get_label() for l in lines]
    ax1.legend(lines, labels, loc='upper center', bbox_to_anchor=(0.5, -0.15), ncol=2)
    
    plt.title('Short-Term and Long-Term Horizon Transformation Map\n(Debt Extinction Transitioning Into Pure Wealth Accumulation)', 
              fontsize=12, fontweight='bold', pad=15)
    
    fig.tight_layout()
    
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
