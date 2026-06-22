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
from homeassistant.helpers.selector import SelectSelector, SelectSelectorConfig
import voluptuous as vol

from .const import (
    CHARGING_POWER_11KW,
    CHARGING_POWER_22KW,
    CONF_CHARGING_POWER,
    CONF_TOPIC,
    DEFAULT_TOPIC_PREFIX,
    DOMAIN,
)

try:
    # < HA 2022.8.0
    from homeassistant.components.mqtt import MqttServiceInfo
except ImportError:
    # >= HA 2022.8.0
    from homeassistant.helpers.service_info.mqtt import MqttServiceInfo

_LOGGER = logging.getLogger(__name__)

DEFAULT_NAME = "go-eCharger"

_CHARGING_POWER_SELECTOR = SelectSelector(
    SelectSelectorConfig(
        options=[
            {"value": CHARGING_POWER_11KW, "label": "11 kW (max. 16 A)"},
            {"value": CHARGING_POWER_22KW, "label": "22 kW (max. 32 A)"},
        ]
    )
)

STEP_USER_DATA_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_TOPIC, default=DEFAULT_TOPIC_PREFIX): cv.string,
        vol.Required(CONF_CHARGING_POWER, default=CHARGING_POWER_22KW): _CHARGING_POWER_SELECTOR,
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
    hub = PlaceholderHub(data[CONF_TOPIC])

    if not await hub.validate_device_topic():
        raise CannotConnectError

    serial_number = data[CONF_TOPIC].rstrip("/").split("/")[-1]
    return {"title": f"{DEFAULT_NAME} {serial_number}"}


class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for go-eCharger (MQTT)."""

    VERSION = 3

    def __init__(self) -> None:
        """Initialize flow."""
        self._topic = None
        self._charging_power = CHARGING_POWER_22KW

    async def async_step_mqtt(self, discovery_info: MqttServiceInfo) -> FlowResult:
        """Handle a flow initialized by MQTT discovery."""
        subscribed_topic = discovery_info.subscribed_topic

        # Subscribed topic must be in sync with the manifest.json
        assert subscribed_topic in ["/go-eCharger/+/var", "go-eCharger/+/var"]

        # Example topic: /go-eCharger/072246/var → store as /go-eCharger/072246
        self._topic = discovery_info.topic.replace("/var", "")
        serial_number = self._topic.rstrip("/").split("/")[-1]

        if not serial_number.isnumeric():
            return self.async_abort(reason="invalid_discovery_info")

        self._charging_power = (
            CHARGING_POWER_11KW
            if str(discovery_info.payload).strip() == "11"
            else CHARGING_POWER_22KW
        )

        await self.async_set_unique_id(serial_number)
        self._abort_if_unique_id_configured()

        return await self.async_step_discovery_confirm()

    async def async_step_discovery_confirm(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Confirm the setup."""
        serial_number = self._topic.rstrip("/").split("/")[-1]
        name = f"{DEFAULT_NAME} {serial_number}"
        self.context["title_placeholders"] = {"name": name}

        if user_input is not None:
            return self.async_create_entry(
                title=name,
                data={
                    CONF_TOPIC: self._topic,
                    CONF_CHARGING_POWER: self._charging_power,
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
        if not await mqtt.async_wait_for_mqtt_client(self.hass):
            return self.async_abort(reason="mqtt_not_available")

        if user_input is None:
            return self.async_show_form(
                step_id="user", data_schema=STEP_USER_DATA_SCHEMA
            )

        errors = {}

        try:
            info = await validate_input(self.hass, user_input)
        except CannotConnectError:
            errors["base"] = "cannot_connect"
        except InvalidAuthError:
            errors["base"] = "invalid_auth"
        except Exception:  # pylint: disable=broad-except
            _LOGGER.exception("Unexpected exception")
            errors["base"] = "unknown"
        else:
            serial_number = user_input[CONF_TOPIC].rstrip("/").split("/")[-1]
            await self.async_set_unique_id(serial_number)
            self._abort_if_unique_id_configured()

            return self.async_create_entry(title=info["title"], data=user_input)

        return self.async_show_form(
            step_id="user", data_schema=STEP_USER_DATA_SCHEMA, errors=errors
        )

    async def async_step_reconfigure(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Allow correcting the MQTT topic after initial setup (e.g. after a firmware update)."""
        reconfigure_entry = self._get_reconfigure_entry()

        if user_input is None:
            return self.async_show_form(
                step_id="reconfigure",
                data_schema=vol.Schema(
                    {
                        vol.Required(
                            CONF_TOPIC,
                            default=reconfigure_entry.data.get(
                                CONF_TOPIC, DEFAULT_TOPIC_PREFIX
                            ),
                        ): cv.string,
                        vol.Required(
                            CONF_CHARGING_POWER,
                            default=reconfigure_entry.data.get(
                                CONF_CHARGING_POWER, CHARGING_POWER_22KW
                            ),
                        ): _CHARGING_POWER_SELECTOR,
                    }
                ),
                description_placeholders={
                    "current_topic": reconfigure_entry.data.get(CONF_TOPIC, "")
                },
            )

        self.hass.config_entries.async_update_entry(
            reconfigure_entry,
            data={
                CONF_TOPIC: user_input[CONF_TOPIC],
                CONF_CHARGING_POWER: user_input[CONF_CHARGING_POWER],
            },
        )
        await self.hass.config_entries.async_reload(reconfigure_entry.entry_id)
        return self.async_abort(reason="reconfigure_successful")


class CannotConnectError(HomeAssistantError):
    """Error to indicate we cannot connect."""


class InvalidAuthError(HomeAssistantError):
    """Error to indicate there is invalid auth."""
