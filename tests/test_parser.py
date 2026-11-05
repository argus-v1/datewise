from datetime import date

import pytest

from datewise import DateParseError, parse_date

TODAY = date(2026, 11, 5)


def test_iso_date():
    assert parse_date("2024-03-15") == date(2024, 3, 15)


def test_iso_single_digit_month_and_day():
    assert parse_date("2024-3-5") == date(2024, 3, 5)


def test_slash_date():
    assert parse_date("2024/03/15") == date(2024, 3, 15)


def test_short_month_name():
    assert parse_date("Mar 15 2024") == date(2024, 3, 15)


def test_long_month_name_with_comma():
    assert parse_date("March 15, 2024") == date(2024, 3, 15)


def test_matching_ignores_case():
    assert parse_date("SEPTEMBER 1, 2025") == date(2025, 9, 1)


def test_surrounding_whitespace_is_ignored():
    assert parse_date("  2024-03-15 \n") == date(2024, 3, 15)


@pytest.mark.parametrize(
    "text", ["", " ", "\t\r\n", "\v\f", "\u00a0", "\u2003", "\u3000", "\t \u2003\n"]
)
def test_empty_or_whitespace_only_input_raises(text):
    with pytest.raises(DateParseError, match="empty"):
        parse_date(text)


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ("\u2003March 15, 2024\u00a0", date(2024, 3, 15)),
        ("\tTODAY\n", TODAY),
        ("\v+3d\f", date(2026, 11, 8)),
        ("\u3000-2w\u3000", date(2026, 10, 22)),
    ],
)
def test_surrounding_whitespace_preserves_other_date_forms(text, expected):
    assert parse_date(text, today=TODAY) == expected


@pytest.mark.parametrize(
    ("word", "expected"),
    [("today", TODAY), ("yesterday", date(2026, 11, 4)), ("tomorrow", date(2026, 11, 6))],
)
def test_keywords(word, expected):
    assert parse_date(word, today=TODAY) == expected


def test_relative_days_forward():
    assert parse_date("+3d", today=TODAY) == date(2026, 11, 8)


def test_relative_weeks_back():
    assert parse_date("-2w", today=TODAY) == date(2026, 10, 22)


def test_leap_day():
    assert parse_date("2024-02-29") == date(2024, 2, 29)


def test_impossible_date_raises():
    with pytest.raises(DateParseError, match="invalid date"):
        parse_date("2023-02-29")


def test_unknown_month_raises():
    with pytest.raises(DateParseError, match="unknown month"):
        parse_date("Foo 3 2024")


def test_unrecognised_text_raises():
    with pytest.raises(DateParseError, match="unrecognised"):
        parse_date("next tuesday")


def test_bad_relative_unit_raises():
    with pytest.raises(DateParseError, match="bad relative date"):
        parse_date("+3y", today=TODAY)


def test_non_string_raises_type_error():
    with pytest.raises(TypeError):
        parse_date(20240315)


def test_parse_error_is_a_value_error():
    assert issubclass(DateParseError, ValueError)
