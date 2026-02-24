"""
jupiter_auto.py — Jupiter Aggregator buy/sell helpers for Lazy Lizard Agent.

⚠️  HIGH RISK: Memecoins can go to zero. Not financial advice.
"""

import logging
import os
from typing import Any, Optional

import requests

logger = logging.getLogger("lazy-lizard.jupiter")

JUPITER_QUOTE_API = "https://quote-api.jup.ag/v6/quote"
JUPITER_SWAP_API = "https://quote-api.jup.ag/v6/swap"

# SOL mint address (wrapped SOL)
SOL_MINT = "So11111111111111111111111111111111111111112"

RPC_ENDPOINT: str = os.getenv("SOLANA_RPC_ENDPOINT", "https://api.mainnet-beta.solana.com")
WALLET_PRIVATE_KEY: str = os.getenv("WALLET_PRIVATE_KEY", "")
SLIPPAGE_BPS: int = int(os.getenv("SLIPPAGE_BPS", "100"))  # 1% default


# ---------------------------------------------------------------------------
# Quote helpers
# ---------------------------------------------------------------------------


def get_quote(
    input_mint: str,
    output_mint: str,
    amount_lamports: int,
    slippage_bps: int = SLIPPAGE_BPS,
) -> Optional[dict[str, Any]]:
    """
    Fetch a Jupiter swap quote.

    :param input_mint: Input token mint address.
    :param output_mint: Output token mint address.
    :param amount_lamports: Amount in lamports (1 SOL = 1_000_000_000).
    :param slippage_bps: Slippage tolerance in basis points.
    :returns: Quote dict or None on error.
    """
    params = {
        "inputMint": input_mint,
        "outputMint": output_mint,
        "amount": amount_lamports,
        "slippageBps": slippage_bps,
    }
    try:
        response = requests.get(JUPITER_QUOTE_API, params=params, timeout=10)
        response.raise_for_status()
        quote = response.json()
        logger.debug("Jupiter quote: %s", quote)
        return quote
    except requests.RequestException as exc:
        logger.error("Failed to fetch Jupiter quote: %s", exc)
        return None


def sol_to_lamports(sol_amount: float) -> int:
    """Convert SOL float to integer lamports."""
    return int(sol_amount * 1_000_000_000)


# ---------------------------------------------------------------------------
# Buy / Sell
# ---------------------------------------------------------------------------


def buy_token(
    token_mint: str,
    sol_amount: float,
    slippage_bps: int = SLIPPAGE_BPS,
) -> Optional[str]:
    """
    Buy a token by swapping SOL → token_mint via Jupiter.

    :param token_mint: Mint address of the token to buy.
    :param sol_amount: Amount of SOL to spend.
    :param slippage_bps: Slippage tolerance in basis points.
    :returns: Transaction signature string, or None on failure.
    """
    if not WALLET_PRIVATE_KEY:
        logger.error("WALLET_PRIVATE_KEY is not set — cannot execute trade.")
        return None

    amount_lamports = sol_to_lamports(sol_amount)
    quote = get_quote(SOL_MINT, token_mint, amount_lamports, slippage_bps)
    if not quote:
        return None

    tx_sig = _execute_swap(quote)
    if tx_sig:
        logger.info("BUY %s | %.4f SOL | tx=%s", token_mint, sol_amount, tx_sig)
    return tx_sig


def sell_token(
    token_mint: str,
    token_amount: float,
    slippage_bps: int = SLIPPAGE_BPS,
) -> Optional[str]:
    """
    Sell a token by swapping token_mint → SOL via Jupiter.

    :param token_mint: Mint address of the token to sell.
    :param token_amount: Raw token amount (in token's base units).
    :param slippage_bps: Slippage tolerance in basis points.
    :returns: Transaction signature string, or None on failure.
    """
    if not WALLET_PRIVATE_KEY:
        logger.error("WALLET_PRIVATE_KEY is not set — cannot execute trade.")
        return None

    amount_int = int(token_amount)
    quote = get_quote(token_mint, SOL_MINT, amount_int, slippage_bps)
    if not quote:
        return None

    tx_sig = _execute_swap(quote)
    if tx_sig:
        logger.info("SELL %s | amount=%s | tx=%s", token_mint, token_amount, tx_sig)
    return tx_sig


# ---------------------------------------------------------------------------
# Swap execution
# ---------------------------------------------------------------------------


def _execute_swap(quote: dict[str, Any]) -> Optional[str]:
    """
    Submit a Jupiter swap transaction.

    Builds the swap transaction from the quote, signs it with the wallet,
    and submits it to the Solana network.

    :param quote: Quote dict returned by get_quote().
    :returns: Transaction signature or None on failure.
    """
    try:
        from solders.keypair import Keypair  # noqa: PLC0415
        from solana.rpc.api import Client  # noqa: PLC0415
        import base58  # noqa: PLC0415
    except ImportError:
        logger.error(
            "solders / solana-py / base58 not installed. "
            "Run: pip install solders solana base58"
        )
        return None

    try:
        keypair = Keypair.from_base58_string(WALLET_PRIVATE_KEY)
        public_key_str = str(keypair.pubkey())
    except Exception as exc:  # noqa: BLE001
        logger.error("Failed to load wallet keypair: %s", exc)
        return None

    payload = {
        "quoteResponse": quote,
        "userPublicKey": public_key_str,
        "wrapAndUnwrapSol": True,
    }
    try:
        resp = requests.post(JUPITER_SWAP_API, json=payload, timeout=15)
        resp.raise_for_status()
        swap_data = resp.json()
    except requests.RequestException as exc:
        logger.error("Failed to get swap transaction from Jupiter: %s", exc)
        return None

    import base64  # noqa: PLC0415

    raw_tx = base64.b64decode(swap_data["swapTransaction"])

    try:
        from solders.transaction import VersionedTransaction  # noqa: PLC0415

        tx = VersionedTransaction.from_bytes(raw_tx)
        signed_tx = VersionedTransaction(tx.message, [keypair])
        client = Client(RPC_ENDPOINT)
        result = client.send_raw_transaction(bytes(signed_tx))
        tx_sig = str(result.value)
        return tx_sig
    except Exception as exc:  # noqa: BLE001
        logger.error("Failed to sign/submit swap transaction: %s", exc)
        return None


# ---------------------------------------------------------------------------
# Price fetching
# ---------------------------------------------------------------------------


def get_token_price_in_sol(token_mint: str, sample_amount: int = 1_000_000) -> Optional[float]:
    """
    Estimate a token's price in SOL by requesting a small Jupiter quote.

    :param token_mint: Mint address of the token.
    :param sample_amount: Token units to quote (default 1_000_000).
    :returns: Price in SOL per token unit, or None on failure.
    """
    quote = get_quote(token_mint, SOL_MINT, sample_amount)
    if not quote:
        return None
    try:
        out_lamports = int(quote["outAmount"])
        price_sol = out_lamports / 1_000_000_000 / sample_amount
        return price_sol
    except (KeyError, ValueError, ZeroDivisionError) as exc:
        logger.error("Could not parse price from quote: %s", exc)
        return None
