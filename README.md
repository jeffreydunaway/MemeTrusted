# 🦎 Lazy Lizard Agent

> **Lazy Solana 5% daily compounder — veteran-wallet filtered pump.fun tokens, auto 5% TP, x402 donations, on-chain via Virtuals Protocol**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/)
[![Solana](https://img.shields.io/badge/chain-Solana-9945FF.svg)](https://solana.com/)

---

> ⚠️ **HIGH RISK DISCLAIMER**: This software is for educational and experimental purposes only. Memecoins can go to zero. This is NOT financial advice. Never invest more than you can afford to lose entirely. The authors assume no responsibility for any financial losses incurred.

---

## What Is Lazy Lizard Agent?

Lazy Lizard Agent is an autonomous Solana memecoin compounder that:

1. **Monitors** pump.fun for new token launches
2. **Filters** by veteran-wallet signals and first-15-buyer analysis
3. **Buys** qualifying tokens automatically via Jupiter Aggregator
4. **Takes profit** at exactly 5% above entry (auto TP)
5. **Compounds** gains daily — lazy but consistent
6. **Donates** a micro-fee via x402 protocol to support open-source development
7. **Tracks reputation** on-chain using ERC-8004 agent reputation standard
8. **Alerts** you via Telegram on every buy, TP, and anomaly
9. **Optionally** manages a Diamond proxy treasury for upgradeable on-chain logic

---

## Features

| Feature | Description |
|---|---|
| 🔍 Veteran-Wallet Filter | Tracks wallets with proven >30-day on-chain history |
| 🥇 First-15-Buyer Analysis | Flags tokens where known alpha wallets are in the first 15 buyers |
| 📈 Auto 5% Take-Profit | Sells immediately at +5% — no greed, no bagholding |
| 🔄 Daily Compounding | Reinvests profits each cycle automatically |
| 💸 x402 Micro-Donations | Sends a tiny HTTP-402 payment per successful trade |
| 🏅 ERC-8004 Reputation | On-chain reputation scoring for the agent |
| 💎 Diamond Proxy Treasury | Optional upgradeable proxy for treasury management |
| 🪐 Jupiter Auto-Trade | Best-route swaps via Jupiter Aggregator API |
| 📲 Telegram Alerts | Real-time notifications on all agent actions |
| 🌐 lazylizardagent.com | Web presence and demo dashboard |

---

## Quick Start

### Prerequisites

- Python 3.10+
- Solana CLI + funded wallet
- Telegram Bot token (optional but recommended)
- RPC endpoint (Helius, QuickNode, or free public)

### Installation

```bash
git clone https://github.com/jeffreydunaway/lazy-lizard-agent.git
cd lazy-lizard-agent
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your keys
```

### Run

```bash
python main.py --mode monitor    # Monitor + analyze only (dry-run safe)
python main.py --mode trade      # Full autonomous trading mode
python main.py --mode report     # Print today's P&L summary
```

---

## Project Structure

```
lazy-lizard-agent/
├── main.py              # Core MemeCompounder class + CLI entry point
├── jupiter_auto.py      # Jupiter Aggregator buy/sell helpers
├── bot.py               # Telegram alert sender
├── requirements.txt     # Pinned dependencies
├── .env.example         # Environment variable template (never commit .env)
├── .gitignore           # Python + secrets exclusions
├── docs/
│   ├── README.md        # Extended documentation
│   ├── DEPLOYMENT.md    # Full deployment guide
│   ├── TELEGRAM-BOT.md  # Telegram bot setup guide
│   ├── PRE-BUY-STRATEGY.md  # Pre-buy signal strategy
│   ├── AUDIT-CHECKLIST.md   # Security audit checklist
│   └── BONUS-OTHERS.md      # Additional integrations & ideas
├── diamond/             # Optional Hardhat/Solidity Diamond proxy (future)
├── CONTRIBUTING.md      # Contribution guidelines
├── SECURITY.md          # Security policy & disclosure
└── CODE_OF_CONDUCT.md   # Community standards
```

---

## Environment Variables

See [`.env.example`](.env.example) for all required and optional configuration values. **Never commit your `.env` file.**

---

## Documentation

| Doc | Description |
|---|---|
| [Deployment Guide](docs/DEPLOYMENT.md) | Step-by-step deployment on VPS/cloud |
| [Telegram Bot Setup](docs/TELEGRAM-BOT.md) | Configure real-time alerts |
| [Pre-Buy Strategy](docs/PRE-BUY-STRATEGY.md) | Veteran-wallet & first-15 logic |
| [Audit Checklist](docs/AUDIT-CHECKLIST.md) | Security review before going live |
| [Bonus & Others](docs/BONUS-OTHERS.md) | x402, ERC-8004, Diamond, Virtuals |

---

## Topics

`solana` `memecoin` `trading-bot` `ai-agent` `pump-fun` `virtuals-protocol` `jupiter-swap` `x402` `erc-8004` `diamond-standard`

---

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). Use feature branches, draft PRs, and reference issues.

---

## Security

See [SECURITY.md](SECURITY.md) for responsible disclosure instructions. **Never share private keys or `.env` contents.**

---

## License

[MIT](LICENSE) © 2026 Lazy Lizard Agent Contributors