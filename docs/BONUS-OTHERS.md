# 🎁 Bonus — x402, ERC-8004, Diamond Proxy & Virtuals Protocol

> ⚠️ **HIGH-RISK DISCLAIMER**: Not financial advice. Experimental protocols. Use at your own risk.

This document covers the advanced integrations in Lazy Lizard Agent.

---

## 💸 x402 — Micro-Donations

### What is x402?

[x402](https://x402.org) is an HTTP-402-inspired protocol for on-chain micro-payments and donations. Lazy Lizard Agent uses it to automatically donate a configurable percentage of trading profits to designated on-chain causes.

### Configuration

```env
X402_DONATE_PCT=1.0   # donate 1% of each trade's profit
```

### How it works

1. After a successful take-profit sell, compute `profit_sol = sell_proceeds - buy_cost`
2. `donation = profit_sol × X402_DONATE_PCT / 100`
3. Submit a Solana transaction to the x402 donation endpoint
4. Include donation amount in the daily Telegram summary

### Implementation status

> 🔧 The `donate_x402()` method in `main.py` has a TODO placeholder.
> Contribution welcome — see [CONTRIBUTING.md](../CONTRIBUTING.md).

---

## ⭐ ERC-8004 — On-Chain Reputation

### What is ERC-8004?

ERC-8004 is a proposed on-chain reputation standard that scores wallet addresses based on their historical behaviour, transaction patterns, and participation in known events.

### How Lazy Lizard Agent uses it

The `score_cohort()` method in `main.py` queries the ERC-8004 registry for each wallet in a token's first-15-buyer cohort and computes an aggregate credibility score (0–100).

Only tokens whose cohort score meets `MIN_REPUTATION_SCORE` are purchased.

### Implementation status

> 🔧 The `score_cohort()` method has a TODO placeholder.
> The ERC-8004 standard is still evolving; implementation depends on available registry endpoints.

---

## 🏛️ Diamond Proxy Treasury (Optional)

### What is the Diamond Standard?

[EIP-2535 Diamond Standard](https://eips.ethereum.org/EIPS/eip-2535) enables modular smart contracts ("diamonds") composed of multiple "facets" (implementation contracts). This allows upgradeable, gas-efficient treasury management.

### Use case in Lazy Lizard Agent

Optionally, accumulated SOL profits can be routed to a Diamond proxy vault on an EVM-compatible chain (e.g. via a bridge), enabling:
- Multi-sig treasury management
- Upgradeable profit-sharing logic
- On-chain governance

### diamond/ folder

The `diamond/` folder is reserved for Hardhat-based Solidity contracts.

```
diamond/
├── contracts/
│   ├── Diamond.sol
│   ├── facets/
│   │   ├── TreasuryFacet.sol
│   │   └── GovernanceFacet.sol
│   └── interfaces/
├── scripts/
│   └── deploy.js
├── test/
├── hardhat.config.js
└── package.json
```

### Setup (when ready)

```bash
cd diamond
npm install
npx hardhat compile
npx hardhat test
npx hardhat run scripts/deploy.js --network mainnet
```

> ⚠️ The `diamond/` folder is optional and not included in the initial commit.
> Only add it when you are ready to work with Solidity contracts.

---

## 🌐 Virtuals Protocol

### What is Virtuals Protocol?

[Virtuals Protocol](https://virtuals.io) is a platform for deploying and monetising autonomous AI agents on-chain.

### Lazy Lizard Agent on Virtuals

Lazy Lizard Agent is designed to run as a Virtuals Protocol agent, enabling:
- On-chain agent identity and reputation
- $LAZY token integration for agent governance
- Agent revenue sharing with $LAZY holders
- Discovery via the Virtuals Protocol marketplace

### Integration notes

- The agent's wallet acts as its on-chain identity
- Virtuals Protocol SDK integration is planned as a future enhancement
- Visit [lazylizardagent.com](https://lazylizardagent.com) for the live agent page

---

## 🚀 Roadmap

| Feature | Status |
|---|---|
| x402 micro-donations | 🔧 Placeholder — contributions welcome |
| ERC-8004 cohort scoring | 🔧 Placeholder — depends on registry availability |
| Diamond proxy treasury | 🔜 Optional future module |
| Virtuals Protocol SDK | 🔜 Planned |
| Streamlit dashboard | 🔜 Coming soon |
| $LAZY token pre-buy | 🔜 Pre-launch phase |
| Backtesting module | 🔜 Planned |
