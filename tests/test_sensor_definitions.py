"""Verify raw MQTT status codes are mapped to slugs (Closes: #227)."""

import json

import pytest

from custom_components.goecharger_mqtt.definitions.sensor import (
    json_array_to_csv,
    to_code_slug,
    to_psm_slug,
)


@pytest.mark.parametrize(
    "value,expected",
    [
        ("0", "auto"),
        ("1", "one_phase"),
        ("2", "three_phases"),
        ("99", "99"),  # unknown code falls back to raw value
    ],
)
def test_to_psm_slug(value, expected) -> None:
    """Psm must resolve slugs regardless of the (empty) attribute passed in."""
    assert to_psm_slug(value, "") == expected


def test_to_code_slug_with_empty_attribute_falls_back_to_raw_value() -> None:
    """Documents why psm can't use to_code_slug with its default attribute=""."""
    assert to_code_slug("2", "") == "2"


def test_json_array_to_csv_with_null_value_returns_empty_string() -> None:
    """The ocu sensor reports the literal string "null" when unset."""
    assert json_array_to_csv("null", "") == ""


def test_json_array_to_csv_joins_items_with_comma_and_space() -> None:
    """The CSV separator between items is ", "."""
    assert (
        json_array_to_csv(json.dumps(["60.6 BETA", "60.5 BETA"]), "")
        == "60.6 BETA, 60.5 BETA"
    )


def test_json_array_to_csv_leaves_short_lists_untouched() -> None:
    """A CSV of 255 chars or less must not be truncated."""
    items = [f"v{i}" for i in range(45)]  # joined length is 213 chars
    value = json.dumps(items)
    csv = json_array_to_csv(value, "")

    assert len(csv) <= 255
    assert csv == ", ".join(items)
    assert not csv.endswith(", ...")


def test_json_array_to_csv_truncates_lists_longer_than_255_chars() -> None:
    """Reproduces the OTA firmware list from #231 that exceeds HA's 255 char state limit."""
    items = [
        "60.6 BETA",
        "60.5 BETA",
        "60.4 BETA",
        "60.3 BETA",
        "60.2 BETA",
        "60.1 BETA",
        "60.0 BETA",
        "59.4",
        "57.1 OUTDATED",
        "V 57.0 OUTDATED",
        "V 56.11 OUTDATED",
        "V 56.9 OUTDATED",
        "V 56.8 OUTDATED",
        "V 56.2 OUTDATED",
        "V 56.1 OUTDATED",
        "V 055.8 OUTDATED",
        "V 055.7 OUTDATED",
        "V 055.5 OUTDATED",
        "V 055.0 OUTDATED",
    ]
    full_csv = ", ".join(items)
    assert len(full_csv) > 255  # sanity check: fixture must reproduce the bug

    csv = json_array_to_csv(json.dumps(items), "")

    assert len(csv) <= 255
    assert csv.endswith(", ...")
    # No version number may be cut in half: every entry before the ellipsis
    # must be one of the original, complete items.
    kept = csv[: -len(", ...")].split(", ")
    assert kept == items[: len(kept)]
    assert len(kept) < len(items)
    # Newest firmware versions are listed first, so they must survive truncation.
    assert csv.startswith("60.6 BETA, 60.5 BETA")


def test_json_array_to_csv_drops_item_that_would_exceed_250_chars() -> None:
    """The item that would push the string past 250 chars is dropped, not cut."""
    # The 41 "aa" items alone join to 162 chars; adding the 100-char item
    # would push the running total to 264, so it must be dropped whole.
    items = ["aa"] * 41 + ["b" * 100]
    value = json.dumps(items)
    assert len(", ".join(items)) > 255  # sanity check: fixture must reproduce the bug

    csv = json_array_to_csv(value, "")

    assert csv == ", ".join(["aa"] * 41) + ", ..."
    assert len(csv) <= 255


def test_json_array_to_csv_truncates_exactly_at_the_255_char_boundary() -> None:
    """A CSV of exactly 256 chars is the smallest input that must be truncated."""
    items = ["a"] * 86  # 86 * "a" joined by ", " == 256 chars
    value = json.dumps(items)
    full_csv = ", ".join(items)
    assert len(full_csv) == 256

    csv = json_array_to_csv(value, "")

    # 84 items join to exactly 250 chars, the most that still fits.
    assert csv == ", ".join(["a"] * 84) + ", ..."
    assert len(csv) == 255
