# 📚 Lazy Lizard Agent — Documentation Index

> ⚠️ **HIGH-RISK DISCLAIMER**: Memecoins are highly speculative assets that can go to zero. This is not financial advice. Use at your own risk.

Welcome to the Lazy Lizard Agent documentation. Use the table below to navigate all guides.

---

## Documentation

| Document | Description |
|---|---|
| [DEPLOYMENT.md](DEPLOYMENT.md) | Full deployment guide: VPS, Docker, systemd service |
| [TELEGRAM-BOT.md](TELEGRAM-BOT.md) | Step-by-step Telegram bot setup |
| [PRE-BUY-STRATEGY.md](PRE-BUY-STRATEGY.md) | Veteran-wallet filtering & first-15-buyer scoring strategy |
| [AUDIT-CHECKLIST.md](AUDIT-CHECKLIST.md) | Pre-launch security audit checklist |
| [BONUS-OTHERS.md](BONUS-OTHERS.md) | x402 donations, ERC-8004 reputation, Diamond proxy, Virtuals Protocol |

---

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                      Lazy Lizard Agent                          │
│                                                                 │
│  pump.fun monitor ──► veteran filter ──► ERC-8004 score        │
│         │                                      │               │
│         ▼                                      ▼               │
│  Jupiter buy ◄────────── threshold? ──────── SKIP              │
│         │                                                       │
│         ▼                                                       │
│  price monitor ──► +5% TP ──► Jupiter sell ──► compound SOL   │
│         │                           │                          │
│         └──────────► x402 donate ◄──┘                          │
│                           │                                     │
│                    Telegram alert                               │
└─────────────────────────────────────────────────────────────────┘
```

---

## Quick Links

- 🌐 Website: [lazylizardagent.com](https://lazylizardagent.com)
- 🐙 GitHub: [github.com/0xloveavax/lazy-lizard-agent](https://github.com/0xloveavax/lazy-lizard-agent)
- ⚡ Jupiter: [jup.ag](https://jup.ag)
- 🚀 Virtuals Protocol: [virtuals.io](https://virtuals.io)
- 💸 x402: [x402.org](https://x402.org)
