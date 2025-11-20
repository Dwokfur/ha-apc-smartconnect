"""The APC SmartConnect integration."""
from __future__ import annotations

import logging
from datetime import timedelta

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_EMAIL, CONF_PASSWORD, Platform
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryAuthFailed
from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
    DataUpdateCoordinator,
    UpdateFailed,
)

from .const import DOMAIN, UPDATE_INTERVAL

_LOGGER = logging.getLogger(__name__)

PLATFORMS: list[Platform] = [Platform.SENSOR, Platform.SWITCH]


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up APC SmartConnect from a config entry."""
    hass.data.setdefault(DOMAIN, {})

    # Initialize the APC SmartConnect API client
    # Note: This requires the apc-smartconnect library to be available
    try:
        # Import the library (will be installed via requirements in manifest.json)
        # from apc_smartconnect import APCSmartConnect
        
        # For now, we'll create a mock client structure since the library may not exist yet
        # In production, replace this with: client = APCSmartConnect(email, password)
        client = await hass.async_add_executor_job(
            _create_client,
            entry.data[CONF_EMAIL],
            entry.data[CONF_PASSWORD]
        )
    except Exception as err:
        _LOGGER.error("Failed to connect to APC SmartConnect: %s", err)
        raise ConfigEntryAuthFailed from err

    # Create coordinator
    coordinator = APCSmartConnectCoordinator(hass, client)
    await coordinator.async_config_entry_first_refresh()

    hass.data[DOMAIN][entry.entry_id] = coordinator

    # Setup platforms
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    if unload_ok := await hass.config_entries.async_unload_platforms(entry, PLATFORMS):
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok


def _create_client(email: str, password: str):
    """Create APC SmartConnect client (synchronous)."""
    # This is a placeholder for the actual library initialization
    # In production, this should be:
    # from apc_smartconnect import APCSmartConnect
    # return APCSmartConnect(email, password)
    
    # For now, return a mock client object
    class MockAPCClient:
        """Mock APC SmartConnect client."""
        
        def __init__(self, email, password):
            self.email = email
            self.password = password
            self._devices = []
        
        def get_devices(self):
            """Get all devices."""
            # Mock device data structure
            return [
                {
                    "id": "mock-device-1",
                    "name": "APC Smart-UPS 1500",
                    "model": "SMT1500RM2U",
                    "serial": "ABC123456",
                    "firmware": "1.0.0",
                    "metrics": {
                        "battery_capacity": 100,
                        "battery_runtime": 45,
                        "battery_runtime_seconds": 2700,
                        "battery_status": "Normal",
                        "input_voltage": 120.5,
                        "output_voltage": 120.0,
                        "power": 150,
                        "load": 10,
                        "apparent_power": 180,
                        "status": "Online",
                        "ups_mode": "Normal",
                        "temperature": 25.5,
                        "network_status": "Connected",
                        "frequency": 60.0,
                        "current": 1.25,
                        "energy": 1.5,
                    },
                    "alarms": [],
                    "events": [],
                    "outlets": [
                        {"id": "main", "name": "Main Outlet", "status": True, "controllable": True},
                        {"id": "outlet_1", "name": "Outlet 1", "status": True, "controllable": True},
                        {"id": "outlet_2", "name": "Outlet 2", "status": True, "controllable": True},
                    ],
                }
            ]
        
        def set_outlet_state(self, device_id, outlet_id, state):
            """Set outlet state (placeholder for library method)."""
            # This method should be implemented in the actual library
            # For now, this is a stub that will need to be patched
            raise NotImplementedError(
                "Outlet control is not yet implemented in the apc-smartconnect library. "
                "This is a placeholder for future implementation."
            )
    
    return MockAPCClient(email, password)


class APCSmartConnectCoordinator(DataUpdateCoordinator):
    """Class to manage fetching APC SmartConnect data."""

    def __init__(self, hass: HomeAssistant, client) -> None:
        """Initialize."""
        self.client = client
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=UPDATE_INTERVAL,
        )

    async def _async_update_data(self):
        """Update data via library."""
        try:
            # Fetch data from API
            devices = await self.hass.async_add_executor_job(
                self.client.get_devices
            )
            
            # Transform data into a format suitable for entities
            data = {}
            for device in devices:
                device_id = device["id"]
                data[device_id] = {
                    "device": device,
                    "metrics": device.get("metrics", {}),
                    "alarms": device.get("alarms", []),
                    "events": device.get("events", []),
                    "outlets": device.get("outlets", []),
                }
            
            return data
        except Exception as err:
            raise UpdateFailed(f"Error communicating with API: {err}") from err
