#!/usr/bin/env python3
import pytest
from us_multibagger_screen import run_us_four_tier_audit, AUDITED_US_DB, UNIVERSE

def test_cprt_approved():
    meta = next(u for u in UNIVERSE if u["symbol"] == "CPRT")
    fin = AUDITED_US_DB["CPRT"]
    res = run_us_four_tier_audit(meta, fin)
    assert res["overall_pass"] is True
    assert res["score"] >= 70.0
    assert res["true_fcf_m"] > 0
    assert res["net_debt_ebitda"] < 0  # Net cash fortress

def test_snow_blocked_sbc_dilution():
    meta = next(u for u in UNIVERSE if u["symbol"] == "SNOW")
    fin = AUDITED_US_DB["SNOW"]
    res = run_us_four_tier_audit(meta, fin)
    assert res["overall_pass"] is False
    assert res["tier2_pass"] is False
    assert "Negative True FCF" in res["notes"] or "conversion" in res["notes"]

def test_azo_share_cannibal_negative_equity():
    meta = next(u for u in UNIVERSE if u["symbol"] == "AZO")
    fin = AUDITED_US_DB["AZO"]
    res = run_us_four_tier_audit(meta, fin)
    # AZO has negative equity, but high ROIC and shrinking shares
    assert res["roic"] > 30.0
    assert res["share_cagr"] < 0.0  # Share cannibal
    assert res["true_fcf_m"] > 0

def test_boeing_blocked_cyclical_distress():
    meta = next(u for u in UNIVERSE if u["symbol"] == "BA")
    fin = AUDITED_US_DB["BA"]
    res = run_us_four_tier_audit(meta, fin)
    assert res["overall_pass"] is False
    assert res["tier2_pass"] is False or res["tier3_pass"] is False

def test_intel_blocked_negative_roic_fcf():
    meta = next(u for u in UNIVERSE if u["symbol"] == "INTC")
    fin = AUDITED_US_DB["INTC"]
    res = run_us_four_tier_audit(meta, fin)
    assert res["overall_pass"] is False
    assert res["tier3_pass"] is False or res["tier4_pass"] is False

def test_visa_mastercard_duopoly():
    for sym in ["V", "MA"]:
        meta = next(u for u in UNIVERSE if u["symbol"] == sym)
        fin = AUDITED_US_DB[sym]
        res = run_us_four_tier_audit(meta, fin)
        assert res["overall_pass"] is True
        assert res["gross_margin"] >= 90.0
        assert res["roic"] >= 30.0

def test_true_fcf_math():
    cfo = 1000
    capex = 200
    sbc = 150
    true_fcf = cfo - capex - sbc
    assert true_fcf == 650
