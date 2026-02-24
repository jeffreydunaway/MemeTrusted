# 📬 Telegram Bot Setup — Lazy Lizard Agent

> ⚠️ **HIGH-RISK DISCLAIMER**: Not financial advice. Memecoins can go to zero.

This guide walks you through creating a Telegram bot and connecting it to Lazy Lizard Agent for trade alerts and daily summaries.

---

## Step 1 — Create a Bot with @BotFather

1. Open Telegram and search for **@BotFather**
2. Send `/newbot`
3. Choose a display name, e.g. `Lazy Lizard Agent`
4. Choose a username, e.g. `lazylizardagent_bot` (must end in `_bot`)
5. BotFather will reply with your **bot token**: `123456789:AAF...`

> 🔒 Keep this token **secret** — anyone with it can send messages as your bot.

---

## Step 2 — Get Your Chat ID

### Option A — Personal chat

1. Start a chat with your new bot (send any message to it)
2. Open: `https://api.telegram.org/bot<YOUR_TOKEN>/getUpdates`
3. Find `"chat": {"id": 123456789}` — that number is your Chat ID

### Option B — Group or channel

1. Add your bot to the group/channel as an **administrator**
2. Send a message in the group
3. Visit the `getUpdates` URL above; find the group's `"id"` (usually negative, e.g. `-100123456789`)

---

## Step 3 — Configure .env

```env
TELEGRAM_BOT_TOKEN=123456789:AAFabcdef...
TELEGRAM_CHAT_ID=123456789
```

---

## Step 4 — Test the Connection

Run a quick test (Python):

```python
import asyncio
from bot import send_message

async def test():
    await send_message(
        token="YOUR_TOKEN",
        chat_id="YOUR_CHAT_ID",
        text="🦎 Lazy Lizard Agent — test message!",
    )

asyncio.run(test())
```

Or via curl:

```bash
curl -s "https://api.telegram.org/bot<TOKEN>/sendMessage" \
  -d chat_id=<CHAT_ID> \
  -d text="Hello from Lazy Lizard Agent!" \
  -d parse_mode=HTML
```

---

## Alert Types

| Alert | Trigger |
|---|---|
| 🟢 **BUY** | Token purchased via Jupiter |
| 🔴 **SELL** | Token sold at take-profit |
| 📊 **Daily Summary** | End-of-day P&L, trade count, x402 donations |
| 🟡 **ONLINE** | Agent startup confirmation |
| ❌ **ERROR** | Unhandled exception in run loop |

---

## Sample Alert

```
🟢 BUY LAZY
💰 Amount: 0.1000 SOL
🪙 Mint: LaZy1111...
⭐ Reputation score: 82
🔗 TX: 3xKf8P9q…

⚠️ Not financial advice. Memecoins can go to zero.
```

---

## Privacy Tips

- Use a **private group** or **private channel** for alerts (not public)
- Restrict who can add the bot to groups via BotFather → `/setjoingroups`
- Rotate the bot token immediately if you suspect it was exposed: BotFather → `/revoke`
