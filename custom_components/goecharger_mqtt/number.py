"""The go-eCharger (MQTT) switch."""
import logging

from homeassistant import config_entries, core
from homeassistant.components import mqtt
from homeassistant.components.number import NumberEntity
from homeassistant.core import callback

from .definitions.number import NUMBERS, GoEChargerNumberEntityDescription
from .entity import GoEChargerEntity

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: core.HomeAssistant,
    config_entry: config_entries.ConfigEntry,
    async_add_entities,
):
    """Config entry setup."""
    async_add_entities(
        GoEChargerNumber(config_entry, description)
        for description in NUMBERS
        if not description.disabled
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
        self._attr_available = False

    async def async_set_native_value(self, value: float) -> None:
        """Update the current value."""
        if self._topic.endswith("/dwo") and value == 0:
            await mqtt.async_publish(self.hass, f"{self._topic}/set", "null")
        else:
            if self.native_step == 1:
                await mqtt.async_publish(self.hass, f"{self._topic}/set", int(value))
            else:
                await mqtt.async_publish(self.hass, f"{self._topic}/set", value)

    async def async_added_to_hass(self):
        """Subscribe to MQTT events."""

        @callback
        def message_received(message):
            """Handle new MQTT messages."""
            self._attr_available = True
            if self.entity_description.state is not None:
                self._attr_native_value = self.entity_description.state(
                    message.payload, self.entity_description.attribute
                )
            else:
                if message.payload == "null":
                    self._attr_native_value = None
                else:
                    self._attr_native_value = message.payload

            self.async_write_ha_state()

        await mqtt.async_subscribe(self.hass, self._topic, message_received, 1)
