"""The go-eCharger (MQTT) integration."""

from __future__ import annotations

import asyncio
import json
import logging
from typing import Any

from homeassistant.components import mqtt
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import CALLBACK_TYPE, HomeAssistant, ServiceCall, callback
from homeassistant.exceptions import HomeAssistantError
from homeassistant.helpers import device_registry as dr
import homeassistant.helpers.config_validation as cv
from homeassistant.helpers.typing import ConfigType
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator
import voluptuous as vol

from .const import (
    API_VERSION_AUTO,
    API_VERSION_V1,
    API_VERSION_V2,
    ATTR_KEY,
    ATTR_VALUE,
    CHARGING_POWER_22KW,
    CONF_API_VERSION,
    CONF_CHARGING_POWER,
    CONF_SERIAL_NUMBER,
    CONF_TOPIC,
    CONF_TOPIC_PREFIX,
    DEFAULT_TOPIC_PREFIX,
    DOMAIN,
    V1_WRITABLE_KEYS,
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
        vol.Required(ATTR_VALUE): vol.Any(None, cv.string),
    }
)

SERVICE_SCHEMA_UPDATE_GRID_POWER = vol.Schema(
    {
        vol.Required("device_id"): cv.string,
        vol.Required("power_grid"): vol.Coerce(float),
        vol.Optional("power_pv"): vol.Coerce(float),
        vol.Optional("power_battery"): vol.Coerce(float),
    }
)


async def async_migrate_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Migrate config entries to the current version."""
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

    if entry.version == 2:
        hass.config_entries.async_update_entry(
            entry,
            data={**entry.data, CONF_CHARGING_POWER: CHARGING_POWER_22KW},
            version=3,
        )
        _LOGGER.info(
            "Migrated config entry %s to v3: charging_power=%s",
            entry.entry_id,
            CHARGING_POWER_22KW,
        )

    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up go-eCharger (MQTT) from a config entry."""
    coordinator: DataUpdateCoordinator[dict[str, Any] | str] = DataUpdateCoordinator(
        hass,
        _LOGGER,
        config_entry=entry,
        name=f"goecharger_mqtt_{entry.entry_id}",
    )
    coordinator.last_update_success = False
    entry.runtime_data = coordinator

    topic = entry.data[CONF_TOPIC]
    api_version = entry.data.get(CONF_API_VERSION, API_VERSION_AUTO)
    _timeout_handle: asyncio.TimerHandle | None = None
    unsubscribers: dict[str, CALLBACK_TYPE] = {}

    @callback
    def _on_heartbeat(message, version: str, data: dict | None = None):
        nonlocal api_version
        nonlocal _timeout_handle
        if api_version == API_VERSION_AUTO:
            api_version = version
            hass.config_entries.async_update_entry(
                entry,
                data={**entry.data, CONF_API_VERSION: version},
            )
            for subscribed_version, unsubscribe in tuple(unsubscribers.items()):
                if subscribed_version != version:
                    unsubscribe()
                    unsubscribers.pop(subscribed_version)

        if _timeout_handle:
            _timeout_handle.cancel()
        if version == API_VERSION_V2:
            updated_data = API_VERSION_V2
        else:
            assert data is not None
            updated_data = data
        coordinator.async_set_updated_data(updated_data)
        _timeout_handle = hass.loop.call_later(HEARTBEAT_TIMEOUT, _on_timeout)

    @callback
    def _on_v2(message):
        _on_heartbeat(message, API_VERSION_V2)

    @callback
    def _on_v1(message):
        try:
            data = json.loads(message.payload)
        except (json.JSONDecodeError, TypeError):
            _LOGGER.warning("Invalid go-eCharger status payload on %s", message.topic)
            return

        if not isinstance(data, dict):
            _LOGGER.warning("Invalid go-eCharger status payload on %s", message.topic)
            return

        _on_heartbeat(message, API_VERSION_V1, data)

    def _on_timeout():
        coordinator.async_set_update_error(Exception("Heartbeat timeout"))

    def _track_subscription(version: str, unsubscribe: CALLBACK_TYPE) -> None:
        active = True

        @callback
        def unsubscribe_once() -> None:
            nonlocal active
            if active:
                active = False
                unsubscribe()

        unsubscribers[version] = unsubscribe_once
        entry.async_on_unload(unsubscribe_once)

    # Register mqtt with callback "_on_v2" for v2 devices
    if api_version in (API_VERSION_V2, API_VERSION_AUTO):
        _track_subscription(
            API_VERSION_V2,
            await mqtt.async_subscribe(hass, f"{topic}/utc", _on_v2, 1),
        )
    # Register mqtt with callback "_on_v1" for v2 devices
    if api_version in (API_VERSION_V1, API_VERSION_AUTO):
        _track_subscription(
            API_VERSION_V1,
            await mqtt.async_subscribe(hass, f"{topic}/status", _on_v1, 1),
        )

    def _cancel_timeout() -> None:
        if _timeout_handle:
            _timeout_handle.cancel()

    entry.async_on_unload(_cancel_timeout)

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)


def _format_config_value(value: str | None) -> str:
    """Encode a set_config_key value as an MQTT payload.

    Numbers, booleans and JSON null are published unquoted. Other strings are
    JSON-quoted so the charger treats them as strings.
    """
    if value is None or value.lower() in ("null", "none"):
        return "null"
    if value.isnumeric():
        return value
    if value in ("true", "True"):
        return "true"
    if value in ("false", "False"):
        return "false"
    return f'"{value}"'


def _entry_for_device(hass: HomeAssistant, device_id: str) -> ConfigEntry | None:
    device = dr.async_get(hass).async_get(device_id)
    if device is None:
        _LOGGER.error("Device %s not found", device_id)
        return None
    entry = next(
        (
            e
            for eid in device.config_entries
            if (e := hass.config_entries.async_get_entry(eid)) and e.domain == DOMAIN
        ),
        None,
    )
    if entry is None:
        _LOGGER.error("No %s config entry found for device %s", DOMAIN, device_id)
    return entry


async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """Set up integration."""

    @callback
    async def set_config_key_service(call: ServiceCall) -> None:
        entry = _entry_for_device(hass, call.data["device_id"])
        if entry is None:
            return

        key = call.data[ATTR_KEY]
        # push values via mqtt based on v1 and v2 different
        await _publish_config_value(
            hass,
            entry,
            key,
            _format_config_value(call.data[ATTR_VALUE]),
            v1_value=call.data[ATTR_VALUE],
        )

    async def update_grid_power_service(call: ServiceCall) -> None:
        entry = _entry_for_device(hass, call.data["device_id"])
        if entry is None:
            return

        # entry.runtime_data.data is a dict in v1 models
        # entry.runtime_data.data is set to "v2" for v2 models
        # value is set in line 131
        if isinstance(entry.runtime_data.data, dict):
            raise HomeAssistantError(
                "Updating grid power is not supported by the go-eCharger v1 API"
            )

        payload: dict[str, float] = {"pGrid": round(call.data["power_grid"], 1)}
        if "power_pv" in call.data:
            payload["pPv"] = round(call.data["power_pv"], 1)
        if "power_battery" in call.data:
            payload["pAkku"] = round(call.data["power_battery"], 1)

        await mqtt.async_publish(
            hass,
            f"{entry.data[CONF_TOPIC]}/ids/set",
            json.dumps(payload),
        )

    hass.services.async_register(
        DOMAIN,
        "set_config_key",
        set_config_key_service,
        schema=SERVICE_SCHEMA_SET_CONFIG_KEY,
    )
    hass.services.async_register(
        DOMAIN,
        "update_grid_power",
        update_grid_power_service,
        schema=SERVICE_SCHEMA_UPDATE_GRID_POWER,
    )

    return True


async def _publish_config_value(
    hass: HomeAssistant,
    entry: ConfigEntry,
    key: str,
    payload: str,
    *,
    v1_value: str | None,
) -> None:
    """Publish a config value using the command format of the detected API."""
    coordinator: DataUpdateCoordinator = entry.runtime_data
    if isinstance(coordinator.data, dict):
        if key not in V1_WRITABLE_KEYS:
            raise HomeAssistantError(
                f"Setting {key} is not supported by the go-eCharger v1 API"
            )
        value = payload if v1_value is None else v1_value
        if value is None or value.lower() in ("null", "none"):
            value = "null"
        elif value.lower() in ("true", "false"):
            value = "1" if value.lower() == "true" else "0"
        await mqtt.async_publish(
            hass,
            f"{entry.data[CONF_TOPIC]}/cmd/req",
            f"{key}={value}",
        )
        return

    await mqtt.async_publish(
        hass,
        f"{entry.data[CONF_TOPIC]}/{key}/set",
        payload,
    )
