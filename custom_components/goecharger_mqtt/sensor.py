"""The go-eCharger (MQTT) sensor."""

import logging

from homeassistant import config_entries, core
from homeassistant.components.sensor import SensorEntity

from .definitions.sensor import SENSORS, GoEChargerSensorEntityDescription
from .entity import GoEChargerEntity, async_add_supported_entities

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: core.HomeAssistant,
    config_entry: config_entries.ConfigEntry,
    async_add_entities,
):
    """Config entry setup."""

    # _LOGGER.debug(
    #     "| Key | Friendly name | Category | Unit | Enabled per default | Supported | Unsupported reason |"
    # )
    # _LOGGER.debug(
    #     "| --- | ------------- | -------- | ---- | ------------------- | --------- | ------------------ |"
    # )
    # for description in SENSORS:
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
    #     native_unit_of_measurement = (
    #         ""
    #         if description.native_unit_of_measurement is None
    #         else description.native_unit_of_measurement
    #     )
    #     entity_category = (
    #         ""
    #         if description.entity_category is None
    #         else f"`{description.entity_category}`"
    #     )
    #     _LOGGER.debug(
    #         f"| `{description.key}` | {description.name} | {entity_category} | {native_unit_of_measurement} | {entity_registry_enabled} | {supported} | {reason} |"
    #     )

    async_add_supported_entities(
        config_entry,
        SENSORS,
        lambda description: GoEChargerSensor(config_entry, description),
        async_add_entities,
    )


class GoEChargerSensor(GoEChargerEntity, SensorEntity):
    """Representation of a go-eCharger sensor that is updated via MQTT."""

    entity_description: GoEChargerSensorEntityDescription

    def __init__(
        self,
        config_entry: config_entries.ConfigEntry,
        description: GoEChargerSensorEntityDescription,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(config_entry, description)

        self.entity_description = description

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
