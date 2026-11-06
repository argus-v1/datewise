"""datewise: parse human-friendly date strings."""

from .parser import DateParseError, parse_date

__all__ = ["DateParseError", "parse_date"]
__version__ = "0.3.1"
