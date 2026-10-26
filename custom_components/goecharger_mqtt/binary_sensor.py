"""The go-eCharger (MQTT) binary sensor."""

import logging

from homeassistant import config_entries, core
from homeassistant.components.binary_sensor import BinarySensorEntity

from .const import API_VERSION_V1
from .definitions.binary_sensor import (
    BINARY_SENSORS,
    GoEChargerBinarySensorEntityDescription,
)
from .entity import GoEChargerEntity, async_add_supported_entities

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: core.HomeAssistant,
    config_entry: config_entries.ConfigEntry,
    async_add_entities,
):
    """Config entry setup."""

    # _LOGGER.debug(
    #     "| Topic | Friendly name | Category | Enabled per default | Supported | Unsupported reason |"
    # )
    # _LOGGER.debug(
    #     "| ----- | ------------- | -------- | ------------------- | --------- | ------------------ |"
    # )
    # for description in BINARY_SENSORS:
    #     entity_registry_enabled = (
    #         ":heavy_check_mark:"
    #         if description.entity_registry_enabled_default
    #         else ":white_large_square:"
    #     )
    #     supported = ":heavy_check_mark:" if not description.disabled else ":x:"
    #     reason = (
    #         "[^1]"
    #         if description.disabled_reason == "Not exposed via MQTT in firmware 053.1"
    #         else description.disabled_reason
    #     )
    #     entity_category = (
    #         ""
    #         if description.entity_category is None
    #         else f"`{description.entity_category}`"
    #     )
    #     _LOGGER.debug(
    #         f"| `{description.key}` | {description.name} | {entity_category} | {entity_registry_enabled} | {supported} | {reason} |"
    #     )

    async_add_supported_entities(
        config_entry,
        BINARY_SENSORS,
        lambda description: GoEChargerBinarySensor(config_entry, description),
        async_add_entities,
    )


class GoEChargerBinarySensor(GoEChargerEntity, BinarySensorEntity):
    """Representation of a go-eCharger sensor that is updated via MQTT."""

    entity_description: GoEChargerBinarySensorEntityDescription

    def __init__(
        self,
        config_entry: config_entries.ConfigEntry,
        description: GoEChargerBinarySensorEntityDescription,
    ) -> None:
        """Initialize the binary sensor."""
        self.entity_description = description

        super().__init__(config_entry, description)

    @property
    def icon(self) -> str | None:
        """Set the icon based on v1 "cdi" (cloud disabled) logic.

        0 = cloud enabled
        1 = cloud disabled
        """

        if (
            self.entity_description.key == "cdi"
            and self.entity_description.api_version == API_VERSION_V1
        ):
            if self.is_on is None:
                return "mdi:cloud-question-outline"
            return "mdi:cloud-off-outline" if self.is_on else "mdi:cloud-check-outline"

        return super().icon

    async def async_added_to_hass(self):
        """Subscribe to MQTT events."""
        await super().async_added_to_hass()

        def message_received(payload):
            """Handle new MQTT messages."""
            if self.entity_description.state is not None:
                self._attr_is_on = self.entity_description.state(
                    payload, self.entity_description.attribute
                )
            elif payload in ("true", "1"):
                self._attr_is_on = True
            elif payload in ("false", "0"):
                self._attr_is_on = False
            else:
                self._attr_is_on = None

            self.async_write_ha_state()

        await self.async_subscribe(message_received)
