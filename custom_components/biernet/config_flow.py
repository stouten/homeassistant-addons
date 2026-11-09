"""Config flow for the Biernet integration."""

from typing import Any

import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import callback
from homeassistant.data_entry_flow import FlowResult
from homeassistant.helpers import selector

from .const import (
    DEFAULT_TOP_N,
    DEFAULT_UPDATE_HOURS,
    DOMAIN,
    PERCENTAGES,
    SOORTEN,
    SORTERINGEN,
    VERPAKKINGEN,
    WINKELS,
)

STEP_SCHEMA = vol.Schema(
    {
        vol.Required("name"): str,
        vol.Optional("winkel", default=[]): selector.SelectSelector(
            selector.SelectSelectorConfig(
                options=list(WINKELS),
                multiple=True,
                sort=True,
                mode=selector.SelectSelectorMode.DROPDOWN,
            )
        ),
        vol.Optional("soort", default=[]): selector.SelectSelector(
            selector.SelectSelectorConfig(
                options=list(SOORTEN),
                multiple=True,
                sort=True,
                mode=selector.SelectSelectorMode.DROPDOWN,
            )
        ),
        vol.Optional("verpakking", default=[]): selector.SelectSelector(
            selector.SelectSelectorConfig(
                options=list(VERPAKKINGEN),
                multiple=True,
                mode=selector.SelectSelectorMode.LIST,
            )
        ),
        vol.Optional("percentage", default="0tm1"): selector.SelectSelector(
            selector.SelectSelectorConfig(
                options=list(PERCENTAGES),
                mode=selector.SelectSelectorMode.DROPDOWN,
            )
        ),
        vol.Optional("sorteer", default="literprijs-oplopend"): selector.SelectSelector(
            selector.SelectSelectorConfig(
                options=list(SORTERINGEN),
                mode=selector.SelectSelectorMode.DROPDOWN,
            )
        ),
        vol.Optional("top_n", default=DEFAULT_TOP_N): selector.NumberSelector(
            selector.NumberSelectorConfig(min=1, max=100, step=1)
        ),
        vol.Optional("update_hours", default=DEFAULT_UPDATE_HOURS): selector.NumberSelector(
            selector.NumberSelectorConfig(min=1, max=168, step=1)
        ),
    }
)


class BiernetConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle the Biernet config flow."""

    VERSION = 1

    async def async_step_user(self, user_input: dict[str, Any] | None = None) -> FlowResult:
        if user_input is not None:
            await self.async_set_unique_id(user_input["name"].lower())
            self._abort_if_unique_id_configured()
            return self.async_create_entry(title=user_input["name"], data=user_input)

        return self.async_show_form(step_id="user", data_schema=STEP_SCHEMA)

    @staticmethod
    @callback
    def async_get_options_flow(
        config_entry: config_entries.ConfigEntry,
    ) -> BiernetOptionsFlow:
        return BiernetOptionsFlow(config_entry)


class BiernetOptionsFlow(config_entries.OptionsFlow):
    """Allow changing the filters of an existing search."""

    def __init__(self, config_entry: config_entries.ConfigEntry) -> None:
        self.config_entry = config_entry

    async def async_step_init(self, user_input: dict[str, Any] | None = None) -> FlowResult:
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        data = self.config_entry.data
        schema = vol.Schema(
            {
                vol.Optional("winkel", default=data.get("winkel", [])): selector.SelectSelector(
                    selector.SelectSelectorConfig(
                        options=list(WINKELS), multiple=True, sort=True,
                        mode=selector.SelectSelectorMode.DROPDOWN,
                    )
                ),
                vol.Optional("soort", default=data.get("soort", [])): selector.SelectSelector(
                    selector.SelectSelectorConfig(
                        options=list(SOORTEN), multiple=True, sort=True,
                        mode=selector.SelectSelectorMode.DROPDOWN,
                    )
                ),
                vol.Optional("verpakking", default=data.get("verpakking", [])): selector.SelectSelector(
                    selector.SelectSelectorConfig(
                        options=list(VERPAKKINGEN), multiple=True,
                        mode=selector.SelectSelectorMode.LIST,
                    )
                ),
                vol.Optional("percentage", default=data.get("percentage", "0tm1")): selector.SelectSelector(
                    selector.SelectSelectorConfig(
                        options=list(PERCENTAGES),
                        mode=selector.SelectSelectorMode.DROPDOWN,
                    )
                ),
                vol.Optional("sorteer", default=data.get("sorteer", "literprijs-oplopend")): selector.SelectSelector(
                    selector.SelectSelectorConfig(
                        options=list(SORTERINGEN),
                        mode=selector.SelectSelectorMode.DROPDOWN,
                    )
                ),
                vol.Optional("top_n", default=data.get("top_n", DEFAULT_TOP_N)): selector.NumberSelector(
                    selector.NumberSelectorConfig(min=1, max=100, step=1)
                ),
                vol.Optional("update_hours", default=data.get("update_hours", DEFAULT_UPDATE_HOURS)): selector.NumberSelector(
                    selector.NumberSelectorConfig(min=1, max=168, step=1)
                ),
            }
        )
        return self.async_show_form(step_id="init", data_schema=schema)
