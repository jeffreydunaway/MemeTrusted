# 🔐 Audit Checklist — Lazy Lizard Agent

> Complete this checklist before switching from `DRY_RUN=true` to `DRY_RUN=false`.

---

## Environment & Secrets

- [ ] `.env` is listed in `.gitignore` and confirmed not tracked by git
  ```bash
  git check-ignore -v .env   # should print: .gitignore:.env
  ```
- [ ] No private keys, API tokens, or wallet addresses are hardcoded in source files
- [ ] `.env.example` contains only placeholder values (no real secrets)
- [ ] `git log --all --full-history -- .env` shows no `.env` commits
- [ ] `git grep -r "SOLANA_PRIVATE_KEY=" -- "*.py"` returns no results

---

## Configuration Validation

- [ ] `DRY_RUN=true` tested successfully — agent starts, logs, and sends Telegram alert
- [ ] `TAKE_PROFIT_PCT` is set to a realistic value (e.g. 5.0)
- [ ] `MAX_POSITION_SOL` is sized appropriately for your risk tolerance
- [ ] `MIN_REPUTATION_SCORE` is set ≥ 60 for production
- [ ] `VETERAN_WALLET_MIN` ≥ 1
- [ ] Telegram bot token and chat ID tested with a manual message

---

## Dependencies

- [ ] All packages in `requirements.txt` are pinned to exact versions
- [ ] `pip install -r requirements.txt` completes without errors
- [ ] No known vulnerabilities in pinned versions (check via `pip audit`)
  ```bash
  pip install pip-audit && pip-audit -r requirements.txt
  ```
- [ ] Optional Solana packages (`solana`, `solders`) are pinned if uncommenting them

---

## Wallet & Funds

- [ ] Wallet holds enough SOL for intended position sizes + transaction fees
- [ ] Wallet is NOT the same as your main/cold storage wallet
- [ ] Wallet has been tested with a real but minimal transaction first
- [ ] Private key backup exists in a secure, offline location

---

## Networking & RPC

- [ ] RPC endpoint is accessible from deployment environment
- [ ] RPC rate limits won't throttle the polling interval
- [ ] Consider upgrading to a paid RPC provider (Helius, QuickNode, Triton) for production

---

## Jupiter Integration

- [ ] `get_quote()` tested manually for a known token pair
- [ ] Slippage `slippage_bps` reviewed (default 100 = 1%; increase for low-liquidity tokens)
- [ ] `buy_token()` tested in dry-run mode
- [ ] `sell_token()` tested in dry-run mode

---

## Telegram Alerts

- [ ] BUY alert format verified (correct token, amount, TX link)
- [ ] SELL alert format verified
- [ ] Daily summary verified
- [ ] Alert delivery latency is acceptable (< 5 seconds)

---

## x402 Donations

- [ ] `X402_DONATE_PCT` is set (0 to disable)
- [ ] Donation address/recipient confirmed
- [ ] x402 transaction tested in dry-run mode

---

## Deployment (Production Only)

- [ ] Agent runs as non-root user
- [ ] systemd service configured with `Restart=on-failure`
- [ ] Logs are being captured (`journalctl -u lazy-lizard -f`)
- [ ] Server firewall: only necessary ports open (no public RPC exposure)
- [ ] Server SSH hardened (key-only auth, no password login)

---

## Legal & Risk

- [ ] You have read and understood the risk disclaimer in README.md
- [ ] You are not operating in a jurisdiction where this activity is prohibited
- [ ] You acknowledge: memecoins can go to zero; never risk more than you can afford to lose

---

## Final Go/No-Go

| Check | Status |
|---|---|
| All environment checks pass | ☐ |
| Dependencies clean | ☐ |
| Dry-run tested for ≥ 1 hour | ☐ |
| Telegram alerts confirmed | ☐ |
| Risk acknowledged | ☐ |

When all rows are ✅ — you may switch `DRY_RUN=false`.
