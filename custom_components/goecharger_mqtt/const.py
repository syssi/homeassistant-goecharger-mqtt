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
CHARGING_POWER_MAX_CURRENT = {
    CHARGING_POWER_11KW: 16,
    CHARGING_POWER_22KW: 32,
}
