# 🚀 Deployment Guide — Lazy Lizard Agent

> ⚠️ **HIGH-RISK DISCLAIMER**: This software interacts with memecoins. Not financial advice. Use at your own risk.

This guide covers deploying Lazy Lizard Agent on:
- [Local machine](#local-development)
- [VPS / Ubuntu server](#vps-ubuntu)
- [Docker](#docker)
- [systemd service](#systemd-service)

---

## Prerequisites

| Requirement | Version |
|---|---|
| Python | 3.10+ |
| pip | 22+ |
| SOL wallet | Funded (at least 0.5 SOL recommended) |
| Telegram bot token | From @BotFather |

---

## Local Development

```bash
git clone https://github.com/0xloveavax/lazy-lizard-agent.git
cd lazy-lizard-agent

# Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate        # Linux / macOS
# .venv\Scripts\activate         # Windows

pip install -r requirements.txt

cp .env.example .env
# Edit .env — fill in your SOLANA_PRIVATE_KEY, TELEGRAM_BOT_TOKEN, etc.

# Always start with DRY_RUN=true to verify configuration
python main.py --dry-run
```

---

## VPS / Ubuntu

### 1. Provision server

Recommended specs: 1 vCPU, 1 GB RAM, Ubuntu 22.04 LTS.
Providers: DigitalOcean, Hetzner, Vultr, Linode.

### 2. Install Python

```bash
sudo apt update && sudo apt upgrade -y
sudo apt install -y python3.11 python3.11-venv python3-pip git
```

### 3. Deploy agent

```bash
cd /opt
sudo git clone https://github.com/0xloveavax/lazy-lizard-agent.git
sudo chown -R $USER:$USER lazy-lizard-agent
cd lazy-lizard-agent
python3.11 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
nano .env   # fill in secrets
```

### 4. Test run

```bash
python main.py --dry-run
```

---

## Docker

### Dockerfile

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Never bake .env into the image — pass at runtime via --env-file
CMD ["python", "main.py"]
```

### Build and run

```bash
docker build -t lazy-lizard-agent .
docker run --env-file .env lazy-lizard-agent
```

> ⚠️ Never commit your real `.env` file or bake secrets into the Docker image.

---

## systemd Service

Create `/etc/systemd/system/lazy-lizard.service`:

```ini
[Unit]
Description=Lazy Lizard Agent — Solana memecoin compounder
After=network.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/opt/lazy-lizard-agent
EnvironmentFile=/opt/lazy-lizard-agent/.env
ExecStart=/opt/lazy-lizard-agent/.venv/bin/python main.py
Restart=on-failure
RestartSec=10
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
```

Enable and start:

```bash
sudo systemctl daemon-reload
sudo systemctl enable lazy-lizard
sudo systemctl start lazy-lizard
sudo journalctl -u lazy-lizard -f   # tail logs
```

---

## Environment Variables Reference

See [../.env.example](../.env.example) for the full list with descriptions.

| Variable | Required | Default | Description |
|---|---|---|---|
| `SOLANA_PRIVATE_KEY` | ✅ | — | Base58 wallet private key |
| `SOLANA_RPC_ENDPOINT` | | mainnet-beta | Solana RPC URL |
| `TAKE_PROFIT_PCT` | | `5.0` | Take-profit % |
| `MAX_POSITION_SOL` | | `0.1` | Max SOL per trade |
| `MIN_REPUTATION_SCORE` | | `70` | Min ERC-8004 cohort score |
| `VETERAN_WALLET_MIN` | | `1` | Min veteran wallets in first 15 |
| `X402_DONATE_PCT` | | `1.0` | % of profit to donate |
| `TELEGRAM_BOT_TOKEN` | | — | Bot token from @BotFather |
| `TELEGRAM_CHAT_ID` | | — | Chat/channel ID |
| `DRY_RUN` | | `true` | Simulate without real transactions |

---

## Security Checklist

- [ ] `.env` is in `.gitignore` and never committed
- [ ] Private key is stored only in `.env` / server secret manager
- [ ] `DRY_RUN=true` confirmed working before switching to `false`
- [ ] RPC endpoint is rate-limit-resilient (consider paid tier for production)
- [ ] systemd service runs as non-root user
- [ ] Firewall configured (only required ports open)
