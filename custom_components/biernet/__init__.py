"""The Biernet integration: one config entry per search profile."""

import logging
from datetime import timedelta
from typing import Any

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryNotReady
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

from .api import BiernetClient, BiernetClientError
from .const import (
    DOMAIN,
    PERCENTAGES,
    SOORTEN,
    VERPAKKING_PARAMS,
    WINKELS,
)

PLATFORMS = [Platform.SENSOR]


def build_filters(data: dict[str, Any]) -> dict[str, str]:
    """Translate entry data into the POST parameters of biernet.nl."""
    filters: dict[str, str] = {}
    if data.get("winkel"):
        filters["winkel"] = "+".join(data["winkel"])
    if data.get("soort"):
        filters["soort"] = "+".join(data["soort"])
    for verpakking in data.get("verpakking", []):
        param = VERPAKKING_PARAMS.get(verpakking)
        if param:
            filters[param] = verpakking
    if data.get("percentage"):
        filters["percentage"] = data["percentage"]
    if data.get("sorteer"):
        filters["sorteer"] = data["sorteer"]
    return filters


def build_site_url(data: dict[str, Any]) -> str:
    """Build the human-readable biernet.nl URL for this search profile."""
    from .const import BASE_URL

    segments: list[str] = []
    if data.get("winkel"):
        segments.append("winkel:" + "+".join(data["winkel"]))
    if data.get("soort"):
        segments.append("soort:" + "+".join(data["soort"]))
    for verpakking in data.get("verpakking", []):
        param = VERPAKKING_PARAMS.get(verpakking)
        if param:
            segments.append(f"{param}:{verpakking}")
    if data.get("percentage"):
        segments.append("percentage:" + data["percentage"])
    if data.get("sorteer"):
        segments.append("sorteer:" + data["sorteer"])
    path = "/".join(segments)
    return f"{BASE_URL}/bier/aanbiedingen/{path}" if path else f"{BASE_URL}/bier/aanbiedingen/"


def humanize_filters(data: dict[str, Any]) -> dict[str, Any]:
    """Return a readable summary of the filters for the sensor attributes."""
    return {
        "winkels": [WINKELS.get(w, w) for w in data.get("winkel", [])],
        "soorten": [SOORTEN.get(s, s) for s in data.get("soort", [])],
        "verpakkingen": [VERPAKKING_PARAMS.get(v, v) for v in data.get("verpakking", [])],
        "percentage": PERCENTAGES.get(data.get("percentage", ""), data.get("percentage", "")),
        "sortering": data.get("sorteer", ""),
    }


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Biernet from a config entry."""
    client = BiernetClient(async_get_clientsession(hass), build_filters(entry.data))
    top_n = int(entry.data.get("top_n", 10))
    update_hours = float(entry.data.get("update_hours", 24))

    async def async_update() -> dict[str, Any]:
        offers = await client.async_fetch_offers()
        return {"items": offers[:top_n], "total": len(offers)}

    coordinator: DataUpdateCoordinator = DataUpdateCoordinator(
        hass,
        logger=logging.getLogger(__name__),
        name=f"{DOMAIN}_{entry.data.get('name', 'search')}",
        update_method=async_update,
        update_interval=timedelta(hours=update_hours),
    )

    await coordinator.async_config_entry_first_refresh()
    if coordinator.last_update_success is False:
        raise ConfigEntryNotReady("Initial biernet.nl fetch failed")

    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = coordinator
    await hass.config_entries.async_forward_platforms(entry, PLATFORMS)
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    unloaded = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unloaded:
        hass.data[DOMAIN].pop(entry.entry_id)
    return unloaded
