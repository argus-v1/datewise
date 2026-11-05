# datewise

Parse human-friendly date strings into `datetime.date` objects. No dependencies.

```python
from datetime import date
from datewise import parse_date

parse_date("2024-03-15")          # date(2024, 3, 15)
parse_date("March 15, 2024")      # date(2024, 3, 15)
parse_date("tomorrow")            # today + 1 day
parse_date("-2w", today=date(2026, 11, 5))  # date(2026, 10, 22)
```

## Install

```bash
pip install -e ".[dev]"
```

## What it understands

| Input | Example |
| --- | --- |
| ISO and slash dates | `2024-03-15`, `2024/3/5` |
| Month names | `Mar 15 2024`, `March 15, 2024` |
| Keywords | `today`, `yesterday`, `tomorrow` |
| Relative offsets | `+3d`, `-2w` |

Case and surrounding whitespace are ignored. Pass `today=` to fix the reference date for keywords and offsets.

## Errors

Anything datewise can't read raises `datewise.DateParseError`, a subclass of `ValueError`, with a message that says what was wrong:

```python
from datewise import DateParseError, parse_date

try:
    parse_date(user_input)
except DateParseError as err:
    print(f"Please enter a date: {err}")
```

## License

MIT
