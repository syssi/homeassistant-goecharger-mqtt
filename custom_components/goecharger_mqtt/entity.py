"""MQTT component mixins and helpers."""

import json
import logging

from homeassistant import config_entries
from homeassistant.components import mqtt
from homeassistant.core import callback
from homeassistant.exceptions import HomeAssistantError
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
    DataUpdateCoordinator,
)
from homeassistant.util import slugify

from .const import (
    API_VERSION_V1,
    API_VERSION_V2,
    CONF_TOPIC,
    DEVICE_INFO_MANUFACTURER,
    DEVICE_INFO_MODEL,
    DOMAIN,
    V1_WRITABLE_KEYS,
    normalize_base_topic,
)
from .definitions import GoEChargerEntityDescription

_LOGGER = logging.getLogger(__name__)


def async_add_supported_entities(
    config_entry: config_entries.ConfigEntry,
    descriptions: tuple[GoEChargerEntityDescription, ...],
    create_entity,
    async_add_entities,
) -> None:
    """Add entities for the detected API and exclude missing v1 fields."""
    coordinator: DataUpdateCoordinator = config_entry.runtime_data
    added = False

    @callback
    def add_entities_if_supported() -> None:
        nonlocal added
        if added:
            return

        data = coordinator.data
        if data is None:
            return

        added = True
        # in v1 a single topic is used for all parameters, so data is a dict (json)
        # in v2 every value uses an individual topic, data is a single value
        api_version = API_VERSION_V1 if isinstance(data, dict) else API_VERSION_V2
        async_add_entities(
            create_entity(description)
            for description in descriptions
            if not description.disabled
            and (not isinstance(data, dict) or description.key in data)
            and (
                description.api_version is None
                or description.api_version == api_version
            )
        )

    remove_listener = coordinator.async_add_listener(add_entities_if_supported)
    config_entry.async_on_unload(remove_listener)
    add_entities_if_supported()


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

        self._base_topic = normalize_base_topic(config_entry.data[CONF_TOPIC])
        serial_number = self._base_topic.split("/")[-1]

        self._topic = f"{self._base_topic}/{description.key}"

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

    async def async_subscribe(self, message_received) -> None:
        """Subscribe to the MQTT topic used by the detected API."""

        if not isinstance(self.coordinator.data, dict):

            @callback
            def on_value_message(message) -> None:
                message_received(message.payload)

            self.async_on_remove(
                await mqtt.async_subscribe(self.hass, self._topic, on_value_message, 1)
            )
            return

        @callback
        def on_status_message(message) -> None:
            try:
                status = json.loads(message.payload)
            except (json.JSONDecodeError, TypeError):
                _LOGGER.warning(
                    "Invalid go-eCharger status payload on %s", message.topic
                )
                return

            if not isinstance(status, dict):
                _LOGGER.warning(
                    "Invalid go-eCharger status payload on %s", message.topic
                )
                return

            key = self.entity_description.key
            if key not in status:
                return

            payload = _v1_status_payload(key, status[key])
            if payload is None:
                return
            message_received(payload)

        self.async_on_remove(
            await mqtt.async_subscribe(
                self.hass,
                f"{self._base_topic}/status",
                on_status_message,
                1,
            )
        )

    async def async_publish_value(
        self,
        payload: str | float | None,
        *,
        v1_payload: str | float | None = None,
    ) -> None:
        """Publish a v2 value or a v1 command."""
        if isinstance(self.coordinator.data, dict):
            key = self.entity_description.key
            if key not in V1_WRITABLE_KEYS:
                raise HomeAssistantError(
                    f"Setting {key} is not supported by the go-eCharger v1 API"
                )
            value = payload if v1_payload is None else v1_payload
            await mqtt.async_publish(
                self.hass,
                f"{self._base_topic}/cmd/req",
                f"{key}={_format_v1_value(value)}",
            )
            return

        await mqtt.async_publish(self.hass, f"{self._topic}/set", payload)


def _format_v1_value(value: str | float | None) -> str:
    """Format a v1 command value without the JSON quoting used by v2."""
    if value is None:
        return "null"
    if isinstance(value, str):
        if value.lower() == "true":
            return "1"
        if value.lower() == "false":
            return "0"
    return str(value)


def _v1_status_payload(key: str, value: object) -> str | None:
    """Convert one v1 status field to the entity's expected MQTT payload."""
    if key == "pha":
        value = _v1_phase_status(value)
        if value is None:
            return None
    elif key in ("dws", "dwo", "eto") and value is not None:
        value = _v1_scaled_status(key, value)
        if value is None:
            return None
    elif key == "nrg" and isinstance(value, list):
        value = _v1_energy_status(value)
        if value is None:
            return None

    return _serialize_v1_status_value(value)


def _v1_phase_status(value: object) -> list[bool] | None:
    """Convert the v1 phase bitmask to a list of phase states."""
    if not isinstance(value, (str, int, float)):
        _LOGGER.warning("Invalid phase status in go-eCharger payload")
        return None
    try:
        phase_mask = int(value)
    except (TypeError, ValueError):
        _LOGGER.warning("Invalid phase status in go-eCharger payload")
        return None
    return [bool(phase_mask & (1 << bit)) for bit in range(6)]


def _v1_scaled_status(key: str, value: object) -> float | int | None:
    """Scale a numeric v1 status value to the entity's expected unit."""
    if not isinstance(value, (str, int, float)):
        _LOGGER.warning("Invalid %s value in go-eCharger payload", key)
        return None
    try:
        numeric_value = float(value)
    except (TypeError, ValueError):
        _LOGGER.warning("Invalid %s value in go-eCharger payload", key)
        return None

    factor = {"dws": 1 / 360, "dwo": 100, "eto": 100}[key]
    scaled_value = numeric_value * factor
    if scaled_value.is_integer():
        return int(scaled_value)
    return scaled_value


def _v1_energy_status(value: list[object]) -> list[object] | None:
    """Scale the numeric fields in the v1 energy status array."""
    scaled_value = value.copy()
    for index, factor in {
        4: 0.1,
        5: 0.1,
        6: 0.1,
        7: 100,
        8: 100,
        9: 100,
        10: 100,
        11: 10,
    }.items():
        if index < len(scaled_value):
            item = scaled_value[index]
            if not isinstance(item, (str, int, float)):
                _LOGGER.warning(
                    "Invalid nrg value at index %s in go-eCharger payload",
                    index,
                )
                return None
            try:
                scaled_value[index] = float(item) * factor
            except (TypeError, ValueError):
                _LOGGER.warning(
                    "Invalid nrg value at index %s in go-eCharger payload",
                    index,
                )
                return None
    return scaled_value


def _serialize_v1_status_value(value: object) -> str:
    """Serialize a converted v1 status value as an MQTT payload."""
    if value is None:
        return "null"
    if isinstance(value, (list, dict)):
        return json.dumps(value)
    if isinstance(value, bool):
        return "true" if value else "false"
    return str(value)
