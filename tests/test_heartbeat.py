"""Test heartbeat-based device unavailability."""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from homeassistant.core import HomeAssistant
from pytest_homeassistant_custom_component.common import MockConfigEntry

from custom_components.goecharger_mqtt import async_setup_entry
from custom_components.goecharger_mqtt.const import CONF_TOPIC, DOMAIN

TOPIC = "go-eCharger/072246"


@pytest.fixture
async def entry_with_mocks(hass: HomeAssistant):
    """Config entry with MQTT subscription and call_later captured."""
    entry = MockConfigEntry(domain=DOMAIN, data={CONF_TOPIC: TOPIC}, version=2)
    entry.add_to_hass(hass)

    mqtt_cbs = {}
    timer_cbs = []

    async def fake_subscribe(h, topic, cb, qos):
        mqtt_cbs[topic] = cb
        return lambda: None

    def fake_call_later(delay, fn):
        handle = MagicMock()
        timer_cbs.append(fn)
        return handle

    with (
        patch(
            "homeassistant.components.mqtt.async_subscribe",
            side_effect=fake_subscribe,
        ),
        patch.object(hass.config_entries, "async_forward_entry_setups", new=AsyncMock()),
        patch.object(hass.loop, "call_later", side_effect=fake_call_later),
    ):
        await async_setup_entry(hass, entry)
        yield entry, mqtt_cbs, timer_cbs


async def test_initially_unavailable(entry_with_mocks):
    """Coordinator starts unavailable until first heartbeat arrives."""
    entry, _, _ = entry_with_mocks
    assert entry.runtime_data.last_update_success is False


async def test_heartbeat_makes_available(hass: HomeAssistant, entry_with_mocks):
    """First heartbeat message marks device available."""
    entry, mqtt_cbs, _ = entry_with_mocks

    mqtt_cbs[f"{TOPIC}/utc"](MagicMock())
    await hass.async_block_till_done()

    assert entry.runtime_data.last_update_success is True


async def test_timeout_makes_unavailable(hass: HomeAssistant, entry_with_mocks):
    """10-second silence marks device unavailable."""
    entry, mqtt_cbs, timer_cbs = entry_with_mocks

    mqtt_cbs[f"{TOPIC}/utc"](MagicMock())
    await hass.async_block_till_done()
    assert entry.runtime_data.last_update_success is True

    timer_cbs[-1]()
    await hass.async_block_till_done()
    assert entry.runtime_data.last_update_success is False


async def test_reconnect_restores_availability(hass: HomeAssistant, entry_with_mocks):
    """Heartbeat after timeout makes device available again."""
    entry, mqtt_cbs, timer_cbs = entry_with_mocks

    mqtt_cbs[f"{TOPIC}/utc"](MagicMock())
    await hass.async_block_till_done()

    timer_cbs[-1]()
    await hass.async_block_till_done()
    assert entry.runtime_data.last_update_success is False

    mqtt_cbs[f"{TOPIC}/utc"](MagicMock())
    await hass.async_block_till_done()
    assert entry.runtime_data.last_update_success is True
