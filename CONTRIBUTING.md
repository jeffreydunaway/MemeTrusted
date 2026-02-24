# Contributing to Lazy Lizard Agent

Thank you for your interest in contributing! 🦎

---

## How to Contribute

1. **Fork** the repository and create a **feature branch** from `main`:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes** — keep commits small and focused.

3. **Reference the related issue** in your PR description (e.g. `Closes #42`).

4. **Open a Pull Request** as a **Draft PR** while work is in progress; mark it ready when done.

5. Wait for review. Address any feedback. Once approved, a maintainer will merge.

---

## Branch Naming Convention

| Prefix | Use for |
|---|---|
| `feature/` | New features |
| `fix/` | Bug fixes |
| `docs/` | Documentation changes |
| `chore/` | Maintenance (deps, CI, etc.) |

---

## Code Style

- Python: follow [PEP 8](https://peps.python.org/pep-0008/)
- Use type hints where practical
- Keep functions small and focused
- Add docstrings for public functions and classes

---

## Security

- **Never** commit `.env`, private keys, wallet addresses, or API tokens
- If you discover a security vulnerability, follow the process in [SECURITY.md](SECURITY.md) — do NOT open a public issue

---

## Testing

- Add tests for new features in the `tests/` directory
- Run existing tests before submitting: `pytest`
- All PRs must pass CI checks

---

## Code of Conduct

This project follows the [Contributor Covenant Code of Conduct](CODE_OF_CONDUCT.md). By participating, you agree to abide by its terms.
