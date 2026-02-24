# Diamond Proxy Treasury (Future)

This directory will contain the optional Hardhat/Solidity implementation of the
[EIP-2535 Diamond Standard](https://eips.ethereum.org/EIPS/eip-2535) proxy treasury.

## Status

🚧 **Coming soon** — Solidity contracts and Hardhat scripts will be added here
in a future release.

## Planned Structure

```
diamond/
├── contracts/
│   ├── Diamond.sol
│   ├── facets/
│   │   ├── CompoundFacet.sol
│   │   ├── DonationFacet.sol
│   │   └── WithdrawFacet.sol
│   └── interfaces/
├── scripts/
│   ├── deploy.js
│   └── upgrade.js
├── test/
├── hardhat.config.js
└── package.json
```

See [docs/BONUS-OTHERS.md](../docs/BONUS-OTHERS.md#diamond-proxy-treasury) for more details.
