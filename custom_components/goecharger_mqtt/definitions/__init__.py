"""Definitions for go-eCharger sensors exposed via MQTT."""
from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
import logging

from homeassistant.helpers.entity import EntityDescription

_LOGGER = logging.getLogger(__name__)


@dataclass
class GoEChargerEntityDescription(EntityDescription):
    """Generic entity description for go-eCharger."""

    state: Callable | None = None
    attribute: str = ""
    domain: str = "generic"
    disabled: bool | None = None
    disabled_reason: str | None = None
