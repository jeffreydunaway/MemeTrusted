"""
Lazy Lizard Agent — bot.py
Telegram alert sender.

⚠️  HIGH-RISK DISCLAIMER: This software interacts with memecoins on Solana.
    Memecoins are highly speculative and can go to zero.
    This is NOT financial advice. Use at your own risk.
"""

import logging
from typing import Optional

import httpx

logger = logging.getLogger("lazy-lizard.bot")

TELEGRAM_API_BASE = "https://api.telegram.org/bot{token}"


async def send_message(
    token: str,
    chat_id: str,
    text: str,
    parse_mode: str = "HTML",
    disable_web_page_preview: bool = True,
) -> Optional[dict]:
    """
    Send a Telegram message via the Bot API.

    Args:
        token: Telegram bot token (from @BotFather).
        chat_id: Destination chat / channel ID or username.
        text: Message text. Supports HTML or Markdown formatting.
        parse_mode: "HTML" or "Markdown" (default "HTML").
        disable_web_page_preview: Suppress URL link previews (default True).

    Returns:
        Telegram API response dict, or None on failure.
    """
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": parse_mode,
        "disable_web_page_preview": disable_web_page_preview,
    }
    try:
        async with httpx.AsyncClient(timeout=10) as client:
            resp = await client.post(url, json=payload)
            resp.raise_for_status()
            result = resp.json()
        logger.debug("Telegram message sent: message_id=%s", result.get("result", {}).get("message_id"))
        return result
    except httpx.HTTPStatusError as exc:
        logger.error(
            "Telegram API error %s: %s", exc.response.status_code, exc.response.text
        )
        return None
    except httpx.RequestError as exc:
        logger.error("Telegram request failed: %s", exc)
        return None


async def send_trade_alert(
    token: str,
    chat_id: str,
    action: str,
    symbol: str,
    mint: str,
    amount_sol: float,
    tx_sig: str,
    reputation_score: Optional[int] = None,
    take_profit_pct: Optional[float] = None,
) -> None:
    """
    Send a formatted trade alert (BUY or SELL).

    Args:
        token: Telegram bot token.
        chat_id: Destination chat ID.
        action: "BUY" or "SELL".
        symbol: Token symbol.
        mint: Token mint address.
        amount_sol: SOL amount involved.
        tx_sig: Solana transaction signature.
        reputation_score: ERC-8004 score (optional).
        take_profit_pct: Take-profit % achieved (optional, for SELL alerts).
    """
    emoji = "🟢" if action.upper() == "BUY" else "🔴"
    lines = [
        f"{emoji} <b>{action.upper()} {symbol}</b>",
        f"💰 Amount: <code>{amount_sol:.4f} SOL</code>",
        f"🪙 Mint: <code>{mint}</code>",
    ]
    if reputation_score is not None:
        lines.append(f"⭐ Reputation score: <code>{reputation_score}</code>")
    if take_profit_pct is not None:
        lines.append(f"🎯 Take-profit: <code>+{take_profit_pct:.1f}%</code>")
    lines.append(
        f"🔗 TX: <a href=\"https://solscan.io/tx/{tx_sig}\">{tx_sig[:16]}…</a>"
    )
    lines.append("")
    lines.append("<i>⚠️ Not financial advice. Memecoins can go to zero.</i>")

    text = "\n".join(lines)
    await send_message(token=token, chat_id=chat_id, text=text)


async def send_daily_summary(
    token: str,
    chat_id: str,
    trades_count: int,
    pnl_sol: float,
    donated_sol: float,
) -> None:
    """
    Send a daily P&L summary alert.

    Args:
        token: Telegram bot token.
        chat_id: Destination chat ID.
        trades_count: Number of completed round-trip trades today.
        pnl_sol: Net profit/loss in SOL for the day.
        donated_sol: Amount donated via x402 today.
    """
    pnl_emoji = "📈" if pnl_sol >= 0 else "📉"
    text = (
        f"🦎 <b>Lazy Lizard Daily Summary</b>\n\n"
        f"🔁 Trades: <code>{trades_count}</code>\n"
        f"{pnl_emoji} P&L: <code>{pnl_sol:+.4f} SOL</code>\n"
        f"💸 x402 Donated: <code>{donated_sol:.6f} SOL</code>\n\n"
        f"<i>⚠️ Not financial advice. Past performance ≠ future results.</i>"
    )
    await send_message(token=token, chat_id=chat_id, text=text)
