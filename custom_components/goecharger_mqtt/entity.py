"""MQTT component mixins and helpers."""
from homeassistant import config_entries
from homeassistant.helpers.entity import DeviceInfo, Entity
from homeassistant.util import slugify

from .const import (
    CONF_TOPIC,
    DEVICE_INFO_MANUFACTURER,
    DEVICE_INFO_MODEL,
    DOMAIN,
)
from .definitions import GoEChargerEntityDescription


class GoEChargerEntity(Entity):
    """Common go-eCharger entity."""

    def __init__(
        self,
        config_entry: config_entries.ConfigEntry,
        description: GoEChargerEntityDescription,
    ) -> None:
        """Initialize the sensor."""
        topic = config_entry.data[CONF_TOPIC]

        self._topic = f"{topic}/{description.key}"

        slug = slugify(self._topic.replace("/", "_"))
        self.entity_id = f"{description.domain}.{slug}"

        self._attr_unique_id = "-".join(
            [topic, description.domain, description.key, description.attribute]
        )
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, topic)},
            name=config_entry.title,
            manufacturer=DEVICE_INFO_MANUFACTURER,
            model=DEVICE_INFO_MODEL,
        )
