"""MQTT component mixins and helpers."""
from homeassistant import config_entries
from homeassistant.helpers.entity import DeviceInfo, Entity
from homeassistant.util import slugify

from .const import (
    CONF_SERIAL_NUMBER,
    CONF_TOPIC_PREFIX,
    DEVICE_INFO_MANUFACTURER,
    DEVICE_INFO_MODEL,
    DOMAIN,
)
from .definitions import GoEChargerEntityDescription


class GoEChargerEntity(Entity):
    """Common go-eCharger entity."""
    
    _attr_has_entity_name = True  # for translations

    def __init__(
        self,
        config_entry: config_entries.ConfigEntry,
        description: GoEChargerEntityDescription,
    ) -> None:
        """Initialize the sensor."""
        topic_prefix = config_entry.data[CONF_TOPIC_PREFIX]
        serial_number = config_entry.data[CONF_SERIAL_NUMBER]

        self._topic = f"{topic_prefix}/{serial_number}/{description.key}"

        slug = slugify(self._topic.replace("/", "_"))
        self.entity_id = f"{description.domain}.{slug}"

        self._attr_unique_id = "-".join(
            [serial_number, description.domain, description.key, description.attribute]
        )
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, serial_number)},
            name=config_entry.title,
            manufacturer=DEVICE_INFO_MANUFACTURER,
            model=DEVICE_INFO_MODEL,
        )
        if description.translation_key is not None:
            self._attr_translation_key = description.translation_key.lower()
        else:
            if description.attribute == "":  # default value ignore it
                self._attr_translation_key = description.key.lower()
            else:                             # append attribute to key
                self._attr_translation_key = description.key.lower() + "_" + description.attribute
