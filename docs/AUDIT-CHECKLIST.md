# Security Audit Checklist — Lazy Lizard Agent

Use this checklist before deploying to a production environment with real funds.

---

## ☐ Wallet Security

- [ ] Using a **dedicated hot wallet** — never your main wallet
- [ ] Hot wallet funded with only the amount you can afford to lose entirely
- [ ] Private key is **only in `.env`** — never hardcoded, never logged
- [ ] `.env` file permissions set to `600` (`chmod 600 .env`)
- [ ] `.env` is listed in `.gitignore` and has never been committed
- [ ] No wallet address or private key appears in any log output
- [ ] RPC endpoint API key is rotated if exposed

---

## ☐ Code Review

- [ ] Reviewed `main.py` — no hardcoded secrets, no exposed keys
- [ ] Reviewed `jupiter_auto.py` — swap logic is correct, slippage is reasonable
- [ ] Reviewed `bot.py` — Telegram token not logged or printed
- [ ] All `import` statements use trusted, pinned packages
- [ ] No `eval()`, `exec()`, or dynamic code execution
- [ ] No shell injection via `subprocess` with user-controlled input
- [ ] Exception handlers do not re-raise secrets in error messages

---

## ☐ Dependency Security

- [ ] All dependencies pinned to exact versions in `requirements.txt`
- [ ] Run `pip audit` to check for known vulnerabilities:
  ```bash
  pip install pip-audit
  pip-audit -r requirements.txt
  ```
- [ ] No development-only packages in production `requirements.txt`

---

## ☐ Network & RPC Security

- [ ] Using HTTPS-only RPC endpoints
- [ ] RPC API key is stored in `.env`, not in source code
- [ ] Rate limiting is handled gracefully (no infinite retry loops)
- [ ] All external HTTP calls use `timeout=` parameter
- [ ] Telegram bot token validated via `getMe` before going live

---

## ☐ Trading Logic

- [ ] `DRY_RUN=true` tested extensively before switching to `false`
- [ ] Take-profit percentage is intentional and understood
- [ ] Position size is within your risk tolerance
- [ ] Slippage tolerance is set appropriately for memecoin liquidity
- [ ] Signal filters (`MIN_VETERAN_WALLETS`, `FIRST_N_BUYERS`) tuned for your strategy
- [ ] Blacklist of rug-pull wallets/tokens is up to date

---

## ☐ Infrastructure Security

- [ ] VPS has SSH key-only login (password login disabled)
- [ ] VPS firewall only exposes necessary ports
- [ ] `systemd` service runs as a non-root user
- [ ] Logs do not contain secrets or private key material
- [ ] Log rotation is configured to prevent disk exhaustion

---

## ☐ Open-Source / Repository Security

- [ ] Repository has no `.env` file in git history
  ```bash
  git log --all --full-history -- .env
  ```
- [ ] No private keys, tokens, or secrets in any commit
- [ ] `SECURITY.md` is present with responsible disclosure instructions
- [ ] Branch protection rules enabled on `main`
- [ ] No unreviewed dependencies added via PRs

---

## ☐ Risk Disclaimers

- [ ] README contains high-risk disclaimer
- [ ] All documentation notes "not financial advice"
- [ ] You understand memecoins can go to zero
- [ ] You have tested with minimal funds before scaling

---

## Post-Audit Sign-Off

Date: _______________  
Reviewer: _______________  
Notes: _______________
