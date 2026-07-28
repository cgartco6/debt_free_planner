import math

def calculate_payoff_schedule(financial_data):
    """
    Simulates the debt payoff month-by-month. 
    When a debt is paid off, the minimum payment is rolled over to the next debt (snowball/avalanche).
    """
    debts = financial_data['debts']
    strategy = financial_data['strategy']
    disposable_income = financial_data['disposable_income']
    total_min_payments = financial_data['total_min_payments']

    # Separate balances, minimums, and rates
    active_debts = []
    for d in debts:
        active_debts.append({
            'name': d['name'],
            'balance': float(d['balance']),
            'rate': float(d['interest_rate']) / 100.0,
            'min_payment': float(d['minimum_payment'])
        })

    # Sort debts based on chosen strategy
    if strategy == 'avalanche':
        active_debts.sort(key=lambda x: x['rate'], reverse=True)
    else:  # 'snowball'
        active_debts.sort(key=lambda x: x['balance'])

    months = 0
    schedule = []
    
    # Calculate amount available to aggressively pay off the focused debt
    extra_payment_fund = disposable_income - total_min_payments

    while any(d['balance'] > 0 for d in active_debts):
        months += 1
        
        if months > 1200:  # 100-year safety break
            break

        # Distribute monthly payments
        monthly_payments = {}
        amount_available_for_extra = extra_payment_fund

        # 1. Pay all minimums or remaining balances if they are lower
        for d in active_debts:
            if d['balance'] > 0:
                payment = min(d['min_payment'], d['balance'])
                monthly_payments[d['name']] = payment
                d['balance'] -= payment
            else:
                monthly_payments[d['name']] = 0.0

        # 2. Add extra fund to the top priority debt
        for d in active_debts:
            if d['balance'] > 0:
                extra_to_apply = min(amount_available_for_extra, d['balance'])
                monthly_payments[d['name']] += extra_to_apply
                d['balance'] -= extra_to_apply
                break # Apply all extra to this debt

        # 3. Add monthly interest
        total_remaining_balance = 0
        for d in active_debts:
            if d['balance'] > 0:
                d['balance'] += d['balance'] * (d['rate'] / 12.0)
                total_remaining_balance += d['balance']

        # 4. Check if a debt is paid off and roll over the payment
        for d in active_debts:
            if d['balance'] <= 0.001 and d['balance'] > 0:
                d['balance'] = 0.0
                # Roll over the minimum payment to the extra fund
                extra_payment_fund += d['min_payment']
                d['min_payment'] = 0.0

        # 5. Record the month's status
        schedule.append({
            "month": months,
            "payments": monthly_payments.copy(),
            "remaining_balance": round(total_remaining_balance, 2)
        })

        if total_remaining_balance <= 0:
            break

    return schedule, months, extra_payment_fund
