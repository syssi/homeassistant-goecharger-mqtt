"""The go-eCharger (MQTT) integration."""

from __future__ import annotations

import asyncio
import logging

from homeassistant.components import mqtt
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, ServiceCall, callback
from homeassistant.helpers import device_registry as dr
import homeassistant.helpers.config_validation as cv
from homeassistant.helpers.typing import ConfigType
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator
import voluptuous as vol

from .const import (
    ATTR_KEY,
    ATTR_VALUE,
    CONF_SERIAL_NUMBER,
    CONF_TOPIC,
    CONF_TOPIC_PREFIX,
    DEFAULT_TOPIC_PREFIX,
    DOMAIN,
)

HEARTBEAT_TIMEOUT = 10

PLATFORMS: list[str] = [
    "binary_sensor",
    "button",
    "number",
    "sensor",
    "select",
    "switch",
]

_LOGGER = logging.getLogger(__name__)

SERVICE_SCHEMA_SET_CONFIG_KEY = vol.Schema(
    {
        vol.Required("device_id"): cv.string,
        vol.Required(ATTR_KEY): cv.string,
        vol.Required(ATTR_VALUE): cv.string,
    }
)


async def async_migrate_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Migrate config entry from v1 (topic_prefix + serial_number) to v2 (topic)."""
    if entry.version == 1:
        topic_prefix = entry.data.get(CONF_TOPIC_PREFIX, DEFAULT_TOPIC_PREFIX).rstrip(
            "/"
        )
        serial_number = entry.data[CONF_SERIAL_NUMBER]
        topic = f"{topic_prefix}/{serial_number}"
        hass.config_entries.async_update_entry(
            entry,
            data={CONF_TOPIC: topic},
            version=2,
        )
        _LOGGER.info("Migrated config entry %s to v2: topic=%s", entry.entry_id, topic)
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up go-eCharger (MQTT) from a config entry."""
    coordinator: DataUpdateCoordinator = DataUpdateCoordinator(
        hass,
        _LOGGER,
        config_entry=entry,
        name=f"goecharger_mqtt_{entry.entry_id}",
    )
    coordinator.last_update_success = False
    entry.runtime_data = coordinator

    topic = entry.data[CONF_TOPIC]
    _timeout_handle: asyncio.TimerHandle | None = None

    @callback
    def _on_heartbeat(message):
        nonlocal _timeout_handle
        if _timeout_handle:
            _timeout_handle.cancel()
        coordinator.async_set_updated_data(None)
        _timeout_handle = hass.loop.call_later(HEARTBEAT_TIMEOUT, _on_timeout)

    def _on_timeout():
        coordinator.async_set_update_error(Exception("Heartbeat timeout"))

    unsub = await mqtt.async_subscribe(hass, f"{topic}/utc", _on_heartbeat, 1)
    entry.async_on_unload(unsub)
    entry.async_on_unload(lambda: _timeout_handle and _timeout_handle.cancel())

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)


async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """Set up integration."""

    @callback
    async def set_config_key_service(call: ServiceCall) -> None:
        device_id = call.data["device_id"]
        key = call.data[ATTR_KEY]
        value = call.data[ATTR_VALUE]

        device = dr.async_get(hass).async_get(device_id)
        if device is None:
            _LOGGER.error("Device %s not found", device_id)
            return

        entry = next(
            (
                e
                for eid in device.config_entries
                if (e := hass.config_entries.async_get_entry(eid))
                and e.domain == DOMAIN
            ),
            None,
        )
        if entry is None:
            _LOGGER.error("No %s config entry found for device %s", DOMAIN, device_id)
            return

        if not value.isnumeric():
            if value in ["true", "True"]:
                value = "true"
            elif value in ["false", "False"]:
                value = "false"
            else:
                value = f'"{value}"'

        await mqtt.async_publish(hass, f"{entry.data[CONF_TOPIC]}/{key}/set", value)

    hass.services.async_register(
        DOMAIN,
        "set_config_key",
        set_config_key_service,
        schema=SERVICE_SCHEMA_SET_CONFIG_KEY,
    )

    return True
