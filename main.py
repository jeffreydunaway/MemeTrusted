"""
Lazy Lizard Agent — main.py
Core MemeCompounder class + CLI entry point.

⚠️  HIGH-RISK DISCLAIMER: This software interacts with memecoins on Solana.
    Memecoins are highly speculative and can go to zero.
    This is NOT financial advice. Use at your own risk.
"""

import argparse
import asyncio
import logging
import os
import sys
from dataclasses import dataclass, field
from typing import Optional

from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)
logger = logging.getLogger("lazy-lizard")


# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

@dataclass
class Config:
    """Runtime configuration loaded from environment variables."""

    solana_private_key: str = field(
        default_factory=lambda: os.environ.get("SOLANA_PRIVATE_KEY", "")
    )
    rpc_endpoint: str = field(
        default_factory=lambda: os.environ.get(
            "SOLANA_RPC_ENDPOINT", "https://api.mainnet-beta.solana.com"
        )
    )
    take_profit_pct: float = field(
        default_factory=lambda: float(os.environ.get("TAKE_PROFIT_PCT", "5.0"))
    )
    min_reputation_score: int = field(
        default_factory=lambda: int(os.environ.get("MIN_REPUTATION_SCORE", "70"))
    )
    x402_donate_pct: float = field(
        default_factory=lambda: float(os.environ.get("X402_DONATE_PCT", "1.0"))
    )
    telegram_bot_token: str = field(
        default_factory=lambda: os.environ.get("TELEGRAM_BOT_TOKEN", "")
    )
    telegram_chat_id: str = field(
        default_factory=lambda: os.environ.get("TELEGRAM_CHAT_ID", "")
    )
    max_position_sol: float = field(
        default_factory=lambda: float(os.environ.get("MAX_POSITION_SOL", "0.1"))
    )
    veteran_wallet_min: int = field(
        default_factory=lambda: int(os.environ.get("VETERAN_WALLET_MIN", "1"))
    )
    dry_run: bool = field(
        default_factory=lambda: os.environ.get("DRY_RUN", "true").lower() == "true"
    )

    def validate(self) -> None:
        """Raise ValueError if required fields are missing."""
        if not self.solana_private_key:
            raise ValueError("SOLANA_PRIVATE_KEY is required")
        if self.take_profit_pct <= 0:
            raise ValueError("TAKE_PROFIT_PCT must be > 0")
        if not (0 <= self.x402_donate_pct <= 100):
            raise ValueError("X402_DONATE_PCT must be between 0 and 100")


# ---------------------------------------------------------------------------
# MemeCompounder
# ---------------------------------------------------------------------------

class MemeCompounder:
    """
    Core autonomous agent that:
      1. Monitors pump.fun for new token launches
      2. Filters by veteran-wallet signals in the first 15 buyers
      3. Scores the first-15-buyer cohort (ERC-8004 reputation)
      4. Auto-buys qualifying tokens via Jupiter
      5. Auto-sells at take-profit threshold and compounds gains
      6. Sends Telegram alerts
      7. Donates a % of profits via x402
    """

    def __init__(self, config: Optional[Config] = None) -> None:
        self.config = config or Config()
        self._running = False

    async def discover_tokens(self) -> list[dict]:
        """
        Poll pump.fun for newly launched tokens.

        Returns a list of token metadata dicts:
          { "mint": str, "name": str, "symbol": str, "launch_ts": int, "first_buyers": list[str] }
        """
        # TODO: Implement pump.fun websocket / REST polling
        logger.info("Discovering new pump.fun tokens…")
        return []

    async def filter_by_veteran_wallets(
        self, tokens: list[dict], veteran_wallets: set[str]
    ) -> list[dict]:
        """
        Keep only tokens where at least ``config.veteran_wallet_min`` of the
        first 15 buyers are known veteran wallets.
        """
        qualified = []
        for token in tokens:
            first_buyers: list[str] = token.get("first_buyers", [])[:15]
            veteran_count = sum(1 for w in first_buyers if w in veteran_wallets)
            if veteran_count >= self.config.veteran_wallet_min:
                token["veteran_count"] = veteran_count
                qualified.append(token)
        logger.info(
            "Veteran-wallet filter: %d/%d tokens passed", len(qualified), len(tokens)
        )
        return qualified

    async def score_cohort(self, first_buyers: list[str]) -> int:
        """
        Score a first-15-buyer cohort using ERC-8004 on-chain reputation data.

        Returns an integer score 0-100.
        """
        # TODO: Implement ERC-8004 reputation lookup
        logger.debug("Scoring cohort of %d wallets…", len(first_buyers))
        return 0

    async def evaluate_token(self, token: dict) -> bool:
        """
        Return True if the token passes the reputation score threshold.
        """
        first_buyers: list[str] = token.get("first_buyers", [])[:15]
        score = await self.score_cohort(first_buyers)
        token["reputation_score"] = score
        passed = score >= self.config.min_reputation_score
        logger.info(
            "Token %s score=%d threshold=%d → %s",
            token.get("symbol", "?"),
            score,
            self.config.min_reputation_score,
            "BUY" if passed else "SKIP",
        )
        return passed

    async def buy(self, token: dict) -> Optional[str]:
        """
        Buy ``token`` via Jupiter.  Returns the transaction signature or None.
        """
        from jupiter_auto import buy_token  # local import to allow dry-run usage

        if self.config.dry_run:
            logger.info("[DRY RUN] Would buy %s", token.get("symbol"))
            return "dry-run-tx"

        mint: str = token["mint"]
        amount_sol = self.config.max_position_sol
        tx_sig = await buy_token(
            mint=mint,
            amount_sol=amount_sol,
            rpc_endpoint=self.config.rpc_endpoint,
            private_key=self.config.solana_private_key,
        )
        logger.info("Bought %s | tx=%s", token.get("symbol"), tx_sig)
        return tx_sig

    async def sell_at_take_profit(self, token: dict, buy_price: float) -> Optional[str]:
        """
        Sell ``token`` when price reaches the take-profit threshold.
        Returns the transaction signature or None.
        """
        from jupiter_auto import sell_token

        tp_price = buy_price * (1 + self.config.take_profit_pct / 100)

        if self.config.dry_run:
            logger.info(
                "[DRY RUN] Would sell %s at TP price %.6f (%.1f%%)",
                token.get("symbol"),
                tp_price,
                self.config.take_profit_pct,
            )
            return "dry-run-tx"

        # TODO: poll price and trigger sell
        tx_sig = await sell_token(
            mint=token["mint"],
            rpc_endpoint=self.config.rpc_endpoint,
            private_key=self.config.solana_private_key,
        )
        logger.info(
            "Sold %s at TP | tx=%s", token.get("symbol"), tx_sig
        )
        return tx_sig

    async def donate_x402(self, profit_sol: float) -> None:
        """Donate x402_donate_pct % of profit_sol via x402 protocol."""
        donation = profit_sol * self.config.x402_donate_pct / 100
        if donation <= 0:
            return
        # TODO: Implement x402 micro-donation transaction
        logger.info("x402 donation: %.6f SOL", donation)

    async def send_alert(self, message: str) -> None:
        """Send a Telegram alert."""
        if not self.config.telegram_bot_token or not self.config.telegram_chat_id:
            logger.debug("Telegram not configured — skipping alert")
            return
        from bot import send_message

        await send_message(
            token=self.config.telegram_bot_token,
            chat_id=self.config.telegram_chat_id,
            text=message,
        )

    async def run_once(self, veteran_wallets: set[str]) -> None:
        """Execute one full discover → filter → score → buy/sell cycle."""
        tokens = await self.discover_tokens()
        qualified = await self.filter_by_veteran_wallets(tokens, veteran_wallets)

        for token in qualified:
            should_buy = await self.evaluate_token(token)
            if not should_buy:
                continue

            tx_sig = await self.buy(token)
            if tx_sig:
                await self.send_alert(
                    f"🦎 BUY {token.get('symbol')} | score={token.get('reputation_score')} | tx={tx_sig}"
                )

    async def run(self, veteran_wallets: set[str], poll_interval: int = 30) -> None:
        """Main event loop — runs indefinitely until stopped."""
        self._running = True
        logger.info(
            "🦎 Lazy Lizard Agent started | dry_run=%s | TP=%.1f%%",
            self.config.dry_run,
            self.config.take_profit_pct,
        )
        await self.send_alert("🦎 Lazy Lizard Agent is ONLINE")

        while self._running:
            try:
                await self.run_once(veteran_wallets)
            except (asyncio.TimeoutError, asyncio.CancelledError):
                raise  # let CancelledError propagate for clean shutdown
            except Exception as exc:  # pylint: disable=broad-except
                logger.exception("Error in run loop: %s", exc)
            await asyncio.sleep(poll_interval)

    def stop(self) -> None:
        """Signal the run loop to stop after the current cycle."""
        self._running = False
        logger.info("Stopping Lazy Lizard Agent…")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def parse_args(argv: Optional[list[str]] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="🦎 Lazy Lizard Agent — Solana 5% daily memecoin compounder",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "⚠️  HIGH-RISK: Memecoins can go to zero. Not financial advice.\n"
            "    Always start with DRY_RUN=true in your .env file.\n"
        ),
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        default=None,
        help="Run in simulation mode (no real transactions). Overrides .env DRY_RUN.",
    )
    parser.add_argument(
        "--poll-interval",
        type=int,
        default=30,
        metavar="SECONDS",
        help="Seconds between pump.fun polls (default: 30)",
    )
    parser.add_argument(
        "--veteran-wallets",
        type=str,
        default="",
        metavar="FILE",
        help="Path to a newline-separated file of veteran wallet addresses",
    )
    return parser.parse_args(argv)


def load_veteran_wallets(path: str) -> set[str]:
    """Load wallet addresses from a newline-separated file."""
    if not path:
        return set()
    try:
        with open(path, encoding="utf-8") as fh:
            return {line.strip() for line in fh if line.strip()}
    except FileNotFoundError:
        logger.warning("Veteran wallets file not found: %s", path)
        return set()


async def async_main(argv: Optional[list[str]] = None) -> None:
    args = parse_args(argv)
    config = Config()

    if args.dry_run is not None:
        config.dry_run = args.dry_run

    try:
        config.validate()
    except ValueError as exc:
        logger.error("Configuration error: %s", exc)
        sys.exit(1)

    veteran_wallets = load_veteran_wallets(args.veteran_wallets)
    agent = MemeCompounder(config=config)

    try:
        await agent.run(veteran_wallets=veteran_wallets, poll_interval=args.poll_interval)
    except KeyboardInterrupt:
        agent.stop()


def main(argv: Optional[list[str]] = None) -> None:
    asyncio.run(async_main(argv))


if __name__ == "__main__":
    main()
