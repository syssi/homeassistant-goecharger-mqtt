"""The go-eCharger (MQTT) binary sensor."""
import logging

from homeassistant import config_entries, core
from homeassistant.components import mqtt
from homeassistant.components.binary_sensor import BinarySensorEntity
from homeassistant.core import callback
from homeassistant.util import slugify

from .definitions import BINARY_SENSORS, GoEChargerBinarySensorEntityDescription
from .entity import GoEChargerEntity

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

    async_add_entities(
        GoEChargerBinarySensor(config_entry, description)
        for description in BINARY_SENSORS
        if not description.disabled
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

        slug = slugify(self._topic.replace("/", "_"))
        self.entity_id = f"binary_sensor.{slug}"

    @property
    def available(self):
        """Return True if entity is available."""
        return self._attr_is_on is not None

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
                if message.payload == "true":
                    self._attr_is_on = True
                elif message.payload == "false":
                    self._attr_is_on = False
                else:
                    self._attr_is_on = None

            self.async_write_ha_state()

        await mqtt.async_subscribe(self.hass, self._topic, message_received, 1)
