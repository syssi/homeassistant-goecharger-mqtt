"""Definitions for go-eCharger numbers exposed via MQTT."""
from __future__ import annotations

from dataclasses import dataclass
import logging

from homeassistant.components.number import NumberDeviceClass, NumberEntityDescription
from homeassistant.const import (
    CURRENCY_CENT,
    UnitOfElectricCurrent,
    UnitOfEnergy,
    UnitOfPower,
    UnitOfTime,
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
    treat_zero_as_null: bool = False


NUMBERS: tuple[GoEChargerNumberEntityDescription, ...] = (
    GoEChargerNumberEntityDescription(
        key="ama",
        name="Maximum current limit",
        entity_category=EntityCategory.CONFIG,
        device_class=NumberDeviceClass.CURRENT,
        native_unit_of_measurement=UnitOfElectricCurrent.AMPERE,
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
        native_unit_of_measurement=UnitOfElectricCurrent.AMPERE,
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
        native_unit_of_measurement=UnitOfEnergy.WATT_HOUR,
        entity_registry_enabled_default=True,
        disabled=False,
        native_max_value=100000,
        native_min_value=1,
        native_step=1,
    ),
    GoEChargerNumberEntityDescription(
        key="pgt",
        name="Grid Target",
        entity_category=EntityCategory.CONFIG,
        device_class=None,
        native_unit_of_measurement=UnitOfPower.WATT,
        entity_registry_enabled_default=True,
        disabled=False,
        native_max_value=10000,
        native_min_value=-10000,
        native_step=1,
    ),
    GoEChargerNumberEntityDescription(
        key="att",
        name="Automatic stop time",
        entity_category=EntityCategory.CONFIG,
        device_class=None,
        native_unit_of_measurement=UnitOfTime.SECONDS,
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
        key="dwo",
        name="Charging energy limit",
        entity_category=EntityCategory.CONFIG,
        device_class=NumberDeviceClass.ENERGY,
        native_unit_of_measurement=UnitOfEnergy.WATT_HOUR,
        entity_registry_enabled_default=True,
        disabled=False,
        native_max_value=1000000,
        native_min_value=0,
        native_step=1,
        treat_zero_as_null=True,
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
