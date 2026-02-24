# Security Policy — Lazy Lizard Agent

## Supported Versions

| Version | Supported |
|---|---|
| `main` branch | ✅ Yes |
| Older tags | ❌ No |

---

## Responsible Disclosure

If you discover a security vulnerability in Lazy Lizard Agent, please **do not**
open a public GitHub issue. Instead, report it privately so we can address it
before public disclosure.

### How to Report

1. **Email**: Open a private security advisory via GitHub:  
   [GitHub Security Advisories](https://github.com/jeffreydunaway/lazy-lizard-agent/security/advisories/new)

2. **Include in your report**:
   - Description of the vulnerability
   - Steps to reproduce
   - Potential impact
   - Suggested fix (if you have one)

3. **Response time**: We aim to acknowledge reports within 48 hours and provide
   a resolution timeline within 7 days.

---

## Scope

The following are **in scope** for security reports:

- Private key or secret exposure (code or git history)
- Arbitrary code execution
- Fund loss due to logic bugs (swap, TP, position management)
- Dependency vulnerabilities with exploitable impact
- Authentication bypasses

The following are **out of scope**:

- Theoretical vulnerabilities without practical impact
- Rate limiting or DoS on third-party APIs (Jupiter, Telegram, Solana RPC)
- Social engineering attacks

---

## Security Best Practices for Users

- **Never commit `.env`** — it's in `.gitignore` for a reason
- Use a **dedicated hot wallet** funded only with what you can afford to lose
- Set `.env` file permissions: `chmod 600 .env`
- Rotate API keys if you suspect exposure
- Review the [Audit Checklist](docs/AUDIT-CHECKLIST.md) before deploying

---

## Disclosure Policy

- We follow [coordinated disclosure](https://en.wikipedia.org/wiki/Coordinated_vulnerability_disclosure).
- Reporters are credited in release notes (unless they prefer anonymity).
- We will not take legal action against good-faith security researchers.
