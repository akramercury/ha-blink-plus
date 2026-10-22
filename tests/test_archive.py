"""Clip archiver against a fake Blink API: names, de-duplication, look-back, live-view pause."""
import asyncio, importlib.util, os, sys, tempfile, types, datetime as dt
ARCHIVE_PY = sys.argv[1]
calls = []
NOW = dt.datetime.now(dt.timezone.utc)
CLIPS = [
    {"id": 101, "camera_name": "FrontDoor", "created_at": (NOW - dt.timedelta(hours=2)).isoformat(), "size": 1},
    {"id": 102, "camera_name": "Backyard", "created_at": (NOW - dt.timedelta(hours=1)).isoformat(), "size": 1},
    {"id": 99, "camera_name": "FrontDoor", "created_at": (NOW - dt.timedelta(days=3)).isoformat(), "size": 1},
]
state = {"live": False, "start_live_after": None}
CLOUD = []   # empty = no subscription (Blink returns an empty media list)

# ---- stubs: blinkpy.api + homeassistant bits ---------------------------------
api = types.ModuleType("blinkpy.api")
async def http_post(blink, url, **kw):
    calls.append(("POST", url.split("/api/v1/accounts/1")[-1]))
    if url.endswith("/manifest/request"):
        return {"id": 555, "network_id": 7}
    return {"id": 900, "network_id": 7}
async def http_get(blink, url, json=True, **kw):
    calls.append(("GET", url.split("/api/v1/accounts/1")[-1]))
    if "/media/changed" in url:
        page = int(url.rsplit("page=", 1)[1])
        return {"media": CLOUD if page == 1 else []}
    if url.endswith(".mp4"):
        class C:
            status = 200
            async def read(self): return b"CLOUD-" + url.encode()
        return C()
    if "/manifest/request/555" in url:
        return {"manifest_id": "M1", "clips": CLIPS}
    cid = int(url.rsplit("/", 1)[1])
    if state["start_live_after"] == cid:
        state["live"] = True
    class R:
        status = 200
        async def read(self): return b"MP4-" + str(cid).encode()
    return R()
async def wait_for_command(blink, resp): calls.append(("WAIT", resp.get("id"))); return True
api.http_post, api.http_get, api.wait_for_command = http_post, http_get, wait_for_command
bp = types.ModuleType("blinkpy"); bp.api = api; sys.modules["blinkpy"] = bp; sys.modules["blinkpy.api"] = api

ha = types.ModuleType("homeassistant"); core = types.ModuleType("homeassistant.core")
core.HomeAssistant = object
helpers = types.ModuleType("homeassistant.helpers"); storage = types.ModuleType("homeassistant.helpers.storage")
_DB = {}
class Store:
    def __init__(self, hass, v, key): self.key = key
    def __class_getitem__(cls, item): return cls
    async def async_load(self): return _DB.get(self.key)
    async def async_save(self, data): _DB[self.key] = data
storage.Store = Store
util = types.ModuleType("homeassistant.util"); dtu = types.ModuleType("homeassistant.util.dt")
dtu.UTC = dt.timezone.utc
dtu.utcnow = lambda: dt.datetime.now(dt.timezone.utc)
dtu.parse_datetime = lambda s: dt.datetime.fromisoformat(s)
dtu.as_local = lambda d: d.astimezone(dt.timezone(dt.timedelta(hours=-6)))
util.dt = dtu
for n, m in {"homeassistant": ha, "homeassistant.core": core, "homeassistant.helpers": helpers,
             "homeassistant.helpers.storage": storage, "homeassistant.util": util, "homeassistant.util.dt": dtu}.items():
    sys.modules[n] = m
spec = importlib.util.spec_from_file_location("archive", ARCHIVE_PY)
archive = importlib.util.module_from_spec(spec); sys.modules["archive"] = archive; spec.loader.exec_module(archive)
archive.PAUSE_BETWEEN_CLIPS = 0

class Bus:
    def __init__(self): self.events = []
    def async_fire(self, e, d): self.events.append((e, d))
class Hass:
    def __init__(self): self.bus = Bus()
    async def async_add_executor_job(self, fn, *a): return fn(*a)
class Srv:
    @property
    def active(self): return state["live"]
class Sync:
    name = "Home"; sync_id = 42; network_id = 7; local_storage = True
    _names_table = {"FrontDoor": "Front Door", "Backyard": "Backyard"}
class Owl:  # Mini without USB storage: must be ignored
    name = "Mini"; sync_id = None; network_id = 8; local_storage = False
class U: base_url = "https://rest-u1.immedia-semi.com"
class Blink: account_id = 1; urls = U(); sync = {"Home": Sync(), "Mini": Owl()}
class Coord: api = Blink(); live_servers = {"a": Srv()}

async def main():
    folder = tempfile.mkdtemp()
    hass = Hass()
    a = archive.ClipArchiver(hass, Coord(), "entry1", folder); await a.async_load()

    r1 = await a.async_run(hours=24)
    files = sorted(os.path.relpath(os.path.join(dp, f), folder) for dp, _, fs in os.walk(folder) for f in fs)
    print("run1:", r1, files)
    assert r1["saved"] == 2, r1
    assert len(files) == 2 and all(f.endswith(".mp4") for f in files), files
    assert any(f.startswith("Front Door/") for f in files) and any(f.startswith("Backyard/") for f in files)
    assert not any("99" in open(os.path.join(folder, f), "rb").read().decode() for f in files), "3-day-old clip copied"
    assert [e[1]["camera"] for e in hass.bus.events] == ["Front Door", "Backyard"], "not oldest-first / events missing"

    n_before = len(calls)
    r2 = await a.async_run(hours=24)
    clip_posts = [c for c in calls[n_before:] if c[0] == "POST" and "/clip/request/" in c[1]]
    print("run2:", r2, "clip uploads requested:", len(clip_posts))
    assert r2["saved"] == 0 and not clip_posts, "re-downloaded already saved clips"

    # remembered across restarts (Store)
    b = archive.ClipArchiver(hass, Coord(), "entry1", folder); await b.async_load()
    r3 = await b.async_run(hours=0)   # 0 = everything on the drive -> only the 3-day-old clip is new
    print("run3 (all clips, after restart):", r3)
    assert r3["saved"] == 1

    state["live"] = True
    r4 = await b.async_run(hours=0); print("live view running:", r4)
    assert "USB skipped" in r4["result"] and r4["saved"] == 0
    state["live"] = False

    CLIPS.extend([{"id": 201, "camera_name": "Backyard", "created_at": NOW.isoformat(), "size": 1},
                  {"id": 202, "camera_name": "Backyard", "created_at": (NOW + dt.timedelta(seconds=5)).isoformat(), "size": 1}])
    state["start_live_after"] = 201
    r5 = await b.async_run(hours=24); print("live view starts mid-run:", r5)
    assert r5["result"].startswith("paused") and r5["saved"] == 1
    print("status:", {k: b.status[k] for k in ("saved_total", "last_clip_camera", "last_result")})
    state["start_live_after"] = None

    # ---- with a subscription: cloud clips (+ USB). Cloud also works during live view.
    CLOUD.extend([
        {"id": 7001, "created_at": (NOW - dt.timedelta(minutes=30)).isoformat(), "device_name": "Driveway",
         "deleted": False, "media": "/api/v2/accounts/1/media/clip/7001.mp4"},
        {"id": 7002, "created_at": (NOW - dt.timedelta(minutes=20)).isoformat(), "device_name": "Driveway",
         "deleted": True, "media": "/api/v2/accounts/1/media/clip/7002.mp4"},
        {"id": 7003, "created_at": (NOW - dt.timedelta(minutes=10)).isoformat(), "device_name": "Front Door",
         "deleted": False, "media": "/api/v2/accounts/1/media/thumb/7003.jpg"},
    ])
    state["live"] = True
    r6 = await b.async_run(hours=24); print("subscribed, live view running:", r6)
    assert r6["saved"] == 1, "cloud clip not saved (or deleted/jpg copied)"
    assert "USB skipped" in r6["result"]
    state["live"] = False
    r7 = await b.async_run(hours=24); print("subscribed, idle:", r7)
    assert r7["saved"] == 1 and "cloud: 0 new" in r7["result"], "USB leftover not copied / cloud re-copied"
    files = sorted(os.path.relpath(os.path.join(dp, f), folder) for dp, _, fs in os.walk(folder) for f in fs)
    print("all files:", files)
    assert any(f.startswith("Driveway/") for f in files)
    assert not any(f.endswith(".part") for f in files)
    print("PASS archive")

asyncio.run(main())
