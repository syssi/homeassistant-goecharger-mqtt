"""Test go-eCharger (MQTT) number entities."""

from unittest.mock import AsyncMock, MagicMock, patch

from pytest_homeassistant_custom_component.common import MockConfigEntry

from custom_components.goecharger_mqtt.const import CONF_TOPIC, DOMAIN
from custom_components.goecharger_mqtt.definitions.number import NUMBERS
from custom_components.goecharger_mqtt.number import GoEChargerNumber


def _entity_for(hass, key: str) -> GoEChargerNumber:
    """Build a GoEChargerNumber for the given definition key."""
    entry = MockConfigEntry(
        domain=DOMAIN, data={CONF_TOPIC: "go-eCharger/072246"}, version=2
    )
    entry.add_to_hass(hass)
    entry.runtime_data = MagicMock()
    description = next(d for d in NUMBERS if d.key == key)
    entity = GoEChargerNumber(entry, description)
    entity.hass = hass
    return entity


async def test_dwo_zero_publishes_numeric_zero_not_null(hass) -> None:
    """dwo=0 now publishes 0 as-is; clearing the limit is the dedicated button's job."""
    entity = _entity_for(hass, "dwo")

    with patch(
        "homeassistant.components.mqtt.async_publish", new_callable=AsyncMock
    ) as mock_pub:
        await entity.async_set_native_value(0)

    mock_pub.assert_called_once_with(hass, "go-eCharger/072246/dwo/set", 0)
