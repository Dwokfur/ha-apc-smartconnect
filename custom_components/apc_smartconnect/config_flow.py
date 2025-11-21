"""Config flow for APC SmartConnect integration."""
from __future__ import annotations

import logging
from typing import Any

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.const import CONF_EMAIL, CONF_PASSWORD
from homeassistant.data_entry_flow import FlowResult
from homeassistant.helpers import config_validation as cv

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

STEP_USER_DATA_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_EMAIL): cv.string,
        vol.Required(CONF_PASSWORD): cv.string,
    }
)


class APCSmartConnectConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for APC SmartConnect."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle the initial step."""
        errors: dict[str, str] = {}

        if user_input is not None:
            # Validate the credentials
            try:
                # Test the connection
                await self._test_credentials(
                    user_input[CONF_EMAIL],
                    user_input[CONF_PASSWORD]
                )
            except InvalidAuth:
                errors["base"] = "invalid_auth"
            except CannotConnect:
                errors["base"] = "cannot_connect"
            except Exception:  # pylint: disable=broad-except
                _LOGGER.exception("Unexpected exception")
                errors["base"] = "unknown"
            else:
                # Create a unique ID based on the email
                await self.async_set_unique_id(user_input[CONF_EMAIL].lower())
                self._abort_if_unique_id_configured()

                return self.async_create_entry(
                    title=user_input[CONF_EMAIL],
                    data=user_input,
                )

        return self.async_show_form(
            step_id="user",
            data_schema=STEP_USER_DATA_SCHEMA,
            errors=errors,
        )

    async def _test_credentials(self, email: str, password: str) -> bool:
        """Test if credentials are valid."""
        try:
            # Import the library (in production, use the actual library)
            # from apc_smartconnect import APCSmartConnect
            
            # For now, we'll simulate the validation
            # In production: client = APCSmartConnect(email, password)
            # client.authenticate() or similar
            
            # Mock validation - always succeeds for demonstration
            # In production, this should actually test the connection
            await self.hass.async_add_executor_job(
                self._validate_credentials,
                email,
                password
            )
            return True
        except Exception as err:
            _LOGGER.error("Failed to authenticate: %s", err)
            raise CannotConnect from err

    def _validate_credentials(self, email: str, password: str) -> None:
        """Validate credentials synchronously."""
        # Import the vendorized library
        from .apc_smartconnect import APCSmartConnect
        
        # Basic validation
        if not email or "@" not in email:
            raise InvalidAuth("Invalid email format")
        
        if not password or len(password) < 6:
            raise InvalidAuth("Invalid password")
        
        # Authenticate with the APC SmartConnect service
        try:
            client = APCSmartConnect()
            client.login(email, password)
            # If login succeeds, credentials are valid
        except Exception as err:
            raise InvalidAuth(f"Authentication failed: {err}") from err


class CannotConnect(Exception):
    """Error to indicate we cannot connect."""


class InvalidAuth(Exception):
    """Error to indicate there is invalid auth."""
