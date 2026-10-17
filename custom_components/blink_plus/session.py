"""Dedicated aiohttp session for Blink (own cookie jar).

The OAuth v2 login is a browser-style flow: authorize -> signin -> 2FA ->
authorize again. Its cookies must survive between those calls and must not mix
with other integrations, so Blink Plus doesn't use HA's shared session.
"""

from __future__ import annotations

import aiohttp

from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_create_clientsession


def async_blink_session(hass: HomeAssistant) -> aiohttp.ClientSession:
    """Create a session with its own cookie jar (closed on HA stop)."""
    return async_create_clientsession(
        hass, cookie_jar=aiohttp.CookieJar(unsafe=True)
    )
