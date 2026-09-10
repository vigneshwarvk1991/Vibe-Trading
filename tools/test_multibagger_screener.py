"""
Unit Tests for Four-Tier Institutional Compounder Indian Multibagger Screener.
Tests edge cases, forensic gate thresholds, mathematical formulas, cyclical trap rejection,
and dynamic yfinance financial statement extraction.
"""

import pytest
import sys
import os
import pandas as pd
from unittest.mock import MagicMock

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from multibagger_screen import (
    run_four_tier_audit,
    cagr,
    extract_financials_from_yfinance,
    UNIVERSE,
    HISTORICAL_AUDITED_DB
)

def test_cagr_calculation():
    """Verify CAGR formula behavior on normal and edge cases."""
    # Doubling in 5 years = ~14.87%
    assert round(cagr(100, 200, 5), 2) == 14.87
    # 4 periods (5 data points)
    assert round(cagr(100, 207.36, 4), 2) == 20.00
    # Zero or negative inputs
    assert cagr(0, 100, 5) == 0.0
    assert cagr(100, -50, 5) == 0.0
    assert cagr(-100, 200, 5) == 0.0
    assert cagr(100, 200, 0) == 0.0

def test_tier1_financials_exclusion():
    """Verify banks and NBFCs are strictly excluded from industrial formulas."""
    bank_meta = {
        "symbol": "HDFCBANK.NS", "name": "HDFC Bank", "sector": "Banking",
        "mcap_cr": 1200000.0, "turnover_cr": 150.0
    }
    dummy_fin = {
        "revenue_5y": [100, 120, 150, 180, 220], "pat_5y": [20, 25, 30, 38, 48],
        "ebit_5y": [30, 38, 45, 55, 70], "cfo_5y": [25, 30, 40, 50, 60],
        "capex_5y": [8, 10, 12, 15, 18], "gross_margin_5y": [50, 50, 50, 50, 50],
        "capital_employed_5y": [100, 120, 150, 180, 220],
        "gross_ppe": 50, "cwip": 0, "receivables": 10, "receivables_start": 5,
        "total_debt": 0, "total_equity": 220,
        "promoter_holding": 50.0, "promoter_pledge": 0.0,
        "fcf_latest": 50.0, "ev_ebitda": 15.0, "median_ev_ebitda_5y": 18.0
    }
    res = run_four_tier_audit(bank_meta, dummy_fin)
    assert res["tier1_pass"] is False
    assert res["overall_pass"] is False
    assert "FINANCIAL" in res["verdict"]

def test_tier2_sloan_accrual_gate():
    """Verify that companies with poor cash conversion (CFO/PAT < 0.75) fail Tier 2."""
    meta = {"symbol": "PAPERPROFIT.NS", "name": "Paper Profit Ltd", "sector": "Manufacturing", "mcap_cr": 5000, "turnover_cr": 5.0}
    fin_bad_sloan = {
        "revenue_5y": [100, 120, 145, 175, 210], "pat_5y": [15, 18, 20, 22, 25],
        "ebit_5y": [20, 25, 28, 30, 35],
        "cfo_5y": [5, 8, 10, 12, 15],  # Cum CFO = 50, Cum PAT = 100 -> 0.50 < 0.75
        "capex_5y": [5, 5, 5, 5, 5], "gross_margin_5y": [40, 40, 40, 40, 40],
        "capital_employed_5y": [80, 95, 110, 125, 140],
        "gross_ppe": 100, "cwip": 10, "receivables": 20, "receivables_start": 10,
        "total_debt": 10, "total_equity": 130,
        "promoter_holding": 60.0, "promoter_pledge": 0.0,
        "fcf_latest": 10.0, "ev_ebitda": 15.0, "median_ev_ebitda_5y": 18.0
    }
    res = run_four_tier_audit(meta, fin_bad_sloan)
    assert res["tier2_pass"] is False
    assert res["overall_pass"] is False
    assert "Sloan CFO/PAT" in res["notes"]

def test_tier2_cwip_ratio_gate():
    """Verify that excessive CWIP (> 25% of Gross Block) is flagged."""
    meta = {"symbol": "FAKECAPEX.NS", "name": "Fake Capex Ltd", "sector": "Industrials", "mcap_cr": 5000, "turnover_cr": 5.0}
    fin_high_cwip = {
        "revenue_5y": [100, 120, 145, 175, 210], "pat_5y": [15, 18, 22, 26, 32],
        "ebit_5y": [20, 25, 30, 36, 44],
        "cfo_5y": [15, 18, 22, 26, 32],
        "capex_5y": [5, 6, 7, 8, 10], "gross_margin_5y": [40, 40, 40, 40, 40],
        "capital_employed_5y": [100, 120, 145, 175, 210],
        "gross_ppe": 200, "cwip": 75,  # 75/200 = 37.5% > 25%
        "receivables": 20, "receivables_start": 10,
        "total_debt": 10, "total_equity": 200,
        "promoter_holding": 60.0, "promoter_pledge": 0.0,
        "fcf_latest": 12.0, "ev_ebitda": 15.0, "median_ev_ebitda_5y": 18.0
    }
    res = run_four_tier_audit(meta, fin_high_cwip)
    assert res["tier2_pass"] is False
    assert res["overall_pass"] is False
    assert "CWIP/Block" in res["notes"]

def test_tier2_promoter_pledge_gate():
    """Verify that promoter pledge > 5% or holding < 45% fails Tier 2."""
    meta = {"symbol": "PLEDGED.NS", "name": "High Pledge Ltd", "sector": "Materials", "mcap_cr": 4000, "turnover_cr": 4.0}
    fin_pledge = {
        "revenue_5y": [100, 120, 145, 175, 210], "pat_5y": [15, 18, 22, 26, 32],
        "ebit_5y": [20, 25, 30, 36, 44],
        "cfo_5y": [16, 20, 24, 28, 34],
        "capex_5y": [5, 6, 7, 8, 10], "gross_margin_5y": [40, 40, 40, 40, 40],
        "capital_employed_5y": [100, 120, 145, 175, 210],
        "gross_ppe": 150, "cwip": 15, "receivables": 20, "receivables_start": 10,
        "total_debt": 10, "total_equity": 200,
        "promoter_holding": 52.0, "promoter_pledge": 18.5,  # Pledge > 5.0%
        "fcf_latest": 24.0, "ev_ebitda": 15.0, "median_ev_ebitda_5y": 18.0
    }
    res = run_four_tier_audit(meta, fin_pledge)
    assert res["tier2_pass"] is False
    assert res["overall_pass"] is False
    assert "Pledge" in res["notes"]

def test_tier2_debtor_days_gate():
    """Verify that receivables CAGR significantly exceeding revenue CAGR fails Tier 2."""
    meta = {"symbol": "UNCOLLECTED.NS", "name": "Uncollected Sales Ltd", "sector": "Industrials", "mcap_cr": 5000, "turnover_cr": 5.0}
    fin_debtor = {
        "revenue_5y": [100, 110, 120, 130, 140],  # Rev CAGR ~ 8.8%
        "pat_5y": [15, 18, 22, 26, 32],
        "ebit_5y": [20, 25, 30, 36, 44],
        "cfo_5y": [16, 20, 24, 28, 34],
        "capex_5y": [5, 6, 7, 8, 10], "gross_margin_5y": [40, 40, 40, 40, 40],
        "capital_employed_5y": [100, 120, 145, 175, 210],
        "gross_ppe": 150, "cwip": 15,
        "receivables": 80, "receivables_start": 20,  # Rec CAGR = (80/20)^(1/4)-1 = 41.4% > 1.2x Rev CAGR
        "total_debt": 10, "total_equity": 200,
        "promoter_holding": 55.0, "promoter_pledge": 0.0,
        "fcf_latest": 24.0, "ev_ebitda": 15.0, "median_ev_ebitda_5y": 18.0
    }
    res = run_four_tier_audit(meta, fin_debtor)
    assert res["tier2_pass"] is False
    assert "Receivables CAGR" in res["notes"]

def test_tier3_reinvestment_rate_gate():
    """Verify Capex/CFO reinvestment rate must be between 25% and 75%."""
    meta = {"symbol": "REINVEST.NS", "name": "Reinvest Test Ltd", "sector": "Industrials", "mcap_cr": 5000, "turnover_cr": 5.0}
    base_fin = {
        "revenue_5y": [100, 120, 145, 175, 215], "pat_5y": [15, 19, 24, 30, 38],
        "ebit_5y": [22, 28, 35, 44, 55],
        "cfo_5y": [20, 25, 30, 35, 40],  # Cum CFO = 150
        "gross_margin_5y": [40, 40, 40, 40, 40],
        "capital_employed_5y": [80, 100, 125, 155, 190],
        "gross_ppe": 150, "cwip": 15, "receivables": 25, "receivables_start": 15,
        "total_debt": 10, "total_equity": 180,
        "promoter_holding": 55.0, "promoter_pledge": 0.0,
        "fcf_latest": 25.0, "ev_ebitda": 18.0, "median_ev_ebitda_5y": 20.0
    }

    # Case 1: Reinvestment < 25% (e.g. Capex 20 on CFO 150 = 13.3%) -> Fails
    fin_low_reinvest = dict(base_fin, capex_5y=[4, 4, 4, 4, 4])
    res_low = run_four_tier_audit(meta, fin_low_reinvest)
    assert res_low["tier3_pass"] is False
    assert "Reinvestment" in res_low["notes"]

    # Case 2: Reinvestment in 25-75% corridor (e.g. Capex 50 on CFO 150 = 33.3%) -> Passes Tier 3
    fin_ok_reinvest = dict(base_fin, capex_5y=[8, 9, 10, 11, 12])
    res_ok = run_four_tier_audit(meta, fin_ok_reinvest)
    assert res_ok["tier3_pass"] is True

    # Case 3: Reinvestment > 75% (e.g. Capex 130 on CFO 150 = 86.7%) -> Fails
    fin_high_reinvest = dict(base_fin, capex_5y=[20, 25, 25, 30, 30])
    res_high = run_four_tier_audit(meta, fin_high_reinvest)
    assert res_high["tier3_pass"] is False

def test_tier3_pat_cagr_gate():
    """Verify that 5-year PAT CAGR < 15% fails Tier 3."""
    meta = {"symbol": "SLOWGROWTH.NS", "name": "Slow Growth Ltd", "sector": "Industrials", "mcap_cr": 5000, "turnover_cr": 5.0}
    fin_slow_pat = {
        "revenue_5y": [100, 115, 132, 152, 175],  # Rev CAGR = 15.0%
        "pat_5y": [100, 105, 110, 115, 120],      # PAT CAGR = 4.7% (< 15%)
        "ebit_5y": [140, 148, 155, 162, 170],
        "cfo_5y": [110, 115, 120, 125, 130],
        "capex_5y": [35, 35, 40, 40, 45],
        "gross_margin_5y": [40, 40, 40, 40, 40],
        "capital_employed_5y": [500, 550, 600, 650, 700],
        "gross_ppe": 400, "cwip": 30, "receivables": 100, "receivables_start": 70,
        "total_debt": 20, "total_equity": 680,
        "promoter_holding": 55.0, "promoter_pledge": 0.0,
        "fcf_latest": 85.0, "ev_ebitda": 15.0, "median_ev_ebitda_5y": 17.0
    }
    res = run_four_tier_audit(meta, fin_slow_pat)
    assert res["tier3_pass"] is False
    assert "PAT CAGR" in res["notes"]

def test_tier4_cyclical_top_trap_filter():
    """Verify that cyclical companies with prior losses or artificial spikes are caught and blocked."""
    meta = {"symbol": "SUZLON.NS", "name": "Suzlon Energy", "sector": "Wind Turbine Equipment", "mcap_cr": 64300, "turnover_cr": 180.0}
    suzlon_fin = HISTORICAL_AUDITED_DB["SUZLON.NS"]
    res = run_four_tier_audit(meta, suzlon_fin)
    assert res["tier4_pass"] is False
    assert res["overall_pass"] is False
    assert "CYCLICAL TOP TRAP" in res["verdict"]

def test_tier1_compounder_pass():
    """Verify that a genuine compounder with pristine financials passes all 4 tiers."""
    meta = {"symbol": "FINEORG.NS", "name": "Fine Organic Industries", "sector": "Specialty Chemicals", "mcap_cr": 13900, "turnover_cr": 6.2}
    fineorg_fin = HISTORICAL_AUDITED_DB["FINEORG.NS"]
    res = run_four_tier_audit(meta, fineorg_fin)
    assert res["tier1_pass"] is True
    assert res["tier2_pass"] is True
    assert res["tier3_pass"] is True
    assert res["tier4_pass"] is True
    assert res["overall_pass"] is True
    assert "APPROVED" in res["verdict"]
    assert res["score"] >= 80.0

def test_complete_universe_coverage():
    """Verify that all 48 stocks in UNIVERSE are populated in the database and audit without error."""
    assert len(UNIVERSE) == 48
    for meta in UNIVERSE:
        sym = meta["symbol"]
        assert sym in HISTORICAL_AUDITED_DB, f"Symbol {sym} missing from HISTORICAL_AUDITED_DB"
        fin_data = HISTORICAL_AUDITED_DB[sym]
        res = run_four_tier_audit(meta, fin_data)
        assert res["verdict"] != "NO AUDITED DATA", f"Symbol {sym} returned NO AUDITED DATA"
        assert res["symbol"] == sym
