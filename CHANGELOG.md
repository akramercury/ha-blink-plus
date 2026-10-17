# Changelog

All notable changes to Blink Plus. The project follows [Semantic Versioning](https://semver.org/). It's pre-1.0, so options and behaviour may still change between minor versions.

## [0.2.0] - 2026-10-17
First public release.

### Added
- **Live view** for every Blink camera type: Outdoor/Indoor (sync module), Mini (owl) and Video Doorbell (lotus). It works in dashboards, Apple Home / Apple TV (HomeKit Bridge), go2rtc, Frigate and VLC.
- Built-in IMMIS client, reverse engineered from the Blink Android app 60.0:
  - v6 / v2 live view endpoints with the new `liveview_token`, plus an automatic fallback to the zero token
  - seamless `extended_liveview` hand-off when Blink's session time limit ends a session
  - ends sessions exactly like the app (IMMIS `STOP`, then closing the command), so the camera and sync module are released straight away
  - RTSPS fallback for firmware that hands out `rtsps://` URLs
- Local HTTP MPEG-TS feed per camera: `http://<host>:<port>/stream.ts`, with an optional fixed port range
- Its own OAuth v2 + PKCE login that handles Blink's 2026 changes: per-install UUID `hardware_id`, 2FA via HTTP 202 or 412, a separate cookie jar, OAuth v2 token refresh, and clear error messages (wrong password, wrong code, rate limited, failing step)
- Brand icon and logo (Home Assistant 2026.3+ shows them from the integration folder)
- Diagnostics with a log of the last 150 Blink API calls
- `blink_plus.stop_live_view` action
- Camera attributes: `live_view_state`, `live_view_last_error`, `live_view_cooldown_s`, `live_view_viewers`, `live_view_url`
- Options: listen address, base port, max minutes, linger, token mode, USB clip-list polling

### Sync module protection
- One live view per Blink system at a time. Opening another camera hands the sync module over, like the app does.
- Failed live views are never retried automatically: one attempt, a clean stop, then a 2-minute cool-down
- 60 s rest after the max-minutes limit, so a player that keeps reconnecting can't hold a session open
- No polling while a live view is running
- No `network/update` sync module command and no per-camera `signals` call on each poll (the same data comes from the cloud homescreen)
- No upload of every new USB clip to the cloud
- The USB clip list (Sync Module 2 local storage) is **not** read by default, because reading it gives "system busy" in the Blink app
- Setup finishes immediately; the first full refresh runs in the background, capped at 240 s

### Based on
- Home Assistant's built-in `blink` integration (Apache-2.0) and [blinkpy](https://github.com/fronzbot/blinkpy)

## 0.1.0 – 0.1.8 (private test builds, October 2026)
Development builds tested on a real setup: 2 battery doorbells, 2 outdoor cameras, Sync Module 2 with USB storage, no subscription.
