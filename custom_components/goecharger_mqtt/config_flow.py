"""Config flow for go-eCharger (MQTT) integration."""
from __future__ import annotations

import logging
from typing import Any

from homeassistant import config_entries
from homeassistant.components import mqtt
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResult
from homeassistant.exceptions import HomeAssistantError
from homeassistant.helpers import config_validation as cv
import voluptuous as vol

from .const import CONF_TOPIC, DEFAULT_TOPIC_PREFIX, DOMAIN

try:
    # < HA 2022.8.0
    from homeassistant.components.mqtt import MqttServiceInfo
except ImportError:
    # >= HA 2022.8.0
    from homeassistant.helpers.service_info.mqtt import MqttServiceInfo

_LOGGER = logging.getLogger(__name__)

DEFAULT_NAME = "go-eCharger"

STEP_USER_DATA_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_TOPIC, default=DEFAULT_TOPIC_PREFIX): cv.string,
    }
)


class PlaceholderHub:
    """Placeholder class to make tests pass.

    TODO Remove this placeholder class and replace with things from your PyPI package.
    """

    def __init__(self, topic: str) -> None:
        """Initialize."""
        self.topic = topic

    async def validate_device_topic(self) -> bool:
        """Test if we can authenticate with the host."""
        return True


async def validate_input(hass: HomeAssistant, data: dict[str, Any]) -> dict[str, Any]:
    """Validate the user input allows us to connect.

    Data has the keys from STEP_USER_DATA_SCHEMA with values provided by the user.
    """
    topic = data[CONF_TOPIC]
    hub = PlaceholderHub(topic)

    if not await hub.validate_device_topic():
        raise CannotConnect

    device_name = topic.split("/")[-1]

    return {"title": f"{DEFAULT_NAME} {device_name}"}


class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for go-eCharger (MQTT)."""

    VERSION = 1

    def __init__(self) -> None:
        """Initialize flow."""
        self._topic = None

    async def async_step_mqtt(self, discovery_info: MqttServiceInfo) -> FlowResult:
        """Handle a flow initialized by MQTT discovery."""
        subscribed_topic = discovery_info.subscribed_topic

        # Subscribed topic must be in sync with the manifest.json
        assert subscribed_topic in ["/go-eCharger/+/var", "go-eCharger/+/var"]

        # Example topic: /go-eCharger/072246/var
        self._topic = discovery_info.topic.replace("/var", "")

        await self.async_set_unique_id(self._topic)
        self._abort_if_unique_id_configured()

        return await self.async_step_discovery_confirm()

    async def async_step_discovery_confirm(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Confirm the setup."""
        name = f"{DEFAULT_NAME} {self._serial_number}"
        self.context["title_placeholders"] = {"name": name}

        if user_input is not None:
            return self.async_create_entry(
                title=name,
                data={
                    CONF_TOPIC: self._topic,
                },
            )

        self._set_confirm_only()
        return self.async_show_form(
            step_id="discovery_confirm",
            description_placeholders={"name": name},
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
            await self.async_set_unique_id(user_input[CONF_TOPIC])
            self._abort_if_unique_id_configured()

            return self.async_create_entry(title=info["title"], data=user_input)

        return self.async_show_form(
            step_id="user", data_schema=STEP_USER_DATA_SCHEMA, errors=errors
        )


class CannotConnect(HomeAssistantError):
    """Error to indicate we cannot connect."""


class InvalidAuth(HomeAssistantError):
    """Error to indicate there is invalid auth."""
