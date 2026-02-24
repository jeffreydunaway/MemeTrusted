"""
bot.py — Telegram alert sender for Lazy Lizard Agent.

Sends real-time notifications on buys, take-profits, errors, and daily reports.
"""

import logging
import os
from typing import Optional

import requests

logger = logging.getLogger("lazy-lizard.bot")

TELEGRAM_BOT_TOKEN: str = os.getenv("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHAT_ID: str = os.getenv("TELEGRAM_CHAT_ID", "")

_TELEGRAM_API_BASE = "https://api.telegram.org/bot{token}/{method}"


def _api_url(method: str) -> str:
    return _TELEGRAM_API_BASE.format(token=TELEGRAM_BOT_TOKEN, method=method)


def send_alert(
    message: str,
    parse_mode: str = "Markdown",
    disable_notification: bool = False,
) -> bool:
    """
    Send a message to the configured Telegram chat.

    :param message: Text to send. Supports Telegram Markdown.
    :param parse_mode: "Markdown" or "HTML".
    :param disable_notification: If True, sends silently.
    :returns: True on success, False on failure.
    """
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        logger.debug("Telegram not configured — skipping alert: %s", message)
        return False

    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": parse_mode,
        "disable_notification": disable_notification,
    }
    try:
        resp = requests.post(_api_url("sendMessage"), json=payload, timeout=10)
        resp.raise_for_status()
        return True
    except requests.RequestException as exc:
        logger.error("Failed to send Telegram alert: %s", exc)
        return False


def send_buy_alert(symbol: str, mint: str, price_sol: float, size_sol: float) -> bool:
    """Alert on a new position being opened."""
    msg = (
        f"🦎 *Lazy Lizard BUY*\n"
        f"Token: `{symbol}`\n"
        f"Mint: `{mint}`\n"
        f"Price: `{price_sol:.8f}` SOL\n"
        f"Size: `{size_sol:.4f}` SOL"
    )
    return send_alert(msg)


def send_tp_alert(
    symbol: str,
    mint: str,
    entry_price: float,
    exit_price: float,
    pnl_sol: float,
) -> bool:
    """Alert on a take-profit being hit."""
    emoji = "✅" if pnl_sol >= 0 else "🔴"
    msg = (
        f"{emoji} *Lazy Lizard TP*\n"
        f"Token: `{symbol}`\n"
        f"Mint: `{mint}`\n"
        f"Entry: `{entry_price:.8f}` SOL\n"
        f"Exit:  `{exit_price:.8f}` SOL\n"
        f"PnL:   `{pnl_sol:+.6f}` SOL"
    )
    return send_alert(msg)


def send_daily_report(report: dict) -> bool:
    """Send a daily P&L summary."""
    trades = report.get("trades_closed", 0)
    pnl = report.get("total_pnl_sol", 0.0)
    date = report.get("date", "?")
    emoji = "📈" if pnl >= 0 else "📉"
    msg = (
        f"{emoji} *Daily Report — {date}*\n"
        f"Trades closed: `{trades}`\n"
        f"Total PnL: `{pnl:+.6f}` SOL"
    )
    return send_alert(msg)


def send_error_alert(error: str) -> bool:
    """Alert on an unexpected error."""
    msg = f"⚠️ *Lazy Lizard ERROR*\n```\n{error[:1000]}\n```"
    return send_alert(msg)


def get_bot_info() -> Optional[dict]:
    """
    Validate bot credentials by calling getMe.

    :returns: Bot info dict or None if credentials are invalid.
    """
    if not TELEGRAM_BOT_TOKEN:
        logger.warning("TELEGRAM_BOT_TOKEN is not set.")
        return None
    try:
        resp = requests.get(_api_url("getMe"), timeout=10)
        resp.raise_for_status()
        data = resp.json()
        if data.get("ok"):
            return data.get("result")
        return None
    except requests.RequestException as exc:
        logger.error("Failed to call Telegram getMe: %s", exc)
        return None
