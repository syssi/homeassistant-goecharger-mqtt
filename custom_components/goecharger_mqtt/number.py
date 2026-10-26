"""The go-eCharger (MQTT) switch."""

import dataclasses
import logging

from homeassistant import config_entries, core
from homeassistant.components.number import NumberEntity

from .const import CHARGING_POWER_22KW, CHARGING_POWER_MAX_CURRENT, CONF_CHARGING_POWER
from .definitions.number import NUMBERS, GoEChargerNumberEntityDescription
from .entity import GoEChargerEntity, async_add_supported_entities

_LOGGER = logging.getLogger(__name__)

_CURRENT_LIMITED_KEYS = {"amp", "ama"}


async def async_setup_entry(
    hass: core.HomeAssistant,
    config_entry: config_entries.ConfigEntry,
    async_add_entities,
):
    """Config entry setup."""
    model = config_entry.data.get(CONF_CHARGING_POWER, CHARGING_POWER_22KW)
    max_current = CHARGING_POWER_MAX_CURRENT.get(model, 32)

    def create_entity(description):
        desc = (
            dataclasses.replace(description, native_max_value=max_current)
            if description.key in _CURRENT_LIMITED_KEYS
            else description
        )
        if description.key == "dwo" and isinstance(
            config_entry.runtime_data.data, dict
        ):
            desc = dataclasses.replace(desc, native_step=100)
        return GoEChargerNumber(config_entry, desc)

    async_add_supported_entities(
        config_entry,
        NUMBERS,
        create_entity,
        async_add_entities,
    )


class GoEChargerNumber(GoEChargerEntity, NumberEntity):
    """Representation of a go-eCharger switch that is updated via MQTT."""

    entity_description: GoEChargerNumberEntityDescription

    def __init__(
        self,
        config_entry: config_entries.ConfigEntry,
        description: GoEChargerNumberEntityDescription,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(config_entry, description)

        self.entity_description = description

    async def async_set_native_value(self, value: float) -> None:
        """Update the current value."""
        if (
            isinstance(self.coordinator.data, dict)
            and self.entity_description.key == "dwo"
        ):
            await self.async_publish_value(round(value / 100))
            return

        if self.native_step == 1:
            await self.async_publish_value(int(value))
        else:
            await self.async_publish_value(value)

    async def async_added_to_hass(self):
        """Subscribe to MQTT events."""
        await super().async_added_to_hass()

        def message_received(payload):
            """Handle new MQTT messages."""
            if self.entity_description.state is not None:
                self._attr_native_value = self.entity_description.state(
                    payload, self.entity_description.attribute
                )
            elif payload == "null":
                self._attr_native_value = None
            else:
                self._attr_native_value = payload

            self.async_write_ha_state()

        await self.async_subscribe(message_received)
