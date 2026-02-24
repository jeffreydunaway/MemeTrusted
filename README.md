# 🦎 Lazy Lizard Agent

> **Lazy Solana 5% daily compounder — veteran-wallet filtered pump.fun tokens, auto 5% TP, x402 donations, on-chain via Virtuals Protocol**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://python.org)
[![Solana](https://img.shields.io/badge/chain-Solana-9945FF.svg)](https://solana.com)
[![Virtuals Protocol](https://img.shields.io/badge/via-Virtuals%20Protocol-00C2FF.svg)](https://virtuals.io)

---

> ⚠️ **HIGH-RISK DISCLAIMER**: This software interacts with memecoins on Solana. Memecoins are highly speculative assets that **can go to zero**. This is **not financial advice**. Never invest more than you can afford to lose entirely. Use at your own risk.

---

## What Is Lazy Lizard Agent?

**Lazy Lizard Agent** is an autonomous Solana trading agent that:

- 🔎 **Discovers** new tokens launched on [pump.fun](https://pump.fun) filtered by veteran-wallet signals
- 🧠 **Analyzes** first-15-buyer wallets for on-chain credibility scoring (ERC-8004 reputation)
- ⚡ **Auto-buys** qualifying tokens via [Jupiter Aggregator](https://jup.ag) for best-price execution
- 🎯 **Takes profit** automatically at **+5%** (configurable) and compounds gains
- 📬 **Alerts** you via Telegram on every buy, sell, and daily summary
- 💸 **Donates** a small % of profits via [x402](https://x402.org) to on-chain causes
- 🏛️ **Optionally** routes treasury funds through a Diamond proxy vault (EIP-2535)
- 🌐 **Runs 24/7** as a Virtuals Protocol agent at [lazylizardagent.com](https://lazylizardagent.com)

### Core Strategy

```
1. Monitor pump.fun for new token launches
2. Filter: only tokens where ≥1 veteran wallet is in the first 15 buyers
3. Score the first-15-buyer cohort (ERC-8004 on-chain reputation)
4. Auto-buy if score ≥ threshold (configurable)
5. Set TP at +5% (default) — sell via Jupiter
6. Compound SOL gains; repeat daily
7. Send Telegram alert after each trade + daily P&L summary
```

---

## Features

| Feature | Status |
|---|---|
| pump.fun token discovery | ✅ |
| Veteran-wallet signal filtering | ✅ |
| First-15-buyer analysis | ✅ |
| Jupiter auto-swap (buy + sell) | ✅ |
| 5% take-profit compounder | ✅ |
| Telegram alerts | ✅ |
| x402 micro-donations | ✅ |
| ERC-8004 reputation scoring | ✅ |
| Diamond proxy treasury (optional) | 🔧 Optional |
| Virtuals Protocol integration | ✅ |
| Streamlit dashboard | 🔜 Coming soon |

---

## Quick Start

### Prerequisites

- Python 3.10+
- Solana wallet (funded with SOL)
- Telegram bot token ([create via @BotFather](https://t.me/BotFather))
- Jupiter API access (free tier available)

### Installation

```bash
git clone https://github.com/0xloveavax/lazy-lizard-agent.git
cd lazy-lizard-agent
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your credentials (NEVER commit .env)
```

### Configuration

Edit `.env` with your values:

```env
SOLANA_PRIVATE_KEY=your_base58_private_key_here
TELEGRAM_BOT_TOKEN=your_telegram_bot_token
TELEGRAM_CHAT_ID=your_telegram_chat_id
TAKE_PROFIT_PCT=5.0
MIN_REPUTATION_SCORE=70
X402_DONATE_PCT=1.0
```

### Run

```bash
python main.py
```

---

## Project Structure

```
lazy-lizard-agent/
├── main.py                  # Core MemeCompounder class + CLI entry point
├── jupiter_auto.py          # Jupiter DEX buy/sell helpers
├── bot.py                   # Telegram alert sender
├── requirements.txt         # Pinned dependencies
├── .env.example             # Environment variable template (never commit .env)
├── .gitignore               # Python + secrets gitignore
├── CONTRIBUTING.md          # Contribution guidelines
├── SECURITY.md              # Responsible disclosure policy
├── CODE_OF_CONDUCT.md       # Contributor Covenant
└── docs/
    ├── README.md            # Extended documentation index
    ├── DEPLOYMENT.md        # Full deployment guide (VPS, Docker, systemd)
    ├── TELEGRAM-BOT.md      # Telegram bot setup walkthrough
    ├── PRE-BUY-STRATEGY.md  # Veteran-wallet & first-15 strategy deep-dive
    ├── AUDIT-CHECKLIST.md   # Pre-launch security audit checklist
    └── BONUS-OTHERS.md      # x402, ERC-8004, Diamond proxy, Virtuals notes
```

---

## Documentation

| Doc | Description |
|---|---|
| [docs/DEPLOYMENT.md](docs/DEPLOYMENT.md) | VPS / Docker / systemd deployment |
| [docs/TELEGRAM-BOT.md](docs/TELEGRAM-BOT.md) | Telegram bot setup |
| [docs/PRE-BUY-STRATEGY.md](docs/PRE-BUY-STRATEGY.md) | Signal & scoring strategy |
| [docs/AUDIT-CHECKLIST.md](docs/AUDIT-CHECKLIST.md) | Security audit checklist |
| [docs/BONUS-OTHERS.md](docs/BONUS-OTHERS.md) | x402 / ERC-8004 / Diamond / Virtuals |

---

## Security

- **Never** commit `.env`, private keys, or API tokens
- All wallet interactions use environment variables only
- See [SECURITY.md](SECURITY.md) for responsible disclosure

---

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). PRs welcome — use feature branches and reference issues.

---

## License

MIT — see [LICENSE](LICENSE).

---

## Topics

`solana` `memecoin` `trading-bot` `ai-agent` `pump-fun` `virtuals-protocol` `jupiter-swap` `x402` `erc-8004` `diamond-standard`