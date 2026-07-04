"""Test go-eCharger (MQTT) button entities."""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from pytest_homeassistant_custom_component.common import MockConfigEntry

from custom_components.goecharger_mqtt.button import GoEChargerButton
from custom_components.goecharger_mqtt.const import CONF_TOPIC, DOMAIN
from custom_components.goecharger_mqtt.definitions.button import BUTTONS


def _entity_for(hass, key: str, attribute: str = "") -> GoEChargerButton:
    """Build a GoEChargerButton for the given definition key/attribute."""
    entry = MockConfigEntry(
        domain=DOMAIN, data={CONF_TOPIC: "go-eCharger/072246"}, version=2
    )
    entry.add_to_hass(hass)
    entry.runtime_data = MagicMock()
    description = next(d for d in BUTTONS if d.key == key and d.attribute == attribute)
    entity = GoEChargerButton(entry, description)
    entity.hass = hass
    return entity


@pytest.mark.parametrize(
    "key,attribute,expected_payload",
    [
        ("rst", "", "true"),
        ("frc", "0", "0"),
        ("frc", "1", "1"),
        ("frc", "2", "2"),
        ("dwo", "", "null"),
    ],
)
async def test_button_publishes_payload_press(
    hass, key, attribute, expected_payload
) -> None:
    """Pressing a button publishes its configured payload_press verbatim."""
    entity = _entity_for(hass, key, attribute)

    with patch(
        "homeassistant.components.mqtt.async_publish", new_callable=AsyncMock
    ) as mock_pub:
        await entity.async_press()

    mock_pub.assert_called_once_with(
        hass, f"go-eCharger/072246/{key}/set", expected_payload
    )
