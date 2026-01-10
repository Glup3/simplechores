"""DataUpdateCoordinator for simplechores."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

if TYPE_CHECKING:
    from .data import IntegrationBlueprintConfigEntry


# https://developers.home-assistant.io/docs/integration_fetching_data#coordinated-single-api-poll-for-data-for-all-entities
class BlueprintDataUpdateCoordinator(DataUpdateCoordinator):
    """Class to manage fetching data from the API."""

    config_entry: IntegrationBlueprintConfigEntry

    async def _async_update_data(self) -> Any:
        """Update data via library."""
        # return await self.config_entry.runtime_data.client.async_get_data()
