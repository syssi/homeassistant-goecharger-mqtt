"""The go-eCharger (MQTT) switch."""
import logging

from homeassistant import config_entries, core
from homeassistant.components import mqtt
from homeassistant.components.select import SelectEntity
from homeassistant.core import callback

from .definitions.select import SELECTS, GoEChargerSelectEntityDescription
from .entity import GoEChargerEntity

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: core.HomeAssistant,
    config_entry: config_entries.ConfigEntry,
    async_add_entities,
):
    """Config entry setup."""
    async_add_entities(
        GoEChargerSelect(config_entry, description)
        for description in SELECTS
        if not description.disabled
    )


class GoEChargerSelect(GoEChargerEntity, SelectEntity):
    """Representation of a go-eCharger switch that is updated via MQTT."""

    entity_description: GoEChargerSelectEntityDescription

    def __init__(
        self,
        config_entry: config_entries.ConfigEntry,
        description: GoEChargerSelectEntityDescription,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(config_entry, description)

        self.entity_description = description
        self._attr_options = list(description.legacy_options.values())
        self._attr_current_option = None

    @property
    def available(self):
        """Return True if entity is available."""
        return self._attr_current_option is not None

    def key_from_option(self, option: str):
        """Return the option a given payload is assigned to."""
        try:
            return next(
                key
                for key, value in self.entity_description.legacy_options.items()
                if value == option
            )
        except StopIteration:
            return None

    async def async_select_option(self, option: str) -> None:
        """Update the current value."""
        await mqtt.async_publish(
            self.hass, f"{self._topic}/set", self.key_from_option(option)
        )

    async def async_added_to_hass(self):
        """Subscribe to MQTT events."""

        @callback
        def message_received(message):
            """Handle new MQTT messages."""
            if self.entity_description.state is not None:
                self._attr_current_option = self.entity_description.state(
                    message.payload, self.entity_description.attribute
                )
            else:
                payload = message.payload
                # if payload is None or payload in ["null", "none"]:
                #     return

                if payload not in self.entity_description.legacy_options.keys():
                    _LOGGER.error(
                        "Invalid option for %s: '%s' (valid options: %s)",
                        self.entity_id,
                        payload,
                        self.options,
                    )
                    return

                self._attr_current_option = self.entity_description.legacy_options[
                    payload
                ]

            self.async_write_ha_state()

        await mqtt.async_subscribe(self.hass, self._topic, message_received, 1)
