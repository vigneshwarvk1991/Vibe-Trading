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
  ACTIVE TRADING CAPITAL              INVESTING CAPITAL
  ₹5,00,000                           Separate (Unlimited)
  ─────────────────────               ─────────────────────
  • 100% allocated to                 • Multibagger portfolio
    positional momentum               • Hold 1–3+ years
  • 5 Slots × ₹1,00,000              • 5+ stocks × flexible sizing
  • Hold 30–90 days                   • No stop-loss
  • Strict stop-loss & trail          • Sell only on business
  • Target: 25–40% CAGR                deterioration
```

> **Rule:** Trading capital and investing capital are NEVER mixed. Trading profits stay in trading. Investing capital is separate long-term wealth building.

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
1. ✅ Stock price is **above the 200-day EMA** (confirms macro uptrend).
2. ✅ The **200-day EMA is sloping upward** (not flat or declining).
3. ✅ Daily Close prints a **new 20-day High** (breakout trigger).

### Exit Rules (Any One Triggers Exit)
1. 🛑 **Initial Stop-Loss:** 5.0% below entry price (set as GTT immediately on entry).
2. 📈 **Trailing Stop (ATR):** Close drops below **2.5× ATR(14)** from swing peak high.
3. 📉 **Trailing Stop (Donchian):** Close drops below the **20-day Low**.
4. ⏰ Whichever trailing stop is hit first triggers the exit.

### Position Sizing
| Parameter | Calculation |
|:---|:---|
| **Capital per Slot** | ₹1,00,000 (20% of ₹5L per slot) |
| **Max Concurrent Positions** | 5 stocks |
| **Shares to Buy** | ₹1,00,000 ÷ Stock Price (round down) |
| **Max Risk per Trade** | ₹5,000 (1% of total capital) |

### Universe Selection: 100% Dynamic Nifty 100 Index Protocol
**Zero Hardcoded Stocks.** The system scans the entire **NIFTY 100 Index universe (NSE India)** dynamically every trading session. 

Any Nifty 100 stock that meets the 3-Step Mathematical Rule (Price > 200 EMA + Positive 200 EMA Slope + Fresh 20-Day High Breakout) is eligible for entry regardless of sector.

* **Universe Scope:** Top 100 large-cap & high-liquidity stocks on the National Stock Exchange (NSE).
* **Liquidity Gate:** Average Daily Volume > 500,000 shares / Turnover > ₹50 Cr daily (eliminates illiquidity & circuit traps).
* **Sector Neutrality:** Maximum 2 positions from the same sector to maintain portfolio diversification across your 5 slots.

### Portfolio Tracker Template

| Slot | Stock | Entry Date | Entry Price | Shares | Stop-Loss | Trail Stop | Status |
|:---|:---|:---|:---|:---|:---|:---|:---|
| 1 | TITAN.NS | 27-Aug-2026 | ₹5,139.30 | 19 | ₹4,882.35 | ₹4,978.31 | 🟢 ACTIVE |
| 2 | — | — | — | — | — | — | 💰 CASH |
| 3 | — | — | — | — | — | — | 💰 CASH |
| 4 | — | — | — | — | — | — | 💰 CASH |
| 5 | — | — | — | — | — | — | 💰 CASH |

---

## 3. TRACK 2 — Multibagger Investing Framework

### The 5 Pillars (ALL Must Be True)

| # | Pillar | Threshold | Why It Matters |
|:---|:---|:---|:---|
| 1 | **ROCE** | > 20% for 5 consecutive years | Business earns extraordinary returns on capital |
| 2 | **Revenue Growth** | > 15% CAGR over 5 years | Structural market expansion |
| 3 | **Debt-to-Equity** | < 0.5 (ideally debt-free) | Survives downturns without bankruptcy risk |
| 4 | **Promoter Holding** | > 50%, increasing, no pledge | Management's wealth is tied to yours |
| 5 | **PEG Ratio** | < 1.5 | Not overpaying for growth |

### Multibagger Sell Rules (ONLY Sell If)
- ❌ ROCE drops below 15% for 2 consecutive years.
- ❌ Management pledges shares or dilutes equity aggressively.
- ❌ Revenue growth declines to < 10% for 2 consecutive years.
- ❌ A structural disruption threatens the core business model.
- ❌ Forensic accounting red flags (cash flow diverging from reported profits).

### Multibagger Buy Rules
- ✅ Stock passes all 5 Pillars.
- ✅ Investment Committee Swarm gives a Buy verdict.
- ✅ Investor Lens score > 70/100.
- ✅ Buy in tranches: 50% at first entry, 25% on a 10% dip, 25% on a 20% dip.
- ✅ **Add on dips** when fundamentals are intact (the opposite of panic selling).

---

## 4. MASTER PROMPT LIBRARY

> **Important:** Always click **`+` (New Session)** before running any prompt to minimize token usage and prevent context confusion.

---

### 4A. DAILY MOMENTUM SCAN (Track 1)
*Run every weekday between 4:00 PM – 8:00 PM IST*

```text
Run our Positional Trend & Breakout Market Scan for Indian Equities as of today's close on:
BHARTIARTL.NS, M&M.NS, SUNPHARMA.NS, ICICIBANK.NS, TRENT.NS, BEL.NS, HAL.NS, TITAN.NS.

My Current Portfolio Holdings:
- Slot 1: [STOCK] ([SHARES] shares bought @ ₹[PRICE])
- Slot 2: [STOCK or CASH] (₹[AMOUNT] available)
- Slot 3: [STOCK or CASH] (₹[AMOUNT] available)
- Slot 4: [STOCK or CASH] (₹[AMOUNT] available)
- Slot 5: [STOCK or CASH] (₹[AMOUNT] available)

Please calculate:
1. NEW ENTRY CHECK: Did any watchlist stock close at a fresh 20-day High today while trading above their 200-day EMA? If yes, calculate the exact quantity to buy for my ₹1,00,000 slot and the 5% initial stop-loss.
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
Screen the Nifty Midcap 150 and Nifty Smallcap 250 universe for potential multibagger candidates:

1. ROCE > 20% for each of the last 5 years.
2. Revenue CAGR > 15% over the last 5 years.
3. PAT CAGR > 18% over the last 5 years.
4. Debt-to-Equity Ratio < 0.5 (prefer debt-free).
5. Promoter Holding > 50% with no pledge.
6. Free Cash Flow positive for at least 4 of the last 5 years.
7. PEG Ratio < 1.5.

Rank survivors by composite score of ROCE + Revenue Growth + FCF Yield. Show the top 10 with all key metrics.
```

---

### 4D. DEEP COMPANY ANALYSIS (Track 2)
*Run on each multibagger candidate before investing*

```text
Run a comprehensive institutional equity research analysis on [TICKER.NS]:

1. Business Model: What does the company do? What is the competitive moat?
2. Financial Quality (5-Year Trends): Revenue, EBITDA, PAT, ROCE, ROE, FCF, Debt/Equity.
3. Management Quality: Promoter holding trend, insider transactions, capital allocation track record, dividend history.
4. Growth Runway: Total addressable market? Current market share? Realistic growth ceiling?
5. Valuation: Current P/E, PEG, EV/EBITDA vs 5-year median. Fair value estimate.
6. Risks & Kill Criteria: What could go wrong? At what point should I exit?
7. Verdict: Buy, Hold, or Avoid at current price? If Buy, what is a good entry zone?
```

---

### 4E. INVESTMENT COMMITTEE SWARM (Track 2)
*Run before committing capital to any multibagger*

```text
Run the investment_committee swarm on [TICKER.NS] at current market price.

The Bull Analyst should argue why this stock can 3x–5x over 3 years.
The Bear Analyst should argue why this stock could underperform or decline.
The Risk Manager should identify key risks and position sizing.
The Portfolio Manager should give the final verdict: Buy, Avoid, or Wait for better price.
```

---

### 4F. INVESTOR LENS ANALYSIS (Track 2)

```text
Analyze [TICKER.NS] through the investment frameworks of:
1. Warren Buffett: Durable competitive moat? ROCE > cost of capital?
2. Peter Lynch: PEG ratio? Is this a "stalwart", "fast grower", or "turnaround"?
3. Philip Fisher: Does management reinvest wisely? Innovation strength?
4. Joel Greenblatt: Magic Formula rank (earnings yield + ROIC)?

Give a consolidated score (0 to 100) and final Buy/Avoid verdict.
```

---

### 4G. QUARTERLY EARNINGS REVIEW (Track 2)
*Run after each quarterly result on every multibagger holding*

```text
Review the latest quarterly results for [TICKER.NS]:
1. Did Revenue grow > 15% YoY? Did PAT grow > 18% YoY?
2. Did ROCE stay above 20%? Did margins expand or contract?
3. Any change in promoter holding or share pledging?
4. Any management commentary on growth guidance or capex?
5. VERDICT: Are the 5 multibagger pillars still intact? Continue holding or reassess?
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
                 → Add to multibagger portfolio if all 5 Pillars pass
```

### Quarterly (After Earnings Season — Jan, Apr, Jul, Oct)
```
[ Post Results ] Run Prompt 4G (Quarterly Review) on EACH multibagger holding
                 → Confirm 5 Pillars intact → Hold
                 → If deteriorating → Run Investment Committee Swarm → Decide

[ Post Results ] Run Prompt 4J (Shadow Account Audit) on past quarter's trades
                 → Identify and eliminate behavioral mistakes
```

---

## 6. RISK MANAGEMENT RULEBOOK

### Active Trading (Track 1) — Iron Rules

| Rule | Description | Why |
|:---|:---|:---|
| **1% Rule** | Max loss per trade = 1% of total capital (₹5,000) | Survives 20 consecutive losses |
| **5% Stop-Loss** | Every position gets a 5% stop-loss GTT on day of entry | No exceptions. No "hoping" |
| **Stops Only Move UP** | Trailing stops are only adjusted upward, never downward | Locks in profits systematically |
| **Max 5 Positions** | Never hold more than 5 active trades simultaneously | Prevents over-diversification |
| **No Averaging Down** | NEVER add to a losing active trade | Averaging down = compounding mistakes |
| **Drawdown Circuit Breaker** | If portfolio drops -15%, reduce slot size to ₹50,000 for 4 weeks | Capital preservation during bad regimes |
| **No Trading During News** | Skip entries on Budget Day, RBI Policy, Election Results | Gap risk destroys stop-losses |

### Multibagger Investing (Track 2) — Patience Rules

| Rule | Description |
|:---|:---|
| **No Stop-Loss** | Multibaggers can drop 30–50% before going up 500%. TRENT fell -45% in COVID then went +900%. |
| **Minimum 1-Year Hold** | Do not evaluate multibaggers on weekly or monthly timeframes. |
| **Buy in Tranches** | 50% initial, 25% on 10% dip, 25% on 20% dip (if fundamentals intact). |
| **Sell Only on Business Failure** | Not on price drops. Only when the 5 Pillars break. |
| **Quarterly Review Only** | Check fundamentals after earnings. Not daily. |

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
cd "/Users/nemo/Documents/Vibe Trading/Vibe-Trading"
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
| **Month 1–2** | Trade with full ₹5L. Learn execution rhythm. |
| **After 3 months of consistent profit** | Add ₹2.5L → ₹7.5L (increase to 5 slots × ₹1.5L) |
| **After 6 months with Sharpe > 1.0** | Add ₹2.5L → ₹10L (5 slots × ₹2L) |
| **After 12 months of audited track record** | Consider adding options (Engine 2) and crypto (Engine 3) |

### When to Scale Down
| Trigger | Action |
|:---|:---|
| **3 consecutive stop-outs** | Pause new entries for 1 week. Review with Shadow Account. |
| **Portfolio drawdown > -15%** | Cut slot size to ₹50,000 for 4 weeks. |
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
| **Drawdown** | Peak-to-trough decline in portfolio value. -24% means your ₹5L temporarily dropped to ₹3.8L |
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
| **Total US Trading Capital** | Configurable (e.g., $2,500 – $5,000 USD) |
| **Number of Slots** | 5 to 10 Slots (e.g., $500 per slot) |
| **Fractional Shares Advantage** | Supported! $\text{Shares} = \frac{\text{Slot Capital}}{\text{Stock Price}}$ (up to 3 decimal places) |
| **Initial Stop-Loss** | **5.0% below buy price** (GTC Stop order in IBKR) |
| **Trailing Stop (ATR)** | Daily Close drops below **2.5× ATR(14)** from peak close |
| **+10% Profit Milestone Rule** | At +10% gain, move GTC Stop to Breakeven (Entry Price) or take 50% partial profit |

---

### Universe Selection: Dynamic S&P 500 & Nasdaq 100 Protocol
1. **Universe Scope**: Top 100 liquid constituents of the S&P 500 and Nasdaq 100.
2. **Liquidity Gate**: Average Daily Volume > 1,000,000 shares (zero liquidity/slippage drag).
3. **Sector Diversification**: Maximum 2 concurrent positions from the same GICS sector.

---

### Operating Schedule (Indian Standard Time - IST)
* **US Market Hours**: 9:30 AM – 4:00 PM EST (**7:00 PM – 1:30 AM IST**).
* **Daily Scan Window**: Run morning at **7:00 AM – 8:00 AM IST** (post-US market close) or late night at **1:45 AM IST**.
* **Order Execution Window**: Place GTC (Good-Til-Cancelled) orders in IBKR anytime during the day before the 7:00 PM IST US market open.

---

### Google Sheet Routing
* **`US_Tradebook`**: Active open US stock positions (Date, Symbol, Qty, Entry Price in USD, Total USD, Stop Loss, Status).
* **`US_to_buy`**: Action orders generated by the morning scan (Action, Symbol, Qty, Limit Buy, Initial Stop Loss).

---

### Master US Prompt Library (Track 1 Momentum)

#### 11A. DAILY US MOMENTUM SCAN
*Run every weekday morning between 7:00 AM – 8:00 AM IST (or 1:45 AM IST)*

```text
Run our US Positional Momentum Market Scan across the S&P 500 and Nasdaq 100 universe as of yesterday's US market close:

My Current US Portfolio Holdings:
- Slot 1: [SYMBOL] ([SHARES] shares @ $[PRICE])
- Slot 2: [SYMBOL or CASH] ($[AMOUNT] available)
- Slot 3: [SYMBOL or CASH] ($[AMOUNT] available)
- Slot 4: [SYMBOL or CASH] ($[AMOUNT] available)
- Slot 5: [SYMBOL or CASH] ($[AMOUNT] available)

Please calculate:
1. NEW ENTRY CHECK: Did any S&P 500 / Nasdaq 100 stock close at a fresh 20-day High while trading above its rising 200-day EMA? If yes, calculate exact fractional quantity for my $[SLOT_SIZE] slot and the 5% initial stop-loss.
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

*(Note: US Multibagger Fundamental Investing [Track 2] is reserved for future expansion).*

---

*Playbook v1.1 — Updated September 2026 (Added Section 11: US Equities Momentum)*  
*Review and update this playbook monthly or after any significant strategy change.*

