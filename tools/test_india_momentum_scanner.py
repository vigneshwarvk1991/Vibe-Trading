#!/usr/bin/env python3
import pytest
import pandas as pd
import numpy as np
from india_momentum_scanner import fetch_nifty500_universe, compute_rs_percentiles, SLOT_CAPITAL, MAX_RISK

def test_fetch_nifty500_universe():
    tickers, meta = fetch_nifty500_universe()
    assert len(tickers) >= 400
    assert all(t.endswith(".NS") for t in tickers[:20])
    assert len(meta) >= 400

def test_compute_rs_percentiles():
    dates = pd.date_range("2025-01-01", periods=150, freq="D")
    data = {
        ("STOCK_A.NS", "Close"): np.linspace(100, 200, 150),  # +100%
        ("STOCK_B.NS", "Close"): np.linspace(100, 150, 150),  # +50%
        ("STOCK_C.NS", "Close"): np.linspace(100, 100, 150),  # 0%
        ("STOCK_D.NS", "Close"): np.linspace(100, 50, 150),   # -50%
    }
    df = pd.DataFrame(data, index=dates)
    df.columns = pd.MultiIndex.from_tuples(df.columns)
    
    rs_map = compute_rs_percentiles(df, ["STOCK_A.NS", "STOCK_B.NS", "STOCK_C.NS", "STOCK_D.NS"])
    assert len(rs_map) == 4
    assert rs_map["STOCK_A.NS"] == 100.0
    assert rs_map["STOCK_B.NS"] == 75.0
    assert rs_map["STOCK_C.NS"] == 50.0
    assert rs_map["STOCK_D.NS"] == 25.0

def test_position_sizing_and_risk():
    curr_c = 1000.0
    shares = max(1, int(SLOT_CAPITAL / curr_c))
    capital = shares * curr_c
    hard_sl = round(curr_c * 0.95, 2)
    risk = round((curr_c - hard_sl) * shares, 2)

    assert shares == 50
    assert capital == 50000.0
    assert hard_sl == 950.0
    assert risk == 2500.0
    assert risk == MAX_RISK
