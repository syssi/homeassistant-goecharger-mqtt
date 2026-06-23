"""Test go-eCharger (MQTT) setup: migration and set_config_key service."""

import json
import logging
from unittest.mock import AsyncMock, patch

from homeassistant.core import HomeAssistant
from homeassistant.helpers import device_registry as dr
from pytest_homeassistant_custom_component.common import MockConfigEntry

from custom_components.goecharger_mqtt import async_migrate_entry, async_setup
from custom_components.goecharger_mqtt.const import (
    CHARGING_POWER_22KW,
    CONF_CHARGING_POWER,
    CONF_TOPIC,
    DOMAIN,
)

# ---------------------------------------------------------------------------
# Migration v1 → v3
# ---------------------------------------------------------------------------

_EXPECTED_V3_DATA = {
    CONF_TOPIC: "/go-eCharger/072246",
    CONF_CHARGING_POWER: CHARGING_POWER_22KW,
}


async def test_migration_v1_with_leading_slash(hass: HomeAssistant) -> None:
    """/go-eCharger + 072246 migrates all the way to v3 with charging_power."""
    entry = MockConfigEntry(
        domain=DOMAIN,
        data={"serial_number": "072246", "topic_prefix": "/go-eCharger"},
        version=1,
    )
    entry.add_to_hass(hass)

    assert await async_migrate_entry(hass, entry) is True
    assert entry.version == 3
    assert entry.data == _EXPECTED_V3_DATA


async def test_migration_v1_without_leading_slash(hass: HomeAssistant) -> None:
    """go-eCharger + 072246 migrates to go-eCharger/072246 with charging_power."""
    entry = MockConfigEntry(
        domain=DOMAIN,
        data={"serial_number": "072246", "topic_prefix": "go-eCharger"},
        version=1,
    )
    entry.add_to_hass(hass)

    await async_migrate_entry(hass, entry)

    assert entry.data == {
        CONF_TOPIC: "go-eCharger/072246",
        CONF_CHARGING_POWER: CHARGING_POWER_22KW,
    }


async def test_migration_v1_missing_topic_prefix_uses_default(
    hass: HomeAssistant,
) -> None:
    """Missing topic_prefix in v1 falls back to DEFAULT_TOPIC_PREFIX."""
    entry = MockConfigEntry(
        domain=DOMAIN,
        data={"serial_number": "072246"},
        version=1,
    )
    entry.add_to_hass(hass)

    await async_migrate_entry(hass, entry)

    assert entry.data == {
        CONF_TOPIC: "go-eCharger/072246",
        CONF_CHARGING_POWER: CHARGING_POWER_22KW,
    }


async def test_migration_v1_strips_trailing_slash_from_prefix(
    hass: HomeAssistant,
) -> None:
    """A trailing slash in the old topic_prefix must not produce a double slash."""
    entry = MockConfigEntry(
        domain=DOMAIN,
        data={"serial_number": "072246", "topic_prefix": "go-eCharger/"},
        version=1,
    )
    entry.add_to_hass(hass)

    await async_migrate_entry(hass, entry)

    assert entry.data == {
        CONF_TOPIC: "go-eCharger/072246",
        CONF_CHARGING_POWER: CHARGING_POWER_22KW,
    }


async def test_migration_v2_adds_charging_power(hass: HomeAssistant) -> None:
    """v2 entries get charging_power=22kw added and are bumped to v3."""
    entry = MockConfigEntry(
        domain=DOMAIN,
        data={CONF_TOPIC: "go-eCharger/072246"},
        version=2,
    )
    entry.add_to_hass(hass)

    assert await async_migrate_entry(hass, entry) is True
    assert entry.version == 3
    assert entry.data == {
        CONF_TOPIC: "go-eCharger/072246",
        CONF_CHARGING_POWER: CHARGING_POWER_22KW,
    }


async def test_migration_v1_also_adds_charging_power(hass: HomeAssistant) -> None:
    """v1 entries pass through both migrations and end up at v3 with charging_power."""
    entry = MockConfigEntry(
        domain=DOMAIN,
        data={"serial_number": "072246", "topic_prefix": "go-eCharger"},
        version=1,
    )
    entry.add_to_hass(hass)

    assert await async_migrate_entry(hass, entry) is True
    assert entry.version == 3
    assert entry.data == {
        CONF_TOPIC: "go-eCharger/072246",
        CONF_CHARGING_POWER: CHARGING_POWER_22KW,
    }


# ---------------------------------------------------------------------------
# set_config_key service helpers
# ---------------------------------------------------------------------------


async def _register_service_and_device(hass: HomeAssistant, topic: str):
    """Set up the service and return a device linked to a config entry."""
    await async_setup(hass, {})

    entry = MockConfigEntry(domain=DOMAIN, data={CONF_TOPIC: topic}, version=2)
    entry.add_to_hass(hass)

    serial_number = topic.rstrip("/").split("/")[-1]
    device = dr.async_get(hass).async_get_or_create(
        config_entry_id=entry.entry_id,
        identifiers={(DOMAIN, serial_number)},
        name=f"go-eCharger {serial_number}",
    )
    return device


# ---------------------------------------------------------------------------
# set_config_key service — value formatting
# ---------------------------------------------------------------------------


async def test_service_numeric_value(hass: HomeAssistant) -> None:
    """Numeric strings are published without quoting."""
    device = await _register_service_and_device(hass, "go-eCharger/072246")

    with patch(
        "homeassistant.components.mqtt.async_publish", new_callable=AsyncMock
    ) as mock_pub:
        await hass.services.async_call(
            DOMAIN,
            "set_config_key",
            {"device_id": device.id, "key": "amp", "value": "16"},
            blocking=True,
        )

    mock_pub.assert_called_once_with(hass, "go-eCharger/072246/amp/set", "16")


async def test_service_string_value_is_quoted(hass: HomeAssistant) -> None:
    """Non-boolean string values are JSON-quoted."""
    device = await _register_service_and_device(hass, "go-eCharger/072246")

    with patch(
        "homeassistant.components.mqtt.async_publish", new_callable=AsyncMock
    ) as mock_pub:
        await hass.services.async_call(
            DOMAIN,
            "set_config_key",
            {"device_id": device.id, "key": "fna", "value": "my-charger"},
            blocking=True,
        )

    mock_pub.assert_called_once_with(hass, "go-eCharger/072246/fna/set", '"my-charger"')


async def test_service_bool_true(hass: HomeAssistant) -> None:
    """The string value 'True' is normalised to lowercase 'true'."""
    device = await _register_service_and_device(hass, "go-eCharger/072246")

    with patch(
        "homeassistant.components.mqtt.async_publish", new_callable=AsyncMock
    ) as mock_pub:
        await hass.services.async_call(
            DOMAIN,
            "set_config_key",
            {"device_id": device.id, "key": "bac", "value": "True"},
            blocking=True,
        )

    mock_pub.assert_called_once_with(hass, "go-eCharger/072246/bac/set", "true")


async def test_service_bool_false(hass: HomeAssistant) -> None:
    """The string value 'False' is normalised to lowercase 'false'."""
    device = await _register_service_and_device(hass, "go-eCharger/072246")

    with patch(
        "homeassistant.components.mqtt.async_publish", new_callable=AsyncMock
    ) as mock_pub:
        await hass.services.async_call(
            DOMAIN,
            "set_config_key",
            {"device_id": device.id, "key": "bac", "value": "False"},
            blocking=True,
        )

    mock_pub.assert_called_once_with(hass, "go-eCharger/072246/bac/set", "false")


# ---------------------------------------------------------------------------
# set_config_key service — topic variants
# ---------------------------------------------------------------------------


async def test_service_leading_slash_topic(hass: HomeAssistant) -> None:
    """Leading slash in the device topic is preserved in the published path."""
    device = await _register_service_and_device(hass, "/go-eCharger/072246")

    with patch(
        "homeassistant.components.mqtt.async_publish", new_callable=AsyncMock
    ) as mock_pub:
        await hass.services.async_call(
            DOMAIN,
            "set_config_key",
            {"device_id": device.id, "key": "amp", "value": "8"},
            blocking=True,
        )

    mock_pub.assert_called_once_with(hass, "/go-eCharger/072246/amp/set", "8")


# ---------------------------------------------------------------------------
# set_config_key service — error paths
# ---------------------------------------------------------------------------


async def test_service_unknown_device_logs_error(hass: HomeAssistant, caplog) -> None:
    """An unknown device_id logs an error and does not publish."""
    await async_setup(hass, {})

    with (
        patch(
            "homeassistant.components.mqtt.async_publish", new_callable=AsyncMock
        ) as mock_pub,
        caplog.at_level(logging.ERROR),
    ):
        await hass.services.async_call(
            DOMAIN,
            "set_config_key",
            {"device_id": "nonexistent-id", "key": "amp", "value": "16"},
            blocking=True,
        )

    mock_pub.assert_not_called()
    assert "nonexistent-id" in caplog.text


async def test_service_device_without_matching_entry_logs_error(
    hass: HomeAssistant, caplog
) -> None:
    """A device linked to a different integration logs an error and does not publish."""
    await async_setup(hass, {})

    # Device linked to a config entry from a different domain
    foreign_entry = MockConfigEntry(domain="other_integration", data={}, version=1)
    foreign_entry.add_to_hass(hass)
    device = dr.async_get(hass).async_get_or_create(
        config_entry_id=foreign_entry.entry_id,
        identifiers={("other_integration", "072246")},
    )

    with (
        patch(
            "homeassistant.components.mqtt.async_publish", new_callable=AsyncMock
        ) as mock_pub,
        caplog.at_level(logging.ERROR),
    ):
        await hass.services.async_call(
            DOMAIN,
            "set_config_key",
            {"device_id": device.id, "key": "amp", "value": "16"},
            blocking=True,
        )

    mock_pub.assert_not_called()
    assert device.id in caplog.text


# ---------------------------------------------------------------------------
# update_grid_power service
# ---------------------------------------------------------------------------


async def test_update_grid_power_p_grid_only(hass: HomeAssistant) -> None:
    """Only p_grid publishes a minimal JSON payload."""
    device = await _register_service_and_device(hass, "go-eCharger/072246")

    with patch(
        "homeassistant.components.mqtt.async_publish", new_callable=AsyncMock
    ) as mock_pub:
        await hass.services.async_call(
            DOMAIN,
            "update_grid_power",
            {"device_id": device.id, "power_grid": 500.0},
            blocking=True,
        )

    mock_pub.assert_called_once_with(
        hass, "go-eCharger/072246/ids/set", '{"pGrid": 500.0}'
    )


async def test_update_grid_power_all_fields(hass: HomeAssistant) -> None:
    """All three power values are included in the payload when provided."""
    device = await _register_service_and_device(hass, "go-eCharger/072246")

    with patch(
        "homeassistant.components.mqtt.async_publish", new_callable=AsyncMock
    ) as mock_pub:
        await hass.services.async_call(
            DOMAIN,
            "update_grid_power",
            {
                "device_id": device.id,
                "power_grid": -200.0,
                "power_pv": 1400.0,
                "power_battery": 0.0,
            },
            blocking=True,
        )

    payload = json.loads(mock_pub.call_args[0][2])
    assert payload == {"pGrid": -200.0, "pPv": 1400.0, "pAkku": 0.0}


async def test_update_grid_power_leading_slash_topic(hass: HomeAssistant) -> None:
    """Leading slash in device topic is preserved."""
    device = await _register_service_and_device(hass, "/go-eCharger/072246")

    with patch(
        "homeassistant.components.mqtt.async_publish", new_callable=AsyncMock
    ) as mock_pub:
        await hass.services.async_call(
            DOMAIN,
            "update_grid_power",
            {"device_id": device.id, "power_grid": 0.0},
            blocking=True,
        )

    assert mock_pub.call_args[0][1] == "/go-eCharger/072246/ids/set"


async def test_update_grid_power_unknown_device_logs_error(
    hass: HomeAssistant, caplog
) -> None:
    """An unknown device_id logs an error and does not publish."""
    await async_setup(hass, {})

    with (
        patch(
            "homeassistant.components.mqtt.async_publish", new_callable=AsyncMock
        ) as mock_pub,
        caplog.at_level(logging.ERROR),
    ):
        await hass.services.async_call(
            DOMAIN,
            "update_grid_power",
            {"device_id": "nonexistent-id", "power_grid": 500.0},
            blocking=True,
        )

    mock_pub.assert_not_called()
    assert "nonexistent-id" in caplog.text
