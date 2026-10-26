"""The go-eCharger (MQTT) switch."""

import logging

from homeassistant import config_entries, core
from homeassistant.components.switch import SwitchEntity

from .definitions.switch import SWITCHES, GoEChargerSwitchEntityDescription
from .entity import GoEChargerEntity, async_add_supported_entities

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: core.HomeAssistant,
    config_entry: config_entries.ConfigEntry,
    async_add_entities,
):
    """Config entry setup."""
    async_add_supported_entities(
        config_entry,
        SWITCHES,
        lambda description: GoEChargerSwitch(config_entry, description),
        async_add_entities,
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
        self._optimistic = self.entity_description.optimistic

    @property
    def assumed_state(self):
        """Return true if we do optimistic updates."""
        return self._optimistic

    async def async_turn_on(self, **kwargs):
        """Turn the switch on."""
        await self.async_publish_value(self.entity_description.payload_on)
        if self._optimistic:
            # Optimistically assume that switch has changed state.
            self._attr_is_on = True
            self.async_write_ha_state()

    async def async_turn_off(self, **kwargs):
        """Turn the switch off."""
        await self.async_publish_value(self.entity_description.payload_off)
        if self._optimistic:
            # Optimistically assume that switch has changed state.
            self._attr_is_on = False
            self.async_write_ha_state()

    async def async_added_to_hass(self):
        """Subscribe to MQTT events."""
        await super().async_added_to_hass()

        def message_received(payload):
            """Handle new MQTT messages."""
            if self.entity_description.state is not None:
                self._attr_is_on = self.entity_description.state(
                    payload, self.entity_description.attribute
                )
            elif payload in (self.entity_description.payload_on, "1", "true"):
                self._attr_is_on = True
            elif payload in (self.entity_description.payload_off, "0", "false"):
                self._attr_is_on = False
            else:
                self._attr_is_on = None

            self.async_write_ha_state()

        await self.async_subscribe(message_received)
