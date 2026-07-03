"""Verify raw MQTT status codes are mapped to slugs (Closes: #227)."""

import pytest

from custom_components.goecharger_mqtt.definitions.sensor import (
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
