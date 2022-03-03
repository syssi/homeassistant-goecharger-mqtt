"""Definitions for go-eCharger select entities exposed via MQTT."""
from __future__ import annotations

from dataclasses import dataclass
import logging

from homeassistant.components.select import SelectEntityDescription
from homeassistant.helpers.entity import EntityCategory

from . import GoEChargerEntityDescription

_LOGGER = logging.getLogger(__name__)


@dataclass
class GoEChargerSelectEntityDescription(
    GoEChargerEntityDescription, SelectEntityDescription
):
    """Select entity description for go-eCharger."""

    options: dict[str, str] | None = None
    domain: str = "select"


SELECTS: tuple[GoEChargerSelectEntityDescription, ...] = (
    GoEChargerSelectEntityDescription(
        key="lmo",
        name="Logic mode",
        options={
            "3": "Default",
            "4": "Awattar",
            "5": "Automatic Stop",
        },
        entity_category=EntityCategory.CONFIG,
        device_class=None,
        entity_registry_enabled_default=True,
        disabled=False,
    ),
    GoEChargerSelectEntityDescription(
        key="ust",
        name="Cable unlock mode",
        options={
            "0": "Normal",
            "1": "Auto Unlock",
            "2": "Always Locked",
        },
        attribute="ust",
        entity_category=EntityCategory.CONFIG,
        device_class=None,
        icon="mdi:account-lock-open",
        entity_registry_enabled_default=True,
        disabled=False,
    ),
    GoEChargerSelectEntityDescription(
        key="frc",
        name="Force state",
        options={
            "0": "Neutral",
            "1": "Don't charge",
            "2": "Charge",
        },
        attribute="frc",
        entity_category=EntityCategory.CONFIG,
        device_class=None,
        icon="mdi:auto-fix",
        entity_registry_enabled_default=True,
        disabled=False,
    ),
)
