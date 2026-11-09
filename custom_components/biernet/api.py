"""Async client for the biernet.nl offer list."""

import logging
import re
from html import unescape
from typing import Any

from aiohttp import ClientError, ClientSession

from .const import BASE_URL, LIST_URL, PAGE_URL, USER_AGENT

_LOGGER = logging.getLogger(__name__)

TOKEN_RE = re.compile(r'bnAt="([^"]+)"')
BLOCK_MARKER = '<li class="cardStyle"'
NAME_RE = re.compile(r'<h3 class="merkenH3"[^>]*>.*?>([^<]+)</a>', re.S)
ARTIKEL_RE = re.compile(r'<p class="artikel">\s*<a[^>]*>([^<]+)</a>', re.S)
WINKEL_RE = re.compile(r'title="([^"]+)"')
PRIJS_RE = re.compile(r'class="voor_prijss+">\s*€\s*([\d.,]+)')
LITER_RE = re.compile(r"€\s*([\d.,]+)\s*per liter")
GELDIG_RE = re.compile(r'class="laatste_regel">([^<]+)<')
URL_RE = re.compile(r'class="item_url" href="([^"]+)"')


class BiernetClientError(Exception):
    """Raised when the biernet.nl endpoint cannot be used."""


def _clean(text: str | None) -> str:
    if not text:
        return ""
    return unescape(re.sub(r"\s+", " ", text)).strip()


def parse_offers(response: str) -> list[dict[str, Any]]:
    """Parse the HTML fragment returned by the offer list endpoint."""
    if "Geen aanbiedingen gevonden" in response:
        return []

    items: list[dict[str, Any]] = []
    for block in response.split(BLOCK_MARKER)[1:]:
        naam = NAME_RE.search(block)
        verpakking = ARTIKEL_RE.search(block)
        winkel = WINKEL_RE.search(block)
        prijs = PRIJS_RE.search(block)
        liter = LITER_RE.search(block)
        geldig = GELDIG_RE.search(block)
        url = URL_RE.search(block)

        if not (naam and prijs and liter):
            continue

        items.append(
            {
                "naam": _clean(naam.group(1)),
                "verpakking": _clean(verpakking.group(1)) if verpakking else "",
                "winkel": _clean(winkel.group(1)).title() if winkel else "",
                "prijs": prijs.group(1).replace(",", "."),
                "literprijs": liter.group(1).replace(",", "."),
                "geldig": _clean(geldig.group(1)) if geldig else "",
                "url": BASE_URL + unescape(url.group(1)) if url else "",
            }
        )

    items.sort(key=lambda item: float(item["literprijs"]))
    return items


class BiernetClient:
    """Fetches filtered beer offers from biernet.nl."""

    def __init__(self, session: ClientSession, filters: dict[str, str]) -> None:
        self._session = session
        self._filters = filters

    async def async_fetch_offers(self) -> list[dict[str, Any]]:
        """Return the offers for the configured filters, sorted by liter price."""
        try:
            async with self._session.get(
                PAGE_URL, headers={"User-Agent": USER_AGENT}
            ) as resp:
                resp.raise_for_status()
                page = await resp.text()

            token_match = TOKEN_RE.search(page)
            if not token_match:
                raise BiernetClientError("Page token not found on biernet.nl")

            params: dict[str, str] = {
                "zoeken": "true",
                "skip": "0",
                "screenType": "large",
                "cookieName": "aanbiedingenFilter",
                "current_url": "/bier/aanbiedingen/",
                "at": token_match.group(1),
            }
            params.update(self._filters)

            body = "&".join(f"{key}={value}" for key, value in params.items())

            async with self._session.post(
                LIST_URL,
                data=body.encode("utf-8"),
                headers={
                    "User-Agent": USER_AGENT,
                    "X-Requested-With": "XMLHttpRequest",
                    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
                    "Referer": PAGE_URL,
                    "Origin": BASE_URL,
                },
            ) as resp:
                resp.raise_for_status()
                response = await resp.text()
        except ClientError as err:
            raise BiernetClientError(f"Error contacting biernet.nl: {err}") from err

        offers = parse_offers(response)
        _LOGGER.debug("Biernet returned %d offers for %s", len(offers), self._filters)
        return offers
