"""Adds config flow for Blueprint."""

from __future__ import annotations

from homeassistant import config_entries

from .const import DOMAIN


class SimpleChoresFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Config flow for Simple Chores."""

    VERSION = 1

    async def async_step_user(
        self,
        _user_input: dict | None = None,
    ) -> config_entries.ConfigFlowResult:
        """Handle a flow initialized by the user."""
        return self.async_create_entry(title="Example Entry", data={})
