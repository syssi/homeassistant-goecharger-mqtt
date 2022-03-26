"""Definitions for go-eCharger sensors exposed via MQTT."""
from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
import logging

from homeassistant.helpers.entity import EntityDescription

_LOGGER = logging.getLogger(__name__)


class GoEChargerStatusCodes:
    """Status code container."""

    car = {
        0: "",
        1: "Idle",
        2: "Charging",
        3: "Wait for car",
        4: "Complete",
        5: "Error",
    }

    err = {
        0: "",
        1: "Residual current circuit breaker",
        2: "FiDC",
        3: "Phase fault",
        4: "Over voltage",
        5: "Over current",
        6: "Diode",
        7: "Pp Invalid",
        8: "No ground",
        9: "Contactor Stuck",
        10: "Contactor Missing",
        11: "FiUnknown",
        12: "Unknown",
        13: "Over temperature",
        14: "No Comm",
        15: "Lock Stuck Open",
        16: "Lock Stuck Locked",
        17: "Reserved20",
        18: "Reserved21",
        19: "Reserved22",
        20: "Reserved23",
        21: "Reserved24",
    }

    modelStatus = {
        0: "Not charging because no charge control data",
        1: "Not charging because of over temperature",
        2: "Not charging because access control wait",
        3: "Charging because of forced ON",
        4: "Not charging because of forced OFF",
        5: "Not charging because of scheduler",
        6: "Not charging because of energy limit",
        7: "Charging because Awattar price under threshold",
        8: "Charging because of automatic stop test charging",
        9: "Charging because of automatic stop not enough time",
        10: "Charging because of automatic stop",
        11: "Charging because of automatic stop no clock",
        12: "Charging because of PV surplus",
        13: "Charging because of fallback (GoE Default)",
        14: "Charging because of fallback (GoE Scheduler)",
        15: "Charging because of fallback (Default)",
        16: "Not charging because of fallback (GoE Awattar)",
        17: "Not charging because of fallback (Awattar)",
        18: "Not charging because of fallback (Automatic Stop)",
        19: "Charging because of car compatibility (Keep Alive)",
        20: "Charging because charge pause not allowed",
        21: "Unknown",
        22: "Not charging because simulate unplugging",
        23: "Not charging because of phase switch",
        24: "Not charging because of minimum pause duration",
    }

    ust = {
        0: "Normal",
        1: "Auto Unlock",
        2: "Always Locked",
        3: "Force Unlock",
    }

    frc = {
        0: "Neutral",
        1: "Don't charge",
        2: "Charge",
    }

    lmo = {
        3: "Default",
        4: "Awattar",
        5: "Automatic Stop",
    }

    psm = {
        1: "1 Phase",
        2: "3 Phases",
    }


@dataclass
class GoEChargerEntityDescription(EntityDescription):
    """Generic entity description for go-eCharger."""

    state: Callable | None = None
    attribute: str = "0"
    domain: str = "generic"
    disabled: bool | None = None
    disabled_reason: str | None = None
