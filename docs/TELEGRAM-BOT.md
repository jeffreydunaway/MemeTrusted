# Telegram Bot Setup — Lazy Lizard Agent

Lazy Lizard Agent sends real-time alerts via Telegram for every buy, take-profit,
daily report, and error event.

---

## Step 1 — Create a Telegram Bot

1. Open Telegram and search for **@BotFather**.
2. Send `/newbot` and follow the prompts:
   - Choose a name: e.g., `Lazy Lizard Agent`
   - Choose a username: e.g., `LazyLizardAgentBot`
3. BotFather will reply with your **HTTP API token**:
   ```
   1234567890:ABCDEF-your-token-here
   ```
4. Copy this token — you will need it for `.env`.

---

## Step 2 — Find Your Chat ID

**Option A — Personal chat:**

1. Start a conversation with your bot (search for it and press Start).
2. Send any message (e.g., `/start`).
3. Visit:
   ```
   https://api.telegram.org/bot<TOKEN>/getUpdates
   ```
4. Find `"chat": {"id": 123456789}` in the response.
5. Copy the numeric `id`.

**Option B — Group or channel:**

1. Add your bot to the group/channel.
2. Give the bot admin rights if needed.
3. Follow the same `getUpdates` method above.
4. Group chat IDs are negative numbers (e.g., `-1001234567890`).

---

## Step 3 — Configure `.env`

```dotenv
TELEGRAM_BOT_TOKEN=1234567890:ABCDEF-your-token-here
TELEGRAM_CHAT_ID=123456789
```

---

## Step 4 — Test the Connection

```python
from bot import get_bot_info, send_alert

info = get_bot_info()
print(info)  # Should print bot details

send_alert("🦎 Lazy Lizard Agent is online!")
```

---

## Alert Types

| Function | When sent |
|---|---|
| `send_buy_alert()` | When a new position is opened |
| `send_tp_alert()` | When take-profit is hit |
| `send_daily_report()` | End of each trading day |
| `send_error_alert()` | On unexpected exceptions |

---

## Customising Alerts

Edit `bot.py` to change message formatting, add emojis, or add new alert types.
All messages support Telegram Markdown syntax.

---

## Disabling Alerts

Simply leave `TELEGRAM_BOT_TOKEN` and `TELEGRAM_CHAT_ID` empty in `.env`.
The agent will continue running — alerts will be silently skipped.
