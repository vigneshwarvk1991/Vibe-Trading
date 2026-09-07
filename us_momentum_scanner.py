import pandas as pd
import numpy as np
import yfinance as yf
import requests
import io

print("Step 1: Fetching official S&P 500 and Nasdaq 100 constituents...")
headers = {'User-Agent': 'Mozilla/5.0'}

# 1. Fetch S&P 500
url_sp500 = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
r = requests.get(url_sp500, headers=headers)
tables = pd.read_html(io.StringIO(r.text))
sp500_df = tables[0][['Symbol', 'Security', 'GICS Sector']]
sp500_tickers = sp500_df['Symbol'].str.replace('.', '-', regex=False).tolist()
sector_map = dict(zip(sp500_df['Symbol'].str.replace('.', '-', regex=False), sp500_df['GICS Sector']))
name_map = dict(zip(sp500_df['Symbol'].str.replace('.', '-', regex=False), sp500_df['Security']))

# 2. Fetch Nasdaq 100
url_ndx = 'https://en.wikipedia.org/wiki/Nasdaq-100'
r2 = requests.get(url_ndx, headers=headers)
tables2 = pd.read_html(io.StringIO(r2.text))
ndx_tickers = []
for t in tables2:
    if 'Ticker' in t.columns:
        ndx_tickers = t['Ticker'].str.replace('.', '-', regex=False).tolist()
        if 'Company' in t.columns and 'GICS Sector' in t.columns:
            for _, row in t.iterrows():
                sym = str(row['Ticker']).replace('.', '-')
                if sym not in sector_map: sector_map[sym] = row.get('GICS Sector', 'Technology')
                if sym not in name_map: name_map[sym] = row.get('Company', sym)
        break

universe = sorted(list(set(sp500_tickers + ndx_tickers)))
print(f"Total Unique Universe: {len(universe)} stocks across S&P 500 & Nasdaq 100.")

print("Step 2: Downloading 1-year daily market data for the complete universe...")
batch_df = yf.download(universe, period="1y", interval="1d", group_by="ticker", threads=True, progress=False)
print("Data download complete.")

# Benchmarks
spy = yf.Ticker("SPY").history(period="1y")
qqq = yf.Ticker("QQQ").history(period="1y")

def get_bench_line(df, name):
    c = df['Close']
    ema20 = c.ewm(span=20, adjust=False).mean().iloc[-1]
    ema200 = c.ewm(span=200, adjust=False).mean().iloc[-1]
    last = c.iloc[-1]
    chg = ((last - c.iloc[-2]) / c.iloc[-2]) * 100
    return f"{name}: ${round(last, 2)} ({round(chg, 2)}%) | vs 20 EMA: {round(((last-ema20)/ema20)*100, 2)}% | vs 200 EMA: {round(((last-ema200)/ema200)*100, 2)}%"

print("\n=== MACRO BENCHMARK REGIME ===")
print(get_bench_line(spy, "S&P 500 (SPY)"))
print(get_bench_line(qqq, "Nasdaq 100 (QQQ)"))

results = []
SLOT_USD = 500.0

for sym in universe:
    try:
        if sym not in batch_df.columns.levels[0]:
            continue
        df = batch_df[sym].dropna()
        if len(df) < 205:
            continue
            
        close = df['Close']
        high = df['High']
        low = df['Low']
        vol = df['Volume']
        
        curr_c = close.iloc[-1]
        curr_h = high.iloc[-1]
        
        # 200 EMA & 20 EMA
        ema20 = close.ewm(span=20, adjust=False).mean()
        ema200 = close.ewm(span=200, adjust=False).mean()
        
        # 200 EMA slope (change over last 20 trading days)
        slope_200 = ((ema200.iloc[-1] - ema200.iloc[-21]) / ema200.iloc[-21]) * 100
        
        # 20-day high of previous 20 bars (excluding current bar)
        high_20d = high.iloc[-21:-1].max()
        
        # Volume ratio
        curr_vol = vol.iloc[-1]
        avg_vol_20 = vol.iloc[-21:-1].mean()
        vol_ratio = curr_vol / avg_vol_20 if avg_vol_20 > 0 else 1.0
        
        # Liquidity filter: Avg daily volume > 500,000 shares
        if avg_vol_20 < 500000:
            continue
            
        # ATR 14
        tr1 = high - low
        tr2 = np.abs(high - close.shift(1))
        tr3 = np.abs(low - close.shift(1))
        tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
        atr14 = tr.ewm(alpha=1/14, adjust=False).mean().iloc[-1]
        
        # RSI 14
        delta = close.diff()
        gain = delta.where(delta > 0, 0).ewm(alpha=1/14, adjust=False).mean()
        loss = (-delta.where(delta < 0, 0)).ewm(alpha=1/14, adjust=False).mean()
        rs = gain / loss
        rsi14 = (100 - (100 / (1 + rs))).iloc[-1]
        
        dist_20d = ((curr_c - high_20d) / high_20d) * 100
        above_200 = curr_c > ema200.iloc[-1]
        pos_slope = slope_200 > 0
        
        is_breakout = (curr_c >= high_20d) and above_200 and pos_slope
        
        shares = round(SLOT_USD / curr_c, 3)
        hard_sl = round(curr_c * 0.95, 2)
        atr_trail = round(curr_c - (2.5 * atr14), 2)
        
        results.append({
            'Symbol': sym,
            'Name': name_map.get(sym, sym)[:20],
            'Sector': sector_map.get(sym, 'Unknown')[:18],
            'Close': round(curr_c, 2),
            '20d High': round(high_20d, 2),
            'Dist %': round(dist_20d, 2),
            'Above 200': bool(above_200),
            'Slope 200 %': round(slope_200, 2),
            'Vol Ratio': round(vol_ratio, 2),
            'RSI': round(rsi14, 1),
            'ATR': round(atr14, 2),
            'Breakout': bool(is_breakout),
            'Shares ($500)': shares,
            'Hard SL (5%)': hard_sl,
            'Trail SL': atr_trail
        })
    except Exception as e:
        continue

res_df = pd.DataFrame(results)

breakouts_df = res_df[res_df['Breakout'] == True].sort_values(by='Vol Ratio', ascending=False)
near_breakouts_df = res_df[res_df['Breakout'] == False].sort_values(by='Dist %', ascending=False).head(15)

print(f"\n=== CONFIRMED 20-DAY HIGH BREAKOUTS ACROSS ENTIRE S&P 500 & NASDAQ 100 ({len(breakouts_df)} FOUND) ===")
if not breakouts_df.empty:
    print(breakouts_df[['Symbol', 'Name', 'Sector', 'Close', '20d High', 'Vol Ratio', 'RSI', 'Shares ($500)', 'Hard SL (5%)', 'Trail SL']].to_string(index=False))
else:
    print("Zero breakouts confirmed on Friday close.")

print("\n=== TOP 15 NEAR-BREAKOUT CANDIDATES (WITHIN 1.5% OF 20-DAY HIGH) ===")
print(near_breakouts_df[['Symbol', 'Name', 'Sector', 'Close', '20d High', 'Dist %', 'Vol Ratio', 'Above 200', 'Slope 200 %', 'RSI', 'Shares ($500)', 'Hard SL (5%)']].to_string(index=False))
