"""
Lazy Lizard Agent — Core MemeCompounder class + CLI entry point.

⚠️  HIGH RISK: Memecoins can go to zero. Not financial advice.
     Never invest more than you can afford to lose entirely.
"""

import argparse
import logging
import os
import time
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Optional

from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%Y-%m-%dT%H:%M:%SZ",
)
logger = logging.getLogger("lazy-lizard")

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

TAKE_PROFIT_PCT: float = float(os.getenv("TAKE_PROFIT_PCT", "0.05"))  # 5% default
POSITION_SIZE_SOL: float = float(os.getenv("POSITION_SIZE_SOL", "0.01"))
MIN_VETERAN_WALLETS: int = int(os.getenv("MIN_VETERAN_WALLETS", "2"))
FIRST_N_BUYERS: int = int(os.getenv("FIRST_N_BUYERS", "15"))
POLL_INTERVAL_SECONDS: int = int(os.getenv("POLL_INTERVAL_SECONDS", "30"))
DRY_RUN: bool = os.getenv("DRY_RUN", "true").lower() == "true"


# ---------------------------------------------------------------------------
# Data models
# ---------------------------------------------------------------------------


@dataclass
class TokenSignal:
    mint: str
    symbol: str
    first_buyers: list[str] = field(default_factory=list)
    veteran_buyer_count: int = 0
    score: float = 0.0
    discovered_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


@dataclass
class Position:
    mint: str
    symbol: str
    entry_price: float
    size_sol: float
    opened_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    closed_at: Optional[datetime] = None
    exit_price: Optional[float] = None
    pnl_sol: Optional[float] = None


# ---------------------------------------------------------------------------
# MemeCompounder
# ---------------------------------------------------------------------------


class MemeCompounder:
    """
    Autonomous compounder that:
    1. Discovers new pump.fun tokens
    2. Filters by veteran-wallet + first-15-buyer signals
    3. Buys qualifying tokens via Jupiter
    4. Auto-sells at TAKE_PROFIT_PCT above entry
    5. Compounds daily gains
    """

    def __init__(self) -> None:
        self.positions: list[Position] = []
        self.closed_positions: list[Position] = []
        self.dry_run = DRY_RUN
        if self.dry_run:
            logger.warning("DRY_RUN mode enabled — no real trades will be executed.")

    # ------------------------------------------------------------------
    # Discovery
    # ------------------------------------------------------------------

    def discover_new_tokens(self) -> list[TokenSignal]:
        """
        Poll pump.fun (or a compatible RPC subscription) for new token mints.
        Returns a list of TokenSignal objects for scoring.

        In production, replace the stub with a real WebSocket or HTTP poll.
        """
        logger.info("Discovering new tokens from pump.fun …")
        # TODO: implement real pump.fun listener (WebSocket or polling)
        return []

    # ------------------------------------------------------------------
    # Filtering
    # ------------------------------------------------------------------

    def score_signal(self, signal: TokenSignal) -> float:
        """
        Score a token based on:
        - Number of veteran wallets in first-N buyers (weighted heavily)
        - Raw first-buyer count within first-15 window
        """
        veteran_weight = 10.0
        score = signal.veteran_buyer_count * veteran_weight
        first_buyer_bonus = min(len(signal.first_buyers), FIRST_N_BUYERS) * 0.5
        signal.score = score + first_buyer_bonus
        return signal.score

    def should_buy(self, signal: TokenSignal) -> bool:
        """Return True if the signal passes minimum thresholds."""
        self.score_signal(signal)
        qualifies = (
            signal.veteran_buyer_count >= MIN_VETERAN_WALLETS
            and signal.score > 0
        )
        logger.info(
            "Token %s | score=%.2f | veteran_wallets=%d | buy=%s",
            signal.symbol,
            signal.score,
            signal.veteran_buyer_count,
            qualifies,
        )
        return qualifies

    # ------------------------------------------------------------------
    # Trading
    # ------------------------------------------------------------------

    def open_position(self, signal: TokenSignal, entry_price: float) -> Position:
        """Buy a token and record the position."""
        position = Position(
            mint=signal.mint,
            symbol=signal.symbol,
            entry_price=entry_price,
            size_sol=POSITION_SIZE_SOL,
        )
        if not self.dry_run:
            from jupiter_auto import buy_token  # noqa: PLC0415

            buy_token(signal.mint, POSITION_SIZE_SOL)
        else:
            logger.info("[DRY RUN] Would buy %s @ %.8f SOL", signal.symbol, entry_price)
        self.positions.append(position)
        return position

    def close_position(self, position: Position, exit_price: float) -> None:
        """Sell a token and record the result."""
        position.exit_price = exit_price
        position.closed_at = datetime.now(timezone.utc)
        position.pnl_sol = (exit_price - position.entry_price) * position.size_sol

        if not self.dry_run:
            from jupiter_auto import sell_token  # noqa: PLC0415

            sell_token(position.mint, position.size_sol)
        else:
            logger.info(
                "[DRY RUN] Would sell %s @ %.8f SOL | PnL=%.6f SOL",
                position.symbol,
                exit_price,
                position.pnl_sol or 0.0,
            )

        self.positions.remove(position)
        self.closed_positions.append(position)

        try:
            from bot import send_alert  # noqa: PLC0415

            send_alert(
                f"✅ Closed {position.symbol} | PnL: {position.pnl_sol:+.6f} SOL"
            )
        except Exception:  # noqa: BLE001
            pass

    # ------------------------------------------------------------------
    # Take-profit loop
    # ------------------------------------------------------------------

    def check_take_profits(self, price_feed: dict[str, float]) -> None:
        """Check open positions against current prices and close at TP."""
        for pos in list(self.positions):
            current_price = price_feed.get(pos.mint)
            if current_price is None:
                continue
            tp_price = pos.entry_price * (1 + TAKE_PROFIT_PCT)
            if current_price >= tp_price:
                logger.info("TP reached for %s — closing position.", pos.symbol)
                self.close_position(pos, current_price)

    # ------------------------------------------------------------------
    # Reporting
    # ------------------------------------------------------------------

    def daily_report(self) -> dict:
        """Summarise closed positions for today."""
        today = datetime.now(timezone.utc).date()
        todays = [
            p for p in self.closed_positions
            if p.closed_at and p.closed_at.date() == today
        ]
        total_pnl = sum(p.pnl_sol or 0.0 for p in todays)
        report = {
            "date": str(today),
            "trades_closed": len(todays),
            "total_pnl_sol": round(total_pnl, 6),
            "positions": [
                {
                    "symbol": p.symbol,
                    "entry": p.entry_price,
                    "exit": p.exit_price,
                    "pnl_sol": p.pnl_sol,
                }
                for p in todays
            ],
        }
        return report

    # ------------------------------------------------------------------
    # Main loop
    # ------------------------------------------------------------------

    def run_monitor(self) -> None:
        """Continuous monitoring loop (dry-run safe)."""
        logger.info("Starting monitor loop (interval=%ds) …", POLL_INTERVAL_SECONDS)
        while True:
            signals = self.discover_new_tokens()
            for signal in signals:
                if self.should_buy(signal):
                    logger.info("Signal qualified: %s — would open position.", signal.symbol)
            time.sleep(POLL_INTERVAL_SECONDS)

    def run_trade(self) -> None:
        """Full autonomous trading loop."""
        from jupiter_auto import get_token_price_in_sol  # noqa: PLC0415

        logger.info("Starting trade loop …")
        while True:
            signals = self.discover_new_tokens()
            for signal in signals:
                if self.should_buy(signal):
                    entry_price = get_token_price_in_sol(signal.mint) or 0.0
                    if entry_price > 0:
                        self.open_position(signal, entry_price)
                    else:
                        logger.warning(
                            "Could not fetch entry price for %s — skipping.", signal.symbol
                        )
            # Fetch current prices for all open positions before checking TP
            price_feed: dict[str, float] = {}
            for pos in self.positions:
                price = get_token_price_in_sol(pos.mint)
                if price is not None:
                    price_feed[pos.mint] = price
            self.check_take_profits(price_feed)
            time.sleep(POLL_INTERVAL_SECONDS)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="lazy-lizard",
        description="Lazy Lizard Agent — Lazy Solana 5% daily compounder",
    )
    parser.add_argument(
        "--mode",
        choices=["monitor", "trade", "report"],
        default="monitor",
        help="Operating mode (default: monitor)",
    )
    return parser


def main() -> None:
    args = _build_parser().parse_args()
    compounder = MemeCompounder()

    if args.mode == "monitor":
        compounder.run_monitor()
    elif args.mode == "trade":
        compounder.run_trade()
    elif args.mode == "report":
        import json

        print(json.dumps(compounder.daily_report(), indent=2))


if __name__ == "__main__":
    main()
