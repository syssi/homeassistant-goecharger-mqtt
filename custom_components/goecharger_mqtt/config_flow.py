"""Config flow for go-eCharger (MQTT) integration."""
from __future__ import annotations

import logging
from typing import Any

from homeassistant import config_entries
from homeassistant.components.mqtt import MqttServiceInfo
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResult
from homeassistant.exceptions import HomeAssistantError
from homeassistant.helpers import config_validation as cv
import voluptuous as vol

from .const import CONF_SERIAL_NUMBER, CONF_TOPIC_PREFIX, DOMAIN

_LOGGER = logging.getLogger(__name__)

DEFAULT_NAME = "go-eCharger"
DEFAULT_TOPIC_PREFIX = "/go-eCharger"

STEP_USER_DATA_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_SERIAL_NUMBER): vol.All(cv.string, vol.Length(min=6, max=6)),
        vol.Optional(CONF_TOPIC_PREFIX, default=DEFAULT_TOPIC_PREFIX): cv.string,
    }
)


class PlaceholderHub:
    """Placeholder class to make tests pass.

    TODO Remove this placeholder class and replace with things from your PyPI package.
    """

    def __init__(self, topic_prefix: str, serial_number: str) -> None:
        """Initialize."""
        self.topic_prefix = topic_prefix
        self.serial_number = serial_number

    async def validate_device_topic(self) -> bool:
        """Test if we can authenticate with the host."""
        return True


async def validate_input(hass: HomeAssistant, data: dict[str, Any]) -> dict[str, Any]:
    """Validate the user input allows us to connect.

    Data has the keys from STEP_USER_DATA_SCHEMA with values provided by the user.
    """
    serial_number = data[CONF_SERIAL_NUMBER]
    hub = PlaceholderHub(data[CONF_TOPIC_PREFIX], serial_number)

    if not await hub.validate_device_topic():
        raise CannotConnect

    return {"title": f"{DEFAULT_NAME} {serial_number}"}


class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for go-eCharger (MQTT)."""

    VERSION = 1

    def __init__(self) -> None:
        """Initialize flow."""
        self._serial_number = None

    async def async_step_mqtt(self, discovery_info: MqttServiceInfo) -> FlowResult:
        """Handle a flow initialized by MQTT discovery."""
        subscribed_topic = discovery_info.subscribed_topic

        # Subscribed topic must be in sync with the manifest.json
        assert subscribed_topic == "/go-eCharger/+/var"

        # Example topic: /go-eCharger/072246/var
        topic = discovery_info.topic
        (prefix, suffix) = subscribed_topic.split("+", 2)
        self._serial_number = topic.replace(prefix, "").replace(suffix, "")

        if not self._serial_number.isnumeric():
            return self.async_abort(reason="invalid_discovery_info")

        await self.async_set_unique_id(self._serial_number)
        self._abort_if_unique_id_configured()

        return await self.async_step_discovery_confirm()

    async def async_step_discovery_confirm(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Confirm the setup."""
        device_name = f"{DEFAULT_NAME} {self._serial_number}"
        if user_input is not None:
            return self.async_create_entry(
                title=device_name,
                data={
                    CONF_SERIAL_NUMBER: self._serial_number,
                    CONF_TOPIC_PREFIX: DEFAULT_TOPIC_PREFIX,
                },
            )

        self._set_confirm_only()
        return self.async_show_form(
            step_id="discovery_confirm",
            description_placeholders={"device_name": device_name},
        )

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle the initial step."""
        if user_input is None:
            return self.async_show_form(
                step_id="user", data_schema=STEP_USER_DATA_SCHEMA
            )

        errors = {}

        try:
            info = await validate_input(self.hass, user_input)
        except CannotConnect:
            errors["base"] = "cannot_connect"
        except InvalidAuth:
            errors["base"] = "invalid_auth"
        except Exception:  # pylint: disable=broad-except
            _LOGGER.exception("Unexpected exception")
            errors["base"] = "unknown"
        else:
            await self.async_set_unique_id(user_input[CONF_SERIAL_NUMBER])
            self._abort_if_unique_id_configured()

            return self.async_create_entry(title=info["title"], data=user_input)

        return self.async_show_form(
            step_id="user", data_schema=STEP_USER_DATA_SCHEMA, errors=errors
        )


class CannotConnect(HomeAssistantError):
    """Error to indicate we cannot connect."""


class InvalidAuth(HomeAssistantError):
    """Error to indicate there is invalid auth."""
