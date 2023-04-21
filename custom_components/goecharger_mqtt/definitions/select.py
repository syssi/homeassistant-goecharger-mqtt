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

    legacy_options: dict[str, str] | None = None
    domain: str = "select"


SELECTS: tuple[GoEChargerSelectEntityDescription, ...] = (
    GoEChargerSelectEntityDescription(
        key="lmo",
        name="Logic mode",
        legacy_options={
            "3": "Default",
            "4": "Eco mode",
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
        legacy_options={
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
        legacy_options={
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
    GoEChargerSelectEntityDescription(
        key="trx",
        name="Transaction",
        legacy_options={
            "null": "None",
            "0": "Without card",
            "1": "Card 0",
            "2": "Card 1",
            "3": "Card 2",
            "4": "Card 3",
            "5": "Card 4",
            "6": "Card 5",
            "7": "Card 6",
            "8": "Card 7",
            "9": "Card 8",
        },
        attribute="trx",
        entity_category=EntityCategory.CONFIG,
        device_class=None,
        icon="mdi:message-text-lock-outline",
        entity_registry_enabled_default=True,
        disabled=False,
    ),
)
