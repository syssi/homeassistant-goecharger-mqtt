"""Test the go-eCharger (MQTT) config flow."""
from unittest.mock import patch

from homeassistant import config_entries
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import RESULT_TYPE_ABORT, RESULT_TYPE_CREATE_ENTRY, RESULT_TYPE_FORM

from custom_components.goecharger_mqtt.config_flow import CannotConnectError
from custom_components.goecharger_mqtt.const import DOMAIN

try:
    from homeassistant.components.mqtt import MqttServiceInfo
except ImportError:
    from homeassistant.helpers.service_info.mqtt import MqttServiceInfo


# ---------------------------------------------------------------------------
# Manual user setup
# ---------------------------------------------------------------------------

async def test_form(hass: HomeAssistant) -> None:
    """Test manual setup with a leading-slash topic."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )
    assert result["type"] == RESULT_TYPE_FORM
    assert result["errors"] is None

    with patch(
        "custom_components.goecharger_mqtt.config_flow.PlaceholderHub.validate_device_topic",
        return_value=True,
    ), patch(
        "custom_components.goecharger_mqtt.async_setup_entry", return_value=True
    ) as mock_setup_entry:
        result2 = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            {"topic": "/go-eCharger/012345"},
        )
        await hass.async_block_till_done()

    assert result2["type"] == RESULT_TYPE_CREATE_ENTRY
    assert result2["title"] == "go-eCharger 012345"
    assert result2["data"] == {"topic": "/go-eCharger/012345"}
    assert len(mock_setup_entry.mock_calls) == 1


async def test_form_without_leading_slash(hass: HomeAssistant) -> None:
    """Test manual setup with a topic that has no leading slash."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )

    with patch(
        "custom_components.goecharger_mqtt.config_flow.PlaceholderHub.validate_device_topic",
        return_value=True,
    ), patch("custom_components.goecharger_mqtt.async_setup_entry", return_value=True):
        result2 = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            {"topic": "go-eCharger/012345"},
        )
        await hass.async_block_till_done()

    assert result2["type"] == RESULT_TYPE_CREATE_ENTRY
    assert result2["title"] == "go-eCharger 012345"
    assert result2["data"] == {"topic": "go-eCharger/012345"}


async def test_form_cannot_connect(hass: HomeAssistant) -> None:
    """Test we handle cannot connect error."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )

    with patch(
        "custom_components.goecharger_mqtt.config_flow.PlaceholderHub.validate_device_topic",
        side_effect=CannotConnectError,
    ):
        result2 = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            {"topic": "/go-eCharger/012345"},
        )

    assert result2["type"] == RESULT_TYPE_FORM
    assert result2["errors"] == {"base": "cannot_connect"}


async def test_form_unknown_error(hass: HomeAssistant) -> None:
    """Test we handle unexpected errors."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )

    with patch(
        "custom_components.goecharger_mqtt.config_flow.PlaceholderHub.validate_device_topic",
        side_effect=Exception("boom"),
    ):
        result2 = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            {"topic": "/go-eCharger/012345"},
        )

    assert result2["type"] == RESULT_TYPE_FORM
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
    assert result["type"] == RESULT_TYPE_FORM
    assert result["step_id"] == "discovery_confirm"

    with patch("custom_components.goecharger_mqtt.async_setup_entry", return_value=True):
        result2 = await hass.config_entries.flow.async_configure(result["flow_id"], {})
        await hass.async_block_till_done()

    assert result2["type"] == RESULT_TYPE_CREATE_ENTRY
    assert result2["title"] == "go-eCharger 072246"
    assert result2["data"] == {"topic": "/go-eCharger/072246"}


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
    assert result["type"] == RESULT_TYPE_FORM
    assert result["step_id"] == "discovery_confirm"

    with patch("custom_components.goecharger_mqtt.async_setup_entry", return_value=True):
        result2 = await hass.config_entries.flow.async_configure(result["flow_id"], {})
        await hass.async_block_till_done()

    assert result2["type"] == RESULT_TYPE_CREATE_ENTRY
    assert result2["data"] == {"topic": "go-eCharger/072246"}


async def test_reconfigure_updates_topic(hass: HomeAssistant) -> None:
    """Reconfigure flow lets the user correct the topic (e.g. after a firmware update)."""
    from pytest_homeassistant_custom_component.common import MockConfigEntry
    from custom_components.goecharger_mqtt.const import CONF_TOPIC

    entry = MockConfigEntry(
        domain=DOMAIN,
        data={CONF_TOPIC: "go-eCharger/072246"},
        version=2,
        unique_id="072246",
    )
    entry.add_to_hass(hass)

    result = await hass.config_entries.flow.async_init(
        DOMAIN,
        context={"source": config_entries.SOURCE_RECONFIGURE, "entry_id": entry.entry_id},
    )
    assert result["type"] == RESULT_TYPE_FORM
    assert result["step_id"] == "reconfigure"

    with patch("custom_components.goecharger_mqtt.async_setup_entry", return_value=True):
        result2 = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            {"topic": "/go-eCharger/072246"},
        )
        await hass.async_block_till_done()

    assert result2["type"] == RESULT_TYPE_ABORT
    assert result2["reason"] == "reconfigure_successful"
    assert entry.data == {CONF_TOPIC: "/go-eCharger/072246"}


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
    assert result["type"] == RESULT_TYPE_ABORT
    assert result["reason"] == "invalid_discovery_info"


async def test_form_duplicate_aborts(hass: HomeAssistant) -> None:
    """Manual setup with an already-configured serial number is aborted."""
    with patch(
        "custom_components.goecharger_mqtt.config_flow.PlaceholderHub.validate_device_topic",
        return_value=True,
    ), patch("custom_components.goecharger_mqtt.async_setup_entry", return_value=True):
        result = await hass.config_entries.flow.async_init(
            DOMAIN, context={"source": config_entries.SOURCE_USER}
        )
        await hass.config_entries.flow.async_configure(
            result["flow_id"], {"topic": "go-eCharger/012345"}
        )
        await hass.async_block_till_done()

    with patch(
        "custom_components.goecharger_mqtt.config_flow.PlaceholderHub.validate_device_topic",
        return_value=True,
    ):
        result2 = await hass.config_entries.flow.async_init(
            DOMAIN, context={"source": config_entries.SOURCE_USER}
        )
        result2 = await hass.config_entries.flow.async_configure(
            result2["flow_id"], {"topic": "/go-eCharger/012345"}
        )

    assert result2["type"] == RESULT_TYPE_ABORT
    assert result2["reason"] == "already_configured"


async def test_mqtt_discovery_duplicate_aborts(hass: HomeAssistant) -> None:
    """A second discovery for the same serial number is aborted."""
    with patch("custom_components.goecharger_mqtt.async_setup_entry", return_value=True):
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
    assert result2["type"] == RESULT_TYPE_ABORT
    assert result2["reason"] == "already_configured"
