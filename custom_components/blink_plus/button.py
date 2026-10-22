"""Blink Plus buttons."""

from __future__ import annotations

from homeassistant.components.button import ButtonEntity
from homeassistant.core import HomeAssistant
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback

from .const import DEFAULT_BRAND, DOMAIN
from .coordinator import BlinkConfigEntry


def account_device(entry: BlinkConfigEntry) -> DeviceInfo:
    """Device that holds account-level entities (clip archive)."""
    return DeviceInfo(
        identifiers={(DOMAIN, f"account-{entry.entry_id}")},
        name="Blink Plus",
        manufacturer=DEFAULT_BRAND,
        model="Clip archive",
    )


async def async_setup_entry(
    hass: HomeAssistant,
    entry: BlinkConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Set up the archive button when an archive folder is configured."""
    archiver = entry.runtime_data.archiver
    if archiver is not None:
        async_add_entities([ArchiveNowButton(entry, archiver)])


class ArchiveNowButton(ButtonEntity):
    """Copy new USB clips to the archive folder now."""

    _attr_has_entity_name = True
    _attr_translation_key = "archive_now"

    def __init__(self, entry: BlinkConfigEntry, archiver) -> None:
        """Initialize."""
        self._archiver = archiver
        self._hours = entry.options.get("archive_lookback_hours", 24)
        self._attr_unique_id = f"{entry.entry_id}-archive-now"
        self._attr_device_info = account_device(entry)

    async def async_press(self) -> None:
        """Run the archive in the background (it can take minutes)."""
        self.hass.async_create_task(self._archiver.async_run(hours=float(self._hours)))
