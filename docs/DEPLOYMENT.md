# Deployment Guide — Lazy Lizard Agent

> ⚠️ **HIGH RISK DISCLAIMER**: Memecoins can go to zero. Not financial advice.  
> Use a dedicated hot wallet funded with only what you can afford to lose entirely.

---

## Prerequisites

| Requirement | Notes |
|---|---|
| Ubuntu 22.04 VPS (1 CPU / 1 GB RAM min) | DigitalOcean, Hetzner, Contabo, etc. |
| Python 3.10+ | `python3 --version` |
| `pip` + `venv` | `python3 -m pip install --upgrade pip` |
| Funded Solana wallet | Dedicated hot wallet only |
| Helius or QuickNode RPC | Public endpoint is rate-limited |
| Telegram bot (optional) | For real-time alerts |

---

## Step 1 — Clone & Install

```bash
git clone https://github.com/jeffreydunaway/lazy-lizard-agent.git
cd lazy-lizard-agent
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

---

## Step 2 — Configure Environment

```bash
cp .env.example .env
nano .env   # or use your preferred editor
```

**Minimum required values:**

```dotenv
SOLANA_RPC_ENDPOINT=https://rpc.helius.xyz/?api-key=YOUR_KEY
WALLET_PRIVATE_KEY=YOUR_BASE58_PRIVATE_KEY
DRY_RUN=true   # Set to false only when ready for live trading
```

> 🔒 **Security**: Set file permissions so only your user can read `.env`:
> ```bash
> chmod 600 .env
> ```

---

## Step 3 — Dry-Run Test

```bash
python main.py --mode monitor
```

Expected output:
```
2026-01-01T00:00:00Z [INFO] lazy-lizard: DRY_RUN mode enabled — no real trades will be executed.
2026-01-01T00:00:00Z [INFO] lazy-lizard: Starting monitor loop (interval=30s) …
2026-01-01T00:00:00Z [INFO] lazy-lizard: Discovering new tokens from pump.fun …
```

---

## Step 4 — Run as a systemd Service

Create `/etc/systemd/system/lazy-lizard.service`:

```ini
[Unit]
Description=Lazy Lizard Agent
After=network.target

[Service]
User=ubuntu
WorkingDirectory=/home/ubuntu/lazy-lizard-agent
EnvironmentFile=/home/ubuntu/lazy-lizard-agent/.env
ExecStart=/home/ubuntu/lazy-lizard-agent/.venv/bin/python main.py --mode trade
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl daemon-reload
sudo systemctl enable lazy-lizard
sudo systemctl start lazy-lizard
sudo journalctl -fu lazy-lizard
```

---

## Step 5 — Enable Live Trading

When you are satisfied with dry-run behaviour:

```bash
# Edit .env
DRY_RUN=false
```

```bash
sudo systemctl restart lazy-lizard
```

---

## Monitoring

```bash
# View live logs
sudo journalctl -fu lazy-lizard

# View today's P&L
source .venv/bin/activate && python main.py --mode report
```

---

## Updating

```bash
cd lazy-lizard-agent
git pull origin main
source .venv/bin/activate
pip install -r requirements.txt
sudo systemctl restart lazy-lizard
```

---

## Security Reminders

- Use a dedicated wallet — never your main wallet
- Fund only what you can lose entirely
- Enable SSH key-only login on your VPS
- Keep `.env` permissions at `600`
- Rotate RPC API keys periodically
- Review all code before going live
