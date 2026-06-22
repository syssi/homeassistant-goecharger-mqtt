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
        key="bac",
        name="Button allow current change",
        legacy_options={
            "0": "always_lock",
            "1": "lock_when_car_connected",
            "2": "lock_when_charging",
            "3": "never_lock",
        },
        attribute="bac",
        entity_category=EntityCategory.CONFIG,
        device_class=None,
        entity_registry_enabled_default=True,
        disabled=False,
    ),
    GoEChargerSelectEntityDescription(
        key="sdp",
        name="Button allow force change",
        legacy_options={
            "0": "always_lock",
            "1": "lock_when_car_connected",
            "2": "lock_when_charging",
            "3": "never_lock",
        },
        attribute="sdp",
        entity_category=EntityCategory.CONFIG,
        device_class=None,
        entity_registry_enabled_default=False,
        disabled=True,
        disabled_reason="Not exposed via MQTT in firmware 060.5",
    ),
    GoEChargerSelectEntityDescription(
        key="lmo",
        name="Logic mode",
        legacy_options={
            "3": "default",
            "4": "awattar",
            "5": "auto_stop",
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
            "0": "normal",
            "1": "auto_unlock",
            "2": "always_locked",
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
            "0": "neutral",
            "1": "dont_charge",
            "2": "charge",
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
            "null": "none",
            "0": "without_card",
            "1": "card_0",
            "2": "card_1",
            "3": "card_2",
            "4": "card_3",
            "5": "card_4",
            "6": "card_5",
            "7": "card_6",
            "8": "card_7",
            "9": "card_8",
            "10": "card_9",
        },
        attribute="trx",
        entity_category=EntityCategory.CONFIG,
        device_class=None,
        icon="mdi:message-text-lock-outline",
        entity_registry_enabled_default=True,
        disabled=False,
    ),
    GoEChargerSelectEntityDescription(
        key="psm",
        name="Phase switch mode",
        legacy_options={
            "0": "auto",
            "1": "one_phase",
            "2": "three_phases",
        },
        attribute="psm",
        entity_category=EntityCategory.CONFIG,
        device_class=None,
        icon="mdi:speedometer",
        entity_registry_enabled_default=True,
        disabled=False,
    ),
)
