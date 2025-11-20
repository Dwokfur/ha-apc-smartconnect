"""Switch platform for APC SmartConnect."""
from __future__ import annotations

import logging
from typing import Any

from homeassistant.components.switch import SwitchEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from . import APCSmartConnectCoordinator
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up APC SmartConnect switch based on a config entry."""
    coordinator: APCSmartConnectCoordinator = hass.data[DOMAIN][entry.entry_id]

    entities: list[SwitchEntity] = []

    # Create switches for each device's outlets
    for device_id, device_data in coordinator.data.items():
        device = device_data["device"]
        outlets = device_data.get("outlets", [])
        
        for outlet in outlets:
            if outlet.get("controllable", False):
                entities.append(
                    APCSmartConnectOutletSwitch(
                        coordinator,
                        device_id,
                        device,
                        outlet,
                    )
                )

    async_add_entities(entities)


class APCSmartConnectOutletSwitch(CoordinatorEntity, SwitchEntity):
    """Representation of an APC SmartConnect outlet switch."""

    def __init__(
        self,
        coordinator: APCSmartConnectCoordinator,
        device_id: str,
        device: dict[str, Any],
        outlet: dict[str, Any],
    ) -> None:
        """Initialize the switch."""
        super().__init__(coordinator)
        self._device_id = device_id
        self._device = device
        self._outlet = outlet
        self._outlet_id = outlet["id"]
        
        # Set unique ID
        self._attr_unique_id = f"{device_id}_outlet_{self._outlet_id}"
        
        # Set name
        outlet_name = outlet.get("name", f"Outlet {self._outlet_id}")
        self._attr_name = f"{device['name']} {outlet_name}"
        
        # Set icon based on outlet type
        if self._outlet_id == "main":
            self._attr_icon = "mdi:power-socket"
        else:
            self._attr_icon = "mdi:power-plug"
        
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
    def is_on(self) -> bool | None:
        """Return true if the switch is on."""
        device_data = self.coordinator.data.get(self._device_id)
        if device_data is None:
            return None
        
        outlets = device_data.get("outlets", [])
        for outlet in outlets:
            if outlet["id"] == self._outlet_id:
                return outlet.get("status", False)
        
        return None

    @property
    def available(self) -> bool:
        """Return if entity is available."""
        return (
            self.coordinator.last_update_success
            and self._device_id in self.coordinator.data
        )

    async def async_turn_on(self, **kwargs: Any) -> None:
        """Turn the switch on."""
        try:
            await self.hass.async_add_executor_job(
                self.coordinator.client.set_outlet_state,
                self._device_id,
                self._outlet_id,
                True,
            )
        except NotImplementedError as err:
            _LOGGER.warning(
                "Outlet control not yet implemented in library: %s. "
                "This is a stub for future functionality.",
                err
            )
            # For now, we'll log the action but not fail
            # In production with the actual library, this would control the outlet
            _LOGGER.info(
                "Would turn on outlet %s on device %s",
                self._outlet_id,
                self._device_id,
            )
        except Exception as err:
            _LOGGER.error("Failed to turn on outlet: %s", err)
            raise
        
        # Request coordinator update
        await self.coordinator.async_request_refresh()

    async def async_turn_off(self, **kwargs: Any) -> None:
        """Turn the switch off."""
        try:
            await self.hass.async_add_executor_job(
                self.coordinator.client.set_outlet_state,
                self._device_id,
                self._outlet_id,
                False,
            )
        except NotImplementedError as err:
            _LOGGER.warning(
                "Outlet control not yet implemented in library: %s. "
                "This is a stub for future functionality.",
                err
            )
            # For now, we'll log the action but not fail
            # In production with the actual library, this would control the outlet
            _LOGGER.info(
                "Would turn off outlet %s on device %s",
                self._outlet_id,
                self._device_id,
            )
        except Exception as err:
            _LOGGER.error("Failed to turn off outlet: %s", err)
            raise
        
        # Request coordinator update
        await self.coordinator.async_request_refresh()

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return extra state attributes."""
        return {
            "outlet_id": self._outlet_id,
            "outlet_name": self._outlet.get("name", "Unknown"),
            "controllable": self._outlet.get("controllable", False),
        }
