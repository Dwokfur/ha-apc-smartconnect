"""Sensor platform for APC SmartConnect."""
from __future__ import annotations

import logging
from typing import Any

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from . import APCSmartConnectCoordinator
from .const import ALARM_SENSOR_TYPES, DOMAIN, SENSOR_TYPES

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up APC SmartConnect sensor based on a config entry."""
    coordinator: APCSmartConnectCoordinator = hass.data[DOMAIN][entry.entry_id]

    entities: list[SensorEntity] = []

    # Create sensors for each device
    for device_id, device_data in coordinator.data.items():
        device = device_data["device"]
        metrics = device_data["metrics"]
        
        # Add standard metric sensors
        for sensor_type, sensor_config in SENSOR_TYPES.items():
            if sensor_type in metrics:
                entities.append(
                    APCSmartConnectSensor(
                        coordinator,
                        device_id,
                        device,
                        sensor_type,
                        sensor_config,
                    )
                )
        
        # Add alarm/event sensors
        alarms = device_data.get("alarms", [])
        events = device_data.get("events", [])
        
        for alarm_type, alarm_config in ALARM_SENSOR_TYPES.items():
            if alarm_type.startswith("alarm"):
                entities.append(
                    APCSmartConnectAlarmSensor(
                        coordinator,
                        device_id,
                        device,
                        alarm_type,
                        alarm_config,
                        alarms,
                    )
                )
            elif alarm_type.startswith("event"):
                entities.append(
                    APCSmartConnectEventSensor(
                        coordinator,
                        device_id,
                        device,
                        alarm_type,
                        alarm_config,
                        events,
                    )
                )

    async_add_entities(entities)


class APCSmartConnectSensor(CoordinatorEntity, SensorEntity):
    """Representation of an APC SmartConnect sensor."""

    def __init__(
        self,
        coordinator: APCSmartConnectCoordinator,
        device_id: str,
        device: dict[str, Any],
        sensor_type: str,
        sensor_config: dict[str, Any],
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._device_id = device_id
        self._device = device
        self._sensor_type = sensor_type
        self._sensor_config = sensor_config
        
        # Set unique ID
        self._attr_unique_id = f"{device_id}_{sensor_type}"
        
        # Set name
        self._attr_name = f"{device['name']} {sensor_config['name']}"
        
        # Set device class
        self._attr_device_class = sensor_config.get("device_class")
        
        # Set unit of measurement
        self._attr_native_unit_of_measurement = sensor_config.get("unit")
        
        # Set icon
        self._attr_icon = sensor_config.get("icon")
        
        # Set state class
        self._attr_state_class = sensor_config.get("state_class")
        
        # Set entity category
        self._attr_entity_category = sensor_config.get("entity_category")
        
        # Set device info
        self._attr_device_info = {
            "identifiers": {(DOMAIN, device_id)},
            "name": device["name"],
            "manufacturer": "APC",
            "model": device.get("model", "Unknown"),
            "sw_version": device.get("firmware", "Unknown"),
            "serial_number": device.get("serial"),
        }

    @property
    def native_value(self) -> Any:
        """Return the state of the sensor."""
        device_data = self.coordinator.data.get(self._device_id)
        if device_data is None:
            return None
        
        metrics = device_data.get("metrics", {})
        return metrics.get(self._sensor_type)

    @property
    def available(self) -> bool:
        """Return if entity is available."""
        return (
            self.coordinator.last_update_success
            and self._device_id in self.coordinator.data
        )


class APCSmartConnectAlarmSensor(CoordinatorEntity, SensorEntity):
    """Representation of an APC SmartConnect alarm sensor."""

    def __init__(
        self,
        coordinator: APCSmartConnectCoordinator,
        device_id: str,
        device: dict[str, Any],
        sensor_type: str,
        sensor_config: dict[str, Any],
        alarms: list,
    ) -> None:
        """Initialize the alarm sensor."""
        super().__init__(coordinator)
        self._device_id = device_id
        self._device = device
        self._sensor_type = sensor_type
        self._sensor_config = sensor_config
        
        # Set unique ID
        self._attr_unique_id = f"{device_id}_{sensor_type}"
        
        # Set name
        self._attr_name = f"{device['name']} {sensor_config['name']}"
        
        # Set device class
        self._attr_device_class = sensor_config.get("device_class")
        
        # Set icon
        self._attr_icon = sensor_config.get("icon")
        
        # Set state class
        self._attr_state_class = sensor_config.get("state_class")
        
        # Set entity category
        self._attr_entity_category = sensor_config.get("entity_category")
        
        # Set device info
        self._attr_device_info = {
            "identifiers": {(DOMAIN, device_id)},
            "name": device["name"],
            "manufacturer": "APC",
            "model": device.get("model", "Unknown"),
            "sw_version": device.get("firmware", "Unknown"),
            "serial_number": device.get("serial"),
        }

    @property
    def native_value(self) -> Any:
        """Return the state of the sensor."""
        device_data = self.coordinator.data.get(self._device_id)
        if device_data is None:
            return None
        
        alarms = device_data.get("alarms", [])
        
        if self._sensor_type == "alarm_active":
            return len(alarms) > 0
        elif self._sensor_type == "alarm_count":
            return len(alarms)
        elif self._sensor_type == "last_alarm":
            if alarms:
                return alarms[-1].get("message", "Unknown alarm")
            return "No alarms"
        
        return None

    @property
    def available(self) -> bool:
        """Return if entity is available."""
        return (
            self.coordinator.last_update_success
            and self._device_id in self.coordinator.data
        )

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return extra state attributes."""
        device_data = self.coordinator.data.get(self._device_id)
        if device_data is None:
            return {}
        
        alarms = device_data.get("alarms", [])
        
        if self._sensor_type in ["alarm_active", "alarm_count", "last_alarm"]:
            return {
                "alarms": alarms,
                "total_count": len(alarms),
            }
        
        return {}


class APCSmartConnectEventSensor(CoordinatorEntity, SensorEntity):
    """Representation of an APC SmartConnect event sensor."""

    def __init__(
        self,
        coordinator: APCSmartConnectCoordinator,
        device_id: str,
        device: dict[str, Any],
        sensor_type: str,
        sensor_config: dict[str, Any],
        events: list,
    ) -> None:
        """Initialize the event sensor."""
        super().__init__(coordinator)
        self._device_id = device_id
        self._device = device
        self._sensor_type = sensor_type
        self._sensor_config = sensor_config
        
        # Set unique ID
        self._attr_unique_id = f"{device_id}_{sensor_type}"
        
        # Set name
        self._attr_name = f"{device['name']} {sensor_config['name']}"
        
        # Set device class
        self._attr_device_class = sensor_config.get("device_class")
        
        # Set icon
        self._attr_icon = sensor_config.get("icon")
        
        # Set state class
        self._attr_state_class = sensor_config.get("state_class")
        
        # Set entity category
        self._attr_entity_category = sensor_config.get("entity_category")
        
        # Set device info
        self._attr_device_info = {
            "identifiers": {(DOMAIN, device_id)},
            "name": device["name"],
            "manufacturer": "APC",
            "model": device.get("model", "Unknown"),
            "sw_version": device.get("firmware", "Unknown"),
            "serial_number": device.get("serial"),
        }

    @property
    def native_value(self) -> Any:
        """Return the state of the sensor."""
        device_data = self.coordinator.data.get(self._device_id)
        if device_data is None:
            return None
        
        events = device_data.get("events", [])
        
        if self._sensor_type == "event_active":
            return len(events) > 0
        elif self._sensor_type == "event_count":
            return len(events)
        elif self._sensor_type == "last_event":
            if events:
                return events[-1].get("message", "Unknown event")
            return "No events"
        
        return None

    @property
    def available(self) -> bool:
        """Return if entity is available."""
        return (
            self.coordinator.last_update_success
            and self._device_id in self.coordinator.data
        )

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return extra state attributes."""
        device_data = self.coordinator.data.get(self._device_id)
        if device_data is None:
            return {}
        
        events = device_data.get("events", [])
        
        if self._sensor_type in ["event_active", "event_count", "last_event"]:
            return {
                "events": events,
                "total_count": len(events),
            }
        
        return {}
