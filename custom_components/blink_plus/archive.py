"""Copy Blink clips to a folder, with or without a Blink subscription.

Two sources, used automatically:

A. Cloud clips (Blink subscription plan):
   GET /api/v1/accounts/{acct}/media/changed?since=<ts>&page=N
       -> {"media": [{id, created_at, device_name, deleted, media: "/api/...mp4"}]}
   GET <media path> -> MP4. Doesn't touch the sync module, so it also runs
   while a live view is open.

B. USB clips (Sync Module 2 local storage, no plan needed).
   Same endpoints the Blink app uses for local storage:
1. POST .../sync_modules/{sm}/local_storage/manifest/request   -> command id
2. GET  .../sync_modules/{sm}/local_storage/manifest/request/{id}
        -> {"manifest_id": ..., "clips": [{id, camera_name, created_at, size}]}
3. for each new clip:
   POST .../local_storage/manifest/{manifest_id}/clip/request/{clip_id}
        (the sync module uploads that clip to Blink's cloud; wait for the command)
   GET  same URL -> MP4 bytes -> saved to
        <folder>/<camera>/<YYYY-MM-DD>/<camera>_<HH-MM-SS>.mp4

Every step occupies the sync module, so the archiver:
* runs one clip at a time, with a pause between clips
* never runs while a live view is active, and stops at once if one starts
* remembers which clips it already saved, so they aren't fetched twice
* caps the number of clips per run
"""

from __future__ import annotations

import asyncio
from datetime import timedelta
import logging
from pathlib import Path
import re
import string
from typing import Any

from blinkpy import api as blink_api

from homeassistant.core import HomeAssistant
from homeassistant.helpers.storage import Store
from homeassistant.util import dt as dt_util

_LOGGER = logging.getLogger(__name__)

EVENT_CLIP_SAVED = "blink_plus_clip_saved"
STORE_VERSION = 1
PAUSE_BETWEEN_CLIPS = 3  # s, gives the sync module (and the Blink app) breathing room
MANIFEST_RETRIES = 6
DOWNLOAD_RETRIES = 3
DOWNLOAD_TIMEOUT = 120  # s per clip
MAX_REMEMBERED = 5000  # clip ids kept per sync module
MAX_FAILS_IN_A_ROW = 5  # then give up this run (and retry later automatically)
RESUME_AFTER_PAUSE = 120  # s, carry on after a live view interrupted the copy
RESUME_AFTER_ERROR = 300  # s
RESUME_AFTER_CAP = 30  # s, more clips waiting
MAX_AUTO_RESUMES = 12  # in a row without progress

CLIP_URL = string.Template(
    "/api/v1/accounts/$account_id/networks/$network_id/sync_modules/$sync_id"
    "/local_storage/manifest/$manifest_id/clip/request/$clip_id"
)


def _safe(name: str) -> str:
    return re.sub(r"[^\w\- ]+", "_", str(name)).strip() or "camera"


class ClipArchiver:
    """Copies new USB clips to a folder, on a schedule or on demand."""

    def __init__(self, hass: HomeAssistant, coordinator, entry_id: str, folder: str) -> None:
        """Initialize."""
        self.hass = hass
        self.coordinator = coordinator
        self.folder = folder.rstrip("/")
        self._store: Store[dict[str, Any]] = Store(
            hass, STORE_VERSION, f"blink_plus.{entry_id}.archive"
        )
        self._saved: dict[str, list[int]] = {}
        self._all: dict[str, Any] = {}
        self._initial_done = False  # first run into a folder copies everything
        self._lock = asyncio.Lock()
        self.status: dict[str, Any] = {
            "state": "idle",
            "last_run": None,
            "last_result": None,
            "last_clip": None,
            "last_clip_path": None,
            "last_clip_camera": None,
            "saved_last_run": 0,
            "saved_total": 0,
            "last_error": None,
            "next_auto_resume_s": None,
        }
        self.listeners: list = []
        self.enabled = True
        self._run_saved = 0
        self.usb_busy = False  # True while the sync module is uploading a clip for us
        self._clip_error = ""
        self._run_failed = 0
        self._resume_handle = None
        self._auto_resumes = 0

    @property
    def blink(self):
        """Return the blinkpy instance."""
        return self.coordinator.api

    async def async_load(self) -> None:
        """Load the clips already copied *to this folder*.

        The memory is kept per folder: pointing the archive at a new folder
        starts fresh, so everything in the look-back window is copied there.
        (0.3.0 kept one list for all folders; that list is left behind.)
        """
        data = await self._store.async_load() or {}
        self._all = dict(data.get("folders", {}))
        if "saved" in data and "folders" not in data:
            self._all["__0.3.0__"] = {"saved": data["saved"], "saved_total": 0}
        mine = self._all.get(self.folder, {})
        self._saved = {k: list(v) for k, v in mine.get("saved", {}).items()}
        self.status["saved_total"] = int(mine.get("saved_total", 0))
        self._initial_done = bool(mine.get("initial_done", False))

    async def _async_save_store(self) -> None:
        self._all[self.folder] = {
            "saved": {k: v[-MAX_REMEMBERED:] for k, v in self._saved.items()},
            "saved_total": self.status["saved_total"],
            "initial_done": self._initial_done,
        }
        await self._store.async_save({"folders": self._all})

    async def async_reset(self) -> None:
        """Forget what was copied to this folder (next run copies again)."""
        if self._lock.locked():
            raise RuntimeError("archive is running, try again when it's done")
        self.cancel_resume()
        self._saved = {}
        self._initial_done = False
        self.status.update(saved_total=0, last_clip=None, last_clip_path=None,
                           last_clip_camera=None, last_result="memory reset")
        await self._async_save_store()
        self._notify()

    def _notify(self) -> None:
        for listener in list(self.listeners):
            try:
                listener()
            except Exception:  # noqa: BLE001
                _LOGGER.debug("archive listener failed", exc_info=True)

    def _live_active(self) -> bool:
        return any(srv.active for srv in self.coordinator.live_servers.values())

    # ------------------------------------------------------------------ run
    async def async_run(self, hours: float = 24, max_clips: int = 25) -> dict[str, Any]:
        """Copy clips from the last `hours` that haven't been saved yet."""
        if not self.enabled:
            return {"result": "disabled", "error": self.status["last_error"]}
        if self._lock.locked():
            return {"result": "already running"}
        async with self._lock:
            self.status.update(state="running", last_error=None, saved_last_run=0)
            self._notify()
            result = "done"
            self._run_saved = 0
            self._run_failed = 0
            full_copy = not self._initial_done
            if full_copy:
                # First run into this folder: everything on the drive / in the
                # cloud, no look-back and no per-run cap.
                hours, max_clips = 0, 100_000
                self.status["state"] = "running (first full copy)"
                self._notify()
            try:
                notes = []
                cloud_found = await self._archive_cloud(hours, max_clips)
                if cloud_found is not None:
                    notes.append(f"cloud: {cloud_found} new")
                syncs = self._local_storage_syncs()
                if syncs and self._run_saved < max_clips:
                    if self._live_active():
                        notes.append("USB skipped: live view running")
                    else:
                        for sync in syncs:
                            await self._archive_sync(
                                sync, hours, max_clips - self._run_saved
                            )
                if cloud_found is None and not syncs:
                    raise RuntimeError(
                        "no clips source: no cloud clips (subscription) and no "
                        "Sync Module with active USB storage"
                    )
                if self._run_saved >= max_clips:
                    notes.append(f"stopped at {max_clips} clips, more next run")
                if full_copy:
                    notes.insert(0, "first full copy")
                    if self._run_failed:
                        notes.append(f"{self._run_failed} clip(s) to retry")
                    elif not any(n.startswith("USB skipped") for n in notes):
                        self._initial_done = True
                result = "done" + (f" ({'; '.join(notes)})" if notes else "")
            except _LiveViewStarted:
                result = "paused: a live view started"
            except Exception as err:  # noqa: BLE001
                _LOGGER.warning("Blink clip archive failed: %s", err, exc_info=True)
                self.status["last_error"] = str(err) or type(err).__name__
                result = "error"
            finally:
                saved = self._run_saved
                self.status.update(
                    state="idle",
                    last_run=dt_util.utcnow().isoformat(),
                    last_result=result,
                    saved_last_run=saved,
                )
                await self._async_save_store()
                self._notify()
            _LOGGER.info("Blink clip archive: %s, %d clip(s) saved", result, saved)
            self._schedule_resume(result, saved, hours, max_clips, full_copy)
            return {"result": result, "saved": saved}

    def _schedule_resume(self, result, saved, hours, max_clips, full_copy) -> None:
        """Carry on by itself after a pause, an error, or the per-run cap."""
        if result.startswith("paused"):
            delay = RESUME_AFTER_PAUSE
        elif result == "error":
            delay = RESUME_AFTER_ERROR
        elif "more next run" in result or (full_copy and not self._initial_done):
            delay = RESUME_AFTER_CAP
        else:
            self._auto_resumes = 0
            return
        self._auto_resumes = 0 if saved else self._auto_resumes + 1
        if self._auto_resumes > MAX_AUTO_RESUMES:
            _LOGGER.warning("Blink clip archive: giving up auto-resume (no progress)")
            self._auto_resumes = 0
            return
        self.cancel_resume()
        self.status["next_auto_resume_s"] = delay
        self._notify()

        async def _resume(_now=None) -> None:
            self._resume_handle = None
            self.status["next_auto_resume_s"] = None
            await self.async_run(hours=hours, max_clips=max_clips)

        from homeassistant.helpers.event import async_call_later  # noqa: PLC0415

        self._resume_handle = async_call_later(self.hass, delay, _resume)

    def cancel_resume(self) -> None:
        """Cancel a scheduled automatic resume (unload / reset)."""
        if self._resume_handle:
            self._resume_handle()
            self._resume_handle = None

    def _local_storage_syncs(self) -> list:
        syncs = []
        for sync in self.blink.sync.values():
            # Only real sync modules (not Minis/doorbells) with an active USB drive
            if getattr(sync, "sync_id", None) and getattr(sync, "local_storage", False):
                syncs.append(sync)
        return syncs

    async def _archive_cloud(self, hours: float, budget: int) -> int | None:
        """Copy cloud clips (subscription). Returns new clips found, None if none exist."""
        since = dt_util.utcnow() - timedelta(hours=hours) if hours else None
        stamp = (since or dt_util.parse_datetime("2015-01-01T00:00:00+00:00")).strftime(
            "%Y-%m-%dT%H:%M:%S%z"
        )
        base = f"{self.blink.urls.base_url}/api/v1/accounts/{self.blink.account_id}"
        items: list[dict[str, Any]] = []
        for page in range(1, 51):
            data = await blink_api.http_get(
                self.blink, f"{base}/media/changed?since={stamp}&page={page}"
            )
            media = data.get("media") if isinstance(data, dict) else None
            if not media:
                break
            items.extend(media)
        clips = [
            m for m in items
            if isinstance(m, dict) and m.get("media") and not m.get("deleted")
            and str(m.get("media")).split("?")[0].endswith(".mp4")
        ]
        if not clips:
            return None
        done = set(self._saved.get("cloud", []))
        todo = []
        for m in clips:
            try:
                cid = int(m["id"])
                created = dt_util.parse_datetime(str(m["created_at"]))
            except (KeyError, TypeError, ValueError):
                continue
            if cid in done or created is None:
                continue
            if created.tzinfo is None:
                created = created.replace(tzinfo=dt_util.UTC)
            todo.append((created, cid, m.get("device_name") or "camera", m["media"]))
        todo.sort()
        for created, cid, camera, media in todo[: max(budget - self._run_saved, 0)]:
            url = f"{self.blink.urls.base_url}{media}"
            try:
                path = await self._fetch_to_file(url, camera, created, cid)
            except Exception as err:  # noqa: BLE001
                self._clip_error = f"{type(err).__name__}: {err}"
                self.status["last_error"] = f"cloud clip {cid}: {self._clip_error}"
                path = None
            if path is not None:
                self._record_saved("cloud", cid, camera, created, path)
                await self._async_save_store()
                await asyncio.sleep(0.5)
        return len(todo)

    def _record_saved(self, key: str, cid: int, camera: str, created, path: Path) -> None:
        self._saved.setdefault(key, []).append(cid)
        self._run_saved += 1
        self.status.update(
            last_clip=created.isoformat(),
            last_clip_path=str(path),
            last_clip_camera=camera,
            saved_total=self.status["saved_total"] + 1,
        )
        self._notify()
        self.hass.bus.async_fire(
            EVENT_CLIP_SAVED,
            {"camera": camera, "path": str(path), "created_at": created.isoformat()},
        )

    async def _manifest(self, sync) -> tuple[Any, list[dict[str, Any]]]:
        base = self.blink.urls.base_url
        prefix = (
            f"{base}/api/v1/accounts/{self.blink.account_id}"
            f"/networks/{sync.network_id}/sync_modules/{sync.sync_id}"
            "/local_storage/manifest/request"
        )
        resp = await blink_api.http_post(self.blink, prefix)
        request_id = resp.get("id") if isinstance(resp, dict) else None
        if not request_id:
            raise RuntimeError(f"USB clip list request refused: {resp}")
        await blink_api.wait_for_command(self.blink, resp)
        for attempt in range(MANIFEST_RETRIES):
            data = await blink_api.http_get(self.blink, f"{prefix}/{request_id}")
            if isinstance(data, dict) and "clips" in data:
                return data.get("manifest_id"), data["clips"]
            await asyncio.sleep(3 * (attempt + 1))
        raise RuntimeError("the Sync Module didn't return the USB clip list")

    async def _archive_sync(self, sync, hours: float, budget: int) -> int:
        if budget <= 0:
            return 0
        self.usb_busy = True
        try:
            manifest_id, clips = await self._manifest(sync)
        finally:
            self.usb_busy = False
        names = getattr(sync, "_names_table", {}) or {}
        done = set(self._saved.get(str(sync.sync_id), []))
        cutoff = dt_util.utcnow() - timedelta(hours=hours) if hours else None

        todo = []
        for clip in clips:
            try:
                cid = int(clip["id"])
                created = dt_util.parse_datetime(str(clip["created_at"]))
            except (KeyError, TypeError, ValueError):
                continue
            if cid in done or created is None:
                continue
            if created.tzinfo is None:
                created = created.replace(tzinfo=dt_util.UTC)
            if cutoff and created < cutoff:
                continue
            camera = names.get(clip.get("camera_name"), clip.get("camera_name", "camera"))
            todo.append((created, cid, camera))
        todo.sort()  # oldest first
        _LOGGER.debug("%d new USB clip(s) to copy on %s", len(todo), sync.name)

        saved = 0
        fails = 0
        for created, cid, camera in todo[:budget]:
            if self._live_active():
                raise _LiveViewStarted
            try:
                path = await self._download(sync, manifest_id, cid, camera, created)
            except _LiveViewStarted:
                raise
            except Exception as err:  # noqa: BLE001  (one bad clip must not end the run)
                self._clip_error = f"{type(err).__name__}: {err}"
                path = None
            if path is None:
                fails += 1
                self._run_failed += 1
                _LOGGER.warning(
                    "Clip %s from %s not copied (%s), %d failed in a row",
                    cid, camera, self._clip_error, fails,
                )
                self.status["last_error"] = f"clip {cid}: {self._clip_error}"
                self._notify()
                if fails >= MAX_FAILS_IN_A_ROW:
                    raise RuntimeError(
                        f"{fails} clips in a row failed, last: {self._clip_error}"
                    )
                if fails == 2:
                    # Blink's clip list can expire during a long copy: get a new one.
                    _LOGGER.debug("Refreshing the USB clip list")
                    self.usb_busy = True
                    try:
                        manifest_id, _ = await self._manifest(sync)
                    finally:
                        self.usb_busy = False
                await asyncio.sleep(PAUSE_BETWEEN_CLIPS * 3)
                continue
            fails = 0
            saved += 1
            self._record_saved(str(sync.sync_id), cid, camera, created, path)
            await self._async_save_store()
            await asyncio.sleep(PAUSE_BETWEEN_CLIPS)
        return saved

    async def _download(self, sync, manifest_id, clip_id, camera, created) -> Path | None:
        url = self.blink.urls.base_url + CLIP_URL.substitute(
            account_id=self.blink.account_id,
            network_id=sync.network_id,
            sync_id=sync.sync_id,
            manifest_id=manifest_id,
            clip_id=clip_id,
        )
        # Ask the sync module to upload the clip, then wait for it.
        self.usb_busy = True
        try:
            resp = await blink_api.http_post(self.blink, url)
            await blink_api.wait_for_command(self.blink, resp)
        finally:
            self.usb_busy = False

        return await self._fetch_to_file(url, camera, created, clip_id)

    async def _fetch_to_file(self, url: str, camera: str, created, clip_id) -> Path | None:
        local = dt_util.as_local(created)
        cam = _safe(camera)
        folder = Path(self.folder) / cam / local.strftime("%Y-%m-%d")
        path = folder / f"{cam}_{local.strftime('%Y-%m-%d_%H-%M-%S')}.mp4"
        if await self.hass.async_add_executor_job(path.exists):
            path = folder / f"{cam}_{local.strftime('%Y-%m-%d_%H-%M-%S')}_{clip_id}.mp4"
        for attempt in range(DOWNLOAD_RETRIES):
            response = await blink_api.http_get(
                self.blink, url, json=False, timeout=DOWNLOAD_TIMEOUT
            )
            status = getattr(response, "status", None)
            if status == 200:
                data = await response.read()
                if data:
                    try:
                        await self.hass.async_add_executor_job(_write, path, data)
                    except OSError as err:
                        self._clip_error = f"can't write to {path.parent}: {err}"
                        raise
                    _LOGGER.debug("Saved %s (%d KB)", path, len(data) // 1024)
                    return path
                self._clip_error = "empty download"
            else:
                self._clip_error = (
                    f"download HTTP {status}" if status else "no response from Blink"
                )
            await asyncio.sleep(3 * (attempt + 1))
        _LOGGER.warning("Could not download clip %s from %s", clip_id, camera)
        return None


class _LiveViewStarted(Exception):
    """Stop archiving: someone opened a live view."""


def _write(path: Path, data: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(".part")
    tmp.write_bytes(data)
    tmp.replace(path)
