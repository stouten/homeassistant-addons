"""Sensor platform for the Biernet integration."""

from typing import Any

from homeassistant.components.sensor import SensorEntity, SensorStateClass
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.device_registry import DeviceEntryType
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from . import build_site_url, humanize_filters
from .const import DOMAIN


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities
) -> None:
    coordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([BiernetOfferSensor(entry, coordinator)])


class BiernetOfferSensor(CoordinatorEntity, SensorEntity):
    """Shows the cheapest liter price of the configured search profile."""

    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_native_unit_of_measurement = "€/l"

    def __init__(self, entry: ConfigEntry, coordinator) -> None:
        super().__init__(coordinator)
        self._entry = entry
        self._attr_unique_id = f"{DOMAIN}_{entry.entry_id}"
        self._attr_name = f"Biernet {entry.data.get('name', 'zoekopdracht')}"
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, entry.entry_id)},
            name=f"Biernet {entry.data.get('name', '')}",
            manufacturer="biernet.nl",
            entry_type=DeviceEntryType.SERVICE,
        )

    @property
    def native_value(self) -> float | None:
        items = self.coordinator.data.get("items") if self.coordinator.data else None
        if not items:
            return None
        return float(items[0]["literprijs"])

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        data = self.coordinator.data or {}
        items = data.get("items", [])
        return {
            "items": items,
            "count": len(items),
            "total_aanbiedingen": data.get("total", 0),
            "filters": humanize_filters(self._entry.data),
            "site_url": build_site_url(self._entry.data),
        }
