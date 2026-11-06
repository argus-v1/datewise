# Contributing to datewise

Thanks for helping. A few rules keep reviews quick.

## Setup

```bash
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
pytest
```

The full suite must pass before you open a pull request.

## Bug fixes

1. **Link the issue** in the PR description (`Fixes #17`).
2. **Add a regression test** that fails without your fix and passes with it. PRs that fix a bug without a test will be asked for one.
3. **Fix the whole class of input**, not just the one string in the report.

## Error policy

Bad input must raise `DateParseError` with a message that says what was wrong. It must never leak an `IndexError`, `KeyError`, or other internal exception to the caller.

## Style

- Keep the public API to `parse_date` and `DateParseError`.
- No new runtime dependencies.
- One change per PR; keep it small.
