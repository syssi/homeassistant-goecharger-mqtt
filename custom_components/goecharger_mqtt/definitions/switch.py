"""Definitions for go-eCharger switches exposed via MQTT."""
from __future__ import annotations

from dataclasses import dataclass
import logging

from homeassistant.components.switch import SwitchEntityDescription
from homeassistant.helpers.entity import EntityCategory

from . import GoEChargerEntityDescription

_LOGGER = logging.getLogger(__name__)


@dataclass
class GoEChargerSwitchEntityDescription(
    GoEChargerEntityDescription, SwitchEntityDescription
):
    """Switch entity description for go-eCharger."""

    domain: str = "switch"
    payload_on: str = "true"
    payload_off: str = "false"
    optimistic: bool = False


SWITCHES: tuple[GoEChargerSwitchEntityDescription, ...] = (
    GoEChargerSwitchEntityDescription(
        key="bac",
        name="Allow current change by button",
        entity_category=EntityCategory.CONFIG,
        device_class=None,
        entity_registry_enabled_default=True,
        disabled=False,
    ),
    GoEChargerSwitchEntityDescription(
        key="ara",
        name="Automatic stop mode",
        entity_category=EntityCategory.CONFIG,
        device_class=None,
        entity_registry_enabled_default=True,
        disabled=False,
    ),
    GoEChargerSwitchEntityDescription(
        key="wen",
        name="WiFi enabled",
        entity_category=EntityCategory.CONFIG,
        device_class=None,
        entity_registry_enabled_default=False,
        disabled=True,
        disabled_reason="Not exposed via MQTT in firmware 053.1",
    ),
    GoEChargerSwitchEntityDescription(
        key="tse",
        name="Time server enabled",
        entity_category=EntityCategory.CONFIG,
        device_class=None,
        entity_registry_enabled_default=False,
        disabled=True,
        disabled_reason="Not exposed via MQTT in firmware 053.1",
    ),
    GoEChargerSwitchEntityDescription(
        key="sdp",
        name="Button allow force change",
        entity_category=EntityCategory.CONFIG,
        device_class=None,
        entity_registry_enabled_default=False,
        disabled=True,
        disabled_reason="Not exposed via MQTT in firmware 053.1",
    ),
    GoEChargerSwitchEntityDescription(
        key="nmo",
        name="Norway mode",
        entity_category=EntityCategory.CONFIG,
        device_class=None,
        entity_registry_enabled_default=False,
        disabled=True,
        disabled_reason="Not exposed via MQTT in firmware 053.1",
    ),
    GoEChargerSwitchEntityDescription(
        key="lse",
        name="LED off on standby",
        entity_category=EntityCategory.CONFIG,
        device_class=None,
        entity_registry_enabled_default=False,
        disabled=True,
        disabled_reason="Not exposed via MQTT in firmware 053.1",
    ),
    GoEChargerSwitchEntityDescription(
        key="awe",
        name="Awattar mode",
        entity_category=EntityCategory.CONFIG,
        device_class=None,
        entity_registry_enabled_default=True,
        disabled=True,
        disabled_reason="Not exposed via MQTT in firmware 053.1",
    ),
    GoEChargerSwitchEntityDescription(
        key="acp",
        name="Allow charge pause",
        entity_category=EntityCategory.CONFIG,
        device_class=None,
        entity_registry_enabled_default=True,
        disabled=True,
        disabled_reason="Not exposed via MQTT in firmware 053.1",
    ),
    GoEChargerSwitchEntityDescription(
        key="esk",
        name="Energy set",
        entity_category=EntityCategory.CONFIG,
        device_class=None,
        entity_registry_enabled_default=False,
        disabled=True,
        disabled_reason="App only",
    ),
    GoEChargerSwitchEntityDescription(
        key="fup",
        name="Use PV surplus",
        entity_category=EntityCategory.CONFIG,
        device_class=None,
        entity_registry_enabled_default=False,
        icon="mdi:solar-power",
        disabled=False,
    ),
    GoEChargerSwitchEntityDescription(
        key="su",
        name="Simulate unplugging",
        entity_category=EntityCategory.CONFIG,
        device_class=None,
        entity_registry_enabled_default=False,
        disabled=True,
        disabled_reason="Not exposed via MQTT in firmware 053.1",
    ),
    GoEChargerSwitchEntityDescription(
        key="hws",
        name="HTTP STA reachable",
        entity_category=EntityCategory.CONFIG,
        device_class=None,
        entity_registry_enabled_default=False,
        disabled=True,
        disabled_reason="Not exposed via MQTT in firmware 053.1",
    ),
    GoEChargerSwitchEntityDescription(
        key="hsa",
        name="HTTP STA authentication",
        entity_category=EntityCategory.CONFIG,
        device_class=None,
        entity_registry_enabled_default=False,
        disabled=True,
        disabled_reason="Not exposed via MQTT in firmware 053.1",
    ),
    GoEChargerSwitchEntityDescription(
        key="loe",
        name="Load balancing enabled",
        entity_category=EntityCategory.CONFIG,
        device_class=None,
        entity_registry_enabled_default=False,
        icon="mdi:seesaw",
        disabled=True,
        disabled_reason="Not exposed via MQTT in firmware 053.1",
    ),
    GoEChargerSwitchEntityDescription(
        key="upo",
        name="Unlock power outage",
        entity_category=EntityCategory.CONFIG,
        device_class=None,
        entity_registry_enabled_default=False,
        disabled=True,
        disabled_reason="Not exposed via MQTT in firmware 053.1",
    ),
    GoEChargerSwitchEntityDescription(
        key="cwe",
        name="Cloud websocket enabled",
        entity_category=EntityCategory.CONFIG,
        device_class=None,
        entity_registry_enabled_default=False,
        disabled=True,
        disabled_reason="Not exposed via MQTT in firmware 053.1",
    ),
    GoEChargerSwitchEntityDescription(
        key="psm",
        name="Force single phase",
        payload_on="1",
        payload_off="2",
        entity_category=EntityCategory.DIAGNOSTIC,
        device_class=None,
        entity_registry_enabled_default=True,
        disabled=False,
    ),
    GoEChargerSwitchEntityDescription(
        key="sua",
        name="Simulate unplugging permanently",
        optimistic=True,
        entity_category=EntityCategory.CONFIG,
        device_class=None,
        entity_registry_enabled_default=True,
        disabled=False,
    ),
    GoEChargerSwitchEntityDescription(
        key="acs",
        name="Card authorization required",
        payload_on="1",
        payload_off="0",
        entity_category=EntityCategory.CONFIG,
        device_class=None,
        entity_registry_enabled_default=True,
        disabled=False,
    ),
)
