#!/usr/bin/env python3
"""
========================================================================================
DYNAMIC S&P 500 & NASDAQ 100 POSITIONAL MOMENTUM SCANNER (TRACK 1 US MOMENTUM)
========================================================================================
100% Dynamic Universe: Downloads all constituents of S&P 500 and Nasdaq 100 live from
Wikipedia tables. ZERO hardcoded stocks.

Quantitative Momentum Breakout Rules:
  1. Macro Trend Gate: Price > 200 EMA with positive 20-day slope (slope > 0%).
  2. 20-Day High Breakout: Close >= 20-day high of previous 20 bars (excluding current bar).
  3. Relative Strength Gate: 126-day (6-month) price return in Top 30% of universe (RS >= 70.0%).
  4. Volume Surge Gate: Traded volume >= 1.40x 20-day average daily volume.
  5. Liquidity Gate: 20-day Average Daily Volume >= 1,000,000 shares (or turnover >= $50M).

Position Sizing & Risk Management:
  - Capital: $2,500 USD across 5 slots = $500 per slot.
  - Initial Hard Stop: Exactly 5.0% below entry price (placed as IBKR GTC stop).
  - Max Risk per Trade: Exactly $25.00 USD (1.0% of portfolio equity).
  - Trailing Stop: 2.5x ATR(14) from highest peak close since entry.
  - Google Sheet Sync: Pushes confirmed buy candidates to tab 'To Buy - US' via AppSheet Webhook.
========================================================================================
"""

import sys
import os
import io
import json
import time
import argparse
import urllib.request
import warnings
from datetime import datetime
import pandas as pd
import numpy as np
import requests
import yfinance as yf

warnings.filterwarnings("ignore")
pd.set_option("display.max_columns", None)
pd.set_option("display.width", 240)
pd.set_option("display.float_format", lambda x: f"{x:.2f}")

try:
    from dotenv import load_dotenv
    load_dotenv()
    agent_env = os.path.join(os.path.dirname(os.path.abspath(__file__)), "agent", ".env")
    if os.path.exists(agent_env):
        load_dotenv(agent_env)
except ImportError:
    pass

WEBHOOK_URL = os.environ.get("GOOGLE_SHEETS_WEBHOOK_URL", "")
SLOT_USD = 500.0
MAX_RISK_USD = 25.0


def fetch_us_universe():
    headers = {"User-Agent": "Mozilla/5.0"}
    sector_map = {}
    name_map = {}

    # 1. Fetch S&P 500
    url_sp500 = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
    r = requests.get(url_sp500, headers=headers, timeout=12)
    tables = pd.read_html(io.StringIO(r.text))
    sp500_df = tables[0][["Symbol", "Security", "GICS Sector"]]
    sp500_tickers = sp500_df["Symbol"].str.replace(".", "-", regex=False).tolist()
    sector_map = dict(zip(sp500_df["Symbol"].str.replace(".", "-", regex=False), sp500_df["GICS Sector"]))
    name_map = dict(zip(sp500_df["Symbol"].str.replace(".", "-", regex=False), sp500_df["Security"]))

    # 2. Fetch Nasdaq 100
    url_ndx = "https://en.wikipedia.org/wiki/Nasdaq-100"
    r2 = requests.get(url_ndx, headers=headers, timeout=12)
    tables2 = pd.read_html(io.StringIO(r2.text))
    ndx_tickers = []
    for t in tables2:
        if "Ticker" in t.columns:
            ndx_tickers = t["Ticker"].str.replace(".", "-", regex=False).tolist()
            if "Company" in t.columns and "GICS Sector" in t.columns:
                for _, row in t.iterrows():
                    sym = str(row["Ticker"]).replace(".", "-")
                    if sym not in sector_map:
                        sector_map[sym] = row.get("GICS Sector", "Technology")
                    if sym not in name_map:
                        name_map[sym] = row.get("Company", sym)
            break

    universe = sorted(list(set(sp500_tickers + ndx_tickers)))
    return universe, sector_map, name_map


def compute_us_rs_percentiles(batch_df, universe):
    returns_6m = {}
    for sym in universe:
        try:
            if sym not in batch_df.columns.levels[0]:
                continue
            df_sym = batch_df[sym]["Close"].dropna()
            if len(df_sym) >= 126:
                ret = (df_sym.iloc[-1] - df_sym.iloc[-126]) / df_sym.iloc[-126] * 100.0
                returns_6m[sym] = ret
        except Exception:
            continue

    if not returns_6m:
        return {}

    s = pd.Series(returns_6m)
    rs_percentiles = s.rank(pct=True) * 100.0
    return rs_percentiles.to_dict()


def run_us_momentum_scanner(sync_to_sheets=False, top_n=10):
    print("\n" + "=" * 125)
    print("  DYNAMIC S&P 500 & NASDAQ 100 POSITIONAL MOMENTUM SCANNER (US EQUITIES)")
    print(f"  System Timestamp: {datetime.now():%Y-%m-%d %H:%M:%S EST} | Slot: ${SLOT_USD:,.2f} | Max Risk: ${MAX_RISK_USD:,.2f} (1%)")
    print("=" * 125 + "\n")

    print("Step 1: Fetching official S&P 500 and Nasdaq 100 constituents...")
    universe, sector_map, name_map = fetch_us_universe()
    print(f"  [OK] Total Unique Universe: {len(universe)} stocks across S&P 500 & Nasdaq 100.")

    print(f"\nStep 2: Downloading 1-year daily market data for {len(universe)} stocks...")
    batch_df = yf.download(universe, period="1y", interval="1d", group_by="ticker", threads=True, progress=False)
    print("  [OK] Data download complete.")

    print("\nStep 3: Calculating 6-month cross-sectional Relative Strength (RS) percentiles across universe...")
    rs_map = compute_us_rs_percentiles(batch_df, universe)
    print(f"  [OK] Relative Strength percentiles computed for {len(rs_map)} stocks.")

    # Macro Benchmark Regime
    try:
        spy = yf.Ticker("SPY").history(period="1y")
        qqq = yf.Ticker("QQQ").history(period="1y")

        def get_bench_line(df, name):
            c = df["Close"]
            ema20 = c.ewm(span=20, adjust=False).mean().iloc[-1]
            ema200 = c.ewm(span=200, adjust=False).mean().iloc[-1]
            last = c.iloc[-1]
            chg = ((last - c.iloc[-2]) / c.iloc[-2]) * 100.0
            return f"{name}: ${last:.2f} ({chg:+.2f}%) | vs 20 EMA: {((last-ema20)/ema20)*100:+.2f}% | vs 200 EMA: {((last-ema200)/ema200)*100:+.2f}%"

        print("\n=== MACRO BENCHMARK REGIME ===")
        print("  " + get_bench_line(spy, "S&P 500 (SPY)"))
        print("  " + get_bench_line(qqq, "Nasdaq 100 (QQQ)"))
    except Exception:
        pass

    results = []
    print("\nStep 4: Scanning for 20-day high breakouts, volume surge (>=1.4x), and RS (>=70%)...")

    for sym in universe:
        try:
            if sym not in batch_df.columns.levels[0]:
                continue
            df = batch_df[sym].dropna()
            if len(df) < 205:
                continue

            close = df["Close"]
            high = df["High"]
            low = df["Low"]
            vol = df["Volume"]

            curr_c = float(close.iloc[-1])
            curr_v = float(vol.iloc[-1])

            # 1. 200 EMA & 20-day slope
            ema200 = close.ewm(span=200, adjust=False).mean()
            slope_200 = float(((ema200.iloc[-1] - ema200.iloc[-21]) / ema200.iloc[-21]) * 100.0)
            above_200 = curr_c > float(ema200.iloc[-1])
            pos_slope = slope_200 > 0.0

            # 2. 20-Day High of PREVIOUS 20 bars (excluding current bar)
            high_20d = float(high.iloc[-21:-1].max())

            # 3. Volume Surge Ratio
            avg_vol_20 = float(vol.iloc[-21:-1].mean())
            vol_ratio = curr_v / avg_vol_20 if avg_vol_20 > 0 else 0.0

            # 4. Liquidity Gate: ADV >= 1,000,000 shares OR Dollar Turnover >= $50M
            turnover_m = (avg_vol_20 * curr_c) / 1e6
            liq_pass = (avg_vol_20 >= 1000000) or (turnover_m >= 50.0)

            # 5. Relative Strength Percentile
            rs_pct = float(rs_map.get(sym, 50.0))

            # 6. ATR(14)
            tr1 = high - low
            tr2 = np.abs(high - close.shift(1))
            tr3 = np.abs(low - close.shift(1))
            tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
            atr14 = float(tr.ewm(alpha=1/14, adjust=False).mean().iloc[-1])

            dist_20d = float(((curr_c - high_20d) / high_20d) * 100.0)

            # STRICT BREAKOUT DEFINITION (All 5 Gates Must Pass)
            is_breakout = (
                (curr_c >= high_20d) and
                above_200 and
                pos_slope and
                (vol_ratio >= 1.40) and
                (rs_pct >= 70.0) and
                liq_pass
            )

            # Near-Breakout definition
            is_near = (
                (-2.0 <= dist_20d <= 0.5) and
                above_200 and
                pos_slope and
                (rs_pct >= 65.0) and
                liq_pass
            )

            shares = round(SLOT_USD / curr_c, 3)
            hard_sl = round(curr_c * 0.95, 2)
            atr_trail = round(curr_c - (2.5 * atr14), 2)
            risk = round((curr_c - hard_sl) * shares, 2)

            results.append({
                "Symbol": sym,
                "Name": name_map.get(sym, sym)[:22],
                "Sector": sector_map.get(sym, "Unknown")[:18],
                "Close": round(curr_c, 2),
                "20d_High": round(high_20d, 2),
                "Dist_%": round(dist_20d, 2),
                "Vol_Ratio": round(vol_ratio, 2),
                "RS_Pct": round(rs_pct, 1),
                "Slope_200_%": round(slope_200, 2),
                "Turnover_$M": round(turnover_m, 1),
                "ATR14": round(atr14, 2),
                "Breakout": bool(is_breakout),
                "Near_Breakout": bool(is_near),
                "Shares": shares,
                "Hard_SL_5%": hard_sl,
                "Trail_SL": atr_trail,
                "Risk_$": risk
            })
        except Exception:
            continue

    df_res = pd.DataFrame(results)
    if df_res.empty:
        print("  [Warning] No valid market data processed.")
        return df_res

    breakouts_df = df_res[df_res["Breakout"] == True].sort_values(by=["RS_Pct", "Vol_Ratio"], ascending=[False, False]).reset_index(drop=True)
    breakouts_df.index += 1

    near_df = df_res[(df_res["Breakout"] == False) & (df_res["Near_Breakout"] == True)].sort_values(by=["Dist_%", "RS_Pct"], ascending=[False, False]).head(15).reset_index(drop=True)
    near_df.index += 1

    print("=" * 125)
    print(f"  CONFIRMED 20-DAY HIGH MOMENTUM BREAKOUTS ({len(breakouts_df)} FOUND)")
    print("  Filters: Close >= 20d High | Price > 200 EMA | Slope > 0 | Vol Ratio >= 1.40x | RS >= 70% | ADV >= 1M / $50M")
    print("=" * 125)
    show_cols = ["Symbol", "Name", "Sector", "Close", "20d_High", "Vol_Ratio", "RS_Pct", "Shares", "Hard_SL_5%", "Trail_SL", "Risk_$"]
    if not breakouts_df.empty:
        print(breakouts_df[show_cols].to_string())
    else:
        print("  Zero confirmed breakouts today meeting all strict institutional gates. Capital 100% protected in cash.")

    print("\n" + "=" * 125)
    print(f"  TOP WATCHLIST: NEAR-BREAKOUT CANDIDATES (WITHIN 2.0% OF 20-DAY HIGH, RS >= 65%)")
    print("=" * 125)
    watch_cols = ["Symbol", "Name", "Sector", "Close", "20d_High", "Dist_%", "Vol_Ratio", "RS_Pct", "Turnover_$M", "Hard_SL_5%"]
    if not near_df.empty:
        print(near_df[watch_cols].to_string())

    csv_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "us_momentum_results.csv")
    df_res.to_csv(csv_path, index=False)
    print(f"\n[OK] Full scan results saved to: {csv_path}")

    if sync_to_sheets and not breakouts_df.empty:
        print("\n[OK] Pushing confirmed buy orders to Google Sheet 'To Buy - US' tab via Webhook...")
        today_str = datetime.now().strftime("%d-%b-%Y")
        sheet_rows = []
        for _, r in breakouts_df.head(top_n).iterrows():
            sheet_rows.append([
                today_str,
                r["Symbol"],
                r["Sector"],
                "BUY",
                float(r["Shares"]),
                float(r["Close"]),
                500.0,
                float(r["Hard_SL_5%"]),
                float(r["Trail_SL"]),
                float(r["Risk_$"]),
                "CONFIRMED BREAKOUT"
            ])
        payload = {"tab": "To Buy - US", "rows": sheet_rows}
        try:
            req = urllib.request.Request(
                WEBHOOK_URL,
                data=json.dumps(payload).encode("utf-8"),
                headers={"Content-Type": "application/json"}
            )
            with urllib.request.urlopen(req, timeout=15) as resp:
                print(f"  [OK] Google Sheet Sync Success: {resp.read().decode('utf-8')[:150]}")
        except Exception as e:
            print(f"  [Notice] Google Sheet Sync Notice: {e}")

    return breakouts_df


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Dynamic S&P 500 & Nasdaq 100 Momentum Scanner")
    parser.add_argument("--sync-sheet", action="store_true", help="Push confirmed breakouts to Google Sheet 'To Buy - US' tab")
    parser.add_argument("--top", type=int, default=10, help="Max candidates to sync")
    args = parser.parse_args()

    run_us_momentum_scanner(sync_to_sheets=args.sync_sheet, top_n=args.top)
