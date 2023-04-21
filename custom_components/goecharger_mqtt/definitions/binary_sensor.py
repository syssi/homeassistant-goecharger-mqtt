"""Definitions for go-eCharger binary sensors exposed via MQTT."""
from __future__ import annotations

from dataclasses import dataclass
import json
import logging

from homeassistant.components.binary_sensor import BinarySensorEntityDescription
from homeassistant.helpers.entity import EntityCategory

from . import GoEChargerEntityDescription

_LOGGER = logging.getLogger(__name__)


@dataclass
class GoEChargerBinarySensorEntityDescription(
    GoEChargerEntityDescription, BinarySensorEntityDescription
):
    """Binary sensor entity description for go-eCharger."""

    domain: str = "binary_sensor"


def extract_item_from_array_to_bool(value, key) -> bool:
    """Extract item from array to int."""
    return bool(json.loads(value)[int(key)])


def map_car_idle_to_bool(value, key) -> bool:
    """Extract item from array to int."""
    return int(value) > int(key)


BINARY_SENSORS: tuple[GoEChargerBinarySensorEntityDescription, ...] = (
    GoEChargerBinarySensorEntityDescription(
        key="car",
        name="Car connected",
        attribute="1",
        state=map_car_idle_to_bool,
        entity_category=EntityCategory.DIAGNOSTIC,
        device_class=None,
        icon="mdi:car",
        entity_registry_enabled_default=True,
        disabled=False,
    ),
    GoEChargerBinarySensorEntityDescription(
        key="fup",
        name="Use PV Surplus",
        entity_category=EntityCategory.CONFIG,
        device_class=None,
        icon="mdi:solar-power",
        entity_registry_enabled_default=True,
        disabled=False,
    ),
    GoEChargerBinarySensorEntityDescription(
        key="pha",
        name="Phase L1 after contactor",
        attribute="0",
        state=extract_item_from_array_to_bool,
        entity_category=EntityCategory.DIAGNOSTIC,
        device_class=None,
        entity_registry_enabled_default=False,
        disabled=False,
    ),
    GoEChargerBinarySensorEntityDescription(
        key="pha",
        name="Phase L2 after contactor",
        attribute="1",
        state=extract_item_from_array_to_bool,
        entity_category=EntityCategory.DIAGNOSTIC,
        device_class=None,
        entity_registry_enabled_default=False,
        disabled=False,
    ),
    GoEChargerBinarySensorEntityDescription(
        key="pha",
        name="Phase L3 after contactor",
        attribute="2",
        state=extract_item_from_array_to_bool,
        entity_category=EntityCategory.DIAGNOSTIC,
        device_class=None,
        entity_registry_enabled_default=False,
        disabled=False,
    ),
    GoEChargerBinarySensorEntityDescription(
        key="pha",
        name="Phase L1 before contactor",
        attribute="3",
        state=extract_item_from_array_to_bool,
        entity_category=EntityCategory.DIAGNOSTIC,
        device_class=None,
        entity_registry_enabled_default=False,
        disabled=False,
    ),
    GoEChargerBinarySensorEntityDescription(
        key="pha",
        name="Phase L2 before contactor",
        attribute="4",
        state=extract_item_from_array_to_bool,
        entity_category=EntityCategory.DIAGNOSTIC,
        device_class=None,
        entity_registry_enabled_default=False,
        disabled=False,
    ),
    GoEChargerBinarySensorEntityDescription(
        key="pha",
        name="Phase L3 before contactor",
        attribute="5",
        state=extract_item_from_array_to_bool,
        entity_category=EntityCategory.DIAGNOSTIC,
        device_class=None,
        entity_registry_enabled_default=False,
        disabled=False,
    ),
    GoEChargerBinarySensorEntityDescription(
        key="cca",
        name="Cloud websocket use client auth",
        entity_category=EntityCategory.CONFIG,
        device_class=None,
        entity_registry_enabled_default=False,
        disabled=True,
        disabled_reason="Not exposed via MQTT in firmware 053.1",
    ),
    GoEChargerBinarySensorEntityDescription(
        key="ocuca",
        name="OTA cloud use client auth",
        entity_category=EntityCategory.CONFIG,
        device_class=None,
        entity_registry_enabled_default=False,
        disabled=True,
        disabled_reason="Not exposed via MQTT in firmware 053.1",
    ),
    GoEChargerBinarySensorEntityDescription(
        key="sbe",
        name="Secure boot enabled",
        entity_category=None,
        device_class=None,
        entity_registry_enabled_default=False,
        disabled=True,
        disabled_reason="Not exposed via MQTT in firmware 053.1",
    ),
    GoEChargerBinarySensorEntityDescription(
        key="adi",
        name="16A adapter used",
        entity_category=EntityCategory.DIAGNOSTIC,
        device_class=None,
        entity_registry_enabled_default=True,
        disabled=False,
    ),
    GoEChargerBinarySensorEntityDescription(
        key="cpe",
        name="Charge control requests the cp signal enabled or not immediately",
        entity_category=EntityCategory.DIAGNOSTIC,
        device_class=None,
        entity_registry_enabled_default=False,
        disabled=True,
        disabled_reason="Not exposed via MQTT in firmware 053.1",
    ),
    GoEChargerBinarySensorEntityDescription(
        key="cpr",
        name="CP enable request",
        entity_category=EntityCategory.DIAGNOSTIC,
        device_class=None,
        entity_registry_enabled_default=False,
        disabled=True,
        disabled_reason="Not exposed via MQTT in firmware 053.1",
    ),
    GoEChargerBinarySensorEntityDescription(
        key="cws",
        name="Cloud websocket started",
        entity_category=EntityCategory.DIAGNOSTIC,
        device_class=None,
        entity_registry_enabled_default=False,
        disabled=True,
        disabled_reason="Not exposed via MQTT in firmware 053.1",
    ),
    GoEChargerBinarySensorEntityDescription(
        key="cwsc",
        name="Cloud websocket connected",
        entity_category=EntityCategory.DIAGNOSTIC,
        device_class=None,
        entity_registry_enabled_default=False,
        disabled=True,
        disabled_reason="Not exposed via MQTT in firmware 053.1",
    ),
    GoEChargerBinarySensorEntityDescription(
        key="fsp",
        name="Force single phase",
        entity_category=EntityCategory.DIAGNOSTIC,
        device_class=None,
        entity_registry_enabled_default=True,
        disabled=False,
        disabled_reason="Is always false. Please use `psm` instead",
    ),
    GoEChargerBinarySensorEntityDescription(
        key="lwcf",
        name="Last failed WiFi connect",
        entity_category=EntityCategory.DIAGNOSTIC,
        device_class=None,
        entity_registry_enabled_default=False,
        disabled=True,
        disabled_reason="Not exposed via MQTT in firmware 053.1",
    ),
    GoEChargerBinarySensorEntityDescription(
        key="tlf",
        name="Test charging finished",
        entity_category=EntityCategory.DIAGNOSTIC,
        device_class=None,
        entity_registry_enabled_default=False,
        disabled=True,
        disabled_reason="Not exposed via MQTT in firmware 053.1",
    ),
    GoEChargerBinarySensorEntityDescription(
        key="tls",
        name="Test charging started",
        entity_category=EntityCategory.DIAGNOSTIC,
        device_class=None,
        entity_registry_enabled_default=False,
        disabled=True,
        disabled_reason="Not exposed via MQTT in firmware 053.1",
    ),
)
