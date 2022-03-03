"""The go-eCharger (MQTT) button."""
import logging

from homeassistant import config_entries, core
from homeassistant.components import mqtt
from homeassistant.components.button import ButtonEntity

from .definitions.button import BUTTONS, GoEChargerButtonEntityDescription
from .entity import GoEChargerEntity

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: core.HomeAssistant,
    config_entry: config_entries.ConfigEntry,
    async_add_entities,
):
    """Config entry setup."""
    async_add_entities(
        GoEChargerButton(config_entry, description)
        for description in BUTTONS
        if not description.disabled
    )


class GoEChargerButton(GoEChargerEntity, ButtonEntity):
    """Representation of a go-eCharger button that can be toggled using MQTT."""

    entity_description: GoEChargerButtonEntityDescription

    def __init__(
        self,
        config_entry: config_entries.ConfigEntry,
        description: GoEChargerButtonEntityDescription,
    ) -> None:
        """Initialize the binary sensor."""
        self.entity_description = description

        super().__init__(config_entry, description)

    async def async_press(self, **kwargs):
        """Turn the device on.

        This method is a coroutine.
        """
        await mqtt.async_publish(
            self.hass, f"{self._topic}/set", self.entity_description.payload_press
        )
