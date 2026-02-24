# Contributing to Lazy Lizard Agent

Thank you for your interest in contributing! Here's how to get started.

---

## Ground Rules

- Be respectful — see [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md)
- **Never** commit secrets, private keys, or `.env` files
- Reference GitHub issues in your PR descriptions
- Keep PRs focused — one feature or fix per PR

---

## Workflow

1. **Fork** the repository (or use a feature branch if you have write access).
2. **Create a branch** with a descriptive name:
   ```bash
   git checkout -b feature/veteran-wallet-cache
   git checkout -b fix/jupiter-quote-timeout
   ```
3. **Make your changes** with small, atomic commits.
4. **Test** your changes locally before pushing.
5. **Open a Draft PR** early to get feedback, then mark as Ready for Review.
6. **Reference the issue** in your PR description:
   ```
   Closes #42
   ```

---

## Commit Message Format

```
<type>: <short summary>

[optional body]
[optional footer: Closes #issue]
```

Types: `feat`, `fix`, `docs`, `refactor`, `test`, `chore`

Examples:
```
feat: add time-based stop-loss to MemeCompounder
fix: handle Jupiter API timeout gracefully
docs: update DEPLOYMENT.md with systemd instructions
```

---

## Setting Up Locally

```bash
git clone https://github.com/jeffreydunaway/lazy-lizard-agent.git
cd lazy-lizard-agent
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# Edit .env — set DRY_RUN=true for development
```

---

## Code Style

- Follow [PEP 8](https://peps.python.org/pep-0008/)
- Use type hints on all public functions
- Docstrings on all public functions and classes
- Keep functions small and focused

---

## Security

- Read [SECURITY.md](SECURITY.md) before submitting any security-related PR
- **Never** include real wallet addresses, private keys, or tokens in code or tests
- If you discover a vulnerability, follow the responsible disclosure process in SECURITY.md

---

## Questions?

Open a [GitHub Discussion](https://github.com/jeffreydunaway/lazy-lizard-agent/discussions)
or file an [issue](https://github.com/jeffreydunaway/lazy-lizard-agent/issues).
