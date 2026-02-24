# Bonus & Additional Integrations — Lazy Lizard Agent

---

## x402 Micro-Donations

### What is x402?

[x402](https://x402.org) is an HTTP-402-based micropayment protocol that allows
agents and services to send tiny payments programmatically, without a payment
processor.

### How Lazy Lizard Uses It

After each successful take-profit, the agent sends a micro-donation (default: 0.0001 SOL)
to the configured `X402_RECIPIENT_ADDRESS`. This supports open-source development
and protocol sustainability.

### Configuration

```dotenv
X402_RECIPIENT_ADDRESS=<recipient_solana_address>
X402_DONATION_SOL=0.0001
```

### Implementation (Stub)

```python
# In main.py close_position(), after successful TP:
from x402 import donate  # Future integration
donate(amount_sol=X402_DONATION_SOL, recipient=X402_RECIPIENT_ADDRESS)
```

---

## ERC-8004 Agent Reputation

### What is ERC-8004?

ERC-8004 is a proposed standard for on-chain agent reputation scoring.
It allows AI agents to accumulate and prove their track record transparently.

### How Lazy Lizard Uses It

After each closed position, the agent updates its on-chain reputation record with:

- Trade outcome (profit/loss)
- Signal accuracy (did the veteran-wallet filter predict correctly?)
- Total P&L history

### Configuration

```dotenv
ERC8004_CONTRACT_ADDRESS=<contract_address>
ERC8004_AGENT_ID=<agent_identifier>
```

### Implementation (Stub)

```python
# After each close_position():
from erc8004 import update_reputation  # Future integration
update_reputation(
    agent_id=ERC8004_AGENT_ID,
    outcome="profit" if pnl > 0 else "loss",
    pnl_sol=pnl,
)
```

---

## Diamond Proxy Treasury

### What is the Diamond Standard?

[EIP-2535 Diamond Standard](https://eips.ethereum.org/EIPS/eip-2535) allows
a single proxy contract to delegate to multiple "facet" implementation contracts.
This enables upgradeable on-chain treasury management.

### When to Use It

Use the Diamond proxy treasury if you want:

- Upgradeable on-chain logic without migrating funds
- Multi-facet treasury (e.g., separate facets for compounding, donations, withdrawals)
- DAO-controlled upgrades

### Setup (Future)

```bash
cd diamond/
npm install
npx hardhat compile
npx hardhat run scripts/deploy.js --network mainnet
```

See `diamond/README.md` (coming soon) for full details.

---

## Virtuals Protocol Integration

Lazy Lizard Agent is designed to be deployable on [Virtuals Protocol](https://virtuals.io)
as an autonomous AI agent.

### Steps

1. Package the agent logic as a Virtuals-compatible module.
2. Register the agent on the Virtuals marketplace.
3. Configure on-chain inference and action signing.
4. Users can stake $VIRTUAL to activate the agent.

---

## Jupiter Aggregator

[Jupiter](https://jup.ag) is Solana's leading DEX aggregator. Lazy Lizard uses
Jupiter v6 API for all swaps.

### Why Jupiter?

- Best routing across all Solana DEXes (Raydium, Orca, Meteora, etc.)
- Price impact minimisation
- Built-in slippage protection
- No additional smart contract risk

### API Reference

- Quote: `GET https://quote-api.jup.ag/v6/quote`
- Swap: `POST https://quote-api.jup.ag/v6/swap`

---

## Future Ideas

- [ ] Streamlit dashboard for real-time monitoring
- [ ] Wallet tracker with historical win-rate analysis
- [ ] Multi-wallet diversification (spread risk across N wallets)
- [ ] Stop-loss implementation (time-based or price-based)
- [ ] Discord alerts alongside Telegram
- [ ] On-chain profit distribution to $LAZY token holders
- [ ] Integration with lazylizardagent.com for public leaderboard
