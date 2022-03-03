"""Definitions for go-eCharger numbers exposed via MQTT."""
from __future__ import annotations

from dataclasses import dataclass
import logging

from homeassistant.components.number import NumberEntityDescription
from homeassistant.const import (
    DEVICE_CLASS_CURRENT,
    DEVICE_CLASS_ENERGY,
    ELECTRIC_CURRENT_AMPERE,
    ENERGY_WATT_HOUR,
    TIME_SECONDS,
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
        key="amp",
        name="Requested current",
        entity_category=EntityCategory.CONFIG,
        device_class=DEVICE_CLASS_CURRENT,
        unit_of_measurement=ELECTRIC_CURRENT_AMPERE,
        entity_registry_enabled_default=True,
        disabled=False,
        max_value=32,
        min_value=6,
        step=1,
    ),
    GoEChargerNumberEntityDescription(
        key="ate",
        name="Automatic stop energy",
        entity_category=EntityCategory.CONFIG,
        device_class=DEVICE_CLASS_ENERGY,
        unit_of_measurement=ENERGY_WATT_HOUR,
        entity_registry_enabled_default=True,
        disabled=False,
        max_value=100000,
        min_value=1,
        step=1,
    ),
    GoEChargerNumberEntityDescription(
        key="att",
        name="Automatic stop time",
        entity_category=EntityCategory.CONFIG,
        device_class=None,
        unit_of_measurement=TIME_SECONDS,
        entity_registry_enabled_default=True,
        disabled=False,
        max_value=86400,
        min_value=60,
        step=1,
    ),
)
