"""Parse human-friendly date strings into ``datetime.date`` objects."""

from __future__ import annotations

import re
from datetime import date, timedelta

__all__ = ["DateParseError", "parse_date"]


class DateParseError(ValueError):
    """Raised when a string can't be read as a date."""


_KEYWORDS = {"today": 0, "yesterday": -1, "tomorrow": 1}

_MONTHS = {
    "jan": 1, "feb": 2, "mar": 3, "apr": 4, "may": 5, "jun": 6,
    "jul": 7, "aug": 8, "sep": 9, "oct": 10, "nov": 11, "dec": 12,
}

_RELATIVE = re.compile(r"([+-])(\d+)([dw])")
_NUMERIC = re.compile(r"(\d{4})[-/](\d{1,2})[-/](\d{1,2})")
_MONTH_NAME = re.compile(r"([a-z]{3})[a-z]*\.?\s+(\d{1,2}),?\s+(\d{4})")


def parse_date(text: str, *, today: date | None = None) -> date:
    """Parse ``text`` into a date.

    Accepted forms:

    * ``2024-03-15``, ``2024/03/15`` (single-digit month and day are fine)
    * ``Mar 15 2024``, ``March 15, 2024``
    * ``today``, ``yesterday``, ``tomorrow``
    * relative offsets: ``+3d``, ``-2w``

    Matching ignores case and surrounding whitespace. ``today`` sets the
    reference date for keywords and offsets (defaults to ``date.today()``).

    Raises :class:`DateParseError` for anything it can't read.
    """
    if not isinstance(text, str):
        raise TypeError(f"parse_date() expects a str, got {type(text).__name__}")

    today = today or date.today()
    cleaned = text.strip().lower()

    if not cleaned:
        raise DateParseError(f"empty date: {text!r}")

    if cleaned[0] in "+-":
        return _parse_relative(cleaned, today, text)

    if cleaned in _KEYWORDS:
        return today + timedelta(days=_KEYWORDS[cleaned])

    if m := _NUMERIC.fullmatch(cleaned):
        year, month, day = (int(g) for g in m.groups())
        return _build(year, month, day, text)

    if m := _MONTH_NAME.fullmatch(cleaned):
        name, day, year = m.groups()
        if name not in _MONTHS:
            raise DateParseError(f"unknown month in {text!r}")
        return _build(int(year), _MONTHS[name], int(day), text)

    raise DateParseError(f"unrecognised date: {text!r}")


def _parse_relative(cleaned: str, today: date, original: str) -> date:
    m = _RELATIVE.fullmatch(cleaned)
    if not m:
        raise DateParseError(f"bad relative date: {original!r} (use e.g. +3d or -2w)")
    sign, amount, unit = m.groups()
    days = int(amount) * (7 if unit == "w" else 1)
    return today + timedelta(days=days if sign == "+" else -days)


def _build(year: int, month: int, day: int, original: str) -> date:
    try:
        return date(year, month, day)
    except ValueError as exc:
        raise DateParseError(f"invalid date {original!r}: {exc}") from None
