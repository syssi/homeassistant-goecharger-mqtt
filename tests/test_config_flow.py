"""Test the go-eCharger (MQTT) config flow."""

from unittest.mock import AsyncMock, patch

from homeassistant import config_entries
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResultType
from pytest_homeassistant_custom_component.common import MockConfigEntry

from custom_components.goecharger_mqtt.config_flow import CannotConnectError
from custom_components.goecharger_mqtt.const import (
    CHARGING_POWER_11KW,
    CHARGING_POWER_22KW,
    CONF_CHARGING_POWER,
    CONF_TOPIC,
    DOMAIN,
)

MQTT_AVAILABLE = patch(
    "custom_components.goecharger_mqtt.config_flow.mqtt.async_wait_for_mqtt_client",
    new_callable=AsyncMock,
    return_value=True,
)

try:
    from homeassistant.components.mqtt import MqttServiceInfo
except ImportError:
    from homeassistant.helpers.service_info.mqtt import MqttServiceInfo


# ---------------------------------------------------------------------------
# Manual user setup
# ---------------------------------------------------------------------------


async def test_form(hass: HomeAssistant) -> None:
    """Test manual setup with a leading-slash topic."""
    with MQTT_AVAILABLE:
        result = await hass.config_entries.flow.async_init(
            DOMAIN, context={"source": config_entries.SOURCE_USER}
        )
    assert result["type"] == FlowResultType.FORM
    assert result["errors"] is None

    with (
        MQTT_AVAILABLE,
        patch(
            "custom_components.goecharger_mqtt.config_flow.PlaceholderHub.validate_device_topic",
            return_value=True,
        ),
        patch(
            "custom_components.goecharger_mqtt.async_setup_entry", return_value=True
        ) as mock_setup_entry,
    ):
        result2 = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            {"topic": "/go-eCharger/012345", "charging_power": CHARGING_POWER_22KW},
        )
        await hass.async_block_till_done()

    assert result2["type"] == FlowResultType.CREATE_ENTRY
    assert result2["title"] == "go-eCharger 012345"
    assert result2["data"] == {
        "topic": "/go-eCharger/012345",
        "charging_power": CHARGING_POWER_22KW,
    }
    assert len(mock_setup_entry.mock_calls) == 1


async def test_form_without_leading_slash(hass: HomeAssistant) -> None:
    """Test manual setup with a topic that has no leading slash."""
    with MQTT_AVAILABLE:
        result = await hass.config_entries.flow.async_init(
            DOMAIN, context={"source": config_entries.SOURCE_USER}
        )

    with (
        MQTT_AVAILABLE,
        patch(
            "custom_components.goecharger_mqtt.config_flow.PlaceholderHub.validate_device_topic",
            return_value=True,
        ),
        patch("custom_components.goecharger_mqtt.async_setup_entry", return_value=True),
    ):
        result2 = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            {"topic": "go-eCharger/012345", "charging_power": CHARGING_POWER_22KW},
        )
        await hass.async_block_till_done()

    assert result2["type"] == FlowResultType.CREATE_ENTRY
    assert result2["title"] == "go-eCharger 012345"
    assert result2["data"] == {
        "topic": "go-eCharger/012345",
        "charging_power": CHARGING_POWER_22KW,
    }


async def test_user_step_aborts_when_mqtt_unavailable(hass: HomeAssistant) -> None:
    """Initiating the user flow without MQTT configured aborts with mqtt_not_available."""
    with patch(
        "custom_components.goecharger_mqtt.config_flow.mqtt.async_wait_for_mqtt_client",
        new_callable=AsyncMock,
        return_value=False,
    ):
        result = await hass.config_entries.flow.async_init(
            DOMAIN, context={"source": config_entries.SOURCE_USER}
        )

    assert result["type"] == FlowResultType.ABORT
    assert result["reason"] == "mqtt_not_available"


async def test_form_cannot_connect(hass: HomeAssistant) -> None:
    """Test we handle cannot connect error."""
    with MQTT_AVAILABLE:
        result = await hass.config_entries.flow.async_init(
            DOMAIN, context={"source": config_entries.SOURCE_USER}
        )

    with (
        MQTT_AVAILABLE,
        patch(
            "custom_components.goecharger_mqtt.config_flow.PlaceholderHub.validate_device_topic",
            side_effect=CannotConnectError,
        ),
    ):
        result2 = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            {"topic": "/go-eCharger/012345", "charging_power": CHARGING_POWER_22KW},
        )

    assert result2["type"] == FlowResultType.FORM
    assert result2["errors"] == {"base": "cannot_connect"}


async def test_form_unknown_error(hass: HomeAssistant) -> None:
    """Test we handle unexpected errors."""
    with MQTT_AVAILABLE:
        result = await hass.config_entries.flow.async_init(
            DOMAIN, context={"source": config_entries.SOURCE_USER}
        )

    with (
        MQTT_AVAILABLE,
        patch(
            "custom_components.goecharger_mqtt.config_flow.PlaceholderHub.validate_device_topic",
            side_effect=Exception("boom"),
        ),
    ):
        result2 = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            {"topic": "/go-eCharger/012345", "charging_power": CHARGING_POWER_22KW},
        )

    assert result2["type"] == FlowResultType.FORM
    assert result2["errors"] == {"base": "unknown"}


# ---------------------------------------------------------------------------
# MQTT discovery
# ---------------------------------------------------------------------------


async def test_mqtt_discovery_with_leading_slash(hass: HomeAssistant) -> None:
    """Test MQTT auto-discovery for firmware that sends /go-eCharger/... topics."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN,
        context={"source": "mqtt"},
        data=MqttServiceInfo(
            topic="/go-eCharger/072246/var",
            payload="",
            qos=0,
            retain=False,
            subscribed_topic="/go-eCharger/+/var",
            timestamp=None,
        ),
    )
    assert result["type"] == FlowResultType.FORM
    assert result["step_id"] == "discovery_confirm"

    with patch(
        "custom_components.goecharger_mqtt.async_setup_entry", return_value=True
    ):
        result2 = await hass.config_entries.flow.async_configure(result["flow_id"], {})
        await hass.async_block_till_done()

    assert result2["type"] == FlowResultType.CREATE_ENTRY
    assert result2["title"] == "go-eCharger 072246"
    assert result2["data"] == {
        "topic": "/go-eCharger/072246",
        CONF_CHARGING_POWER: CHARGING_POWER_22KW,
    }


async def test_mqtt_discovery_without_leading_slash(hass: HomeAssistant) -> None:
    """Test MQTT auto-discovery for firmware that sends go-eCharger/... topics."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN,
        context={"source": "mqtt"},
        data=MqttServiceInfo(
            topic="go-eCharger/072246/var",
            payload="",
            qos=0,
            retain=False,
            subscribed_topic="go-eCharger/+/var",
            timestamp=None,
        ),
    )
    assert result["type"] == FlowResultType.FORM
    assert result["step_id"] == "discovery_confirm"

    with patch(
        "custom_components.goecharger_mqtt.async_setup_entry", return_value=True
    ):
        result2 = await hass.config_entries.flow.async_configure(result["flow_id"], {})
        await hass.async_block_till_done()

    assert result2["type"] == FlowResultType.CREATE_ENTRY
    assert result2["data"] == {
        "topic": "go-eCharger/072246",
        CONF_CHARGING_POWER: CHARGING_POWER_22KW,
    }


async def test_mqtt_discovery_payload_11_sets_11kw(hass: HomeAssistant) -> None:
    """Discovery with payload '11' stores 11 kW charging power."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN,
        context={"source": "mqtt"},
        data=MqttServiceInfo(
            topic="go-eCharger/072246/var",
            payload="11",
            qos=0,
            retain=False,
            subscribed_topic="go-eCharger/+/var",
            timestamp=None,
        ),
    )
    with patch(
        "custom_components.goecharger_mqtt.async_setup_entry", return_value=True
    ):
        result2 = await hass.config_entries.flow.async_configure(result["flow_id"], {})
        await hass.async_block_till_done()

    assert result2["type"] == FlowResultType.CREATE_ENTRY
    assert result2["data"][CONF_CHARGING_POWER] == CHARGING_POWER_11KW


async def test_mqtt_discovery_payload_22_sets_22kw(hass: HomeAssistant) -> None:
    """Discovery with payload '22' stores 22 kW charging power."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN,
        context={"source": "mqtt"},
        data=MqttServiceInfo(
            topic="go-eCharger/072246/var",
            payload="22",
            qos=0,
            retain=False,
            subscribed_topic="go-eCharger/+/var",
            timestamp=None,
        ),
    )
    with patch(
        "custom_components.goecharger_mqtt.async_setup_entry", return_value=True
    ):
        result2 = await hass.config_entries.flow.async_configure(result["flow_id"], {})
        await hass.async_block_till_done()

    assert result2["type"] == FlowResultType.CREATE_ENTRY
    assert result2["data"][CONF_CHARGING_POWER] == CHARGING_POWER_22KW


async def test_mqtt_discovery_unknown_payload_falls_back_to_22kw(
    hass: HomeAssistant,
) -> None:
    """Discovery with an unexpected payload falls back to 22 kW."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN,
        context={"source": "mqtt"},
        data=MqttServiceInfo(
            topic="go-eCharger/072246/var",
            payload="99",
            qos=0,
            retain=False,
            subscribed_topic="go-eCharger/+/var",
            timestamp=None,
        ),
    )
    with patch(
        "custom_components.goecharger_mqtt.async_setup_entry", return_value=True
    ):
        result2 = await hass.config_entries.flow.async_configure(result["flow_id"], {})
        await hass.async_block_till_done()

    assert result2["type"] == FlowResultType.CREATE_ENTRY
    assert result2["data"][CONF_CHARGING_POWER] == CHARGING_POWER_22KW


async def test_reconfigure_updates_topic(hass: HomeAssistant) -> None:
    """Reconfigure flow lets the user correct the topic (e.g. after a firmware update)."""
    entry = MockConfigEntry(
        domain=DOMAIN,
        data={CONF_TOPIC: "go-eCharger/072246"},
        version=3,
        unique_id="072246",
    )
    entry.add_to_hass(hass)

    result = await hass.config_entries.flow.async_init(
        DOMAIN,
        context={
            "source": config_entries.SOURCE_RECONFIGURE,
            "entry_id": entry.entry_id,
        },
    )
    assert result["type"] == FlowResultType.FORM
    assert result["step_id"] == "reconfigure"

    with patch(
        "custom_components.goecharger_mqtt.async_setup_entry", return_value=True
    ):
        result2 = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            {"topic": "/go-eCharger/072246", "charging_power": CHARGING_POWER_22KW},
        )
        await hass.async_block_till_done()

    assert result2["type"] == FlowResultType.ABORT
    assert result2["reason"] == "reconfigure_successful"
    assert entry.data == {
        CONF_TOPIC: "/go-eCharger/072246",
        CONF_CHARGING_POWER: CHARGING_POWER_22KW,
    }


async def test_mqtt_discovery_invalid_serial_aborts(hass: HomeAssistant) -> None:
    """Discovery of a topic whose last segment is not numeric is aborted."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN,
        context={"source": "mqtt"},
        data=MqttServiceInfo(
            topic="/go-eCharger/not-a-serial/var",
            payload="",
            qos=0,
            retain=False,
            subscribed_topic="/go-eCharger/+/var",
            timestamp=None,
        ),
    )
    assert result["type"] == FlowResultType.ABORT
    assert result["reason"] == "invalid_discovery_info"


async def test_form_duplicate_aborts(hass: HomeAssistant) -> None:
    """Manual setup with an already-configured serial number is aborted."""
    with (
        MQTT_AVAILABLE,
        patch(
            "custom_components.goecharger_mqtt.config_flow.PlaceholderHub.validate_device_topic",
            return_value=True,
        ),
        patch("custom_components.goecharger_mqtt.async_setup_entry", return_value=True),
    ):
        result = await hass.config_entries.flow.async_init(
            DOMAIN, context={"source": config_entries.SOURCE_USER}
        )
        await hass.config_entries.flow.async_configure(
            result["flow_id"],
            {"topic": "go-eCharger/012345", "charging_power": CHARGING_POWER_22KW},
        )
        await hass.async_block_till_done()

    with (
        MQTT_AVAILABLE,
        patch(
            "custom_components.goecharger_mqtt.config_flow.PlaceholderHub.validate_device_topic",
            return_value=True,
        ),
    ):
        result2 = await hass.config_entries.flow.async_init(
            DOMAIN, context={"source": config_entries.SOURCE_USER}
        )
        result2 = await hass.config_entries.flow.async_configure(
            result2["flow_id"], {"topic": "/go-eCharger/012345"}
        )

    assert result2["type"] == FlowResultType.ABORT
    assert result2["reason"] == "already_configured"


async def test_mqtt_discovery_duplicate_aborts(hass: HomeAssistant) -> None:
    """A second discovery for the same serial number is aborted."""
    with patch(
        "custom_components.goecharger_mqtt.async_setup_entry", return_value=True
    ):
        result = await hass.config_entries.flow.async_init(
            DOMAIN,
            context={"source": "mqtt"},
            data=MqttServiceInfo(
                topic="/go-eCharger/072246/var",
                payload="",
                qos=0,
                retain=False,
                subscribed_topic="/go-eCharger/+/var",
                timestamp=None,
            ),
        )
        await hass.config_entries.flow.async_configure(result["flow_id"], {})
        await hass.async_block_till_done()

    result2 = await hass.config_entries.flow.async_init(
        DOMAIN,
        context={"source": "mqtt"},
        data=MqttServiceInfo(
            topic="/go-eCharger/072246/var",
            payload="",
            qos=0,
            retain=False,
            subscribed_topic="/go-eCharger/+/var",
            timestamp=None,
        ),
    )
    assert result2["type"] == FlowResultType.ABORT
    assert result2["reason"] == "already_configured"


# ---------------------------------------------------------------------------
# Charging power selection
# ---------------------------------------------------------------------------


async def test_form_11kw_charging_power_stored(hass: HomeAssistant) -> None:
    """Selecting 11 kW stores the correct charging_power in config entry data."""
    with MQTT_AVAILABLE:
        result = await hass.config_entries.flow.async_init(
            DOMAIN, context={"source": config_entries.SOURCE_USER}
        )

    with (
        MQTT_AVAILABLE,
        patch(
            "custom_components.goecharger_mqtt.config_flow.PlaceholderHub.validate_device_topic",
            return_value=True,
        ),
        patch("custom_components.goecharger_mqtt.async_setup_entry", return_value=True),
    ):
        result2 = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            {"topic": "go-eCharger/012345", "charging_power": CHARGING_POWER_11KW},
        )
        await hass.async_block_till_done()

    assert result2["type"] == FlowResultType.CREATE_ENTRY
    assert result2["data"][CONF_CHARGING_POWER] == CHARGING_POWER_11KW


async def test_reconfigure_can_change_model(hass: HomeAssistant) -> None:
    """Reconfigure lets the user switch from 22 kW to 11 kW."""
    entry = MockConfigEntry(
        domain=DOMAIN,
        data={
            CONF_TOPIC: "go-eCharger/072246",
            CONF_CHARGING_POWER: CHARGING_POWER_22KW,
        },
        version=3,
        unique_id="072246",
    )
    entry.add_to_hass(hass)

    result = await hass.config_entries.flow.async_init(
        DOMAIN,
        context={
            "source": config_entries.SOURCE_RECONFIGURE,
            "entry_id": entry.entry_id,
        },
    )

    with patch(
        "custom_components.goecharger_mqtt.async_setup_entry", return_value=True
    ):
        await hass.config_entries.flow.async_configure(
            result["flow_id"],
            {"topic": "go-eCharger/072246", "charging_power": CHARGING_POWER_11KW},
        )
        await hass.async_block_till_done()

    assert entry.data[CONF_CHARGING_POWER] == CHARGING_POWER_11KW


async def test_reconfigure_prefills_existing_model(hass: HomeAssistant) -> None:
    """Reconfigure form shows the currently configured charging power as default."""
    entry = MockConfigEntry(
        domain=DOMAIN,
        data={
            CONF_TOPIC: "go-eCharger/072246",
            CONF_CHARGING_POWER: CHARGING_POWER_11KW,
        },
        version=3,
        unique_id="072246",
    )
    entry.add_to_hass(hass)

    result = await hass.config_entries.flow.async_init(
        DOMAIN,
        context={
            "source": config_entries.SOURCE_RECONFIGURE,
            "entry_id": entry.entry_id,
        },
    )

    assert result["type"] == FlowResultType.FORM
    schema = result["data_schema"].schema
    charger_key = next(k for k in schema if str(k) == CONF_CHARGING_POWER)
    assert charger_key.default() == CHARGING_POWER_11KW
