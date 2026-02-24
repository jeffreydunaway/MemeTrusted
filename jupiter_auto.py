"""
Lazy Lizard Agent — jupiter_auto.py
Jupiter Aggregator buy/sell helpers for Solana token swaps.

⚠️  HIGH-RISK DISCLAIMER: This software interacts with memecoins on Solana.
    Memecoins are highly speculative and can go to zero.
    This is NOT financial advice. Use at your own risk.
"""

import logging
from typing import Optional

import httpx

logger = logging.getLogger("lazy-lizard.jupiter")

JUPITER_QUOTE_API = "https://quote-api.jup.ag/v6/quote"
JUPITER_SWAP_API = "https://quote-api.jup.ag/v6/swap"

# Native SOL mint address
SOL_MINT = "So11111111111111111111111111111111111111112"

# Lamports per SOL
LAMPORTS_PER_SOL = 1_000_000_000


async def get_quote(
    input_mint: str,
    output_mint: str,
    amount_lamports: int,
    slippage_bps: int = 100,
) -> dict:
    """
    Fetch a swap quote from Jupiter v6.

    Args:
        input_mint: Input token mint address.
        output_mint: Output token mint address.
        amount_lamports: Amount of input token in lamports (or smallest unit).
        slippage_bps: Slippage tolerance in basis points (default 100 = 1%).

    Returns:
        Jupiter quote response dict.

    Raises:
        httpx.HTTPStatusError: On non-2xx responses.
    """
    params = {
        "inputMint": input_mint,
        "outputMint": output_mint,
        "amount": str(amount_lamports),
        "slippageBps": str(slippage_bps),
    }
    async with httpx.AsyncClient(timeout=15) as client:
        resp = await client.get(JUPITER_QUOTE_API, params=params)
        resp.raise_for_status()
        quote = resp.json()
    logger.debug("Jupiter quote: %s → %s | %s", input_mint, output_mint, quote)
    return quote


async def build_swap_transaction(
    quote: dict,
    user_public_key: str,
) -> str:
    """
    Build a serialised swap transaction from a Jupiter quote.

    Args:
        quote: Quote dict returned by ``get_quote``.
        user_public_key: The trader's Solana public key (base58).

    Returns:
        Base64-encoded serialised transaction string.
    """
    payload = {
        "quoteResponse": quote,
        "userPublicKey": user_public_key,
        "wrapAndUnwrapSol": True,
        "dynamicComputeUnitLimit": True,
        "prioritizationFeeLamports": "auto",
    }
    async with httpx.AsyncClient(timeout=15) as client:
        resp = await client.post(JUPITER_SWAP_API, json=payload)
        resp.raise_for_status()
        data = resp.json()
    return data["swapTransaction"]


async def sign_and_send(
    serialized_tx: str,
    private_key: str,
    rpc_endpoint: str,
) -> str:
    """
    Sign and broadcast a serialised Solana transaction.

    Args:
        serialized_tx: Base64-encoded transaction from Jupiter.
        private_key: Wallet private key (base58).
        rpc_endpoint: Solana RPC URL.

    Returns:
        Transaction signature string.

    Note:
        Requires ``solders`` and ``solana-py`` packages.
    """
    # Import here so the module loads even without optional solana deps installed
    try:
        import base64

        from solders.keypair import Keypair  # type: ignore[import]
        from solders.transaction import VersionedTransaction  # type: ignore[import]
        from solana.rpc.async_api import AsyncClient  # type: ignore[import]
        from solana.rpc.types import TxOpts  # type: ignore[import]
    except ImportError as exc:
        raise ImportError(
            "Install solana-py and solders: pip install solana solders"
        ) from exc

    keypair = Keypair.from_base58_string(private_key)
    tx_bytes = base64.b64decode(serialized_tx)
    tx = VersionedTransaction.from_bytes(tx_bytes)
    tx.sign([keypair])

    async with AsyncClient(rpc_endpoint) as client:
        result = await client.send_raw_transaction(
            bytes(tx),
            opts=TxOpts(skip_preflight=False, preflight_commitment="confirmed"),
        )
    sig = str(result.value)
    logger.info("Transaction sent: %s", sig)
    return sig


async def buy_token(
    mint: str,
    amount_sol: float,
    rpc_endpoint: str,
    private_key: str,
    slippage_bps: int = 100,
) -> Optional[str]:
    """
    Buy ``mint`` token using ``amount_sol`` SOL via Jupiter.

    Args:
        mint: Target token mint address.
        amount_sol: Amount of SOL to spend.
        rpc_endpoint: Solana RPC URL.
        private_key: Wallet private key (base58).
        slippage_bps: Slippage tolerance in basis points.

    Returns:
        Transaction signature or None on failure.
    """
    amount_lamports = int(amount_sol * LAMPORTS_PER_SOL)
    logger.info("Buying %s | %.4f SOL (%d lamports)", mint, amount_sol, amount_lamports)

    try:
        quote = await get_quote(
            input_mint=SOL_MINT,
            output_mint=mint,
            amount_lamports=amount_lamports,
            slippage_bps=slippage_bps,
        )

        # Derive public key from private key for transaction building
        from solders.keypair import Keypair  # type: ignore[import]

        keypair = Keypair.from_base58_string(private_key)
        user_pubkey = str(keypair.pubkey())

        serialized_tx = await build_swap_transaction(quote, user_pubkey)
        tx_sig = await sign_and_send(serialized_tx, private_key, rpc_endpoint)
        return tx_sig
    except (httpx.HTTPError, ImportError, ValueError, KeyError) as exc:
        logger.error("buy_token failed for %s: %s", mint, exc)
        return None
    except Exception as exc:  # pylint: disable=broad-except
        logger.exception("Unexpected error in buy_token for %s: %s", mint, exc)
        return None


async def sell_token(
    mint: str,
    rpc_endpoint: str,
    private_key: str,
    slippage_bps: int = 100,
    amount_tokens: Optional[int] = None,
) -> Optional[str]:
    """
    Sell all (or ``amount_tokens``) of ``mint`` back to SOL via Jupiter.

    Args:
        mint: Token mint address to sell.
        rpc_endpoint: Solana RPC URL.
        private_key: Wallet private key (base58).
        slippage_bps: Slippage tolerance in basis points.
        amount_tokens: Exact token amount (smallest unit). If None, sells full balance.

    Returns:
        Transaction signature or None on failure.
    """
    logger.info("Selling %s", mint)

    try:
        if amount_tokens is None:
            amount_tokens = await get_token_balance(mint, private_key, rpc_endpoint)

        if not amount_tokens:
            logger.warning("No balance found for %s — skipping sell", mint)
            return None

        quote = await get_quote(
            input_mint=mint,
            output_mint=SOL_MINT,
            amount_lamports=amount_tokens,
            slippage_bps=slippage_bps,
        )

        from solders.keypair import Keypair  # type: ignore[import]

        keypair = Keypair.from_base58_string(private_key)
        user_pubkey = str(keypair.pubkey())

        serialized_tx = await build_swap_transaction(quote, user_pubkey)
        tx_sig = await sign_and_send(serialized_tx, private_key, rpc_endpoint)
        return tx_sig
    except (httpx.HTTPError, ImportError, ValueError, KeyError) as exc:
        logger.error("sell_token failed for %s: %s", mint, exc)
        return None
    except Exception as exc:  # pylint: disable=broad-except
        logger.exception("Unexpected error in sell_token for %s: %s", mint, exc)
        return None


async def get_token_balance(
    mint: str,
    private_key: str,
    rpc_endpoint: str,
) -> Optional[int]:
    """
    Return the token balance (in smallest units) for the wallet derived from ``private_key``.

    Returns:
        Integer balance or None if unavailable.
    """
    try:
        from solders.keypair import Keypair  # type: ignore[import]
        from solana.rpc.async_api import AsyncClient  # type: ignore[import]
        from solders.pubkey import Pubkey  # type: ignore[import]

        keypair = Keypair.from_base58_string(private_key)
        owner = keypair.pubkey()
        mint_pubkey = Pubkey.from_string(mint)

        async with AsyncClient(rpc_endpoint) as client:
            resp = await client.get_token_accounts_by_owner_json_parsed(
                owner, {"mint": mint_pubkey}
            )
        accounts = resp.value
        if not accounts:
            return None
        amount_str = (
            accounts[0].account.data.parsed["info"]["tokenAmount"]["amount"]
        )
        return int(amount_str)
    except (ImportError, ValueError, KeyError, IndexError) as exc:
        logger.error("get_token_balance failed for %s: %s", mint, exc)
        return None
    except Exception as exc:  # pylint: disable=broad-except
        logger.exception("Unexpected error in get_token_balance for %s: %s", mint, exc)
        return None
