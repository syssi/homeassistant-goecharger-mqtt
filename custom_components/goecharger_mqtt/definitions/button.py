"""Definitions for go-eCharger buttons exposed via MQTT."""
from __future__ import annotations

from dataclasses import dataclass
import logging

from homeassistant.components.button import ButtonEntityDescription
from homeassistant.helpers.entity import EntityCategory

from . import GoEChargerEntityDescription

_LOGGER = logging.getLogger(__name__)


@dataclass
class GoEChargerButtonEntityDescription(
    GoEChargerEntityDescription, ButtonEntityDescription
):
    """Button entity description for go-eCharger."""

    domain: str = "button"
    payload_press: str = "true"


BUTTONS: tuple[GoEChargerButtonEntityDescription, ...] = (
    GoEChargerButtonEntityDescription(
        key="rst",
        name="Restart device",
        payload_press="true",
        entity_category=EntityCategory.CONFIG,
        device_class=None,
        icon="mdi:restart",
        entity_registry_enabled_default=True,
        disabled=False,
    ),
    GoEChargerButtonEntityDescription(
        key="frc",
        name="Force state neutral",
        attribute="0",
        payload_press="0",
        entity_category=EntityCategory.CONFIG,
        device_class=None,
        icon="mdi:auto-fix",
        entity_registry_enabled_default=False,
        disabled=False,
    ),
    GoEChargerButtonEntityDescription(
        key="frc",
        name="Force state dont charge",
        attribute="1",
        payload_press="1",
        entity_category=EntityCategory.CONFIG,
        device_class=None,
        icon="mdi:auto-fix",
        entity_registry_enabled_default=False,
        disabled=False,
    ),
    GoEChargerButtonEntityDescription(
        key="frc",
        name="Force state charge",
        attribute="2",
        payload_press="2",
        entity_category=EntityCategory.CONFIG,
        device_class=None,
        icon="mdi:auto-fix",
        entity_registry_enabled_default=False,
        disabled=False,
    ),
)
