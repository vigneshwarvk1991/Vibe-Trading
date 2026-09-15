import yfinance as yf

# Current IBKR holdings (from live positions pull):
holdings = {
    'VWRA': {'units': 81.9183, 'avg_cost': 178.93, 'ticker': 'VWRA.L'},
    'WSML': {'units': 291.9701, 'avg_cost': 10.14, 'ticker': 'WSML.L'},
    'USSC': {'units': 17.9816, 'avg_cost': 90.48, 'ticker': 'USSC.L'}
}

cash_available = 8215.60

prices = {}
for name, data in holdings.items():
    try:
        t = yf.Ticker(data['ticker'])
        hist = t.history(period='5d')
        if not hist.empty:
            prices[name] = float(hist['Close'].iloc[-1])
        else:
            prices[name] = data['avg_cost']
    except Exception:
        prices[name] = data['avg_cost']

# Print current status
print("=== CURRENT ETF HOLDINGS IN IBKR ===")
current_val = {}
total_etf_val = 0.0
for name, data in holdings.items():
    p = prices[name]
    val = data['units'] * p
    current_val[name] = val
    total_etf_val += val
    print(f"{name:6}: {data['units']:<10.4f} units @ ${p:<8.2f} = ${val:<10.2f}")

print(f"\nTotal Current ETF Value: ${total_etf_val:,.2f}")
print(f"Current Available Cash:  ${cash_available:,.2f}")
for name in holdings:
    w = current_val[name] / total_etf_val * 100
    print(f"  {name:6} current weight: {w:.2f}%")

target_weights = {
    'VWRA': 0.60,
    'WSML': 0.20,
    'USSC': 0.20
}

# -------------------------------------------------------------
# Case 1: Deploying the current Cash ($8,215.60) into ETFs
# Total new ETF Capital = total_etf_val + cash_available
# -------------------------------------------------------------
new_total_1 = total_etf_val + cash_available
print(f"\n=== SCENARIO 1: DEPLOYING CURRENT CASH (${cash_available:,.2f}) ===")
print(f"New Target ETF Portfolio Value: ${new_total_1:,.2f}")

allocations_1 = {}
for name in target_weights:
    target_val = new_total_1 * target_weights[name]
    diff = target_val - current_val[name]
    allocations_1[name] = {
        'target_val': target_val,
        'current_val': current_val[name],
        'to_invest': max(diff, 0.0),
        'diff': diff
    }

# Normalize to invest exactly cash_available if purely buying
pure_buys = {k: max(v['diff'], 0) for k, v in allocations_1.items()}
sum_pure_buys = sum(pure_buys.values())

print(f"\nExact Target vs Current (Target 60/20/20 of ${new_total_1:,.2f}):")
for name in target_weights:
    info = allocations_1[name]
    target_v = info['target_val']
    cur_v = info['current_val']
    diff = info['diff']
    p = prices[name]
    shares = diff / p if diff > 0 else 0
    print(f"{name:6} | Target: ${target_v:<9.2f} ({(target_weights[name]*100):.0f}%) | Current: ${cur_v:<9.2f} | Need to Buy: ${diff:<9.2f} (~{shares:<6.2f} units)")

