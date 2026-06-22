"""MQTT component mixins and helpers."""

from homeassistant import config_entries
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.util import slugify

from .const import (
    CONF_TOPIC,
    DEVICE_INFO_MANUFACTURER,
    DEVICE_INFO_MODEL,
    DOMAIN,
)
from .definitions import GoEChargerEntityDescription


class GoEChargerEntity(CoordinatorEntity):
    """Common go-eCharger entity."""

    _attr_has_entity_name = True

    def __init__(
        self,
        config_entry: config_entries.ConfigEntry,
        description: GoEChargerEntityDescription,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(config_entry.runtime_data)

        topic = config_entry.data[CONF_TOPIC]
        serial_number = topic.rstrip("/").split("/")[-1]

        self._topic = f"{topic}/{description.key}"

        slug = slugify(self._topic.replace("/", "_"))
        self.entity_id = f"{description.domain}.{slug}"

        self._attr_unique_id = "-".join(
            [
                serial_number,
                description.domain,
                description.key,
                description.attribute or "0",
            ]
        )
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, serial_number)},
            name=config_entry.title,
            manufacturer=DEVICE_INFO_MANUFACTURER,
            model=DEVICE_INFO_MODEL,
        )

        if description.translation_key is not None:
            self._attr_translation_key = description.translation_key.lower()
        elif description.attribute in ("", description.key):
            self._attr_translation_key = description.key.lower()
        else:
            self._attr_translation_key = (
                description.key.lower() + "_" + description.attribute
            )
