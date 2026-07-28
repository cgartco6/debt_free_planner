def calculate_payoff_schedule(financial_data):
    """
    Simulates timeline while applying step-by-step rollover velocity 
    integrated with real-time seasonal variations.
    """
    debts = financial_data['debts']
    strategy = financial_data['strategy']
    base_disposable = financial_data['base_disposable_income']
    total_min_payments = financial_data['total_min_payments']
    seasonal_schedule = financial_data['seasonal_schedule']

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
    
    # Extra base fund left over after satisfying standard baseline obligations
    base_extra_pool = base_disposable - total_min_payments
    cumulative_savings = 0.0

    while months < 600: # 50-year cap
        months += 1
        
        # Calculate dynamic seasonal/variable injection for this specific month
        variable_injection = seasonal_schedule.get(months, 0.0)
        
        # Check if total baseline structural debt is already eliminated
        if not any(d['balance'] > 0 for d in active_debts):
            # All payments shift directly to high-yield tracking accumulation
            monthly_freed_cash = base_disposable + variable_injection
            cumulative_savings += monthly_freed_cash
            
            schedule.append({
                "month": months,
                "payments": {d['name']: 0.0 for d in active_debts},
                "remaining_balance": 0.0,
                "monthly_savings": monthly_freed_cash,
                "cumulative_savings": round(cumulative_savings, 2)
            })
            
            # Simulate 12 solid months of pure visual savings growth post-debt
            if len([s for s in schedule if s["remaining_balance"] == 0.0]) >= 12:
                break
            continue

        # Process Active Debt Math Loop
        monthly_payments = {}
        
        # Dynamic active rollover calculations
        current_freed_minimums = sum(d['original_min'] for d in active_debts if d['balance'] <= 0)
        active_extra_fund = base_extra_pool + current_freed_minimums + variable_injection

        # 1. Distribute Base Obligations
        for d in active_debts:
            if d['balance'] > 0:
                payment = min(d['min_payment'], d['balance'])
                monthly_payments[d['name']] = payment
                d['balance'] -= payment
            else:
                monthly_payments[d['name']] = 0.0

        # 2. Crash-inject the variable-amplified snowball fund into target
        for d in active_debts:
            if d['balance'] > 0:
                extra_to_apply = min(active_extra_fund, d['balance'])
                monthly_payments[d['name']] += extra_to_apply
                d['balance'] -= extra_to_apply
                active_extra_fund -= extra_to_apply
                if active_extra_fund <= 0:
                    break

        # If extra cash outpaces remaining monthly debt, redirect rest to savings
        if active_extra_fund > 0:
            cumulative_savings += active_extra_fund
            current_month_savings = active_extra_fund
        else:
            current_month_savings = 0.0

        # 3. Monthly Compound Accruals
        total_remaining_balance = 0
        for d in active_debts:
            if d['balance'] > 0:
                d['balance'] += d['balance'] * (d['rate'] / 12.0)
                total_remaining_balance += d['balance']

        schedule.append({
            "month": months,
            "payments": monthly_payments.copy(),
            "remaining_balance": round(total_remaining_balance, 2),
            "monthly_savings": round(current_month_savings, 2),
            "cumulative_savings": round(cumulative_savings, 2)
        })

    return schedule, months

