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

from .apc_smartconnect import APCSmartConnect
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
    # Create wrapper around the vendorized apc_smartconnect library
    class APCSmartConnectWrapper:
        """Wrapper for APC SmartConnect client to adapt API to integration needs."""
        
        def __init__(self, email, password):
            self.email = email
            self.password = password
            self._apc_client = APCSmartConnect()
            # Authenticate with the APC SmartConnect service
            self._apc_client.login(email, password)
        
        def get_devices(self):
            """Get all devices and transform data to integration format."""
            devices = []
            
            try:
                # Fetch all gateways from APC SmartConnect API
                gateways_response = self._apc_client.gateways()
            except Exception as err:
                _LOGGER.error("Failed to fetch gateways from APC SmartConnect: %s", err)
                raise
            
            for gateway in gateways_response.get('gateways', []):
                device_id = gateway.get('deviceId')
                if not device_id:
                    _LOGGER.warning("Gateway missing deviceId, skipping: %s", gateway)
                    continue
                
                try:
                    # Get detailed information for each gateway
                    detail = self._apc_client.gateway_info_detail(device_id)
                except Exception as err:
                    _LOGGER.error("Failed to fetch details for device %s: %s", device_id, err)
                    continue
                
                # Transform the data into the format expected by the integration
                device_data = {
                    "id": device_id,
                    "name": gateway.get('deviceName', 'APC UPS'),
                    "model": gateway.get('model', 'Unknown'),
                    "serial": gateway.get('serialNumber', 'Unknown'),
                    "firmware": gateway.get('firmwareVersion', 'Unknown'),
                    "metrics": self._extract_metrics(detail),
                    "alarms": detail.get('alarms', []),
                    "events": detail.get('events', []),
                    "outlets": self._extract_outlets(detail),
                }
                
                devices.append(device_data)
            
            return devices
        
        def _extract_metrics(self, detail):
            """Extract metrics from gateway detail response."""
            metrics = {}
            
            # Battery metrics
            battery = detail.get('battery', {})
            metrics['battery_capacity'] = battery.get('capacity')
            metrics['battery_runtime'] = battery.get('runtime')
            metrics['battery_runtime_seconds'] = battery.get('runtimeSeconds')
            metrics['battery_status'] = battery.get('status')
            
            # Input metrics
            input_data = detail.get('input', {})
            metrics['input_voltage'] = input_data.get('voltage')
            metrics['frequency'] = input_data.get('frequency')
            
            # Output metrics
            output = detail.get('output', {})
            metrics['output_voltage'] = output.get('voltage')
            metrics['power'] = output.get('activePower')
            metrics['apparent_power'] = output.get('apparentPower')
            metrics['load'] = output.get('loadPercentage')
            metrics['current'] = output.get('current')
            metrics['energy'] = output.get('energy')
            
            # Status metrics
            metrics['status'] = detail.get('status')
            metrics['ups_mode'] = detail.get('upsMode')
            
            # Network metrics
            network = detail.get('network', {})
            metrics['network_status'] = network.get('status')
            
            # Temperature
            metrics['temperature'] = detail.get('temperature')
            
            return metrics
        
        def _extract_outlets(self, detail):
            """Extract outlet information from gateway detail response."""
            outlets = []
            
            # Main outlet
            main_outlet = detail.get('main_outlet', {})
            if main_outlet:
                outlets.append({
                    "id": "main",
                    "name": "Main Outlet",
                    "status": main_outlet.get('status') == 'on',
                    "controllable": main_outlet.get('controllable', True)
                })
            
            # Switched outlets
            switched_outlets = detail.get('switched_outlets', [])
            for idx, outlet in enumerate(switched_outlets, 1):
                outlets.append({
                    "id": f"outlet_{idx}",
                    "name": outlet.get('name', f"Outlet {idx}"),
                    "status": outlet.get('status') == 'on',
                    "controllable": outlet.get('controllable', True)
                })
            
            return outlets
        
        def set_outlet_state(self, device_id, outlet_id, state):
            """Set outlet state (placeholder for library method)."""
            # The apc-smartconnect library doesn't yet implement outlet control
            # This is a stub that will need to be implemented when the library adds support
            raise NotImplementedError(
                "Outlet control is not yet implemented in the apc-smartconnect library. "
                "This is a placeholder for future implementation."
            )
    
    return APCSmartConnectWrapper(email, password)


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
