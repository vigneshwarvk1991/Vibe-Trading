# THE EQUITY PLAYBOOK
### Personal Quantitative Trading & Investing Operating Manual

**Version:** 1.0 — August 2026  
**System:** Vibe-Trading SDK v0.1.14  
**LLM:** Gemini 3.6 Flash (Free Tier) / Ollama qwen2.5-coder:32b (Local)  
**Dashboard:** http://localhost:8000  

---

## TABLE OF CONTENTS

1. [Capital Structure](#1-capital-structure)
2. [TRACK 1 — Active Momentum Trading System](#2-track-1--active-momentum-trading-system)
3. [TRACK 2 — Multibagger Investing Framework](#3-track-2--multibagger-investing-framework)
4. [Master Prompt Library](#4-master-prompt-library)
5. [Daily, Weekly, Monthly & Quarterly Routine](#5-daily-weekly-monthly--quarterly-routine)
6. [Risk Management Rulebook](#6-risk-management-rulebook)
7. [BTST Signal Validation Protocol](#7-btst-signal-validation-protocol)
8. [Vibe-Trading SDK Quick Reference](#8-vibe-trading-sdk-quick-reference)
9. [Capital Scaling Guidelines](#9-capital-scaling-guidelines)
10. [Glossary of Key Terms](#10-glossary-of-key-terms)

---

## 1. CAPITAL STRUCTURE

```
========================================================================================================
                                     TOTAL CAPITAL ARCHITECTURE
========================================================================================================

       INDIA PORTFOLIO (₹5,00,000 Total)                 US PORTFOLIO (~$5,500 / ₹5,00,000 Total)
  ───────────────────────────────────────────       ──────────────────────────────────────────────────
  TRACK 1: Active Momentum (₹2,50,000)              TRACK 1: Active Momentum ($2,500 USD)
    • 5 Slots × ₹50,000 per position (20%)            • 5 Slots × $500 USD per position (20%)
    • Max risk per trade: ₹2,500 (1% of capital)      • Max risk per trade: $25 USD (1% of capital)
    • 5% initial stop + 2.5× ATR trailing stop        • 5% initial stop + 2.5× ATR trailing stop
    • Holding horizon: 30–90 days                     • Holding horizon: 25–40 days
    • Target: 25–40% CAGR                             • Target: 25–35% CAGR

  TRACK 2: Institutional Quality Compounders (₹2,50,000)  TRACK 2: US Moat Compounders (₹2,50,000 / ~$2,900)
    • 8–10 Core Positions × ₹25,000 – ₹31,250 (10%–12.5%)   • 6–8 World-Class Monopolies × $360 – $480 USD
    • Tranches: 65% initial conviction, 35% milestone dip   • Tranches: 65% initial conviction, 35% milestone
    • Holding horizon: 1–3+ years (Zero stop-loss)          • Holding horizon: 1–3+ years (Zero stop-loss)
    • Sell ONLY on forensic / moat breakdown                • Sell ONLY on structural moat deterioration
========================================================================================================
```

> **Iron Rule:** Trading capital and investing capital are NEVER mixed. Trading profits stay in trading. Investing capital compounds separately for multi-year wealth building.

---

## 2. TRACK 1 — Active Momentum Trading System

### Strategy Identity
| Parameter | Value |
|:---|:---|
| **Strategy Name** | 20-Day Positional Momentum Breakout |
| **Backtest Performance** | Sharpe 2.52 · Sortino 4.89 · Monte Carlo p=0.000 |
| **Long Trade Win Rate** | 72.7% (trades held >20 days) |
| **Average Holding Period** | 33 days |
| **Max Drawdown** | -24.08% |

### Entry Rules (All Must Be True)
1. ✅ **Macro Trend Filter:** Stock price is **above the 200-day EMA** with the **200-day EMA sloping upward**.
2. ✅ **Price Breakout Trigger:** Daily Close prints a fresh **20-day High Breakout** (Close $\ge$ max Close of prior 20 sessions).
3. ✅ **Relative Strength (RS) Gate:** 6-month (126-day) price performance ranks in the **top 30% of the universe (RS Percentile $\ge$ 70.0%)**.
4. ✅ **Institutional Volume Surge:** Breakout day volume is **$\ge$ 1.40× the 20-day average volume** (confirms big-money accumulation).
5. ✅ **Macro Regime Defense (Dual Momentum):** Broad benchmark (**Nifty 50**) is trading above its 200-day EMA, and India VIX is $\le$ 22. If breached, pause all new entries.

### Exit & Trailing Rules (Any One Triggers Exit)
1. 🛑 **Initial Stop-Loss:** **5.0% below buy price** (placed as Zerodha GTT immediately upon entry).
2. 📈 **Trailing Stop (ATR):** Daily Close drops below **2.5× ATR(14)** from the highest closing peak.
3. 🔒 **Breakeven Profit Lock (+12% Rule):** When position hits **+12% unrealized gain**, immediately adjust GTT stop to **Breakeven (Entry Price)**.
4. 🚀 **Windfall Protection (+20% Rule):** When position hits **+20% unrealized gain**, tighten trailing stop from 2.5× ATR to **1.5× ATR(14)**.
5. 📉 **Trend Invalidation:** Close drops below the 200-day EMA.
6. ⏰ Whichever exit trigger is hit first executes the exit immediately.

### Position Sizing
| Parameter | Calculation |
|:---|:---|
| **Total Track 1 Capital** | ₹2,50,000 (Allocated from 10-Sep-2026) |
| **Capital per Slot** | ₹50,000 (20% of ₹2.5L per slot) |
| **Max Concurrent Positions** | 5 stocks |
| **Shares to Buy** | ₹50,000 ÷ Stock Price (round down) |
| **Max Risk per Trade** | ₹2,500 (1.0% of total ₹2.5L capital at 5% stop) |

### Universe Selection: 100% Dynamic Liquid Nifty 500 Protocol
**Zero Hardcoded Stocks.** The system dynamically scans the entire **NIFTY 500 Index universe (NSE India)** every trading session.

Any Nifty 500 stock that satisfies the full institutional rulebook is eligible for entry regardless of sector.

* **Universe Scope:** 501 large, mid, and liquid small-cap constituents of the Nifty 500 index.
* **Liquidity Gates (Mandatory):**
  * **Turnover Gate:** 20-day Average Daily Turnover $\ge$ **₹5.0 Crore** (eliminates illiquid traps and pump-and-dump microcaps).
  * **Volume Gate:** 20-day Average Daily Volume $\ge$ **500,000 shares** (guarantees instantaneous order execution with zero slippage).
* **Sector Diversification:** Maximum 2 positions from the same industry sector to eliminate concentration risk across your 5 slots.

### Portfolio Tracker Template

| Slot | Stock | Entry Date | Entry Price | Shares | Stop-Loss | Trail Stop | Status |
|:---|:---|:---|:---|:---|:---|:---|:---|
| 1 | HAL.NS | 28-Aug-2026 | ₹4,861.00 | 2 | ₹4,617.95 | ₹4,823.90 | 🟢 ACTIVE (Trail to ₹4,823.90) |
| 2 | DIVISLAB.NS | 03-Sep-2026 | ₹9,244.00 | 3 | ₹8,781.80 | ₹9,063.44 | 🟢 ACTIVE (Trail to ₹9,063.44) |
| 3 | CHENNPETRO.NS | 10-Sep-2026 | ₹1,594.00 | 30 | ₹1,514.30 | ₹1,514.30 | 🟢 ACTIVE |
| 4 | ADANIPORTS.NS | 10-Sep-2026 | ₹1,768.00 | 28 | ₹1,679.60 | ₹1,679.60 | 🟢 ACTIVE |
| 5 | — | — | — | — | — | — | 💰 CASH (Slot 5: ₹50,000 capacity · ₹1,15,222 free cash available) |

*Capital Deployment Note:* Slots 1 (HAL) and 2 (DIVISLAB) were entered with 2 and 3 shares respectively (₹37,454 combined) prior to capital expansion to ₹2.5L. Slots 3 (CHENNPETRO) and 4 (ADANIPORTS) are sized at the full ₹50,000 slot capacity. Total invested: ₹1,34,778. Free account cash: ₹1,15,222. Total portfolio risk heat: ₹6,738.90 (2.70% of ₹2,50,000 equity, safely below 5.0% maximum risk ceiling).

---

## 3. TRACK 2 — Multibagger Investing Framework (Four-Tier Institutional Compounder System)

### The Problem with Naive Screens (Why the Old 5 Pillars Failed)
1. **The Cyclical PEG Trap:** Naive trailing PEG ratios (< 1.5) flag cyclical commodity stocks (like Suzlon, sugar, paper, or steel mills) at the exact cyclical top when earnings temporarily explode, leading to devastating drawdowns.
2. **Single-Point ROE Illusion:** Single-point ROE from snapshot data (`t.info`) fails to detect leverage-driven returns, unbilled revenue, or sudden one-off asset sales.
3. **Financials Distortion:** Applying debt-to-equity (< 0.5) and ROCE to Banks/NBFCs produces absurd conclusions because lenders operate by taking on debt (deposits/borrowings) as their core raw material.
4. **Catastrophic Concentration Risk:** Allocating ₹2,50,000 into only 5 stocks (₹50k each) with zero stop-loss means a single corporate governance failure or structural disruption wipes out 20% of the entire investing capital.

---

### The Four-Tier Institutional Compounder Framework (ALL Must Pass)

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│              TIER 1: UNIVERSE & LIQUIDITY GATE (Pre-Screening)                  │
│  • Universe: Nifty Midcap 150 + Nifty Smallcap 250 + Liquid Microcaps           │
│  • Market Cap ≥ ₹1,000 Cr  ·  20-Day Avg Daily Turnover ≥ ₹2.0 Cr               │
│  • STRICT EXCLUSION: Banks, Financial Services, and NBFCs (Separate Model)      │
└──────────────────────────────────────┬──────────────────────────────────────────┘
                                       │ (Passes Liquidity)
                                       ▼
┌─────────────────────────────────────────────────────────────────────────────────┐
│            TIER 2: FORENSIC ACCOUNTING GATES (Pass / Fail — Zero Tolerance)     │
│  • Sloan Accrual Test: 5-Yr Cumulative CFO / Cumulative PAT ≥ 0.75 (Cash is Real)│
│  • CWIP / Gross Block Ratio ≤ 25% (No fake capital work-in-progress masking opex)│
│  • Debtor Days Growth Discipline: Receivables CAGR ≤ 1.2× Revenue CAGR (3-5 Yr) │
│  • Promoter Integrity: Promoter Holding ≥ 45%  ·  Total Promoter Pledge ≤ 5.0%  │
│  • Auditor Quality: Clean unmodified audit opinion; zero mid-term resignations   │
└──────────────────────────────────────┬──────────────────────────────────────────┘
                                       │ (Passes Forensic Audit)
                                       ▼
┌─────────────────────────────────────────────────────────────────────────────────┐
│          TIER 3: SECULAR MOAT & COMPOUNDING ENGINE (Audited Historicals)        │
│  • Audited ROCE: ROCE ≥ 18.0% in at least 4 of the last 5 fiscal years          │
│  • Pricing Power: Gross Margin ≥ 30.0% and flat or expanding over 5 years       │
│  • Growth Engine: 5-Year Revenue CAGR ≥ 12.0%  ·  5-Year PAT CAGR ≥ 15.0%        │
│  • Reinvestment Discipline: Capex / CFO between 25% and 75% (High Reinvestment) │
│  • Balance Sheet Fortress: Debt-to-Equity < 0.50 (or Net Cash / Debt-Free)      │
└──────────────────────────────────────┬──────────────────────────────────────────┘
                                       │ (Passes Compounder Engine)
                                       ▼
┌─────────────────────────────────────────────────────────────────────────────────┐
│             TIER 4: VALUATION GUARDRAIL & CYCLICAL ANTI-TRAP SHIELD             │
│  • Cash Flow Yield: Free Cash Flow Yield ≥ 2.0% OR EV/EBITDA < 5-Year Median     │
│  • Cyclical Top Filter: REJECT if 1-Yr EPS spiked >50% while 5-Yr median < 10%  │
└─────────────────────────────────────────────────────────────────────────────────┘
```

---

### Position Sizing: Institutional 8 to 10 Slot Architecture

To eliminate the fatal concentration risk of a 5-stock portfolio with zero stop-loss, Track 2 capital is distributed across **8 to 10 high-conviction compounders**:

| Parameter | Calculation / Protocol |
|:---|:---|
| **Total Track 2 Capital** | **₹2,50,000** (Clean slate as of September 2026) |
| **Number of Positions** | **8 to 10 Quality Compounders** |
| **Capital Allocation per Stock** | **₹25,000 to ₹31,250 per company** (10.0% to 12.5% max weight) |
| **Sector Diversification** | Maximum **2 positions** from any single industry sector |
| **Stop-Loss Policy** | **Zero Hard Stop-Loss** (True multi-year business compounding) |
| **Holding Horizon** | **1 to 3+ Years** (Evaluated strictly on quarterly earnings fundamentals) |

---

### Tranche Accumulation Protocol (Institutional Dip-Buying)
*Never commit 100% of a long-term position in a single market order.*

* 🎯 **Tranche 1 (65% — ₹16,250 to ₹20,312):** Initial conviction entry immediately upon passing all 4 Tiers and receiving Investment Committee Swarm Buy approval.
* 🛡️ **Tranche 2 (35% — ₹8,750 to ₹10,938):** Milestone accumulation entry deployed ONLY upon:
  1. **A 7% to 12% market or sector-wide pullback** where company fundamentals remain completely pristine; OR
  2. **90-day post-entry quarterly earnings verification** confirming continued ROCE $\ge 18\%$ and Sloan cash conversion (CFO/PAT $\ge 0.75$).

---

### Multibagger Sell Rules (Fundamental Kill Switches — NO Panic Selling)

> **Iron Rule:** Multibaggers are NEVER sold due to general market corrections, index volatility, or macroeconomic geopolitical noise. A position is exited IMMEDIATELY (100% liquidated) ONLY if ANY of the following fundamental breakdown criteria occur:

1. ❌ **ROCE Breakdown:** ROCE drops below $15.0\%$ for 2 consecutive fiscal years (signals moat erosion or bad capital allocation).
2. ❌ **Forensic Accounting Red Flag:** Sloan cash conversion fails (5-year cumulative CFO / PAT drops below $0.60$), or statutory auditor resigns mid-term.
3. ❌ **Promoter Integrity Failure:** Total promoter pledge exceeds $10.0\%$, promoter aggressively sells equity in open market, or promoter faces SEBI/regulatory fraud indictment.
4. ❌ **Margin Collapse:** Gross margin compresses by $> 300\text{ bps}$ for 2 consecutive fiscal years due to loss of pricing power or commoditization.
5. ❌ **Perpetual CWIP Trap:** Capital Work-in-Progress (CWIP) exceeds $35\%$ of Gross Block for over 18 months without commercial production or revenue generation.
6. ❌ **Structural Obsolescence:** Emergence of disruptive substitute technology or regulatory ban that permanently impairs the company's terminal value.

---

## 4. MASTER PROMPT LIBRARY

> **Important:** Always click **`+` (New Session)** before running any prompt to minimize token usage and prevent context confusion.

---

### 4A. DAILY MOMENTUM SCAN (Track 1)
*Run every weekday between 4:00 PM – 8:00 PM IST*

```text
Execute the Dynamic Liquid Nifty 500 Positional Momentum Scanner across all 501 constituents:
Command: python india_momentum_scanner.py --sync-sheet

My Current Portfolio Holdings (Managed in Zerodha Kite CNC & synced with Google Sheet 'Tradebook IN'):
- Slot 1: HAL.NS (2 shares bought @ ₹4,861.00, SL ₹4,617.95, GTT Trail SL updated to ₹4,823.90)
- Slot 2: DIVISLAB.NS (3 shares bought @ ₹9,244.00, SL ₹8,781.80, GTT Trail SL updated to ₹9,063.44)
- Slot 3: CHENNPETRO.NS (30 shares bought @ ₹1,594.00, SL ₹1,514.30)
- Slot 4: ADANIPORTS.NS (28 shares bought @ ₹1,768.00, SL ₹1,679.60)
- Slot 5: CASH (₹50,000 slot capacity, ₹1,15,222 free cash available)

Please calculate:
1. NEW ENTRY CHECK: Did any Nifty 500 stock print a confirmed 20-day High Breakout with Vol Surge >= 1.4x and RS >= 70%? If yes, calculate the exact quantity to buy for my open ₹50,000 slot and the 5% initial stop-loss.
2. TRAILING STOP UPDATE: For my open holdings, calculate the updated 2.5x ATR(14) trailing stop level based on today's session high. Should I update my stop-loss GTT or exit?
3. SUMMARY TABLE: Give me an executive trade execution sheet for tomorrow morning.
```

---

### 4B. MONTHLY WATCHLIST REFRESH (Track 1)
*Run on the 1st weekend of every month*

```text
Run a momentum leadership scan across the Nifty 100 universe as of today:
1. Filter stocks trading above their 200-day EMA with the EMA slope positive.
2. Rank survivors by 6-month price momentum (highest return over 126 trading days).
3. Show the top 15 momentum leaders with: Symbol, Sector, 6M Return, Distance from 52-Week High, Average Daily Volume, and 200-day EMA slope direction.
4. Identify which of my current watchlist stocks have fallen below their 200-day EMA and should be replaced.
```

---

### 4C. MULTIBAGGER SCREENER (Track 2)
*Run on the 1st weekend of every month*

```text
Screen the Nifty Midcap 150, Nifty Smallcap 250, and liquid microcap universe for institutional multibagger compounders:

TIER 1 — UNIVERSE & LIQUIDITY:
1. Market Cap ≥ ₹1,000 Cr and 20-day Average Daily Turnover ≥ ₹2.0 Cr.
2. Strictly exclude Financials, Banks, and NBFCs (non-financials only).

TIER 2 — FORENSIC ACCOUNTING GATES (Must Pass All):
3. Sloan Accrual Test: 5-year cumulative CFO / Cumulative PAT ≥ 0.75 (Cash Flow aligns with net profits).
4. CWIP / Gross Block Ratio ≤ 25% (No stalled or inflated unfinished assets).
5. Debtor Days Growth: Receivables CAGR ≤ 1.2× Revenue CAGR over past 3 years.
6. Promoter Holding ≥ 45% with Total Promoter Pledge ≤ 5.0%.
7. Clean unmodified audit report with zero mid-term auditor resignations in past 3 years.

TIER 3 — SECULAR MOAT & COMPOUNDING ENGINE:
8. Audited ROCE ≥ 18% in at least 4 of the last 5 fiscal years.
9. Gross Margin ≥ 30% and flat or expanding over 5 years.
10. 5-year Revenue CAGR ≥ 12% and 5-year PAT CAGR ≥ 15%.
11. Reinvestment Rate: Capex / CFO between 25% and 75%.
12. Debt-to-Equity < 0.50 (or Net Cash).

TIER 4 — VALUATION GUARDRAIL:
13. Free Cash Flow Yield ≥ 2.0% OR EV/EBITDA < 5-year historical median.
14. Cyclical Top Filter: Reject 1-year earnings spikes (>50%) where 5-year median growth is < 10%.

Rank survivors by composite quality score (ROCE stability + CFO/PAT conversion + FCF yield). Display top 10 with full diagnostic metrics.
```

---

### 4D. DEEP COMPANY ANALYSIS (Track 2)
*Run on each multibagger candidate before investing*

```text
Run a comprehensive institutional equity research teardown on [TICKER.NS] using the Four-Tier Compounder Framework:

1. Business Model & Moat: What is the core business? What is the pricing power source (network effect, high switching costs, patents, cost leadership)? Why can competitors not replicate this?
2. Forensic Accounting Teardown:
   - Sloan Accrual Check: 5-year cumulative CFO vs PAT (is CFO/PAT ≥ 0.75?).
   - Capitalization Check: CWIP as % of Gross Block (is CWIP ≤ 25%?).
   - Working Capital Discipline: Receivables growth vs Revenue growth. Are Debtor Days stable?
   - Balance Sheet Quality: Debt/Equity, contingent liabilities, related-party transactions, auditor identity and tenure.
3. Compounding Engine (5-Year Historicals):
   - Audited ROCE trend across FY20–FY25 (consistent ≥ 18%?).
   - Gross Margin and EBITDA Margin trajectory (expanding or compressing?).
   - Revenue and PAT CAGRs over 3 and 5 years.
   - Reinvestment Rate (Capex / CFO): Are they reinvesting at high return on capital?
4. Management Track Record:
   - Promoter holding and pledge trend over last 8 quarters.
   - Capital allocation history: Past M&A track record, return on past capex, dividend payout prudence.
5. Valuation & Cyclicality Check:
   - Current EV/EBITDA and P/E vs 5-year and 10-year historical medians.
   - Free Cash Flow Yield at current market cap.
   - Cyclical Top Filter: Is current high profit an anomalous commodity cycle peak or secular structural expansion?
6. Kill Criteria & Risk Matrix: What specific events would trigger an immediate exit?
7. Verdict & Tranche Execution: Buy, Wait, or Reject? If Buy, specify Tranche 1 (65% @ ₹[PRICE]) and Tranche 2 (35% milestone accumulation trigger).
```

---

### 4E. INVESTMENT COMMITTEE SWARM (Track 2)
*Run before committing capital to any multibagger*

```text
Run the investment_committee swarm on [TICKER.NS] under the Four-Tier Institutional Compounder Framework.

- The Bull Analyst: Present the structural 3-year compounding thesis (addressing addressable market runway, pricing power, ROCE durability, and reinvestment rate).
- The Bear Analyst: Stress-test every vulnerability (cyclical peak risk, customer concentration, input cost inflation, regulatory threats, technological disruption).
- The Forensic Accountant: Audit the financial statements (Sloan accrual test CFO/PAT, CWIP/Gross Block, debtor days, related party transactions, promoter pledge, and auditor quality).
- The Risk Manager: Audit sector concentration, verify 8–10 position sizing (₹25,000–₹31,250 allocation, max 12.5%), and establish Tranche 1 (65%) and Tranche 2 (35%) accumulation rules.
- The Portfolio Manager: Deliver the final institutional verdict: Conviction BUY (Approved for Tranche 1), WAIT FOR MILESTONE, or REJECT (with explicit failure tier).
```

---

### 4F. INVESTOR LENS ANALYSIS (Track 2)

```text
Evaluate [TICKER.NS] through the distinct lenses of master investors:

1. Warren Buffett (Economic Moat & Return on Capital): Does the company possess a durable pricing power moat? Is ROCE consistently > 18% without excessive leverage? Would you hold this business if the stock market closed for 5 years?
2. Peter Lynch (Category & Peg Sanity): Classify the business (Fast Grower, Stalwart, Cyclical, Turnaround). Does it avoid the cyclical peak trap? Is valuation reasonable relative to secular (not 1-year spike) growth?
3. Philip Fisher (Scuttlebutt & Management Quality): Does management have integrity and transparent accounting? Is R&D and capex creating genuine customer value? Are margins expanding?
4. Joel Greenblatt (Magic Formula): Calculate Earnings Yield (EBIT / Enterprise Value) and Return on Capital (EBIT / [Net Working Capital + Net Fixed Assets]). Does it rank in the top tier?

Consolidated Score: 0 to 100. Provide explicit Buy/Avoid recommendation with key strengths and fatal weaknesses.
```

---

### 4G. QUARTERLY EARNINGS REVIEW (Track 2)
*Run after each quarterly result on every multibagger holding*

```text
Perform an institutional quarterly earnings healthcheck on multibagger holding [TICKER.NS]:

1. Operational Performance: Did Revenue and PAT meet or exceed 12% / 15% YoY hurdles?
2. Margin & Pricing Power: Did Gross Margin contract or expand? Did EBITDA margin hold steady?
3. Cash Conversion: Is operating cash flow tracking net income for the trailing 12 months? Any working capital bloat?
4. Balance Sheet & Governance: Any increase in debt, CWIP accumulation, promoter pledge, or insider selling?
5. Fundamental Kill Switch Audit: Are all 4 Tiers still completely intact?
   - ROCE ≥ 18% intact?
   - Sloan CFO/PAT ≥ 0.75 intact?
   - Promoter pledge ≤ 5% intact?
   - Gross Margin flat/expanding?
6. PORTFOLIO ACTION:
   - CONTINUE HOLDING (Fundamentals completely sound)
   - DEPLOY TRANCHE 2 (35% milestone addition — if post-earnings dip or positive operational milestone reached)
   - LIQUIDATE IMMEDIATELY (Fundamental kill switch triggered — state exact broken rule)
```

---

### 4H. BTST SIGNAL VALIDATION (External Tips)
*Run BEFORE taking any Buy Today Sell Tomorrow tip*

```text
Perform an instant BTST Quantitative Validation for: [TICKER.NS] at proposed entry ₹[PRICE].

1. Day's Price Action: Did the stock close in the top 10% of today's high-low range?
2. Volume Confirmation: Is today's volume > 1.5x the 20-day average volume?
3. Trend & Momentum: Is 14-day RSI between 55 and 70? Price above 20 and 50 EMAs?
4. Overhead Roadblock: Where is the nearest resistance? Is there +2% room?
5. BTST VERDICT: Score (0 to 10) and final verdict:
   - [APPROVED] with exact Target and Stop-Loss.
   - [REJECTED] with exact reasons to avoid.
```

---

### 4I. WEEKLY PORTFOLIO RISK CHECK (Both Tracks)

```text
Run the risk_committee swarm on my current portfolio:

Active Trading Holdings:
- [List your current active positions]

Multibagger Holdings:
- [List your multibagger positions]

Analyze: Total portfolio beta, sector concentration risk, correlation between holdings, current drawdown status, and any position that needs attention.
```

---

### 4J. SHADOW ACCOUNT — TRADE JOURNAL AUDIT

```text
Import my trade journal and run a Shadow Account behavioral analysis.
Identify: disposition effect score, overtrading frequency, average winner vs loser holding period, and delta-PnL between my actual trades vs. systematic rule execution.
Show me exactly where I lost money due to emotional decisions.
```

---

## 5. DAILY, WEEKLY, MONTHLY & QUARTERLY ROUTINE

### Daily (5 minutes — Weekdays Only)
```
[ 4:00 PM IST ]  Run Prompt 4A (Daily Momentum Scan)
[ 4:03 PM IST ]  Check: Any new entry signal? Any trailing stop update?
[ 4:05 PM IST ]  Open broker app → Place GTT orders or update stop-losses
[ Done ]         Close everything. Do NOT watch charts during market hours.
```

### Weekly (15 minutes — Saturday)
```
[ Saturday ]     Run Prompt 4I (Portfolio Risk Check via risk_committee swarm)
                 Review: Any position breaching risk limits?
                 Update the Portfolio Tracker Template (Section 2)
```

### Monthly (1 hour — 1st Weekend)
```
[ 1st Saturday ] Run Prompt 4B (Monthly Watchlist Refresh)
                 → Replace any stock below 200-day EMA with next momentum leader

[ 1st Saturday ] Run Prompt 4C (Multibagger Screener)
                 → Deep-dive any new candidates using Prompt 4D + 4E + 4F
                 → Add to multibagger portfolio if all Four Tiers pass
```

### Quarterly (After Earnings Season — Jan, Apr, Jul, Oct)
```
[ Post Results ] Run Prompt 4G (Quarterly Review) on EACH multibagger holding
                 → Confirm Four Tiers intact → Hold
                 → If deteriorating → Run Investment Committee Swarm → Decide

[ Post Results ] Run Prompt 4J (Shadow Account Audit) on past quarter's trades
                 → Identify and eliminate behavioral mistakes
```

---

## 6. RISK MANAGEMENT RULEBOOK

### Active Trading (Track 1) — Iron Rules

| Rule | Description | Why |
|:---|:---|:---|
| **1% Rule** | Max loss per trade = 1% of total trading capital (₹2,500) | Survives 20 consecutive losses |
| **5% Stop-Loss** | Every position gets a 5% stop-loss GTT on day of entry | No exceptions. No "hoping" |
| **Stops Only Move UP** | Trailing stops are only adjusted upward, never downward | Locks in profits systematically |
| **Max 5 Positions** | Never hold more than 5 active trades simultaneously | Prevents over-diversification |
| **No Averaging Down** | NEVER add to a losing active trade | Averaging down = compounding mistakes |
| **Drawdown Circuit Breaker** | If portfolio drops -15%, reduce slot size to ₹25,000 for 4 weeks | Capital preservation during bad regimes |
| **No Trading During News** | Skip entries on Budget Day, RBI Policy, Election Results | Gap risk destroys stop-losses |

### Multibagger Investing (Track 2) — Patience Rules

| Rule | Description |
|:---|:---|
| **No Stop-Loss** | Multibaggers can drop 30–50% during market panics before going up 500%+. TRENT fell -45% in COVID then surged +900%. |
| **8–10 Slot Distribution** | Capital is divided across 8 to 10 stocks (₹25,000 to ₹31,250 each) to eliminate fatal concentration risk. |
| **Minimum 1-Year Hold** | Do not evaluate multibaggers on weekly or monthly market noise. |
| **Buy in Tranches** | 65% initial conviction entry, 35% milestone accumulation (on a 7%–12% dip or 90-day post-earnings verification). |
| **Sell Only on Business Failure** | Never sell on price drops. Exit ONLY when any of the 4-Tier Fundamental Kill Switches trigger. |
| **Quarterly Review Only** | Audit fundamentals strictly after audited quarterly financial filings. Not daily. |

---

## 7. BTST SIGNAL VALIDATION PROTOCOL

When your friend (or any external source) sends you a BTST tip:

```
  STEP 1: Open Vibe-Trading → Click + (New Session)
  STEP 2: Paste Prompt 4H with the ticker and proposed price
  STEP 3: Read the VERDICT:

  Score ≥ 7/10  →  ✅ APPROVED. Place the trade with the given Target & Stop-Loss.
  Score 4–6/10  →  ⚠️ RISKY. Skip unless you have strong conviction.
  Score ≤ 3/10  →  ❌ REJECTED. Do NOT enter. Protect your capital.

  STEP 4: If APPROVED, set a strict 1.5% stop-loss (BTST is overnight risk).
  STEP 5: Sell at 9:15–9:30 AM next morning regardless of profit or loss.
```

---

## 8. VIBE-TRADING SDK QUICK REFERENCE

### Starting the Server
```bash
cd /path/to/Vibe-Trading
source .venv/bin/activate
python agent/api_server.py
```
Dashboard: http://localhost:8000

### Key Settings (⚙️)
| Setting | Recommended Value |
|:---|:---|
| **Provider** | Gemini (Free) or Ollama (Local) |
| **Model** | gemini-3.6-flash or qwen2.5-coder:32b |
| **Timeout** | 300 seconds (for local models) |
| **Temperature** | 0.2 |

### Useful Swarm Presets
| Command | Use Case |
|:---|:---|
| `investment_committee` | Before any major Buy/Sell decision |
| `risk_committee` | Weekly portfolio health check |
| `fundamental_research_team` | Deep multibagger analysis |
| `value_investing_committee` | Valuation and margin-of-safety check |
| `technical_analysis_panel` | Multi-school technical confirmation |
| `quant_strategy_desk` | Building new systematic strategies |

### Saving a Custom Skill
```text
Save this [scan/strategy/analysis] as a permanent custom skill
named "[skill-name]". Make it triggerable by typing "run [skill-name]".
```

### Scheduling Automated Scans
Go to **Scheduled** tab → Create Scheduled Run:
- Cron: `0 16 * * 1-5` (Monday–Friday at 4:00 PM IST)
- Prompt: Paste your Daily Momentum Scan prompt

---

## 9. CAPITAL SCALING GUIDELINES

### When to Scale Up Active Trading Capital

| Milestone | Action |
|:---|:---|
| **Month 1–2** | Trade with initial ₹2.5L capital (5 slots × ₹50,000). Master execution rhythm. |
| **After 3 months of consistent profit** | Add ₹2.5L → ₹5.0L (increase to 5 slots × ₹1.0L) |
| **After 6 months with Sharpe > 1.0** | Add ₹2.5L → ₹7.5L (5 slots × ₹1.5L) |
| **After 12 months of audited track record** | Consider adding options (Engine 2) and crypto (Engine 3) |

### When to Scale Down
| Trigger | Action |
|:---|:---|
| **3 consecutive stop-outs** | Pause new entries for 1 week. Review with Shadow Account. |
| **Portfolio drawdown > -15%** | Cut slot size to ₹25,000 for 4 weeks. |
| **Monthly loss > -5%** | Run risk_committee swarm. Identify if market regime changed. |

---

## 10. GLOSSARY OF KEY TERMS

| Term | Definition |
|:---|:---|
| **EMA** | Exponential Moving Average — a weighted moving average giving more importance to recent prices |
| **ATR** | Average True Range — measures daily price volatility (higher ATR = more volatile) |
| **GTT** | Good Till Triggered — a broker order that stays active until your price level is hit |
| **ROCE** | Return on Capital Employed — how efficiently a company uses its capital to generate profits |
| **PEG** | Price/Earnings to Growth ratio — P/E divided by earnings growth rate. Below 1.5 = reasonably priced |
| **Sharpe Ratio** | Risk-adjusted return metric. Above 1.0 = good, Above 2.0 = excellent |
| **Monte Carlo p-value** | Statistical test. Below 0.05 = your strategy's edge is real, not luck |
| **Drawdown** | Peak-to-trough decline in portfolio value. -24% means your ₹2.5L temporarily dropped to ₹1.9L |
| **CNC / Delivery** | Cash and Carry — buying shares for delivery (you own them). Not intraday. |
| **BTST** | Buy Today Sell Tomorrow — buying at 3:15 PM and selling at 9:15 AM next morning |
| **Theta** | Time decay in options — the amount an option loses in value every day |
| **Delta-Neutral** | A position with zero directional exposure (equal long and short) |
| **Swarm** | A team of multiple AI agents that debate and analyze from different perspectives |

---

> **Remember:** The goal is not to get rich overnight. The goal is to compound small, consistent, mathematically validated gains over months and years — while eliminating emotional mistakes through systematic discipline.

---

## 11. US EQUITIES PLAYBOOK (Track 1 Momentum for Interactive Brokers)

### Strategy Identity
| Parameter | Value |
|:---|:---|
| **Strategy Name** | US 20-Day Positional Momentum Breakout |
| **Asset Class** | US Cash Equities (Long-Only Delivery, S&P 500 & Nasdaq 100) |
| **Broker Engine** | Interactive Brokers (IBKR India / Global) — Zero direct API, 100% human-in-the-loop |
| **Regulatory Framework** | RBI Liberalised Remittance Scheme (LRS) — Cash Delivery Only, 0% Leverage, No US Derivatives |
| **Backtest Benchmark** | S&P 500 (`SPY`) / Nasdaq 100 (`QQQ`) |
| **Average Holding Period** | 25–40 days |

---

### Position Sizing & Parameters
| Parameter | Calculation / Value |
|:---|:---|
| **Total US Trading Capital** | **$2,500 USD** (Allocated from 10-Sep-2026) |
| **Number of Slots** | **5 Slots × $500.00 USD per slot (20%)** |
| **Fractional Shares Advantage** | Supported! $\text{Shares} = \frac{\$500.00}{\text{Stock Price}}$ (filled to 3 decimal places) |
| **Initial Stop-Loss** | **5.0% below buy price** (GTC Stop order placed in IBKR upon entry) |
| **Trailing Stop (ATR)** | Daily Close drops below **2.5× ATR(14)** from peak close |
| **Max Risk per Trade** | **$25.00 USD** (1.0% of total $2,500 capital at 5% stop) |
| **+12% Profit Lock Rule** | At +12% gain, move GTC Stop to Breakeven (Entry Price) |
| **+20% Windfall Protection**| At +20% gain, tighten trailing stop to **1.5× ATR(14)** |

---

### Universe Selection: Dynamic S&P 500 & Nasdaq 100 Protocol
1. **Universe Scope**: 503 liquid constituents of the S&P 500 and Nasdaq 100.
2. **Liquidity Gate**: Average Daily Volume > 1,000,000 shares (zero slippage drag).
3. **Sector Diversification**: Maximum 2 concurrent positions from the same GICS sector.

---

### Operating Schedule (Indian Standard Time - IST)
* **US Market Hours**: 9:30 AM – 4:00 PM EST (**7:00 PM – 1:30 AM IST**).
* **Daily Scan Window**: Run morning at **7:00 AM – 8:00 AM IST** (post-US market close) or late night at **1:45 AM IST**.
* **Order Execution Window**: Place GTC (Good-Til-Cancelled) orders in IBKR anytime during the day before the 7:00 PM IST US market open.

### Active US Portfolio Tracker Template (Interactive Brokers)

| Slot | Stock | GICS Sector | Entry Date | Entry Price | Shares | Total Capital | Hard Stop (5%) | Trail Stop | Max Risk ($) | Status |
|:---|:---|:---|:---|:---|:---|:---|:---|:---|:---|:---|
| 1 | VLO | Energy / Refining | 09-Sep-2026 | $383.00 | 1.310 | $501.73 | $363.71 | $363.71 | $25.27 (1.01%) | 🟢 ACTIVE (CMP: $388.95) |
| 2 | SWKS | Technology / Semis | 09-Sep-2026 | $76.15 | 6.633 | $505.10 | $72.34* | $72.34 | $25.27 (1.01%) | 🟢 ACTIVE (CMP: $76.54) |
| 3 | BG | Consumer / Agribusiness | 09-Sep-2026 | $123.29 | 4.100 | $505.49 | $117.70 | $117.70 | $22.92 (0.92%) | 🟢 ACTIVE (CMP: $123.50) |
| 4 | — | Cash Reserve | — | — | — | $500.00 | — | — | $0.00 | 💰 CASH |
| 5 | — | Cash Reserve | — | — | — | $487.68 | — | — | $0.00 | 💰 CASH |

*\*Risk Audit Finding & Corrective Action on SWKS:* In IBKR broker order, the stop-loss was originally set at $71.61 ($30.11 risk / 1.20% equity). GTC Stop must be tightened to **$72.34** ($76.15 × 0.95), restoring exact 1.0% maximum risk adherence ($25.00 max risk).

* **Total US Trading Capital:** $2,500.00 USD (5 slots × $500.00)
* **Total Invested Capital:** $1,512.32 USD (3 Active Positions)
* **Total Cash Available:** $987.68 USD (2 Open Slots for Next Breakouts)
* **Combined Portfolio Heat:** $73.46 USD (2.94% of total US equity, safely below 5.0% ceiling)

---

### Google Sheet Routing
* **`Tradebook US`**: Active open US stock positions (Date, Symbol, Sector, Action, Quantity, Entry Price, Total Capital, Stop Loss).
* **`To Buy - US`**: Action orders generated by the morning scan (Date, Symbol, Sector, Action, Quantity, Entry Price, Total Capital, Stop Loss, Trail Stop, Max Risk, Status).

---

### Master US Prompt Library (Track 1 Momentum)

#### 11A. DAILY US MOMENTUM SCAN
*Run every weekday morning between 7:00 AM – 8:00 AM IST (or 1:45 AM IST)*

```text
Run our US Positional Momentum Market Scan across the S&P 500 and Nasdaq 100 universe as of yesterday's US market close:

My Current US Portfolio Holdings:
- Slot 1: VLO (3.364 shares bought @ $148.65, SL $141.22)
- Slot 2: SWKS (6.645 shares bought @ $76.15, SL $72.34)
- Slot 3: BG (5.124 shares bought @ $98.80, SL $93.86)
- Slot 4: CASH ($500.00 available)
- Slot 5: CASH ($487.67 available)

Please calculate:
1. NEW ENTRY CHECK: Did any S&P 500 / Nasdaq 100 stock close at a fresh 20-day High while trading above its rising 200-day EMA? If yes, calculate exact fractional quantity for my $500 slot and the 5% initial stop-loss.
2. TRAILING STOP UPDATE: For my open US holdings, calculate the updated 2.5x ATR(14) trailing stop level based on peak close. Should I adjust my IBKR GTC stop or exit?
3. SUMMARY TABLE: Format an executive trade sheet with Symbol, Action (BUY/HOLD/EXIT), Qty, Entry Limit, and GTC Stop-Loss, and push to Google Sheet "US_to_buy" tab.
```

---

#### 11B. MONTHLY US LEADERSHIP REFRESH
*Run on the 1st weekend of every month*

```text
Run a momentum leadership scan across the S&P 500 and Nasdaq 100 universe as of today:
1. Filter stocks trading above their 200-day EMA with a positive 200 EMA slope.
2. Rank survivors by 6-month price momentum (126-day return).
3. Display the top 15 US momentum leaders with: Symbol, Sector, 6M Return, Distance from 52-Week High, 20-day ATR, and Volume.
4. Flag any current US watchlist stocks that have fallen below their 200-day EMA and should be rotated out.
```

---

## 12. US MULTIBAGGER INVESTING FRAMEWORK (Track 2 US)

### Capital Allocation & Structure
| Parameter | Value / Protocol |
|:---|:---|
| **Total Track 2 US Capital** | **₹2,50,000** (~**$2,850 – $3,000 USD** at current FX) |
| **Number of Core Positions** | **6 to 8 World-Class Moat Compounders** |
| **Allocation per Company** | **~$360 – $480 USD** per stock (12.5%–16.6% max weight) |
| **Broker Engine** | Interactive Brokers (IBKR Cash Delivery — Zero Margin, No Options) |
| **Fractional Sizing** | Exact fractional shares to 4 decimal places via IBKR |
| **Google Sheet Routing** | **`Multibagger - US`** |
| **Holding Horizon** | **1–3+ Years** (Long-term business compounders, Zero stop-loss) |

---

### The Four-Tier US Institutional Compounder Framework (ALL Must Pass)

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│              TIER 1: ELITE US MOAT UNIVERSE (Pre-Screening)                     │
│  • Universe: S&P 500 + S&P MidCap 400 + Nasdaq 100 constituents                 │
│  • Market Cap Floor: Market Capitalization ≥ $5.0 Billion USD                   │
│  • Liquidity Floor: 20-Day Average Daily Volume ≥ 1,000,000 shares              │
└──────────────────────────────────────┬──────────────────────────────────────────┘
                                       │ (Passes Universe Gate)
                                       ▼
┌─────────────────────────────────────────────────────────────────────────────────┐
│       TIER 2: TRUE OWNER EARNINGS & ANTI-DILUTION GATES (Zero Tolerance)        │
│  • SBC-Adjusted True FCF: True FCF = CFO - Capex - Stock-Based Comp > 0        │
│  • True FCF Conversion: True FCF ÷ Net Income ≥ 70.0%                           │
│  • Share Cannibal Gate: 3-Year Diluted Shares CAGR ≤ 0.0% (Flat or Shrinking)   │
│  • Institutional Sponsorship: 60%–85% held by Tier-1 institutions               │
└──────────────────────────────────────┬──────────────────────────────────────────┘
                                       │ (Passes True FCF & Anti-Dilution)
                                       ▼
┌─────────────────────────────────────────────────────────────────────────────────┐
│         TIER 3: RETURN ON INVESTED CAPITAL (ROIC) & MOAT RESILIENCE             │
│  • ROIC on Invested Capital: ROIC = NOPAT ÷ Invested Capital ≥ 15% (5 Years)    │
│    (Invested Capital = Net Working Capital + Net PP&E; NOT Book Equity)         │
│  • Gross Margin Moat: Gross Margin ≥ 40.0% (confirms pricing power & switching) │
│  • Debt Fortress: Net Debt ÷ EBITDA ≤ 2.0x  ·  Interest Coverage ≥ 5.0x        │
│    (Handles negative book equity from share repurchases like AutoZone/Home Depot)│
└──────────────────────────────────────┬──────────────────────────────────────────┘
                                       │ (Passes Moat & Balance Sheet)
                                       ▼
┌─────────────────────────────────────────────────────────────────────────────────┐
│             TIER 4: VALUATION GUARDRAILS (Replacing Naive PEG)                  │
│  • True FCF Yield: True FCF ÷ Enterprise Value ≥ 2.5%                           │
│  • Forward EV/EBITDA: Below its 5-year historical median                        │
└─────────────────────────────────────────────────────────────────────────────────┘
```

---

### Two-Tranche Milestone Deployment Protocol (Anti-Cash Drag)
*Never buy 100% upfront; never wait indefinitely for market crashes.*
* **Tranche 1 (65% — ~$235–$310 USD):** Deployed immediately upon a stock passing all 4 Tiers and Investment Committee review.
* **Tranche 2 (35% — ~$125–$170 USD):** Deployed under EITHER path:
  * **Path A (Market Dip):** A **7%–12% broader market pullback** with company fundamentals intact.
  * **Path B (Earnings Verification):** If no dip occurs within 90 days, deploy Tranche 2 immediately following the company's next quarterly earnings report that verifies Revenue CAGR ≥ 10% and ROIC is holding.

---

### Multibagger US Sell Rules (Sell ONLY If)
* ❌ ROIC drops below 14% for two consecutive fiscal quarters.
* ❌ True FCF (after SBC) turns negative for two consecutive years.
* ❌ Structural technological obsolescence threatens the core business moat.
* ❌ Aggressive stock-based compensation dilutes share count (>2% per year).
* *(Never sell due to macro headlines, election news, or general market drawdowns).*

---

*Playbook v2.0 — Updated September 2026 (Institutional 4-Quadrant Architecture: India & US)*  
*Review and update this playbook monthly or after any significant capital/strategy changes.*

