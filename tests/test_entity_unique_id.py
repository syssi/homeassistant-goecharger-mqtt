"""Verify that entity unique_ids remain stable across refactors.

Any change to GoEChargerEntityDescription.attribute or the unique_id
construction in GoEChargerEntity will cause this test to fail, giving
an early signal before users end up with duplicate entities in HA.

Variants covered:
  - attribute=""  (default)       → fallback "0" keeps historic format
  - attribute="0" (explicit)      → numeric multi-instance, e.g. nrg[0..15]
  - attribute="N" (explicit N>0)  → e.g. pha[1..5], car binary, frc buttons
  - attribute=key (string=key)    → e.g. select.frc, sensor.car, sensor.frc
  - attribute≠key (other string)  → e.g. sensor.awcp (marketprice)
  - leading-slash topic           → serial extraction unaffected by prefix
"""

import pytest
from pytest_homeassistant_custom_component.common import MockConfigEntry

from custom_components.goecharger_mqtt.const import CONF_TOPIC, DOMAIN
from custom_components.goecharger_mqtt.definitions import GoEChargerEntityDescription
from custom_components.goecharger_mqtt.entity import GoEChargerEntity


@pytest.mark.parametrize(
    "topic,key,domain,attribute,expected_uid",
    [
        # --- attribute="" (default) — most sensors, switches, numbers, binary_sensors ---
        # Before #200 these had attribute="0" as default; the fallback must keep them stable.
        ("go-eCharger/072246", "ate",  "sensor",        "", "072246-sensor-ate-0"),
        ("go-eCharger/072246", "bac",  "switch",        "", "072246-switch-bac-0"),
        ("go-eCharger/072246", "amp",  "number",        "", "072246-number-amp-0"),
        ("go-eCharger/072246", "lmo",  "select",        "", "072246-select-lmo-0"),
        ("go-eCharger/072246", "adi",  "binary_sensor", "", "072246-binary_sensor-adi-0"),
        ("go-eCharger/072246", "rst",  "button",        "", "072246-button-rst-0"),

        # --- attribute="0" (explicit) — first element of multi-instance entities ---
        ("go-eCharger/072246", "nrg",  "sensor",        "0",  "072246-sensor-nrg-0"),
        ("go-eCharger/072246", "pha",  "binary_sensor", "0",  "072246-binary_sensor-pha-0"),
        ("go-eCharger/072246", "frc",  "button",        "0",  "072246-button-frc-0"),

        # --- attribute="N" (explicit N>0) — subsequent elements ---
        ("go-eCharger/072246", "nrg",  "sensor",        "15", "072246-sensor-nrg-15"),
        ("go-eCharger/072246", "pha",  "binary_sensor", "5",  "072246-binary_sensor-pha-5"),
        ("go-eCharger/072246", "car",  "binary_sensor", "1",  "072246-binary_sensor-car-1"),
        ("go-eCharger/072246", "frc",  "button",        "1",  "072246-button-frc-1"),
        ("go-eCharger/072246", "frc",  "button",        "2",  "072246-button-frc-2"),

        # --- attribute=key (string equals key) — select & named sensor variants ---
        ("go-eCharger/072246", "frc",  "select",        "frc",         "072246-select-frc-frc"),
        ("go-eCharger/072246", "ust",  "select",        "ust",         "072246-select-ust-ust"),
        ("go-eCharger/072246", "trx",  "select",        "trx",         "072246-select-trx-trx"),
        ("go-eCharger/072246", "psm",  "select",        "psm",         "072246-select-psm-psm"),
        ("go-eCharger/072246", "frc",  "sensor",        "frc",         "072246-sensor-frc-frc"),
        ("go-eCharger/072246", "lmo",  "sensor",        "lmo",         "072246-sensor-lmo-lmo"),
        ("go-eCharger/072246", "car",  "sensor",        "car",         "072246-sensor-car-car"),

        # --- attribute≠key (distinct string) — sensor.awcp uses "marketprice" ---
        ("go-eCharger/072246", "awcp", "sensor",        "marketprice", "072246-sensor-awcp-marketprice"),

        # --- leading-slash topic — serial extracted from last path segment ---
        ("/go-eCharger/072246", "ate", "sensor",        "",  "072246-sensor-ate-0"),
        ("/go-eCharger/072246", "nrg", "sensor",        "0", "072246-sensor-nrg-0"),
        ("/go-eCharger/072246", "frc", "select",        "frc", "072246-select-frc-frc"),
    ],
)
async def test_entity_unique_id_stable(
    hass, topic, key, domain, attribute, expected_uid
) -> None:
    entry = MockConfigEntry(domain=DOMAIN, data={CONF_TOPIC: topic}, version=2)
    entry.add_to_hass(hass)

    description = GoEChargerEntityDescription(key=key, domain=domain, attribute=attribute)
    entity = GoEChargerEntity(entry, description)

    assert entity._attr_unique_id == expected_uid
