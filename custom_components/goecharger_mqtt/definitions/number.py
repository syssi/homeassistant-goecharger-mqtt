"""Definitions for go-eCharger numbers exposed via MQTT."""
from __future__ import annotations

from dataclasses import dataclass
import logging

from homeassistant.components.number import NumberDeviceClass, NumberEntityDescription
from homeassistant.const import (
    ELECTRIC_CURRENT_AMPERE,
    ENERGY_WATT_HOUR,
    TIME_SECONDS,
    CURRENCY_CENT,
)
from homeassistant.helpers.entity import EntityCategory

from . import GoEChargerEntityDescription

_LOGGER = logging.getLogger(__name__)


@dataclass
class GoEChargerNumberEntityDescription(
    GoEChargerEntityDescription, NumberEntityDescription
):
    """Number entity description for go-eCharger."""

    domain: str = "number"


NUMBERS: tuple[GoEChargerNumberEntityDescription, ...] = (
    GoEChargerNumberEntityDescription(
        key="ama",
        name="Maximum current limit",
        entity_category=EntityCategory.CONFIG,
        device_class=NumberDeviceClass.CURRENT,
        native_unit_of_measurement=ELECTRIC_CURRENT_AMPERE,
        entity_registry_enabled_default=True,
        disabled=False,
        native_max_value=32,
        native_min_value=6,
        native_step=1,
    ),
    GoEChargerNumberEntityDescription(
        key="amp",
        name="Requested current",
        entity_category=EntityCategory.CONFIG,
        device_class=NumberDeviceClass.CURRENT,
        native_unit_of_measurement=ELECTRIC_CURRENT_AMPERE,
        entity_registry_enabled_default=True,
        disabled=False,
        native_max_value=32,
        native_min_value=6,
        native_step=1,
    ),
    GoEChargerNumberEntityDescription(
        key="ate",
        name="Automatic stop energy",
        entity_category=EntityCategory.CONFIG,
        device_class=NumberDeviceClass.ENERGY,
        native_unit_of_measurement=ENERGY_WATT_HOUR,
        entity_registry_enabled_default=True,
        disabled=False,
        native_max_value=100000,
        native_min_value=1,
        native_step=1,
    ),
    GoEChargerNumberEntityDescription(
        key="att",
        name="Automatic stop time",
        entity_category=EntityCategory.CONFIG,
        device_class=None,
        native_unit_of_measurement=TIME_SECONDS,
        entity_registry_enabled_default=True,
        disabled=False,
        native_max_value=86400,
        native_min_value=60,
        native_step=1,
    ),
    GoEChargerNumberEntityDescription(
        key="awp",
        name="Awattar maximum price threshold",
        entity_category=EntityCategory.CONFIG,
        device_class=None,
        native_unit_of_measurement=CURRENCY_CENT,
        entity_registry_enabled_default=True,
        disabled=False,
        native_max_value=100,
        native_min_value=-100,
        native_step=0.1,
    ),
    GoEChargerNumberEntityDescription(
        key="lop",
        name="Load balancing priority",
        entity_category=EntityCategory.CONFIG,
        device_class=None,
        native_unit_of_measurement=None,
        entity_registry_enabled_default=False,
        disabled=True,
        native_max_value=99,
        native_min_value=1,
        native_step=1,
    ),
)
