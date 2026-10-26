"""Constants for the go-eCharger (MQTT) integration."""

DOMAIN = "goecharger_mqtt"

ATTR_KEY = "key"
ATTR_VALUE = "value"

CONF_TOPIC = "topic"
# Kept for migration from config entry version 1
CONF_SERIAL_NUMBER = "serial_number"
CONF_TOPIC_PREFIX = "topic_prefix"

DEFAULT_TOPIC_PREFIX = "go-eCharger"

DEVICE_INFO_MANUFACTURER = "go-e GmbH"
DEVICE_INFO_MODEL = "go-eCharger HOME"

CONF_CHARGING_POWER = "charging_power"
CHARGING_POWER_11KW = "11kw"
CHARGING_POWER_22KW = "22kw"
CONF_API_VERSION = "api_version"
API_VERSION_AUTO = "auto"
API_VERSION_V1 = "v1"
API_VERSION_V2 = "v2"
CHARGING_POWER_MAX_CURRENT = {
    CHARGING_POWER_11KW: 16,
    CHARGING_POWER_22KW: 32,
}

V1_WRITABLE_KEYS = frozenset(
    {
        "amp",
        "amx",
        "ast",
        "alw",
        "stp",
        "dwo",
        "wss",
        "wke",
        "wen",
        "tof",
        "tds",
        "lbr",
        "aho",
        "afi",
        "ama",
        "al1",
        "al2",
        "al3",
        "al4",
        "al5",
        "cid",
        "cch",
        "cfi",
        "lse",
        "ust",
        "wak",
        "r1x",
        "dto",
        "nmo",
        "rna",
        "rnm",
        "rne",
        "rn4",
        "rn5",
        "rn6",
        "rn7",
        "rn8",
        "rn9",
        "rn1",
    }
)


def normalize_base_topic(topic: str) -> str:
    """Return the base topic when given a complete status or var topic."""
    return topic.removesuffix("/status").removesuffix("/var").rstrip("/")
