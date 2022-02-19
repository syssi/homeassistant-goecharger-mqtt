"""The go-eCharger (MQTT) switch."""
import logging

from homeassistant import config_entries, core
from homeassistant.components import mqtt
from homeassistant.components.switch import SwitchEntity
from homeassistant.core import callback

from .definitions import SWITCHES, GoEChargerSwitchEntityDescription
from .entity import GoEChargerEntity

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: core.HomeAssistant,
    config_entry: config_entries.ConfigEntry,
    async_add_entities,
):
    """Config entry setup."""
    async_add_entities(
        GoEChargerSwitch(config_entry, description)
        for description in SWITCHES
        if not description.disabled
    )


class GoEChargerSwitch(GoEChargerEntity, SwitchEntity):
    """Representation of a go-eCharger switch that is updated via MQTT."""

    entity_description: GoEChargerSwitchEntityDescription

    def __init__(
        self,
        config_entry: config_entries.ConfigEntry,
        description: GoEChargerSwitchEntityDescription,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(config_entry, description)

        self.entity_description = description

    @property
    def available(self):
        """Return True if entity is available."""
        return self._attr_is_on is not None

    async def async_turn_on(self, **kwargs):
        """Turn the switch on."""
        await mqtt.async_publish(
            self.hass, f"{self._topic}/set", self.entity_description.payload_on
        )

    async def async_turn_off(self, **kwargs):
        """Turn the switch off."""
        await mqtt.async_publish(
            self.hass, f"{self._topic}/set", self.entity_description.payload_off
        )

    async def async_added_to_hass(self):
        """Subscribe to MQTT events."""

        @callback
        def message_received(message):
            """Handle new MQTT messages."""
            if self.entity_description.state is not None:
                self._attr_is_on = self.entity_description.state(
                    message.payload, self.entity_description.attribute
                )
            else:
                if message.payload == self.entity_description.payload_on:
                    self._attr_is_on = True
                elif message.payload == self.entity_description.payload_off:
                    self._attr_is_on = False
                else:
                    self._attr_is_on = None

            self.async_write_ha_state()

        await mqtt.async_subscribe(self.hass, self._topic, message_received, 1)
