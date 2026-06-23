"""Verify that entity unique_ids remain stable across refactors.

Any change to GoEChargerEntityDescription.attribute or the unique_id
construction in GoEChargerEntity will cause these tests to fail, giving
an early signal before users end up with duplicate entities in HA.

test_entity_unique_id_stable      — covers one case per logic variant
test_all_entity_unique_ids        — locks down every entity definition (235 entries)
test_entity_snapshot_is_complete  — fails when a new entity is added without
                                    a corresponding entry in _ALL_ENTITIES below
"""

from unittest.mock import MagicMock

import pytest
from pytest_homeassistant_custom_component.common import MockConfigEntry

from custom_components.goecharger_mqtt.const import CONF_TOPIC, DOMAIN
from custom_components.goecharger_mqtt.definitions import GoEChargerEntityDescription
from custom_components.goecharger_mqtt.definitions.binary_sensor import BINARY_SENSORS
from custom_components.goecharger_mqtt.definitions.button import BUTTONS
from custom_components.goecharger_mqtt.definitions.number import NUMBERS
from custom_components.goecharger_mqtt.definitions.select import SELECTS
from custom_components.goecharger_mqtt.definitions.sensor import SENSORS
from custom_components.goecharger_mqtt.definitions.switch import SWITCHES
from custom_components.goecharger_mqtt.entity import GoEChargerEntity

_TOPIC = "go-eCharger/072246"


# ---------------------------------------------------------------------------
# Logic-variant test (documents WHY the formula works)
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "topic,key,domain,attribute,expected_uid",
    [
        # attribute="" (default) — must fall back to "0" to keep pre-#200 unique_id format
        ("go-eCharger/072246", "ate", "sensor", "", "072246-sensor-ate-0"),
        ("go-eCharger/072246", "bac", "select", "bac", "072246-select-bac-bac"),
        ("go-eCharger/072246", "amp", "number", "", "072246-number-amp-0"),
        ("go-eCharger/072246", "lmo", "select", "", "072246-select-lmo-0"),
        (
            "go-eCharger/072246",
            "adi",
            "binary_sensor",
            "",
            "072246-binary_sensor-adi-0",
        ),
        ("go-eCharger/072246", "rst", "button", "", "072246-button-rst-0"),
        # attribute="0" (explicit) — first element of multi-instance entities (nrg, pha, frc buttons)
        ("go-eCharger/072246", "nrg", "sensor", "0", "072246-sensor-nrg-0"),
        (
            "go-eCharger/072246",
            "pha",
            "binary_sensor",
            "0",
            "072246-binary_sensor-pha-0",
        ),
        ("go-eCharger/072246", "frc", "button", "0", "072246-button-frc-0"),
        # attribute="N" (N>0) — subsequent elements of multi-instance entities
        ("go-eCharger/072246", "nrg", "sensor", "15", "072246-sensor-nrg-15"),
        (
            "go-eCharger/072246",
            "pha",
            "binary_sensor",
            "5",
            "072246-binary_sensor-pha-5",
        ),
        (
            "go-eCharger/072246",
            "car",
            "binary_sensor",
            "1",
            "072246-binary_sensor-car-1",
        ),
        ("go-eCharger/072246", "frc", "button", "2", "072246-button-frc-2"),
        # attribute=key — select entities and named sensor variants
        ("go-eCharger/072246", "frc", "select", "frc", "072246-select-frc-frc"),
        ("go-eCharger/072246", "ust", "select", "ust", "072246-select-ust-ust"),
        ("go-eCharger/072246", "trx", "select", "trx", "072246-select-trx-trx"),
        ("go-eCharger/072246", "frc", "sensor", "frc", "072246-sensor-frc-frc"),
        ("go-eCharger/072246", "car", "sensor", "car", "072246-sensor-car-car"),
        # attribute≠key — sensor.awcp exposes the "marketprice" sub-field
        (
            "go-eCharger/072246",
            "awcp",
            "sensor",
            "marketprice",
            "072246-sensor-awcp-marketprice",
        ),
        # psm sensor: #200 incorrectly added attribute="psm", changing uid from psm-0 to psm-psm; reverted
        ("go-eCharger/072246", "psm", "sensor", "", "072246-sensor-psm-0"),
        # leading-slash topic — serial is always the last path segment
        ("/go-eCharger/072246", "ate", "sensor", "", "072246-sensor-ate-0"),
        ("/go-eCharger/072246", "nrg", "sensor", "0", "072246-sensor-nrg-0"),
    ],
)
async def test_entity_unique_id_stable(
    hass, topic, key, domain, attribute, expected_uid
) -> None:
    """Verify unique_id format for one representative case per attribute variant."""
    entry = MockConfigEntry(domain=DOMAIN, data={CONF_TOPIC: topic}, version=2)
    entry.add_to_hass(hass)
    entry.runtime_data = MagicMock()
    entity = GoEChargerEntity(
        entry, GoEChargerEntityDescription(key=key, domain=domain, attribute=attribute)
    )
    assert entity._attr_unique_id == expected_uid


# ---------------------------------------------------------------------------
# Full-coverage snapshot — every entity definition, every platform
# ---------------------------------------------------------------------------

_ALL_ENTITIES = [
    # --- sensor (195 entries) ---
    ("+/result", "sensor", "", "072246-sensor-+/result-0"),
    ("ate", "sensor", "", "072246-sensor-ate-0"),
    ("att", "sensor", "", "072246-sensor-att-0"),
    ("awc", "sensor", "", "072246-sensor-awc-0"),
    ("awp", "sensor", "", "072246-sensor-awp-0"),
    ("cch", "sensor", "", "072246-sensor-cch-0"),
    ("cco", "sensor", "", "072246-sensor-cco-0"),
    ("cfi", "sensor", "", "072246-sensor-cfi-0"),
    ("cid", "sensor", "", "072246-sensor-cid-0"),
    ("clp", "sensor", "", "072246-sensor-clp-0"),
    ("ct", "sensor", "", "072246-sensor-ct-0"),
    ("cwc", "sensor", "", "072246-sensor-cwc-0"),
    ("fna", "sensor", "", "072246-sensor-fna-0"),
    ("frc", "sensor", "frc", "072246-sensor-frc-frc"),
    ("frc", "sensor", "", "072246-sensor-frc-0"),
    ("lbr", "sensor", "", "072246-sensor-lbr-0"),
    ("lmo", "sensor", "lmo", "072246-sensor-lmo-lmo"),
    ("lof", "sensor", "", "072246-sensor-lof-0"),
    ("log", "sensor", "", "072246-sensor-log-0"),
    ("lop", "sensor", "", "072246-sensor-lop-0"),
    ("lot", "sensor", "", "072246-sensor-lot-0"),
    ("loty", "sensor", "", "072246-sensor-loty-0"),
    ("map", "sensor", "", "072246-sensor-map-0"),
    ("mca", "sensor", "", "072246-sensor-mca-0"),
    ("mci", "sensor", "", "072246-sensor-mci-0"),
    ("mcpd", "sensor", "", "072246-sensor-mcpd-0"),
    ("mptwt", "sensor", "", "072246-sensor-mptwt-0"),
    ("mpwst", "sensor", "", "072246-sensor-mpwst-0"),
    ("pass", "sensor", "", "072246-sensor-pass-0"),
    ("psmd", "sensor", "", "072246-sensor-psmd-0"),
    ("sch_satur", "sensor", "", "072246-sensor-sch_satur-0"),
    ("sch_sund", "sensor", "", "072246-sensor-sch_sund-0"),
    ("sch_week", "sensor", "", "072246-sensor-sch_week-0"),
    ("spl3", "sensor", "", "072246-sensor-spl3-0"),
    ("sumd", "sensor", "", "072246-sensor-sumd-0"),
    ("tds", "sensor", "", "072246-sensor-tds-0"),
    ("tof", "sensor", "", "072246-sensor-tof-0"),
    ("ts", "sensor", "", "072246-sensor-ts-0"),
    ("tssi", "sensor", "", "072246-sensor-tssi-0"),
    ("tssm", "sensor", "", "072246-sensor-tssm-0"),
    ("tsss", "sensor", "", "072246-sensor-tsss-0"),
    ("ust", "sensor", "ust", "072246-sensor-ust-ust"),
    ("ust", "sensor", "", "072246-sensor-ust-0"),
    ("wak", "sensor", "", "072246-sensor-wak-0"),
    ("wan", "sensor", "", "072246-sensor-wan-0"),
    ("wifis", "sensor", "", "072246-sensor-wifis-0"),
    ("apd", "sensor", "", "072246-sensor-apd-0"),
    ("arv", "sensor", "", "072246-sensor-arv-0"),
    ("ecf", "sensor", "", "072246-sensor-ecf-0"),
    ("eci", "sensor", "", "072246-sensor-eci-0"),
    ("eem", "sensor", "", "072246-sensor-eem-0"),
    ("efi", "sensor", "", "072246-sensor-efi-0"),
    ("facwak", "sensor", "", "072246-sensor-facwak-0"),
    ("fem", "sensor", "", "072246-sensor-fem-0"),
    ("ffna", "sensor", "", "072246-sensor-ffna-0"),
    ("fwan", "sensor", "", "072246-sensor-fwan-0"),
    ("fwc", "sensor", "", "072246-sensor-fwc-0"),
    ("fwv", "sensor", "", "072246-sensor-fwv-0"),
    ("mod", "sensor", "", "072246-sensor-mod-0"),
    ("oem", "sensor", "", "072246-sensor-oem-0"),
    ("otap", "sensor", "", "072246-sensor-otap-0"),
    ("part", "sensor", "", "072246-sensor-part-0"),
    ("pto", "sensor", "", "072246-sensor-pto-0"),
    ("sse", "sensor", "", "072246-sensor-sse-0"),
    ("typ", "sensor", "", "072246-sensor-typ-0"),
    ("var", "sensor", "", "072246-sensor-var-0"),
    ("del", "sensor", "", "072246-sensor-del-0"),
    ("delw", "sensor", "", "072246-sensor-delw-0"),
    ("lrn", "sensor", "", "072246-sensor-lrn-0"),
    ("oct", "sensor", "", "072246-sensor-oct-0"),
    ("acu", "sensor", "", "072246-sensor-acu-0"),
    ("amt", "sensor", "", "072246-sensor-amt-0"),
    ("atp", "sensor", "", "072246-sensor-atp-0"),
    ("awcp", "sensor", "marketprice", "072246-sensor-awcp-marketprice"),
    ("awpl", "sensor", "", "072246-sensor-awpl-0"),
    ("car", "sensor", "car", "072246-sensor-car-car"),
    ("cbl", "sensor", "", "072246-sensor-cbl-0"),
    ("ccu", "sensor", "", "072246-sensor-ccu-0"),
    ("ccw", "sensor", "", "072246-sensor-ccw-0"),
    ("cdi", "sensor", "1", "072246-sensor-cdi-1"),
    ("cdi", "sensor", "0", "072246-sensor-cdi-0"),
    ("cus", "sensor", "", "072246-sensor-cus-0"),
    ("cus", "sensor", "cus", "072246-sensor-cus-cus"),
    ("cwsca", "sensor", "", "072246-sensor-cwsca-0"),
    ("efh", "sensor", "", "072246-sensor-efh-0"),
    ("efh32", "sensor", "", "072246-sensor-efh32-0"),
    ("efh8", "sensor", "", "072246-sensor-efh8-0"),
    ("ehs", "sensor", "", "072246-sensor-ehs-0"),
    ("emfh", "sensor", "", "072246-sensor-emfh-0"),
    ("emhb", "sensor", "", "072246-sensor-emhb-0"),
    ("err", "sensor", "err", "072246-sensor-err-err"),
    ("err", "sensor", "", "072246-sensor-err-0"),
    ("esr", "sensor", "", "072246-sensor-esr-0"),
    ("eto", "sensor", "", "072246-sensor-eto-0"),
    ("etop", "sensor", "", "072246-sensor-etop-0"),
    ("ffb", "sensor", "", "072246-sensor-ffb-0"),
    ("ffba", "sensor", "", "072246-sensor-ffba-0"),
    ("fhz", "sensor", "", "072246-sensor-fhz-0"),
    ("fsptws", "sensor", "", "072246-sensor-fsptws-0"),
    ("host", "sensor", "", "072246-sensor-host-0"),
    ("lbp", "sensor", "", "072246-sensor-lbp-0"),
    ("lccfc", "sensor", "", "072246-sensor-lccfc-0"),
    ("lccfi", "sensor", "", "072246-sensor-lccfi-0"),
    ("lcctc", "sensor", "", "072246-sensor-lcctc-0"),
    ("lck", "sensor", "", "072246-sensor-lck-0"),
    ("led", "sensor", "", "072246-sensor-led-0"),
    ("lfspt", "sensor", "", "072246-sensor-lfspt-0"),
    ("lmsc", "sensor", "", "072246-sensor-lmsc-0"),
    ("loa", "sensor", "", "072246-sensor-loa-0"),
    ("loc", "sensor", "", "072246-sensor-loc-0"),
    ("lom", "sensor", "", "072246-sensor-lom-0"),
    ("los", "sensor", "", "072246-sensor-los-0"),
    ("lssfc", "sensor", "", "072246-sensor-lssfc-0"),
    ("lsstc", "sensor", "", "072246-sensor-lsstc-0"),
    ("mcpea", "sensor", "", "072246-sensor-mcpea-0"),
    ("mmp", "sensor", "", "072246-sensor-mmp-0"),
    ("modelStatus", "sensor", "modelStatus", "072246-sensor-modelStatus-modelStatus"),
    ("modelStatus", "sensor", "", "072246-sensor-modelStatus-0"),
    ("msi", "sensor", "", "072246-sensor-msi-0"),
    ("nrg", "sensor", "0", "072246-sensor-nrg-0"),
    ("nrg", "sensor", "1", "072246-sensor-nrg-1"),
    ("nrg", "sensor", "2", "072246-sensor-nrg-2"),
    ("nrg", "sensor", "3", "072246-sensor-nrg-3"),
    ("nrg", "sensor", "4", "072246-sensor-nrg-4"),
    ("nrg", "sensor", "5", "072246-sensor-nrg-5"),
    ("nrg", "sensor", "6", "072246-sensor-nrg-6"),
    ("nrg", "sensor", "7", "072246-sensor-nrg-7"),
    ("nrg", "sensor", "8", "072246-sensor-nrg-8"),
    ("nrg", "sensor", "9", "072246-sensor-nrg-9"),
    ("nrg", "sensor", "10", "072246-sensor-nrg-10"),
    ("nrg", "sensor", "11", "072246-sensor-nrg-11"),
    ("nrg", "sensor", "12", "072246-sensor-nrg-12"),
    ("nrg", "sensor", "13", "072246-sensor-nrg-13"),
    ("nrg", "sensor", "14", "072246-sensor-nrg-14"),
    ("nrg", "sensor", "15", "072246-sensor-nrg-15"),
    ("oca", "sensor", "", "072246-sensor-oca-0"),
    ("ocl", "sensor", "", "072246-sensor-ocl-0"),
    ("ocm", "sensor", "", "072246-sensor-ocm-0"),
    ("ocp", "sensor", "", "072246-sensor-ocp-0"),
    ("ocs", "sensor", "", "072246-sensor-ocs-0"),
    ("ocu", "sensor", "", "072246-sensor-ocu-0"),
    ("onv", "sensor", "", "072246-sensor-onv-0"),
    ("pwm", "sensor", "", "072246-sensor-pwm-0"),
    ("qsc", "sensor", "", "072246-sensor-qsc-0"),
    ("qsw", "sensor", "", "072246-sensor-qsw-0"),
    ("rbc", "sensor", "", "072246-sensor-rbc-0"),
    ("rbt", "sensor", "", "072246-sensor-rbt-0"),
    ("rcd", "sensor", "", "072246-sensor-rcd-0"),
    ("rfb", "sensor", "", "072246-sensor-rfb-0"),
    ("rr", "sensor", "", "072246-sensor-rr-0"),
    ("rssi", "sensor", "", "072246-sensor-rssi-0"),
    ("scaa", "sensor", "", "072246-sensor-scaa-0"),
    ("scan", "sensor", "", "072246-sensor-scan-0"),
    ("scas", "sensor", "", "072246-sensor-scas-0"),
    ("tma", "sensor", "0", "072246-sensor-tma-0"),
    ("tma", "sensor", "1", "072246-sensor-tma-1"),
    ("tpa", "sensor", "", "072246-sensor-tpa-0"),
    ("trx", "sensor", "", "072246-sensor-trx-0"),
    ("tsom", "sensor", "", "072246-sensor-tsom-0"),
    ("utc", "sensor", "", "072246-sensor-utc-0"),
    ("wcch", "sensor", "", "072246-sensor-wcch-0"),
    ("wccw", "sensor", "", "072246-sensor-wccw-0"),
    ("wh", "sensor", "", "072246-sensor-wh-0"),
    ("wsms", "sensor", "", "072246-sensor-wsms-0"),
    ("wst", "sensor", "", "072246-sensor-wst-0"),
    ("psm", "sensor", "", "072246-sensor-psm-0"),
    ("cards", "sensor", "0", "072246-sensor-cards-0"),
    ("cards", "sensor", "1", "072246-sensor-cards-1"),
    ("cards", "sensor", "2", "072246-sensor-cards-2"),
    ("cards", "sensor", "3", "072246-sensor-cards-3"),
    ("cards", "sensor", "4", "072246-sensor-cards-4"),
    ("cards", "sensor", "5", "072246-sensor-cards-5"),
    ("cards", "sensor", "6", "072246-sensor-cards-6"),
    ("cards", "sensor", "7", "072246-sensor-cards-7"),
    ("cards", "sensor", "8", "072246-sensor-cards-8"),
    ("cards", "sensor", "9", "072246-sensor-cards-9"),
    ("ppv", "sensor", "", "072246-sensor-ppv-0"),
    ("pgrid", "sensor", "", "072246-sensor-pgrid-0"),
    ("pakku", "sensor", "", "072246-sensor-pakku-0"),
    # --- binary_sensor (13 entries) ---
    ("car", "binary_sensor", "1", "072246-binary_sensor-car-1"),
    ("pha", "binary_sensor", "0", "072246-binary_sensor-pha-0"),
    ("pha", "binary_sensor", "1", "072246-binary_sensor-pha-1"),
    ("pha", "binary_sensor", "2", "072246-binary_sensor-pha-2"),
    ("pha", "binary_sensor", "3", "072246-binary_sensor-pha-3"),
    ("pha", "binary_sensor", "4", "072246-binary_sensor-pha-4"),
    ("pha", "binary_sensor", "5", "072246-binary_sensor-pha-5"),
    ("cca", "binary_sensor", "", "072246-binary_sensor-cca-0"),
    ("ocuca", "binary_sensor", "", "072246-binary_sensor-ocuca-0"),
    ("sbe", "binary_sensor", "", "072246-binary_sensor-sbe-0"),
    ("adi", "binary_sensor", "", "072246-binary_sensor-adi-0"),
    ("cpe", "binary_sensor", "", "072246-binary_sensor-cpe-0"),
    ("cpr", "binary_sensor", "", "072246-binary_sensor-cpr-0"),
    ("cws", "binary_sensor", "", "072246-binary_sensor-cws-0"),
    ("cwsc", "binary_sensor", "", "072246-binary_sensor-cwsc-0"),
    ("fsp", "binary_sensor", "", "072246-binary_sensor-fsp-0"),
    ("lwcf", "binary_sensor", "", "072246-binary_sensor-lwcf-0"),
    ("tlf", "binary_sensor", "", "072246-binary_sensor-tlf-0"),
    ("tls", "binary_sensor", "", "072246-binary_sensor-tls-0"),
    # --- button (4 entries) ---
    ("rst", "button", "", "072246-button-rst-0"),
    ("frc", "button", "0", "072246-button-frc-0"),
    ("frc", "button", "1", "072246-button-frc-1"),
    ("frc", "button", "2", "072246-button-frc-2"),
    # --- number (8 entries) ---
    ("ama", "number", "", "072246-number-ama-0"),
    ("amp", "number", "", "072246-number-amp-0"),
    ("ate", "number", "", "072246-number-ate-0"),
    ("pgt", "number", "", "072246-number-pgt-0"),
    ("att", "number", "", "072246-number-att-0"),
    ("awp", "number", "", "072246-number-awp-0"),
    ("dwo", "number", "", "072246-number-dwo-0"),
    ("lop", "number", "", "072246-number-lop-0"),
    ("fst", "number", "", "072246-number-fst-0"),
    ("sh", "number", "", "072246-number-sh-0"),
    ("psh", "number", "", "072246-number-psh-0"),
    ("po", "number", "", "072246-number-po-0"),
    ("zfo", "number", "", "072246-number-zfo-0"),
    # --- select (7 entries) ---
    ("bac", "select", "bac", "072246-select-bac-bac"),
    ("sdp", "select", "sdp", "072246-select-sdp-sdp"),
    ("lmo", "select", "", "072246-select-lmo-0"),
    ("ust", "select", "ust", "072246-select-ust-ust"),
    ("frc", "select", "frc", "072246-select-frc-frc"),
    ("trx", "select", "trx", "072246-select-trx-trx"),
    ("psm", "select", "psm", "072246-select-psm-psm"),
    # --- switch (17 entries) ---
    ("ara", "switch", "", "072246-switch-ara-0"),
    ("wen", "switch", "", "072246-switch-wen-0"),
    ("tse", "switch", "", "072246-switch-tse-0"),
    ("nmo", "switch", "", "072246-switch-nmo-0"),
    ("lse", "switch", "", "072246-switch-lse-0"),
    ("awe", "switch", "", "072246-switch-awe-0"),
    ("acp", "switch", "", "072246-switch-acp-0"),
    ("esk", "switch", "", "072246-switch-esk-0"),
    ("fup", "switch", "", "072246-switch-fup-0"),
    ("fzf", "switch", "", "072246-switch-fzf-0"),
    ("su", "switch", "", "072246-switch-su-0"),
    ("hws", "switch", "", "072246-switch-hws-0"),
    ("hsa", "switch", "", "072246-switch-hsa-0"),
    ("loe", "switch", "", "072246-switch-loe-0"),
    ("upo", "switch", "", "072246-switch-upo-0"),
    ("cwe", "switch", "", "072246-switch-cwe-0"),
    ("sua", "switch", "", "072246-switch-sua-0"),
    ("acs", "switch", "", "072246-switch-acs-0"),
]


@pytest.mark.parametrize(
    "key,domain,attribute,expected_uid",
    _ALL_ENTITIES,
    ids=lambda v: v if isinstance(v, str) else "",
)
async def test_all_entity_unique_ids(
    hass, key, domain, attribute, expected_uid
) -> None:
    """Assert the hard-coded unique_id for every entity definition across all platforms."""
    entry = MockConfigEntry(domain=DOMAIN, data={CONF_TOPIC: _TOPIC}, version=2)
    entry.add_to_hass(hass)
    entry.runtime_data = MagicMock()
    entity = GoEChargerEntity(
        entry, GoEChargerEntityDescription(key=key, domain=domain, attribute=attribute)
    )
    assert entity._attr_unique_id == expected_uid


def test_entity_snapshot_is_complete() -> None:
    """Fail when a new entity definition is added without updating _ALL_ENTITIES."""
    all_defs = [
        *SENSORS,
        *BINARY_SENSORS,
        *BUTTONS,
        *NUMBERS,
        *SELECTS,
        *SWITCHES,
    ]
    defined = {(d.key, d.domain, d.attribute) for d in all_defs}
    snapshot = {(key, domain, attribute) for key, domain, attribute, _ in _ALL_ENTITIES}
    missing = defined - snapshot
    assert not missing, (
        "New entity definitions not covered in _ALL_ENTITIES snapshot:\n"
        + "\n".join(
            f"  key={k!r} domain={d!r} attribute={a!r}" for k, d, a in sorted(missing)
        )
        + "\nAdd them to _ALL_ENTITIES in tests/test_entity_unique_id.py."
    )
