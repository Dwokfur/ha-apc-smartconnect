"""Constants for the APC SmartConnect integration."""
from datetime import timedelta
from typing import Final

DOMAIN: Final = "apc_smartconnect"

# Update interval
UPDATE_INTERVAL = timedelta(minutes=5)

# Device classes
DEVICE_CLASS_BATTERY: Final = "battery"
DEVICE_CLASS_POWER: Final = "power"
DEVICE_CLASS_VOLTAGE: Final = "voltage"
DEVICE_CLASS_TEMPERATURE: Final = "temperature"
DEVICE_CLASS_FREQUENCY: Final = "frequency"
DEVICE_CLASS_CURRENT: Final = "current"
DEVICE_CLASS_ENERGY: Final = "energy"

# Unit of measurement
PERCENTAGE: Final = "%"
VOLT: Final = "V"
WATT: Final = "W"
AMPERE: Final = "A"
HERTZ: Final = "Hz"
CELSIUS: Final = "°C"
MINUTE: Final = "min"
SECONDS: Final = "s"
KILOWATT_HOUR: Final = "kWh"
VOLT_AMPERE: Final = "VA"

# Sensor types
SENSOR_TYPES = {
    # Battery sensors
    "battery_capacity": {
        "name": "Battery Capacity",
        "device_class": DEVICE_CLASS_BATTERY,
        "unit": PERCENTAGE,
        "icon": "mdi:battery",
        "state_class": "measurement",
        "entity_category": None,
    },
    "battery_runtime": {
        "name": "Battery Runtime",
        "device_class": None,
        "unit": MINUTE,
        "icon": "mdi:battery-clock",
        "state_class": "measurement",
        "entity_category": None,
    },
    "battery_runtime_seconds": {
        "name": "Battery Runtime Seconds",
        "device_class": "duration",
        "unit": SECONDS,
        "icon": "mdi:battery-clock",
        "state_class": "measurement",
        "entity_category": None,
    },
    "battery_status": {
        "name": "Battery Status",
        "device_class": None,
        "unit": None,
        "icon": "mdi:battery-heart",
        "state_class": None,
        "entity_category": "diagnostic",
    },
    # Voltage sensors
    "input_voltage": {
        "name": "Input Voltage",
        "device_class": DEVICE_CLASS_VOLTAGE,
        "unit": VOLT,
        "icon": "mdi:flash",
        "state_class": "measurement",
        "entity_category": None,
    },
    "output_voltage": {
        "name": "Output Voltage",
        "device_class": DEVICE_CLASS_VOLTAGE,
        "unit": VOLT,
        "icon": "mdi:flash-outline",
        "state_class": "measurement",
        "entity_category": None,
    },
    # Power sensors
    "power": {
        "name": "Power",
        "device_class": DEVICE_CLASS_POWER,
        "unit": WATT,
        "icon": "mdi:lightning-bolt",
        "state_class": "measurement",
        "entity_category": None,
    },
    "load": {
        "name": "Load",
        "device_class": None,
        "unit": PERCENTAGE,
        "icon": "mdi:gauge",
        "state_class": "measurement",
        "entity_category": None,
    },
    "apparent_power": {
        "name": "Apparent Power",
        "device_class": "apparent_power",
        "unit": VOLT_AMPERE,
        "icon": "mdi:flash-circle",
        "state_class": "measurement",
        "entity_category": None,
    },
    # Status sensors
    "status": {
        "name": "Status",
        "device_class": None,
        "unit": None,
        "icon": "mdi:information",
        "state_class": None,
        "entity_category": None,
    },
    "ups_mode": {
        "name": "UPS Mode",
        "device_class": None,
        "unit": None,
        "icon": "mdi:state-machine",
        "state_class": None,
        "entity_category": "diagnostic",
    },
    # Temperature sensors
    "temperature": {
        "name": "Temperature",
        "device_class": DEVICE_CLASS_TEMPERATURE,
        "unit": CELSIUS,
        "icon": "mdi:thermometer",
        "state_class": "measurement",
        "entity_category": None,
    },
    # Network sensors
    "network_status": {
        "name": "Network Status",
        "device_class": None,
        "unit": None,
        "icon": "mdi:lan",
        "state_class": None,
        "entity_category": "diagnostic",
    },
    # Frequency sensor
    "frequency": {
        "name": "Frequency",
        "device_class": DEVICE_CLASS_FREQUENCY,
        "unit": HERTZ,
        "icon": "mdi:sine-wave",
        "state_class": "measurement",
        "entity_category": None,
    },
    # Current sensor
    "current": {
        "name": "Current",
        "device_class": DEVICE_CLASS_CURRENT,
        "unit": AMPERE,
        "icon": "mdi:current-ac",
        "state_class": "measurement",
        "entity_category": None,
    },
    # Energy sensor
    "energy": {
        "name": "Energy",
        "device_class": DEVICE_CLASS_ENERGY,
        "unit": KILOWATT_HOUR,
        "icon": "mdi:lightning-bolt-circle",
        "state_class": "total_increasing",
        "entity_category": None,
    },
}

# Alarm/Event sensor types
ALARM_SENSOR_TYPES = {
    "alarm_active": {
        "name": "Alarm Active",
        "device_class": "problem",
        "icon": "mdi:alarm-light",
        "entity_category": "diagnostic",
    },
    "alarm_count": {
        "name": "Alarm Count",
        "device_class": None,
        "icon": "mdi:counter",
        "state_class": "measurement",
        "entity_category": "diagnostic",
    },
    "last_alarm": {
        "name": "Last Alarm",
        "device_class": None,
        "icon": "mdi:bell-alert",
        "entity_category": "diagnostic",
    },
    "event_active": {
        "name": "Event Active",
        "device_class": "problem",
        "icon": "mdi:information-outline",
        "entity_category": "diagnostic",
    },
    "event_count": {
        "name": "Event Count",
        "device_class": None,
        "icon": "mdi:counter",
        "state_class": "measurement",
        "entity_category": "diagnostic",
    },
    "last_event": {
        "name": "Last Event",
        "device_class": None,
        "icon": "mdi:message-alert",
        "entity_category": "diagnostic",
    },
}
