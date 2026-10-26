"""The go-eCharger (MQTT) switch."""

import logging

from homeassistant import config_entries, core
from homeassistant.components.select import SelectEntity

from .definitions.select import SELECTS, GoEChargerSelectEntityDescription
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
        SELECTS,
        lambda description: GoEChargerSelect(config_entry, description),
        async_add_entities,
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
        assert description.legacy_options is not None
        self._attr_options = list(description.legacy_options.values())
        self._attr_current_option = None

    def key_from_option(self, option: str):
        """Return the option a given payload is assigned to."""
        assert self.entity_description.legacy_options is not None
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
        await self.async_publish_value(self.key_from_option(option))

    async def async_added_to_hass(self):
        """Subscribe to MQTT events."""
        await super().async_added_to_hass()

        def message_received(payload):
            """Handle new MQTT messages."""
            if self.entity_description.state is not None:
                self._attr_current_option = self.entity_description.state(
                    payload, self.entity_description.attribute
                )
            else:
                # if payload is None or payload in ["null", "none"]:
                #     return

                if payload not in self.entity_description.legacy_options:
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

        await self.async_subscribe(message_received)
