"""The go-eCharger (MQTT) integration."""
from __future__ import annotations

import logging

from homeassistant.components import mqtt
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, ServiceCall, callback
import homeassistant.helpers.config_validation as cv
from homeassistant.helpers.typing import ConfigType
import voluptuous as vol

from .const import (
    ATTR_KEY,
    ATTR_SERIAL_NUMBER,
    ATTR_VALUE,
    CONF_SERIAL_NUMBER,
    CONF_TOPIC_PREFIX,
    DEFAULT_TOPIC_PREFIX,
    DOMAIN,
)

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
        vol.Required(ATTR_SERIAL_NUMBER): cv.string,
        vol.Required(ATTR_KEY): cv.string,
        vol.Required(ATTR_VALUE): cv.string,
    }
)


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up go-eCharger (MQTT) from a config entry."""
    hass.data.setdefault(DOMAIN, {})
    
    # Store config entries for service access
    if DOMAIN not in hass.data:
        hass.data[DOMAIN] = {}
    hass.data[DOMAIN][entry.data[CONF_SERIAL_NUMBER]] = entry
    
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    
    # Remove config entry from storage
    if unload_ok:
        hass.data[DOMAIN].pop(entry.data[CONF_SERIAL_NUMBER], None)
    
    return unload_ok


async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """Set up integration."""

    @callback
    async def set_config_key_service(call: ServiceCall) -> None:
        serial_number = call.data.get(ATTR_SERIAL_NUMBER)
        key = call.data.get(ATTR_KEY)
        value = call.data.get(ATTR_VALUE)
        
        # Retrieve the topic_prefix from config_entry
        topic_prefix = DEFAULT_TOPIC_PREFIX
        if DOMAIN in hass.data and serial_number in hass.data[DOMAIN]:
            entry = hass.data[DOMAIN][serial_number]
            topic_prefix = entry.data.get(CONF_TOPIC_PREFIX, DEFAULT_TOPIC_PREFIX)
        else:
            _LOGGER.warning(
                "No config entry found for serial number %s, using default topic prefix %s",
                serial_number,
                DEFAULT_TOPIC_PREFIX,
            )
        
        topic = f"{topic_prefix}/{serial_number}/{key}/set"
        
        # Handle value formatting
        if not value.isnumeric():
            if value in ["true", "True"]:
                value = "true"
            elif value in ["false", "False"]:
                value = "false"
            else:
                value = f'"{value}"'
        
        _LOGGER.debug(
            "Publishing to topic %s with value %s (serial: %s, key: %s)",
            topic,
            value,
            serial_number,
            key,
        )
        
        await mqtt.async_publish(hass, topic, value)

    hass.services.async_register(
        DOMAIN,
        "set_config_key",
        set_config_key_service,
        schema=SERVICE_SCHEMA_SET_CONFIG_KEY,
    )

    return True
