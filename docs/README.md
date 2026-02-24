# Lazy Lizard Agent — Extended Documentation

> ⚠️ **HIGH RISK DISCLAIMER**: Memecoins can go to zero. This is NOT financial advice.  
> Never invest more than you can afford to lose entirely.

## Architecture Overview

```
pump.fun (WebSocket/Poll)
        │
        ▼
  Veteran-Wallet Filter ──► First-15-Buyer Scorer
        │
        ▼
   MemeCompounder (main.py)
        │
    ┌───┴───┐
    │       │
 Jupiter   Telegram
 Auto-     Bot
 Trade     Alerts
    │
    ▼
  5% Take-Profit
    │
    ▼
  Daily Compound
    │
    ▼
 x402 Donation + ERC-8004 Reputation Update
```

## Module Reference

### `main.py`

| Class / Function | Description |
|---|---|
| `MemeCompounder` | Core orchestrator |
| `TokenSignal` | Dataclass for a discovered token |
| `Position` | Dataclass for an open/closed position |
| `MemeCompounder.discover_new_tokens()` | Polls pump.fun for new mints |
| `MemeCompounder.score_signal()` | Veteran-wallet + first-buyer scoring |
| `MemeCompounder.should_buy()` | Returns True if signal passes thresholds |
| `MemeCompounder.open_position()` | Buys token via Jupiter |
| `MemeCompounder.close_position()` | Sells token + sends Telegram alert |
| `MemeCompounder.check_take_profits()` | Checks all open positions vs TP price |
| `MemeCompounder.daily_report()` | Summarises today's closed positions |
| `MemeCompounder.run_monitor()` | Continuous dry-run monitor loop |
| `MemeCompounder.run_trade()` | Full autonomous trading loop |

### `jupiter_auto.py`

| Function | Description |
|---|---|
| `get_quote()` | Fetch swap quote from Jupiter v6 API |
| `buy_token()` | Swap SOL → token |
| `sell_token()` | Swap token → SOL |
| `get_token_price_in_sol()` | Estimate token price via small quote |
| `sol_to_lamports()` | Convert SOL float to lamports int |

### `bot.py`

| Function | Description |
|---|---|
| `send_alert()` | Generic Telegram message sender |
| `send_buy_alert()` | Formatted buy notification |
| `send_tp_alert()` | Formatted TP notification |
| `send_daily_report()` | Daily P&L summary |
| `send_error_alert()` | Error notification |
| `get_bot_info()` | Validate bot credentials (getMe) |

## Configuration Reference

See [`.env.example`](../.env.example) for all environment variables with descriptions.

## Extending the Agent

### Adding a new signal filter

1. Add your logic to `MemeCompounder.score_signal()` in `main.py`.
2. Adjust `MemeCompounder.should_buy()` thresholds.

### Adding a new alert channel

1. Create a new module (e.g., `discord_bot.py`).
2. Import and call in `MemeCompounder.close_position()`.

### Replacing Jupiter with another DEX

1. Implement `buy_token()` / `sell_token()` equivalents in a new module.
2. Update imports in `main.py`.
