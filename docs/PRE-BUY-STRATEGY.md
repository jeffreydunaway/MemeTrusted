# Pre-Buy Strategy — Lazy Lizard Agent

> ⚠️ **HIGH RISK DISCLAIMER**: Memecoins can go to zero. Not financial advice.  
> Signal filters reduce but do NOT eliminate risk.

---

## Overview

Lazy Lizard Agent uses two complementary signals to filter pump.fun token launches
before committing any capital:

1. **Veteran-Wallet Signal** — tracks wallets with a proven on-chain track record
2. **First-15-Buyer Analysis** — flags tokens where known alpha wallets are among the first 15 buyers

Only tokens that pass **both** filters are considered for a buy.

---

## Signal 1: Veteran-Wallet Filter

### Definition

A "veteran wallet" is a Solana wallet that satisfies ALL of the following:

| Criterion | Threshold |
|---|---|
| On-chain age | ≥ 30 days since first transaction |
| Total transactions | ≥ 500 lifetime txns |
| Previous memecoin trades | ≥ 10 pump.fun interactions |
| Win rate (historical) | ≥ 40% profitable exits |
| No rug-pull associations | Not linked to known rug wallets |

### Implementation Notes

- Maintain a local or Redis-cached list of known veteran wallet addresses.
- Refresh the list periodically (e.g., daily) from on-chain data.
- Use the Helius or Solscan API to fetch wallet transaction history.
- New wallets (< 30 days) are never counted as veterans, regardless of activity.

### Scoring

Each veteran wallet found in the first-N buyers adds **+10 points** to the signal score.

---

## Signal 2: First-15-Buyer Analysis

### Definition

Analyse the first 15 wallet addresses that buy a newly launched pump.fun token.

### Why First 15?

- The earliest buyers have the most information advantage.
- Veteran wallets appearing in the first 15 strongly suggest insider or alpha knowledge.
- Beyond 15, the signal degrades as retail buyers dilute the signal.

### Scoring

Each of the first 15 buyers that is a veteran wallet adds +10 points (via veteran filter).  
Each first-15 buyer (veteran or not) also adds **+0.5 points** as a raw activity bonus.

### Maximum Score Example

- 3 veteran wallets in first 15 → 3 × 10 + 15 × 0.5 = **37.5 points**

---

## Buy Decision Logic

```python
qualifies = (
    signal.veteran_buyer_count >= MIN_VETERAN_WALLETS  # default: 2
    and signal.score > 0
)
```

Tune `MIN_VETERAN_WALLETS` and `FIRST_N_BUYERS` in `.env` based on your risk appetite:

| Setting | Conservative | Default | Aggressive |
|---|---|---|---|
| `MIN_VETERAN_WALLETS` | 3 | 2 | 1 |
| `FIRST_N_BUYERS` | 10 | 15 | 20 |

---

## Blacklist / Exclusion Criteria

Tokens are **automatically excluded** if:

- The deployer wallet is on a known rug-pull blacklist
- Liquidity is below a minimum threshold
- Token age is > 5 minutes (missed the early window)
- The token symbol contains known scam patterns

---

## Take-Profit Strategy

Once a qualifying token is bought, the exit is strict and automatic:

- **Take-profit**: +5% above entry price (default, configurable via `TAKE_PROFIT_PCT`)
- **No stop-loss by default** — position is held until TP or manual intervention
- Consider adding a time-based stop (e.g., auto-sell after 10 minutes) in future versions

> 🧠 The laziness is the strategy: take 5%, move on, repeat.
