# 🧠 Pre-Buy Strategy — Lazy Lizard Agent

> ⚠️ **HIGH-RISK DISCLAIMER**: Memecoins are highly speculative. Past performance does not guarantee future results. Not financial advice.

This document explains the signal logic Lazy Lizard Agent uses to decide which pump.fun tokens to buy.

---

## Overview

The strategy combines two complementary signals:

1. **Veteran-wallet filtering** — Is a known "smart money" wallet in the first 15 buyers?
2. **ERC-8004 reputation scoring** — What is the on-chain credibility score of the first-15 cohort?

Both filters must pass before a buy is triggered.

---

## Signal 1 — Veteran-Wallet Filter

### What are veteran wallets?

"Veteran wallets" are Solana addresses with a track record of:
- Early entry into tokens that 10×+ within 24 hours
- Low rug-pull participation history
- Consistent profitable exits

You maintain a curated list of such wallets in a local file (e.g. `veteran_wallets.txt`).

### How the filter works

```
first_buyers = first 15 wallet addresses that bought the token on pump.fun
veteran_count = count of first_buyers that appear in your veteran wallets list

if veteran_count >= VETERAN_WALLET_MIN:
    → pass to ERC-8004 scoring
else:
    → SKIP
```

Default: `VETERAN_WALLET_MIN=1` (at least 1 veteran wallet in the first 15).

### Building your veteran wallet list

Sources to find high-quality veteran wallets:
- On-chain analytics: [Birdeye](https://birdeye.so), [Solscan](https://solscan.io)
- Alpha communities: Telegram / Discord groups tracking smart-money
- Manual backtesting: run `--dry-run` and log which wallets consistently precede winners

> ⚠️ Veteran wallets are a signal, not a guarantee. Wallets can change behavior or be imitated.

---

## Signal 2 — ERC-8004 Reputation Scoring

### What is ERC-8004?

ERC-8004 is an on-chain reputation standard that assigns credibility scores to wallet addresses based on their historical behavior.

### How the score is calculated

The agent fetches the ERC-8004 score for each wallet in the first-15-buyer cohort and computes an aggregate:

```python
cohort_score = average(erc8004_score(wallet) for wallet in first_15_buyers)
```

Score range: **0–100**

| Score | Interpretation |
|---|---|
| 80–100 | High-credibility cohort — strong signal |
| 60–79 | Moderate credibility — proceed with caution |
| 40–59 | Low credibility — likely skip |
| 0–39 | Poor credibility — SKIP |

Default threshold: `MIN_REPUTATION_SCORE=70`

---

## Combined Decision Logic

```
token → veteran filter → ERC-8004 score → buy?
                ↓                  ↓
            SKIP               score < threshold → SKIP
                                   ↓
                              score ≥ threshold → BUY via Jupiter
```

---

## Take-Profit Logic

After buying:

1. Agent monitors token price (via Jupiter quote API)
2. When price ≥ `buy_price × (1 + TAKE_PROFIT_PCT / 100)`:
   - Sell full position via Jupiter
   - Log profit in SOL
   - Donate `X402_DONATE_PCT`% via x402
   - Send Telegram SELL alert
   - Compound: available SOL = original + profit

Default: `TAKE_PROFIT_PCT=5.0` (sell at +5%)

---

## Tuning Parameters

| Parameter | Conservative | Balanced | Aggressive |
|---|---|---|---|
| `VETERAN_WALLET_MIN` | 2 | 1 | 1 |
| `MIN_REPUTATION_SCORE` | 80 | 70 | 50 |
| `TAKE_PROFIT_PCT` | 10.0 | 5.0 | 3.0 |
| `MAX_POSITION_SOL` | 0.05 | 0.1 | 0.25 |

> Always start with `DRY_RUN=true` to validate your configuration before using real SOL.

---

## Backtesting

Currently, the agent runs forward in production only. A backtesting module is planned. Contributions welcome — see [CONTRIBUTING.md](../CONTRIBUTING.md).
