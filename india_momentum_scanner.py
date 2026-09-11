#!/usr/bin/env python3
"""
========================================================================================
DYNAMIC LIQUID NIFTY 500 POSITIONAL MOMENTUM SCANNER (TRACK 1 INDIA MOMENTUM)
========================================================================================
100% Dynamic Universe: Downloads all ~501 constituents of the Nifty 500 index live from
NSE Archives with local universe fallback. ZERO hardcoded stocks.

Quantitative Momentum Breakout Rules:
  1. Macro Trend Gate: Price > 200 EMA with positive 20-day slope (slope > 0%).
  2. 20-Day High Breakout: Close >= 20-day high of previous 20 bars (excluding current bar).
  3. Relative Strength Gate: 126-day (6-month) price return in Top 30% of universe (RS >= 70.0%).
  4. Volume Surge Gate: Traded volume >= 1.40x 20-day average daily volume.
  5. Liquidity Gates: 20-day ADV >= 300,000 shares AND 20-day Turnover >= Rs 3.0 Crore.

Position Sizing & Risk Management:
  - Capital: Rs 2,50,000 across 5 slots = Rs 50,000 per slot.
  - Initial Hard Stop: Exactly 5.0% below entry price (placed as Zerodha GTT).
  - Max Risk per Trade: Exactly Rs 2,500 (1.0% of portfolio equity).
  - Trailing Stop: 2.5x ATR(14) from highest peak close since entry.
  - Google Sheet Sync: Pushes confirmed buy candidates to tab 'To buy' via AppSheet Webhook.
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
SLOT_CAPITAL = 50000.0
MAX_RISK = 2500.0


def fetch_nifty500_universe():
    url = "https://archives.nseindia.com/content/indices/ind_nifty500list.csv"
    headers = {"User-Agent": "Mozilla/5.0"}
    tickers = []
    meta_map = {}

    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=12) as resp:
            df = pd.read_csv(io.StringIO(resp.read().decode("utf-8")))
            for _, row in df.iterrows():
                raw_sym = str(row["Symbol"]).strip().replace("&", "_")
                sym = f"{raw_sym}.NS"
                tickers.append(sym)
                meta_map[sym] = {
                    "symbol": sym,
                    "name": str(row.get("Company Name", raw_sym)),
                    "industry": str(row.get("Industry", "General"))
                }
        print(f"  [OK] Live official Nifty 500 constituents fetched: {len(tickers)} stocks.")
        return sorted(list(set(tickers))), meta_map
    except Exception as e:
        print(f"  [Notice] Live NSE fetch exception: {e}; using local universe fallback...")

    local_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "multibagger_full_universe.csv")
    if os.path.exists(local_path):
        df_local = pd.read_csv(local_path)
        for _, row in df_local.iterrows():
            sym = str(row["symbol"]).strip()
            if not sym.endswith(".NS"):
                sym = f"{sym}.NS"
            tickers.append(sym)
            meta_map[sym] = {
                "symbol": sym,
                "name": str(row.get("name", sym)),
                "industry": str(row.get("industry", str(row.get("sector", "General"))))
            }
        print(f"  [OK] Local universe fallback loaded: {len(tickers)} stocks.")
        return sorted(list(set(tickers))), meta_map

    raise RuntimeError("Unable to load Indian equity universe.")


def compute_rs_percentiles(batch_df, tickers):
    returns_6m = {}
    for sym in tickers:
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


def run_india_momentum_scanner(sync_to_sheets=False, top_n=10):
    print("\n" + "=" * 125)
    print("  DYNAMIC LIQUID NIFTY 500 POSITIONAL MOMENTUM SCANNER (NSE INDIA)")
    print(f"  System Timestamp: {datetime.now():%Y-%m-%d %H:%M:%S IST} | Slot: Rs {SLOT_CAPITAL:,.0f} | Max Risk: Rs {MAX_RISK:,.0f}")
    print("=" * 125 + "\n")

    print("Step 1: Fetching 100% dynamic universe constituents (Zero Hardcoded Stocks)...")
    tickers, meta_map = fetch_nifty500_universe()

    print(f"\nStep 2: Downloading 1-year daily market data for {len(tickers)} stocks...")
    batch_df = yf.download(tickers, period="1y", interval="1d", group_by="ticker", threads=True, progress=False)
    print("  [OK] Batch download complete.")

    print("\nStep 3: Calculating 6-month cross-sectional Relative Strength (RS) percentiles across universe...")
    rs_map = compute_rs_percentiles(batch_df, tickers)
    print(f"  [OK] Relative Strength percentiles computed for {len(rs_map)} stocks.")

    results = []
    print("\nStep 4: Scanning for 20-day high breakouts, volume surge (>=1.4x), and RS (>=70%)...")

    for sym in tickers:
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

            # 200 EMA & 20-day slope
            ema200 = close.ewm(span=200, adjust=False).mean()
            slope_200 = float(((ema200.iloc[-1] - ema200.iloc[-21]) / ema200.iloc[-21]) * 100.0)
            above_200 = curr_c > float(ema200.iloc[-1])
            pos_slope = slope_200 > 0.0

            # 20-Day High of PREVIOUS 20 bars (excluding current bar)
            high_20d = float(high.iloc[-21:-1].max())

            # Volume Surge Ratio
            avg_vol_20 = float(vol.iloc[-21:-1].mean())
            vol_ratio = curr_v / avg_vol_20 if avg_vol_20 > 0 else 0.0

            # Liquidity Gate: 20-day ADV >= 300k shares AND Turnover >= Rs 3.0 Cr
            turnover_cr = (avg_vol_20 * curr_c) / 1e7
            liq_pass = (avg_vol_20 >= 300000) and (turnover_cr >= 3.0)

            # Relative Strength Percentile
            rs_pct = float(rs_map.get(sym, 50.0))

            # ATR(14)
            tr1 = high - low
            tr2 = np.abs(high - close.shift(1))
            tr3 = np.abs(low - close.shift(1))
            tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
            atr14 = float(tr.ewm(alpha=1/14, adjust=False).mean().iloc[-1])

            dist_20d = float(((curr_c - high_20d) / high_20d) * 100.0)

            # Strict Breakout
            is_breakout = (
                (curr_c >= high_20d) and
                above_200 and
                pos_slope and
                (vol_ratio >= 1.40) and
                (rs_pct >= 70.0) and
                liq_pass
            )

            # Near Breakout
            is_near = (
                (-2.0 <= dist_20d <= 0.5) and
                above_200 and
                pos_slope and
                (rs_pct >= 65.0) and
                liq_pass
            )

            shares = max(1, int(SLOT_CAPITAL / curr_c))
            capital = round(shares * curr_c, 2)
            hard_sl = round(curr_c * 0.95, 2)
            atr_trail = round(curr_c - (2.5 * atr14), 2)
            risk = round((curr_c - hard_sl) * shares, 2)

            meta = meta_map.get(sym, {})
            results.append({
                "Symbol": sym,
                "Name": meta.get("name", sym)[:24],
                "Industry": meta.get("industry", "General")[:18],
                "Close": round(curr_c, 2),
                "20d_High": round(high_20d, 2),
                "Dist_%": round(dist_20d, 2),
                "Vol_Ratio": round(vol_ratio, 2),
                "RS_Pct": round(rs_pct, 1),
                "Slope_200_%": round(slope_200, 2),
                "Turnover_Cr": round(turnover_cr, 1),
                "ATR14": round(atr14, 2),
                "Breakout": bool(is_breakout),
                "Near_Breakout": bool(is_near),
                "Shares": shares,
                "Capital": capital,
                "Hard_SL_5%": hard_sl,
                "Trail_SL": atr_trail,
                "Risk_INR": risk
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
    print("  Filters: Close >= 20d High | Price > 200 EMA | Slope > 0 | Vol Ratio >= 1.40x | RS >= 70% | Turnover >= Rs 3Cr")
    print("=" * 125)
    show_cols = ["Symbol", "Name", "Industry", "Close", "20d_High", "Vol_Ratio", "RS_Pct", "Shares", "Capital", "Hard_SL_5%", "Trail_SL", "Risk_INR"]
    if not breakouts_df.empty:
        print(breakouts_df[show_cols].to_string())
    else:
        print("  Zero confirmed breakouts today meeting all strict institutional gates. Capital 100% protected in cash.")

    print("\n" + "=" * 125)
    print("  TOP WATCHLIST: NEAR-BREAKOUT CANDIDATES (WITHIN 2.0% OF 20-DAY HIGH, RS >= 65%)")
    print("=" * 125)
    watch_cols = ["Symbol", "Name", "Industry", "Close", "20d_High", "Dist_%", "Vol_Ratio", "RS_Pct", "Turnover_Cr", "Hard_SL_5%"]
    if not near_df.empty:
        print(near_df[watch_cols].to_string())

    csv_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "india_momentum_results.csv")
    df_res.to_csv(csv_path, index=False)
    print(f"\n[OK] Full scan results saved to: {csv_path}")

    if sync_to_sheets and not breakouts_df.empty:
        print("\n[OK] Pushing confirmed buy orders to Google Sheet 'To buy' tab via Webhook...")
        today_str = datetime.now().strftime("%d-%b-%Y")
        sheet_rows = []
        for _, r in breakouts_df.head(top_n).iterrows():
            sheet_rows.append([
                today_str,
                r["Symbol"],
                r["Industry"],
                "BUY",
                int(r["Shares"]),
                float(r["Close"]),
                float(r["Capital"]),
                float(r["Hard_SL_5%"]),
                float(r["Trail_SL"]),
                float(r["Risk_INR"]),
                "CONFIRMED BREAKOUT"
            ])
        payload = {"tab": "To buy", "rows": sheet_rows}
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
    parser = argparse.ArgumentParser(description="Dynamic Liquid Nifty 500 Momentum Scanner")
    parser.add_argument("--sync-sheet", action="store_true", help="Push confirmed breakouts to Google Sheet 'To buy' tab")
    parser.add_argument("--top", type=int, default=10, help="Max candidates to sync")
    args = parser.parse_args()

    run_india_momentum_scanner(sync_to_sheets=args.sync_sheet, top_n=args.top)
