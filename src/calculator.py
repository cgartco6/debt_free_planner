def run_simulation_engine(financial_data, strategy='avalanche'):
    """ Runs a targeted execution configuration path based on explicit strategy parameters. """
    debts = financial_data['debts']
    net_income = financial_data['net_income']
    base_expenses = financial_data['base_expenses']
    seasonal_schedule = financial_data['seasonal_schedule']
    investment_rate = financial_data['investment_rate']
    inflation_rate = financial_data['inflation_rate']
    ef_months_target = financial_data['ef_months_target']
    
    active_debts = []
    for d in debts:
        active_debts.append({
            'name': d['name'],
            'balance': float(d['balance']),
            'rate': float(d['interest_rate']) / 100.0,
            'min_payment': float(d['minimum_payment']),
            'original_min': float(d['minimum_payment'])
        })

    if strategy == 'avalanche':
        active_debts.sort(key=lambda x: x['rate'], reverse=True)
    else:
        active_debts.sort(key=lambda x: x['balance'])

    months = 0
    schedule = []
    cumulative_investments = 0.0
    emergency_fund = financial_data['current_ef_savings']
    current_expenses = base_expenses
    total_interest_paid = 0.0

    while months < 600:
        months += 1
        
        if months > 1 and (months - 1) % 12 == 0:
            current_expenses *= (1.0 + inflation_rate)

        dynamic_ef_target = current_expenses * ef_months_target
        monthly_disposable_pool = net_income - current_expenses
        variable_injection = seasonal_schedule.get(months, 0.0)
        
        if cumulative_investments > 0:
            cumulative_investments += cumulative_investments * (investment_rate / 12.0)

        if not any(d['balance'] > 0 for d in active_debts):
            monthly_freed_cash = monthly_disposable_pool + variable_injection
            if monthly_freed_cash < 0: 
                monthly_freed_cash = 0.0
            
            if emergency_fund < dynamic_ef_target:
                deficit = dynamic_ef_target - emergency_fund
                to_ef = min(monthly_freed_cash, deficit)
                emergency_fund += to_ef
                monthly_freed_cash -= to_ef

            cumulative_investments += monthly_freed_cash
            
            schedule.append({
                "month": months,
                "payments": {d['name']: 0.0 for d in active_debts},
                "remaining_balance": 0.0,
                "emergency_fund": round(emergency_fund, 2),
                "monthly_savings": round(monthly_freed_cash, 2),
                "cumulative_savings": round(cumulative_investments, 2),
                "tracked_expenses": round(current_expenses, 2),
                "total_interest_paid": round(total_interest_paid, 2)
            })
            
            if len([s for s in schedule if s["remaining_balance"] == 0.0]) >= 24:
                break
            continue

        monthly_payments = {}
        total_min_required = sum(d['min_payment'] for d in active_debts if d['balance'] > 0)
        base_extra_pool = monthly_disposable_pool - total_min_required
        active_extra_fund = base_extra_pool + variable_injection

        for d in active_debts:
            if d['balance'] > 0:
                payment = min(d['min_payment'], d['balance'])
                monthly_payments[d['name']] = payment
                d['balance'] -= payment
            else:
                monthly_payments[d['name']] = 0.0

        current_month_savings = 0.0
        if emergency_fund < dynamic_ef_target and active_extra_fund > 0:
            ef_deficit = dynamic_ef_target - emergency_fund
            fill_amount = min(active_extra_fund, ef_deficit)
            emergency_fund += fill_amount
            active_extra_fund -= fill_amount

        if active_extra_fund > 0:
            for d in active_debts:
                if d['balance'] > 0:
                    extra_to_apply = min(active_extra_fund, d['balance'])
                    monthly_payments[d['name']] += extra_to_apply
                    d['balance'] -= extra_to_apply
                    active_extra_fund -= extra_to_apply
                    break

        if active_extra_fund > 0:
            cumulative_investments += active_extra_fund
            current_month_savings = active_extra_fund

        total_remaining_balance = 0
        for d in active_debts:
            if d['balance'] > 0:
                interest_charge = d['balance'] * (d['rate'] / 12.0)
                total_interest_paid += interest_charge
                d['balance'] += interest_charge
                total_remaining_balance += d['balance']

        schedule.append({
            "month": months,
            "payments": monthly_payments.copy(),
            "remaining_balance": round(total_remaining_balance, 2),
            "emergency_fund": round(emergency_fund, 2),
            "monthly_savings": round(current_month_savings, 2),
            "cumulative_savings": round(cumulative_investments, 2),
            "tracked_expenses": round(current_expenses, 2),
            "total_interest_paid": round(total_interest_paid, 2)
        })

    return schedule
