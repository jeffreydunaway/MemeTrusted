# Security Policy — Lazy Lizard Agent

## Supported Versions

| Version | Supported |
|---|---|
| `main` branch | ✅ |

---

## Reporting a Vulnerability

**Please do NOT open a public GitHub issue for security vulnerabilities.**

If you discover a security vulnerability in this project, please report it responsibly:

1. **Email**: Send details to the repository owner via GitHub's private contact mechanism or the email listed in the GitHub profile.
2. **Include**:
   - Description of the vulnerability
   - Steps to reproduce
   - Potential impact
   - Any suggested mitigations

We will acknowledge your report within **48 hours** and aim to provide a fix or mitigation within **7 days** for critical issues.

---

## Security Best Practices for Users

- **Never** commit your `.env` file, private keys, or API tokens to any repository
- Store your Solana private key in environment variables only, never in source code
- Run with `DRY_RUN=true` until you have validated your configuration
- Use a dedicated hot wallet with limited funds — never your main/cold storage wallet
- Regularly rotate your Telegram bot token if you suspect exposure
- Keep dependencies up to date: `pip install --upgrade -r requirements.txt`

---

## Disclaimer

This software is provided as-is for educational and research purposes. The maintainers make no guarantees about the security or safety of on-chain transactions made by this software. Use at your own risk.
